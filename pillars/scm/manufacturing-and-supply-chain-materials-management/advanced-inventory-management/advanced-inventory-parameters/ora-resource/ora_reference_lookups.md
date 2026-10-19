# Advanced Inventory Parameters Reference Lookups

Applies only to the REST-backed BO route. FSM archives bypass these resolvers: preserve native codes and names, including `CrossDockItemCategoryCode` and `PutAwaySuggestionP1`–`PutAwaySuggestionP4`. The pending REST Cycle Count meaning resolver does not make the observed FSM `CycleCountCountingMode` column unsupported; its native domain still requires verification.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
| --- | --- | --- | --- | --- | --- | --- | --- |
| resolve_advanced_inventory_counting_mode | `PhysicalInvCountingModeMeaning` is supplied as a display value | The supplied physical counting-mode meaning | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_INV_PHY_INV_COUNT_METHOD'&fields=LookupCode,LookupType,Meaning&onlyData=true` | `LookupCode`, `LookupType`, `Meaning` | Trim outer whitespace and require exactly one case-insensitive exact `Meaning` match. Never fuzzy-match or select the first result. | `PhysicalInvCountingMode`: `LookupCode` | Stop Data Loader handoff for zero or multiple exact matches, a lookup read failure, or conflicting supplied display value and code. |
| resolve_advanced_inventory_crossdock_due_date_sort | `CrossDockDueDateSortMeaning` is supplied as a display value | Supplied due-date-sort meaning | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_PICK_SEQUENCE_RULE_SORT'&fields=LookupCode,LookupType,Meaning&onlyData=true` | `LookupCode`, `LookupType`, `Meaning` | Trim outer whitespace and require exactly one case-insensitive exact `Meaning` match. Never fuzzy-match or select the first result. | `CrossDockDueDateSort`: `LookupCode` | Stop Data Loader handoff for zero or multiple exact matches, a lookup read failure, or conflicting supplied display value and code. |
| resolve_advanced_inventory_putaway_priority | A put-away priority display value is supplied | Supplied priority meaning and target priority field | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_RCV_PUT_AWAY_SUGGESTIONS'&fields=LookupCode,LookupType,Meaning&onlyData=true` | `LookupCode`, `LookupType`, `Meaning` | Trim outer whitespace and require exactly one case-insensitive exact `Meaning` match. Resolve every supplied meaning before final priority validation; do not reject against intermediate or earlier slot values. Never fuzzy-match or select the first result. | `PutAwaySuggestionPriorityOne`, `PutAwaySuggestionPriorityTwo`, `PutAwaySuggestionPriorityThree`, or `PutAwaySuggestionPriorityFour`: `LookupCode` | Stop Data Loader handoff for zero or multiple exact matches, a lookup read failure, or conflicting supplied display value and code. Final excluded-code and duplicate checks belong to ora_input_validation.md. |

## Lookup Inventory

| UI area | Display attribute | Backend value | Source evidence | Resolver status |
| --- | --- | --- | --- | --- |
| Physical inventory counting mode | `PhysicalInvCountingModeMeaning` | `PhysicalInvCountingMode` | `ORA_INV_PHY_INV_COUNT_METHOD` maps the stored lookup code to `Meaning`. | Resolver defined above. |
| Cycle-count counting mode | `CycleCountCountingModeMeaning` | `CycleCountCountingMode` | No matching control or payload mapping found in the supplied Redwood source; user feature validation is pending. | Unverified: block requests requiring this meaning resolution until evidence is confirmed. No active Cycle Count resolver. |
| Cross-dock due-date sort | `CrossDockDueDateSortMeaning` | `CrossDockDueDateSort` | `WSH_PICK_SEQUENCE_RULE_SORT` maps the stored lookup code to `Meaning`. | Resolver defined above. |
| Put-away suggestion priorities 1–4 | `PutAwaySuggestionPriority{One,Two,Three,Four}Meaning` | `PutAwaySuggestionPriority{One,Two,Three,Four}` | `ORA_RCV_PUT_AWAY_SUGGESTIONS` maps each stored lookup code to `Meaning`; selected priority codes are excluded from later priority LOVs. | Resolver defined above. |
| Cross-dock item category | `CrossDockItemCategoryName` | `CrossDockItemCategoryName` | The registered business object exposes `CrossDockItemCategoryName` as writable. Preserve the supplied category name without local resolution. | Direct pass-through; no resolver. |

## Resolution and Handoff

The three standard lookup paths use the selected task environment; do not embed a pod host or runtime revision. Collect all result pages needed to establish a unique exact match. A failed or incomplete read cannot establish no-match or uniqueness.

Treat `PhysicalInvCountingModeMeaning`, `CrossDockDueDateSortMeaning`, and `PutAwaySuggestionPriority{One,Two,Three,Four}Meaning` as friendly input fields. After successful resolution and conflict checking, consume these fields and retain only their target codes in write data; preserve original meanings in validation evidence. Never send unresolved meanings to Data Loader. An explicitly null or blank meaning must not trigger a default or be guessed; request clarification if it cannot be resolved.

Run `ADV_INV_PARAMS.VALIDATE_EFFECTIVE_VALUES` after resolution or when resolution is not applicable. This node owns final priority exclusions and duplicate checks for both direct and resolved codes. Supplying only codes must not bypass it. A supplied `CycleCountCountingModeMeaning` blocks this stage pending feature verification; it must not fall through as an ordinary field.

`CrossDockItemCategoryName` remains exact direct pass-through by user-approved policy. This intentionally differs from the Redwood category chooser, which selects `CategoryId`; do not restore an item-category resolver.

## Parent and DFF Relationship

`InvAdvancedInvParamsDFF` is exposed by `InvAdvancedInvParamsVO` as a view-link accessor and is represented as a child section of the `advancedInventoryParameters` parent template. This relationship is not a display-value lookup, does not create a local resolver, and does not require separate child-BO registration or invocation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ADV_INV_PARAMS.RESOLVE_REFERENCE_LOOKUPS | step | 30 | reference_lookup | resolved->ADV_INV_PARAMS.VALIDATE_EFFECTIVE_VALUES;not-applicable->ADV_INV_PARAMS.VALIDATE_EFFECTIVE_VALUES;blocked->ADV_INV_PARAMS.RETURN_ISSUES;failure->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.CHECK_READINESS | stop | Evaluate supplied meanings for every request; resolve supported meanings, block unverified Cycle Count meanings, or take not-applicable for code-only inputs. |
