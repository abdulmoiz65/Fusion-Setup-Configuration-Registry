"""Private durable recovery snapshots, never an approval authority.

Consumers must reverify the original consumed approval and both fingerprints
against the durable ledger. An evidence file alone cannot authorize anything.
Secure storage requires POSIX directory-descriptor, ownership and no-follow
primitives. Unsupported platforms fail closed without disabling module import.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import uuid

ROOT = Path(__file__).resolve().parents[6]
EVIDENCE_HOME = Path.home() / ".local/state/fscr/cpq-setup-assistant/evidence"
MAX_BYTES = 64 * 1024 * 1024


class EvidenceError(ValueError):
    """Sanitized evidence persistence or validation failure."""


def _require(condition):
    if not condition:
        raise EvidenceError("Protected CPQ recovery evidence is unavailable or invalid.")


def _require_platform():
    supported = {getattr(function, "__name__", "") for function in getattr(os, "supports_dir_fd", ())}
    if (os.name != "posix" or not callable(getattr(os, "getuid", None))
            or not all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
            or not {"open", "mkdir", "rename", "unlink"} <= supported):
        raise EvidenceError("Protected CPQ recovery storage is unsupported on this platform.")


def _attempt_id(value):
    try:
        parsed = uuid.UUID(value) if isinstance(value, str) else None
    except ValueError:
        parsed = None
    _require(parsed is not None and parsed.version == 4 and str(parsed) == value)
    return value


def _canonical(value):
    try:
        data = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise EvidenceError("Protected CPQ recovery evidence is unavailable or invalid.") from None
    _require(len(data) <= MAX_BYTES)
    return data


def _open_home(create):
    """Walk with directory descriptors so no ancestor or final symlink is followed."""
    path = Path(EVIDENCE_HOME)
    _require(path.is_absolute() and ".." not in path.parts and path != Path("/"))
    _require(path != ROOT and ROOT not in path.parents)
    root_info = ROOT.stat()
    repository_identity = (root_info.st_dev, root_info.st_ino)
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[1:]:
            if create:
                try:
                    os.mkdir(component, 0o700, dir_fd=descriptor)
                    os.fsync(descriptor)
                except FileExistsError:
                    pass
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
            info = os.fstat(descriptor)
            _require((info.st_dev, info.st_ino) != repository_identity)
        info = os.fstat(descriptor)
        _require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _read(home, attempt):
    descriptor = os.open(attempt + ".json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=home)
    try:
        info = os.fstat(descriptor)
        _require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                 and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1
                 and 0 < info.st_size <= MAX_BYTES)
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            data = stream.read(MAX_BYTES + 1)
        _require(len(data) <= MAX_BYTES)
        try:
            result = json.loads(data)
        except (ValueError, UnicodeError, RecursionError):
            raise EvidenceError("Protected CPQ recovery evidence is unavailable or invalid.") from None
        _require(isinstance(result, dict) and set(result) == {"schemaVersion", "attemptId", "manifest", "approvalRecord"}
                 and result["schemaVersion"] == "cpq-recovery-evidence/1" and result["attemptId"] == attempt
                 and isinstance(result["manifest"], dict) and isinstance(result["approvalRecord"], dict)
                 and result["manifest"].get("nonce") == attempt and result["approvalRecord"].get("nonce") == attempt)
        _require(_canonical(result) == data)
        return data, result
    finally:
        os.close(descriptor)


def retain(manifest, approval_record):
    """Persist exact evidence before approval consumption; return its immutable nonce ID."""
    _require_platform()
    try:
        import fcntl
    except ImportError:
        raise EvidenceError("Protected CPQ recovery storage is unsupported on this platform.") from None
    _require(isinstance(manifest, dict) and isinstance(approval_record, dict))
    attempt = _attempt_id(manifest.get("nonce"))
    _require(approval_record.get("nonce") == attempt)
    data = _canonical({"schemaVersion": "cpq-recovery-evidence/1", "attemptId": attempt,
                       "manifest": manifest, "approvalRecord": approval_record})
    home = None
    publication_lock = None
    temporary = ".pending-" + str(uuid.uuid4())
    created = False
    try:
        home = _open_home(True)
        lock_flags = os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK
        try:
            publication_lock = os.open(".publish.lock", lock_flags | os.O_CREAT | os.O_EXCL,
                                       0o600, dir_fd=home)
        except FileExistsError:
            publication_lock = os.open(".publish.lock", lock_flags, dir_fd=home)
        info = os.fstat(publication_lock)
        _require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                 and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1)
        fcntl.flock(publication_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            existing, _ = _read(home, attempt)
        except FileNotFoundError:
            pass
        else:
            _require(existing == data)
            os.fsync(home)
            return attempt
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=home)
        created = True
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        # The exclusive publication lock serializes absence checking and atomic rename.
        # Unlike link/unlink publication, a crash cannot strand a multiply-linked record.
        os.rename(temporary, attempt + ".json", src_dir_fd=home, dst_dir_fd=home)
        created = False
        os.fsync(home)
        return attempt
    except OSError:
        raise EvidenceError("Protected CPQ recovery evidence could not be persisted.") from None
    finally:
        if publication_lock is not None:
            os.close(publication_lock)
        if home is not None:
            try:
                if created:
                    try:
                        os.unlink(temporary, dir_fd=home)
                    except OSError:
                        pass  # An unpublished file can never be loaded as an attempt.
            finally:
                os.close(home)


def load(attempt_id):
    """Read a recovery snapshot; the caller must authenticate it against the ledger."""
    _require_platform()
    attempt = _attempt_id(attempt_id)
    home = None
    try:
        home = _open_home(False)
        _, result = _read(home, attempt)
        return result["manifest"], result["approvalRecord"]
    except OSError:
        raise EvidenceError("Protected CPQ recovery evidence could not be read.") from None
    finally:
        if home is not None:
            os.close(home)
