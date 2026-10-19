#!/usr/bin/env python3
"""Validate Party Hierarchy Generation inputs and build an ESS request payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


CONTRACT_VERSION = 7
APPLICATION = "CrmEss"
JOB_DEFINITION_ID = (
    "JobDefinition://oracle/apps/ess/cdm/foundation/parties/"
    "HzPartyHierarchyFlattenedDataGenJob"
)
CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")
PARAM_TYPE = "STRING"

HIERARCHY_TYPE_TRANSPORT_VALUES = {
    "CUSTOMER": "HZ_CUSTOMER_HIERARCHY",
    "DUNS_AND_BRADSTREET": "HZ_DNB_HIERARCHY",
    "PARTNER": "HZ_PARTNER_HIERARCHY",
    "TRADING_COMMUNITY_PARTY": "HZ_PARTY_HIERARCHY",
}

FLATTENING_METHOD_TRANSPORT_VALUES = {
    "INCREMENTAL": "INCREMENTAL_FLATTENING",
    "FORCE": "FORCE_FLATTENING",
}

HIERARCHY_TYPE_ALIASES = {
    "CUSTOMER": "CUSTOMER",
    "CUSTOMER HIERARCHY": "CUSTOMER",
    "CUSTOMER_HIERARCHY": "CUSTOMER",
    "D&B": "DUNS_AND_BRADSTREET",
    "DUN AND BRADSTREET": "DUNS_AND_BRADSTREET",
    "DUN AND BRADSTREET HIERARCHY": "DUNS_AND_BRADSTREET",
    "DUNS AND BRADSTREET": "DUNS_AND_BRADSTREET",
    "DUNS AND BRADSTREET HIERARCHY": "DUNS_AND_BRADSTREET",
    "DUNS_AND_BRADSTREET": "DUNS_AND_BRADSTREET",
    "PARTNER": "PARTNER",
    "PARTNER HIERARCHY": "PARTNER",
    "PARTNER HIERARCHIES": "PARTNER",
    "PARTNER_HIERARCHY": "PARTNER",
    "TRADING COMMUNITY PARTY": "TRADING_COMMUNITY_PARTY",
    "TRADING COMMUNITY PARTY HIERARCHY": "TRADING_COMMUNITY_PARTY",
    "TRADING_COMMUNITY_PARTY": "TRADING_COMMUNITY_PARTY",
}

FLATTENING_METHOD_ALIASES = {
    "INCREMENTAL": "INCREMENTAL",
    "INCREMENTAL FLATTENING": "INCREMENTAL",
    "INCREMENTAL_FLATTENING": "INCREMENTAL",
    "FORCE": "FORCE",
    "FORCE FLATTENING": "FORCE",
    "FORCE_FLATTENING": "FORCE",
    "FULL MODE": "FORCE",
    "FULL FLATTENING": "FORCE",
}

JOB_FIELDS = {
    "hierarchy_type",
    "hierarchy_name",
    "hierarchy_version",
    "flattening_method",
}
CONTROL_FIELDS = {
    "all_hierarchies_explicit",
    "force_flattening_explicit",
}
ALLOWED_FIELDS = JOB_FIELDS | CONTROL_FIELDS


class ContractError(ValueError):
    """Raised when canonical parameters do not satisfy the preview contract."""


def _text(value: Any, field: str, *, required: bool = False) -> str | None:
    if value is None:
        if required:
            raise ContractError(f"Missing required field: {field}")
        return None
    if isinstance(value, bool) or isinstance(value, (dict, list)):
        raise ContractError(f"{field} must be a scalar text value")
    normalized = str(value).strip()
    if not normalized:
        if required:
            raise ContractError(f"Missing required field: {field}")
        return None
    if CONTROL_CHARACTERS.search(normalized):
        raise ContractError(f"{field} must not contain control characters")
    return normalized


def _flag(value: Any, field: str) -> bool:
    if value is None:
        return False
    if not isinstance(value, bool):
        raise ContractError(f"{field} must be true or false")
    return value


def _enumeration(
    value: Any,
    field: str,
    aliases: dict[str, str],
) -> str:
    normalized = _text(value, field, required=True)
    assert normalized is not None
    key = re.sub(r"\s+", " ", normalized.upper())
    if key not in aliases:
        accepted = sorted(set(aliases.values()))
        raise ContractError(f"{field} must be one of: {', '.join(accepted)}")
    return aliases[key]


def normalize_parameters(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ContractError("Canonical parameters must be a JSON object")

    unknown = sorted(set(raw) - ALLOWED_FIELDS)
    if unknown:
        raise ContractError(f"Unsupported canonical field(s): {', '.join(unknown)}")

    normalized_job_parameters = {
        "hierarchy_type": _enumeration(
            raw.get("hierarchy_type"),
            "hierarchy_type",
            HIERARCHY_TYPE_ALIASES,
        ),
        "hierarchy_name": _text(raw.get("hierarchy_name"), "hierarchy_name"),
        "hierarchy_version": _text(
            raw.get("hierarchy_version"), "hierarchy_version"
        ),
        "flattening_method": _enumeration(
            raw.get("flattening_method"),
            "flattening_method",
            FLATTENING_METHOD_ALIASES,
        ),
    }
    return {
        "job_parameters": normalized_job_parameters,
        "authorization_context": {
            "all_hierarchies_explicit": _flag(
                raw.get("all_hierarchies_explicit"),
                "all_hierarchies_explicit",
            ),
            "force_flattening_explicit": _flag(
                raw.get("force_flattening_explicit"),
                "force_flattening_explicit",
            ),
        },
    }


def build_document(
    raw: dict[str, Any], description: str | None = None
) -> dict[str, Any]:
    normalized = normalize_parameters(raw)
    job = normalized["job_parameters"]
    authorization = normalized["authorization_context"]

    warnings: list[str] = []
    approval_required = False

    if job["hierarchy_name"] is None:
        warnings.append(
            "No hierarchy name is specified; null removes the name filter and the "
            "resulting broad scope must be explicitly confirmed."
        )
        if not authorization["all_hierarchies_explicit"]:
            approval_required = True

    if job["flattening_method"] == "FORCE":
        warnings.append(
            "Force Flattening was selected; make the full reflattening method explicit "
            "in the execution preview."
        )
        if not authorization["force_flattening_explicit"]:
            approval_required = True

    hierarchy_type_transport = HIERARCHY_TYPE_TRANSPORT_VALUES.get(
        job["hierarchy_type"]
    )
    flattening_method_transport = FLATTENING_METHOD_TRANSPORT_VALUES.get(
        job["flattening_method"]
    )
    hierarchy_version_transport = job["hierarchy_version"]

    blocking_gaps: list[str] = []
    if hierarchy_type_transport is None:
        blocking_gaps.append(
            f"No source-verified argument1 transport value exists for hierarchy type {job['hierarchy_type']}."
        )
    if flattening_method_transport is None:
        blocking_gaps.append(
            f"No source-verified argument4 transport value exists for flattening method {job['flattening_method']}."
        )
    argument_contract = [
        {
            "name": "submit.argument1",
            "business_field": "hierarchy_type",
            "param_type": PARAM_TYPE,
            "value": hierarchy_type_transport,
        },
        {
            "name": "submit.argument2",
            "business_field": "hierarchy_name",
            "param_type": PARAM_TYPE,
            "value": job["hierarchy_name"],
        },
        {
            "name": "submit.argument3",
            "business_field": "hierarchy_version",
            "param_type": PARAM_TYPE,
            "value": hierarchy_version_transport,
        },
        {
            "name": "submit.argument4",
            "business_field": "flattening_method",
            "param_type": PARAM_TYPE,
            "value": flattening_method_transport,
        },
    ]

    payload: dict[str, Any] | None = None
    if not blocking_gaps:
        request_parameters: list[dict[str, str]] = []
        for argument in argument_contract:
            parameter = {
                "name": str(argument["name"]),
                "paramType": str(argument["param_type"]),
            }
            if argument["value"] is not None:
                parameter["value"] = str(argument["value"])
            request_parameters.append(parameter)
        payload = {
            "application": APPLICATION,
            "jobDefinitionId": JOB_DEFINITION_ID,
            "retries": 0,
            "requestParameters": request_parameters,
        }
        normalized_description = _text(description, "description")
        if normalized_description is not None:
            payload["description"] = normalized_description

    document = {
        "contract_version": CONTRACT_VERSION,
        "normalized_job_parameters": job,
        "verified_ess_identity": {
            "application": APPLICATION,
            "job_definition_id": JOB_DEFINITION_ID,
        },
        "verified_argument_contract": argument_contract,
        "optional_parameter_transport": {
            "hierarchy_name": job["hierarchy_name"],
            "hierarchy_version": hierarchy_version_transport,
        },
        "verified_success_evidence": {
            "source": "Developer-provided Scheduled Processes UI evidence",
            "status": "Succeeded",
        },
        "execution_safety_policy": {
            "retries": 0,
            "automatic_resubmission": False,
            "submission_mode": "submit once, checkpoint requestId, then poll separately",
        },
        "authorization_context": authorization,
        "documented_defaults": {
            "hierarchy_type": "CUSTOMER",
            "flattening_method": "INCREMENTAL",
        },
        "warnings": warnings,
        "approval_required": approval_required,
        "consolidated_confirmation_effects": {
            "authorizes_all_hierarchies_when_name_omitted": job["hierarchy_name"] is None,
            "authorizes_force_impact_when_selected": job["flattening_method"] == "FORCE",
            "authorizes_single_submission": True,
        },
        "live_execution_ready": payload is not None and not approval_required,
        "blocking_gaps": blocking_gaps,
    }
    if payload is not None:
        document["ess_request_payload"] = payload
    return document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a guarded Party Hierarchy Generation preview and, for the "
            "documented hierarchy types and flattening methods, an ESS request payload."
        )
    )
    parser.add_argument("--input", required=True, help="Canonical parameter JSON file.")
    parser.add_argument(
        "--description",
        help="Optional non-sensitive correlation description added to the ESS payload.",
    )
    parser.add_argument(
        "--payload-output",
        help="Write only the executable ESS request payload to this file.",
    )
    parser.add_argument(
        "--report-output",
        help="Write the normalized preview and contract-gap report to this file.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing report after explicit approval.",
    )
    return parser.parse_args()


def _validate_output_paths(args: argparse.Namespace) -> None:
    input_path = Path(args.input).resolve()
    output_paths = [
        Path(value).resolve()
        for value in (args.payload_output, args.report_output)
        if value is not None
    ]
    if input_path in output_paths:
        raise ContractError("An output path must not replace the canonical input file")
    if len(output_paths) != len(set(output_paths)):
        raise ContractError("payload_output and report_output must use different paths")
    if not args.force:
        existing = [str(path) for path in output_paths if path.exists()]
        if existing:
            raise ContractError(
                "Output already exists; use a new path or approved --force: "
                + ", ".join(existing)
            )


def main() -> int:
    args = parse_args()
    try:
        _validate_output_paths(args)
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        document = build_document(raw, args.description)
        rendered = json.dumps(document, indent=2, sort_keys=False) + "\n"
        if args.payload_output:
            payload = document.get("ess_request_payload")
            if payload is None:
                raise ContractError(
                    "Executable payload is unavailable: "
                    + "; ".join(document["blocking_gaps"])
                )
            Path(args.payload_output).write_text(
                json.dumps(payload, indent=2, sort_keys=False) + "\n",
                encoding="utf-8",
            )
        if args.report_output:
            Path(args.report_output).write_text(rendered, encoding="utf-8")
        if not args.report_output:
            sys.stdout.write(rendered)
        return 0
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"Party hierarchy request validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
