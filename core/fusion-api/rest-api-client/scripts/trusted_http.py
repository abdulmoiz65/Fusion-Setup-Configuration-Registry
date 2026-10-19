"""HTTPS origin enforcement for authenticated service requests.

The approved origin must come from the trusted environment profile, separately
from an override, a server-supplied link, or a redirect destination.
"""

from __future__ import annotations

import ipaddress
import re
import urllib.parse
import urllib.request


class DestinationError(ValueError):
    """An authenticated request would leave its approved service origin."""


def https_origin(url: str) -> tuple[str, str, int]:
    if (
        not isinstance(url, str)
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url)
        or "\\" in url
    ):
        raise DestinationError("Service URLs must not contain whitespace, controls, or backslashes.")
    try:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme.lower() != "https" or not parsed.hostname:
            raise ValueError("HTTPS required")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("Credentials in URL")
        # urlsplit accepts an empty port and trailing text after an IPv6
        # bracket. Do not normalize malformed authorities into trusted ones.
        if parsed.netloc.startswith("["):
            suffix = parsed.netloc[parsed.netloc.index("]") + 1:]
            if suffix and not re.fullmatch(r":[0-9]+", suffix):
                raise ValueError("Invalid IPv6 authority")
        elif ":" in parsed.netloc:
            if not re.fullmatch(r"[0-9]+", parsed.netloc.rsplit(":", 1)[1]):
                raise ValueError("Invalid port")
        host = parsed.hostname
        if "%" in host:
            raise ValueError("Encoded hostname")
        try:
            host = ipaddress.ip_address(host).compressed
        except ValueError:
            host = host.encode("idna").decode("ascii").lower()
        port = parsed.port if parsed.port is not None else 443
        if not 1 <= port <= 65535:
            raise ValueError("Invalid port")
    except (ValueError, UnicodeError) as exc:
        raise DestinationError("Service URL must have a valid HTTPS origin and no embedded credentials.") from exc
    return "https", host, port


def normalize_service_origin(raw: str) -> str:
    if not isinstance(raw, str) or any(ord(char) < 32 or ord(char) == 127 for char in raw):
        raise DestinationError("Service URLs must not contain control characters.")
    value = raw.strip()
    if value.startswith("//"):
        value = "https:" + value
    elif "://" not in value:
        value = "https://" + value
    scheme, host, port = https_origin(value)
    authority = f"[{host}]" if ":" in host else host
    if port != 443:
        authority += f":{port}"
    return f"{scheme}://{authority}"


def validate_destination(url: str, approved_origin: str) -> str:
    if https_origin(url) != https_origin(approved_origin):
        raise DestinationError("Authenticated request destination differs from the approved service origin.")
    if urllib.parse.urlsplit(url).fragment:
        raise DestinationError("Authenticated request URLs must not contain fragments.")
    return url


class SameOriginRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, approved_origin: str) -> None:
        self.approved_origin = normalize_service_origin(approved_origin)

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            validate_destination(newurl, self.approved_origin)
            method = req.get_method()
            if method not in {"GET", "HEAD"}:
                raise DestinationError("Automatic redirects of authenticated write requests are not allowed.")
        except DestinationError:
            fp.close()
            raise
        return urllib.request.Request(
            newurl,
            headers={key: value for key, value in req.headers.items()
                     if key.lower() not in {"content-length", "content-type"}},
            method=method,
            origin_req_host=req.origin_req_host,
            unverifiable=True,
        )

    # Python versions without built-in 308 handling must apply the same policy.
    http_error_308 = urllib.request.HTTPRedirectHandler.http_error_302


def open_authenticated(request: urllib.request.Request, *, approved_origin: str, timeout: int = 120):
    validate_destination(request.full_url, approved_origin)
    opener = urllib.request.build_opener(SameOriginRedirectHandler(approved_origin))
    return opener.open(request, timeout=timeout)
