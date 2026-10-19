#!/usr/bin/env python3
"""Write a safe, self-contained inline dashboard for Loader chat results."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any


ASSET_PATH = Path(__file__).resolve().parents[1] / "assets" / "data-load-dashboard-template.html"
PLACEHOLDER = "__LOADER_REPORT__"


def render_dashboard(model: dict[str, Any]) -> str:
    template = ASSET_PATH.read_text(encoding="utf-8")
    encoded = json.dumps(model, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    if template.count(PLACEHOLDER) != 1:
        raise ValueError("Loader dashboard template must contain exactly one report placeholder.")
    return template.replace(PLACEHOLDER, encoded)


def write_dashboard(model: dict[str, Any], output_path: Path) -> Path:
    if output_path.suffix.lower() != ".html":
        raise ValueError("Inline Loader output must use an .html filename.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_dashboard(model)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.stem}-", suffix=".tmp", dir=output_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(rendered)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, output_path)
        directory_descriptor = os.open(output_path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary_path.unlink(missing_ok=True)
    return output_path


def verify_dashboard(output_path: Path) -> bool:
    """Confirm the exact inline artifact is a readable, non-empty regular file."""
    try:
        file_status = output_path.stat()
        if not stat.S_ISREG(file_status.st_mode) or file_status.st_size <= 0:
            return False
        with output_path.open("rb") as dashboard_file:
            return bool(dashboard_file.read(1))
    except OSError:
        return False
