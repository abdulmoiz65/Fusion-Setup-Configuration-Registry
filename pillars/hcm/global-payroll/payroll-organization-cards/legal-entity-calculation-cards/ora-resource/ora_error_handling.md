# Legal Entity Calculation Cards Error Handling

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
| Payroll statutory unit cannot be resolved | Stop and ask for a unique target owner |
| FS_SCOPEINFOS is missing or malformed | Stop and ask for a redacted launch URL or extracted scope values |
| Legal entity search text is empty or contains only `%` wildcards | Stop and ask for a meaningful name or identifier fragment; do not execute an unbounded availability search |
| Legal entity availability payload omits `filters`, uses an empty filter array, or does not contain `PsuFlag=Y` | Stop before the POST and rebuild the request with the mandatory PSU eligibility filter |
| Legal entity availability returns zero rows | Report that no legal entity matched and ask the user to refine the search; do not classify this read-only result as a Fusion failure |
| Legal entity availability returns multiple rows | Return only the candidate names, one per line, and complete a list-only request. Wait for an explicit selection only when downstream PSU or card work was also requested |
| Legal entity availability response lacks `result.summary`, `result.items`, `Name`, or `LegalEntityId` | Classify as a Fusion API/source-contract failure and preserve redacted response diagnostics |
| Legislative Data Group name search is empty or contains only `%` wildcards | Stop and ask for a meaningful full or partial LDG name unless the request is a supported territory search with a nonblank restrictive filter |
| Legislative Data Group request has an empty query and no nonblank restrictive filter | Stop before POST; do not execute an unbounded search |
| US territory response contains `TerritoryShortName` other than `United States` | Classify as a response-contract failure and do not return or use the mismatched row |
| Legislative Data Group availability returns zero rows | Report that no Legislative Data Group matched and invite the user to refine the search; do not classify this read-only result as a Fusion failure |
| Legislative Data Group availability returns multiple rows | Return every candidate name, one per line, and complete a list-only request. Wait for selection only when downstream card work was also requested |
| Legislative Data Group availability response lacks `result.summary`, `result.items`, `Name`, or `LegislativeDataGroupId` | Classify as a Fusion API/source-contract failure and preserve redacted response diagnostics |
| Legislative Data Group availability paging fails before `hasMore=false` | Stop with a partial-results diagnostic; do not present the partial list as complete |
| Legal entity availability response contains a row whose `PsuFlag` is not `Y` | Classify as a Fusion API/source-contract failure, preserve redacted diagnostics, and do not return or use that row |
| Advanced-search POST returns HTTP 400 saying the operation is unsupported for the invoked method | Retrieve `/hcmRestApi/resources/11.13.18.05/hcmLegalEntities/describe`, confirm POST and the Oracle action media types, correct the versioned path or headers, and make at most one corrected attempt because this action is a read-only idempotent search |
| Browser-routed `rv:` URL is stale, `rv:null`, or belongs to another environment | Stop using the routed form and use the versioned standard resource path against `restBaseUrl`; never reuse or guess a route token |
| Guessed browser-routed URL returns HTTP 500 | Do not retry the same routed POST; use the live-described versioned standard path and Oracle action media types |
| OrgPayrollStatutoryUnitPVO returns no row for the internally resolved legal-entity key | Repeat owner resolution by PSU/legal-entity business name; ask for corrected business context only if no unique owner can be resolved |
| OrgPayrollStatutoryUnitPVO returns multiple rows for the internally resolved legal-entity key | Show PSU/legal-entity business names and LDG names for selection; keep source and LDG IDs internal |
| OrgPayrollStatutoryUnitPVO returns no row for pLegislationCode | Report that no payroll statutory unit matched the supplied legislation code and ask for a valid code |
| OrgPayrollStatutoryUnitPVO returns multiple rows for pLegislationCode | Return only the candidate names, one per line, and complete a list-only request. Wait for an explicit selection only when downstream PSU or card work was also requested |
| OrgPayrollStatutoryUnitPVO legislation-code row is missing LegalEntityId, Name, OrganizationId, or LdgId | Classify as a Fusion API/source-contract failure and do not return or use the malformed row for downstream work |
| OrgPayrollStatutoryUnitPVO returns no row for pLegislationCode and pLdgId | Report that no payroll statutory unit matched the supplied legislation and LDG |
| OrgPayrollStatutoryUnitPVO returns a row whose LdgId differs from pLdgId | Classify as a Fusion API/source-contract failure and do not return or use the mismatched row |
| Calculation card cannot be resolved | Stop and ask for a unique card reference or approved card-list lookup |
| Owner-scoped getCardDetails existing-card discovery fails or returns incomplete scope | Classify as a Fusion API/source-contract failure; do not treat the failure as proof that the card doesn't exist and do not switch to mode=ADD |
| Owner-scoped existing-card discovery returns multiple exact card matches | Show business names and effective intervals and request a business selection; retain CardSequence and IDs internally |
| Existing card lacks original EffectiveStartDate, current EffectiveEndDate, or CardSequence | Stop the DAT preview with an HDL parent-key diagnostic; do not expose a placeholder or apply new-card defaults |
| Exact drilldown returns no card for the internally resolved dirCardId and date | Repeat owner-scoped business-name/history discovery; ask for corrected business context only if resolution remains impossible |
| getCardDetails mode=ADD returns no available cards | Stop and ask for a valid source owner, effective date, or card selection |
| getCardDetails returns a card outside sourceType=PSU or the selected sourceId | Stop and report a scope mismatch |
| Component-specific operation has no component rows | Stop and ask for a valid component selection |
| Existing component matches but lacks original EffectiveStartDate, current EffectiveEndDate, or ComponentSequence | Stop the DAT preview with an HDL component-key diagnostic; do not create a duplicate component or apply new-component defaults |
| Component flexfield value lookup matches no component or multiple components | Stop and show component business names/effective intervals for selection; keep component sequence and IDs internal |
| Selected component has no FLEX override rows | Complete the read-only request successfully with `Flexfield values:` followed by `None` |
| Stored LOV value has no unique display meaning | Return the stored value for the read-only list and do not guess; if a later write is requested, require unique LOV validation first |
| ComponentContextPVO returns zero rows | Continue only when no context-specific field is required; otherwise stop as a source-contract blocker |
| Deduction group or override LOV returns no rows | Stop and show the lookup source and supplied value |
| Deduction group or override LOV returns multiple candidate rows | Stop, show business labels/meanings, and ask the user to select one; keep codes and identifiers internal |
| Requested override is not in the selected card metadata | Stop and show the active card/component schema |
| Requested override has blank or unsupported overrideType | Stop before HDL mapping and report the returned type; do not force the field into ComponentDetail |
| overrideType=OVERRIDE is removed by a FLEX-only filter | Treat as an HDL mapping defect and rebuild the child plan as CalculationValueDefinition plus EnterableCalculationValue |
| HDL component name comes from source, UI, base display, or generic documentation without exact target proof | Stop and resolve an existing target HDL/exported key or the exact unique target `CIRComponentPVO.ComponentName`; corroborate it with the selected target `getCardDetails` row |
| Enterable-value display text does not resolve uniquely to a stored code | Stop and run the metadata-declared LOV or request authoritative component guidance; do not guess Value1 |
| Yes/No value domain is not proven as Y/N | Stop before normalizing the value; use Y/N only when active metadata or component guidance proves it |
| Override dataSource cannot be parsed | Stop and preserve the redacted metadata needed for resolver support |
| Dependent LOV parent value is missing or invalid | Stop and ask for the parent field value before resolving the child |
| Override dependency graph is cyclic or references an unknown parent | Stop and classify as source contract blocker |
| CSV or FSM contract is missing | Stop before preview and request the approved task-specific contract |
| `fusionEnv.properties` target is missing or conflicts with an assumed environment | Stop and require the properties file to identify the active target; never silently reuse the source pod |
| Target card already has the intended component | Notify the user, show the existing interval, reuse keys internally, and ask for Update or Correction; do not auto-update or duplicate it |
| Live `CalculationCard` template does not contain a planned child section or key | Stop the DAT preview and report the exact missing ComponentDetail/FLEX or CalculationValueDefinition/EnterableCalculationValue item |
| Source instance or definition ID appears in target DAT | Remove it and resolve target linkage by validated names and sequences; block when that is not unique |
| Import succeeds but load reports an invalid `DirCardCompDefId` and shows the submitted component/card names | Classify it as an HDL component-key blocker. The archive parsed and staged, but the target could not resolve that logical user-key pair. Re-run the target component-name resolver, update the parent and every applicable child, generate a new immutable ZIP, and require retry approval; do not add a numeric ID or retry the same archive |
| ComponentDetail reports an invalid parent reference | Compare every parent user-key value and correct `ComponentDetail.DirCardCompDefName` to the exact parent `CardComponent.DirCardCompDefName`; do not use the Flex-context display name |
| Completed DAT preview still contains an original-date, sequence, component-name, value-definition, or stored-value placeholder | Stop and identify the owning resolver. Do not present the preview as ready and do not ask the user to supply values that the exact target lookup owns |
| DAT preview is not approved | Keep the content in chat only; do not create a file, ZIP it, upload it, or initiate a load |
| HDL action, target-template section, user key, or value mapping is TBD | Stop before DAT preview or loader handoff |
| Live execution fails | Preserve status, diagnostics, rejected rows, and external IDs when available |

