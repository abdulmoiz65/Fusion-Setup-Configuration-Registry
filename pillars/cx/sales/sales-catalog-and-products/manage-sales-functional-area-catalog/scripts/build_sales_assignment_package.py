#!/usr/bin/env python3
"""Create a staged FSM package that changes only the Sales catalog assignment."""

import argparse
import csv
import io
import tempfile
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
PROJECTS_ROOT = REPOSITORY_ROOT / "project"
ASSIGNMENT_MEMBER = "EGP_DEFAULT_CATALOG_FUNCTIONAL_AREA.csv"
METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
HEADER_ONLY_MEMBERS = (
    "ORA_EGP_VALID_CATALOG_CATEGORY.csv",
    "EGP_CATEGORY.csv",
    "EGP_CATALOG.csv",
)


def project_root_for(value: Path) -> Path:
    root = value.resolve(strict=True)
    if not root.is_dir() or root.parent != PROJECTS_ROOT.resolve() or value.is_symlink():
        raise ValueError("project-root must be an existing non-symlink project/{project_id} directory")
    return root


def contained_file(value: Path, root: Path, label: str, *, must_exist: bool) -> Path:
    candidate = value.resolve(strict=must_exist)
    if not candidate.is_relative_to(root) or (must_exist and (not candidate.is_file() or value.is_symlink())):
        raise ValueError(f"{label} must be a regular file inside project-root")
    return candidate


def safe_parent(target: Path, root: Path) -> None:
    relative_parent = target.parent.relative_to(root)
    current = root
    for component in relative_parent.parts:
        current = current / component
        if current.exists() and current.is_symlink():
            raise ValueError("output parent must not contain symlinks")
        if not current.exists():
            current.mkdir()
        if not current.is_dir() or not current.resolve().is_relative_to(root):
            raise ValueError("output parent must remain inside project-root")


def csv_bytes(rows: list[list[str]]) -> bytes:
    stream = io.StringIO(newline="")
    csv.writer(stream, lineterminator="\n").writerows(rows)
    return stream.getvalue().encode("utf-8")


def read_csv(source: zipfile.ZipFile, member: str) -> list[list[str]]:
    try:
        rows = list(csv.reader(io.StringIO(source.read(member).decode("utf-8-sig"))))
    except KeyError as exc:
        raise ValueError(f"baseline is missing required member {member}") from exc
    if not rows or not rows[0]:
        raise ValueError(f"baseline member {member} has no CSV header")
    return rows


def package_rows(source: zipfile.ZipFile, catalog_code: str) -> tuple[list[list[str]], dict[str, list[list[str]]], bytes]:
    if METADATA_MEMBER not in source.namelist():
        raise ValueError("baseline is not a supported Manage Functional Area Catalogs FSM package")
    assignment_rows = read_csv(source, ASSIGNMENT_MEMBER)
    header, data = assignment_rows[0], assignment_rows[1:]
    try:
        functional_area_id_index = header.index("FunctionalAreaId")
        catalog_code_index = header.index("CatalogCode")
    except ValueError as exc:
        raise ValueError("Sales assignment CSV is missing required columns") from exc
    matches = [row for row in data if len(row) > functional_area_id_index and row[functional_area_id_index] == "38"]
    if len(matches) != 1 or len(matches[0]) <= catalog_code_index:
        raise ValueError("baseline must contain exactly one complete Sales functional-area assignment")
    assignment = list(matches[0])
    assignment[catalog_code_index] = catalog_code
    headers = {member: [read_csv(source, member)[0]] for member in HEADER_ONLY_MEMBERS}
    return [header, assignment], headers, source.read(METADATA_MEMBER)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--catalog-code", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--replace-after-confirmation", action="store_true")
    args = parser.parse_args()
    catalog_code = args.catalog_code.strip()
    if not catalog_code:
        raise ValueError("catalog-code must be nonblank")
    root = project_root_for(args.project_root)
    baseline = contained_file(args.baseline, root, "baseline", must_exist=True)
    output = contained_file(args.output, root, "output", must_exist=False)
    if baseline == output:
        raise ValueError("baseline and output must be different files")
    if output.exists() and not args.replace_after_confirmation:
        raise ValueError("output already exists; require --replace-after-confirmation")
    safe_parent(output, root)

    with zipfile.ZipFile(baseline) as source:
        assignment_rows, headers, metadata = package_rows(source, catalog_code)

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=output.parent, prefix=f".{output.name}.", delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as destination:
            for member in HEADER_ONLY_MEMBERS:
                destination.writestr(member, csv_bytes(headers[member]))
            destination.writestr(ASSIGNMENT_MEMBER, csv_bytes(assignment_rows))
            destination.writestr(METADATA_MEMBER, metadata)
        with zipfile.ZipFile(temporary) as staged:
            if set(staged.namelist()) != set(HEADER_ONLY_MEMBERS + (ASSIGNMENT_MEMBER, METADATA_MEMBER)):
                raise ValueError("staged package has an unexpected member set")
        temporary.replace(output)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
