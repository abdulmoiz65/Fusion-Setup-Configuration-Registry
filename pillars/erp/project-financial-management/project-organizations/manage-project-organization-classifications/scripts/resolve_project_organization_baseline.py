#!/usr/bin/env python3
"""Collect a complete, read-only Organization baseline through shared core services.

Default execution is a local plan. Live reads require --execute after the caller
has passed the selected task's workflow gates and resolved --rest-framework-version
from the selected core client/workflow. No mutation API is implemented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit, unquote

REPO = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO / "core/fusion-api/rest-api-client/scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rest_client_common import read_properties
from trusted_http import validate_destination, normalize_service_origin
from validate_project_organization_classifications_hdl import as_date, dates, identity, text

ORGANIZATIONS = "/hcmRestApi/resources/11.13.18.05/organizations"
IDENTITY_FIELDS = ("OrganizationId", "Name", "EffectiveStartDate", "EffectiveEndDate")
CLASS_FIELDS = ("OrganizationId", "ClassificationCode", "Status", "EffectiveStartDate", "EffectiveEndDate")
SNAPSHOT_FIELDS = set(IDENTITY_FIELDS + CLASS_FIELDS)


class BaselineError(ValueError):
    def __init__(self, message, failure_class="Fusion API"):
        super().__init__(message)
        self.failure_class = failure_class


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def exact_name_query(name):
    text(name, "organization_name")
    return "Name='" + name.replace("'", "''") + "'"


def validate_framework_version(value):
    version = str(value) if value is not None else ""
    if not re.fullmatch(r"[1-9][0-9]*", version):
        raise BaselineError("Resolve --rest-framework-version from the selected core client/workflow before execution.",
                            "input validation")
    return version


def destination(endpoint, target):
    if not isinstance(endpoint, str) or endpoint.startswith("//"):
        raise BaselineError("Invalid returned REST link.")
    url = urljoin(target + "/", endpoint)
    try:
        validate_destination(url, target)
    except ValueError as exc:
        raise BaselineError("REST link leaves the selected HTTPS environment.", "transport/environment") from exc
    path = unquote(urlsplit(url).path)
    if path != ORGANIZATIONS:
        raise BaselineError("REST link leaves the declared organizations resource.")
    return url


def links(row):
    value = row.get("links", [])
    if not isinstance(value, list) or any(not isinstance(link, dict) for link in value):
        raise BaselineError("Invalid REST links collection.")
    return value


class CoreReader:
    """Delegate authentication, transport and read retries to the core client."""
    def __init__(self, properties, target, open_browser=False, *, framework_version=None):
        self.properties, self.target, self.open_browser = properties, target, open_browser
        # The workflow selects the version; this single-equality query works with
        # both query-by-example and expanded grammar. Never choose a pillar default.
        self.framework_version = validate_framework_version(framework_version)

    def __call__(self, url):
        destination(url, self.target)  # Before invoking any credential-bearing service.
        with tempfile.TemporaryDirectory(prefix="project-organization-read-") as temporary:
            output = Path(temporary) / "response.json"
            parts = urlsplit(url)
            endpoint = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
            command = [sys.executable,
                       str(REPO / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"),
                       endpoint, "--method", "GET", "--properties", str(self.properties),
                       "--header", "Accept=application/json", "--header",
                       "REST-Framework-Version=" + self.framework_version,
                       "--output", str(output), "--timeout", "60",
                       "--open-browser" if self.open_browser else "--no-open-browser"]
            for key, value in parse_qsl(parts.query, keep_blank_values=True):
                command.extend(("--query", key + "=" + value))
            try:
                result = subprocess.run(command, cwd=REPO, capture_output=True, text=True,
                                        timeout=180, check=False)
                if result.returncode:
                    # Core owns detailed diagnostics; never copy raw response bodies or OAuth output.
                    status = re.search(r"^Error: HTTP ([1-5][0-9]{2}) calling ", result.stderr, re.MULTILINE)
                    if status:
                        code = int(status.group(1))
                        category = "auth/authz" if code in {401, 403} else "Fusion API"
                        raise BaselineError(f"Core baseline GET failed with HTTP {code}.", category)
                    raise BaselineError("Core REST client failed; no complete baseline evidence was produced.",
                                        "transport/environment")
                if "HTTP 200" not in result.stdout.splitlines():
                    raise BaselineError("Baseline GET did not return HTTP 200.")
                return json.loads(output.read_text(encoding="utf-8"))
            except subprocess.TimeoutExpired as exc:
                raise BaselineError("Core baseline GET timed out; no complete evidence was produced.", "process timeout") from exc
            except OSError as exc:
                raise BaselineError("Core baseline GET or response handoff failed.", "transport/environment") from exc
            except (json.JSONDecodeError, UnicodeError) as exc:
                raise BaselineError("Baseline GET returned invalid JSON.") from exc


class Collector:
    def __init__(self, getter, target, as_of, max_pages=1000):
        self.getter, self.target, self.as_of = getter, target, as_of
        self.max_pages = max_pages
        self.audit = []

    def collection(self, endpoint, stage, query=None):
        initial = destination(endpoint, self.target)
        parsed = urlsplit(initial)
        base_query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        # Returned links must not narrow the declared complete collection.
        allowed = {"q", "effectiveDate", "limit", "offset"}
        if set(base_query) - allowed:
            raise BaselineError("Returned collection link has unsupported query parameters.")
        expected = dict(query or {})
        expected["effectiveDate"] = self.as_of
        if "q" in base_query and base_query["q"] != expected.get("q"):
            raise BaselineError("Returned collection link changes the requested filter.")
        if "effectiveDate" in base_query and base_query["effectiveDate"] != self.as_of:
            raise BaselineError("Returned collection link changes the effective date.")
        expected.update(limit="100", offset="0")
        current = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(expected), ""))
        rows, visited, page_hashes = [], set(), set()
        for page in range(self.max_pages):
            current = destination(current, self.target)
            if current in visited:
                raise BaselineError("Pagination loop detected.")
            visited.add(current)
            record = {"stage": stage, "page": page + 1, "requestSha256": digest(current),
                      "startedAt": stamp(), "status": "reading"}
            self.audit.append(record)
            payload = self.getter(current)
            if not isinstance(payload, dict) or not isinstance(payload.get("items"), list) or type(payload.get("hasMore")) is not bool:
                raise BaselineError("Collection is missing items or a Boolean hasMore; completeness is unknown.")
            items = payload["items"]
            if any(not isinstance(row, dict) for row in items):
                raise BaselineError("Collection contains a malformed row.")
            offset = int(dict(parse_qsl(urlsplit(current).query))["offset"])
            if "offset" in payload and (type(payload["offset"]) is not int or payload["offset"] != offset):
                raise BaselineError("Pagination response offset does not match the request.")
            if "count" in payload and (type(payload["count"]) is not int or payload["count"] != len(items)):
                raise BaselineError("Pagination response count does not match its items.")
            # A server ignoring offset must not masquerade as a complete read.
            fingerprint = digest(items)
            if items and fingerprint in page_hashes:
                raise BaselineError("Pagination repeated an earlier page.")
            page_hashes.add(fingerprint)
            record.update(status="read", endedAt=stamp(), httpStatus=200, count=len(items),
                          hasMore=payload["hasMore"], responseSha256=digest(payload),
                          rows=[{k: v for k, v in row.items() if k in SNAPSHOT_FIELDS} for row in items])
            rows.extend(items)
            next_links = [link for link in links(payload) if link.get("rel") == "next"]
            if not payload["hasMore"]:
                if next_links:
                    raise BaselineError("Pagination has contradictory terminal and next-page markers.")
                return rows
            if not items or len(next_links) > 1:
                raise BaselineError("Pagination cannot make unambiguous forward progress.")
            next_offset = offset + len(items)
            if next_links:
                nxt = destination(next_links[0].get("href"), self.target)
                parts = urlsplit(nxt)
                params = dict(parse_qsl(parts.query, keep_blank_values=True))
                if parts.path != parsed.path or set(params) - allowed:
                    raise BaselineError("Next-page link changes the collection.")
                if params.get("offset") != str(next_offset):
                    raise BaselineError("Next-page link skips or repeats records.")
                for key in ("q", "effectiveDate"):
                    if key in params and params[key] != expected.get(key):
                        raise BaselineError("Next-page link changes the requested filter or effective date.")
            # Keep original query/date, use the server's actual page length.
            expected["offset"] = str(next_offset)
            current = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(expected), ""))
        raise BaselineError("Baseline pagination exceeded its bounded page limit.", "process timeout")

    def collect(self, name, selected_id=None, requested_target=None):
        if requested_target not in {None, "PTO", "PEO", "BOTH"}:
            raise BaselineError("Select PTO, PEO or BOTH.", "input validation")
        rows = self.collection(ORGANIZATIONS, "organization-search", {"q": exact_name_query(name)})
        matches, by_id = [], {}
        for row in rows:
            if row.get("Name") != name:
                raise BaselineError("Exact-name response contains a different organization name.")
            try:
                oid = identity(row.get("OrganizationId"))
                period = dates(row)
                if not period[0] <= as_date(self.as_of) <= period[1]:
                    raise ValueError("Outside effective range")
                match = {k: row[k] for k in IDENTITY_FIELDS}
            except (ValueError, KeyError) as exc:
                raise BaselineError("Organization identity or effective range is invalid.", "input validation") from exc
            if oid in by_id and by_id[oid] != match:
                raise BaselineError("Conflicting effective organization records require reconciliation.", "input validation")
            if oid not in by_id:
                matches.append(match)
            by_id[oid] = match
        if not by_id:
            raise BaselineError("Exact-name lookup found no existing organization.", "input validation")
        if selected_id is None and len(by_id) != 1:
            raise BaselineError("Multiple OrganizationIds match; select one with --organization-id.", "input validation")
        oid = identity(selected_id) if selected_id is not None else next(iter(by_id))
        if oid not in by_id:
            raise BaselineError("Selected OrganizationId is not in the complete search.", "input validation")
        selected_rows = [row for row in rows if identity(row["OrganizationId"]) == oid]
        classes = []
        for row in selected_rows:
            try:
                text(row.get("ClassificationCode"), "ClassificationCode")
                if row.get("Status") not in {"A", "I"}:
                    raise ValueError("Invalid classification status")
                classes.append({k: row[k] for k in CLASS_FIELDS})
            except (KeyError, ValueError, TypeError) as exc:
                raise BaselineError("Classification code or status is missing; classification visibility is incomplete.") from exc
        # These flags are issued only after every required collection completed.
        return {"TargetEnvironment": self.target, "EvidenceRef": "baseline:" + digest(self.audit),
                "Fresh": True, "CollectedAt": stamp(), "AsOfDate": self.as_of,
                "OrganizationSearchComplete": True, "OrganizationMatches": matches,
                "SelectedOrganization": by_id[oid], "SelectionConfirmed": selected_id is not None,
                "ClassificationsComplete": True, "Classifications": classes,
                "OrgInformationComplete": False, "OrgInformation": [],
                "OrgInformationReadStatus": "not_read_add_classifications_only",
                "RequestedTargetClassification": requested_target,
                "ParentReference": {"Attribute": "OrganizationId", "Value": oid,
                                    "OrganizationId": oid, "Verified": True},
                "ReadAudit": self.audit}


def collect_bulk_baseline(request, getter, target, as_of, run_id, audit=None):
    """Fresh reads per requested name; publish no aggregate on any failed row."""
    from bulk_project_organization_classifications import normalize_bulk_request
    from validate_project_organization_classifications_hdl import resolve_classification_state
    normalize_bulk_request(request)
    text(run_id, "run_id")
    if request["target_environment"] != target:
        raise BaselineError("Bulk request target differs from the configured environment.", "input validation")
    records = []
    for row in request["organizations"]:
        collector = Collector(getter, target, as_of)
        try:
            proof = collector.collect(row["organization_name"])
            proof["ValidationRunId"] = run_id
            item = {k: v for k, v in row.items() if k != "update_existing_pto_permissions"}
            resolve_classification_state(item, proof)
            records.append(proof)
        finally:
            if audit is not None:
                audit.extend(collector.audit)
    return {"TargetEnvironment": target, "RunId": run_id, "Organizations": records}


def output_preflight(output, project):
    project = project.absolute()
    output = output.absolute()
    if any(p.is_symlink() for p in (project, *project.parents, output, *output.parents)):
        raise BaselineError("Symlinks are not allowed in baseline output paths.", "artifact persistence")
    if not project.is_dir():
        raise BaselineError("Select an existing project workspace.", "input validation")
    try:
        relative = output.relative_to(project)
    except ValueError as exc:
        raise BaselineError("Baseline output must be inside the selected project workspace.", "artifact persistence") from exc
    if ".." in relative.parts or len(relative.parts) < 2 or relative.parts[0] not in {"artifacts", "baselines"}:
        raise BaselineError("Baseline output must be under project artifacts or baselines.", "artifact persistence")
    run_dir = output.with_name(output.name + ".run")
    if output.exists() or run_dir.exists():
        raise BaselineError("Baseline output or run directory already exists; choose a new run path.", "artifact persistence")
    return output, run_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--organization-name")
    selection.add_argument("--bulk-request", type=Path)
    parser.add_argument("--run-id", help="Required for a bulk baseline; durable current workflow run ID")
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--target-environment", required=True)
    parser.add_argument("--organization-id")
    parser.add_argument("--requested-target-classification", choices=("PTO", "PEO", "BOTH"),
                        help="Explicit addition intent only; omission preserves all classifications. Baseline reads no PTO EFF.")
    parser.add_argument("--properties", type=Path, default=REPO / "core/auth/fusionEnv.properties")
    parser.add_argument("--rest-framework-version",
                        help="Effective version resolved from the selected core client/workflow; required with --execute")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    parser.add_argument("--open-browser", action="store_true", help="Only when workflow permits OAuth browser login")
    args = parser.parse_args(argv)
    diagnostic, run_dir, collector = None, None, None
    try:
        bulk = None
        if args.bulk_request:
            from bulk_project_organization_classifications import normalize_bulk_request
            bulk = normalize_bulk_request(json.loads(args.bulk_request.read_text(encoding="utf-8")))
            text(args.run_id, "run_id")
            if args.organization_id or args.requested_target_classification:
                raise BaselineError("Bulk identity/scope comes only from organizations entries.", "input validation")
        else:
            exact_name_query(args.organization_name)
        when = as_date(args.as_of_date).isoformat()
        if args.organization_id is not None:
            identity(args.organization_id)
        framework_version = (validate_framework_version(args.rest_framework_version)
                             if args.execute or args.rest_framework_version is not None else None)
        output, run_dir = output_preflight(args.output, args.project_root)
        try:
            props = read_properties(args.properties)
            target = normalize_service_origin(props["restBaseUrl"])
            validate_destination(args.target_environment, target)
        except (ValueError, KeyError, OSError) as exc:
            raise BaselineError("Selected target must match a valid configured Fusion HTTPS origin.", "transport/environment") from exc
        if bulk is not None and bulk["target_environment"] != target:
            raise BaselineError("Bulk request target differs from configured environment.", "input validation")
        if not args.execute:
            print(json.dumps({"status": "planned", "operation": "GET organization baseline",
                              "target": target, "asOfDate": when, "output": str(output),
                              "restFrameworkVersion": framework_version,
                              "querySyntax": "single equality"}))
            return 0
        # Reserve a new run before authenticating or making any external read.
        run_dir.mkdir(parents=True, exist_ok=False)
        diagnostic = {"status": "failed", "stage": "baseline-read", "environment": target,
                      "startedAt": stamp(), "artifactRefs": [], "externalIds": [],
                      "restFrameworkVersion": framework_version, "querySyntax": "single equality",
                      "coreClient": "core.fusion-api.rest-api-client"}
        collector = Collector(CoreReader(args.properties, target, args.open_browser,
                                        framework_version=framework_version), target, when)
        if bulk is not None:
            evidence = collect_bulk_baseline(bulk, collector.getter, target, when, args.run_id, collector.audit)
        else:
            evidence = collector.collect(args.organization_name, args.organization_id, args.requested_target_classification)
        diagnostic.update(status="success", stage="complete", failureClass=None,
                          message="Complete baseline collected.", recommendedAction="Evaluate the task request against this baseline.")
        diagnostic["artifactRefs"] = [str(output.relative_to(args.project_root.absolute()))]
        diagnostic["endedAt"] = stamp()
        diagnostic["readAudit"] = collector.audit
        # Persist provenance before publishing the evidence consumed downstream.
        with (run_dir / "read-audit.json").open("x", encoding="utf-8") as stream:
            json.dump({"status": "collected", "readAudit": collector.audit}, stream, indent=2)
        with output.open("x", encoding="utf-8") as stream:
            json.dump(evidence, stream, indent=2)
        with (run_dir / "diagnostic.json").open("x", encoding="utf-8") as stream:
            json.dump(diagnostic, stream, indent=2)
        print(json.dumps({"status": "success", "evidence": str(output), "diagnostic": str(run_dir / "diagnostic.json")}))
        return 0
    except (ValueError, OSError) as exc:
        category = getattr(exc, "failure_class", "artifact persistence" if isinstance(exc, OSError) else "input validation")
        message = str(exc) if isinstance(exc, BaselineError) else "Baseline input or artifact validation failed."
        if diagnostic is not None:
            diagnostic.update(status="failed", failureClass=category, message=message, endedAt=stamp(),
                              recommendedAction="Resolve the reported failure and rerun into a new output path.",
                              readAudit=collector.audit if collector else [])
            try:
                with (run_dir / "failure.json").open("x", encoding="utf-8") as stream:
                    json.dump(diagnostic, stream, indent=2)
            except OSError:
                message += " Failure diagnostic could not be persisted."
        print(json.dumps({"status": "failed", "failureClass": category, "message": message}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
