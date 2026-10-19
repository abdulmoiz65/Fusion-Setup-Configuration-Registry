#!/usr/bin/env python3
"""Preview and execute a country-scoped Supplier Notification attachment add.

Live capability is enabled. Invocation still requires an authorized workflow
and exact-preview approval. Offline tests use an injected fake client.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import subprocess
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit

TASK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TASK_ROOT.parents[4]
RESOURCE = "/fscmRestApi/resources/11.13.18.05/newSupplierNotification"
TERRITORIES = "/fscmRestApi/resources/11.13.18.05/territoriesLOV"
CATEGORY_NAME = "TO_SUPPLIER"
ENTITY_NAME = "POZ_NEW_SUPP_DOC_CONFIG"
LIVE_ROUTE_ENABLED = True  # Local capability enabled at the user's explicit request.
FIELDS = ("DatatypeCode", "FileName", "Title", "UploadedFileName",
          "UploadedFileContentType", "FileContents", "CategoryName")


class AttachmentError(ValueError):
    """Sanitized, user-facing validation or execution failure."""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def write_private(path, value, *, exclusive=False):
    """Persist private JSON without replacing an existing execution journal."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise AttachmentError("Artifact path must not be a symlink")
    if exclusive:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(canonical(value))
            out.flush()
            os.fsync(out.fileno())
        return
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".attachment-")
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(canonical(value))
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def core_route(properties, core_repo=REPO_ROOT):
    """Bind opaque CLI selection only; Core alone reads environment properties."""
    return {"properties_path": str(Path(properties).absolute()) if properties is not None else None,
            "rest_client": str(Path(core_repo).resolve() /
                               "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py")}


def content_endpoint(href, expected):
    """Validate resource identity; leave HTTPS origin authorization to Core."""
    if not isinstance(href, str):
        raise AttachmentError("Unsafe attachment content read link")
    link = urlsplit(href)
    if (link.path != expected or link.query or link.fragment or link.username or link.password
            or link.scheme not in {"", "https"} or (link.netloc and not link.scheme)):
        raise AttachmentError("Unsafe attachment content read link")
    return href if link.scheme else expected


def file_facts(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise AttachmentError("Attachment must be a regular, non-symlink file")
    name = path.name
    if (not name or len(name) > 2048 or name in {".", ".."}
            or any(c in name for c in "/\\|") or any(ord(c) < 32 for c in name)):
        raise AttachmentError("Attachment filename is unsafe")
    content = path.read_bytes()
    if not content:
        raise AttachmentError("Attachment is empty")
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    if content.startswith(b"%PDF-"):
        mime = "application/pdf"
    elif mime == "application/pdf":
        raise AttachmentError("PDF extension does not match file signature")
    return {"basename": name, "mime_type": mime, "size_bytes": len(content),
            "sha256": digest(content), "content": content}


def payload(facts, title):
    if not isinstance(title, str) or not title.strip():
        raise AttachmentError("Attachment title must be nonempty text")
    return dict(zip(FIELDS, ("FILE", facts["basename"], title, facts["basename"],
                            facts["mime_type"],
                            base64.b64encode(facts["content"]).decode("ascii"),
                            CATEGORY_NAME)))


class CoreClient:
    """Invoke Core's REST CLI, as HCM does; never read configuration or tokens."""
    def __init__(self, properties, core_repo=REPO_ROOT):
        self.route = core_route(properties, core_repo)
        self.core_repo = Path(core_repo).resolve()

    def request(self, endpoint, *, method="GET", query=None, body=None, binary=False):
        path = urlsplit(endpoint).path
        if (not path.startswith(RESOURCE + "/") and path != RESOURCE
                and not (path == TERRITORIES and method == "GET")):
            raise AttachmentError("Endpoint is outside Supplier Notification scope")
        with tempfile.TemporaryDirectory(prefix="supplier-notification-rest-") as temporary:
            response = Path(temporary) / "response"
            command = [sys.executable, self.route["rest_client"], endpoint,
                       "--method", method, "--output", str(response), "--no-open-browser",
                       "--timeout", "60", "--callback-timeout", "30",
                       "--header", "REST-Framework-Version=9",
                       "--header", "Accept=application/json"]
            if self.route["properties_path"] is not None:
                command.extend(["--properties", self.route["properties_path"]])
            for key, value in (query or {}).items():
                command.extend(["--query", f"{key}={value}"])
            if body is not None:
                body_path = Path(temporary) / "request.json"
                write_private(body_path, body, exclusive=True)
                command.extend(["--body-file", str(body_path)])
            try:
                completed = subprocess.run(command, cwd=self.core_repo, capture_output=True,
                                           timeout=150, check=False)
            except (OSError, subprocess.TimeoutExpired):
                raise AttachmentError("Core REST execution failed or timed out; reconcile before retrying a write") from None
            if completed.returncode != 0 or not response.is_file():
                # Core diagnostics may contain sensitive data: never echo them.
                raise AttachmentError("Core REST request failed; reconcile before retrying a write")
            raw = response.read_bytes()
        if binary:
            return raw
        try:
            return json.loads(raw)
        except (ValueError, UnicodeError):
            raise AttachmentError("Fusion returned an unusable response") from None


def all_items(client, endpoint, query=None):
    items = []
    for page in range(100):
        response = client.request(endpoint, query={**(query or {}), "onlyData": "true",
                                                   "limit": "100", "offset": str(page * 100)})
        rows = response.get("items") if isinstance(response, dict) else None
        more = response.get("hasMore") if isinstance(response, dict) else None
        if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows) or not isinstance(more, bool):
            raise AttachmentError("Invalid collection paging response")
        items.extend(rows)
        if not more:
            return items
        if len(rows) != 100:
            raise AttachmentError("Incomplete collection page; cannot prove uniqueness")
    raise AttachmentError("Collection exceeded bounded paging; cannot prove uniqueness")


