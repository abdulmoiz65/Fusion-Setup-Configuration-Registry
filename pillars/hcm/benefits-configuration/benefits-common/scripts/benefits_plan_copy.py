#!/usr/bin/env python3
"""Benefits-owned native Plan Copy adapters in the Benefits Common area.

Ordinary ZIP validation remains DAT-only. This route delegates native archive,
OpenAPI, task, target, and immutable approval validation to the maintained
Benefits adapter; it never repackages a Plan Copy archive as HDL or sends it
to UCM/initiateDataLoad.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SKILL_ROOT = REPOSITORY_ROOT / "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles"
TASK_CODE = "BEN_MANAGE_ELIGIBILITY_PROFILES"
PLAN_SKILL_ROOT = REPOSITORY_ROOT / "pillars/hcm/benefits-configuration/benefits-program-and-plan-hierarchy/benefit-programs"


def load_plan_adapter():
    spec = importlib.util.spec_from_file_location(
        "benefits_native_plan_adapter", PLAN_SKILL_ROOT / "scripts/import_plan_configuration.py"
    )
    if spec is None or spec.loader is None:
        raise ValueError("The maintained Benefits plan adapter is unavailable.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_adapter():
    spec = importlib.util.spec_from_file_location(
        "benefits_native_eligibility_adapter", SKILL_ROOT / "scripts/eligibility.py"
    )
    if spec is None or spec.loader is None:
        raise ValueError("The maintained Benefits Plan Copy adapter is unavailable.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.plan_copy_import


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    # Contract selection belongs to this route, never to a caller-supplied file.
    if any(arg == "--openapi" or arg.startswith("--openapi=") for arg in arguments):
        print("ERROR: This route uses the maintained Plan Copy OpenAPI contract.", file=sys.stderr)
        return 1
    if arguments and arguments[0] == "plan":
        return load_plan_adapter().native_import_main(arguments[1:])
    adapter = load_adapter()
    args = adapter.parse_args([
        *arguments, "--openapi", str(SKILL_ROOT / "references/plan-copy.openapi.json")
    ])
    try:
        if args.workbook is not None or args.resume_pl_copy_id is not None:
            raise ValueError("Use an already generated ZIP and explicit effective date; workbook regeneration and resume are not supported by this route.")
        if not args.effective_date:
            raise ValueError("An explicit --effective-date is required and remains approval-bound.")
        if args.task_name != "Eligibility Profiles":
            raise ValueError("This native route supports only Eligibility Profiles.")
        if args.approve_upload:
            artifact = adapter._read_json_object(args.approval_preview, "Approval preview")
            preview = adapter._preview_from_artifact(artifact)
            if preview.get("taskCode") != TASK_CODE:
                raise ValueError("The approved preview is not for Eligibility Profiles.")
        else:
            plan = adapter.task_hook.resolve_task_rules_from_context(
                repository_root=REPOSITORY_ROOT,
                task_context_path=args.task_context.resolve(strict=True),
                task_name=args.task_name,
                sequence=args.sequence,
            )
            if plan.get("taskCode") != TASK_CODE:
                raise ValueError("The selected task is not Eligibility Profiles.")
        # _run validates archive and contract before Task Hook preview. Approved
        # execution checks the retained bytes, target and Run Book binding, and
        # never regenerates the workbook or repeats reference lookups.
        return adapter._run(args)
    except (OSError, ValueError, adapter.PlanCopyImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
