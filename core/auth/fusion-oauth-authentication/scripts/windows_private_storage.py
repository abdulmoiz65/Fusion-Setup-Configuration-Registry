"""Windows private JSON storage for the Fusion OAuth trust policy and token cache.

The POSIX implementation in fusion_auth.py is intentionally untouched. Windows
uses protected ACLs on its dedicated directory and files. pywin32 is required.
"""

from __future__ import annotations

import json
import os
import secrets
import stat
from pathlib import Path
from typing import Any


def _windows_api():
    try:
        import win32api
        import win32con
        import win32security
        import ntsecuritycon
    except ImportError as exc:
        raise RuntimeError("Windows Fusion OAuth storage requires pywin32") from exc
    return win32api, win32con, win32security, ntsecuritycon


def _credential_api():
    try:
        import win32cred
    except ImportError as exc:
        raise RuntimeError("Windows Fusion OAuth credential storage requires pywin32") from exc
    return win32cred


def _credential_target(service: str, account: str) -> str:
    if not service or not account or any(c in service + account for c in "\r\n\x00"):
        raise ValueError("Invalid Fusion OAuth credential identity")
    return f"{service}:{account}"


def load_client_secret_windows(service: str, account: str) -> str:
    win32cred = _credential_api()
    try:
        credential = win32cred.CredRead(_credential_target(service, account), win32cred.CRED_TYPE_GENERIC)
    except Exception as exc:
        if exc.args and exc.args[0] == 1168:  # ERROR_NOT_FOUND
            raise ValueError("No confidential-client secret is enrolled in Windows Credential Manager") from exc
        raise RuntimeError("Windows Credential Manager could not read the OAuth secret") from exc
    blob = credential.get("CredentialBlob", b"")
    try:
        secret = blob.decode("utf-16-le") if isinstance(blob, bytes) else str(blob)
    except UnicodeError as exc:
        raise ValueError("Windows Credential Manager returned an invalid OAuth secret") from exc
    if not secret or any(c in secret for c in "\r\n\x00"):
        raise ValueError("Windows Credential Manager returned an invalid OAuth secret")
    return secret


def store_client_secret_windows(service: str, account: str, secret: str) -> None:
    if not secret or any(c in secret for c in "\r\n\x00"):
        raise ValueError("OAuth client secret must be nonempty and single-line")
    win32cred = _credential_api()
    win32cred.CredWrite({
        "Type": win32cred.CRED_TYPE_GENERIC,
        "TargetName": _credential_target(service, account),
        "UserName": account,
        "CredentialBlob": secret,
        "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
    }, 0)
    if load_client_secret_windows(service, account) != secret:
        raise RuntimeError("Windows Credential Manager verification failed")


def _current_user_sid(win32api: Any, win32con: Any, win32security: Any) -> Any:
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
    try:
        return win32security.GetTokenInformation(token, win32security.TokenUser)[0]
    finally:
        token.Close()


def _reject_reparse(path: Path) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return
    if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError("Refusing a reparse point in Fusion private storage")


def _restrict_acl(path: Path, user_sid: Any, win32security: Any, ntsecuritycon: Any) -> None:
    acl = win32security.ACL()
    acl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_ALL_ACCESS, user_sid)
    system_sid = win32security.CreateWellKnownSid(win32security.WinLocalSystemSid, None)
    acl.AddAccessAllowedAce(win32security.ACL_REVISION, ntsecuritycon.FILE_ALL_ACCESS, system_sid)
    win32security.SetNamedSecurityInfo(
        str(path), win32security.SE_FILE_OBJECT,
        win32security.DACL_SECURITY_INFORMATION | win32security.PROTECTED_DACL_SECURITY_INFORMATION,
        None, None, acl, None,
    )


def _private_path(path: Path, home: Path, *, create: bool) -> tuple[Path, tuple[Any, Any, Any, Any], Any]:
    """Limit writes to the managed directory and reject path redirection."""
    path = Path(os.path.abspath(path.expanduser()))
    home = Path(os.path.abspath(home.expanduser()))
    if path.parent != home:
        raise ValueError("Windows Fusion private storage must be in the managed ~/.fusionaim directory")
    api = _windows_api()
    win32api, win32con, win32security, ntsecuritycon = api
    sid = _current_user_sid(win32api, win32con, win32security)
    for parent in reversed(home.parents):
        _reject_reparse(parent)
    _reject_reparse(home)
    if create:
        home.mkdir(mode=0o700, exist_ok=True)
    if not home.is_dir():
        raise FileNotFoundError("Fusion private storage directory is unavailable")
    _reject_reparse(home)
    owner = win32security.GetNamedSecurityInfo(
        str(home), win32security.SE_FILE_OBJECT, win32security.OWNER_SECURITY_INFORMATION,
    ).GetSecurityDescriptorOwner()
    if owner != sid:
        raise ValueError("Fusion private storage directory must be owned by the current user")
    _restrict_acl(home, sid, win32security, ntsecuritycon)
    _reject_reparse(path)
    return path, api, sid


def _check_file(path: Path, api: tuple[Any, ...], sid: Any) -> None:
    info = path.lstat()
    if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError("Refusing a reparse point in Fusion private storage")
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError("Fusion private storage requires a single-link regular file")
    _, _, win32security, ntsecuritycon = api
    owner = win32security.GetNamedSecurityInfo(
        str(path), win32security.SE_FILE_OBJECT, win32security.OWNER_SECURITY_INFORMATION,
    ).GetSecurityDescriptorOwner()
    if owner != sid:
        raise ValueError("Fusion private storage file must be owned by the current user")
    _restrict_acl(path, sid, win32security, ntsecuritycon)


def read_private_json_windows(path: Path, home: Path) -> Any:
    path, api, sid = _private_path(path, home, create=False)
    _check_file(path, api, sid)
    return json.loads(path.read_text(encoding="utf-8"))


def write_private_json_windows(path: Path, value: Any, home: Path, *, replace: bool = True) -> None:
    path, api, sid = _private_path(path, home, create=True)
    _, _, win32security, ntsecuritycon = api
    if path.exists():
        _check_file(path, api, sid)
    encoded = json.dumps(value, indent=2).encode("utf-8")
    temporary = path.parent / (".fscr-" + secrets.token_hex(16))
    try:
        with temporary.open("xb") as handle:
            _restrict_acl(temporary, sid, win32security, ntsecuritycon)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        _check_file(temporary, api, sid)
        _reject_reparse(path)
        if replace:
            os.replace(temporary, path)
        else:
            # Atomic create without replacing a concurrent trust enrollment.
            os.link(temporary, path)
            temporary.unlink()
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
