# Document Types Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| DOCT-01 | The Document Type or Delivery Preference REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| DOCT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| DOCT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| DOCT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| DOCT-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| DOCT-03 | Create finds an exact existing Document Type | Input validation | Stop the duplicate create |
| DOCT-04 | The Core Data Loader contract does not support the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting browser, FSM, CSV, or another write route |
| DOCT-05 | A mutation has no reviewed XLSX source | Artifact persistence | Generate the live DocumentType workbook through Core Data Loader and stop if it cannot validate. |
| DOCT-06 | Source keys are partial, copied, caller-solicited, or lack deterministic supported provenance | Input validation | Stop; never ask the user for technical keys. Generate and collision-check a complete child pair only for a Data Loader create that requires it. |
| DOCT-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| DOCT-08 | Delivery Preferences returns JBO-27008 because PsuId or LevelCode cannot be set | Fusion API | Reject the complete row; remove attributes only when current loader metadata proves they are non-settable, then revalidate, re-preview, and reapprove |
| DOCT-08A | Data Loader requires a hierarchy code for the default document delivery preference | Fusion API | Re-read the exact parent, preserve its current nonblank HierarchyCode on the root DocumentType row, rebuild the source, revalidate, re-preview, and reapprove |
| DOCT-08B | Data Loader rejects a Delivery Preferences LegislationCode after a territory code was placed in the Country attribute | Fusion API | Resolve the country through HCM Countries LOV, use CountryName for Country or TerritoryCode for LegislationCode according to the exact live heading, then rebuild, revalidate, re-preview, and reapprove |
| DOCT-08C | Data Loader rejects PsuId or PayrollStatutoryUnitName because the wrong identity form was used for the preference level | Fusion API | For a Data Loader `Payroll Statutory Unit` anchor, preserve the exact canonical LOV name and leave PsuId blank; for Data Loader Department/Location, use numeric PsuId and leave the name blank. Rebuild, revalidate, re-preview, and reapprove. |
| DOCT-08D | A Department or Location preference exists without its PAYROLL PSU or GENERAL Legal Employer physical anchor | Input validation | Reconcile current rows and use the declared Data Loader contract to author the missing anchor. Stop if the metadata cannot represent it. Re-preview and reapprove. |
| DOCT-08E | A missing organization anchor user-key-only MERGE routes to DocumentDeliveryDefaultPreferenceLogical and derives a non-settable PsuId or LempId | Fusion API | Stop that identity form. Reconcile physical state and stop unless current Data Loader metadata provides a different declared supported key. Never replay the user-key form. |
| DOCT-08F | A PAYROLL PSU anchor source-key create is rejected because the exact user key belongs to a record with a different source key | Fusion API | Stop all Data Loader retries for that anchor. Re-read the physical children, preserve diagnostics, and stop for correction; do not substitute a REST mutation. |
| DOCT-08I | A Location preference is reported missing because the child response has null LocationId even though its returned level code, organization ID, LevelId, and LocationName match | Input validation | Do not create a duplicate. Reconcile the row by current returned LevelCode plus organization ID and LevelId equal to the resolved Location ID, then classify its modes from the fresh row. |
| DOCT-08J | A mode-only edit would overwrite an unrequested Online or Paper value or resubmit an unchanged anchor | Input validation | Re-read the exact child, use its fresh DocumentDeliveryPreferenceId, preserve the unrequested mode, author only the changed child, then revalidate and re-preview. |
| DOCT-08K | A Document Type create without requested Delivery Preferences requires, defaults, or emits HierarchyCode, or declares a header-only DeliveryPreference component | Artifact persistence | Remove the intake requirement and omit both the unpopulated DeliveryPreference section and unused HierarchyCode column from the DAT. Do not request, enable, or invent `GENERAL` or `PAYROLL`; rebuild, revalidate, re-preview, and reapprove. |
| DOCT-09 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| DOCT-09A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected document types |
| DOCT-09B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| DOCT-09C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| DOCT-10 | A new `DocumentTypeAttachment` MERGE for an existing parent fails because it lacks values defining a unique reference | Catalog mismatch | Stop the Data Loader route. If the live REST child describe contract advertises POST create, attachment-typed `FileContents`, and generated `AttachedDocumentId`, rebuild as an immutable REST attachment preview and obtain standalone approval; otherwise stop. |
| DOCT-10A | The approved REST attachment preview no longer matches the parent, file bytes, payload, contract, or current child names | Approval blocker | Stop before POST, rebuild the preview from fresh evidence, and obtain new standalone approval. |
| DOCT-10B | The approved attachment POST fails or its outcome cannot be verified | Fusion API | Preserve sanitized diagnostics, do not retry, and reconcile through a fresh bounded attachment read. |
| DOCT-11 | HDL rejects a Document Type create without Delivery Preferences because it requires a hierarchy for its generated default preference | Catalog mismatch | Do not ask for or invent a hierarchy and do not retry HDL. Rebuild through the declared REST parent-create adapter only when live metadata marks HierarchyCode optional, then obtain standalone approval. |
| DOCT-11A | The REST parent create succeeds but attachment creation or verification fails | Fusion API | Persist the parent-created partial result, stop without retrying or deleting it, and reconcile both parent and child before any new action. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, or source key is invalid or ambiguous | Correct the input and restart from validation |
| Catalog mismatch | The registered loader object or current metadata does not support the mutation | Refresh the contract and rebuild the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects a complete Delivery Preferences row | Correct the row only from current loader metadata |
| Artifact persistence | The reviewed XLSX or derived immutable artifact is unavailable | Rebuild and preserve the complete source artifact |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| JBO-27008 | Rejected row identity, non-settable attributes confirmed by current metadata, and required source correction |
| Missing parent hierarchy | Rejected row identity, confirmation that the exact parent was re-read, and the required root-row preservation correction |
| Country representation mismatch | Rejected row identity, the exact live loader heading, and the resolved CountryName/TerritoryCode pair used for correction |
| PSU identity mismatch | Rejected row identity, confirmation that the canonical LOV name contained surrounding whitespace, and confirmation that the current OrganizationId will be used without disclosing it in user-facing output |
| Missing hierarchy anchor | Parent hierarchy, expected organization anchor level, requested lower level, which row already exists, and which missing row will be loaded |
| Anchor logical-view routing failure | Rejected anchor level, preserved diagnostic, current physical-row absence, current route eligibility, and the next exact preview without exposing resolved internal IDs outside the approval preview |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Document Type or Delivery Preference rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A declared mutation route is unavailable | Do not substitute a browser, FSM import, CSV import, or an undeclared generic REST write. The only REST write exception here is the declared existing-parent attachment child-create adapter. |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| PsuId or LevelCode is rejected | Do not remove either attribute unless current loader metadata confirms it is non-settable |
| A parent HierarchyCode is missing | Do not invent or hard-code it; obtain it from a fresh exact parent item read |
| A plain Document Type create has no Delivery Preferences | Do not ask for, require, infer, or default `HierarchyCode`; use the declared REST parent-create route with the attribute omitted. |
| A Delivery Preferences country fails validation | Do not swap names and codes by guesswork; resolve both values and map them from the exact live loader heading |
| A Delivery Preferences PsuId fails validation | Do not reuse one identity form: Data Loader uses canonical name on the organization anchor and numeric ID only on lower-level rows. Require a new preview and approval. |
| A lower-level preference already exists | Do not submit it again solely to make the source contain two rows; load only the missing anchor or explicitly changed row after reconciliation |
| An anchor user-key MERGE reaches a non-settable organization ID | Do not retry the user-key representation. Stop unless current Data Loader metadata provides a different supported key. |
| A lower PAYROLL row already proves an implicit hierarchy but the physical PSU anchor is absent | Reconcile the hierarchy and use only a supported Core Data Loader source; otherwise stop. |
| A key or target is unresolved | Do not infer or invent a value |
| A new existing-parent attachment has only system-generated `AttachedDocumentId` as its HDL unique key | Do not ask the user for the ID, reuse another record's ID, or retry a parent-ID-only child MERGE. Use only the declared REST child-create adapter after live contract validation and approval. |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOCT.ROUTE | decision | 6 | execution_gate | read->DOCT.DONE;loader_ready->DOCT.LOADER_READY;rest_create_ready->DOCT.REST_CREATE_READY;attachment_rest_ready->DOCT.ATTACHMENT_REST_READY;mutation_blocked->DOCT.ERROR | DOCT.ENFORCE | stop | Select read completion, Core Data Loader, hierarchy-free REST create, or existing-parent attachment REST create |
| DOCT.ERROR | step | 7 | error_handler | stopped->DOCT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| DOCT.DONE | terminal | 8 | terminal | none | DOCT.ROUTE | continue | Read completed |
| DOCT.LOADER_READY | terminal | 9 | terminal | none | DOCT.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| DOCT.ATTACHMENT_REST_READY | terminal | 10 | terminal | none | DOCT.ROUTE | continue | Existing-parent attachment checks passed; build the immutable REST preview and wait for standalone approval |
| DOCT.REST_CREATE_READY | terminal | 11 | terminal | none | DOCT.ROUTE | continue | Hierarchy-free create checks passed; build the immutable REST create preview and wait for standalone approval |
| DOCT.BLOCKED | terminal | 12 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
