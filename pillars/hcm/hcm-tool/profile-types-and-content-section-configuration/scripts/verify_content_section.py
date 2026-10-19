#!/usr/bin/env python3
"""Standalone GET-only setup verification; never an import validator or executor.

Raw responses and cached credentials stay in memory. Authentication and HTTP
transport belong to the shared core client; this module owns only domain reads,
exact comparisons, bounded paging, and a sanitized terminal report.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[5]
BASE = "/hcmRestApi/resources/11.13.18.05/"
TYPES = {1: "PERSON", 2: "JOB", 3: "POSITION", 4: "ORGANIZATION", 5: "TEMPLATE",
         10: "REQUISITION", 11: "PREREQUISITE", 12: "GUIDE"}
PROPERTY_KEY = ("FieldName", "ColumnName", "SourceProfileTypeCode", "SourceCode")
PROPERTY_VALUES = {"DisplayModeCode", "Label", "CustomLabel", "DisplayOrder", "DefaultValue",
                   "DefaultListValue", "ValueSetName", "ValueSetDisplayName", "InputType", "SearchFlag",
                   "AttributeLabelKey", "AttributeDisplayLabel", "InputFieldTypeMeaning", "RequiredFlag",
                   "ViewAttrbName", "ContentValueSetCode"}
ATTRIBUTES = {"ActiveFlag", "ApprovalRequiredFlag", "DefaultSectionFlag"}
SECTION_FIELDS = "ProfileTypeId,SectionId,SectionContext,Name,ContentTypeId,ApprovalRequiredFlag,DefaultFlag"
PATHS = re.compile(r"(?:profileTypeSectionsLOV|talentProfileSectionSubscribersLOV)")
LIST_OPERATION = "list_profile_content_sections"


class Blocked(ValueError):
    def __init__(self, stage, message, failure_class=None):
        super().__init__(message)
        self.stage = stage
        self.failure_class = failure_class or ("catalog_mismatch" if stage in
            {"runtime_capability", "template_catalog", "seeded_profile"} else
            "fusion_api" if stage in {"pagination", "response_validation"} else "input_validation")


def require(condition, message, stage="input_preflight"):
    if not condition:
        raise Blocked(stage, message)


def positive(value):
    return not isinstance(value, bool) and bool(re.fullmatch(r"[1-9][0-9]*", str(value)))


def validate_request(request):
    require(isinstance(request, dict), "Request must be a JSON object.")
    allowed = {"operation", "method", "environment", "profile_type_id", "profile_type_key",
               "section_context", "section_name", "content_type_id", "template_name",
               "expected_attributes", "expected_properties", "expected_subscribers",
               "expected_catalog", "effective_date"}
    require(not set(request) - allowed, "Unknown fields or write/payload options are not permitted.")
    require(request.get("operation") in ("verify_profile_content_section", LIST_OPERATION),
            "Only section verification or inventory is supported.")
    require(request.get("method", "GET") == "GET", "Only GET is permitted.")
    require(positive(request.get("profile_type_id")), "An exact seeded profile identity is required.")
    require(TYPES.get(int(request["profile_type_id"])) == request.get("profile_type_key"),
            "The seeded profile ID/key pair does not match.")
    require(int(request["profile_type_id"]) in {1, 2, 3, 4, 10, 11},
            "This diagnostic supports only the profile types documented by the section LOV.")
    require(isinstance(request.get("environment"), str) and request["environment"].strip(),
            "The configured environment alias is required.")
    if request["operation"] == LIST_OPERATION:
        require(not set(request) - {"operation", "method", "environment", "profile_type_id", "profile_type_key"},
                "Section inventory does not accept section filters or comparison inputs.")
        return request
    for key in ("section_context", "section_name", "template_name", "effective_date"):
        if key in request:
            require(isinstance(request[key], str) and bool(request[key].strip()), "Empty or invalid identity/date.")
    if "content_type_id" in request:
        require(positive(request["content_type_id"]), "Content type must be a positive identity.")
    require(request.get("section_context") or (request.get("section_name") and request.get("content_type_id")),
            "Supply an exact section context, or section name and content type.")
    if request.get("template_name"):
        require(positive(request.get("content_type_id")), "Template verification also requires exact content type.")
    if request.get("effective_date"):
        try:
            require(date.fromisoformat(request["effective_date"]).isoformat() == request["effective_date"], "Invalid effective date.")
        except ValueError:
            raise Blocked("input_preflight", "Effective date must be YYYY-MM-DD.") from None
    attributes = request.get("expected_attributes", {})
    require(isinstance(attributes, dict) and not set(attributes) - ATTRIBUTES,
            "Unsupported section attributes.")
    require(all(type(value) is bool for value in attributes.values()), "Section flags must be booleans.")
    properties = request.get("expected_properties", [])
    require(isinstance(properties, list), "Expected properties must be a list.")
    require(not properties, "Property comparison needs a supported Profile Types metadata provider and is unavailable.", "catalog_mismatch")
    keys = []
    for row in properties:
        require(isinstance(row, dict) and set(PROPERTY_KEY) <= set(row), "Each property needs all four identity fields.")
        require(all(isinstance(row[key], str) and row[key].strip() for key in PROPERTY_KEY[:2]),
                "FieldName and ColumnName must be nonempty strings.")
        require(all(row[key] is None or isinstance(row[key], str) for key in PROPERTY_KEY[2:]),
                "Property source identity must be a string or null.")
        require(not set(row) - set(PROPERTY_KEY) - PROPERTY_VALUES, "Unsupported property field.")
        require(all(value is None or isinstance(value, (str, bool, int, float)) for value in row.values()),
                "Property fields must be scalar values.")
        require(bool(set(row) & PROPERTY_VALUES), "Each property needs a value to compare.")
        keys.append(tuple(row[key] for key in PROPERTY_KEY))
    require(len(keys) == len(set(keys)), "Duplicate expected property identity.")
    subscribers = request.get("expected_subscribers", [])
    require(isinstance(subscribers, list), "Expected subscribers must be a list of exact codes.")
    require(all(isinstance(code, str) and code.strip() for code in subscribers), "Invalid subscriber code.")
    require(len(subscribers) == len(set(subscribers)), "Duplicate subscriber code.")
    catalog = request.get("expected_catalog")
    if catalog is not None:
        require(isinstance(catalog, dict) and set(catalog) == {"code", "property_key", "value_set_name"},
                "Catalog comparison requires exact code, property_key, and value_set_name.")
        require(all(isinstance(catalog[k], str) and catalog[k].strip() for k in ("code", "value_set_name")),
                "Catalog identities must be nonempty strings.")
        require(isinstance(catalog["property_key"], dict) and set(catalog["property_key"]) == set(PROPERTY_KEY),
                "Catalog assignment requires the four-field property key.")
        require(all(v is None or isinstance(v, str) for v in catalog["property_key"].values()), "Invalid catalog property key.")
        require(positive(request.get("content_type_id")), "Catalog verification requires exact content type.")
        raise Blocked("catalog_mismatch", "Content-item assignment comparison needs a supported Profile Types metadata provider and is unavailable.")
    return request


def build_plan(request):
    validate_request(request)
    inventory = request["operation"] == LIST_OPERATION
    return {"workflow": "ptcs.read-only-verification", "status": "planned", "read_only": True,
            "operation": request["operation"],
            "allowed_methods": ["GET"], "writes_performed": False,
            "stages": (["input_preflight", "authentication_preflight", "profile_section_lov", "section_inventory", "report"]
                       if inventory else ["input_preflight", "authentication_preflight", "template_catalog",
                                          "profile_section_lov", "exact_section", "requested_component_capabilities", "report"]),
            "terminal": True, "configuration_readiness": "not_evaluated",
            "next_action": "Run this same verification request; no export, import, or execution follows."}


class CoreGetClient:
    def __init__(self, environment, properties, token_cache):
        sys.path.insert(0, str(ROOT / "core/fusion-api/rest-api-client/scripts"))
        sys.path.insert(0, str(ROOT / "core/auth/fusion-oauth-authentication/scripts"))
        from fusion_auth import load_file_cached_access_token, read_properties
        from fusion_rest_client import main
        self.main, self.properties = main, properties
        try:
            props = read_properties(properties)
            require(props.get("environment") == environment, "Configured environment alias differs from the request.", "authentication_preflight")
            self.token = load_file_cached_access_token(token_cache, props)
        except Blocked:
            raise
        except Exception:
            raise Blocked("authentication_preflight", "Unable to read local authentication configuration.", "auth_authz") from None
        if not self.token:
            raise Blocked("authentication_preflight", "Fusion login is required; this verifier does not refresh credentials.", "auth_authz")

    def get(self, resource, query):
        require(bool(PATHS.fullmatch(resource)), "Resource is outside the GET allowlist.", "request_preflight")
        # Token is assigned in process memory, never passed in an OS command line.
        argv = ["fusion_rest_client.py", BASE + resource, "--method", "GET", "--properties", str(self.properties),
                "--access-token", self.token, "--timeout", "20", "--header", "REST-Framework-Version=9"]
        for key, value in query.items():
            argv.extend(["--query", f"{key}={value}"])
        previous = sys.argv
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            sys.argv = argv
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.main()
            response = json.loads(stdout.getvalue())
            require(isinstance(response, dict), "Unexpected response shape.", "response_validation")
            return response
        except Blocked:
            raise
        except Exception as exc:
            status = getattr(exc, "status_code", None)
            failure = "auth_authz" if status in {401, 403} else "fusion_api" if status else "transport_environment"
            message = f"GET failed (HTTP {status})." if status else "GET failed; transport or response could not be verified."
            raise Blocked("runtime_get", message, failure) from None
        finally:
            sys.argv = previous
            stdout.close()
            stderr.close()


def skeleton(request):
    result = {"operation": request.get("operation"), "workflow": "ptcs.read-only-verification",
            "source_environment": request.get("environment"), "status": "blocked", "read_only": True,
            "target": {"profile_type_key": request.get("profile_type_key"),
                       "section_name": request.get("section_name"), "section_context": request.get("section_context")},
            "methods_used": [], "writes_performed": False, "request_ledger": [], "capability_evidence": [],
            "existence_status": "blocked", "pagination_complete": False, "target_pagination_complete": False,
            "component_results": {key: "not_requested" for key in
                                  ("template", "section_attributes", "properties", "content_item_catalog",
                                   "catalog_assignment", "subscriber_catalog", "subscriber_assignments", "model_parent")},
            "differences": [], "unverifiable": [], "errors": [],
            "configuration_readiness": "not_evaluated", "immutable_preview_generated": False,
            "next_action": "Resolve reported blockers; verification never authorizes submission."}
    if request.get("operation") == LIST_OPERATION:
        result.update(sections=[], section_count=None, existence_status="not_evaluated",
                      coverage="section_inventory_only",
                      visibility="Sections visible to the authenticated user; not a full configuration snapshot.")
    return result


class Verifier:
    def __init__(self, client, result):
        self.client, self.result, self.started = client, result, time.monotonic()

    def get(self, resource, query):
        require(bool(PATHS.fullmatch(resource)), "Resource is outside the GET allowlist.", "request_preflight")
        if time.monotonic() - self.started >= 120:
            raise Blocked("runtime_get", "Verification exceeded its 120-second request budget.", "process_timeout")
        entry = {"method": "GET", "resource": re.sub(r"/[0-9]+(?=/|$)", "/{id}", resource), "status": "attempted"}
        self.result["request_ledger"].append(entry)
        self.result["methods_used"] = ["GET"]
        response = self.client.get(resource, query)
        entry["status"] = "succeeded"
        return response

    def collection(self, resource, fields, order_by, **query):
        rows, fingerprints, offset = [], set(), 0
        for _ in range(50):
            page = self.get(resource, dict(query, fields=fields, orderBy=order_by, onlyData="true", limit=100, offset=offset))
            require(isinstance(page.get("items"), list) and type(page.get("hasMore")) is bool,
                    "Missing collection or explicit pagination state.", "pagination")
            items = page["items"]
            require(all(isinstance(row, dict) for row in items), "Invalid collection row.", "pagination")
            if "offset" in page:
                require(type(page["offset"]) is int and page["offset"] == offset, "Returned page offset differs from the request.", "pagination")
            fingerprint = hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()
            require(fingerprint not in fingerprints, "Repeated page; completeness cannot be proved.", "pagination")
            fingerprints.add(fingerprint)
            rows.extend(items)
            if not page["hasMore"]:
                return rows
            require(bool(items), "Empty page with hasMore=true.", "pagination")
            offset += len(items)
        raise Blocked("pagination", "Page limit reached before hasMore=false.")

    def capability(self, partial, path):
        data = self.get("describe.openapi", {"partialDescriptionForCatalogOpenAPI": partial})
        paths = data.get("paths")
        require(isinstance(paths, dict), "Runtime OpenAPI paths unavailable.", "runtime_capability")
        normalize = lambda value: re.sub(r"\{[^}]+\}", "{id}", value)
        expected = normalize(BASE + path)
        # Swagger 2 uses basePath; OpenAPI 3 uses servers[].url. Server URLs
        # are metadata only: never follow them or replace the configured host.
        bases = {""}
        if isinstance(data.get("basePath"), str):
            bases.add(data["basePath"].rstrip("/"))
        servers = data.get("servers", [])
        require(isinstance(servers, list), "Invalid OpenAPI server metadata.", "runtime_capability")
        for server in servers:
            if isinstance(server, dict) and isinstance(server.get("url"), str):
                bases.add(urlsplit(server["url"]).path.rstrip("/"))
        matches = [operations for candidate, operations in paths.items()
                   if any(normalize(base + candidate) == expected for base in bases)
                   and isinstance(operations, dict) and isinstance(operations.get("get"), dict)]
        # Counts and supported method names only; never record server URLs,
        # schema contents, opaque paths, or protected response fields.
        operations = {method for candidate, methods in paths.items() if normalize(candidate).endswith("/" + normalize(path))
                      and isinstance(methods, dict) for method in methods
                      if method in {"get", "post", "put", "patch", "delete"}}
        self.result["capability_evidence"].append({"resource": partial, "exact_get_matches": len(matches),
                                                  "advertised_resource_methods": sorted(operations)})
        require(len(matches) == 1, "Exact collection GET is absent or ambiguous in runtime metadata.", "runtime_capability")

    def compare(self, name, actual, expected):
        if any(key not in actual for key in expected):
            self.result["component_results"][name] = "unverifiable"
            self.result["unverifiable"].append(name + ": required response fields are absent")
        elif all(type(actual[key]) is type(value) and actual[key] == value for key, value in expected.items()):
            self.result["component_results"][name] = "matches"
        else:
            self.result["component_results"][name] = "differs"
            self.result["differences"].append(name)

    def run(self, request):
        components = self.result["component_results"]
        if request.get("template_name"):
            components["template"] = "unverifiable"
            templates = self.collection("profileTypeSectionsLOV", "Name,SectionId,SectionContext,ContentTypeId,ProfileTypeId,TemplateFlag,DffContextName,Description,DisplayOrder,ApprovalRequiredFlag,DefaultFlag", "Name",
                                        finder="findTemplateSections")
            matches = [row for row in templates if row.get("Name") == request["template_name"]
                       and str(row.get("ContentTypeId")) == str(request["content_type_id"]) and row.get("TemplateFlag") is True]
            require(len(matches) == 1, "Exact predefined template is missing or ambiguous.", "template_catalog")
            components["template"] = "matches"
        profile_id = int(request["profile_type_id"])
        # The documented section LOV is the primary existence/approval read,
        # not a fallback after a rejected environment-specific resource call.
        # Its supported ProfileTypeId enum is checked before authentication.
        raw_sections = self.collection("profileTypeSectionsLOV", SECTION_FIELDS, "SectionId",
                                       finder=f"findByProfileTypeId;ProfileTypeId={profile_id}")
        require(all(str(row.get("ProfileTypeId")) == str(profile_id) for row in raw_sections),
                "Section finder did not preserve the exact seeded profile identity.", "seeded_profile")
        sections = []
        for row in raw_sections:
            section = dict(row)
            if "Name" in row:
                section["SectionName"] = row["Name"]
            if "DefaultFlag" in row:
                section["DefaultSectionFlag"] = row["DefaultFlag"]
            sections.append(section)
        if request["operation"] == LIST_OPERATION:
            inventory, identities, contexts = [], set(), set()
            for section in sections:
                require(positive(section.get("SectionId")) and
                        all(isinstance(section.get(key), str) and section[key].strip()
                            for key in ("SectionContext", "SectionName")),
                        "Section inventory identity fields are missing or invalid.", "response_validation")
                identity, context = str(section["SectionId"]), section["SectionContext"]
                require(identity not in identities and context not in contexts,
                        "Duplicate section identity; inventory completeness cannot be proved.", "response_validation")
                identities.add(identity)
                contexts.add(context)
                # Display only business identities and documented flags. Internal
                # surrogate IDs and unrequested response fields remain in memory.
                item = {key: section[key] for key in ("SectionContext", "SectionName")}
                for key in ("ApprovalRequiredFlag", "DefaultSectionFlag"):
                    value = section.get(key)
                    require(value is None or type(value) is bool,
                            "Section inventory flag has an invalid type.", "response_validation")
                    item[key] = value  # Missing/null means unknown, never false.
                inventory.append(item)
            # Publish only after all pages and identities have been validated.
            self.result.update(sections=inventory, section_count=len(inventory),
                               pagination_complete=True, target_pagination_complete=True)
            return
        identity_fields = {"SectionContext"} if request.get("section_context") else {"SectionName", "ContentTypeId"}
        require(all(identity_fields <= set(row) for row in sections), "Section identity fields are missing.", "exact_section")
        self.result["pagination_complete"] = True
        self.result["target_pagination_complete"] = True
        if request.get("section_context"):
            matches = [row for row in sections if row.get("SectionContext") == request["section_context"]]
        else:
            matches = [row for row in sections if row.get("SectionName") == request["section_name"]
                       and str(row.get("ContentTypeId")) == str(request["content_type_id"])]
        self.result["existence_status"] = "exists" if len(matches) == 1 else "not_found" if not matches else "ambiguous"
        if len(matches) != 1:
            return
        section = matches[0]
        require(positive(section.get("SectionId")), "Section child identity unavailable.", "exact_section")
        if request.get("expected_attributes"):
            self.compare("section_attributes", section, request["expected_attributes"])
        if request.get("content_type_id") and str(section.get("ContentTypeId")) != str(request["content_type_id"]):
            components["template"] = "differs"
            self.result["differences"].append("section_content_type")
        if request.get("expected_subscribers"):
            catalog = self.collection(
                "talentProfileSectionSubscribersLOV", "SourceCode", "SourceCode"
            )
            require(all(isinstance(row.get("SourceCode"), str) and row["SourceCode"].strip()
                        for row in catalog),
                    "Subscriber catalog identity fields are missing.", "subscriber_catalog")
            expected = request["expected_subscribers"]
            matches_by_code = {
                code: [row for row in catalog if row["SourceCode"] == code]
                for code in expected
            }
            require(all(len(matches) <= 1 for matches in matches_by_code.values()),
                    "Subscriber catalog identity is ambiguous.", "subscriber_catalog")
            components["subscriber_catalog"] = (
                "matches" if all(matches_by_code.values()) else "differs"
            )
            components["subscriber_assignments"] = "unverifiable"
            self.result["unverifiable"].append(
                "subscriber_assignments: the public subscriber LOV establishes catalog presence, not section assignment"
            )


def verify(request, client_factory):
    # Validate before constructing the client: even reading a token cache is
    # forbidden for a malformed or write-capable request.
    validate_request(request)
    result = skeleton(request)
    if request.get("effective_date"):
        result["unverifiable"].append("effective_date: scheduled activation is not exposed by these setup reads")
    for expected, component in (("expected_attributes", "section_attributes"), ("expected_properties", "properties"),
                                ("template_name", "template"),
                                ("expected_catalog", "content_item_catalog"), ("expected_catalog", "catalog_assignment"),
                                ("expected_subscribers", "subscriber_catalog"), ("expected_subscribers", "subscriber_assignments")):
        if request.get(expected):
            result["component_results"][component] = "unverifiable"
    try:
        Verifier(client_factory(), result).run(request)
        result["status"] = "complete" if (request["operation"] == LIST_OPERATION and result["pagination_complete"]
                                          or result["existence_status"] in {"exists", "not_found"}) else "blocked"
        if result["status"] == "complete" and (result["unverifiable"] or
                (result["existence_status"] == "exists" and "unverifiable" in result["component_results"].values())):
            result["status"] = "partial"
        result["next_action"] = "Read-only report complete; no configuration, preview, export, or import was performed."
    except Blocked as exc:
        result["status"] = "partial" if result["existence_status"] == "exists" else "blocked"
        if exc.stage == "pagination":
            result["pagination_complete"] = False
        result["errors"].append({"stage": exc.stage, "failure_class": exc.failure_class, "message": str(exc)})
    result["differences"] = sorted(set(result["differences"]) | {
        name for name, outcome in result["component_results"].items() if outcome == "differs"})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--request", type=Path)
    source.add_argument("--input-stdin", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate and plan locally without credentials or network.")
    parser.add_argument("--properties", type=Path, default=ROOT / "core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    args = parser.parse_args()
    try:
        request = json.loads(sys.stdin.read() if args.input_stdin else args.request.read_text(encoding="utf-8"))
        plan = build_plan(request)
        result = plan if args.dry_run else verify(request, lambda: CoreGetClient(request["environment"], args.properties, args.token_cache))
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in {"planned", "complete"} else 1
    except (Blocked, OSError, ValueError):
        print(json.dumps({"status": "blocked", "stage": "input_preflight", "failure_class": "input_validation",
                          "message": "Invalid verification input; no business request was submitted.", "writes_performed": False}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
