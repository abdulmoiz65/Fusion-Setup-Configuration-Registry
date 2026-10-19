"""Owner-protected, one-use CX import approvals; never trust workspace envelopes.

The approving OS account is the authority. Records live outside the checkout in
a fixed private store, not at a caller-selected path. This protects against
workspace/artifact substitution, not compromise of that account or its code.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import time
from typing import NamedTuple
import urllib.parse

CORE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CORE_ROOT / "auth/fusion-oauth-authentication/scripts"))
sys.path.insert(0, str(CORE_ROOT / "data-loader/scripts"))
from fusion_auth import (  # noqa: E402
    AUTH_HOME, oauth_endpoints, pkce_enabled, read_private_json,
    write_private_json, require_authorized_rest_url,
)
from cx_import_integrity import cx_import_group_bytes  # noqa: E402

APPROVAL_HOME = AUTH_HOME / "cx-import-approvals"
VERSION = 1
MAX_AGE = 3600


class ApprovalError(ValueError):
    """An approval, artifact, or environment no longer authorizes execution."""


class SourceFile(NamedTuple):
    member_name: str
    content: bytes


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def fingerprint(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def record_path(approval_id: str, suffix: str) -> Path:
    if not isinstance(approval_id, str) or not re.fullmatch(r"[0-9a-f]{64}", approval_id):
        raise ApprovalError("Missing or invalid approval ID")
    return APPROVAL_HOME / f"{approval_id}.{suffix}.json"


def _read(approval_id: str, suffix: str) -> dict:
    try:
        record = read_private_json(record_path(approval_id, suffix))
    except (OSError, ValueError) as exc:
        raise ApprovalError("Missing, invalid, or unsafe approval record") from exc
    if not isinstance(record, dict):
        raise ApprovalError("Invalid approval record")
    return record


def _unused(approval_id: str) -> None:
    # lstat also treats dangling symlinks as used; never follow them.
    try:
        record_path(approval_id, "used").lstat()
    except FileNotFoundError:
        return
    raise ApprovalError("Approval already consumed; obtain a new approval after reconciliation")


def read_sources(paths: list[str]) -> tuple[SourceFile, ...]:
    if not paths:
        raise ApprovalError("At least one local data CSV is required")
    files = []
    names = set()
    for supplied in paths:
        path = Path(supplied)
        name = path.name
        if (path.suffix.lower() != ".csv" or name.casefold() in names or
                any(ord(c) < 32 or ord(c) == 127 or c in "\\/" for c in name)):
            raise ApprovalError("Sources must have unique, safe CSV basenames")
        names.add(name.casefold())
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as source:
            before = os.fstat(source.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ApprovalError("Source must be a regular file")
            content = source.read()
            after = os.fstat(source.fileno())
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise ApprovalError("Source changed while being read")
        files.append(SourceFile(name, content))
    return tuple(files)


def normalize_account(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ApprovalError("Exact object metadata must provide UcmAccount")
    segments = value.strip().strip("/").split("/")
    if any(not re.fullmatch(r"[A-Za-z0-9_.-]+\$?", part) or part.rstrip("$") in {".", ".."} for part in segments):
        raise ApprovalError("Malformed UCM account")
    return "/".join(part.rstrip("$") + "$" for part in segments)


def target_context(props: dict[str, str]) -> dict:
    require_authorized_rest_url(props, props["restBaseUrl"])
    endpoints = oauth_endpoints(props)  # No token or secret access.
    parsed = urllib.parse.urlsplit(props["restBaseUrl"])
    if parsed.path not in {"", "/"}:
        raise ApprovalError("Fusion target must be an HTTPS origin")
    return {
        "environment": props["environment"],
        "origin": f"https://{parsed.hostname}:{parsed.port or 443}",
        "clientId": props["clientId"],
        "authorizeUrl": endpoints["authorizeUrl"],
        "tokenUrl": endpoints["tokenUrl"],
        "scope": " ".join(props["scope"].split()),
        "pkce": pkce_enabled(props),
    }


def import_manifest(props: dict[str, str], args, files: tuple[SourceFile, ...]) -> dict:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", args.object_code):
        raise ApprovalError("An exact object code is required")
    if not args.name.strip():
        raise ApprovalError("Import activity name is required")
    return {
        "version": VERSION,
        "operation": "cx-import",
        "target": target_context(props),
        "files": [{"name": f.member_name, "size": len(f.content), "sha256": hashlib.sha256(f.content).hexdigest()} for f in files],
        "groupSha256": hashlib.sha256(cx_import_group_bytes(files)).hexdigest(),
        "payload": {"Name": args.name, "ObjectCode": args.object_code,
                    "ImportMode": args.import_mode, "Activate": args.activate, "Schedule": args.schedule},
        "ucm": {"account": normalize_account(args.ucm_document_account),
                "uploadMode": "rest", "operation": "uploadFileToUCM", "contentType": "csv"},
    }


def prepare(manifest: dict) -> dict:
    approval_id = secrets.token_hex(32)
    record = {"version": VERSION, "approvalId": approval_id, "createdAt": time.time(), "manifest": manifest}
    write_private_json(record_path(approval_id, "preview"), record, replace=False)
    return {**record, "reviewSha256": fingerprint(manifest), "status": "awaiting_approval"}


def approve(approval_id: str, review_sha256: str, ttl: int = 900) -> dict:
    if not 1 <= ttl <= MAX_AGE:
        raise ApprovalError("Approval lifetime must be 1-3600 seconds")
    _unused(approval_id)
    preview = _read(approval_id, "preview")
    now = time.time()
    if not 0 <= now - preview.get("createdAt", 0) < MAX_AGE:
        raise ApprovalError("Preview expired; prepare and review a new import")
    digest = fingerprint(preview.get("manifest"))
    if not hmac.compare_digest(digest, review_sha256):
        raise ApprovalError("Reviewed manifest differs from the protected preview")
    record = {**preview, "approvedAt": now, "expiresAt": now + ttl,
              "actorUid": os.getuid(), "reviewSha256": digest}
    try:
        write_private_json(record_path(approval_id, "approved"), record, replace=False)
    except FileExistsError as exc:
        raise ApprovalError("Approval already issued; it cannot be renewed or replaced") from exc
    return {"approvalId": approval_id, "reviewSha256": digest, "expiresAt": record["expiresAt"], "status": "approved"}


def load_approved(approval_id: str) -> dict:
    _unused(approval_id)
    record = _read(approval_id, "approved")
    now = time.time()
    try:
        valid = (record["version"] == VERSION and record["approvalId"] == approval_id
                 and record["actorUid"] == os.getuid()
                 and 0 < record["expiresAt"] - record["approvedAt"] <= MAX_AGE
                 and record["approvedAt"] <= now < record["expiresAt"]
                 and hmac.compare_digest(record["reviewSha256"], fingerprint(record["manifest"])))
    except (KeyError, TypeError, ValueError):
        valid = False
    if not valid:
        raise ApprovalError("Invalid or expired approval")
    return record


def compare(record: dict, current_manifest: dict) -> None:
    if not hmac.compare_digest(canonical(record["manifest"]), canonical(current_manifest)):
        raise ApprovalError("Source bytes, order, settings, or target changed after approval")


def consume(approval_id: str, current_manifest: dict) -> None:
    # Atomic no-clobber publication admits only one executor, including processes.
    compare(load_approved(approval_id), current_manifest)
    try:
        write_private_json(record_path(approval_id, "used"), {"consumedAt": time.time()}, replace=False)
    except FileExistsError as exc:
        raise ApprovalError("Approval already consumed by another execution") from exc
