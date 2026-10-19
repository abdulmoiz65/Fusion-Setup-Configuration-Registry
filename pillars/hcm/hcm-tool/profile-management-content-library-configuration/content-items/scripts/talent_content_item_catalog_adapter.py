#!/usr/bin/env python3
"""Collect sanitized, read-only Talent Content Item Catalog evidence.

The adapter invokes the repository core Fusion REST client and can issue GET
requests only. It discovers parent template metadata or checks one exact
ContentItemCode through the registry-selected child relation across every
owning catalog. Its certification operation also checks the exact V2 name,
release seed identity, provider lifecycle, and catalog ownership. It never
constructs an opaque catalog key and never performs a Fusion mutation.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Mapping, Sequence
import urllib.parse


SCHEMA_VERSION = "1.0"
PROVIDER = "CATALOG_REST"
MAX_PAGES = 1000
MAX_RESPONSE_BYTES = 32 * 1024 * 1024
MAX_API_VERSION_CANDIDATES = 3
VALID_READ_STATUSES = frozenset({"candidate", "verified", "read-only", "unsupported"})
VALID_CREATE_STATUSES = frozenset({"blocked", "certification-only", "verified"})
VALID_SELECTOR_STATUSES = frozenset({"discovery-required", "registered", "unsupported"})
VALID_PROVIDER_LIFECYCLES = frozenset({"blocked", "certification-only", "verified"})
SAFE_CONTEXT_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_]{0,79}$")
SENSITIVE_KEY_PATTERN = re.compile(
    r"authorization|access.?token|refresh.?token|client.?secret|password|private.?key",
    re.IGNORECASE,
)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"\bbearer\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b[A-Za-z0-9+/]{120,}={0,2}\b"),
)
CATALOG_HDL_PROVIDER = "CATALOG_CONTENT_ITEM_V2_HDL"
CATALOG_PROVIDER_KEYS = frozenset(
    {
        "schema_version",
        "provider",
        "business_object",
        "task_code",
        "profile_mode",
        "source_fusion_releases",
        "evidence_provider",
        "readback_providers",
        "user_key",
        "code_identity",
        "max_rows_per_package",
        "date_format",
        "execution_route",
        "mutation_boundary",
        "contexts",
    }
)
CATALOG_PROVIDER_CONTEXT_KEYS = frozenset(
    {
        "context_name",
        "template_id",
        "child_relation",
        "release_source_file",
        "release_template_context",
        "lifecycle",
        "builder_route",
        "row_fields",
        "required_fields",
        "fixed_values",
        "blocked_catalog_codes",
        "ownership_restrictions",
    }
)


class ProviderContractError(ValueError):
    """Expected fail-closed provider validation error."""

    def __init__(self, message: str, failure_class: str = "input_validation") -> None:
        super().__init__(message)
        self.failure_class = failure_class


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_text(value: Any, label: str, *, max_length: int = 256) -> str:
    if not isinstance(value, str) or not value:
        raise ProviderContractError(f"{label} must be a nonempty string")
    if value != value.strip():
        raise ProviderContractError(f"{label} must not have leading or trailing whitespace")
    if len(value) > max_length or any(ord(char) < 32 for char in value):
        raise ProviderContractError(f"{label} contains unsupported characters or is too long")
    return value


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _fusion_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _safe_scalar(value: Any) -> str | int | float | bool | None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ProviderContractError(
        "Fusion returned a non-scalar comparable field",
        "catalog_or_metadata_mismatch",
    )


def _assert_sanitized(value: Any) -> None:
    """Fail closed if a result contains credential keys or secret-shaped values."""
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if SENSITIVE_KEY_PATTERN.search(str(key)):
                raise ProviderContractError(
                    "sanitized evidence contains a sensitive key",
                    "artifact_persistence",
                )
            _assert_sanitized(nested)
        return
    if isinstance(value, (list, tuple)):
        for nested in value:
            _assert_sanitized(nested)
        return
    if isinstance(value, str) and any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
        raise ProviderContractError(
            "sanitized evidence contains secret-shaped material",
            "artifact_persistence",
        )


def load_registry(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProviderContractError("provider registry is not readable JSON", "artifact_persistence") from error
    if not isinstance(raw, dict):
        raise ProviderContractError("provider registry must be an object")
    required = {
        "schema_version",
        "provider",
        "resource_name",
        "parent_resource",
        "api_version_candidates",
        "source_fusion_releases",
        "page_size",
        "identity_field",
        "common_comparable_fields",
        "contexts",
    }
    if set(raw) != required:
        raise ProviderContractError("provider registry has missing or unexpected top-level keys")
    if raw["schema_version"] != SCHEMA_VERSION or raw["provider"] != PROVIDER:
        raise ProviderContractError("provider registry schema or provider is unsupported")
    parent = _require_text(raw["parent_resource"], "parent_resource")
    if parent != "/hcmRestApi/resources/11.13.18.05/talentContentItemCatalogs":
        raise ProviderContractError("provider registry parent_resource is not allowlisted")
    if raw["resource_name"] != "talentContentItemCatalogs":
        raise ProviderContractError("provider registry resource_name is unsupported")
    candidates = raw["api_version_candidates"]
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= MAX_API_VERSION_CANDIDATES:
        raise ProviderContractError("api_version_candidates must contain one through three entries")
    seen_versions: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict) or set(candidate) != {
            "api_version",
            "parent_resource",
            "capability_query",
            "source_reference",
        }:
            raise ProviderContractError("an API version candidate has an invalid shape")
        version = _require_text(candidate["api_version"], "api_version", max_length=32)
        if version in seen_versions or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version):
            raise ProviderContractError("API version candidates must be unique numeric namespaces")
        seen_versions.add(version)
        candidate_parent = _require_text(candidate["parent_resource"], "candidate parent_resource")
        expected_parent = f"/hcmRestApi/resources/{version}/talentContentItemCatalogs"
        if candidate_parent != expected_parent:
            raise ProviderContractError("API version candidate path is outside the registered resource")
        query = candidate["capability_query"]
        if query != {"limit": "1", "offset": "0", "onlyData": "true"}:
            raise ProviderContractError("API version candidate capability query is not bounded")
        _require_text(candidate["source_reference"], "candidate source_reference", max_length=500)
    if parent not in {candidate["parent_resource"] for candidate in candidates}:
        raise ProviderContractError("parent_resource is not an API version candidate")
    releases = raw["source_fusion_releases"]
    if not isinstance(releases, list) or not releases or any(not isinstance(v, str) for v in releases):
        raise ProviderContractError("source_fusion_releases must be a nonempty string array")
    page_size = raw["page_size"]
    if isinstance(page_size, bool) or not isinstance(page_size, int) or not 1 <= page_size <= 500:
        raise ProviderContractError("page_size must be an integer from 1 through 500")
    identity = _require_text(raw["identity_field"], "identity_field")
    if identity != "ContentItemCode":
        raise ProviderContractError("identity_field must be ContentItemCode")
    fields = raw["common_comparable_fields"]
    if not isinstance(fields, list) or identity not in fields or len(fields) != len(set(fields)):
        raise ProviderContractError("common_comparable_fields must be unique and include ContentItemCode")
    for field in fields:
        _require_text(field, "common_comparable_fields entry")
    contexts = raw["contexts"]
    if not isinstance(contexts, list) or not contexts:
        raise ProviderContractError("contexts must be a nonempty array")
    seen_contexts: set[str] = set()
    seen_relations: set[str] = set()
    for entry in contexts:
        _validate_registry_entry(entry, seen_contexts, seen_relations)
    return raw


def load_catalog_hdl_provider(path: Path) -> tuple[dict[str, Any], str]:
    """Load and strictly validate the release-bound catalog HDL contract."""
    try:
        serialized = path.read_bytes()
        raw = json.loads(serialized.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProviderContractError(
            "catalog HDL provider contract is not readable JSON",
            "artifact_persistence",
        ) from error
    if not isinstance(raw, dict) or set(raw) != set(CATALOG_PROVIDER_KEYS):
        raise ProviderContractError("catalog HDL provider contract has an invalid top-level shape")
    expected = {
        "schema_version": SCHEMA_VERSION,
        "provider": CATALOG_HDL_PROVIDER,
        "business_object": "ContentItem",
        "task_code": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
        "profile_mode": "enhanced",
        "source_fusion_releases": ["26C"],
        "evidence_provider": PROVIDER,
        "readback_providers": ["CATALOG_REST", "ITEM_CATALOG_FSM_EXPORT"],
        "user_key": ["ContextName", "ContentItemValueSetName", "Name"],
        "code_identity": ["ContextName", "ContentItemCode"],
        "max_rows_per_package": 1,
        "date_format": "YYYY/MM/DD",
        "execution_route": "core.data-loader",
        "mutation_boundary": "create-only-single-row",
    }
    for field, value in expected.items():
        if raw[field] != value:
            raise ProviderContractError(
                f"catalog HDL provider contract has an unsupported {field}"
            )
    contexts = raw["contexts"]
    if not isinstance(contexts, list) or not contexts:
        raise ProviderContractError("catalog HDL provider contexts must be a nonempty array")
    seen: set[str] = set()
    for entry in contexts:
        if not isinstance(entry, dict) or set(entry) != set(CATALOG_PROVIDER_CONTEXT_KEYS):
            raise ProviderContractError("catalog HDL provider context has an invalid shape")
        context = _require_text(entry["context_name"], "provider context_name", max_length=80)
        if not SAFE_CONTEXT_PATTERN.fullmatch(context) or context in seen:
            raise ProviderContractError("catalog HDL provider context names must be unique codes")
        seen.add(context)
        if isinstance(entry["template_id"], bool) or not isinstance(entry["template_id"], int):
            raise ProviderContractError("catalog HDL provider template_id must be an integer")
        _require_text(entry["child_relation"], "provider child_relation", max_length=120)
        lifecycle = entry["lifecycle"]
        if not isinstance(lifecycle, dict) or set(lifecycle) != {"status", "reason"}:
            raise ProviderContractError("catalog HDL provider lifecycle has an invalid shape")
        if lifecycle["status"] not in VALID_PROVIDER_LIFECYCLES:
            raise ProviderContractError("catalog HDL provider lifecycle is invalid")
        _require_text(lifecycle["reason"], "provider lifecycle reason", max_length=1000)
        if entry["builder_route"] not in {
            "catalog-provider",
            "existing-competency-provider",
            "blocked",
        }:
            raise ProviderContractError("catalog HDL provider builder_route is invalid")
        for field in ("row_fields", "required_fields", "blocked_catalog_codes", "ownership_restrictions"):
            if not isinstance(entry[field], list) or any(
                not isinstance(value, str) for value in entry[field]
            ):
                raise ProviderContractError(f"catalog HDL provider {field} must be a string array")
        row_fields = entry["row_fields"]
        if len(row_fields) != len(set(row_fields)):
            raise ProviderContractError("catalog HDL provider row_fields must be unique")
        if not set(entry["required_fields"]).issubset(row_fields):
            raise ProviderContractError("catalog HDL provider required_fields must be row fields")
        fixed = entry["fixed_values"]
        if not isinstance(fixed, dict) or not set(fixed).issubset(row_fields):
            raise ProviderContractError("catalog HDL provider fixed_values are invalid")
        if entry["builder_route"] == "catalog-provider":
            if lifecycle["status"] not in {"certification-only", "verified"}:
                raise ProviderContractError("catalog-provider route must have an eligible lifecycle")
            if fixed.get("ContextName") != context:
                raise ProviderContractError("catalog HDL fixed ContextName must match its context")
            if not isinstance(entry["release_source_file"], str):
                raise ProviderContractError("catalog HDL provider release source is required")
            if entry["release_template_context"] != context:
                raise ProviderContractError("catalog HDL provider release context is not aligned")
        elif entry["builder_route"] == "blocked" and lifecycle["status"] != "blocked":
            raise ProviderContractError("a blocked builder route must have blocked lifecycle")
    return raw, _sha256_bytes(serialized)


def _validate_registry_entry(
    entry: Any, seen_contexts: set[str], seen_relations: set[str]
) -> None:
    if not isinstance(entry, dict):
        raise ProviderContractError("each provider registry context must be an object")
    required = {
        "context_name",
        "child_relation",
        "catalog_selector",
        "read_certification",
        "hdl_create_certification",
        "ownership_restrictions",
    }
    if set(entry) != required:
        raise ProviderContractError("provider registry context has missing or unexpected keys")
    context = _require_text(entry["context_name"], "context_name", max_length=80)
    if not SAFE_CONTEXT_PATTERN.fullmatch(context) or context in seen_contexts:
        raise ProviderContractError("provider registry context names must be unique technical codes")
    seen_contexts.add(context)
    relation = _require_text(entry["child_relation"], "child_relation", max_length=120)
    if relation in seen_relations or not relation.endswith("ContentItems"):
        raise ProviderContractError("provider registry child relations must be unique ContentItems names")
    seen_relations.add(relation)
    selector = entry["catalog_selector"]
    if not isinstance(selector, dict) or set(selector) != {"status", "template_id", "template_name"}:
        raise ProviderContractError("catalog_selector has an invalid shape")
    if selector["status"] not in VALID_SELECTOR_STATUSES:
        raise ProviderContractError("catalog_selector.status is invalid")
    if selector["status"] == "registered":
        if isinstance(selector["template_id"], bool) or not isinstance(selector["template_id"], int):
            raise ProviderContractError("a registered catalog selector requires an integer template_id")
        if selector["template_name"] is not None:
            _require_text(selector["template_name"], "catalog_selector.template_name")
    elif selector["template_id"] is not None or selector["template_name"] is not None:
        raise ProviderContractError("an unresolved catalog selector must not contain template values")
    read = entry["read_certification"]
    create = entry["hdl_create_certification"]
    if not isinstance(read, dict) or set(read) != {"status", "release", "reason"}:
        raise ProviderContractError("read_certification has an invalid shape")
    if read["status"] not in VALID_READ_STATUSES:
        raise ProviderContractError("read_certification.status is invalid")
    if not isinstance(create, dict) or set(create) != {"status", "release", "reason"}:
        raise ProviderContractError("hdl_create_certification has an invalid shape")
    if create["status"] not in VALID_CREATE_STATUSES:
        raise ProviderContractError("hdl_create_certification.status is invalid")
    _require_text(read["release"], "read_certification.release")
    _require_text(read["reason"], "read_certification.reason", max_length=800)
    _require_text(create["release"], "hdl_create_certification.release")
    _require_text(create["reason"], "hdl_create_certification.reason", max_length=800)
    restrictions = entry["ownership_restrictions"]
    if not isinstance(restrictions, list) or any(not isinstance(value, str) for value in restrictions):
        raise ProviderContractError("ownership_restrictions must be a string array")


def _context_entry(registry: Mapping[str, Any], context_name: str) -> dict[str, Any]:
    context = _require_text(context_name, "context", max_length=80)
    if not SAFE_CONTEXT_PATTERN.fullmatch(context):
        raise ProviderContractError("context must be an uppercase technical code")
    matches = [entry for entry in registry["contexts"] if entry["context_name"] == context]
    if len(matches) != 1:
        raise ProviderContractError(
            f"context {context} is not registered exactly once",
            "catalog_or_metadata_mismatch",
        )
    return dict(matches[0])


def _catalog_provider_context(
    provider: Mapping[str, Any],
    registry_context: Mapping[str, Any],
) -> dict[str, Any]:
    context_name = registry_context["context_name"]
    matches = [
        entry for entry in provider["contexts"] if entry["context_name"] == context_name
    ]
    if len(matches) != 1:
        raise ProviderContractError(
            f"context {context_name} is not registered exactly once in the catalog HDL provider",
            "catalog_or_metadata_mismatch",
        )
    entry = dict(matches[0])
    if (
        entry["template_id"] != registry_context["catalog_selector"]["template_id"]
        or entry["child_relation"] != registry_context["child_relation"]
    ):
        raise ProviderContractError(
            f"context {context_name} differs between the REST registry and HDL provider",
            "catalog_or_metadata_mismatch",
        )
    if entry["lifecycle"]["status"] != registry_context["hdl_create_certification"]["status"]:
        raise ProviderContractError(
            f"context {context_name} lifecycle differs between the REST registry and HDL provider",
            "catalog_or_metadata_mismatch",
        )
    return entry


def _seeded_identity_check(
    seeded_catalog_dir: Path,
    *,
    fusion_release: str,
    context_name: str,
    content_item_code: str,
    content_item_name: str,
) -> dict[str, Any]:
    manifest_path = seeded_catalog_dir / "manifest.json"
    items_path = seeded_catalog_dir / "content-items.csv"
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        items_bytes = items_path.read_bytes()
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProviderContractError(
            "seeded Content Items evidence is unreadable",
            "catalog_or_metadata_mismatch",
        ) from error
    if not isinstance(manifest, dict) or manifest.get("catalog_kind") != "oracle-seeded-profile-content-items":
        raise ProviderContractError(
            "seeded Content Items evidence has an invalid catalog kind",
            "catalog_or_metadata_mismatch",
        )
    file_contract = manifest.get("files", {}).get("content-items.csv", {})
    if file_contract.get("sha256") != _sha256_bytes(items_bytes):
        raise ProviderContractError(
            "seeded Content Items evidence fingerprint is invalid",
            "catalog_or_metadata_mismatch",
        )
    try:
        text = items_bytes.decode("utf-8-sig")
        reader = csv.DictReader(text.splitlines())
        expected_fields = {
            "ContextName",
            "ContentItemCode",
            "Name",
            "ContentSupplierCode",
            "DateFrom",
            "DateTo",
        }
        if set(reader.fieldnames or ()) != expected_fields:
            raise ProviderContractError(
                "seeded Content Items evidence fields are invalid",
                "catalog_or_metadata_mismatch",
            )
        rows = list(reader)
    except (UnicodeError, csv.Error) as error:
        raise ProviderContractError(
            "seeded Content Items evidence is malformed",
            "catalog_or_metadata_mismatch",
        ) from error
    if file_contract.get("row_count") != len(rows):
        raise ProviderContractError(
            "seeded Content Items evidence row count is invalid",
            "catalog_or_metadata_mismatch",
        )
    code_matches = sum(
        1
        for row in rows
        if row.get("ContextName") == context_name
        and row.get("ContentItemCode") == content_item_code
    )
    name_matches = sum(
        1
        for row in rows
        if row.get("ContextName") == context_name and row.get("Name") == content_item_name
    )
    return {
        "seeded_content_item_manifest_sha256": _sha256_bytes(manifest_bytes),
        "seeded_exact_code_matches": code_matches,
        "seeded_exact_name_matches": name_matches,
    }


def _validate_release(
    registry: Mapping[str, Any], fusion_release: str | None, *, required: bool = True
) -> str | None:
    """Retain optional metadata without requiring or allowlisting a release."""
    if fusion_release is None:
        return None
    release = _require_text(fusion_release, "trusted fusion_release", max_length=32)
    return release


def _release_evidence(release: str | None) -> dict[str, Any]:
    if release is None:
        return {"release_status": "unknown"}
    return {"release_status": "verified", "fusion_release": release}


def _trusted_quarterly_release(value: str | None) -> str | None:
    """Keep only an explicit quarterly-release value; never derive it from an API version."""

    if value is None:
        return None
    candidate = _require_text(value, "trusted quarterly release", max_length=32)
    return candidate if re.fullmatch(r"[0-9]{2}[A-Z]", candidate) else None


def select_rest_api_capability(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    trusted_fusion_release: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Select one source-backed REST namespace through a bounded authenticated GET."""

    target = _require_text(target_environment, "target_environment", max_length=64)
    release = _trusted_quarterly_release(trusted_fusion_release)
    failures = []
    selected = None
    for candidate in registry["api_version_candidates"]:
        try:
            payload = transport.get(candidate["parent_resource"], candidate["capability_query"])
            _validate_page(payload, 0)
            selected = candidate
            break
        except ProviderContractError as error:
            if error.failure_class in {
                "auth_expired_or_invalid",
                "authorization_or_privilege",
                "transport_or_environment",
            }:
                raise
            failures.append(candidate["api_version"])
    if selected is None:
        raise ProviderContractError(
            "no registry-declared Fusion REST API version passed the bounded capability check",
            "catalog_or_metadata_mismatch",
        )
    captured = now or _utc_now()
    environment_fingerprint = _sha256(
        {"target_environment": target, "selected_api_version": selected["api_version"]}
    )
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "verified",
        "operation": "read-only-capability-check",
        "provider": PROVIDER,
        "target_environment": target,
        "environment_fingerprint": environment_fingerprint,
        "authenticated_context_source": "repository-fusion-authentication",
        "selected_api_version": selected["api_version"],
        "selected_resource": selected["parent_resource"],
        **_release_evidence(release),
        "checked_at": _timestamp(captured),
    }
    return {**body, "capability_fingerprint": _sha256(body)}


