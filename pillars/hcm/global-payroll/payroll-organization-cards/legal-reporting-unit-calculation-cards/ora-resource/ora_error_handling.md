# Legal Reporting Unit Calculation Cards Error Handling

## REST Mutation Refusal

| Situation | What Must Happen |
|---|---|
| A direct REST calculation-card create, update, correction, end-date, or delete route is selected | Classify it as a policy blocker, do not call or retry the endpoint, discard the proposed payload, and prepare target-supported HDL instead |
| The target HDL action or key contract is not proven | Classify it as a catalog mismatch and stop; do not use REST as a fallback |

## Existing-Data Decision Handling

| Situation | Required response |
|---|---|
| Complete lookup finds no exact requested leaf business key | State that no existing matching data was found and continue as CREATE for that leaf while reusing existing parents |
| Existing card/component/override/FLEX/value/assignment/association or related row is found | Show business path, current value when relevant, interval, requested date, and adjacent future row; recommend Update or Correction and wait for the user's choice |
| Requested date equals selected EffectiveStartDate | Recommend Correction; do not attempt a same-date duplicate Update unless the live HDL contract explicitly supports it |
| Requested date is later inside the selected interval | Recommend Update to preserve earlier history; explain that Correction changes the whole selected slice |
| Same business key exists outside the requested date | Do not classify as create; show history/future intervals and offer only supported date-effective actions |
| Technical key is missing | Run the parent-scoped read-only resolver. If it remains ambiguous, ask for a business name/date-range discriminator, never the ID |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Tax reporting unit cannot be resolved | Stop and ask for a unique target owner |
| Legal reporting search text is empty or contains only `%` wildcards | Stop and ask for a meaningful name or registration-number fragment; do not execute an unbounded availability search |
| Legal reporting availability returns zero rows | Report that no legal reporting unit matched and ask the user to refine the search; do not classify this read-only result as a Fusion failure |
| Legal reporting availability returns multiple rows | Return only the candidate names, one per line, and complete a list-only request. Wait for an explicit selection only when downstream TRU or card work was also requested |
| Legal reporting availability response lacks `result.summary`, `result.items`, `Name`, or `EstablishmentId` | Classify as a Fusion API/source-contract failure and preserve redacted response diagnostics |
| Legislative Data Group name search is empty or contains only `%` wildcards | Stop and ask for a meaningful full or partial LDG name unless the request is a supported territory search with a nonblank restrictive filter |
| Legislative Data Group request has an empty query and no nonblank restrictive filter | Stop before POST; do not execute an unbounded search |
| US territory response contains `TerritoryShortName` other than `United States` | Classify as a response-contract failure and do not return or use the mismatched row |
| Legislative Data Group availability returns zero rows | Report that no Legislative Data Group matched and invite the user to refine the search; do not classify this read-only result as a Fusion failure |
| Legislative Data Group availability returns multiple rows | Return every candidate name, one per line, and complete a list-only request. Wait for selection only when downstream card work was also requested |
| Legislative Data Group availability response lacks `result.summary`, `result.items`, `Name`, or `LegislativeDataGroupId` | Classify as a Fusion API/source-contract failure and preserve redacted response diagnostics |
| Legislative Data Group availability paging fails before `hasMore=false` | Stop with a partial-results diagnostic; do not present the partial list as complete |
| Browser-routed `rv:` URL is stale or belongs to another environment | Resolve the route from the active environment; never reuse the captured host or route token |
| OrgTaxReportingUnitPVO returns no row for the internally resolved establishment key | Repeat owner resolution by TRU/legal-reporting-unit business name; ask for corrected business context only if no unique owner can be resolved |
| OrgTaxReportingUnitPVO returns multiple rows for the internally resolved establishment key | Show TRU/legal-reporting-unit business names and LDG names for selection; keep source and LDG IDs internal |
| Calculation card cannot be resolved | Stop and ask for a unique card reference or approved card-list lookup |
| Exact drilldown returns no card for the internally resolved dirCardId and date | Repeat owner-scoped business-name/history discovery; ask for corrected business context only if resolution remains impossible |
| getCardDetails mode=ADD returns no available cards | Stop and ask for a valid source owner, effective date, or card selection |
| getCardDetails returns a card outside sourceType=TRU or the selected sourceId | Stop and report a scope mismatch |
| Component-specific operation has no component rows | Stop and ask for a valid component selection |
| Component flexfield value lookup matches no component or multiple components | Stop and show component business names/effective intervals for selection; keep component sequence and IDs internal |
| Selected component has no FLEX override rows | Complete the read-only request successfully with `Flexfield values:` followed by `None` |
| Stored LOV value has no unique display meaning | Return the stored value for the read-only list and do not guess; if a later write is requested, require unique LOV validation first |
| ComponentContextPVO returns zero rows | Continue only when no context-specific field is required; otherwise stop as a source-contract blocker |
| Deduction group or override LOV returns no rows | Stop and show the lookup source and supplied value |
| Deduction group or override LOV returns multiple candidate rows | Stop, show business labels/meanings, and ask the user to select one; keep codes and identifiers internal |
| Requested override is not in the selected card metadata | Stop and show the active card/component schema |
| Override dataSource cannot be parsed | Stop and preserve the redacted metadata needed for resolver support |
| Dependent LOV parent value is missing or invalid | Stop and ask for the parent field value before resolving the child |
| Override dependency graph is cyclic or references an unknown parent | Stop and classify as source contract blocker |
| CSV or FSM contract is missing | Stop before preview and request the approved task-specific contract |
| HDL action, target-template section, user key, or value mapping is TBD | Stop before DAT preview or loader handoff |
| Live execution fails | Preserve status, diagnostics, rejected rows, and external IDs when available |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required operation, owner, card, or artifact is missing | Ask for corrected input |
| Catalog mismatch | Task code or task name does not match the nested skill | Stop and use the selected task skill |
| Approval blocker | Live HDL upload or load is requested without exact DAT preview approval | Show the immutable DAT preview and require the `core.data-loader` approval gate |
| Source contract blocker | Endpoint, payload, lookup, or CSV contract is missing | Request source evidence |
| Scope mismatch | Runtime card, component, or owner does not match sourceType=TRU and selected sourceId | Stop and correct target context |
| Lookup ambiguity | payGenericRestQuery or payrollGenericLOV returns zero or multiple required candidates | Return candidate context and ask for a unique value |
| Legal reporting availability ambiguity | `hcmLegalReportingUnits` `findByAdvancedSearchQuery` returns multiple candidates and downstream TRU or card work was requested | Return the names-only list and wait for the user's choice; do not classify a list-only result as an ambiguity error |
| Legislative Data Group availability ambiguity | Direct LDG name or territory search returns multiple candidates and downstream card work was requested | Return the complete names-only list and wait for the user's choice; do not classify a list-only result as an ambiguity error |
| Dynamic schema blocker | getCardDetails override metadata does not support the requested field or resolver | Stop and use the active card schema |
| Component selection ambiguity | The read-only flexfield value request matches zero or multiple component instances | Show component business names, effective intervals, and current-value context and ask for a functional selection before returning values; keep sequence internal |
| Dependent LOV blocker | Parent values required by a child LOV are missing, invalid, cyclic, or not source-backed | Resolve parent values first or request source evidence |
| Fusion API | A read-only retrieval or approved loader operation returns an error | Preserve redacted diagnostics and stop before retry |

