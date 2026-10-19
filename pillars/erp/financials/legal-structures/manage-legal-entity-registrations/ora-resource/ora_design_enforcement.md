# Manage Legal Entity Registrations Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Parent and reference gate | Parent, jurisdiction, and legal address resolve exactly and effective ranges are compatible |
| 2 | Collision and identifying gate | Complete scoped export shows no equivalent, conflicting, or second identifying registration |
| 3 | Authority/function scope gate | All authority values are null and the function CSV has zero candidate rows |
| 4 | Package gate | The exact unchanged current parent row and preserved empty function child are present in current target hierarchy; this graph validates final-package readiness, while the selected task SKILL.md local FSM workflow constructs the archive; resource rules do not construct, approve, upload, or import it |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every CREATE | Error | verify_registration_parent_entity | Parent is absent, inactive, ineffective, ambiguous, or mismatched | Resolve one effective entity and exact identifier | Yes |
| Every CREATE | Error | resolve_entity_registration_jurisdiction | Jurisdiction is absent, inactive, ineffective, incompatible, or ambiguous | Select one active compatible jurisdiction | Yes |
| Every CREATE | Error | resolve_entity_registration_address | Address is absent, inactive, ambiguous, or country-incompatible | Resolve one exact address natural key | Yes |
| Before CREATE | Error | find_entity_registration_conflict | Equivalent, conflicting, ambiguous, or second identifying registration exists | Reuse or make an explicit update/design decision | Yes |
| Every supported candidate | Error | resolve_enabled_registration_function_code | Any authority or function value is present, or function CSV has a candidate row | Remove unsupported values and preserve zero function rows | Yes |
| Package preview | Error | verify_entity_registration_package | Current parent row, hierarchy, header, empty child, or fingerprint evidence is absent | Refresh the target export and rerun the selected task SKILL.md local FSM package-preparation workflow | Yes |

## Resolved Scope Decisions

| ID | Status | Enforced Contract | Future Expansion Gate |
|---|---|---|---|
| LS-TBD-007 | Resolved for supported scope | Authority is optional and unsupported; authority/site carriers remain null and any supplied authority blocks | Exact active eligible XLE authority plus active identifying authority-site/address resolver |
| LS-TBD-008 | Resolved for supported scope | Function CSV has zero candidate rows; any supplied function blocks; fndStaticLookups proves enabled codes/meanings only | JurisdictionFunctionVO or XLE_JUR_FUNCTIONS permission resolver plus LS-TBD-007 authority/site contract |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_registration_parent_entity | Every CREATE | Parent identifier and effective receipt | ora_reference_lookups.md |
| resolve_entity_registration_jurisdiction | Every CREATE | Jurisdiction name, identifying flag, label, context | ora_reference_lookups.md |
| resolve_entity_registration_address | Every CREATE | Exact FormattedAddress natural key | ora_reference_lookups.md |
| find_entity_registration_conflict | Before CREATE | Existing definition and identifying-state receipt | ora_reference_lookups.md |
| resolve_enabled_registration_function_code | Function input is supplied for scope assessment | Enabled code/meaning receipt that does not authorize CREATE | ora_reference_lookups.md |
| verify_entity_registration_package | Before final-package readiness validation | Current parent, hierarchy, headers, empty function child, preservation, and baseline fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->LER.PACKAGE_PREVIEW_GATE;blocked->LER.HANDLE_ERROR | LER.APPLY_DEFAULTS | stop | Before final-package readiness validation |