def country_code(value):
    if not isinstance(value, str) or not re.fullmatch(r"GLOBAL|[A-Z]{2}", value):
        raise AttachmentError("Select GLOBAL or an uppercase two-letter tax-country code")
    return value


def parent_and_endpoint(client, country="GLOBAL"):
    country = country_code(country)
    rows = all_items(client, RESOURCE, {"q": f"TaxCountryCode='{country}'"})
    if len(rows) != 1 or rows[0].get("TaxCountryCode") != country:
        raise AttachmentError(f"Require exactly one current {country} notification; no country fallback or parent creation")
    parent = rows[0]
    identity = str(parent.get("NewSupplierNotificationId", ""))
    if not identity.isdigit() or int(identity) <= 0:
        raise AttachmentError("Selected notification has no valid identity")
    return parent, f"{RESOURCE}/{identity}/child/attachments"


def contract(client, endpoint, body):
    # The entity is bound by this resource, not an invented upload attribute.
    if not re.fullmatch(re.escape(RESOURCE) + r"/[1-9][0-9]*/child/attachments", endpoint):
        raise AttachmentError("Attachment endpoint is outside the notification entity")
    description = client.request(endpoint + "/describe")
    resource = description.get("Resources", {}).get("attachments", {})
    return attachment_contract(resource, body)


def validate_attachment_identity(values):
    if values.get("CategoryName") != CATEGORY_NAME:
        raise AttachmentError("Attachment CategoryName must be " + CATEGORY_NAME)
    if "EntityName" in values and values["EntityName"] != ENTITY_NAME:
        raise AttachmentError("Attachment EntityName must be " + ENTITY_NAME)


def attachment_contract(resource, body):
    validate_attachment_identity(body)
    actions = resource.get("collection", {}).get("actions", [])
    attrs = {a.get("name"): a for a in resource.get("attributes", [])}
    entity_default = attrs.get("EntityName", {}).get("defaultValue")
    if entity_default is not None and entity_default != ENTITY_NAME:
        raise AttachmentError("Child contract has a conflicting attachment entity")
    if not any(a.get("name") == "create" and a.get("method") == "POST" for a in actions):
        raise AttachmentError("Child contract lacks POST create")
    if attrs.get("FileContents", {}).get("type") != "attachment":
        raise AttachmentError("Child contract lacks attachment-type FileContents")
    if attrs.get("AttachedDocumentId", {}).get("hasDefaultValueExpression") is not True:
        raise AttachmentError("Child contract does not generate AttachedDocumentId")
    for name, value in body.items():
        attr = attrs.get(name)
        if not attr:
            raise AttachmentError("Reviewed payload field absent from child contract: " + name)
        if attr.get("updatable") is False:
            raise AttachmentError("Reviewed payload field is read-only: " + name)
        maximum = str(attr.get("maxLength", ""))
        if maximum.isdigit() and len(value) > int(maximum):
            raise AttachmentError("Reviewed payload exceeds child field length: " + name)
    for name, attr in attrs.items():
        # Fusion's describe marks server-owned audit fields mandatory too.
        # They cannot be supplied on create when the contract says never.
        if attr.get("updatable") is False and attr.get("allowChanges") == "never":
            continue
        if attr.get("mandatory") is True and name not in body and not attr.get("hasDefaultValueExpression") and attr.get("defaultValue") is None:
            raise AttachmentError("Missing mandatory child create field: " + name)
    # Nested and resolved-child descriptions have different URL links. Bind the
    # create capability and attribute contract, not placeholder URL spelling.
    return digest(canonical({"actions": actions, "attributes": resource.get("attributes", [])}))


