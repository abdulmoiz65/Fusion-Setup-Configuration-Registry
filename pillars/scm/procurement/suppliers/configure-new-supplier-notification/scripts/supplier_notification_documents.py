#!/usr/bin/env python3
"""Preview and execute country documents: create a missing row, then add files.

Email content and enablement are deliberately outside this REST operation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import supplier_notification_attachment as attachment

Error = attachment.AttachmentError


def fingerprint(core_repo):
    return attachment.digest(attachment.canonical([
        attachment.digest(Path(__file__).read_bytes()),
        attachment.executor_fingerprint(core_repo),
    ]))


def exact_rows(client, country):
    rows = attachment.all_items(client, attachment.RESOURCE,
                                {"q": f"TaxCountryCode='{country}'"})
    if len(rows) > 1 or any(row.get("TaxCountryCode") != country for row in rows):
        raise Error("Country identity is ambiguous; rebuild after reconciliation")
    return rows


def validate_country(client, country):
    if country == "GLOBAL":
        return
    rows = attachment.all_items(client, attachment.TERRITORIES,
                                {"q": f"TerritoryCode='{country}'"})
    if len(rows) != 1 or rows[0].get("TerritoryCode") != country:
        raise Error("Country does not resolve uniquely in the live territory reference")


def parent_contract(resource, body):
    actions = resource.get("collection", {}).get("actions", [])
    attrs = {a.get("name"): a for a in resource.get("attributes", [])}
    if not any(a.get("name") == "create" and a.get("method") == "POST" for a in actions):
        raise Error("Country collection does not advertise POST create")
    if attrs.get("NewSupplierNotificationId", {}).get("hasDefaultValueExpression") is not True:
        raise Error("Country create does not generate NewSupplierNotificationId")
    if not set(body).issubset({"TaxCountryCode", "UserComments"}):
        raise Error("Parent payload contains fields outside country-document creation")
    for name, value in body.items():
        attr = attrs.get(name, {})
        if not attr or attr.get("updatable") is False:
            raise Error("Unsupported country create field: " + name)
        maximum = str(attr.get("maxLength", attr.get("precision", "")))
        if not isinstance(value, str) or (maximum.isdigit() and len(value) > int(maximum)):
            raise Error("Invalid country create value: " + name)
    for name, attr in attrs.items():
        if attr.get("updatable") is False and attr.get("allowChanges") == "never":
            continue
        if (attr.get("mandatory") is True and name not in body
                and not attr.get("hasDefaultValueExpression") and attr.get("defaultValue") is None):
            raise Error("Missing mandatory country create field: " + name)
    return attachment.digest(attachment.canonical({
        "actions": actions, "attributes": resource.get("attributes", []),
    }))


def resolve_plan(client, country, bodies, comments):
    validate_country(client, country)
    rows = exact_rows(client, country)
    if not rows:
        if country == "GLOBAL":
            raise Error("Missing GLOBAL notification is a configuration blocker")
        body = {"TaxCountryCode": country}
        if comments is not None:
            body["UserComments"] = comments
        resource = client.request(attachment.RESOURCE + "/describe").get(
            "Resources", {}).get("newSupplierNotification", {})
        parent_sha = parent_contract(resource, body)
        child = resource.get("children", {}).get("attachments", {})
        evidence = [attachment.attachment_contract(child, payload) for payload in bodies]
        return {"mode": "create", "parent_id": None, "parent_fields": body,
                "parent_contract_sha256": parent_sha,
                "child_contract_sha256": evidence, "existing_attachment_ids": []}
    parent, endpoint = attachment.parent_and_endpoint(client, country)
    if comments is not None and parent.get("UserComments") != comments:
        raise Error("Existing-row comment changes require the configuration route")
    evidence = [attachment.contract(client, endpoint, payload) for payload in bodies]
    existing = attachment.all_items(client, endpoint)
    for body in bodies:
        if any(body["FileName"] in (r.get("FileName"), r.get("UploadedFileName")) for r in existing):
            raise Error("Same-name attachment exists; reconcile instead of uploading again")
    return {"mode": "existing", "parent_id": str(parent["NewSupplierNotificationId"]),
            "parent_fields": {}, "parent_contract_sha256": None,
            "child_contract_sha256": evidence,
            "existing_attachment_ids": sorted(str(r["AttachedDocumentId"]) for r in existing)}


def content_state(client, country):
    global_parent, _ = attachment.parent_and_endpoint(client, "GLOBAL")
    selected = exact_rows(client, country)
    fields = ("TaxCountryCode", "EmailSubject", "EmailBody", "UserComments")
    return attachment.digest(attachment.canonical({
        "global": {k: global_parent.get(k) for k in fields},
        "selected": [{k: p.get(k) for k in fields} for p in selected],
    }))


def global_content_state(client):
    parent, _ = attachment.parent_and_endpoint(client, "GLOBAL")
    return attachment.digest(attachment.canonical({
        k: parent.get(k) for k in ("NewSupplierNotificationId", "EmailSubject", "EmailBody", "UserComments")
    }))


def build_preview(files, titles, properties, *, country, comments=None,
                  client=None, core_repo=attachment.REPO_ROOT):
    country = attachment.country_code(country)
    if not files or (titles is not None and len(titles) != len(files)):
        raise Error("Supply files and, when used, exactly one title per file")
    facts = [attachment.file_facts(path) for path in files]
    names = [f["basename"].casefold() for f in facts]
    if len(set(names)) != len(names):
        raise Error("Duplicate filenames in the requested upload batch")
    bodies = [attachment.payload(f, titles[i] if titles else f["basename"])
              for i, f in enumerate(facts)]
    client = client or attachment.CoreClient(properties, core_repo)
    plan = resolve_plan(client, country, bodies, comments)
    return {"schema_version": 2, "operation": "ensure_country_and_add_files",
            "core_route": attachment.core_route(properties, core_repo),
            "tax_country_code": country, "comments": comments,
            "parent_plan": plan, "parent_endpoint": attachment.RESOURCE,
            "content_state_sha256": content_state(client, country),
            "global_content_sha256": global_content_state(client),
            "executor_sha256": fingerprint(core_repo),
            "core_repo": str(Path(core_repo).resolve()), "approval_required": True,
            "files": [{"source_path": str(Path(path).absolute()), "title": body["Title"],
                       "attachment": {k: v for k, v in f.items() if k != "content"},
                       "payload_sha256": attachment.digest(attachment.canonical(body))}
                      for path, f, body in zip(files, facts, bodies)]}


def verify_file(client, endpoint, response, facts, title):
    identity = str(response.get("AttachedDocumentId", ""))
    if not identity.isdigit() or int(identity) <= 0:
        raise Error("Upload response lacks generated attachment identity")
    rows = attachment.all_items(client, endpoint)
    matches = [r for r in rows if str(r.get("AttachedDocumentId")) == identity]
    if len(matches) != 1 or matches[0].get("FileName") != facts["basename"] or matches[0].get("Title") != title:
        raise Error("Uploaded file metadata could not be verified")
    attachment.validate_attachment_identity(matches[0])
    links = [l.get("href") for l in matches[0].get("links", [])
             if l.get("rel") == "enclosure" and l.get("name") == "FileContents"]
    result = {"file_name": facts["basename"], "status": "metadata_verified",
              "byte_verification": "unavailable", "created_attachment_id": identity}
    if links:
        expected = endpoint + "/" + identity + "/enclosure/FileContents"
        if len(links) != 1:
            raise Error("Ambiguous content read")
        content = attachment.content_endpoint(links[0], expected)
        if attachment.digest(client.request(content, binary=True)) != facts["sha256"]:
            raise Error("Uploaded file bytes differ from the approved file")
        result.update(status="verified", byte_verification="sha256_matched")
    return result


def execute_preview(path, approved_sha256, properties, *, client=None,
                    core_repo=attachment.REPO_ROOT):
    if not attachment.LIVE_ROUTE_ENABLED:
        raise Error("Live attachment executor is disabled")
    path = Path(path)
    preview = json.loads(path.read_text(encoding="utf-8"))
    if attachment.digest(attachment.canonical(preview)) != approved_sha256:
        raise Error("Approved preview fingerprint mismatch")
    if preview.get("schema_version") != 2 or preview.get("operation") != "ensure_country_and_add_files":
        raise Error("Unsupported combined preview")
    if (preview.get("core_route") != attachment.core_route(properties, core_repo)
            or preview.get("core_repo") != str(Path(core_repo).resolve())
            or preview.get("executor_sha256") != fingerprint(core_repo)):
        raise Error("Core profile selection or executor changed; rebuild and reapprove")
    country = attachment.country_code(preview["tax_country_code"])
    facts, bodies = [], []
    for item in preview["files"]:
        f = attachment.file_facts(item["source_path"])
        body = attachment.payload(f, item["title"])
        if ({k: v for k, v in f.items() if k != "content"} != item["attachment"]
                or attachment.digest(attachment.canonical(body)) != item["payload_sha256"]):
            raise Error("File or payload changed; rebuild and reapprove")
        facts.append(f)
        bodies.append(body)
    client = client or attachment.CoreClient(properties, core_repo)
    plan = resolve_plan(client, country, bodies, preview["comments"])
    if (plan != preview["parent_plan"] or content_state(client, country) != preview["content_state_sha256"]
            or global_content_state(client) != preview["global_content_sha256"]):
        raise Error("Parent, contract, or content changed; rebuild and reapprove")
    journal = path.parent / ("documents-execution-" + approved_sha256 + ".json")
    result = {"core_route": preview["core_route"], "tax_country_code": country,
              "status": "reserved", "parent_status": "existing" if plan["mode"] == "existing" else "not_attempted",
              "files": [{"file_name": f["basename"], "status": "not_attempted"} for f in facts]}
    try:
        attachment.write_private(journal, result, exclusive=True)
    except FileExistsError:
        raise Error("Preview already dispatched or reserved; reconcile, do not replay") from None
    try:
        if plan["mode"] == "create":
            result["parent_status"] = "dispatching"
            attachment.write_private(journal, result)
            response = client.request(attachment.RESOURCE, method="POST", body=plan["parent_fields"])
            result["parent_status"] = "accepted_unverified"
            identity = str(response.get("NewSupplierNotificationId", ""))
            if not identity.isdigit() or int(identity) <= 0:
                raise Error("Country create response lacks generated identity")
            result["created_parent_id"] = identity
            attachment.write_private(journal, result)
        parent, endpoint = attachment.parent_and_endpoint(client, country)
        expected_id = result.get("created_parent_id", plan["parent_id"])
        if str(parent["NewSupplierNotificationId"]) != expected_id:
            raise Error("Country identity changed after approval")
        if plan["mode"] == "create":
            if any(parent.get(k) != v for k, v in plan["parent_fields"].items()):
                raise Error("Created country row differs from the approved fields")
            if global_content_state(client) != preview["global_content_sha256"]:
                raise Error("GLOBAL content changed during country creation; stop before upload")
            result["parent_status"] = "created_verified"
            attachment.write_private(journal, result)
        baseline = content_state(client, country)
        existing_ids = set(plan["existing_attachment_ids"])
        for i, (f, body, item) in enumerate(zip(facts, bodies, preview["files"])):
            if attachment.contract(client, endpoint, body) != plan["child_contract_sha256"][i]:
                raise Error("Child contract changed; stop before upload")
            attachment.no_duplicate(client, endpoint, f["basename"])
            result["files"][i]["status"] = "dispatching"
            attachment.write_private(journal, result)
            response = client.request(endpoint, method="POST", body=body)
            result["files"][i]["status"] = "accepted_unverified"
            if response.get("AttachedDocumentId") is not None:
                result["files"][i]["created_attachment_id"] = str(response["AttachedDocumentId"])
            attachment.write_private(journal, result)
            verified = verify_file(client, endpoint, response, f, item["title"])
            after_ids = {str(r["AttachedDocumentId"]) for r in attachment.all_items(client, endpoint)}
            if not existing_ids.issubset(after_ids) or content_state(client, country) != baseline:
                raise Error("Existing documents or email content were not preserved")
            existing_ids.add(verified["created_attachment_id"])
            result["files"][i] = verified
            attachment.write_private(journal, result)
        result["status"] = ("verified" if all(f["status"] == "verified" for f in result["files"])
                            else "metadata_verified")
    except Exception:
        result["status"] = "partial" if result["parent_status"] in {"created_verified", "accepted_unverified"} or any(
            f["status"] in {"verified", "metadata_verified", "accepted_unverified"} for f in result["files"]) else "unknown"
        result["reconciliation_required"] = True
        attachment.write_private(journal, result)
        raise Error("Country-document execution incomplete; journal retained; reconcile before retry") from None
    attachment.write_private(journal, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("preview")
    plan.add_argument("--country", required=True)
    plan.add_argument("--file", action="append", type=Path, required=True)
    plan.add_argument("--title", action="append")
    plan.add_argument("--comments")
    plan.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("execute")
    run.add_argument("--preview", type=Path, required=True)
    run.add_argument("--approved-preview-sha256", required=True)
    for command in (plan, run):
        command.add_argument("--properties", type=Path,
                             help="Opaque properties-file path passed to Core; omitted uses Core's default")
        command.add_argument("--core-repo", type=Path, default=attachment.REPO_ROOT)
    args = parser.parse_args()
    if args.command == "preview":
        value = build_preview(args.file, args.title, args.properties, country=args.country,
                              comments=args.comments, core_repo=args.core_repo)
        attachment.write_private(args.output, value, exclusive=True)
        print(json.dumps({"status": "preview_ready", "configuration_source": "Core REST client",
                          "country": value["tax_country_code"], "parent_operation": value["parent_plan"]["mode"],
                          "files": [f["attachment"]["basename"] for f in value["files"]],
                          "preview_sha256": attachment.digest(attachment.canonical(value))}))
    else:
        result = execute_preview(args.preview, args.approved_preview_sha256, args.properties,
                                 core_repo=args.core_repo)
        print(json.dumps({k: ([{a: b for a, b in f.items() if a != "created_attachment_id"} for f in v]
                             if k == "files" else v) for k, v in result.items() if k != "created_parent_id"}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error: " + (str(error) if isinstance(error, Error) else "document operation failed; no automatic retry"), file=sys.stderr)
        sys.exit(2)
