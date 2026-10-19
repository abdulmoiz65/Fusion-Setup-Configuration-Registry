"""Reconcile Core's review ZIP with its protected CX CSV-group preview, offline."""

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import zipfile


class PreviewMismatch(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def require(condition, message):
    if not condition:
        raise PreviewMismatch(message)


def origin(value):
    parsed = urlsplit(value)
    require(parsed.scheme == "https" and parsed.hostname and not parsed.username
            and not parsed.password and parsed.path in ("", "/")
            and not parsed.query and not parsed.fragment, "Invalid target origin.")
    return parsed.hostname.lower(), parsed.port or 443


def reconcile(preflight_path, adapter_path, object_code, import_mode):
    envelope = json.loads(Path(preflight_path).read_text())
    review = json.loads(Path(adapter_path).read_text())
    require(envelope.get("schemaVersion") == "1.0", "Unsupported Core preflight schema.")
    unsigned = {k: v for k, v in envelope.items() if k != "fingerprint"}
    require(envelope.get("fingerprint") == digest(canonical(unsigned)),
            "Core preflight fingerprint mismatch.")
    preflight = envelope["preflight"]
    manifest = review["manifest"]
    require(review.get("status") == "awaiting_approval", "CX preview is not awaiting approval.")
    require(review.get("reviewSha256") == digest(canonical(manifest)),
            "CX manifest review digest mismatch.")
    require(re.fullmatch(r"[0-9a-f]{64}", review.get("approvalId", "")), "Invalid approval ID.")
    group_digest = manifest.get("groupSha256", "")
    require(re.fullmatch(r"[0-9a-f]{64}", group_digest), "Missing CX group digest.")
    payload, target = manifest["payload"], manifest["target"]
    require(preflight.get("mappingComplete") is True
            and preflight.get("sourceType") == "ORA_CX_IMPORT", "Core CX review is incomplete.")
    require(manifest.get("operation") == "cx-import", "Wrong adapter operation.")
    require(preflight.get("cxImportObjectCode") == payload.get("ObjectCode") == object_code,
            "Import object mismatch.")
    require(import_mode in ("CREATE_ONLY", "CREATE_RECORD", "DELETE_RECORD")
            and payload.get("ImportMode") == import_mode, "Import mode mismatch.")
    require(preflight.get("environment") == target.get("environment"), "Environment mismatch.")
    require(origin(preflight["host"]) == origin(target["origin"]), "Target host mismatch.")
    require(preflight.get("cxUcmAccount") == manifest["ucm"].get("account"), "UCM account mismatch.")
    files, cx_files = manifest["files"], preflight["cxFiles"]
    require(files and len(files) == len(cx_files), "CSV membership mismatch.")
    names = [f["name"] for f in files]
    require(len(set(n.casefold() for n in names)) == len(names), "Duplicate CSV names.")
    require(all(f.get("role") == "Data" for f in cx_files), "Mapping CSVs are unsupported.")
    require(names == [f["fileName"] for f in cx_files]
            == [f["memberName"] for f in cx_files], "CSV names or order mismatch.")
    require(all(Path(n).name == n and n.lower().endswith(".csv") for n in names),
            "Unsafe CSV member name.")
    archive = Path(preflight["approvedArtifactPath"])
    with archive.open("rb") as source:
        require(hashlib.file_digest(source, "sha256").hexdigest() == preflight["archiveSha256"],
                "Core review ZIP digest mismatch.")
        source.seek(0)
        with zipfile.ZipFile(source) as zipped:
            require(zipped.namelist() == names, "Review ZIP membership or order mismatch.")
            for item, expected in zip(zipped.infolist(), files):
                require(item.file_size == expected["size"] and item.file_size > 0,
                        "CSV size mismatch.")
                with zipped.open(item) as member:
                    require(hashlib.file_digest(member, "sha256").hexdigest() == expected["sha256"],
                            "CSV bytes differ between Core and CX previews.")
    return {"status": "reconciled", "objectCode": object_code, "ImportMode": import_mode,
            "orderedFilenames": names, "dataLoaderArchiveSha256": preflight["archiveSha256"],
            "groupSha256": group_digest, "approvalId": review["approvalId"],
            "reviewSha256": review["reviewSha256"], "executionAdapter":
            "core.fusion-api.cx-import-export-management", "approvalGranted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", required=True, type=Path)
    parser.add_argument("--adapter-preview", required=True, type=Path)
    parser.add_argument("--object-code", required=True)
    parser.add_argument("--import-mode", required=True,
                        choices=["CREATE_ONLY", "CREATE_RECORD", "DELETE_RECORD"])
    args = parser.parse_args()
    try:
        result = reconcile(args.preflight, args.adapter_preview, args.object_code, args.import_mode)
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, RuntimeError):
        # Do not echo untrusted artifact content or source data in diagnostics.
        print(json.dumps({"status": "blocked", "failureClass": "approval_blocker",
                          "message": "Core/CX review reconciliation failed. Check artifact integrity, CSV membership/order/bytes, target, object, mode, and UCM account."}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
