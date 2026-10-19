"""Offline FSM export identity checks; never a global HZ location lookup.

Parent references come from the exact task CSV metadata. Receipt-from identity
is corroborated by RemitToAddressEO.AltCriteria. Import matching is defined by
RemitToServiceAMImpl.deriveLocationId and LocationVO.LocationVOCriteria.
This module does not grant operation support or generate an import package.
"""
from __future__ import annotations

PARENT = "AR_REMIT_TO_LOCATION"
CHILD = "AR_REMIT_TO_ADDRESS"
PARENT_FIELDS = (
    "SetCode", "TerritoryCode", "Address1", "OrigSystemReference",
    "PostalCode", "State", "City",
)
CRITERIA_FIELDS = ("Country", "State", "PostalCodeLow", "PostalCodeHigh")
IMPORT_MATCH_FIELDS = (
    "Address1", "OrigSystemReference", "TerritoryCode", "PostalCode", "State", "City",
)
# These values are copied only on the new-location branch, not the reuse branch.
CREATE_ONLY_POSTAL_FIELDS = (
    "Address2", "Address3", "Address4", "County", "Province",
    "AddrElementAttribute2", "AddrElementAttribute3",
)


class IdentityError(ValueError):
    """An export/reference/selection failure, not an API availability issue."""


def operation_questions(operations: list[dict], supported: list[str]) -> list[dict]:
    """Retain every unresolved lifecycle request instead of failing on row one.

    This intake check does not extend the FSM import contract. UI criteria
    removal and update-enabled attributes do not establish CSV lifecycle support.
    """
    questions = []
    explanations = {
        "update": (
            "Which existing postal address or customer-coverage rule should change, and which values should be different?",
            "The requested update needs an exact target and a field-specific FSM update contract; CSV column presence alone is insufficient.",
        ),
        "delete": (
            "Do you want to remove the postal destination itself or only the customer-coverage rule that uses it?",
            "Oracle's task CSV import does not delete existing records. Removing a CSV row or assigning status D is not an authorized delete mechanism.",
        ),
        "end-date": (
            "When should this stop applying, and should that affect the address or only particular customer coverage?",
            "The reviewed task CSV has no end-date field; a status change must not be substituted for a requested date.",
        ),
    }
    for position, operation in enumerate(operations, 1):
        if not isinstance(operation, dict):
            continue  # The adapter's shape validator owns malformed rows.
        action = operation.get("action")
        supported_update = (operation.get("entity") == CHILD
                            and isinstance(operation.get("values"), dict)
                            and set(operation["values"]) == {"Status"})
        if isinstance(action, str) and action in supported and (action != "update" or supported_update):
            continue
        question, gap = explanations.get(action if isinstance(action, str) else "", (
            "Should this row create a new address, change an existing one, or retire customer coverage?",
            "An explicit supported operation must be resolved before packaging.",
        ))
        questions.append({
            "code": "OPERATION_CONTRACT_REQUIRED",
            "operationId": operation.get("id", f"OP-{position:03d}"),
            "row": position,
            "action": action,
            "question": question,
            "evidenceGap": gap,
            "nextOwner": "task-skill-developer",
            "answerAloneEnablesImport": False,
        })
    return questions


def text(row: dict, field: str) -> str:
    value = row.get(field, "")
    if not isinstance(value, str):
        raise IdentityError(f"{field} must be a CSV string; do not coerce identifiers.")
    return value


def parent_key(row: dict, prefix: str = "") -> tuple[str, ...]:
    """Exact exported transport reference, including meaningful blank fields."""
    values = tuple(text(row, prefix + field) for field in PARENT_FIELDS)
    if not values[0] or not values[1]:
        raise IdentityError("A parent reference requires SetCode and TerritoryCode.")
    return values


def criteria_key(row: dict) -> tuple[str, ...]:
    return parent_key(row, PARENT + ".") + tuple(text(row, f) for f in CRITERIA_FIELDS)


