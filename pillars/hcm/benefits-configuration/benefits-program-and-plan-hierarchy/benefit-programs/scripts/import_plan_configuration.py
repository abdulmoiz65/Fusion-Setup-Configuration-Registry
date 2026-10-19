#!/usr/bin/env python3
"""Import a native Benefits plan ZIP with the existing Plan Copy REST engine."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
BENEFITS_DIR = SKILL_DIR.parent
REPOSITORY_ROOT = SKILL_DIR.parents[4]
ELIGIBILITY_SCRIPTS = (
    REPOSITORY_ROOT
    / "pillars"
    / "hcm"
    / "benefits-configuration"
    / "benefits-eligibility"
    / "eligibility-profiles"
    / "scripts"
)
TEMPLATES = {
    "401k": SKILL_DIR / "assets" / "plan-copy" / "Greenfield 401k Plan.zip",
    "commuter": SKILL_DIR / "assets" / "plan-copy" / "Greenfield Commuter Benefits Plan.zip",
}
DEFAULT_ZIP = TEMPLATES["401k"]
DEFAULT_OPENAPI = SKILL_DIR / "references" / "plan-copy.openapi.json"
DEFAULT_PROPERTIES = REPOSITORY_ROOT / "core" / "auth" / "fusionEnv.properties"
DEFAULT_TOKEN_CACHE = Path("auto")
PREVIEW_OBJECT_TYPES = (
    ("Plan", "Plan"),
    ("PlanType", "Plan Type"),
    ("Option", "Option"),
    ("YearPeriod", "Year Period"),
    ("EligibilityProfile", "Eligibility Profile"),
    ("BenefitsGroup", "Benefit Group"),
    ("AgeFactor", "Age Factor"),
)
DEFAULT_PREVIEW = Path.cwd() / "benefits-plan-copy-preview.json"


def _default_auth_path(default: Path, *override_variables: str) -> Path:
    """Use the repository OAuth default unless the caller configured an override."""
    for variable in override_variables:
        override = os.environ.get(variable)
        if override:
            return Path(override).expanduser()
    return default

for module_path in (SCRIPT_DIR, ELIGIBILITY_SCRIPTS):
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))

from types import ModuleType

plan_configuration_package = ModuleType('plan_configuration_package')
plan_configuration_package.__file__ = __file__
sys.modules['plan_configuration_package'] = plan_configuration_package
exec(compile(r'''
#!/usr/bin/env python3
"""Validate and inventory native Benefits Plan Copy export packages."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from typing import Any
import xml.etree.ElementTree as ET
import zipfile


MAX_OUTER_MEMBERS = 256
MAX_OUTER_UNCOMPRESSED_BYTES = 250 * 1024 * 1024
MAX_INNER_UNCOMPRESSED_BYTES = 100 * 1024 * 1024
REQUIRED_MEMBERS = {"MIGRATOR_PROPERTIES.xml", "checksum.txt"}
SUPPORT_OBJECT_TYPES = {"PlanCopyMap", "BenIntegrationKeyMap"}
CHECKSUM_PATTERN = re.compile(r"[0-9A-Fa-f]{128}")
REPORT_ROW_PATTERN = re.compile(r"^(.+?)\s+-\s+(\d+)\s*$")


class PackageValidationError(ValueError):
    """The supplied ZIP is not an internally consistent native plan package."""


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _safe_member_name(name: str, description: str) -> None:
    path = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or name.startswith("/")
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise PackageValidationError(f"Unsafe {description} member path: {name!r}.")


