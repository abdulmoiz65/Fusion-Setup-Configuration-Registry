"""Resolve Default Set names and explicitly labeled codes from a live set collection."""


class ReferenceSetResolutionError(ValueError):
    pass


def resolve_reference_set(rows, *, set_name=None, set_code=None):
    """Return one canonical set record.

    Ordinary user input is represented as ``set_name``.  ``set_code`` is only
    accepted when the caller explicitly labeled the input as a code.
    """
    if ((set_name is None) == (set_code is None)
            or not isinstance(rows, list)
            or any(not isinstance(row, dict) for row in rows)):
        raise ReferenceSetResolutionError("Supply exactly one of set_name or explicitly labeled set_code with a set collection.")
    value = set_name if set_name is not None else set_code
    if not isinstance(value, str) or not value.strip():
        raise ReferenceSetResolutionError("The supplied default set value must be nonblank text.")
    field = "SetName" if set_name is not None else "SetCode"
    matches = [row for row in rows if row.get(field) == value]
    if len(matches) != 1:
        kind = "name" if field == "SetName" else "code"
        raise ReferenceSetResolutionError(f"Default set {kind} must match exactly one returned set; found {len(matches)} matches.")
    match = matches[0]
    if (not isinstance(match.get("SetCode"), str) or not match["SetCode"].strip()
            or not isinstance(match.get("SetName"), str) or not match["SetName"].strip()):
        raise ReferenceSetResolutionError("The matched set is missing canonical SetCode or SetName.")
    result = {"SetCode": match["SetCode"], "SetName": match["SetName"],
              "ResolutionBasis": "explicit_set_code" if field == "SetCode" else "default_set_name"}
    if isinstance(match.get("Description"), str):
        result["Description"] = match["Description"]
    return result