def no_duplicate(client, endpoint, name):
    rows = all_items(client, endpoint)
    if any(name in (r.get("FileName"), r.get("UploadedFileName")) for r in rows):
        raise AttachmentError("Same-name attachment exists; add must not overwrite it")
    return rows


def executor_fingerprint(core_repo=REPO_ROOT):
    core_repo = Path(core_repo).resolve()
    paths = [Path(__file__), core_repo / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py",
             core_repo / "core/fusion-api/rest-api-client/scripts/rest_client_common.py",
             core_repo / "core/auth/fusion-oauth-authentication/scripts/fusion_auth.py"]
    return digest(canonical([digest(p.read_bytes()) for p in paths]))


def build_preview(file, title, properties, client=None, core_repo=REPO_ROOT, *, country="GLOBAL"):
    country = country_code(country)
    facts = file_facts(file)
    body = payload(facts, title if title is not None else facts["basename"])
    client = client or CoreClient(properties, core_repo)
    parent, endpoint = parent_and_endpoint(client, country)
    evidence = contract(client, endpoint, body)
    current = no_duplicate(client, endpoint, facts["basename"])
    return {"schema_version": 3, "operation": "add_supplier_notification_attachment",
            "tax_country_code": country,
            "core_route": core_route(properties, core_repo),
            "parent_id": str(parent["NewSupplierNotificationId"]),
            "endpoint": endpoint, "executor_sha256": executor_fingerprint(core_repo),
            "core_repo": str(Path(core_repo).resolve()),
            "contract_sha256": evidence, "payload_sha256": digest(canonical(body)),
            "source_path": str(Path(file).absolute()), "title": body["Title"],
            "attachment": {k: v for k, v in facts.items() if k != "content"},
            "current_attachment_count": len(current), "approval_required": True,
            "live_route_enabled": LIVE_ROUTE_ENABLED}


