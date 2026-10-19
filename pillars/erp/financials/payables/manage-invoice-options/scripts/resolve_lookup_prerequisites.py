#!/usr/bin/env python3
"""Resolve Invoice Options lookup-code prerequisites through Financials REST.

This is a live, read-only preflight that runs before ``fsm_task_adapter.py
normalize``.  The adapter remains deliberately offline: this helper adds the
normalized prerequisite receipt that the adapter validates.

If the caller cannot use a supporting lookup resource (for example, HTTP
401/403), or the resource returns multiple records, the helper records an
explicit advisory ``validation_skipped`` receipt and leaves Fusion import as
the authority. A readable zero-result is conclusive: it blocks candidate
creation. Create-time BU/ledger derivation is the exception because it
supplies required CSV values.

Reading guide: URL helpers create the supported read-only queries, resolver
functions add receipts to a copy of the design, and ``main`` writes that
resolved design. No helper in this file performs a Fusion write.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any


TASK_ROOT = Path(__file__).resolve().parents[1]


def _repository_root() -> Path:
    for candidate in (TASK_ROOT, *TASK_ROOT.parents):
        if (candidate / "core" / "data-loader" / "scripts" / "data_loader_metadata.py").is_file():
            return candidate
    raise RuntimeError("Could not locate the FSCR repository root.")


REPOSITORY_ROOT = _repository_root()
DATA_LOADER_SCRIPTS = REPOSITORY_ROOT / "core" / "data-loader" / "scripts"
if str(DATA_LOADER_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(DATA_LOADER_SCRIPTS))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import data_loader_metadata as metadata  # noqa: E402
from fsm_task_adapter import (  # noqa: E402
    CURRENCY_RECEIPT_CONTRACTS,
    LOOKUP_RECEIPT_CONTRACTS,
    PAYMENT_TERM_RECEIPT_FIELDS,
    SYSTEM_LOOKUP_CODES,
)


PAYMENT_TERMS_PATH = "/fscmRestApi/resources/11.13.18.05/payablesPaymentTerms"
CURRENCIES_PATH = "/fscmRestApi/resources/11.13.18.05/currenciesLOV"
BUSINESS_UNITS_PATH = "/fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV"
LEDGERS_PATH = "/fscmRestApi/resources/11.13.18.05/ledgersLOV"
ADVISORY_UNAVAILABLE_STATUSES = frozenset({400, 401, 403, 408, 429})


class LookupPreflightError(Exception):
    """A readable lookup result cannot support the requested design."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LookupPreflightError(f"Cannot read design JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LookupPreflightError("Design JSON must contain one object.")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_advisory_unavailable(error: metadata.DataLoadError) -> bool:
    """Return true only for unavailable/authentication read preflight states."""
    status = error.http_status
    return status is None or status in ADVISORY_UNAVAILABLE_STATUSES or status >= 500


# These functions build requests only. HTTP execution is delegated to the
# central Data Loader client so authentication stays outside this task script.
def _payment_term_url(host: str, name: str) -> str:
    return host + PAYMENT_TERMS_PATH + "?" + urllib.parse.urlencode(
        {"onlyData": "true", "fields": "name,termsId", "q": f"name='{name}'"}
    )


def _currency_url(host: str, code: str) -> str:
    return host + CURRENCIES_PATH + "?" + urllib.parse.urlencode(
        {"finder": f"CurrencyCodeAllRowsFinder;CurrencyCode={code}"}
    )


def _business_unit_url(host: str, name: str) -> str:
    return host + BUSINESS_UNITS_PATH + "?" + urllib.parse.urlencode({
        "onlyData": "true", "fields": "BusinessUnitId,BusinessUnitName,ActiveFlag,PrimaryLedgerId",
        "q": f"BusinessUnitName='{name}'",
    })


def _ledger_url(host: str, ledger_id: object) -> str:
    return host + LEDGERS_PATH + "/" + urllib.parse.quote(str(ledger_id)) + "?" + urllib.parse.urlencode(
        {"onlyData": "true", "fields": "LedgerId,Name,CurrencyCode"}
    )


def _items(response: Any) -> list[dict[str, Any]]:
    if not isinstance(response, dict):
        raise LookupPreflightError("Lookup response must be a JSON object.")
    values = response.get("items")
    if not isinstance(values, list):
        raise LookupPreflightError("Lookup response does not contain an items array.")
    return [item for item in values if isinstance(item, dict)]


