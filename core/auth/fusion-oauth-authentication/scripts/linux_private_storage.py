"""Read a cloud-managed OAuth client secret mounted on a headless Linux VM."""

from __future__ import annotations

import os
import stat
from pathlib import Path


SECRET_FILE_ENV = "FSCR_OAUTH_CLIENT_SECRET_FILE"
SECRET_ACCOUNT_ENV = "FSCR_OAUTH_CLIENT_SECRET_ACCOUNT"


def cloud_secret_configured() -> bool:
    """A partial cloud configuration must fail rather than use a local secret."""
    return SECRET_FILE_ENV in os.environ or SECRET_ACCOUNT_ENV in os.environ


def local_secret_path(auth_home: Path, account: str) -> Path:
    if len(account) != 64 or any(c not in "0123456789abcdef" for c in account):
        raise ValueError("Invalid Linux OAuth secret account binding")
    return auth_home / "oauth-client-secrets" / f"{account}.json"


def validate_secret(secret: str) -> str:
    if not isinstance(secret, str) or not secret or any(c in secret for c in "\r\n\x00"):
        raise ValueError("OAuth client secret must be nonempty and single-line")
    return secret


def load_client_secret_linux(service: str, account: str, repository_root: Path) -> str:
    """Read only a pinned-account secret from a private, non-symlinked mount."""
    path_value = os.environ.get(SECRET_FILE_ENV, "")
    configured_account = os.environ.get(SECRET_ACCOUNT_ENV, "")
    if not path_value or not configured_account:
        raise ValueError("Linux confidential-client login requires a cloud-managed secret file and account binding")
    if configured_account != account:
        raise ValueError("Linux OAuth secret account does not match the enrolled environment and client")
    path = Path(path_value)
    if not path.is_absolute() or not path.name or any(part in {".", ".."} for part in path.parts):
        raise ValueError("Linux OAuth secret path must be absolute and canonical")
    if path.is_relative_to(repository_root):
        raise ValueError("Linux OAuth secret file must be outside the repository")

    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
    directory = os.open(path.anchor, flags | os.O_DIRECTORY)
    try:
        for part in path.parts[1:-1]:
            next_directory = os.open(part, flags | os.O_DIRECTORY, dir_fd=directory)
            os.close(directory)
            directory = next_directory
        descriptor = os.open(path.name, flags | os.O_NONBLOCK, dir_fd=directory)
        try:
            info = os.fstat(descriptor)
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                    or info.st_uid not in {0, os.getuid()}
                    or stat.S_IMODE(info.st_mode) & 0o077):
                raise ValueError("Linux OAuth secret must be a private, single-link regular file owned by root or the runner")
            if info.st_size < 1 or info.st_size > 65536:
                raise ValueError("Linux OAuth secret has an invalid size")
            with os.fdopen(descriptor, "rb", closefd=False) as handle:
                raw = handle.read(65537)
            if len(raw) > 65536:
                raise ValueError("Linux OAuth secret exceeds the size limit")
            try:
                secret = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("Linux OAuth secret must be UTF-8") from exc
            if not secret or any(c in secret for c in "\r\n\x00"):
                raise ValueError("Linux OAuth secret must be nonempty and single-line")
            return secret
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)