def execute_preview(preview_path, approved_sha256, properties, client=None, core_repo=REPO_ROOT):
    # Disabling the capability blocks execution before authentication or calls.
    if not LIVE_ROUTE_ENABLED:
        raise AttachmentError("Live attachment executor is disabled")
    preview_path = Path(preview_path)
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    if digest(canonical(preview)) != approved_sha256:
        raise AttachmentError("Approved preview fingerprint mismatch")
    if preview.get("schema_version") != 3 or preview.get("operation") != "add_supplier_notification_attachment":
        raise AttachmentError("Unsupported preview")
    country = country_code(preview.get("tax_country_code"))
    if preview.get("core_route") != core_route(properties, core_repo):
        raise AttachmentError("Core profile selection changed; rebuild and reapprove")
    if preview.get("core_repo") != str(Path(core_repo).resolve()):
        raise AttachmentError("Core executor selection changed; rebuild and reapprove")
    if preview["executor_sha256"] != executor_fingerprint(core_repo):
        raise AttachmentError("Executor changed; rebuild and reapprove")
    facts = file_facts(preview["source_path"])
    if {k: v for k, v in facts.items() if k != "content"} != preview["attachment"]:
        raise AttachmentError("File changed; rebuild and reapprove")
    body = payload(facts, preview["title"])
    if digest(canonical(body)) != preview["payload_sha256"]:
        raise AttachmentError("Payload changed; rebuild and reapprove")
    client = client or CoreClient(properties, core_repo)
    parent, endpoint = parent_and_endpoint(client, country)
    if endpoint != preview["endpoint"] or str(parent["NewSupplierNotificationId"]) != preview["parent_id"]:
        raise AttachmentError("Parent changed; rebuild and reapprove")
    if contract(client, endpoint, body) != preview["contract_sha256"]:
        raise AttachmentError("Contract changed; rebuild and reapprove")
    before = no_duplicate(client, endpoint, facts["basename"])
    # A canonical sibling journal binds dispatch to this immutable preview.
    journal = preview_path.parent / ("attachment-execution-" + approved_sha256 + ".json")
    result = {"status": "dispatch_pending", "preview_sha256": approved_sha256,
              "tax_country_code": country,
              "core_route": preview["core_route"], "file_name": facts["basename"],
              "byte_verification": "not_attempted"}
    try:
        write_private(journal, result, exclusive=True)
    except FileExistsError:
        raise AttachmentError("Preview already dispatched or reserved; reconcile, do not replay") from None
    try:
        response = client.request(endpoint, method="POST", body=body)
        identity = str(response.get("AttachedDocumentId", ""))
        result["status"] = "accepted_unverified"
        if not identity.isdigit() or int(identity) <= 0:
            raise AttachmentError("Create response lacks generated attachment identity")
        result["created_attachment_id"] = identity  # Internal only.
        after = all_items(client, endpoint)
        matches = [r for r in after if str(r.get("AttachedDocumentId")) == identity]
        if len(matches) != 1 or matches[0].get("FileName") != facts["basename"] or matches[0].get("Title") != preview["title"]:
            raise AttachmentError("Created attachment metadata could not be verified")
        validate_attachment_identity(matches[0])
        before_ids = {str(r.get("AttachedDocumentId")) for r in before}
        if not before_ids.issubset({str(r.get("AttachedDocumentId")) for r in after}):
            raise AttachmentError("Existing attachment preservation could not be verified")
        current_parent, current_endpoint = parent_and_endpoint(client, country)
        if current_endpoint != endpoint or any(current_parent.get(k) != parent.get(k) for k in ("EmailSubject", "EmailBody")):
            raise AttachmentError("Notification content preservation could not be verified")
        result["status"] = "metadata_verified"
        # Only a same-child advertised enclosure may be downloaded.
        prefix = endpoint + "/" + identity + "/enclosure/FileContents"
        links = matches[0].get("links", [])
        content_links = [l.get("href") for l in links if l.get("rel") == "enclosure" and l.get("name") == "FileContents"]
        if content_links:
            if len(content_links) != 1:
                raise AttachmentError("Ambiguous attachment content read")
            downloaded = client.request(content_endpoint(content_links[0], prefix), binary=True)
            if digest(downloaded) != facts["sha256"]:
                raise AttachmentError("Uploaded attachment bytes differ from approved file")
            result.update(status="verified", byte_verification="sha256_matched")
        else:
            result["byte_verification"] = "unavailable"
    except Exception:
        if result["status"] == "dispatch_pending":
            result["status"] = "unknown"
        result["reconciliation_required"] = True
        write_private(journal, result)
        raise AttachmentError("Attachment outcome requires reconciliation; journal retained; do not retry") from None
    write_private(journal, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("preview", help="Read-only contract and file preflight")
    plan.add_argument("--file", type=Path, required=True)
    plan.add_argument("--country", required=True, help="GLOBAL or an exact two-letter TaxCountryCode, e.g. US")
    plan.add_argument("--title")
    plan.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("execute", help="Execute an exactly approved attachment preview")
    run.add_argument("--preview", type=Path, required=True)
    run.add_argument("--approved-preview-sha256", required=True)
    for command in (plan, run):
        command.add_argument("--properties", type=Path,
                             help="Opaque properties-file path passed to Core; omitted uses Core's default")
        command.add_argument("--core-repo", type=Path, default=REPO_ROOT,
                             help="Explicit Core helper repository, bound into approval")
    args = parser.parse_args()
    if args.command == "preview":
        value = build_preview(args.file, args.title, args.properties, core_repo=args.core_repo,
                              country=args.country)
        write_private(args.output, value, exclusive=True)
        print(json.dumps({"status": "preview_ready", "file_name": value["attachment"]["basename"],
                          "configuration_source": "Core REST client", "preview_sha256": digest(canonical(value)),
                          "tax_country_code": value["tax_country_code"],
                          "live_route_enabled": LIVE_ROUTE_ENABLED}))
    else:
        result = execute_preview(args.preview, args.approved_preview_sha256, args.properties,
                                 core_repo=args.core_repo)
        print(json.dumps({k: v for k, v in result.items() if k != "created_attachment_id"}))


if __name__ == "__main__":
    try:
        main()
    except AttachmentError as error:
        print("Error: " + str(error), file=sys.stderr)
        sys.exit(2)
    except Exception:
        print("Error: attachment operation failed; no automatic retry", file=sys.stderr)
        sys.exit(2)
