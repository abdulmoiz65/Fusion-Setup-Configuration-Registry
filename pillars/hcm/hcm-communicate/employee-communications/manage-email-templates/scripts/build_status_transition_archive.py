#!/usr/bin/env python3
"""Build an FSM archive that changes only selected Campaign template statuses."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
import zipfile


PARENT_MEMBER = "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN.csv"
REQUIRED_MEMBERS = (
    PARENT_MEMBER,
    "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN_METADATA.csv",
    "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN_TYPES.csv",
    "ASM_SETUP_CSV_METADATA.xml",
)
ALLOWED_STATUSES = {"ORA_ACTIVE", "ORA_INACTIVE"}


class ArchiveError(ValueError):
    """Raised when a controlled status archive cannot be built safely."""


def read_parent(archive: zipfile.ZipFile) -> tuple[list[str], list[dict[str, str]]]:
    try:
        content = archive.read(PARENT_MEMBER).decode("utf-8-sig")
    except KeyError as error:
        raise ArchiveError(f"Archive is missing required member {PARENT_MEMBER}.") from error
    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames or not {"DesignName", "MessageDesignCode", "DesignStatusCode"} <= set(reader.fieldnames):
        raise ArchiveError("Parent CSV must contain DesignName, MessageDesignCode, and DesignStatusCode.")
    return reader.fieldnames, list(reader)


def parse_transition(value: str) -> tuple[str, str]:
    name, separator, status = value.partition("=")
    if not separator or not name.strip() or status.strip() not in ALLOWED_STATUSES:
        raise argparse.ArgumentTypeError("Each --transition must be DesignName=ORA_ACTIVE or DesignName=ORA_INACTIVE.")
    return name.strip(), status.strip()


def render_parent(fieldnames: list[str], rows: list[dict[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def build_archive(source: Path, output: Path, transitions: dict[str, str]) -> None:
    if not source.is_file():
        raise ArchiveError("Source export archive does not exist.")
    if output.resolve() == source.resolve():
        raise ArchiveError("Output archive must differ from the source export.")
    with zipfile.ZipFile(source) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ArchiveError("Source archive contains duplicate member names.")
        missing = [member for member in REQUIRED_MEMBERS if member not in archive.namelist()]
        if missing:
            raise ArchiveError("Source archive is missing required members: " + ", ".join(missing))
        fieldnames, rows = read_parent(archive)
        matched = {name: [] for name in transitions}
        codes: set[str] = set()
        for row in rows:
            name = (row.get("DesignName") or "").strip()
            code = (row.get("MessageDesignCode") or "").strip()
            if not name or not code or code in codes:
                raise ArchiveError("Parent CSV contains a blank or duplicate template identity.")
            codes.add(code)
            if name in matched:
                matched[name].append(row)
        invalid = [name for name, found in matched.items() if len(found) != 1]
        if invalid:
            raise ArchiveError("Each selected template must occur exactly once: " + ", ".join(sorted(invalid)))
        for name, found in matched.items():
            row = found[0]
            current = (row.get("DesignStatusCode") or "").strip()
            requested = transitions[name]
            if current not in ALLOWED_STATUSES:
                raise ArchiveError(f"{name} has unsupported current status {current or '<blank>'}.")
            if current == requested:
                raise ArchiveError(f"{name} is already {requested}.")
            row["DesignStatusCode"] = requested

        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as candidate:
            for member in archive.namelist():
                candidate.writestr(
                    member,
                    render_parent(fieldnames, rows) if member == PARENT_MEMBER else archive.read(member),
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-export", type=Path, required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    parser.add_argument("--transition", type=parse_transition, action="append", required=True)
    args = parser.parse_args()
    transitions = dict(args.transition)
    if len(transitions) != len(args.transition):
        parser.error("Each template may have only one requested status.")
    try:
        build_archive(args.source_export, args.output_archive, transitions)
    except (ArchiveError, OSError, UnicodeDecodeError, zipfile.BadZipFile) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