def _upsert_prerequisite(design: dict[str, Any], prerequisite: dict[str, Any]) -> None:
    existing = design.get("prerequisites", [])
    if not isinstance(existing, list):
        raise LookupPreflightError("Design prerequisites must be an array.")
    identity = tuple(prerequisite[key] for key in ("entity", "field", "resolver"))
    design["prerequisites"] = [
        item
        for item in existing
        if not (
            isinstance(item, dict)
            and tuple(item.get(key) for key in ("entity", "field", "resolver")) == identity
        )
    ] + [prerequisite]


def _append_warning(design: dict[str, Any], warning: str) -> None:
    warnings = design.setdefault("warnings", [])
    if not isinstance(warnings, list):
        raise LookupPreflightError("Design warnings must be an array.")
    if warning not in warnings:
        warnings.append(warning)


def _append_resolver_contract_issue(
    design: dict[str, Any], *, operation_id: str, field: str, resolver: str,
    endpoint: str, requested_value: str, error: metadata.DataLoadError,
) -> None:
    """Record a sanitized maintainer finding for an HTTP 400 preflight failure."""
    findings = design.setdefault("resolverFindings", [])
    if not isinstance(findings, list):
        raise LookupPreflightError("Design resolverFindings must be an array.")
    finding = {
        "classification": "resolver_contract_issue",
        "severity": "maintenance_required",
        "owner": "skill_maintainer",
        "actionRequired": "fix_or_reverify",
        "operationId": str(operation_id),
        "field": field,
        "resolver": resolver,
        "endpoint": endpoint,
        "httpStatus": 400,
        "requestedValue": requested_value,
        "querySha256": hashlib.sha256((endpoint + requested_value).encode("utf-8")).hexdigest(),
        "observedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "diagnostic": {"message": error.message},
    }
    if finding not in findings:
        findings.append(finding)


def _unavailable_receipt(
    design: dict[str, Any], *, entity: str, field: str, resolver: str,
    evidence: dict[str, Any], summary: dict[str, int],
) -> None:
    _upsert_prerequisite(design, {
        "entity": entity, "field": field, "resolver": resolver,
        "status": "validation_skipped", "evidence": {
            **evidence, "availability": "unavailable",
            "preflightPolicy": "advisory_on_unavailable",
        },
    })
    _append_warning(
        design,
        f"Read-only validation skipped for {field}; its Financials endpoint was unavailable. Fusion import remains authoritative.",
    )
    summary["validationSkipped"] += 1


def _multiple_results_receipt(
    design: dict[str, Any], *, entity: str, field: str, resolver: str,
    evidence: dict[str, Any], summary: dict[str, int],
) -> None:
    """Preserve an ambiguous readable response for authoritative FSM validation."""
    _upsert_prerequisite(design, {
        "entity": entity, "field": field, "resolver": resolver,
        "status": "validation_skipped", "evidence": {
            **evidence, "availability": "multiple_results",
            "preflightPolicy": "advisory_on_multiple_results",
        },
    })
    _append_warning(
        design,
        f"Read-only validation returned multiple records for {field}; preserving the submitted value for authoritative Fusion import validation.",
    )
    summary["validationSkipped"] += 1