def _validate_infos(
    infos: list[zipfile.ZipInfo],
    *,
    description: str,
    maximum_members: int,
    maximum_uncompressed_bytes: int,
) -> None:
    if not infos:
        raise PackageValidationError(f"{description} must not be empty.")
    if len(infos) > maximum_members:
        raise PackageValidationError(
            f"{description} has {len(infos)} members; maximum is {maximum_members}."
        )
    names = [item.filename for item in infos]
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise PackageValidationError(
            f"{description} contains duplicate member(s): {', '.join(duplicates)}."
        )
    total_size = 0
    for info in infos:
        _safe_member_name(info.filename, description)
        if info.flag_bits & 0x1:
            raise PackageValidationError(
                f"{description} member is encrypted: {info.filename}."
            )
        mode = (info.external_attr >> 16) & 0o170000
        if mode == stat.S_IFLNK:
            raise PackageValidationError(
                f"{description} member must not be a symbolic link: {info.filename}."
            )
        total_size += info.file_size
    if total_size > maximum_uncompressed_bytes:
        raise PackageValidationError(
            f"{description} expands to {total_size} bytes; maximum is "
            f"{maximum_uncompressed_bytes}."
        )


def _open_zip(contents: bytes, description: str) -> zipfile.ZipFile:
    try:
        archive = zipfile.ZipFile(io.BytesIO(contents))
        bad_member = archive.testzip()
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise PackageValidationError(f"{description} is not a readable ZIP: {exc}.") from exc
    if bad_member is not None:
        archive.close()
        raise PackageValidationError(
            f"{description} failed its CRC check at {bad_member}."
        )
    return archive


def _direct_text(element: ET.Element, name: str) -> str:
    for child in list(element):
        if _local_name(child.tag) == name:
            return (child.text or "").strip()
    return ""


def _named_rows(root: ET.Element) -> list[ET.Element]:
    return [element for element in root.iter() if _direct_text(element, "ViewInstanceName")]


def _batch_sequence(contents: bytes) -> list[str]:
    try:
        root = ET.fromstring(contents)
    except ET.ParseError as exc:
        raise PackageValidationError(f"MIGRATOR_PROPERTIES.xml is malformed: {exc}.") from exc
    for element in root.iter():
        if _local_name(element.tag) != "void" or element.attrib.get("property") != "batchImportSequence":
            continue
        sequence = [
            (candidate.text or "").strip()
            for candidate in element.iter()
            if _local_name(candidate.tag) == "string" and (candidate.text or "").strip()
        ]
        if not sequence or len(sequence) != len(set(sequence)):
            raise PackageValidationError(
                "MIGRATOR_PROPERTIES.xml has an empty or duplicate batchImportSequence."
            )
        return sequence
    raise PackageValidationError(
        "MIGRATOR_PROPERTIES.xml has no batchImportSequence property."
    )


def _export_report(contents: bytes) -> dict[str, Any]:
    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise PackageValidationError("The Plan Copy export report is not UTF-8 text.") from exc

    def header(label: str) -> str:
        match = re.search(rf"^{re.escape(label)}\s*:\s*(.*?)\s*$", text, re.MULTILINE)
        return match.group(1).strip() if match else ""

    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = REPORT_ROW_PATTERN.match(line)
        if match:
            counts[match.group(1).strip()] = int(match.group(2))
    if not counts:
        raise PackageValidationError("The Plan Copy export report has no object inventory.")
    effective_date = header("Effective Date")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", effective_date):
        raise PackageValidationError(
            "The Plan Copy export report has no valid YYYY-MM-DD Effective Date."
        )
    return {
        "planCopyName": header("Plan Copy Name"),
        "planCopyObject": header("Plan Copy Object"),
        "effectiveDate": effective_date,
        "reportedObjectCounts": counts,
    }