def coverage_unique_key(row: dict) -> tuple[str, ...]:
    """RA_REMIT_TOS_U1 scope, distinct from the parent-qualified transport key.

    Source ra_remit_tos_all.table index lines 1066-1088: STATE, COUNTRY,
    POSTAL_CODE_LOW, POSTAL_CODE_HIGH, SET_ID. Parent and Status are absent.
    SetCode is the export's resolved business reference to SET_ID. Preserve
    exact strings and blanks; do not infer range-overlap semantics.
    """
    return (text(row, PARENT + ".SetCode"),) + tuple(text(row, f) for f in CRITERIA_FIELDS)


def key_fields(entity: str) -> tuple[str, ...]:
    if entity == PARENT:
        return PARENT_FIELDS
    if entity == CHILD:
        return tuple(PARENT + "." + f for f in PARENT_FIELDS) + CRITERIA_FIELDS
    raise IdentityError("Unknown Remit-to entity")


def import_key(entity: str, row: dict) -> tuple[str, ...]:
    result = parent_key(row) if entity == PARENT else criteria_key(row)
    if entity == CHILD and not text(row, "Country"):
        raise IdentityError("Which customers' country or default coverage should use this address?")
    return result


def parent_dependencies(operations: list[dict], exported: dict) -> dict:
    """Resolve required parent rows, without widening the requested mutation."""
    parents = dict(exported[PARENT])
    explicit = set()
    for op in operations:
        if op["entity"] == PARENT:
            row = dict(op["targetKey"], **op["values"])
            key = parent_key(row)
            parents[key] = row
            explicit.add(key)
    dependencies = {}
    for op in operations:
        if op["entity"] != CHILD:
            continue
        key = criteria_key(op["targetKey"])[:len(PARENT_FIELDS)]
        if key not in parents:
            raise IdentityError("Which exact exported or newly requested remit-to address owns this coverage?")
        row = dict(exported[CHILD].get(criteria_key(op["targetKey"]), {})) if op["action"] == "update" else {}
        row.update(op["values"])
        if text(row, "SetCode") != key[0]:
            raise IdentityError("Receipt-from SetCode must match its selected parent's set.")
        if key not in explicit:
            dependencies[key] = dict(parents[key])
    return dependencies


def validate_creates(operations: list[dict], exported: dict) -> None:
    """Reject known collisions/reuse drift, but do not assert global absence."""
    proposed = list(exported[PARENT].values())
    for op in operations:
        if op["action"] != "create" or op["entity"] != PARENT:
            continue
        row = dict(op["targetKey"], **op["values"])
        validate_postal_input(row)
        match = inspect_import_match(row, proposed)
        if match["status"] != "FSM_RESOLUTION_REQUIRED":
            raise IdentityError("Clarify the postal destination: " + match["status"])
        # A blank external reference is an omitted service predicate, not an
        # empty-identity value that guarantees a new remit-to parent.
        for existing in proposed:
            one = inspect_import_match(row, [existing])
            if one["exportedMatchCount"] and text(row, "SetCode") == text(existing, "SetCode"):
                raise IdentityError("This address already exists in the selected set; was an update intended?")
        proposed.append(row)
    parent_dependencies(operations, exported)
    # Inactivation does not release the set-wide coverage key, even in a batch.
    coverage = {coverage_unique_key(row): row for row in exported[CHILD].values()}
    for op in operations:
        if op["action"] != "create" or op["entity"] != CHILD:
            continue
        row = dict(op["targetKey"], **op["values"])
        key = coverage_unique_key(row)
        if key in coverage:
            owner = text(coverage[key], PARENT + ".Address1")
            raise IdentityError(
                f"Coverage collision for {op['id']}: the same country, state and postal bounds "
                f"already belong to {owner!r} in reference set {key[0]!r}, or were requested "
                "earlier in this batch. Inactive coverage still reserves this combination. "
                "Which different customer coverage is intended, or did you mean to change "
                "the existing coverage? Moving coverage to another destination is not a "
                "supported Status-only update; no partial package will be generated."
            )
        coverage[key] = row