## Combined Discovery Failures

| Failure | Classification | Required Response |
|---|---|---|
| TRU association paging stops before completion | Fusion API/source-contract failure | Stop; report that the combined mapping is incomplete and do not render partial associations |
| OrgTaxReportingUnitPVO legislation finder requests LegalEntityId or returns zero rows with that invalid display schema | Input/source-contract failure | Rebuild the finder with `DisplayAttributes=PsuId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId`; do not treat the zero-row result as proof that no TRUs exist |
| TRU association row lacks Name, OrganizationId, or LdgId | Fusion API/source-contract failure | Stop and preserve redacted row diagnostics |
| TRU association LdgId is not in the retrieved territory LDG set | Fusion API/source-contract failure | Report the orphan association; do not infer an LDG or silently discard the TRU |
| TRU association PsuId does not match a retrieved same-LDG PSU OrganizationId | Fusion API/source-contract failure | Report the parent-PSU mismatch; do not associate the TRU by name |
| Multiple LDGs are returned | Expected combined-discovery result | Render every LDG with `PSUs:` and `TRUs:` groups; request selection only after the complete mapping when downstream card work was also requested |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Task identity, target tax reporting unit, business card/component path, complete existence evidence, existing-data disclosure and confirmed Update/Correction choices, exact HDL rows, and unresolved fields |
| Live approval | Exact DAT or immutable ZIP, HDL action, effective date, target card/component, row count, loader target, and rollback or retry limits |
| Failure | Failure class, status, external IDs, rejected rows, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing source contract | Do not infer endpoint, payload, lookup, or defaulting behavior |
| Ambiguous tax reporting unit | Do not choose one target owner |
| Direct REST business mutation | Never call a calculation-card REST create, update, correction, end-date, delete, or association endpoint, even after approval |
| Unapproved HDL load | Do not write, package, upload, or load a DAT/ZIP without the required approval gate |
| Non-TRU target | Do not reuse the Legal Reporting Unit parity contract |
| Unresolved dependent LOV | Do not guess child LOV candidates or values |
| Secret or customer-sensitive payload is supplied | Do not persist sensitive examples in resource files |
| Environment-specific advanced-search capture | Do not persist the captured host, `rv:` identifier, establishment IDs, registration numbers, or reporting-unit names; use placeholders or synthetic examples |
| Functional user lacks technical identifiers | Do not request `dirCardId`, component/definition IDs, override-group IDs, source/LDG IDs, or assignment/association IDs; resolve them internally |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUC.DONE_BLOCKED | terminal | 7 | terminal | none | none | stop | Input, lookup, source-contract, or approval blocker |
