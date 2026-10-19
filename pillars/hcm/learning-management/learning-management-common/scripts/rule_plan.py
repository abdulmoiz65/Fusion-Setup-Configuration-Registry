#!/usr/bin/env python3
"""Read and validate a Learning task's shipped rule registry, without Fusion I/O."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


class AuthoringIncomplete(ValueError):
    """A selected task has unresolved rule nodes."""


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def tables(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    heading = ""
    index = 0
    while index < len(lines):
        if lines[index].startswith("#"):
            heading = lines[index]
        if lines[index].startswith("|") and index + 1 < len(lines) and lines[index + 1].startswith("|"):
            headers = [part.strip() for part in lines[index].strip("|").split("|")]
            row = index + 2
            while row < len(lines) and lines[row].startswith("|"):
                values = [part.strip() for part in lines[row].strip("|").split("|")]
                if len(values) != len(headers):
                    raise ValueError(f"column mismatch in {path}:{row + 1}")
                yield heading, dict(zip(headers, values)), row + 1
                row += 1
            index = row
            continue
        index += 1


def _metadata(path: Path, key: str) -> str:
    match = re.search(rf'(?m)^{re.escape(key)}:\s*["\']?([^"\'\n]+)', path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"missing {key} in {path}")
    return match.group(1).strip()


class TARGET:
    @staticmethod
    def resolve_target(area: Path, selector: str) -> dict:
        slug = slugify(selector)
        flat = area / f"{slug}.md"
        nested = area / slug / "SKILL.md"
        if flat.is_file() == nested.is_file():
            return {"status": "ambiguous", "reason": "Expected exactly one task representation"}
        selected = nested if nested.is_file() else flat
        return {"status": "resolved", "representation": "nested" if nested.is_file() else "flat",
                "representation_artifact": str(selected),
                "target_resource_folder": str(selected.parent / "ora-resource" if nested.is_file() else area / "ora-resource")}


def compile_task(area: Path, selector: str) -> tuple[dict, dict]:
    area = Path(area)
    target = TARGET.resolve_target(area, selector)
    if target["status"] != "resolved":
        raise ValueError(target["reason"])
    resource = Path(target["target_resource_folder"])
    metadata = Path(target["representation_artifact"])
    code = _metadata(metadata, "task_code")
    name = _metadata(metadata, "task_name")
    registry = json.loads((resource / "ora_rule_registry.json").read_text(encoding="utf-8"))
    if registry.get("representation") != target["representation"]:
        raise ValueError("Task representation does not match the registry")
    matching = [task for task in registry.get("tasks", []) if task.get("task_code") == code]
    if len(matching) != 1 or matching[0].get("task_name") != name:
        raise ValueError("Task identity does not match the registry")
    task = matching[0]
    nodes = task.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("Task has no rule nodes")
    by_id = {node["id"]: node for node in nodes}
    if len(by_id) != len(nodes) or task.get("start_node") not in by_id:
        raise ValueError("Task graph has duplicate nodes or no start node")
    for node in nodes:
        source = node.get("source", {})
        filename, line = source.get("file"), source.get("line")
        if not isinstance(filename, str) or not filename.startswith("ora_") or not filename.endswith(".md"):
            raise ValueError(f"Invalid source for {node['id']}")
        path = (resource / filename).resolve(strict=True)
        if path.parent != resource.resolve() or not isinstance(line, int):
            raise ValueError(f"Unsafe source for {node['id']}")
        rows = [row for _, row, row_number in tables(path) if row_number == line]
        if len(rows) != 1 or rows[0].get("Rule ID") != node["id"]:
            raise ValueError(f"Stale source anchor for {node['id']}")
        row = rows[0]
        if target["representation"] == "flat" and (row.get("Task Code"), row.get("Task Name")) != (code, name):
            raise ValueError(f"Source row belongs to another task: {node['id']}")
        transitions = {} if row.get("Transitions", "none").lower() == "none" else dict(
            part.strip().split("->", 1) for part in row["Transitions"].split(";")
        )
        prerequisites = [] if row.get("Prerequisites", "none").lower() == "none" else [
            part.strip() for part in row["Prerequisites"].split(",")
        ]
        if (row.get("Node Type") != node.get("node_type")
                or row.get("Sequence") != str(node.get("sequence"))
                or row.get("Action Type") != node.get("action_type")
                or transitions != node.get("transitions")
                or prerequisites != node.get("prerequisites")
                or row.get("On Failure") != node.get("on_failure")
                or row.get("Applies When") != node.get("applies_when")):
            raise ValueError(f"Stale rule row for {node['id']}")
        if set(node.get("transitions", {}).values()) - by_id.keys() or set(node.get("prerequisites", [])) - by_id.keys():
            raise ValueError(f"Broken graph edge for {node['id']}")
    return target, task


def build_plan(area: Path, selector: str, registry_path: Path | None = None) -> dict:
    target, task = compile_task(area, selector)
    if registry_path is not None and Path(registry_path).resolve() != (Path(target["target_resource_folder"]) / "ora_rule_registry.json").resolve():
        raise ValueError("Requested registry does not match the selected task")
    readiness = task.get("readiness", {})
    if readiness.get("status") != "ready" or readiness.get("blocking_reasons"):
        reasons = readiness.get("blocking_reasons", [])
        details = "; ".join(f"{item.get('file', '')}: {item.get('column', '')}: {item.get('message', '')}" for item in reasons)
        raise AuthoringIncomplete(details or "Task graph is incomplete")
    return {"representation": target["representation"], "task": task,
            "execution_guide": "pillars/hcm/learning-management/learning-management-common/references/task-node-execution.md",
            "validation": {"status": "ready", "override_scope": None, "warning": None,
                           "task_specific_approval_required": True}}


def catalog():
    actions = {key: {} for key in ("validate_input", "resolve_dependency", "reference_lookup", "apply_default",
                                  "design_enforcement", "error_handler", "execution_gate", "evaluate_result", "terminal")}
    return actions, {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pillar-skill-path", required=True, type=Path)
    parser.add_argument("--setup-task", required=True)
    args = parser.parse_args()
    try:
        plan = build_plan(args.pillar_skill_path, args.setup_task)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "blocked", "message": str(error)}))
        return 2
    print(json.dumps({"status": "planned", "plan": plan, "node_count": len(plan["task"]["nodes"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
