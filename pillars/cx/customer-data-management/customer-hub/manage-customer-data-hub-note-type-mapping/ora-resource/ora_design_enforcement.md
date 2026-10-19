# Design Enforcement

## Design Rules
| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| REST read | Error | resolve_note_type_mapping | Target environment, source-object scope, or exact code filter is ambiguous; SourceObjectCode is outside NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST | Resolve one environment; use NOTE by default or one supported exact source object and exact code filter when supplied | Yes |
| REST mutation | Error | resolve_note_type_mapping | Any POST, PATCH, DELETE, or PUT is requested | Refuse; live resource is read-only | No |
| Mapping change | Error |  | Apps Common is selected as the mapping writer | Use supported FSM route or guided UI | Yes |
| FSM ZIP | Error |  | Metadata/hash/envelope unsafe or wrong task | Rebuild Core Data Loader preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_note_type_mapping | Before every REST mapping read | Exact environment, supported noteTypes GET route, SourceObjectCode defaulted to NOTE or one supported exact source object, optional exact mapped-code filter, and returned mapping fields | ora_reference_lookups.md |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.ENFORCE | decision | 40 | design_enforcement | pass->NTM.READY;fail->NTM.ERROR | NTM.DEPENDENCIES | stop | Before REST read or setup-data readiness. |