class CoreRestCliTransport:
    """GET-only subprocess adapter for core.fusion-api.rest-api-client."""

    def __init__(
        self,
        *,
        rest_client: Path,
        properties: Path | None = None,
        token_cache: Path | None = None,
        expected_environment: str | None = None,
        timeout: int = 60,
        run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        self.rest_client = rest_client
        self.properties = properties
        self.token_cache = token_cache
        self.timeout = timeout
        self._run = run
        self.expected_environment = expected_environment
        self._environment_checked = False

    def _validate_environment_binding(self) -> None:
        if self._environment_checked or self.expected_environment is None:
            return
        properties = self.properties or self.rest_client.parents[3] / "auth" / "fusionEnv.properties"
        auth_script = self.rest_client.parents[3] / "auth" / "fusion-oauth-authentication" / "scripts" / "fusion_auth.py"
        spec = importlib.util.spec_from_file_location("content_item_rest_fusion_auth", auth_script)
        if spec is None or spec.loader is None:
            raise ProviderContractError(
                "core Fusion authentication service is unavailable",
                "transport_or_environment",
            )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        configured = module.read_properties(properties).get("environment")
        if configured != self.expected_environment:
            raise ProviderContractError(
                "target_environment does not match the selected Fusion OAuth environment",
                "transport_or_environment",
            )
        self._environment_checked = True

    def get(self, endpoint: str, query: Mapping[str, str]) -> dict[str, Any]:
        self._validate_environment_binding()
        command = [
            sys.executable,
            str(self.rest_client),
            endpoint,
            "--method",
            "GET",
            "--timeout",
            str(self.timeout),
        ]
        if self.properties is not None:
            command.extend(["--properties", str(self.properties)])
        if self.token_cache is not None:
            command.extend(["--token-cache", str(self.token_cache)])
        for key, value in query.items():
            command.extend(["--query", f"{key}={value}"])
        attempts = 0
        while True:
            attempts += 1
            result = self._run(command, text=True, capture_output=True, check=False)
            if result.returncode == 0:
                if len(result.stdout.encode("utf-8")) > MAX_RESPONSE_BYTES:
                    raise ProviderContractError("Fusion REST response exceeds the size limit", "fusion_api_error")
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as error:
                    raise ProviderContractError("Fusion REST returned non-JSON content", "fusion_api_error") from error
                if not isinstance(payload, dict):
                    raise ProviderContractError("Fusion REST response must be an object", "fusion_api_error")
                return payload
            diagnostic = (result.stderr or "")[-4000:]
            recoverable_transport = any(
                marker in diagnostic.casefold()
                for marker in ("failed calling", "timed out", "temporary failure", "connection reset")
            )
            if recoverable_transport and attempts < 3:
                time.sleep(0.25 * attempts)
                continue
            folded_diagnostic = diagnostic.casefold()
            if "http 401" in folded_diagnostic or "oauth" in folded_diagnostic or "token response" in folded_diagnostic:
                failure_class = "auth_expired_or_invalid"
            elif "http 403" in folded_diagnostic or "not authorized" in folded_diagnostic:
                failure_class = "authorization_or_privilege"
            else:
                failure_class = "transport_or_environment" if recoverable_transport else "fusion_api_error"
            raise ProviderContractError(
                "The core Fusion REST client could not complete the read-only request",
                failure_class,
            )


def _validate_page(payload: Any, expected_offset: int) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(payload, dict):
        raise ProviderContractError("Fusion page must be an object", "fusion_api_error")
    items = payload.get("items")
    count = payload.get("count")
    has_more = payload.get("hasMore")
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise ProviderContractError("Fusion page items are malformed", "fusion_api_error")
    if isinstance(count, bool) or not isinstance(count, int) or count != len(items):
        raise ProviderContractError("Fusion page count is inconsistent", "fusion_api_error")
    if not isinstance(has_more, bool):
        raise ProviderContractError("Fusion page hasMore is unavailable", "fusion_api_error")
    offset = payload.get("offset")
    if offset is not None and (isinstance(offset, bool) or not isinstance(offset, int) or offset != expected_offset):
        raise ProviderContractError("Fusion page offset is inconsistent", "fusion_api_error")
    if has_more and not items:
        raise ProviderContractError("Fusion pagination stalled on an empty page", "fusion_api_error")
    return [dict(item) for item in items], has_more


def _get_all_pages(
    transport: Any,
    endpoint: str,
    base_query: Mapping[str, str],
    page_size: int,
) -> list[dict[str, Any]]:
    all_items: list[dict[str, Any]] = []
    offset = 0
    seen_offsets: set[int] = set()
    for _page in range(MAX_PAGES):
        if offset in seen_offsets:
            raise ProviderContractError("Fusion pagination repeated an offset", "fusion_api_error")
        seen_offsets.add(offset)
        query = dict(base_query)
        query["limit"] = str(page_size)
        query["offset"] = str(offset)
        payload = transport.get(endpoint, query)
        items, has_more = _validate_page(payload, offset)
        all_items.extend(items)
        if not has_more:
            return all_items
        offset += len(items)
    raise ProviderContractError("Fusion pagination exceeded the page limit", "fusion_api_error")


def _links(item: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = item.get("links")
    if not isinstance(value, list) or any(not isinstance(link, dict) for link in value):
        available = ", ".join(
            sorted(key for key in item if not SENSITIVE_KEY_PATTERN.search(key))
        )
        raise ProviderContractError(
            f"Fusion catalog links are unavailable ({type(value).__name__}); safe parent fields: {available}",
            "catalog_or_metadata_mismatch",
        )
    return [dict(link) for link in value]


def _child_endpoint(item: Mapping[str, Any], parent_resource: str, relation: str) -> str:
    matches = [
        link
        for link in _links(item)
        if link.get("rel") == "child" and link.get("name") == relation
    ]
    if len(matches) != 1 or not isinstance(matches[0].get("href"), str):
        raise ProviderContractError(
            f"Fusion did not return exactly one child link named {relation}",
            "catalog_or_metadata_mismatch",
        )
    parsed = urllib.parse.urlsplit(matches[0]["href"])
    if parsed.scheme and parsed.scheme != "https":
        raise ProviderContractError("Fusion child link must use HTTPS", "catalog_or_metadata_mismatch")
    if parsed.username or parsed.password or parsed.fragment:
        raise ProviderContractError("Fusion child link contains unsupported URL parts", "catalog_or_metadata_mismatch")
    expected_prefix = parent_resource.rstrip("/") + "/"
    expected_suffix = "/child/" + relation
    if not parsed.path.startswith(expected_prefix) or not parsed.path.endswith(expected_suffix):
        raise ProviderContractError("Fusion child link path is outside the registered provider", "catalog_or_metadata_mismatch")
    existing_query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if any(key in existing_query for key in ("q", "limit", "offset")):
        raise ProviderContractError("Fusion child link contains conflicting query parameters", "catalog_or_metadata_mismatch")
    return parsed.path + (("?" + parsed.query) if parsed.query else "")


def _normalize_template_id(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _template_descriptor(item: Mapping[str, Any]) -> tuple[int, str | None]:
    template_id = _normalize_template_id(item.get("TemplateId"))
    template_name = item.get("Template")
    if template_id is None:
        available = ", ".join(
            sorted(key for key in item if key != "links" and not SENSITIVE_KEY_PATTERN.search(key))
        )
        raise ProviderContractError(
            f"Fusion catalog TemplateId is unavailable; safe parent fields: {available}",
            "catalog_or_metadata_mismatch",
        )
    if template_name is not None and (not isinstance(template_name, str) or not template_name):
        raise ProviderContractError("Fusion catalog Template has an invalid shape", "catalog_or_metadata_mismatch")
    return template_id, template_name


def _catalog_identity(
    item: Mapping[str, Any], template_id: int, template_name: str | None
) -> dict[str, Any]:
    code = _safe_scalar(item.get("ContentItemValueSetCode"))
    name = _safe_scalar(item.get("ContentItemValueSetName"))
    if not isinstance(code, str) or not code or not isinstance(name, str) or not name:
        raise ProviderContractError(
            "Fusion catalog code or name is unavailable",
            "catalog_or_metadata_mismatch",
        )
    return {
        "catalog_code": code,
        "catalog_name": name,
        "template_id": template_id,
        "template_name": template_name,
    }


def discover(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    target = _require_text(target_environment, "target_environment", max_length=64)
    release = _validate_release(registry, fusion_release, required=False)
    captured = now or _utc_now()
    items = _get_all_pages(
        transport,
        registry["parent_resource"],
        {"links": "self,child"},
        registry["page_size"],
    )
    relations = {entry["child_relation"] for entry in registry["contexts"]}
    templates: dict[tuple[int, str | None], dict[str, Any]] = {}
    unresolved_template_catalogs = 0
    for item in items:
        if _normalize_template_id(item.get("TemplateId")) is None:
            unresolved_template_catalogs += 1
            continue
        template_id, template_name = _template_descriptor(item)
        key = template_id, template_name
        descriptor = templates.setdefault(
            key,
            {
                "template_id": template_id,
                "template_name": template_name,
                "catalog_count": 0,
                "catalog_statuses": set(),
                "registered_child_relations": set(),
                "catalogs": [],
            },
        )
        descriptor["catalog_count"] += 1
        if item.get("Status") is not None:
            descriptor["catalog_statuses"].add(str(item.get("Status")))
        descriptor["registered_child_relations"].update(
            str(link.get("name"))
            for link in _links(item)
            if link.get("rel") == "child" and link.get("name") in relations
        )
        catalog_identity = _catalog_identity(item, template_id, template_name)
        descriptor["catalogs"].append(
            {
                **catalog_identity,
                "catalog_identity_sha256": _sha256(catalog_identity),
                "status": _safe_scalar(item.get("Status")),
                "number_of_items": _safe_scalar(item.get("NumberofItems")),
            }
        )
    normalized_templates = []
    for descriptor in sorted(templates.values(), key=lambda value: (value["template_id"], value["template_name"])):
        normalized_templates.append(
            {
                **{key: value for key, value in descriptor.items() if key not in {"catalog_statuses", "registered_child_relations"}},
                "catalog_statuses": sorted(descriptor["catalog_statuses"]),
                "registered_child_relations": sorted(descriptor["registered_child_relations"]),
                "catalogs": sorted(
                    descriptor["catalogs"],
                    key=lambda value: (str(value["catalog_code"]), str(value["catalog_name"])),
                ),
            }
        )
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "discovered",
        "operation": "read-only-parent-discovery",
        "provider": PROVIDER,
        "target_environment": target,
        **_release_evidence(release),
        "coverage": "complete",
        "catalog_count": len(items),
        "unresolved_template_catalog_count": unresolved_template_catalogs,
        "templates": normalized_templates,
        "captured_at": _timestamp(captured),
        "valid_through": _timestamp(captured + timedelta(minutes=15)),
    }
    return {**body, "evidence_sha256": _sha256(body)}


def check_exact_code(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    context_name: str,
    content_item_code: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    target = _require_text(target_environment, "target_environment", max_length=64)
    release = _validate_release(registry, fusion_release, required=False)
    context = _context_entry(registry, context_name)
    code = _require_text(content_item_code, "content_item_code", max_length=160)
    selector = context["catalog_selector"]
    if selector["status"] != "registered":
        raise ProviderContractError(
            f"context {context_name} has no certified catalog selector",
            "catalog_or_metadata_mismatch",
        )
    if context["read_certification"]["status"] == "unsupported":
        raise ProviderContractError(
            f"context {context_name} is not supported for read evidence",
            "catalog_or_metadata_mismatch",
        )
    captured = now or _utc_now()
    template_id = selector["template_id"]
    catalogs = _get_all_pages(
        transport,
        registry["parent_resource"],
        {"q": f"TemplateId={template_id}", "links": "self,child"},
        registry["page_size"],
    )
    if not catalogs:
        raise ProviderContractError(
            f"Fusion returned no catalogs for registered context {context_name}",
            "catalog_or_metadata_mismatch",
        )
    comparable_fields = tuple(registry["common_comparable_fields"])
    exact_rows: list[dict[str, Any]] = []
    catalog_results: list[dict[str, Any]] = []
    for catalog in catalogs:
        observed_id, observed_name = _template_descriptor(catalog)
        expected_name = selector["template_name"]
        if observed_id != template_id or (expected_name is not None and observed_name != expected_name):
            raise ProviderContractError(
                f"Fusion catalog template does not match the registered {context_name} selector",
                "catalog_or_metadata_mismatch",
            )
        endpoint = _child_endpoint(catalog, registry["parent_resource"], context["child_relation"])
        child_rows = _get_all_pages(
            transport,
            endpoint,
            {
                "onlyData": "true",
                "q": f"{registry['identity_field']}={_fusion_literal(code)}",
            },
            registry["page_size"],
        )
        if any(row.get(registry["identity_field"]) != code for row in child_rows):
            raise ProviderContractError(
                "Fusion exact-code filter returned a nonmatching item",
                "fusion_api_error",
            )
        sanitized_rows = [
            {field: _safe_scalar(row[field]) for field in comparable_fields if field in row}
            for row in child_rows
        ]
        exact_rows.extend(sanitized_rows)
        catalog_identity = _catalog_identity(catalog, observed_id, observed_name)
        catalog_results.append(
            {
                **catalog_identity,
                "catalog_identity_sha256": _sha256(catalog_identity),
                "status": _safe_scalar(catalog.get("Status")),
                "child_relation": context["child_relation"],
                "match_count": len(sanitized_rows),
                "available_comparable_fields": sorted(
                    {field for row in sanitized_rows for field in row}
                ),
            }
        )
    match_count = len(exact_rows)
    classification = "not-found" if match_count == 0 else ("exact" if match_count == 1 else "multiple-exact")
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "operation": "read-only-exact-code-check",
        "provider": PROVIDER,
        "target_environment": target,
        **_release_evidence(release),
        "profile_mode": "enhanced",
        "context_name": context["context_name"],
        "child_relation": context["child_relation"],
        "coverage": "complete",
        "exact_provider_key": {
            "ContextName": context["context_name"],
            "ContentItemCode": code,
        },
        "catalog_count": len(catalogs),
        "catalogs": catalog_results,
        "match_count": match_count,
        "classification": classification,
        "matches": exact_rows,
        "read_certification": dict(context["read_certification"]),
        "hdl_create_certification": dict(context["hdl_create_certification"]),
        "ownership_restrictions": list(context["ownership_restrictions"]),
        "captured_at": _timestamp(captured),
        "valid_through": _timestamp(captured + timedelta(minutes=15)),
    }
    return {**body, "evidence_sha256": _sha256(body)}


def check_exact_identity(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    context_name: str,
    content_item_code: str,
    content_item_name: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Prove complete exact code and V2-name absence across every owning catalog."""
    captured = now or _utc_now()
    name = _require_text(content_item_name, "content_item_name", max_length=700)
    exact_code = check_exact_code(
        registry,
        transport,
        target_environment=target_environment,
        fusion_release=fusion_release,
        context_name=context_name,
        content_item_code=content_item_code,
        now=captured,
    )
    context = _context_entry(registry, context_name)
    selector = context["catalog_selector"]
    catalogs = _get_all_pages(
        transport,
        registry["parent_resource"],
        {"q": f"TemplateId={selector['template_id']}", "links": "self,child"},
        registry["page_size"],
    )
    name_matches: list[dict[str, Any]] = []
    name_catalogs: list[dict[str, Any]] = []
    comparable_fields = tuple(registry["common_comparable_fields"])
    for catalog in catalogs:
        observed_id, observed_name = _template_descriptor(catalog)
        expected_name = selector["template_name"]
        if observed_id != selector["template_id"] or (
            expected_name is not None and observed_name != expected_name
        ):
            raise ProviderContractError(
                f"Fusion catalog template does not match the registered {context_name} selector",
                "catalog_or_metadata_mismatch",
            )
        endpoint = _child_endpoint(
            catalog, registry["parent_resource"], context["child_relation"]
        )
        child_rows = _get_all_pages(
            transport,
            endpoint,
            {"onlyData": "true", "q": f"Name={_fusion_literal(name)}"},
            registry["page_size"],
        )
        if any(row.get("Name") != name for row in child_rows):
            raise ProviderContractError(
                "Fusion exact-name filter returned a nonmatching item",
                "fusion_api_error",
            )
        sanitized_rows = [
            {field: _safe_scalar(row[field]) for field in comparable_fields if field in row}
            for row in child_rows
        ]
        name_matches.extend(sanitized_rows)
        identity = _catalog_identity(catalog, observed_id, observed_name)
        name_catalogs.append(
            {
                **identity,
                "catalog_identity_sha256": _sha256(identity),
                "status": _safe_scalar(catalog.get("Status")),
                "child_relation": context["child_relation"],
                "exact_name_match_count": len(sanitized_rows),
            }
        )
    code_catalog_identity = [
        (item["catalog_code"], item["catalog_name"], item["catalog_identity_sha256"], item["status"])
        for item in exact_code["catalogs"]
    ]
    name_catalog_identity = [
        (item["catalog_code"], item["catalog_name"], item["catalog_identity_sha256"], item["status"])
        for item in name_catalogs
    ]
    if code_catalog_identity != name_catalog_identity:
        raise ProviderContractError(
            "owning catalogs changed during the dual-key evidence read",
            "catalog_or_metadata_mismatch",
        )
    combined_catalogs = []
    for code_catalog, name_catalog in zip(exact_code["catalogs"], name_catalogs):
        combined_catalogs.append(
            {
                **name_catalog,
                "exact_code_match_count": code_catalog["match_count"],
            }
        )
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "operation": "read-only-exact-code-and-name-check",
        "provider": PROVIDER,
        "target_environment": exact_code["target_environment"],
        **_release_evidence(exact_code.get("fusion_release")),
        "profile_mode": "enhanced",
        "context_name": context["context_name"],
        "child_relation": context["child_relation"],
        "coverage": "complete",
        "exact_provider_key": {
            "ContextName": context["context_name"],
            "ContentItemCode": content_item_code,
            "Name": name,
        },
        "catalog_count": len(catalogs),
        "catalogs": combined_catalogs,
        "exact_code_match_count": exact_code["match_count"],
        "exact_name_match_count": len(name_matches),
        "code_classification": exact_code["classification"],
        "name_classification": (
            "not-found"
            if not name_matches
            else ("exact" if len(name_matches) == 1 else "multiple-exact")
        ),
        "code_matches": exact_code["matches"],
        "name_matches": name_matches,
        "read_certification": dict(context["read_certification"]),
        "hdl_create_certification": dict(context["hdl_create_certification"]),
        "ownership_restrictions": list(context["ownership_restrictions"]),
        "captured_at": exact_code["captured_at"],
        "valid_through": exact_code["valid_through"],
    }
    return {**body, "evidence_sha256": _sha256(body)}


def sample_context(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    context_name: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Read at most one item per owning catalog for field-contract certification."""
    target = _require_text(target_environment, "target_environment", max_length=64)
    release = _validate_release(registry, fusion_release, required=False)
    context = _context_entry(registry, context_name)
    selector = context["catalog_selector"]
    if selector["status"] != "registered":
        raise ProviderContractError(
            f"context {context_name} has no certified catalog selector",
            "catalog_or_metadata_mismatch",
        )
    captured = now or _utc_now()
    template_id = selector["template_id"]
    catalogs = _get_all_pages(
        transport,
        registry["parent_resource"],
        {"q": f"TemplateId={template_id}", "links": "self,child"},
        registry["page_size"],
    )
    if not catalogs:
        raise ProviderContractError(
            f"Fusion returned no catalogs for registered context {context_name}",
            "catalog_or_metadata_mismatch",
        )
    comparable_fields = tuple(registry["common_comparable_fields"])
    samples = []
    for catalog in catalogs:
        observed_id, observed_name = _template_descriptor(catalog)
        expected_name = selector["template_name"]
        if observed_id != template_id or (expected_name is not None and observed_name != expected_name):
            raise ProviderContractError(
                f"Fusion catalog template does not match the registered {context_name} selector",
                "catalog_or_metadata_mismatch",
            )
        endpoint = _child_endpoint(catalog, registry["parent_resource"], context["child_relation"])
        payload = transport.get(
            endpoint,
            {"onlyData": "true", "limit": "1", "offset": "0"},
        )
        rows, has_more = _validate_page(payload, 0)
        row = rows[0] if rows else None
        available_fields = []
        sanitized_row = None
        if row is not None:
            available_fields = sorted(
                key
                for key in row
                if key not in {"links", "@context"}
                and not key.endswith("Id")
                and key not in {"CreatedBy", "CreationDate", "LastUpdatedBy", "LastUpdateDate"}
                and not SENSITIVE_KEY_PATTERN.search(key)
            )
            sanitized_row = {
                field: _safe_scalar(row[field]) for field in comparable_fields if field in row
            }
        catalog_identity = _catalog_identity(catalog, observed_id, observed_name)
        samples.append(
            {
                **catalog_identity,
                "catalog_identity_sha256": _sha256(catalog_identity),
                "catalog_status": _safe_scalar(catalog.get("Status")),
                "reported_item_count": _safe_scalar(catalog.get("NumberofItems")),
                "sample_returned": row is not None,
                "sample_page_has_more": has_more,
                "available_business_fields": available_fields,
                "sample": sanitized_row,
            }
        )
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "operation": "read-only-bounded-field-sample",
        "provider": PROVIDER,
        "target_environment": target,
        **_release_evidence(release),
        "context_name": context["context_name"],
        "child_relation": context["child_relation"],
        "coverage": "bounded-sample",
        "catalog_count": len(catalogs),
        "sampled_nonempty_catalog_count": sum(1 for item in samples if item["sample_returned"]),
        "catalog_samples": samples,
        "read_certification": dict(context["read_certification"]),
        "hdl_create_certification": dict(context["hdl_create_certification"]),
        "ownership_restrictions": list(context["ownership_restrictions"]),
        "captured_at": _timestamp(captured),
        "valid_through": _timestamp(captured + timedelta(minutes=15)),
    }
    return {**body, "evidence_sha256": _sha256(body)}


def resolve_create_catalog(
    registry: Mapping[str, Any],
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    context_name: str,
    content_item_code: str,
    catalog_code: str,
    catalog_name: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Bind approved catalog intent to complete zero-match create evidence."""
    release = _validate_release(registry, fusion_release)
    context = _context_entry(registry, context_name)
    if context["hdl_create_certification"]["status"] != "verified":
        raise ProviderContractError(
            f"context {context_name} is not independently certified for HDL creation",
            "catalog_or_metadata_mismatch",
        )
    approved_code = _require_text(catalog_code, "catalog_code", max_length=160)
    approved_name = _require_text(catalog_name, "catalog_name", max_length=240)
    captured = now or _utc_now()
    exact = check_exact_code(
        registry,
        transport,
        target_environment=target_environment,
        fusion_release=release,
        context_name=context_name,
        content_item_code=content_item_code,
        now=captured,
    )
    intended = [
        catalog
        for catalog in exact["catalogs"]
        if catalog["catalog_code"] == approved_code and catalog["catalog_name"] == approved_name
    ]
    if len(intended) != 1:
        raise ProviderContractError(
            "approved Item Catalog intent did not resolve to exactly one owning catalog",
            "catalog_or_metadata_mismatch",
        )
    selected_status = intended[0]["status"]
    if isinstance(selected_status, str) and selected_status.upper() in {"I", "INACTIVE"}:
        raise ProviderContractError(
            "approved Item Catalog is inactive",
            "catalog_or_metadata_mismatch",
        )
    if exact["classification"] != "not-found":
        raise ProviderContractError(
            "Content Item code already exists or is ambiguous across the owning catalogs",
            "catalog_or_metadata_mismatch",
        )
    body = {
        "source": "talentContentItemCatalogs",
        "target_environment": exact["target_environment"],
        "fusion_release": exact.get("fusion_release", "unknown"),
        "captured_at": exact["captured_at"],
        "valid_through": exact["valid_through"],
        "complete": exact["coverage"] == "complete",
        "content_type_context": exact["context_name"],
        "catalog_code": approved_code,
        "catalog_name": approved_name,
        "exact_content_item_matches": exact["match_count"],
    }
    return {**body, "evidence_sha256": _sha256(body)}


def resolve_certification_catalog(
    registry: Mapping[str, Any],
    provider: Mapping[str, Any],
    provider_sha256: str,
    transport: Any,
    *,
    target_environment: str,
    fusion_release: str | None,
    context_name: str,
    content_item_code: str,
    content_item_name: str,
    catalog_code: str,
    catalog_name: str,
    provider_use: str,
    seeded_catalog_dir: Path,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Bind one lifecycle-gated catalog intent to dual-key and seed evidence."""
    release = _validate_release(registry, fusion_release)
    context = _context_entry(registry, context_name)
    provider_context = _catalog_provider_context(provider, context)
    lifecycle = provider_context["lifecycle"]["status"]
    use = _require_text(provider_use, "provider_use", max_length=32)
    if provider_context["builder_route"] != "catalog-provider":
        raise ProviderContractError(
            f"context {context_name} does not use the catalog certification builder",
            "catalog_or_metadata_mismatch",
        )
    if use == "certification":
        if lifecycle not in {"certification-only", "verified"}:
            raise ProviderContractError(
                f"context {context_name} is not eligible for provider certification",
                "catalog_or_metadata_mismatch",
            )
    elif use == "general":
        if lifecycle != "verified":
            raise ProviderContractError(
                f"context {context_name} is not verified for general HDL creation",
                "catalog_or_metadata_mismatch",
            )
    else:
        raise ProviderContractError("provider_use must be certification or general")
    approved_code = _require_text(catalog_code, "catalog_code", max_length=160)
    approved_name = _require_text(catalog_name, "catalog_name", max_length=240)
    item_code = _require_text(content_item_code, "content_item_code", max_length=160)
    item_name = _require_text(content_item_name, "content_item_name", max_length=700)
    captured = now or _utc_now()
    exact = check_exact_identity(
        registry,
        transport,
        target_environment=target_environment,
        fusion_release=release,
        context_name=context_name,
        content_item_code=item_code,
        content_item_name=item_name,
        now=captured,
    )
    intended = [
        catalog
        for catalog in exact["catalogs"]
        if catalog["catalog_code"] == approved_code
        and catalog["catalog_name"] == approved_name
    ]
    if len(intended) != 1:
        raise ProviderContractError(
            "approved Item Catalog intent did not resolve to exactly one owning catalog",
            "catalog_or_metadata_mismatch",
        )
    selected_status = intended[0]["status"]
    if isinstance(selected_status, str) and selected_status.upper() in {"I", "INACTIVE"}:
        raise ProviderContractError(
            "approved Item Catalog is inactive",
            "catalog_or_metadata_mismatch",
        )
    if approved_code in provider_context["blocked_catalog_codes"]:
        raise ProviderContractError(
            "approved Item Catalog is blocked by the provider ownership policy",
            "catalog_or_metadata_mismatch",
        )
    if exact["exact_code_match_count"] != 0 or exact["exact_name_match_count"] != 0:
        raise ProviderContractError(
            "Content Item code or V2 name already exists or is ambiguous across the owning catalogs",
            "catalog_or_metadata_mismatch",
        )
    seeded = _seeded_identity_check(
        seeded_catalog_dir,
        fusion_release=release,
        context_name=context_name,
        content_item_code=item_code,
        content_item_name=item_name,
    )
    if seeded["seeded_exact_code_matches"] or seeded["seeded_exact_name_matches"]:
        raise ProviderContractError(
            "Content Item code or name exists in the packaged seed catalog",
            "catalog_or_metadata_mismatch",
        )
    body = {
        "schema_version": SCHEMA_VERSION,
        "status": "ready",
        "source": "talentContentItemCatalogs",
        "provider": CATALOG_HDL_PROVIDER,
        "provider_contract_sha256": provider_sha256,
        "provider_use": use,
        "provider_lifecycle": lifecycle,
        "target_environment": exact["target_environment"],
        "fusion_release": exact.get("fusion_release", "unknown"),
        "profile_mode": "enhanced",
        "captured_at": exact["captured_at"],
        "valid_through": exact["valid_through"],
        "complete": exact["coverage"] == "complete",
        "content_type_context": exact["context_name"],
        "child_relation": exact["child_relation"],
        "catalog_code": approved_code,
        "catalog_name": approved_name,
        "catalog_identity_sha256": intended[0]["catalog_identity_sha256"],
        "catalog_status": selected_status,
        "exact_key": {
            "ContextName": exact["context_name"],
            "ContentItemCode": item_code,
            "ContentItemValueSetName": approved_name,
            "Name": item_name,
        },
        "exact_content_item_code_matches": exact["exact_code_match_count"],
        "exact_content_item_name_matches": exact["exact_name_match_count"],
        **seeded,
        "row_fields": list(provider_context["row_fields"]),
        "required_fields": list(provider_context["required_fields"]),
        "fixed_values": dict(provider_context["fixed_values"]),
        "ownership_restrictions": list(provider_context["ownership_restrictions"]),
    }
    return {**body, "evidence_sha256": _sha256(body)}


def _inside_project(project_root: Path, relative: str) -> Path:
    supplied = Path(relative)
    if supplied.is_absolute():
        raise ProviderContractError("output must be relative to project_root", "artifact_persistence")
    root = project_root.resolve(strict=True)
    target = (root / supplied).resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise ProviderContractError("output must remain inside project_root", "artifact_persistence") from error
    return target


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    _assert_sanitized(value)
    serialized = json.dumps(value, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".content-item-rest-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _default_paths() -> tuple[Path, Path]:
    skill = Path(__file__).resolve().parents[1]
    registry = skill / "references" / "content-item-rest-provider-registry.json"
    repo = skill.parents[4]
    rest_client = repo / "core" / "fusion-api" / "rest-api-client" / "scripts" / "fusion_rest_client.py"
    return registry, rest_client


def _default_catalog_provider_paths() -> tuple[Path, Path]:
    skill = Path(__file__).resolve().parents[1]
    provider = skill / "references" / "content-item-catalog-hdl-provider.json"
    seeded = skill.parent / "assets" / "seeded-content-items"
    return provider, seeded


def resolve_authenticated_context(
    *,
    rest_client: Path,
    properties: Path | None = None,
    expected_environment: str | None = None,
    supplied_fusion_release: str | None = None,
) -> dict[str, Any]:
    """Resolve sanitized target identity from repository Fusion authentication config."""

    property_path = properties or rest_client.parents[3] / "auth" / "fusionEnv.properties"
    auth_script = rest_client.parents[3] / "auth" / "fusion-oauth-authentication" / "scripts" / "fusion_auth.py"
    spec = importlib.util.spec_from_file_location("content_item_context_fusion_auth", auth_script)
    if spec is None or spec.loader is None:
        raise ProviderContractError(
            "core Fusion authentication service is unavailable",
            "transport_or_environment",
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    values = module.read_properties(property_path)
    environment = values.get("environment")
    rest_base = values.get("restBaseUrl")
    if not isinstance(environment, str) or not environment.strip() or not isinstance(rest_base, str) or not rest_base.strip():
        raise ProviderContractError(
            "authenticated Fusion target configuration is incomplete",
            "transport_or_environment",
        )
    environment = environment.strip()
    if expected_environment is not None and expected_environment != environment:
        raise ProviderContractError(
            "expected environment does not match authenticated Fusion configuration",
            "transport_or_environment",
        )
    releases = {
        release
        for key in ("fusionRelease", "quarterlyRelease")
        if values.get(key) is not None
        for release in [_trusted_quarterly_release(str(values[key]).strip())]
        if release is not None
    }
    # Ambiguous ancillary metadata is unknown, not an operation blocker.
    trusted_release = next(iter(releases)) if len(releases) == 1 else None
    if supplied_fusion_release is not None:
        _require_text(supplied_fusion_release, "supplied fusion_release", max_length=32)
        # An unverified user assertion is context, not evidence. Do not let it
        # block release-independent reads or promote it to verified metadata.
    return {
        "target_environment": environment,
        **_release_evidence(trusted_release),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    registry, rest_client = _default_paths()
    provider_contract, seeded_catalog = _default_catalog_provider_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        choices=(
            "capability",
            "discover",
            "sample",
            "check",
            "check-identity",
            "resolve-create-catalog",
            "resolve-certification-catalog",
        ),
    )
    parser.add_argument(
        "--target-environment",
        help="Optional expert mismatch assertion; target identity is resolved from authenticated FDOS configuration.",
    )
    parser.add_argument(
        "--fusion-release",
        help="Optional informational release; never a compatibility or execution gate.",
    )
    parser.add_argument("--context")
    parser.add_argument("--content-item-code")
    parser.add_argument("--content-item-name")
    parser.add_argument("--catalog-code")
    parser.add_argument("--catalog-name")
    parser.add_argument("--provider-use", choices=("certification", "general"))
    parser.add_argument("--registry", default=str(registry))
    parser.add_argument("--provider-contract", default=str(provider_contract))
    parser.add_argument("--seeded-catalog-dir", default=str(seeded_catalog))
    parser.add_argument("--rest-client", default=str(rest_client))
    parser.add_argument("--properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--project-root")
    parser.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        registry = load_registry(Path(args.registry))
        rest_client = Path(args.rest_client)
        properties = Path(args.properties) if args.properties else None
        authenticated_context = resolve_authenticated_context(
            rest_client=rest_client,
            properties=properties,
            expected_environment=args.target_environment,
            supplied_fusion_release=args.fusion_release,
        )
        target_environment = authenticated_context["target_environment"]
        trusted_fusion_release = authenticated_context.get("fusion_release")
        transport = CoreRestCliTransport(
            rest_client=rest_client,
            properties=properties,
            token_cache=Path(args.token_cache) if args.token_cache else None,
            expected_environment=target_environment,
            timeout=args.timeout,
        )
        capability = select_rest_api_capability(
            registry,
            transport,
            target_environment=target_environment,
            trusted_fusion_release=trusted_fusion_release,
        )
        registry = dict(registry)
        registry["parent_resource"] = capability["selected_resource"]
        if args.operation == "capability":
            if any(
                (
                    args.context,
                    args.content_item_code,
                    args.content_item_name,
                    args.catalog_code,
                    args.catalog_name,
                    args.provider_use,
                )
            ):
                raise ProviderContractError("capability does not accept content or catalog selectors")
            result = capability
        elif args.operation == "discover":
            if any(
                (
                    args.context,
                    args.content_item_code,
                    args.content_item_name,
                    args.catalog_code,
                    args.catalog_name,
                    args.provider_use,
                )
            ):
                raise ProviderContractError("discover does not accept context, item, or catalog selectors")
            result = discover(
                registry,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
            )
        elif args.operation == "sample":
            if not args.context or any(
                (
                    args.content_item_code,
                    args.content_item_name,
                    args.catalog_code,
                    args.catalog_name,
                    args.provider_use,
                )
            ):
                raise ProviderContractError("sample requires context and does not accept item or catalog selectors")
            result = sample_context(
                registry,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
                context_name=args.context,
            )
        elif args.operation == "check":
            if (
                not args.context
                or not args.content_item_code
                or any(
                    (
                        args.content_item_name,
                        args.catalog_code,
                        args.catalog_name,
                        args.provider_use,
                    )
                )
            ):
                raise ProviderContractError("check requires context and content_item_code only")
            result = check_exact_code(
                registry,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
                context_name=args.context,
                content_item_code=args.content_item_code,
            )
        elif args.operation == "check-identity":
            if (
                not args.context
                or not args.content_item_code
                or not args.content_item_name
                or any((args.catalog_code, args.catalog_name, args.provider_use))
            ):
                raise ProviderContractError(
                    "check-identity requires context, content_item_code, and content_item_name only"
                )
            result = check_exact_identity(
                registry,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
                context_name=args.context,
                content_item_code=args.content_item_code,
                content_item_name=args.content_item_name,
            )
        elif args.operation == "resolve-create-catalog":
            if not all((args.context, args.content_item_code, args.catalog_code, args.catalog_name)):
                raise ProviderContractError(
                    "resolve-create-catalog requires context, content_item_code, catalog_code, and catalog_name"
                )
            if args.content_item_name or args.provider_use:
                raise ProviderContractError(
                    "resolve-create-catalog does not accept content_item_name or provider_use"
                )
            result = resolve_create_catalog(
                registry,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
                context_name=args.context,
                content_item_code=args.content_item_code,
                catalog_code=args.catalog_code,
                catalog_name=args.catalog_name,
            )
        else:
            if not all(
                (
                    args.context,
                    args.content_item_code,
                    args.content_item_name,
                    args.catalog_code,
                    args.catalog_name,
                    args.provider_use,
                )
            ):
                raise ProviderContractError(
                    "resolve-certification-catalog requires context, content_item_code, content_item_name, catalog_code, catalog_name, and provider_use"
                )
            provider, provider_sha256 = load_catalog_hdl_provider(
                Path(args.provider_contract)
            )
            result = resolve_certification_catalog(
                registry,
                provider,
                provider_sha256,
                transport,
                target_environment=target_environment,
                fusion_release=trusted_fusion_release,
                context_name=args.context,
                content_item_code=args.content_item_code,
                content_item_name=args.content_item_name,
                catalog_code=args.catalog_code,
                catalog_name=args.catalog_name,
                provider_use=args.provider_use,
                seeded_catalog_dir=Path(args.seeded_catalog_dir),
            )
        if args.operation != "capability":
            result = {**result, "environment_capability": capability}
        if bool(args.project_root) != bool(args.output):
            raise ProviderContractError("project_root and output must be supplied together")
        if args.output:
            output = _inside_project(Path(args.project_root), args.output)
            _atomic_json(output, result)
        _assert_sanitized(result)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ProviderContractError, OSError) as error:
        failure = {
            "status": "blocked",
            "failure_class": getattr(error, "failure_class", "artifact_persistence"),
            "message": str(error),
        }
        try:
            _assert_sanitized(failure)
        except ProviderContractError:
            failure = {
                "status": "blocked",
                "failure_class": "artifact_persistence",
                "message": "A diagnostic could not be rendered safely",
            }
        print(json.dumps(failure, indent=2, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
