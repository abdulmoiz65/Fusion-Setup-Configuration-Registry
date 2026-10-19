# Design Enforcement

## Design Rules
| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any REST request | Error | resolve_customer_data_hub_note_type | ZMM_NOTE_TYPE, Standard category, or Extensible level not proven | Reconcile current GET | Yes |
| Create | Error | resolve_customer_data_hub_note_type | Code exists, begins ORA_, or upsert is enabled | Use a unique nonreserved code | Yes |
| Update/delete | Error | resolve_customer_data_hub_note_type | Custom origin, describe, preview, or approval not proven | Complete exact preflight | Yes |
| Any mutation | Error | resolve_customer_data_hub_note_type | Rename, parent/module/security/level change, Tag change, or seeded destructive change | Refuse unsupported fields | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_customer_data_hub_note_type | Before any REST read or mutation preview | Exact ZMM_NOTE_TYPE identity, Standard category, Extensible level, current type/code values, seed evidence, links, and describe metadata | ora_reference_lookups.md |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.ENFORCE | decision | 40 | design_enforcement | pass->NT.READY;fail->NT.ERROR | NT.DEPENDENCIES | stop | Before REST or setup-data readiness. |
