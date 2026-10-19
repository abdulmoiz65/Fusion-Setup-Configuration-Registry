"""Read and update the active Run Book ID configuration."""

import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Dict, List, Optional, Sequence, Tuple


def _replace_run_id(content: str, run_id: str) -> str:
    lines = content.splitlines(keepends=True)
    matches: List[Tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        body = line.rstrip("\r\n")
        line_ending = line[len(body) :]
        separator = body.find("=")
        if separator >= 0 and body[:separator].strip() == "runID":
            matches.append((index, separator, line_ending))

    if len(matches) > 1:
        raise ValueError("Data Loader config contains multiple runID entries.")
    if matches:
        index, separator, line_ending = matches[0]
        body = lines[index].rstrip("\r\n")
        existing_value = body[separator + 1 :]
        leading_space = existing_value[: len(existing_value) - len(existing_value.lstrip())]
        trailing_space = existing_value[len(existing_value.rstrip()) :]
        lines[index] = (
            f"{body[: separator + 1]}{leading_space}{run_id}"
            f"{trailing_space}{line_ending}"
        )
        return "".join(lines)

    newline = "\r\n" if "\r\n" in content else "\n"
    had_final_newline = content.endswith(("\r", "\n"))
    separator = "" if not content or had_final_newline else newline
    final_newline = newline if had_final_newline else ""
    return f"{content}{separator}runID={run_id}{final_newline}"


def read_run_id(config_path: Path) -> Optional[str]:
    """Read the single non-empty, case-sensitive Data Loader runID."""

    path = Path(config_path)
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError("Data Loader config path must be a file.")

    values: List[str] = []
    for line in path.read_bytes().decode("utf-8").splitlines():
        separator = line.find("=")
        if separator >= 0 and line[:separator].strip() == "runID":
            values.append(line[separator + 1 :].strip())

    if len(values) > 1:
        raise ValueError("Data Loader config contains multiple runID entries.")
    if not values or not values[0]:
        return None
    return values[0]


def stamp_run_id(config_path: Path, run_id: Any) -> Dict[str, Any]:
    """Atomically stamp only Data Loader's runID with an active Run Book ID."""

    if (
        isinstance(run_id, bool)
        or not isinstance(run_id, (int, str))
        or not str(run_id).strip()
    ):
        raise ValueError("Run Book ID must be a non-empty integer or string.")
    normalized_run_id = str(run_id).strip()
    path = Path(config_path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("Data Loader config path must be a file.")
    content = path.read_bytes().decode("utf-8")
    updated = _replace_run_id(content, normalized_run_id)
    changed = updated != content
    if changed:
        mode = stat.S_IMODE(path.stat().st_mode)
        temporary_path: Optional[Path] = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                temporary.write(updated.encode("utf-8"))
                temporary.flush()
                os.fsync(temporary.fileno())
            os.chmod(temporary_path, mode)
            os.replace(temporary_path, path)
        except Exception:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise

    return {
        "configured": True,
        "changed": changed,
    }
