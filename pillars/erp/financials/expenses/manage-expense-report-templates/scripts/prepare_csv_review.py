#!/usr/bin/env python3
"""Extract exact candidate CSVs and a string-grid manifest for workbook review."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tempfile
import zipfile
from pathlib import Path

from build_import_candidate import CandidateBuildError, read_baseline, sha256_file


def prepare_review(candidate: Path, output_dir: Path) -> dict:
    if output_dir.exists():
        raise CandidateBuildError(f"Refusing to overwrite review directory: {output_dir}")
    infos, members = read_baseline(candidate)
    csvs = []
    for info in infos:
        if not info.filename.lower().endswith(".csv"):
            continue
        content = members[info.filename]
        try:
            rows = list(csv.reader(io.StringIO(content.decode("utf-8-sig"), newline=""), strict=True))
        except (UnicodeDecodeError, csv.Error) as error:
            raise CandidateBuildError(f"Unreadable CSV member: {info.filename}") from error
        if not rows or not rows[0] or len(set(rows[0])) != len(rows[0]):
            raise CandidateBuildError(f"Missing or duplicate header in {info.filename}")
        if any(len(row) != len(rows[0]) for row in rows):
            raise CandidateBuildError(f"Unequal row widths in {info.filename}")
        if len(rows) > 1048576 or len(rows[0]) > 16384 or any(
            len(cell) > 32767 for row in rows for cell in row
        ):
            raise CandidateBuildError(f"{info.filename} exceeds Excel limits; review the exact CSV directly.")
        csvs.append({
            "member": info.filename,
            "sha256": hashlib.sha256(content).hexdigest(),
            "row_count": len(rows) - 1,
            "columns": rows[0],
            "rows": rows,
            "grid_sha256": hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest(),
        })
    if not csvs:
        raise CandidateBuildError("Candidate has no CSV members.")
    manifest = {
        "schema_version": "1.0",
        "candidate": {"zip": str(candidate.resolve()), "sha256": sha256_file(candidate)},
        "csvs": csvs,
    }
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".csv-review-", dir=output_dir.parent) as temporary:
        staged = Path(temporary) / "review"
        staged.mkdir()
        for entry in csvs:
            (staged / entry["member"]).write_bytes(members[entry["member"]])
        (staged / "csv-review.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        staged.rename(output_dir)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-zip", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = prepare_review(args.candidate_zip, args.output_dir)
    except (CandidateBuildError, OSError, zipfile.BadZipFile) as error:
        parser.exit(2, f"CSV review preparation failed: {error}\n")
    print(json.dumps({"status": "review_prepared", "csv_count": len(manifest["csvs"]),
                      "manifest": str(args.output_dir / "csv-review.json"),
                      "candidate_sha256": manifest["candidate"]["sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
