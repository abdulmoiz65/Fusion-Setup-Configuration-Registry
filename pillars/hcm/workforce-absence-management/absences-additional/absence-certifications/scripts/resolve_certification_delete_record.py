#!/usr/bin/env python3
"""Assemble dated certification deletion from declared configuration and complete History reads.

Offline validation only: no browser, Fusion call or deletion approval.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sys

from hashlib import sha256
from urllib.parse import urlsplit

RESOLVER = "resolve_absence_certification_delete_record_from_history"


def fingerprint(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Declared read timestamps must be strings")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Read timestamps require a timezone")
    return parsed


def origin(value):
    if not isinstance(value, str):
        raise ValueError("Declared environment must be a URL string")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Declared reads require a valid HTTPS environment")
    return parsed.scheme, parsed.hostname.lower(), parsed.port or 443

FIELDS = ("AbsenceCertificationId", "EffectiveStartDate", "EffectiveEndDate")


def iso(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError("Selected row and History require stored ISO dates")
    return value


def validate_protection(saved, meanings):
    if not isinstance(saved.get("Name"), str) or not saved["Name"].strip():
        raise ValueError("Delete Record needs the exact resolved certification Name")
    result = {}
    for field, label in (("ClassificationCode", "Classification"), ("LegislationCode", "Legislation"),
                         ("ManagementTypeCode", "Management")):
        value = meanings.get(field)
        if (not isinstance(value, dict) or value.get("code") != saved.get(field)
                or not isinstance(value.get("meaning"), str) or not value["meaning"].strip()):
            raise ValueError("Delete Record requires a resolved display meaning for " + label)
        result[label] = value["meaning"]
    if result["Management"] != "User-defined":
        raise ValueError("Delete Record cannot maintain a predefined certification")
    if result["Classification"] not in {"Documentation", "Entitlement"}:
        raise ValueError("Delete Record requires a reviewed Redwood certification classification")
    return result


def validate_history(saved, history):
    if not isinstance(history, list) or len(history) < 2 or any(not isinstance(h, dict) for h in history):
        raise ValueError("Certification Delete Record requires a complete multi-row History")
    ranges = sorted((iso(h.get("EffectiveStartDate")), iso(h.get("EffectiveEndDate"))) for h in history)
    if (len({start for start, _ in ranges}) != len(ranges) or any(start > end for start, end in ranges)
            or any((date.fromisoformat(ranges[i][0]) - date.fromisoformat(ranges[i-1][1])).days != 1
                   for i in range(1, len(ranges)))):
        raise ValueError("Certification Delete Record History must contain unique contiguous ranges")
    selected = (iso(saved.get("EffectiveStartDate")), iso(saved.get("EffectiveEndDate")))
    if selected not in ranges or ranges.index(selected) == 0:
        raise ValueError("Certification Delete Record must preserve an earlier row; first-row deletion is unavailable")


def validate_evidence(evidence, saved, meanings):
    if evidence.get("resolver") != RESOLVER or evidence.get("source") != "configuration-and-history":
        raise ValueError("Delete Record requires the declared History resolver output")
    validate_protection(saved, meanings)
    reads = evidence.get("historyRead")
    if not isinstance(reads, dict):
        raise ValueError("Delete Record requires complete bound configuration and History reads")
    resolved = resolve_context(reads)["deleteRecordEvidence"]
    if (evidence != resolved or fingerprint(saved) != evidence.get("beforeStateSha256")
            or reads["configuration"]["meanings"] != meanings):
        raise ValueError("Delete Record evidence must bind the exact configuration and complete History")


def resolve_context(bundle):
    expected = bundle["readContext"]
    configuration, history = bundle["configuration"], bundle["history"]
    if not expected.get("principal") or not expected.get("runId"):
        raise ValueError("Declared reads require the authenticated principal and current run")
    for packet in (configuration, history):
        if not isinstance(packet, dict) or packet.get("complete") is not True:
            raise ValueError("Delete Record needs complete declared configuration and History reads")
        if (origin(packet.get("baseUrl")) != origin(expected.get("baseUrl"))
                or any(packet.get(f) != expected.get(f) for f in ("principal", "runId"))
                or not timestamp(expected.get("runStartedAt")) <= timestamp(packet.get("retrievedAt")) <= datetime.now(timezone.utc)):
            raise ValueError("Delete Record read environment, principal, run or retrieval time differs")
    saved, meanings = configuration["record"], configuration["meanings"]
    identity = saved.get("AbsenceCertificationId")
    if not isinstance(identity, str) or not re.fullmatch(r"[1-9][0-9]*", identity):
        raise ValueError("Delete Record needs the exact resolved certification identity")
    if history.get("AbsenceCertificationId") != identity:
        raise ValueError("Delete Record History belongs to another certification")
    validate_history(saved, history.get("rows"))
    for row in history["rows"]:
        if row.get("AbsenceCertificationId", identity) != identity:
            raise ValueError("Delete Record History row belongs to another certification")
    validate_protection(saved, meanings)
    evidence = {**{f: saved[f] for f in FIELDS}, "resolver": RESOLVER,
                "source": "configuration-and-history", "action": "Delete Record",
                "historyComplete": True, "history": deepcopy(history["rows"]),
                "adapterContract": "DELETE_CHANGES_PHYSICAL_ROW",
                "historyRead": deepcopy({k: bundle[k] for k in ("readContext", "configuration", "history")}),
                "beforeStateSha256": fingerprint(saved), "historySha256": fingerprint(history["rows"])}
    return {"beforeState": deepcopy(saved), "meanings": deepcopy(meanings), "deleteRecordEvidence": evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Declared current read bundle")
    parser.add_argument("--contract", required=True, type=Path, help="Current registered Data Loader metadata")
    parser.add_argument("--output", required=True, type=Path, help="New resolved intent JSON; no overwrite")
    args = parser.parse_args()
    try:
        source_scripts = Path(__file__).resolve().parents[3] / "absence" / "scripts"
        if str(source_scripts) not in sys.path:
            sys.path.insert(0, str(source_scripts))
        from absence_source_io import load_contract
        from prepare_absence_source import build_model
        schema = load_contract(args.contract)
        if schema.discriminator != "absenceCertifications":
            raise ValueError("Delete Record requires the absenceCertifications contract")
        context = resolve_context(json.loads(args.input.read_text()))
        saved = context["beforeState"]
        intent = {"businessObject": "absenceCertifications", "records": [{"operation": "delete-changes",
                  "effectiveStartDate": saved["EffectiveStartDate"],
                  "values": {"AbsenceCertificationId": saved["AbsenceCertificationId"]}, "uiContext": context}]}
        build_model(schema, intent)  # Reuse the owning current-template and operation validator.
        with args.output.open("x") as stream:
            stream.write(json.dumps(intent, indent=2) + "\n")
        print(json.dumps({"status": "resolved_not_approved", "resolver": RESOLVER,
                          "output": str(args.output), "externalMutationSubmitted": False}))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "blocked", "stage": "delete-record-evidence-binding",
                          "failure_class": getattr(exc, "failure_class", "input_validation"), "message": str(exc),
                          "recommended_action": "Refresh the declared selected configuration and complete History reads; do not submit"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
