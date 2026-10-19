"""Offline checks for compiled nested v3 task rules; never compile or execute rules."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import argparse
CURRENT_ACTION_TYPES = {"validate_input", "resolve_dependency", "reference_lookup", "apply_default", "design_enforcement", "error_handler", "execution_gate", "evaluate_result", "terminal"}
class TaskRuleContractError(ValueError):
    """Invalid Expenses task planning contract."""


GUIDE = "pillars/erp/financials/expenses/references/task-rule-execution.md"
NODE_COLUMNS = {"Rule ID", "Node Type", "Sequence", "Action Type", "Transitions",
                "Prerequisites", "On Failure", "Applies When"}
RESOURCE_FILES = {f"ora_{name}.md" for name in (
    "input_validation", "dependency_readiness", "reference_lookups",
    "defaulting_rules", "design_enforcement", "error_handling")}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise TaskRuleContractError("The compiled registry has duplicate JSON keys.")
        result[key] = value
    return result


def _inside_file(path: Path, parent: Path) -> Path:
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(parent.resolve(strict=True)) or not resolved.is_file():
        raise TaskRuleContractError("Rule planning requires files inside the selected scope.")
    return resolved


def _rows(path: Path):
    """Read the existing task-node table format, retaining its heading and line."""
    heading = ""
    headers = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            heading = line.lstrip("#").strip().lower().replace(" ", "-")
        if not line.startswith("|"):
            headers = None
            continue
        values = [value.strip() for value in line.strip().strip("|").split("|")]
        if NODE_COLUMNS <= set(values):
            headers = values
        elif headers is not None:
            if all(re.fullmatch(r":?-+:?", value) for value in values):
                continue
            if len(values) != len(headers):
                raise TaskRuleContractError(f"Malformed task-node row in {path.name}:{number}.")
            yield heading, number, dict(zip(headers, values))


def _check_source(node: dict, rows: dict) -> None:
    source = node.get("source", {})
    matches = [entry for entry in rows.get(source.get("file"), [])
               if entry[2]["Rule ID"] == node["id"]]
    if len(matches) != 1:
        raise TaskRuleContractError(f"Rule {node['id']} must have exactly one owning source row.")
    anchor, line, row = matches[0]
    if source.get("anchor") != anchor or source.get("line") != line:
        raise TaskRuleContractError(f"Rule {node['id']} has a stale source anchor or line.")
    expected = {
        "Rule ID": node["id"], "Node Type": node.get("node_type"),
        "Sequence": str(node["sequence"]), "Action Type": node["action_type"],
        "On Failure": node.get("on_failure"), "Applies When": node.get("applies_when"),
    }
    if any(row[key] != value for key, value in expected.items()):
        raise TaskRuleContractError(f"Rule {node['id']} disagrees with its owning source row.")
    prerequisites = [] if row["Prerequisites"].lower() == "none" else [
        value.strip() for value in row["Prerequisites"].split(",")]
    transitions = {}
    if row["Transitions"].lower() != "none":
        for item in row["Transitions"].split(";"):
            pair = item.strip().split("->")
            if len(pair) != 2 or not all(pair) or pair[0] in transitions:
                raise TaskRuleContractError(f"Rule {node['id']} has malformed source transitions.")
            transitions[pair[0]] = pair[1]
    if prerequisites != node["prerequisites"] or transitions != node.get("transitions"):
        raise TaskRuleContractError(f"Rule {node['id']} has stale prerequisites or transitions.")
    if any(re.search(r"\bTBD\b", value, re.I) for value in row.values()):
        raise TaskRuleContractError(f"Rule {node['id']} has an incomplete source contract.")


def _check_graph(task: dict, rows: dict) -> None:
    nodes = task["nodes"]
    by_id = {node["id"]: node for node in nodes}
    start = task.get("start_node")
    if not isinstance(start, str) or start not in by_id or by_id[start]["prerequisites"]:
        raise TaskRuleContractError("The rule graph needs a valid start without prerequisites.")
    sequences = set()
    terminals = set()
    for node in nodes:
        identifier = node["id"]
        if node["sequence"] in sequences or node["action_type"] not in CURRENT_ACTION_TYPES:
            raise TaskRuleContractError(f"Rule {identifier} has a duplicate sequence or unsupported action.")
        sequences.add(node["sequence"])
        readiness = node.get("readiness")
        if (not isinstance(readiness, dict) or readiness.get("status") != "ready"
                or readiness.get("blocking_reasons") != []):
            raise TaskRuleContractError(f"Rule {identifier} is not ready.")
        transitions = node.get("transitions")
        if not isinstance(transitions, dict) or not all(
            isinstance(outcome, str) and outcome and isinstance(target, str) and target in by_id and by_id[target]["sequence"] > node["sequence"]
            for outcome, target in transitions.items()
        ):
            raise TaskRuleContractError(f"Rule {identifier} has invalid transition targets.")
        if any(target not in by_id or by_id[target]["sequence"] >= node["sequence"] for target in node["prerequisites"]):
            raise TaskRuleContractError(f"Rule {identifier} has invalid prerequisites.")
        terminal = node.get("node_type") == "terminal"
        if (terminal != (node["action_type"] == "terminal")
                or (terminal and transitions) or (not terminal and not transitions)
                or node.get("node_type") not in ("step", "decision", "terminal")
                or node.get("execution_route") not in ("local", "fusion-rest")):
            raise TaskRuleContractError(f"Rule {identifier} has an invalid node contract.")
        if terminal:
            terminals.add(identifier)
        _check_source(node, rows)
    reachable, pending = set(), [start]
    while pending:
        current = pending.pop()
        if current not in reachable:
            reachable.add(current)
            pending.extend(by_id[current]["transitions"].values())
    if reachable != set(by_id):
        raise TaskRuleContractError("The rule graph contains unreachable nodes.")
    visited, active = set(), set()

    def visit(identifier):
        if identifier in active:
            raise TaskRuleContractError("The rule graph has cyclic prerequisites.")
        if identifier not in visited:
            active.add(identifier)
            for prerequisite in by_id[identifier]["prerequisites"]:
                visit(prerequisite)
            active.remove(identifier)
            visited.add(identifier)

    for identifier in by_id:
        visit(identifier)
    can_finish = set(terminals)
    while True:
        previous = set(can_finish)
        can_finish.update(node["id"] for node in nodes
                          if any(target in can_finish for target in node["transitions"].values()))
        if previous == can_finish:
            break
    if can_finish != set(by_id):
        raise TaskRuleContractError("Every rule must have a declared path to a terminal.")


def plan_task_rules(repository_root: Path, skill_path: Path, task_name: str, task_code: str) -> dict:
    """Plan one explicitly selected nested v3 task without context, auth, or writes."""
    root = repository_root.resolve(strict=True)
    supplied = skill_path if skill_path.is_absolute() else root / skill_path
    manifest = supplied if supplied.name == "SKILL.md" else supplied / "SKILL.md"
    manifest = _inside_file(manifest, root / "pillars")
    frontmatter = manifest.read_text(encoding="utf-8").split("---", 2)
    if len(frontmatter) != 3 or frontmatter[0].strip():
        raise TaskRuleContractError("The nested task needs a manifest with frontmatter.")
    for key, expected in (("task_name", task_name), ("task_code", task_code)):
        # These generated identity scalars have no YAML interpolation or multiline form.
        values = re.findall(rf"^{key}:\s*([^\n]+)$", frontmatter[1], re.M)
        if len(values) != 1 or values[0].strip().strip('"\'') != expected:
            raise TaskRuleContractError(f"The requested {key} must match the nested manifest exactly.")
    resources = (manifest.parent / "ora-resource").resolve(strict=True)
    if not resources.is_relative_to(manifest.parent):
        raise TaskRuleContractError("Rule resources must remain inside the task package.")
    registry_path = _inside_file(resources / "ora_rule_registry.json", resources)
    registry = json.loads(registry_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    if not isinstance(registry, dict) or registry.get("schema_version") != "3.0" or registry.get("representation") != "nested":
        raise TaskRuleContractError("Offline planning supports compiled nested v3 registries only.")
    tasks = registry.get("tasks")
    if (not isinstance(tasks, list) or len(tasks) != 1 or not isinstance(tasks[0], dict)
            or tasks[0].get("task_name") != task_name or tasks[0].get("task_code") != task_code):
        raise TaskRuleContractError("A nested registry must identify exactly the selected task.")
    task = tasks[0]
    if task.get("readiness") != {"status": "ready", "blocking_reasons": []}:
        raise TaskRuleContractError("Task readiness is not ready.")
    nodes = task.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise TaskRuleContractError("Missing rule nodes.")
    identifiers = set()
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"] or node["id"] in identifiers:
            raise TaskRuleContractError("Invalid or duplicate node identity.")
        identifiers.add(node["id"])
        if type(node.get("sequence")) is not int or node["sequence"] <= 0:
            raise TaskRuleContractError("Invalid node sequence.")
        if not isinstance(node.get("source"), dict) or not isinstance(node["source"].get("file"), str):
            raise TaskRuleContractError("Invalid node source.")
        if not isinstance(node.get("prerequisites"), list) or not all(isinstance(p, str) for p in node["prerequisites"]):
            raise TaskRuleContractError("Invalid prerequisites.")
    files = [manifest, registry_path]
    rows = {}
    source_names = {node["source"]["file"] for node in task["nodes"]}
    source_names.update(RESOURCE_FILES)
    source_names.update(path.name for path in resources.glob("ora_*.md"))
    for name in source_names:
        if not re.fullmatch(r"ora_[a-z_]+\.md", name):
            raise TaskRuleContractError("Rule source must be a task-local ora-resource Markdown file.")
        path = _inside_file(resources / name, resources)
        rows[name] = list(_rows(path))
        files.append(path)
    if {row["Rule ID"] for entries in rows.values() for _, _, row in entries} != {
        node["id"] for node in task["nodes"]
    }:
        raise TaskRuleContractError("The registry and source task-node inventory disagree.")
    _check_graph(task, rows)
    _inside_file(root / GUIDE, root)
    return {
        "status": "planned", "node_count": len(task["nodes"]),
        "plan": {"representation": "nested", "execution_guide": GUIDE,
                 "validation": {"status": "ready", "override_scope": None,
                                "task_specific_approval_required": True}, "task": task},
        "sourceDigests": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sorted(files)},
        "live_checks_performed": False,
        "nextAction": "Read execution_guide and owning rules; continue the selected task workflow. "
                      "Planning is not runtime validation, target qualification, or import approval.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--task-code", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[5]
    try:
        selected = args.skill_path if args.skill_path.is_absolute() else root / args.skill_path
        if not selected.resolve().is_relative_to(root / "pillars/erp/financials/expenses"):
            raise TaskRuleContractError("Select an Expenses task.")
        print(json.dumps(plan_task_rules(root, selected, args.task_name, args.task_code), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "error", "failure_class": "input_validation", "message": str(exc)}))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
