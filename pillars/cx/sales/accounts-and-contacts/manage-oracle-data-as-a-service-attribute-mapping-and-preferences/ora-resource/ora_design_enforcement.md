# Design Enforcement

Enforce the user's selected-row intent. Omitted CSV rows are unchanged by the
FSM import and must not be interpreted as deletions.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Preserve current state | Use the fresh-export row when present and the complete seeded row only when the pod omits it |
| 2 | Apply explicit changes | Modify only allowlisted fields named in the user's change set |
| 3 | Minimize import scope | Write exactly the selected keys to both Oracle CSV members |
| 4 | Bind approval | Route the exact ZIP, hash, target, validation result, and row preview to Data Loader |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A row change is requested | Error | | Key is absent, ambiguous, blank, or not present in the complete seeded catalog | Correct the exact AttributeCategory and DaasAttributeName | Yes, before preview |
| A field change is requested | Error | | Field is outside the allowlist or a preference flag is not Y or N | Supply only documented editable fields and accepted values | Yes, before preview |
| A mapping-field change is requested | Error | validate_fusion_mapping_attributes | Effective object/attribute state is inconsistent, target-pod metadata is missing or incomplete, or a nonblank attribute lacks an exact case-sensitive `AttributeCode` match | Correct the exact pair or metadata-access gap; do not substitute a seeded or documented list | Yes, before preview |
| Display During Real-time Enrichment is requested | Error | | The user-facing display checkbox is not represented by an editable selected-row FSM field | Explain that it requires the separate task UI/manual route; do not substitute `AutofillBlank` or `AutoupdateNonBlank` | No, for this package |
| A package is prepared | Error | | Either CSV contains an unrequested key, omits a selected key, or the two members contain different selected key sets | Rebuild the package from the validated source export and catalog | Yes, before preview |
| An import is ready | Error | | ZIP, hash, target, task code, or row preview differs from the Data Loader approval preview | Revalidate and create a fresh Data Loader preview | Yes, with fresh approval |
| A create, delete, reset, or whole-baseline request is made | Error | | Requested operation exceeds selected existing-row updates | Refuse and route only a supported selected-row change | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| validate_fusion_mapping_attributes | A requested change includes `FusionObjectName` or `FusionAttributeName` | Complete exact-object `AttributeCode` catalog and validation result for every effective pair | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| DAAS.ENFORCE_SELECTED_ROWS | step | 4 | design_enforcement | pass->DAAS.APPROVAL;fail->DAAS.ERROR | DAAS.RESOLVE_FUSION_ATTRIBUTES | stop | Before an immutable Data Loader approval preview |
