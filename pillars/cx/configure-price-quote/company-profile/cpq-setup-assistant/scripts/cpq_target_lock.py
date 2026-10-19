"""Cross-process exclusion for CPQ sessions on one host and OS account.

Lock files are not approval records and contain no credentials or payloads.
Never unlink them: another process could otherwise lock a different inode.
This local lock cannot serialize independent machines or OS accounts.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import urllib.parse

try:
    from cpq_approval_contract import ContractError
except ModuleNotFoundError:
    from scripts.cpq_approval_contract import ContractError


def target_identity(host: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(host)
        port = parsed.port or 443
    except (ValueError, TypeError) as error:
        raise ContractError("CPQ session requires a valid HTTPS Fusion origin.") from error
    if (
        parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
        or parsed.query or parsed.fragment or parsed.path not in ("", "/")
    ):
        raise ContractError("CPQ session requires an HTTPS origin without credentials, path or query.")
    return parsed.hostname.lower().rstrip(".") + ":" + str(port) + "/SA_SETUP_ASSISTANT"


class TargetLock:
    def __init__(self, host: str, *, directory: Path | None = None) -> None:
        self.identity = target_identity(host)
        self.directory = directory or Path.home() / ".fscr" / "cpq-approval-locks"
        self.path = self.directory / (hashlib.sha256(self.identity.encode()).hexdigest() + ".lock")
        self._fd: int | None = None
        self._pid: int | None = None

    def __enter__(self) -> TargetLock:
        if self._fd is not None:
            raise ContractError("CPQ target lock is already held by this session.")
        try:
            self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
            # A redirected writable directory would make the lock ineffective.
            for path in (self.directory.parent, self.directory):
                info = path.lstat()
                if not stat.S_ISDIR(info.st_mode):
                    raise ContractError("CPQ target-lock directory must not be a symbolic link.")
                if os.name != "nt" and (info.st_uid != os.getuid() or info.st_mode & 0o022):
                    raise ContractError("CPQ target-lock directory must be owned by this user and not writable by others.")
            fd = os.open(self.path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
            try:
                info = os.fstat(fd)
                if not stat.S_ISREG(info.st_mode):
                    raise ContractError("CPQ target lock must be a regular file.")
                if os.name != "nt" and (info.st_uid != os.getuid() or info.st_mode & 0o077):
                    raise ContractError("CPQ target lock must be private to this OS user.")
                if os.name == "nt":
                    import msvcrt
                    if info.st_size == 0:
                        os.write(fd, b"\0")
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BaseException:
                os.close(fd)
                raise
            self._fd, self._pid = fd, os.getpid()
            try:
                self.assert_held()
            except BaseException:
                self.__exit__()
                raise
            return self
        except OSError as error:
            raise ContractError("CPQ target is locked by another session or its private lock cannot be acquired.") from error

    def assert_held(self) -> None:
        if self._fd is None or self._pid != os.getpid():
            raise ContractError("CPQ execution requires its original process to hold the target lock.")
        try:
            descriptor, current = os.fstat(self._fd), self.path.lstat()
        except OSError as error:
            raise ContractError("CPQ target lock is no longer available.") from error
        if not stat.S_ISREG(current.st_mode) or (descriptor.st_dev, descriptor.st_ino) != (current.st_dev, current.st_ino):
            raise ContractError("CPQ target lock was replaced; execution is blocked.")

    def __exit__(self, *_args) -> None:
        if self._fd is None:
            return
        fd, self._fd = self._fd, None
        try:
            # A fork must not release the original process's inherited lock.
            if self._pid == os.getpid():
                if os.name == "nt":
                    import msvcrt
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
