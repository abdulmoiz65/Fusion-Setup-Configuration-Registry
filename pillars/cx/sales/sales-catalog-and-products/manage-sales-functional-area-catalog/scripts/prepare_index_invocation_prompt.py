#!/usr/bin/env python3
"""Persist an immediate, non-executing Manage Sales Index invocation prompt."""

import argparse
import json
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
PROJECTS_ROOT = REPOSITORY_ROOT / "project"
RELATIVE = Path("artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-functional-area-catalog/current/index-invocation-prompt.json")


def nonblank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonblank text")
    return value.strip()


def safe_project_root(value: Path) -> Path:
    root = value.resolve(strict=True)
    if not root.is_dir() or root.parent != PROJECTS_ROOT.resolve() or value.is_symlink():
        raise ValueError("project-root must be an existing non-symlink project/{project_id} directory")
    return root


def safe_target(root: Path) -> Path:
    current = root
    for component in RELATIVE.parent.parts:
        current = current / component
        if current.exists() and current.is_symlink():
            raise ValueError("prompt parent must not contain symlinks")
        if not current.exists():
            current.mkdir()
        if not current.is_dir() or not current.resolve().is_relative_to(root):
            raise ValueError("prompt parent must remain inside project-root")
    return root / RELATIVE


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--import-reference", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--catalog-code")
    parser.add_argument("--replace-after-confirmation", action="store_true")
    args = parser.parse_args()
    root = safe_project_root(args.project_root)
    target = safe_target(root)
    if target.exists() and not args.replace_after_confirmation:
        raise ValueError("prompt already exists; require --replace-after-confirmation")
    prompt = {
        "schema_version": "1.0",
        "status": "catalog_assignment_import_accepted",
        "target_fusion_environment": nonblank(args.environment, "environment"),
        "import_reference": nonblank(args.import_reference, "import_reference"),
        "catalog_code": args.catalog_code.strip() if args.catalog_code and args.catalog_code.strip() else None,
        "message": "The Sales catalog-assignment import has started. You can now invoke Manage Sales Index for Item and/or Catalog indexing in the same Fusion environment. The catalog association has not yet been verified.",
        "next_action": "Invoke Manage Sales Index separately when indexing is desired; this prompt does not start it.",
    }
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
            json.dump(prompt, handle, indent=2)
            handle.write("\n")
            temporary = Path(handle.name)
        temporary.replace(target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(json.dumps({"status": prompt["status"], "prompt": str(RELATIVE)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