def validate_postal_input(row: dict) -> None:
    """Local business-input checks, not a replica of target CDM validation.

    LocationEO.Country is mandatory with precision 2. Do not invent a universal
    state/city/postal requirement or a country domain from a partial task export.
    Requiring an address line is this skill's complete-destination intake rule,
    not a claim that LocationEO always marks Address1 mandatory.
    """
    country = text(row, "TerritoryCode")
    if len(country) != 2 or not country.isascii() or not country.isalpha() or country != country.upper():
        raise IdentityError("Which destination country is intended? Resolve it to its exact two-letter country code; receipt-from DEFAULT is not a destination country.")
    if not text(row, "Address1").strip():
        raise IdentityError("What is the destination's street address or postal address line? Do not infer it from customer coverage.")


def postal_application_validation(operations: list[dict]) -> list[dict]:
    """Immutable disclosure of server-owned work; never a passed receipt."""
    return [{
        "operationId": op["id"],
        "entity": PARENT,
        "policy": "fsm-postal-application-validation-v1",
        "status": "pending_import",
        "executionOwner": "core.data-loader:FSM",
        "checks": ["target-country-and-address-validation", "shared-location-resolution"],
        "sharedLocationMayBeReused": True,
        "globalUniquenessProven": False,
        "completionRequires": ["successful-process-without-unresolved-warnings",
                               "fresh-exact-task-export", "all-requested-values-reconciled"],
    } for op in operations if op.get("action") == "create" and op.get("entity") == PARENT]


def persisted_key(entity: str, candidate: dict, persisted: dict) -> tuple[str, ...]:
    """Allow only the source-proven omitted external-reference derivation.

    All other reference components remain exact, including intentional blanks.
    Multiple matches are a failure, never a first-row choice.
    """
    key = import_key(entity, candidate)
    reference = "OrigSystemReference" if entity == PARENT else PARENT + ".OrigSystemReference"
    if text(candidate, reference):
        return key
    fields = key_fields(entity)
    matches = [actual for actual in persisted if all(
        field == reference or actual[i] == key[i] for i, field in enumerate(fields)
    )]
    if len(matches) != 1:
        raise IdentityError("Generated external reference must resolve to exactly one persisted record.")
    if not matches[0][fields.index(reference)]:
        raise IdentityError("Persisted external reference is still empty.")
    return matches[0]


def index_export(rows: dict, headers: dict) -> dict:
    """Check exact-task exported rows only; no global-absence assertion."""
    refs = [f for f in headers.get(CHILD, []) if f.startswith(PARENT + ".")]
    expected = [PARENT + "." + f for f in PARENT_FIELDS]
    if refs != expected or any(f not in headers.get(PARENT, []) for f in PARENT_FIELDS):
        raise IdentityError("Parent-reference headers differ from the reviewed task metadata.")
    parents, children = {}, {}
    for number, row in enumerate(rows.get(PARENT, []), 2):
        key = parent_key(row)
        if key in parents:
            raise IdentityError(f"Duplicate exported parent reference at CSV record {number}.")
        parents[key] = row
    for number, row in enumerate(rows.get(CHILD, []), 2):
        key = criteria_key(row)
        pkey = key[:len(PARENT_FIELDS)]
        if pkey not in parents:
            raise IdentityError(f"Receipt-from CSV record {number} has no exact exported parent.")
        if text(row, "SetCode") != pkey[0]:
            raise IdentityError(f"Receipt-from CSV record {number} differs from its parent's set.")
        if key in children:
            raise IdentityError(f"Duplicate receipt-from identity at CSV record {number}.")
        children[key] = row
    return {PARENT: parents, CHILD: children}


def select_parent(index: dict, selector: dict) -> dict:
    """Resolve explicit business selection, without changing case or blank scope."""
    if not isinstance(selector, dict) or not selector:
        raise IdentityError("Which remit-to address and reference data set do you mean?")
    if set(selector) - set(PARENT_FIELDS):
        raise IdentityError("Use the exported address and reference-set fields to identify the parent.")
    if not text(selector, "SetCode"):
        raise IdentityError("Which reference data set should own the remit-to address?")
    for field in selector:
        text(selector, field)
    matches = [row for row in index[PARENT].values()
               if all(text(row, field) == value for field, value in selector.items())]
    if not matches:
        raise IdentityError("No exported remit-to address matches; clarify the target, not a create fallback.")
    if len(matches) != 1:
        raise IdentityError("More than one exported address matches; specify the address or external reference.")
    return dict(matches[0])