## HDL Component-Key Training Case

| Learning | Evidence Pattern | Reusable Rule |
|---|---|---|
| Import success is not load success | The archive is accepted and imported, then the business-object load rejects a row | Import validates and stages the package. Load performs target business-key resolution and can still fail |
| The error names an ID but the supplied logical key is the defect | The message says `DirCardCompDefId` is invalid and reports the submitted component name plus card definition name | Diagnose the component/card name pair first. Resolve the exact target `DirCardCompDefName`; do not add a numeric definition ID to the DAT |
| Target metadata outranks a generic example | A generic guide uses `Federal Income Tax`, while the exact target `CIRComponentPVO` row for `BaseComponentName=US_ORG_FEDERAL_INCOME_TAX` returns `ComponentName=Federal Taxes` | Use `Federal Taxes` for that target. Generic guidance can confirm row structure or field labels but cannot replace a different target-supported key |
| Parent and child keys form one contract | `CardComponent` and one or more child rows carry the component definition name | Propagate the exact same `DirCardCompDefName` to every applicable `ComponentDetail`, `CalculationValueDefinition`, and `EnterableCalculationValue` row |
| Component and override names are independent | The component resolves as `Federal Taxes`, while the live override title is `Enforce Federal Income Tax Look-back Rule` | Preserve each object’s own target key. Do not rename the value definition merely because the parent component name changed |
| The corrected DAT succeeds because the user key resolves | The corrected component/card pair matches target metadata and all child rows use the same component name | The loader can resolve the target component definition and attach the override records to the intended parent |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required operation, owner, card, or artifact is missing | Ask for corrected input |
| Catalog mismatch | Task code or task name does not match the nested skill | Stop and use the selected task skill |
| Approval blocker | Live HDL upload or load is requested without exact DAT preview approval | Show the immutable DAT preview and require the `core.data-loader` approval gate |
| Source contract blocker | Endpoint, payload, lookup, or CSV contract is missing | Request source evidence |
| Launch context blocker | FS_SCOPEINFOS does not include the required Legal Entity Calculation Cards scope shape | Request corrected launch context |
| Scope mismatch | Runtime card, component, or owner does not match sourceType=PSU and selected sourceId | Stop and correct target context |
| Lookup ambiguity | payGenericRestQuery or payrollGenericLOV returns zero or multiple required candidates | Return candidate context and ask for a unique value |
| Legal entity availability ambiguity | `findByAdvancedSearchQuery` returns multiple candidates and downstream PSU or card work was requested | Return the names-only list and wait for the user's choice; do not classify a list-only result as an ambiguity error |
| Legislative Data Group availability ambiguity | Direct LDG name or territory search returns multiple candidates and downstream card work was requested | Return the complete names-only list and wait for the user's choice; do not classify a list-only result as an ambiguity error |
| Dynamic schema blocker | getCardDetails override metadata does not support the requested field or resolver | Stop and use the active card schema |
| HDL parent-key blocker | Existing card or component dates/sequences are absent, incomplete, or ambiguous | Repeat the exact target lookup or return the unresolved resolver; never apply creation defaults to existing rows |
| HDL record-type blocker | overrideType is absent/unsupported or mapped to the wrong CalculationCard child discriminator | Rebuild the child plan from the active override metadata |
| HDL value-definition blocker | ValueDefinitionName, Value1, stored-code mapping, or effective interval is unresolved | Resolve the enterable-value contract before preview |
| HDL component-key blocker | The submitted `DirCardCompDefName` and card definition do not resolve to one target component, including a load-time invalid-`DirCardCompDefId` diagnostic | Resolve the existing target export or exact unique target `CIRComponentPVO.ComponentName`, propagate it to all applicable rows, rebuild the ZIP, and obtain retry approval |
| Component selection ambiguity | The read-only flexfield value request matches zero or multiple component instances | Show component business names, effective intervals, and current-value context and ask for a functional selection before returning values; keep sequence internal |
| HDL schema blocker | Live target `CalculationCard` template does not expose the required section or context-qualified attribute | Stop before creating an artifact |
| Duplicate component blocker | A create plan targets a component instance already returned by getCardDetails | Stop the create plan, disclose the existing interval, and ask for Update or Correction; never auto-select the action |
| Parent reference blocker | ComponentDetail parent keys do not resolve the existing or same-file CardComponent | Correct the child linkage before generating or loading the DAT |
| Dependent LOV blocker | Parent values required by a child LOV are missing, invalid, cyclic, or not source-backed | Resolve parent values first or request source evidence |
| Fusion API | A read-only retrieval or approved loader operation returns an error | Preserve redacted diagnostics and stop before retry |

