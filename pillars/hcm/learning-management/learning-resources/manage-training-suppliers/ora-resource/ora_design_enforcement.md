# Manage Training Suppliers Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve identity | Keep the user-provided supplier name without business-name rewriting |
| 2 | Resolve ambiguity | Obtain explicit intent for same-name suppliers and ambiguous contacts |
| 3 | Build proposal | Show provenance, warnings, blockers, and exact proposed action per row |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every supplier row | Blocker |  | Name was derived, defaulted, recommended, or is blank | Require a user-provided name | Yes |
| Description is blank | Warning |  | None | Recommend a short operational description but permit creation | Yes |
| Contact is blank | Warning |  | None | Recommend a contact but permit creation | Yes |
| Same-name suppliers exist | Blocker | inspect_existing_training_suppliers | User has not chosen use-existing or create-another | Show identifiers and statuses and request intent | Yes |
| Set filtering is enabled | Blocker | validate_required_supplier_configuration | Set is absent, inaccessible, ambiguous, or invalid | Require one accessible Set and disclose immutability | Yes |
| Every create proposal | Blocker |  | REST upload or Data Loader has not been selected explicitly | Present both routes; recommend REST for one row and Data Loader for multiple rows | Yes |
| Approved proposal | Blocker |  | Execution route differs from the approved proposal | Build and approve a new proposal version | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_existing_training_suppliers | Before proposing creation | Existing supplier identifiers and statuses | ora_reference_lookups.md |
| validate_required_supplier_configuration | Required tenant configuration applies | Set and required flexfield values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.ENFORCE_DESIGN | decision | 4 | design_enforcement | passed->TS.APPROVAL_GATE;blocked->TS.BLOCKED;failure->TS.FAILED | TS.CHECK_DEPENDENCIES | stop | Before displaying the versioned proposal |
