# Manage Legal Reporting Unit Registrations Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Two-level parent gate | Entity and LRU resolve exactly, are effective, and ownership matches |
| 2 | Jurisdiction/address gate | One compatible jurisdiction and one exact active address resolve |
| 3 | Collision/identifying gate | No same-LRU match, sibling collision, ambiguity, or second identifying row exists |
| 4 | Authority/function/package gate | Authority values are null, function CSV is empty, and exact unchanged parent rows/hierarchy are present; this graph validates final-package readiness, while the selected task SKILL.md local FSM workflow constructs the archive; resource rules do not construct, approve, upload, or import it |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every CREATE | Error | verify_lru_registration_parents | Entity/LRU is absent, inactive, ineffective, ambiguous, mismatched, or ownership differs | Resolve both exact parents | Yes |
| Every CREATE | Error | resolve_lru_registration_jurisdiction | Jurisdiction is absent, inactive, ineffective, incompatible, or ambiguous | Select one active compatible jurisdiction | Yes |
| Every CREATE | Error | resolve_lru_registration_address_exact | Address is absent, inactive, ambiguous, or country-incompatible | Resolve one exact address natural key | Yes |
| Before CREATE | Error | find_lru_registration_conflict | Same-LRU match, sibling collision, ambiguity, or second identifying registration exists | Reuse or make explicit update/design decision | Yes |
| Every supported candidate | Error | resolve_lru_enabled_function_code | Any authority/function value is present or function CSV contains a candidate row | Remove unsupported values and preserve zero rows | Yes |
| Package preview | Error | verify_lru_registration_package | Either unchanged parent, current hierarchy/header, empty child, or fingerprint evidence is absent | Refresh the target export and rerun the selected task SKILL.md local FSM package-preparation workflow | Yes |

## Resolved Scope Decisions

| ID | Status | Enforced Contract | Future Expansion Gate |
|---|---|---|---|
| LS-TBD-007 | Resolved for supported scope | Authority is optional and unsupported; authority/site carriers remain null; supplied authority blocks | Exact active eligible XLE authority plus active identifying authority-site/address resolver |
| LS-TBD-008 | Resolved for supported scope | Function CSV has zero candidate rows; supplied function blocks; enabled lookup proves code/meaning only | JurisdictionFunctionVO or XLE_JUR_FUNCTIONS permission resolver plus LS-TBD-007 authority/site contract |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_lru_registration_parents | Every CREATE | Entity/LRU natural keys, ownership, effective receipt | ora_reference_lookups.md |
| resolve_lru_registration_jurisdiction | Every CREATE | Jurisdiction name, identifying flag, label, context | ora_reference_lookups.md |
| resolve_lru_registration_address_exact | Every CREATE | Exact FormattedAddress natural key | ora_reference_lookups.md |
| find_lru_registration_conflict | Before CREATE | Same-LRU and sibling collision receipt | ora_reference_lookups.md |
| resolve_lru_enabled_function_code | Function input is supplied for scope assessment | Enabled code/meaning receipt that does not authorize CREATE | ora_reference_lookups.md |
| verify_lru_registration_package | Before final-package readiness validation | Both unchanged parents, hierarchy, headers, empty function child, preservation, and baseline fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->LRUR.PACKAGE_PREVIEW_GATE;blocked->LRUR.HANDLE_ERROR | LRUR.APPLY_DEFAULTS | stop | Before final-package readiness validation |
