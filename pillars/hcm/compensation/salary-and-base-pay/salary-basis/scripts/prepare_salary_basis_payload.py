"""Prepare a SalaryBasis DAT payload from validated resolver evidence.

This task-owned runbook helper performs no Fusion calls.  It fails closed unless
the input-value resolver supplied one exact match for the element and input
value represented in the SalaryBasis source.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
from typing import Any


REQUIRED_EVIDENCE_FIELDS = {
    "resolver": "resolve_salary_basis_input_value_id",
    "status": "passed",
    "classification": "resolved",
    "matchedRecords": 1,
}


def _non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Resolver evidence must contain a non-empty {label}.")
    return value.strip()


def _load_evidence(path: Path) -> dict[str, Any]:
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Resolver evidence must be valid JSON.") from exc
    if not isinstance(evidence, dict):
        raise ValueError("Resolver evidence must be a JSON object.")
    for field, expected in REQUIRED_EVIDENCE_FIELDS.items():
        if evidence.get(field) != expected:
            raise ValueError(
                f"Resolver evidence {field} must be {expected!r}; "
                "do not prepare a payload from incomplete or ambiguous evidence."
            )
    if not isinstance(evidence.get("requested"), dict):
        raise ValueError("Resolver evidence must include a requested object.")
    if not isinstance(evidence.get("values"), dict):
        raise ValueError("Resolver evidence must include a values object.")
    return evidence


def _parse_salary_basis_dat(content: str) -> tuple[list[str], list[str], str]:
    lines = content.splitlines()
    metadata = [line for line in lines if line.startswith("METADATA|SalaryBasis|")]
    merges = [line for line in lines if line.startswith("MERGE|SalaryBasis|")]
    if len(metadata) != 1 or len(merges) != 1:
        raise ValueError("Source must contain exactly one SalaryBasis METADATA and MERGE row.")
    header = metadata[0].split("|")[2:]
    values = merges[0].split("|")[2:]
    if len(header) != len(values):
        raise ValueError("SalaryBasis METADATA and MERGE column counts do not match.")
    if len(set(header)) != len(header):
        raise ValueError("SalaryBasis METADATA contains duplicate attribute names.")
    return header, values, "\r\n" if "\r\n" in content else "\n"


def _set_attribute(header: list[str], values: list[str], attribute: str, value: str) -> None:
    if attribute in header:
        values[header.index(attribute)] = value
        return
    insertion_index = header.index("InputValueName") + 1
    header.insert(insertion_index, attribute)
    values.insert(insertion_index, value)


def prepare_payload(source: Path, evidence_path: Path) -> str:
    content = source.read_text(encoding="utf-8")
    header, values, newline = _parse_salary_basis_dat(content)
    evidence = _load_evidence(evidence_path)
    fields = dict(zip(header, values, strict=True))

    element_name = _non_empty_string(fields.get("ElementName"), "ElementName in the source")
    input_value_name = fields.get("InputValueName", "").strip() or "Amount"
    requested = evidence["requested"]
    resolved = evidence["values"]
    if _non_empty_string(requested.get("elementName"), "requested.elementName") != element_name:
        raise ValueError("Resolver evidence elementName does not match the SalaryBasis source.")
    if _non_empty_string(requested.get("inputValueName"), "requested.inputValueName") != input_value_name:
        raise ValueError("Resolver evidence inputValueName does not match the SalaryBasis source.")
    if _non_empty_string(resolved.get("ElementName"), "values.ElementName") != element_name:
        raise ValueError("Resolved ElementName does not match the SalaryBasis source.")
    if _non_empty_string(resolved.get("InputValueName"), "values.InputValueName") != input_value_name:
        raise ValueError("Resolved InputValueName does not match the SalaryBasis source.")
    input_value_id = _non_empty_string(resolved.get("InputValueId"), "values.InputValueId")

    _set_attribute(header, values, "InputValueName", input_value_name)
    _set_attribute(header, values, "InputValueId", input_value_id)
    return (
        "METADATA|SalaryBasis|" + "|".join(header) + newline
        + "MERGE|SalaryBasis|" + "|".join(values) + newline
    )


def _write_atomically(output: Path, content: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent, prefix=f".{output.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, output)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="SalaryBasis DAT source")
    parser.add_argument("--resolver-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Prepared DAT output")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("--output must be different from --source to preserve the reviewed source.")
    try:
        prepared = prepare_payload(args.source, args.resolver_evidence)
        _write_atomically(args.output, prepared)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
