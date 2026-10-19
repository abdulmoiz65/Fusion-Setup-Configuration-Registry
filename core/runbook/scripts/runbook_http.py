"""HTTP transport used by the Run Book Oracle Fusion client."""

from http.client import HTTPException
import json
from typing import Any, Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TIMEOUT_SECONDS = 60


class ApiError(RuntimeError):
    """An Oracle Fusion REST request or response failed validation."""


class SuccessResponseError(ApiError):
    """Oracle Fusion returned HTTP success with an unusable response body."""


class IndeterminateWriteError(ApiError):
    """A write was dispatched, but Oracle Fusion's outcome could not be determined."""


def _decode_error_body(body: bytes, status: int) -> Any:
    if not body:
        return {"status": status}
    text = body.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"status": status, "body": text}


def _decode_success_body(body: bytes, status: int) -> Any:
    if not body:
        return {"status": status}
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SuccessResponseError(
            f"Oracle Fusion REST returned a non-JSON success response with HTTP {status}."
        ) from error


class JsonTransport:
    """Send JSON requests with the Run Book retry and write-safety rules."""

    def __init__(
        self,
        *,
        base_url: str,
        authorization: str,
        refresh_authorization: Optional[Callable[[], str]] = None,
        timeout: int = TIMEOUT_SECONDS,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("Run Book REST base URL must be non-empty text.")
        if not isinstance(authorization, str) or not authorization.strip():
            raise ValueError("Run Book authorization must be non-empty text.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener
        self._authorization = authorization
        self._refresh_authorization = refresh_authorization

    def request_json(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
        payload_content_type: str = "application/json",
        additional_headers: Optional[dict[str, str]] = None,
        read_semantic_post: bool = False,
        allow_unusable_success_body: bool = False,
    ) -> Any:
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"

        body = None
        headers = {
            "Accept": "application/json",
            "Authorization": self._authorization,
            "REST-Framework-Version": "9",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = payload_content_type
        if additional_headers:
            headers.update(additional_headers)

        normalized_method = method.upper()
        is_write = normalized_method not in {"GET", "HEAD", "OPTIONS"} and not (
            normalized_method == "POST" and read_semantic_post
        )
        can_refresh_and_retry = (
            normalized_method == "GET" or read_semantic_post
        ) and self._refresh_authorization is not None

        for attempt in range(2 if can_refresh_and_retry else 1):
            headers["Authorization"] = self._authorization
            request = Request(url, data=body, headers=headers, method=normalized_method)
            try:
                with self._opener(request, timeout=self.timeout) as response:
                    status = response.status
                    try:
                        response_body = response.read()
                    except (HTTPException, OSError) as error:
                        if allow_unusable_success_body:
                            return {"status": status}
                        if is_write:
                            raise SuccessResponseError(
                                "Oracle Fusion REST returned HTTP "
                                f"{status}, but its response body could not be read."
                            ) from error
                        raise ApiError(
                            "Oracle Fusion REST request failed during transport while "
                            f"reading its HTTP {status} response: {error}"
                        ) from error
                    try:
                        return _decode_success_body(response_body, status)
                    except SuccessResponseError as error:
                        if allow_unusable_success_body:
                            return {"status": status}
                        if read_semantic_post:
                            raise ApiError(str(error)) from error
                        raise
            except HTTPError as error:
                if (
                    error.code in {401, 403}
                    and attempt == 0
                    and can_refresh_and_retry
                ):
                    error.close()
                    refreshed = self._refresh_authorization()
                    if not isinstance(refreshed, str) or not refreshed.strip():
                        raise ApiError(
                            "Fusion authentication refresh returned no authorization."
                        )
                    self._authorization = refreshed
                    continue
                try:
                    detail = _decode_error_body(error.read(), error.code)
                except (HTTPException, OSError):
                    detail = {"status": error.code, "body": "unavailable"}
                raise ApiError(
                    f"Oracle Fusion REST request failed with HTTP {error.code}: {detail}"
                ) from error
            except URLError as error:
                if is_write:
                    raise IndeterminateWriteError(
                        "The Run Book write was dispatched, but no response was "
                        f"received: {error.reason}"
                    ) from error
                raise ApiError(
                    f"Oracle Fusion REST request could not be reached: {error.reason}"
                ) from error
            except (HTTPException, OSError) as error:
                if is_write:
                    raise IndeterminateWriteError(
                        "The Run Book write was dispatched, but its outcome is "
                        f"unknown: {error}"
                    ) from error
                raise ApiError(
                    f"Oracle Fusion REST request failed during transport: {error}"
                ) from error

        raise ApiError("Oracle Fusion REST request failed after authentication refresh.")
