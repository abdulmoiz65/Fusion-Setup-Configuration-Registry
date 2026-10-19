"""Complete, read-only CPQ reconciliation discovery through declared paths.

The caller supplies the existing authenticated, target-bound GET adapter. This
module neither authenticates independently nor follows links from responses.
"""

from __future__ import annotations

import urllib.parse
from typing import Any, Callable, Mapping

import cpq_live_contract as live


_ADAPTER_ORIGIN = "https://cpq-discovery.invalid"
_CHILDREN = ("CompanyProfiles", "CPQUsers")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise live.contract.ContractError(message)


def _identity(value: Any) -> str:
    _require(type(value) in (str, int) and bool(str(value).strip()),
             "CPQ reconciliation returned an invalid record identity.")
    return str(value).strip()


def _collection(name: str, read_json: Callable) -> list[dict[str, Any]]:
    path = live.ASSISTANT_PATH + "/child/" + name
    seen_rows: set[str] = set()
    seen_identities: set[tuple[str, str]] = set()

    def get_page(url, _auth, *, stage):
        # live.collection constructs every URL locally. Translate only that
        # fixed URL shape to the caller's already-approved read route.
        parsed = urllib.parse.urlsplit(url)
        _require(parsed.scheme == "https" and parsed.netloc == "cpq-discovery.invalid"
                 and parsed.path == path and not parsed.fragment,
                 "CPQ reconciliation attempted an undeclared discovery path.")
        pairs = urllib.parse.parse_qsl(parsed.query, strict_parsing=True)
        params = dict(pairs)
        _require(len(pairs) == len(params) and set(params) == {"onlyData", "limit", "offset"}
                 and params["onlyData"] == "true"
                 and params["limit"].isdigit() and params["offset"].isdigit(),
                 "CPQ reconciliation pagination parameters are invalid.")
        limit, offset = int(params["limit"]), int(params["offset"])
        response = read_json(path, {"onlyData": "true", "limit": limit, "offset": offset})
        _require(isinstance(response, dict) and isinstance(response.get("items"), list)
                 and type(response.get("hasMore")) is bool,
                 "CPQ reconciliation requires an explicit paginated collection response.")
        rows = response["items"]
        _require(len(rows) <= limit,
                 "CPQ reconciliation returned more records than the requested page limit.")
        for field, expected in (("count", len(rows)), ("offset", offset)):
            _require(field not in response or type(response[field]) is int and response[field] == expected,
                     "CPQ reconciliation page count or offset is inconsistent.")
        _require("limit" not in response or type(response["limit"]) is int
                 and 0 < response["limit"] <= limit and len(rows) <= response["limit"],
                 "CPQ reconciliation page limit is inconsistent.")
        for row in rows:
            _require(isinstance(row, dict), "CPQ reconciliation returned an invalid collection record.")
            fingerprint = live.contract.digest(live._clean(row))
            _require(fingerprint not in seen_rows,
                     "CPQ reconciliation repeated a record; completeness is unproven.")
            seen_rows.add(fingerprint)
            identities = []
            if name == "CompanyProfiles":
                ids = [_identity(row[field]) for field in ("Id", "CompanyProfileId") if field in row]
                _require(bool(ids) and len(set(ids)) == 1,
                         "CPQ reconciliation Company Profile identity is missing or ambiguous.")
                identities.append(("company", ids[0]))
            else:
                email = row.get("Email")
                _require(isinstance(email, str) and bool(email.strip()),
                         "CPQ reconciliation lacks an administrator email identity.")
                identities.append(("email", email.strip().casefold()))
                # Email is the required administrator identity. Generated
                # fields may still be null before final provisioning; check
                # their uniqueness only when the service supplies a value.
                identities.extend((field, _identity(row[field])) for field in ("Id", "CPQUserId")
                                  if field in row and row[field] is not None and row[field] != "")
            _require(all(identity not in seen_identities for identity in identities),
                     "CPQ reconciliation returned duplicate record identities.")
            seen_identities.update(identities)
        return response

    return live.collection(path, {"host": _ADAPTER_ORIGIN, "auth": None}, getter=get_page)


def discover(read_json: Callable[[str, Mapping[str, Any]], Any]) -> dict[str, Any]:
    """Return full CompanyProfiles and CPQUsers in the expanded response shape.

    Identity/status checks bracket the bounded child reads. Submission-status
    inspection may observe a non-editable status; its caller decides whether
    that status is eligible for a mutation or merely a read-only inspection.
    """
    before = read_json(live.ASSISTANT_PATH, {"onlyData": "true"})
    identity = live._assistant_identity(before)
    result = live._clean(before)
    for name in _CHILDREN:
        rows = _collection(name, read_json)
        result[name] = {"items": rows, "hasMore": False, "count": len(rows)}
    after = read_json(live.ASSISTANT_PATH, {"onlyData": "true"})
    _require(live._assistant_identity(after) == identity,
             "CPQ Setup Assistant changed during reconciliation discovery; verify current state again.")
    return result