def inspect_plan_package(contents: bytes) -> dict[str, Any]:
    """Validate a native plan export and return approval-safe inventory data."""
    if not contents:
        raise PackageValidationError("Plan Copy ZIP must not be empty.")
    archive_sha256 = hashlib.sha256(contents).hexdigest()
    outer = _open_zip(contents, "Plan Copy ZIP")
    try:
        infos = outer.infolist()
        _validate_infos(
            infos,
            description="Plan Copy ZIP",
            maximum_members=MAX_OUTER_MEMBERS,
            maximum_uncompressed_bytes=MAX_OUTER_UNCOMPRESSED_BYTES,
        )
        names = {info.filename for info in infos}
        missing = sorted(REQUIRED_MEMBERS - names)
        if missing:
            raise PackageValidationError(
                f"Plan Copy ZIP is missing required member(s): {', '.join(missing)}."
            )
        log_names = sorted(name for name in names if name.endswith(".log"))
        if len(log_names) != 1:
            raise PackageValidationError("Plan Copy ZIP must contain exactly one export .log file.")

        sequence = _batch_sequence(outer.read("MIGRATOR_PROPERTIES.xml"))
        expected_batches = [f"{name}/1_BATCH.zip" for name in sequence]
        actual_batches = sorted(name for name in names if name.endswith("/1_BATCH.zip"))
        if set(actual_batches) != set(expected_batches):
            missing_batches = sorted(set(expected_batches) - set(actual_batches))
            extra_batches = sorted(set(actual_batches) - set(expected_batches))
            raise PackageValidationError(
                "Batch layout does not match MIGRATOR_PROPERTIES.xml; "
                f"missing={missing_batches}, extra={extra_batches}."
            )
        extras = sorted(names - set(expected_batches) - REQUIRED_MEMBERS - set(log_names))
        if extras:
            raise PackageValidationError(
                f"Plan Copy ZIP has undeclared outer member(s): {', '.join(extras)}."
            )
        checksum = outer.read("checksum.txt").decode("ascii", errors="strict").strip()
        if not CHECKSUM_PATTERN.fullmatch(checksum):
            raise PackageValidationError("checksum.txt must contain one SHA-512-shaped value.")

        object_counts: Counter[str] = Counter()
        batches: list[dict[str, Any]] = []
        plan_names: list[str] = []
        for object_type in sequence:
            batch_name = f"{object_type}/1_BATCH.zip"
            inner = _open_zip(outer.read(batch_name), batch_name)
            try:
                inner_infos = inner.infolist()
                _validate_infos(
                    inner_infos,
                    description=batch_name,
                    maximum_members=8,
                    maximum_uncompressed_bytes=MAX_INNER_UNCOMPRESSED_BYTES,
                )
                xml_infos = [item for item in inner_infos if not item.is_dir()]
                if len(xml_infos) != 1 or not xml_infos[0].filename.endswith(".xml"):
                    raise PackageValidationError(
                        f"{batch_name} must contain exactly one XML member."
                    )
                try:
                    root = ET.fromstring(inner.read(xml_infos[0]))
                except ET.ParseError as exc:
                    raise PackageValidationError(
                        f"{batch_name}/{xml_infos[0].filename} is malformed XML: {exc}."
                    ) from exc
                rows = _named_rows(root)
                batch_counts = Counter(_direct_text(row, "ViewInstanceName") for row in rows)
                object_counts.update(batch_counts)
                if object_type == "Plan":
                    for row in rows:
                        if _direct_text(row, "ViewInstanceName") == "Plan":
                            name = _direct_text(row, "Name") or _direct_text(row, "PlanName")
                            if name and name not in plan_names:
                                plan_names.append(name)
                batches.append(
                    {
                        "objectType": object_type,
                        "member": batch_name,
                        "xmlMember": xml_infos[0].filename,
                        "xmlRoot": _local_name(root.tag),
                        "rowCount": sum(batch_counts.values()),
                    }
                )
            finally:
                inner.close()

        if object_counts.get("Plan", 0) < 1:
            raise PackageValidationError("Plan/1_BATCH.zip contains no Plan row.")
        program_objects = sorted(
            name for name, count in object_counts.items()
            if count > 0 and "program" in name.casefold()
        )
        if program_objects:
            raise PackageValidationError(
                "Program setup rows are not supported by this plan-only workflow: "
                + ", ".join(program_objects) + "."
            )
        report = _export_report(outer.read(log_names[0]))
        mismatches: list[dict[str, Any]] = []
        for object_type, reported in sorted(report["reportedObjectCounts"].items()):
            actual = object_counts.get(object_type, 0)
            if actual != reported:
                mismatches.append(
                    {"objectType": object_type, "reported": reported, "actual": actual}
                )

        for mismatch in mismatches:
            raise PackageValidationError(
                "Export-report inventory mismatch for "
                f"{mismatch['objectType']}: report={mismatch['reported']}, "
                f"package={mismatch['actual']}."
            )

        package_observed_counts = {
            key: count
            for key, count in sorted(object_counts.items())
            if key not in SUPPORT_OBJECT_TYPES
        }
        logged_counts = dict(sorted(report["reportedObjectCounts"].items()))
        return {
            "packageKind": "benefits-plan-configuration",
            "componentObjectType": "PLN",
            "archiveSha256": archive_sha256,
            "batchCount": len(batches),
            "nonEmptyBatchCount": sum(1 for item in batches if item["rowCount"] > 0),
            "setupObjectCount": sum(logged_counts.values()),
            "setupObjectTypeCount": len(logged_counts),
            "setupObjectCounts": logged_counts,
            "objectCountSource": log_names[0],
            "packageObservedObjectCount": sum(package_observed_counts.values()),
            "packageObservedObjectCounts": package_observed_counts,
            "planCount": object_counts["Plan"],
            "planNames": plan_names,
            "planCopyMappingCount": object_counts["PlanCopyMap"],
            "integrationKeyMappingCount": object_counts["BenIntegrationKeyMap"],
            "checksumManifestPresent": True,
            "exportReportName": log_names[0],
            "batches": batches,
            **report,
        }
    finally:
        outer.close()