## Combined Discovery Failures

| Failure | Classification | Required Response |
|---|---|---|
| PSU association paging stops before completion | Fusion API/source-contract failure | Stop; report that the combined mapping is incomplete and do not render partial associations |
| PSU association row lacks Name, OrganizationId, or LdgId | Fusion API/source-contract failure | Stop and preserve redacted row diagnostics |
| PSU association LdgId is not in the retrieved territory LDG set | Fusion API/source-contract failure | Report the orphan association; do not infer an LDG or silently discard the PSU |
| Multiple LDGs are returned | Expected combined-discovery result | Render every LDG with `PSUs:` and `TRUs:` groups; request selection only after the complete mapping when downstream card work was also requested |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Task identity, redacted launch scope when supplied, target payroll statutory unit, card reference, component reference, read-only lookup evidence, LOV resolutions, exact HDL rows, unresolved fields, and planned HDL action |
| HDL preview readiness | Complete per-object existence classification; existing-data disclosure and confirmed Update/Correction choices; resolved internal technical keys and HDL parent keys; exact fields/values and live-template validation |
| Live approval | Exact DAT or immutable ZIP, HDL action, effective date, target card/component, row count, loader target, and rollback or retry limits |
| Failure | Failure class, status, external IDs, rejected rows, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing source contract | Do not infer endpoint, payload, lookup, or defaulting behavior |
| Environment-specific launch values | Do not persist concrete host, legal entity ID, legal entity name, or user/session values in packaged resources |
| Ambiguous payroll statutory unit | Do not choose one target owner |
| Direct REST business mutation | Never call a calculation-card REST create, update, correction, end-date, delete, or association endpoint, even after approval |
| Unapproved HDL load | Do not write, package, upload, or load a DAT/ZIP without the required approval gate |
| Unapproved artifact generation | Do not write a DAT or ZIP before approval of the exact in-chat DAT preview |
| Source/target confusion | Do not use a source environment URL as the target; resolve the target from `core/auth/fusionEnv.properties` |
| Source identifiers | Do not persist or import source card, component, definition, Flex, owner, or LDG IDs |
| Functional user lacks technical identifiers | Do not request `dirCardId`, component/definition IDs, override-group IDs, source/LDG IDs, or assignment/association IDs; resolve them internally |
| Unresolved HDL keys | Do not emit original-date or sequence placeholders as a completed preview and do not ask the user to provide target values owned by read-only metadata |
| Wrong HDL child type | Do not discard OVERRIDE rows with a FLEX filter and do not map all requested values to ComponentDetail |
| Non-PSU or Legal Reporting Unit target | Do not reuse the Legal Entity HAR contract |
| Unresolved dependent LOV | Do not guess child LOV candidates or values |
| Secret or customer-sensitive payload is supplied | Do not persist sensitive examples in resource files |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LEC.DONE_BLOCKED | terminal | 7 | terminal | none | none | stop | Input, lookup, source-contract, or approval blocker |
