"""Bind extracted FSM members to the exact downloaded task export ZIP."""

import hashlib
import json
from pathlib import Path
import sys
from zipfile import BadZipFile, ZipFile


MEMBERS = {
    "ASM_SETUP_CSV_METADATA.xml",
    "EXM_SETUP_OPTION.csv",
    "EXM_ORG_SETTING.csv",
    "EXM_CASH_ADV_SETUP_AND_POLICY.csv",
}
MAX_MEMBER_BYTES = 50 * 1024 * 1024


def verify(archive_path: Path, extracted_dir: Path) -> dict:
    with ZipFile(archive_path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(MEMBERS) or set(names) != MEMBERS:
            raise ValueError("Export ZIP must contain exactly the four expected root members")
        for entry in entries:
            if entry.flag_bits & 1 or entry.file_size > MAX_MEMBER_BYTES:
                raise ValueError(f"Unsupported or oversized export member: {entry.filename}")
            exported = archive.read(entry)
            extracted = (extracted_dir / entry.filename).read_bytes()
            if exported != extracted:
                raise ValueError(f"Extracted member differs from export ZIP: {entry.filename}")
    return {"archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest()}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(Path(sys.argv[1]), Path(sys.argv[2]))))
    except (BadZipFile, OSError, ValueError, IndexError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(2)