def inspect_path(path: Path) -> tuple[Path, bytes, dict[str, Any]]:
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_file() or resolved.suffix.casefold() != ".zip":
            raise OSError
        contents = resolved.read_bytes()
    except OSError as exc:
        raise PackageValidationError(f"Plan Copy ZIP is unreadable: {path}.") from exc
    return resolved, contents, inspect_plan_package(contents)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--zip", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        resolved, _contents, summary = inspect_path(args.zip)
        print(json.dumps({"archivePath": str(resolved), **summary}, indent=2, sort_keys=True))
        return 0
    except PackageValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
''', __file__ + ":plan_configuration_package", "exec"), plan_configuration_package.__dict__)


from eligibility import plan_copy_import  # noqa: E402
from plan_object_report import build_object_report, render_markdown  # noqa: E402

USAGE = f"""Usage: {Path(sys.argv[0]).name} [Plan Copy options]

Imports an existing native Benefits plan ZIP through the Plan Copy REST API.
The default archive is:
  {DEFAULT_ZIP}

Preview (no Fusion write):
  --task-context FILE [--properties FILE] [--token-cache FILE]

Approved execution:
  --approve-upload --approval-preview FILE [same target/auth options]
  [--object-report-output FILE]

Report from already downloaded logs (read-only):
  report --zip FILE --import-log FILE --report-output FILE

Common overrides:
  --zip FILE --effective-date YYYY-MM-DD
  --import-name NAME --preview-output FILE

All live writes remain subject to the immutable-preview and exact approval
checks implemented by the existing eligibility Plan Copy REST engine.
"""


def _option_value(arguments: list[str], option: str) -> str | None:
    for argument in arguments:
        if argument.startswith(option + "="):
            return argument.split("=", 1)[1]
    try:
        index = arguments.index(option)
    except ValueError:
        return None
    if index + 1 >= len(arguments):
        raise SystemExit(f"ERROR: {option} requires a value.")
    return arguments[index + 1]


def _pop_option(arguments: list[str], option: str) -> str | None:
    value = _option_value(arguments, option)
    if value is None:
        return None
    for index, argument in enumerate(arguments):
        if argument == option:
            del arguments[index:index + 2]
            return value
        if argument.startswith(option + "="):
            del arguments[index]
            return value
    return value


def _write_object_report(path: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    """Persist parsed object rows, never the raw RequestLogs body."""
    path = path.expanduser().resolve()
    json_path = path.with_suffix(".json")
    if path == json_path or path.exists() or json_path.exists():
        raise OSError("Object report destination already exists; choose a new path.")
    if not path.parent.is_dir():
        raise OSError("Object report parent directory does not exist.")

    def write_atomic(destination: Path, contents: str) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix="." + destination.name + ".", delete=False,
        ) as stream:
            temp_path = Path(stream.name)
            stream.write(contents)
        try:
            os.replace(temp_path, destination)
        finally:
            temp_path.unlink(missing_ok=True)

    write_atomic(json_path, json.dumps(report, indent=2, sort_keys=True) + "\n")
    try:
        write_atomic(path, render_markdown(report))
    except OSError:
        json_path.unlink(missing_ok=True)
        raise
    return path, json_path


def _report_from_logs(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Compare Benefits plan export and import logs.")
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--import-log", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--import-status", default="UNKNOWN")
    args = parser.parse_args(arguments)
    try:
        _, _, summary = plan_configuration_package.inspect_path(args.zip)
        log_text = args.import_log.read_bytes().decode("utf-8-sig", errors="replace")
        if not log_text.strip():
            raise OSError("Import log is empty.")
        report = build_object_report(summary, log_text, import_status=args.import_status)
        report_path, json_path = _write_object_report(args.report_output, report)
    except (OSError, plan_configuration_package.PackageValidationError) as exc:
        print(f"ERROR [artifact persistence or input validation]: {exc}", file=sys.stderr)
        return 1
    print(render_markdown(report))
    print(f"Object report: {report_path}\nMachine report: {json_path}")
    return 0


def _current_plan_copy_name(arguments: list[str], fallback: str) -> str:
    preview_value = _option_value(arguments, "--approval-preview")
    if preview_value:
        try:
            payload = json.loads(Path(preview_value).expanduser().read_text(encoding="utf-8"))
            name = payload["preview"]["finalData"]["metadata"]["Name"]
            if isinstance(name, str) and name.strip():
                return name.strip()
        except (KeyError, OSError, TypeError, ValueError):
            pass
    return _option_value(arguments, "--import-name") or fallback


def _read_package(path: Path) -> tuple[Path, bytes, dict[str, Any]]:
    try:
        return plan_configuration_package.inspect_path(path)
    except plan_configuration_package.PackageValidationError as exc:
        raise plan_copy_import.PlanCopyImportError(
            "input validation", "archive-validation", str(exc)
        ) from exc


def _preview_object_counts(import_objects: dict[str, Any]) -> list[dict[str, Any]]:
    logged_counts = import_objects["setupObjectCounts"]
    return [
        {
            "objectType": object_type,
            "label": label,
            "count": logged_counts.get(object_type, 0),
        }
        for object_type, label in PREVIEW_OBJECT_TYPES
        if logged_counts.get(object_type, 0) > 0
    ]


def _print_plan_summary(import_objects: dict[str, Any], indent: str = "  ") -> None:
    print(f"{indent}Object counts from {import_objects['objectCountSource']}:")
    for item in _preview_object_counts(import_objects):
        print(f"{indent}  - {item['label']}: {item['count']}")


def _user_facing_result(
    result: dict[str, Any], *, plan_copy_name: str
) -> dict[str, Any]:
    displayed: dict[str, Any] = {
        "planCopyName": plan_copy_name,
        "status": result.get("mappingStatus") or "UNKNOWN",
    }
    if result.get("errorDetails"):
        displayed["errorDetails"] = result["errorDetails"]
    return displayed


def _print_plan_import_result(
    result: dict[str, Any], *, plan_copy_name: str
) -> None:
    displayed = _user_facing_result(result, plan_copy_name=plan_copy_name)
    print(json.dumps(displayed, indent=2, sort_keys=True))


def _print_plan_preview(
    *,
    output: Path,
    archive_path: Path,
    archive_contents: bytes,
    contract: Any,
    metadata: dict[str, str],
    import_objects: dict[str, Any],
) -> None:
    print(f"Approval preview: {output}")
    print(f"Target environment: {contract.base_url}")
    print(f"ZIP: {archive_path} ({len(archive_contents)} bytes)")
    print(f"SHA-256: {plan_copy_import._sha256(archive_contents)}")
    print(f"Plan Copy name: {metadata['Name']}")
    print(f"Effective date: {metadata['EffectiveDate']}")
    print("Objects to import:")
    _print_plan_summary(import_objects)
    print("No Fusion POST or PUT request was sent.")
    print("Reply exactly `approve` to authorize this immutable preview.")


def native_import_main(argv: list[str]) -> int:
    """Benefits plan-only adapter entry; retain the immutable approval gate."""
    parser = argparse.ArgumentParser(
        description="Native Benefits plan import (preview by default).",
        allow_abbrev=False,
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--template", choices=tuple(TEMPLATES))
    selection.add_argument("--zip", type=Path)
    parser.add_argument("--task-name", default="Benefit Programs", choices=["Benefit Programs"])
    parser.add_argument("--task-context", type=Path)
    parser.add_argument("--sequence", type=int, default=1)
    parser.add_argument("--approve-upload", action="store_true")
    parser.add_argument("--approval-preview", type=Path)
    args, _remaining = parser.parse_known_args(argv)
    try:
        forbidden = {"--openapi", "--workbook", "--resume-pl-copy-id", "--mapping-request-id"}
        if any(argument.split("=", 1)[0] in forbidden for argument in argv):
            raise ValueError("Use the maintained contract and unchanged plan ZIP; workbook and resume options are unsupported.")
        if args.approve_upload:
            if args.approval_preview is None:
                raise ValueError("--approval-preview is required for approved execution.")
            artifact = plan_copy_import._read_json_object(args.approval_preview, "Approval preview")
            task = plan_copy_import._preview_from_artifact(artifact)
        else:
            if args.task_context is None:
                raise ValueError("--task-context is required for the plan preview.")
            task = plan_copy_import.task_hook.resolve_task_rules_from_context(
                repository_root=REPOSITORY_ROOT,
                task_context_path=args.task_context.resolve(strict=True),
                task_name=args.task_name,
                sequence=args.sequence,
            )
        if task.get("taskCode") != "BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS":
            raise ValueError("This native plan route requires the Benefit Programs task and its own approval preview.")
        # main verifies the retained bytes, inventory, contract, target and Run
        # Book before any write. Approval never reruns task rules or lookups.
        return main([*argv, "--openapi", str(DEFAULT_OPENAPI)])
    except (OSError, ValueError, plan_copy_import.PlanCopyImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "report":
        return _report_from_logs(arguments[1:])
    if "--help" in arguments or "-h" in arguments:
        print(USAGE)
        print("Select --template {401k,commuter} (default: 401k), or --zip for a custom package.")
        return 0

    selector = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    selection = selector.add_mutually_exclusive_group()
    selection.add_argument("--template", choices=tuple(TEMPLATES))
    selection.add_argument("--zip")
    selected, arguments = selector.parse_known_args(arguments)
    report_value = _pop_option(arguments, "--object-report-output")
    approved = "--approve-upload" in arguments
    if report_value is not None and not approved:
        print("ERROR: --object-report-output requires --approve-upload.", file=sys.stderr)
        return 1
    preview_value = _option_value(arguments, "--approval-preview") if approved else None
    report_path = (
        Path(report_value) if report_value else
        Path(preview_value).with_suffix(".object-report.md") if preview_value else None
    )
    if report_path is not None:
        resolved_report = report_path.expanduser().resolve()
        if resolved_report.exists() or resolved_report.with_suffix(".json").exists():
            print("ERROR: Object report destination already exists; no import was started.", file=sys.stderr)
            return 1
        if not resolved_report.parent.is_dir():
            print("ERROR: Object report parent directory does not exist; no import was started.", file=sys.stderr)
            return 1
    zip_path = (Path(selected.zip).expanduser() if selected.zip
                else TEMPLATES[selected.template or "401k"])
    arguments.extend(("--zip", str(zip_path)))

    try:
        resolved, _contents, summary = plan_configuration_package.inspect_path(zip_path)
    except plan_configuration_package.PackageValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if _option_value(arguments, "--effective-date") is None and _option_value(
        arguments, "--workbook"
    ) is None:
        arguments.extend(("--effective-date", summary["effectiveDate"]))
    defaults = {
        "--openapi": str(DEFAULT_OPENAPI),
        "--properties": str(
            _default_auth_path(
                DEFAULT_PROPERTIES, "FUSION_PROPERTIES", "FUSION_OAUTH_PROPERTIES"
            )
        ),
        "--token-cache": str(
            _default_auth_path(DEFAULT_TOKEN_CACHE, "FUSION_TOKEN_CACHE")
        ),
        "--task-name": "Benefit Programs",
        "--operation-label": "Benefits plan configuration Plan Copy import",
        "--import-prefix": "BENEFITS_PLAN_",
        "--preview-output": str(DEFAULT_PREVIEW.with_name(
            zip_path.name + ".plan-copy-import-preview.json"
        )),
    }
    for option, value in defaults.items():
        if _option_value(arguments, option) is None:
            arguments.extend((option, value))

    plan_copy_import.TASK_CODE = "BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS"
    plan_copy_import.TASK_NAME = "Benefit Programs"
    plan_copy_import.COMPONENT_OBJECT_TYPE = "PLN"
    current_plan_copy_name = _current_plan_copy_name(
        arguments, fallback=summary["planCopyName"]
    )
    plan_copy_import._read_package = lambda _path: _read_package(resolved)
    plan_copy_import.print_import_object_summary = _print_plan_summary
    plan_copy_import._print_preview_result = _print_plan_preview
    final_result: dict[str, Any] = {}
    plan_copy_import._print_import_result = lambda result: final_result.update(result)
    captured_log: dict[str, Any] = {}
    original_log_reader = plan_copy_import._request_log_evidence

    def capture_log(*args: Any, **kwargs: Any) -> dict[str, Any]:
        evidence = original_log_reader(*args, **kwargs)
        captured_log.clear()
        captured_log.update(evidence)
        return evidence

    plan_copy_import._request_log_evidence = capture_log
    try:
        status = plan_copy_import.main(arguments)
    finally:
        plan_copy_import._request_log_evidence = original_log_reader
    if approved and status == 0 and (not captured_log or not final_result):
        print(
            "ERROR [artifact persistence]: Plan Copy returned success without "
            "the final result or RequestLogs needed for the object report; "
            "do not repeat the import.",
            file=sys.stderr,
        )
        return 1
    if approved and captured_log and report_path is not None:
        report = build_object_report(
            summary,
            captured_log["text"],
            import_status="SUCCESS" if status == 0 else "ERROR",
        )
        try:
            output, machine_output = _write_object_report(report_path, report)
        except OSError as exc:
            print(
                "ERROR [artifact persistence]: Plan Copy operation finished, "
                f"but the object report could not be saved: {exc}",
                file=sys.stderr,
            )
            return 1
        print(render_markdown(report))
        print(f"Object report: {output}\nMachine report: {machine_output}")
    if approved and status == 0:
        _print_plan_import_result(final_result, plan_copy_name=current_plan_copy_name)
    return status


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        raise SystemExit(plan_configuration_package.main(sys.argv[2:]))
    raise SystemExit(main())
