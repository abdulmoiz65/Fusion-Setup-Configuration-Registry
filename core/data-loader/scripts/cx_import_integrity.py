"""Canonical ordered CX file bytes shared by preview and execution."""

from typing import Iterable, Protocol


class ImportFile(Protocol):
    member_name: str
    content: bytes


def cx_import_group_bytes(files: Iterable[ImportFile]) -> bytes:
    """Length-prefix names and content so order and boundaries are unambiguous."""
    parts: list[bytes] = []
    for file in files:
        name = file.member_name.encode("utf-8")
        parts.extend((len(name).to_bytes(8, "big"), name, len(file.content).to_bytes(8, "big"), file.content))
    return b"".join(parts)