def resolve_lookup_prerequisites(
    design: dict[str, Any], config: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, int]]:
    """Return a design augmented with live or advisory lookup receipts."""
    resolved = copy.deepcopy(design)
    operations = resolved.get("operations")
    if not isinstance(operations, list) or not operations:
        raise LookupPreflightError("Design must contain a nonempty operations array.")

    summary = {"satisfied": 0, "validationSkipped": 0}
    for operation in operations:
        if not isinstance(operation, dict):
            raise LookupPreflightError("Each operation must be an object.")
        entity = operation.get("entity")
        values = operation.get("values")
        operation_id = operation.get("id", "<unnamed>")
        if not isinstance(entity, str) or not entity.strip() or not isinstance(values, dict):
            raise LookupPreflightError(
                f"Operation {operation_id} must contain entity and values objects."
            )
        for field, (resolver, lookup_type, allow_blank) in LOOKUP_RECEIPT_CONTRACTS.items():
            if field not in values:
                continue
            code = str(values[field]).strip()
            if allow_blank and not code:
                continue
            if not code:
                raise LookupPreflightError(
                    f"Operation {operation_id} supplies a blank required lookup code for {field}."
                )
            allowed_codes = SYSTEM_LOOKUP_CODES.get(lookup_type)
            if allowed_codes is not None:
                if code not in allowed_codes:
                    raise LookupPreflightError(
                        f"Operation {operation_id} {field} must use one of the supported "
                        f"system {lookup_type} codes: {', '.join(sorted(allowed_codes))}."
                    )
                summary["satisfied"] += 1
                continue
        # Live preflight portion of `resolve_business_unit_by_name_and_enterprise`:
        # resolve the active requested business unit and its primary ledger.
        # EnterpriseId resolution is completed locally by the task adapter.
        if operation.get("action", "update") == "create" and entity == "AP_SYSTEM_PARAMETER":
            target = operation.get("targetKey")
            bu_name = target.get("BuName") if isinstance(target, dict) else None
            if not isinstance(bu_name, str) or not bu_name.strip():
                raise LookupPreflightError(f"Operation {operation_id} create requires targetKey.BuName.")
            try:
                bu_rows = _items(metadata.get_json(
                    _business_unit_url(config["host"], bu_name), config["auth"],
                    stage="resolve invoice-options business unit",
                ))
                matches = [item for item in bu_rows if item.get("BusinessUnitName") == bu_name and item.get("ActiveFlag") is True]
                primary_ledger_ids = {str(item.get("PrimaryLedgerId", "")).strip() for item in matches}
                if not matches or "" in primary_ledger_ids or len(primary_ledger_ids) != 1:
                    raise LookupPreflightError(f"Operation {operation_id} requires active exact Business Unit rows with one shared primary ledger.")
                bu = matches[0]
                ledger = metadata.get_json(_ledger_url(config["host"], bu["PrimaryLedgerId"]), config["auth"], stage="resolve primary ledger")
                ledger_item = ledger if isinstance(ledger, dict) and "LedgerId" in ledger else (_items(ledger)[0] if len(_items(ledger)) == 1 else None)
                if not isinstance(ledger_item, dict) or not str(ledger_item.get("Name", "")).strip() or not str(ledger_item.get("CurrencyCode", "")).strip():
                    raise LookupPreflightError(f"Operation {operation_id} primary ledger result is incomplete.")
            except metadata.DataLoadError as exc:
                if exc.http_status == 400:
                    _append_resolver_contract_issue(
                        resolved, operation_id=operation_id, field="BuName",
                        resolver="resolve_business_unit_primary_ledger", endpoint=BUSINESS_UNITS_PATH,
                        requested_value=bu_name, error=exc,
                    )
                    _unavailable_receipt(
                        resolved, entity=entity, field="BuName",
                        resolver="resolve_business_unit_primary_ledger",
                        evidence={"buName": bu_name}, summary=summary,
                    )
                    # The adapter will later surface the missing required create
                    # context.  Do not discard the advisory receipt or its
                    # maintainer finding at this preflight stage.
                    continue
                raise LookupPreflightError(f"Operation {operation_id} cannot derive required BU primary-ledger values: {exc.message}") from exc
            scope = resolved.setdefault("resolvedScope", {})
            entries = scope.setdefault("businessUnits", []) if isinstance(scope, dict) else None
            if not isinstance(entries, list):
                raise LookupPreflightError("resolvedScope.businessUnits must be an array.")
            prior = next((item for item in entries if isinstance(item, dict) and item.get("entity") == entity and item.get("targetKey") == target), {})
            entry = {
                "entity": entity, "targetKey": target,
                "resolvedValues": {**(prior.get("resolvedValues", {}) if isinstance(prior, dict) else {}), "SOBName": ledger_item["Name"], "BaseCurrencyCode": ledger_item["CurrencyCode"]},
                "evidence": {**(prior.get("evidence", {}) if isinstance(prior, dict) else {}), "finBusinessUnitsLOV": {"source": "finBusinessUnitsLOV", "matchedBuName": bu_name, "businessUnitId": bu["BusinessUnitId"], "primaryLedgerId": bu["PrimaryLedgerId"], "resultCount": len(matches), "active": True}, "ledgersLOV": {"source": "ledgersLOV", "ledgerId": bu["PrimaryLedgerId"], "name": ledger_item["Name"], "currencyCode": ledger_item["CurrencyCode"]}},
            }
            entries[:] = [item for item in entries if not (isinstance(item, dict) and item.get("entity") == entity and item.get("targetKey") == target)] + [entry]
            summary["satisfied"] += 2
        # Implementation of the `resolve_payment_term_from_name` resolver
        # contract: create a read-only corroborating receipt for each supplied
        # payment-term name.  FSM import remains the authoritative resolver.
        for field in PAYMENT_TERM_RECEIPT_FIELDS:
            if field not in values:
                continue
            name = str(values[field]).strip()
            if not name:
                raise LookupPreflightError(f"Operation {operation_id} supplies blank {field}.")
            try:
                response = metadata.get_json(
                    _payment_term_url(config["host"], name), config["auth"],
                    stage=f"validate {field} payment term",
                )
            except metadata.DataLoadError as exc:
                if not _is_advisory_unavailable(exc):
                    raise LookupPreflightError(f"Operation {operation_id} cannot validate {field}: {exc.message}") from exc
                if exc.http_status == 400:
                    _append_resolver_contract_issue(
                        resolved, operation_id=operation_id, field=field,
                        resolver="resolve_payment_term_from_name", endpoint=PAYMENT_TERMS_PATH,
                        requested_value=name, error=exc,
                    )
                _unavailable_receipt(resolved, entity=entity, field=field,
                    resolver="resolve_payment_term_from_name",
                    evidence={"name": name}, summary=summary)
                continue
            # This query is corroborating evidence only.  It does not carry the
            # complete FSM import context, so do not impose a local case-sensitive
            # name comparison or select a term ID from its result set.
            matches = _items(response)
            if not matches:
                raise LookupPreflightError(
                    f"Operation {operation_id} {field} has no exact match in readable "
                    "payablesPaymentTerms results."
                )
            if len(matches) > 1:
                _multiple_results_receipt(resolved, entity=entity, field=field,
                    resolver="resolve_payment_term_from_name",
                    evidence={"name": name, "returnedNames": [entry.get("name") for entry in matches],
                              "termsIds": [entry.get("termsId") for entry in matches],
                              "resultCount": len(matches), "source": "payablesPaymentTerms"}, summary=summary)
                continue
            item = matches[0]
            _upsert_prerequisite(resolved, {
                "entity": entity, "field": field,
                "resolver": "resolve_payment_term_from_name", "status": "satisfied",
                "evidence": {
                    "name": name,
                    "returnedNames": [entry.get("name") for entry in matches],
                    "termsId": item.get("termsId"),
                    "termsIds": [entry.get("termsId") for entry in matches],
                    "resultCount": len(matches),
                    "source": "payablesPaymentTerms"
                },
            })
            summary["satisfied"] += 1
        for field, resolver in CURRENCY_RECEIPT_CONTRACTS.items():
            if field not in values:
                continue
            code = str(values[field]).strip().upper()
            if not code:
                raise LookupPreflightError(f"Operation {operation_id} supplies blank {field}.")
            # Currency codes have a task-owned canonical representation.  Persist
            # it so the REST receipt and eventual FSM CSV use the same value.
            if isinstance(values[field], str):
                values[field] = code
            try:
                response = metadata.get_json(
                    _currency_url(config["host"], code), config["auth"],
                    stage=f"validate {field} currency",
                )
            except metadata.DataLoadError as exc:
                if not _is_advisory_unavailable(exc):
                    raise LookupPreflightError(f"Operation {operation_id} cannot validate {field}: {exc.message}") from exc
                if exc.http_status == 400:
                    _append_resolver_contract_issue(
                        resolved, operation_id=operation_id, field=field,
                        resolver=resolver, endpoint=CURRENCIES_PATH,
                        requested_value=code, error=exc,
                    )
                _unavailable_receipt(resolved, entity=entity, field=field,
                    resolver=resolver, evidence={"currencyCode": code}, summary=summary)
                continue
            # This is a corroborating preflight, not the context-aware FSM
            # resolver.  Retain readable currency results without requiring a
            # unique or case-exact local match.
            matches = _items(response)
            if not matches:
                raise LookupPreflightError(
                    f"Operation {operation_id} {field} has no exact match in readable "
                    "currenciesLOV results."
                )
            if len(matches) > 1:
                _multiple_results_receipt(resolved, entity=entity, field=field,
                    resolver=resolver, evidence={"currencyCode": code,
                        "returnedCurrencyCodes": [item.get("CurrencyCode", item.get("currencyCode")) for item in matches],
                        "resultCount": len(matches), "source": "currenciesLOV"}, summary=summary)
                continue
            _upsert_prerequisite(resolved, {
                "entity": entity, "field": field, "resolver": resolver,
                "status": "satisfied", "evidence": {
                    "currencyCode": code,
                    "returnedCurrencyCodes": [item.get("CurrencyCode", item.get("currencyCode")) for item in matches],
                    "resultCount": len(matches),
                    "source": "currenciesLOV",
                },
            })
            summary["satisfied"] += 1
    return resolved, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, required=True, help="Input request/design JSON.")
    parser.add_argument("--output", type=Path, required=True, help="Resolved design JSON output.")
    metadata.add_oauth_arguments(parser)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = metadata.read_config(args.properties, **metadata.oauth_kwargs(args))
        resolved, summary = resolve_lookup_prerequisites(_read_json(args.design), config)
        _write_json(args.output, resolved)
        print(json.dumps({"status": "PASS", **summary, "output": str(args.output)}, sort_keys=True))
        return 0
    except (LookupPreflightError, metadata.DataLoadError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