def bind_criteria(parent: dict, values: dict) -> dict:
    """Derive all seven child references from the selected parent, never IDs."""
    parent_key(parent)
    if any(field.startswith(PARENT + ".") for field in values):
        raise IdentityError("Parent references are derived, not separately supplied child values.")
    if "SetCode" in values and text(values, "SetCode") != text(parent, "SetCode"):
        raise IdentityError("Receipt-from coverage must use the selected parent's reference set.")
    result = dict(values)
    result["SetCode"] = text(parent, "SetCode")
    result.update({PARENT + "." + field: text(parent, field) for field in PARENT_FIELDS})
    return result


def inspect_import_match(request: dict, exported_parents: list[dict]) -> dict:
    """Model known FSM matching hazards, not complete shared-location cardinality.

    Missing/empty XML inputs omit optional predicates; whitespace is not trimmed.
    UPPER comparison is modeled only for ASCII Address1/City. Non-ASCII matching
    needs target collation evidence and is returned as unresolved, never guessed.
    """
    supplied = {field: text(request, field) for field in IMPORT_MATCH_FIELDS
                if text(request, field) != ""}
    if not supplied:
        raise IdentityError("Provide a postal destination; the FSM import would report Address is empty.")
    if any(not value.isascii() for field, value in supplied.items() if field in {"Address1", "City"}):
        return {"status": "COLLATION_EVIDENCE_REQUIRED", "globalAbsenceProven": False,
                "exportedMatchCount": None, "ignoredChangeFields": []}
    matches = []
    for row in exported_parents:
        equal = True
        collation_unknown = False
        for field, value in supplied.items():
            actual = text(row, field)
            if field in {"Address1", "City"}:
                if not actual.isascii():
                    # All supplied predicates are conjunctive. A different
                    # country, reference, postal code, or safely comparable
                    # address component can exclude this row without guessing
                    # its non-ASCII uppercase behavior.
                    collation_unknown = True
                    continue
                actual, value = actual.upper(), value.upper()
            if actual != value:
                equal = False
                break
        if equal:
            if collation_unknown:
                return {"status": "COLLATION_EVIDENCE_REQUIRED", "globalAbsenceProven": False,
                        "exportedMatchCount": None, "ignoredChangeFields": []}
            matches.append(row)
    ignored = sorted({field for row in matches for field in CREATE_ONLY_POSTAL_FIELDS
                      if field in request and text(request, field) != text(row, field)})
    return {
        "status": ("KNOWN_REUSE_VALUE_CONFLICT" if ignored else
                   "KNOWN_AMBIGUOUS_LOCATION_MATCH" if len({text(r, "OrigSystemReference") for r in matches}) > 1 else
                   "FSM_RESOLUTION_REQUIRED"),
        "globalAbsenceProven": False,
        "exportedMatchCount": len(matches),
        "ignoredChangeFields": ignored,
    }


def preservation_issues(before: dict, after: dict, headers: dict, audit_fields: dict,
                        permitted_changes: dict | None = None) -> list[dict]:
    """Protect baseline rows while permitting unrelated concurrent additions.

    permitted_changes maps (entity, exact exported key) to explicitly requested
    fields. It never permits deletion, key changes or arbitrary target-row drift.
    """
    permitted_changes = permitted_changes or {}
    issues = []
    for entity in (PARENT, CHILD):
        for key, old in before[entity].items():
            new = after[entity].get(key)
            if new is None:
                issues.append({"entity": entity, "kind": "BASELINE_ROW_MISSING", "key": key})
                continue
            allowed = set(permitted_changes.get((entity, key), ())) | set(audit_fields[entity])
            changed = [f for f in headers[entity] if f not in allowed and text(old, f) != text(new, f)]
            if changed:
                issues.append({"entity": entity, "kind": "BASELINE_VALUES_CHANGED",
                               "key": key, "fields": changed})
    return issues
