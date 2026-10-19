# Calculation Value Definitions Error Handling

## Registered-BO Evidence and Refusal

Registered-BO child writes are unavailable for objects without a released native
HDL business-object contract. The stable historical evidence reference is
`CVD-RBO03–CVD-RBO16`; it is non-authorizing and does not open an execution
path.

For every new registered-BO child request, return `CVD_HDL_ROUTE_FROZEN`
before candidate authoring, approval, or dispatch. Do not retry, replay, or use
a product REST write as a fallback. Preserve a sanitized terminal outcome for
read-only reconciliation and classify an unknown or incomplete outcome without
submitting a replacement. Reconsideration requires new authoritative proof of a
supported contract.

## Error Situations

Rows that describe product REST write responses apply only to historical
receipt interpretation and read-only reconciliation. They are not dispatch or
fallback routes under CVD-HDL01. The exact CVD-HDL04 native parent create,
CVD-HDL10 combined parent-plus-Range-Item create, supported CVD-HDL05 native
Range Item create, CVD-HDL11 Range Item Override Create, CVD-HDL07A
currency-only Parent Correct, CVD-HDL07B currency-only new-slice Parent Update, and CVD-HDL07C
  childless single-slice Parent Delete, CVD-HDL09A Range Item Correct,
  CVD-HDL09B Range Item Update, and restricted CVD-HDL09D Range Item Delete are
  the normal executable mutation exceptions. The registered-BO evidence reference is
terminal historical evidence and provides no execution authority; registered-BO child
creation and Override Usage remain nonexecutable.

| Situation | What Should Happen |
|---|---|
| A required operation, scope, input, or effective date is missing or invalid | Classify as INPUT_VALIDATION, return every affected field, and stop before lookup or preview. |
| A collecting response requests or exposes a Fusion surrogate ID, or stops without asking the next missing business question | Classify as INPUT_VALIDATION, discard the user-visible ID rendering, retain only valid operation-local state, and continue from the input-kind and continuation rules in ora_input_validation.md. Do not prepare a preview or ask for approval. |
| A lookup returns no exact match | Classify as NOT_FOUND, show the field and sanitized supplied value, and leave the reference unresolved. |
| A lookup returns multiple exact matches | Classify as AMBIGUOUS, show concise distinguishing fields, and require user selection. |
| A Generic LOV returns an empty calculation-type list for a valid LDG | Classify as CATALOG_MISMATCH or TRANSPORT_ENVIRONMENT based on the confirmed response; do not enable parent create. |
| CalculationTypeVO repeats CalculationTypeId in Code and a CVD-HDL04 parent selection is absent from the packaged semantic map | Keep the exact live selection valid and run resolve_parent_payload_shape. If current evidence cannot establish its semantics and complete field/read-back contract, return PAYLOAD_SHAPE_UNRESOLVED and remain before DAT authoring; do not classify the label as CATALOG_MISMATCH. A conflicting live ID/name row is still CATALOG_MISMATCH. |
| A CVD-HDL04 Calculation Type and applicable Unit resolve successfully, including a customer-defined label or non-Money unit | Permit the business selection and require a complete parentPayloadShape. Author only its fixed plus proved conditional fields. If the shape, resolver lineage, live template, or any read-back mapping is incomplete, return PAYLOAD_SHAPE_UNRESOLVED without guessing or calling the LOV value invalid. |
| CalculationTypeVO and OverrideTypeLOVVO cannot produce an exact short-code-to-ID intersection | Classify the explicit calculation-type override on a regular RangeItem as UNSUPPORTED; keep CalculationTypeId omitted. This is not the independent-root CVD-HDL11 RangeItemOverride profile. |
| A product REST POST, PATCH, PUT, or DELETE is proposed | Classify as UNSUPPORTED and stop. Product REST is GET-only; do not construct the request or use it as fallback. |
| An Allowed Override or Override Usage create is requested | Classify as CVD_HDL_ROUTE_FROZEN. Registered-BO child creation is unavailable; do not prepare a candidate, replay the registered-BO evidence reference, or fall back to product REST. |
| A catalog-supported setup-task CSV import is requested | Exit this native-HDL task-hook contract and route through the existing `SKILL.md` CSV workflow and `core.data-loader`. Do not classify the request as unsupported, convert CSV to DAT, or dispatch it from this route. |
| A Value Definition Group create is requested | Classify as CVD_HDL_ROUTE_FROZEN. This task has no released native HDL group-create profile; perform zero archive authoring, approval, or write. |
| A parent create is requested outside standalone CVD-HDL04 or fixed CVD-HDL10, or an unsupported parent/child lifecycle mutation is requested | Classify as CVD_HDL_ROUTE_FROZEN and stop before archive authoring or approval. A CVD-HDL04 shape that is eligible but not yet provable is PAYLOAD_SHAPE_UNRESOLVED, not an unsupported business value. Historical REST or registered-BO evidence is not native HDL proof. |
| A Range Item create is requested | Permit the CVD-HDL05 one-child supported profile. Require an exact proved parent with zero Range Items, no matching lower bound, current native template validation, immutable archive validation, and Task Hook validation before approval. |
| A Range Item Override create is requested | Permit only CVD-HDL11: one independent-root RangeItemOverride MERGE against one exact nonproduction open-ended parent whose type and applicable unit resolve exactly in the current tenant, including customer-defined type labels and non-Money units. Require a resolved result-slot shape, exactly one baseline Range Item, zero other child families, no matching lower bound, no type-comparable overlap, current root template validation, immutable archive and Task Hook validation, and standalone hash-bound approval before dispatch. |
| A combined parent and Range Item create is requested | Permit only CVD-HDL10: one new Flat Amount/Money parent and one same-start Range Item in one archive. Require complete label resolution, zero parent duplicates, both live template sections, matching archive and Task Hook hashes, standalone approval, terminal loader success, and one expanded-parent read proving the exact parent, exact child, and zero other children. |
| A CVD-HDL10 result has a duplicate, changed archive, failed loader, mismatched Range Item, extra child, or non-expanded read-back | Stop before dispatch when possible; otherwise classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the receipt, and never replay the write automatically. |
| A CVD-HDL04 terminal load cannot be matched through the operation-bound parentReadbackMappings, including any authored CurrencyCode, Uom, DateMode, Periodicity, DatabaseItemName, or ValueIdentifier | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the exact request, archive hash, loader receipt, and read-back, and never replay the write automatically. |
| Another unsupported child create or any Range Item Override lifecycle action beyond CVD-HDL11 Create is requested | Classify as CVD_HDL_ROUTE_FROZEN and stop before archive authoring or approval. |
| A CVD-HDL05 load succeeds but expanded read-back omits the Range Item, changes its bounds, or does not map Value1 to RangeValueA | Classify as CONTRACT_INCOMPLETE, preserve the request, and do not replay it. |
| A CVD-HDL11 exact type or applicable unit is absent or ambiguous in its current tenant LOV | Classify as NOT_FOUND or AMBIGUOUS and remain in preflight; do not replace it with Flat Amount or Money. A packaged-map omission alone is not an error. |
| A CVD-HDL11 exact type/unit resolves but its required result-slot signature cannot be established from current semantic metadata and the required baseline row | Classify the payload as INPUT_VALIDATION or dependency-blocked and remain in collecting/preflight. Do not call the LOV value invalid and do not author a guessed field set. |
| A CVD-HDL11 request finds a matching lower bound or a type-comparable interval overlap | Classify as CONFLICT and stop before archive authoring or dispatch. Select a nonoverlapping interval or reconcile the existing row; do not retry automatically. |
| A CVD-HDL11 archive, parent baseline, or target fingerprint changes after approval | Classify as STALE_PLAN, invalidate approval, and do not dispatch. Rebuild from fresh read-only evidence and require a new archive hash and approval. |
| A CVD-HDL11 load is terminal but loader detail and complete expanded-parent read-back do not jointly prove one loaded/zero failed row, Range Item count 1 -> 2, the unchanged baseline, and exactly one requested open-ended row with every authored Value1/Value2/Value3 mapped type-aware to RangeValueA/RangeValueB/RangeValueC and every additional authored result field matched through its predeclared readable response attribute | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the request and receipt, and never replay the write automatically. |
| Parent Correct is requested | Permit only CVD-HDL07A: one explicitly selected, nonproduction, childless, open-ended Flat Amount/Money parent and one different Currency selected from the current LOV. Reject every other changed field or target shape as CVD_HDL_ROUTE_FROZEN. |
| A CVD-HDL07A Parent Correct is a no-op, stale, or not target-bound | Classify an equal current/corrected Currency as INPUT_VALIDATION. Classify changed target identity, profile, physical range, child counts, archive SHA-256, or target fingerprint as STALE_PLAN, invalidate approval, and do not dispatch. |
| Parent Update is requested | Permit only CVD-HDL07B: one explicitly selected, nonproduction, childless, open-ended Flat Amount/Money parent with no existing future slice, one explicit later effective boundary, and one different Currency selected from the current LOV. Reject every broader update as CVD_HDL_ROUTE_FROZEN. |
| A CVD-HDL07B Parent Update is a no-op, has an invalid boundary, is stale, or is not target-bound | Classify equal current/new Currency or a boundary not after the current physical start as INPUT_VALIDATION. Classify changed target identity, profile, physical range, future-slice state, child counts, archive SHA-256, target fingerprint, or boundary as STALE_PLAN, invalidate approval, and do not dispatch. |
| Parent Delete is requested | Permit only CVD-HDL07C: one explicitly selected nonproduction parent whose exact expanded read proves zero children and whose complete timeline evidence proves exactly one physical slice. Reject every broader Delete as CVD_HDL_ROUTE_FROZEN. |
| A CVD-HDL07C Parent Delete is stale or not target-bound | Classify changed target identity, physical range, child counts, timeline evidence, archive SHA-256, or target fingerprint as STALE_PLAN, invalidate approval, and do not dispatch. |
| End Date, Parent Delete outside CVD-HDL07C, a child lifecycle mutation outside CVD-HDL09A Range Item Correct, CVD-HDL09B Range Item Update, or restricted CVD-HDL09D Range Item Delete, or a Parent Correct/Update outside its exact released profile is requested | Classify as CVD_HDL_ROUTE_FROZEN and stop before archive authoring or approval. Controlled evidence is not an executable native HDL route until its exact action contract is productized. |
| A CVD-HDL09B Range Item Update is a no-op, has an invalid boundary, is stale, or is not target-bound | Classify equal current/new Flat Amount or a boundary not after the current item start as INPUT_VALIDATION. Classify changed target identity, dates, bounds, amount, archive SHA-256, target fingerprint, or boundary as STALE_PLAN, invalidate approval, and do not dispatch. |
| Native HDL template validation rejects an authored field or control | Classify as INPUT_VALIDATION before dispatch. Rebuild only from the current live template and exact operation allowlist, then create a new archive hash and approval preview. Do not substitute historical REST or registered-BO fields. |
| Data Loader rejects a native parent row because legislative scope is mixed or unresolved | Classify as PROCESS_FAILED, preserve the sanitized receipt, and verify parent absence. Re-resolve the exact LDG and rebuild with LegislativeDataGroupName only; omit LegislativeDataGroupId and LegislationCode. Require a new hash and approval; never replay the failed archive. |
| Data Loader cannot resolve ValueGroupName or CalculationTypeName | Classify as PROCESS_FAILED, preserve the sanitized receipt, verify parent absence, and re-resolve the exact current-operation business selection. Rebuild with the exact business names and no corresponding IDs. Require a new hash and approval. |
| A terminal Data Loader summary shows a total/loaded gap or nonzero aggregate error count, while the Data Loader process log reports zero failed objects and one or more objects requiring external loading | Do not label the external-loading objects or the CVD parent as failed. Report explicit process-log counts for succeeded, failed, warnings, and external loading separately, disclose the aggregate mismatch, and classify the parent only after its detail-object result and exact scoped read-back agree. |
| The CVD parent lifecycle handoff, approved Task Hook envelope, native HDL loader facts, or exact expanded parent GET do not all agree | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN as applicable. Do not report completion and do not replay the archive. Retain the immutable archive SHA-256 and reconcile the existing request/read-back before preparing any replacement. |
| Reconciliation lacks expanded-parent provenance, omits RangeItems, separates parent and Range Items across responses, or uses the direct /child/RangeItems link | Classify as CONTRACT_INCOMPLETE. Run only a fresh collection-level expanded parent GET at the operation effective date. The direct child route returned HTTP 404 and must not be retried or reconstructed. |
| The exact create duplicate check finds an existing parent, or Data Loader reports a duplicate conflict | Classify as CONFLICT; do not retry automatically. Ask for a new unique name or select the existing intended record after exact reconciliation. |
| A new Create command resembles or duplicates a prior run | Allocate a new operation ID and empty collecting state. Do not resume, retry, clone, or import values from the prior run. If the target could collide with a pending, uncertain, or completed operation, perform the required read-only reconciliation before dispatch without seeding the new request from that operation. |
| A read-only lookup receives 401 or an expired-session response | Refresh the configured session once and retry that read only; never expose credentials. |
| The shared setup-data validation context resolves this task but reports fallback_to_oracle_docs_required: true with no guidance files | Check the task-owned ora-resource/ directory directly. When all required CVD guidance files are present and readable, record a nonblocking guidance-discovery mismatch, cite those files, and continue validation without a user waiver. Block only for mismatched task metadata or missing/unreadable required guidance. |
| An approved Data Loader request returns a Request ID | Report initiation, persist the identifier immediately, and begin automatic read-only polling for that same request. Do not require the user to ask for status. |
| A status check reports a nonterminal process | Report the same Request ID and current status. Do not create a replacement process or infer completion. |
| A process-creation response is lost before ProcessId is persisted | Compare the current task-scoped process collection with the persisted pre-dispatch process-ID snapshot. Adopt and poll exactly one new process; record reconciled_not_created when there are none; classify more than one new process as AMBIGUOUS. Never ask the user to reconstruct the ID and never replay the POST automatically. |
| A process is terminal but its result enclosure is not yet available | Continue read-only result retrieval for the same ProcessId until FileContent, ProcessLog, or the declared terminal result is obtained, unless an unrecoverable authentication or environment blocker occurs. |
| A mutation receives 401, 403, timeout, connection loss, or 5xx after dispatch | Classify as OUTCOME_UNKNOWN, persist the request fingerprint and any returned identifiers, and reconcile by read before considering another write. |
| Data Loader initiation succeeds but no durable request identifier is captured | Classify as OUTCOME_UNKNOWN and reconcile task-scoped request history against the pre-dispatch snapshot; do not upload or initiate again automatically. |
| A parent or child mutation target link is stale | Refresh it only for read/reconciliation evidence. Do not turn the new link into a product-resource mutation or an unverified BO preview. |
| CVD-HDL07A Data Loader status is terminal success | Re-read the exact parent with expansion at the physical start date and following day. Mark Corrected only when both reads retain the same business identity and physical range, show the corrected Currency, and prove zero children. |
| CVD-HDL07B Data Loader status is terminal success | Re-read the exact parent with expansion immediately before, on, and after the new boundary. Mark Updated only when the old slice ends immediately before the boundary with the old Currency, the new open-ended slice starts on the boundary with the new Currency, and every read proves zero children. |
| CVD-HDL07C Data Loader status is terminal success | Run complete exact Name-and-LDG searches at the former start date, following day, and a later date. Mark Deleted only when loader detail proves one successful Delete row and all three reads return zero exact matches. |
| CVD-HDL09D Data Loader status is terminal success | Mark Deleted only when loader detail proves one loaded and zero failed Range Item rows and complete expanded-parent reads on the item start and following day prove the parent remains with zero Range Items. |
| A Range Item End Date request reaches source preparation | Return CVD_HDL_ROUTE_FROZEN. The source-backed ReplaceLastEffectiveEndDate candidate is blocked by shared template validation before upload; do not bypass the validator or substitute a plain shorter-end-date MERGE. |
| An unsupported Correct, Update, or End Date shape has historical 2xx evidence | Retain the evidence for contract design only. Do not dispatch or promote it without a separate released native HDL contract. |
| Parent or Range Item Delete has terminal loader success | Do not replay. Reconcile by exact scoped reads across the former range and mark complete only when every expected read returns no target row. For Range Item Delete, also prove that the parent remains present. |
| Parent or Range Item Delete was dispatched but its outcome was lost | Classify as OUTCOME_UNKNOWN and run only the exact former-range reconciliation reads; a new DELETE requires a fresh plan and confirmation only if the target still exists. |
| Pagination is incomplete | Continue the read before reporting no match, totals, or a complete list. |
| A child lifecycle mutation other than exact CVD-HDL09A Range Item Correct, CVD-HDL09B Range Item Update, or restricted CVD-HDL09D Range Item Delete, or a parent lifecycle mutation other than exact CVD-HDL07A Parent Correct, CVD-HDL07B Parent Update, or CVD-HDL07C Parent Delete, is requested as ordinary work | Classify as CVD_HDL_ROUTE_FROZEN and do not author, preview, or execute it. Include historical REST behavior only as supporting evidence. |
| An Allowed Override Delete target still has nested Override Usages | Classify as CVD_HDL_ROUTE_FROZEN. Do not plan or attempt prerequisite usage deletions, infer cascade behavior, author a candidate, request approval, or dispatch. |
| ValueUsages, RelatedElements, or an unapproved independent override route is targeted for write | Classify as UNSUPPORTED and refuse the mutation. |
| Confirmation is absent, expired, or bound to another fingerprint | Classify as APPROVAL_BLOCKER and stop before handoff. |
| A prior mutation is pending or outcome_unknown on resume | Run read-only reconciliation; do not repeat the mutation or ask the user to reconstruct state. |
| Persisted state or diagnostics contain secret material | Stop, remove the secret, rotate it through the authorized owner if exposure occurred, and keep only an environment/credential reference. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Required fields, dates, IDs, field matrix, or payload shape is invalid | Correct every reported field and validate again. |
| NOT_FOUND | An exact scoped reference or target is absent | Request a valid value or confirm the intended scope/date. |
| AMBIGUOUS | More than one exact/plausible scoped target remains | Require explicit user selection; do not choose automatically. |
| CATALOG_MISMATCH | REST attributes, links, or lookup semantics conflict with the shipped task contract | Stop and reconcile current target metadata with the task contract. |
| CONTRACT_UNAVAILABLE | The shipped task contract or governed adapter does not expose the requested action | Refuse execution and return supported alternatives. |
| CVD_HDL_ROUTE_FROZEN | The exact native HDL section, field shape, or operation lacks a released validated DAT, terminal loader result, and authoritative read-back and is not a declared CVD-HDL04 controlled QA candidate | Perform zero writes; require a separate controlled nonproduction proof before promotion. |
| CVD_REGISTERED_BO_ROUTE_EVIDENCE | Stable historical evidence shows that the registered-BO child route is unavailable | Preserve the evidence reference, return CVD_HDL_ROUTE_FROZEN, and prohibit retry or replay. |
| CVD_REGISTERED_BO_METADATA_DRIFT | Current registered-BO metadata differs from the reviewed historical evidence | Preserve the audit finding; it cannot release the unavailable child route. |
| CONTROLLED_VERIFICATION_REQUIRED | The source-backed request is not yet promoted for normal execution, including a nonbaseline CVD-HDL04 parent shape whose exact live values, current template, resolvers, and read-back mappings are complete but whose shape lacks terminal runtime proof | Permit only an explicitly requested disposable nonproduction test with its own immutable preview and approval. |
| PAYLOAD_SHAPE_UNRESOLVED | An exact tenant-valid CVD-HDL04 Calculation Type resolved, but preliminary UOM applicability or the finalized required/optional/forbidden field, template, resolver, or read-back contract is incomplete | Retain the valid business selection, refresh current metadata or collect a missing required business value, and perform no DAT authoring or write; do not classify the LOV value as invalid. |
| UNSUPPORTED | The resource/action is outside the current task policy | Refuse the write and offer supported read/guidance when useful. |
| AUTH_AUTHZ | Authentication, functional privilege, or LDG data security denies access | Correct access through the authorized environment owner. |
| TRANSPORT_ENVIRONMENT | Planned outage, network failure, 5xx before dispatch, or unavailable service blocks safe work | Preserve sanitized diagnostics and retry only after service recovery. |
| CONFLICT | HTTP 409 or an exact duplicate identity exists | Reconcile existing data, then rename or intentionally select it. |
| STALE_PLAN | Scope, link, target version, payload, or fingerprint changed after preview | Rebuild preview and obtain fresh confirmation. |
| APPROVAL_BLOCKER | Current confirmation is absent or not bound to the exact plan | Show the full immutable preview and request explicit confirmation. |
| OUTCOME_UNKNOWN | A dispatched mutation has no confirmed terminal response | Reconcile by read and do not replay automatically. |
| CONTRACT_INCOMPLETE | A nominal success lacks required ID/link data or authoritative read-back proves no requested state change | Preserve the mismatch receipt, block the operation, and do not replay while the service contract remains incomplete. |
| PROCESS_FAILED | Fusion confirms that a mutation was rejected or failed | Correct the confirmed cause and create a newly reviewed plan. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation | Operation, environment alias, effective scope, affected fields, sanitized values, and corrections. |
| Reference resolution | Resolver, supplied display value, resolved business-facing name or code when the task declares it safe to display, scope/date, and ambiguity choices when needed. Keep Fusion surrogate IDs, opaque keys, ID-bearing links, and route-owned transport values in machine-only evidence. |
| Read-only completion | Query/filter context, complete row count or pagination state, selected columns, and retrieval time. |
| Long-running process completion | Attempt identifier, process type, ProcessId, latest status, elapsed monitoring time, terminal status, retrieved ZIP/log/result path, and whether reconciliation recovered or disproved process creation. |
| Terminal business outcome | Lead with Created, Corrected, Updated, Deleted, Already exists and verified, Completed read-only, Blocked, or Failed; then show the exact parent identity and read-back, distinct failed/warning/external-loading counts, child counts, where to find the record in Fusion when it remains present, and evidence paths. |
| Mutation preview | Native HDL business object, parent create, Range Item create, Range Item Override Create, Parent Correct, Parent Update, or restricted Parent Delete operation, business-facing values, exact ZIP member and row counts, archive SHA-256, target fingerprint and date/timeline boundary when applicable, validation receipts, expected read-back, and confirmation status. |
| Mutation receipt | Upload and Data Loader request identifiers, terminal detail result, archive SHA-256, exact parent read-back, and completion classification. |
| Failure or uncertainty | Phase, sanitized status/message, known identifiers, whether dispatch occurred, last confirmed state, and one safe next action. |
| Sensitive data | State that credentials, tokens, cookies, authorization headers, and CSRF values were neither displayed nor persisted. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A target, LDG, date, reference, or opaque link is unresolved | Do not guess, concatenate, or select the first result. |
| An operation is outside the allowlist | Do not generate an execution-ready mutation plan. |
| A product-resource mutation is proposed | Do not dispatch it; within this resource, the only mutation routes are the exact native HDL04 parent create, HDL10 combined parent-plus-Range-Item create, HDL05 Range Item create, HDL11 Range Item Override Create, HDL09A Range Item Correct, HDL09B Range Item Update, HDL09D Range Item Delete, HDL07A Parent Correct, HDL07B Parent Update, and HDL07C Parent Delete profiles. |
| A setup-task CSV import enters the native-HDL route | Do not parse, convert, validate, or dispatch it here. Return it to the catalog-supported CSV workflow declared in `SKILL.md`. |
| A valid type/unit differs from Flat Amount (F) with Money (M) | Do not reject it for standalone CVD-HDL04: accept every exact current tenant LOV match, including customer-defined labels and non-Money units, and require parentPayloadShape. Keep the restriction for CVD-HDL10, ordinary Range Item, and the existing currency-only parent lifecycle profiles. For CVD-HDL11, accept every exact current tenant match and require its result shape. |
| A RangeItem child operation is outside CVD-HDL05, CVD-HDL10, CVD-HDL09A, CVD-HDL09B, or restricted CVD-HDL09D; a separate-root Range Item Override operation is outside CVD-HDL11 Create; a parent lifecycle operation is outside CVD-HDL07A/CVD-HDL07B/CVD-HDL07C; or an allowed operation lacks its controlled preflight proof | Do not author an archive, request approval, or dispatch it. |
| The native HDL route, durable state, or deterministic contract does not cover an operation | Do not dispatch it. |
| Explicit RangeItem calculation type override is requested | Do not offer or send CalculationTypeId while the mapping is unreliable. |
| A native HDL row contains a field or control outside its operation allowlist | Do not hand it to an executor. |
| An LDG-scoped native parent DAT omits LegislativeDataGroupName or contains LegislativeDataGroupId or LegislationCode | Do not generate, hash, approve, upload, or initiate it; author only the exact selected LDG name. |
| A native parent DAT omits ValueGroupName or CalculationTypeName, or includes their surrogate IDs | Do not use the historical registered-BO shape. Re-resolve both current-operation business choices and rebuild before archive generation. |
| Shared guidance discovery is empty while the required task-owned ora-resource/ files are present and readable | Do not classify that helper limitation as a blocking validation failure, request a waiver, or substitute external documentation. Load and cite the task-owned files directly. |
| A mutation preview is unconfirmed or changed | Do not dispatch it. |
| A mutation returns an uncertain outcome | Do not retry before reconciliation and fresh approval if another write is needed. |
| A Data Loader request is nonterminal | Do not create a replacement process or replay the archive. Continue automatic read-only polling of the same request until terminal or an unrecoverable authentication/environment blocker occurs. |
| Aggregate Data Loader counters conflict with the explicit Data Loader process-log categories | Do not infer a failed row by subtracting loaded from total, and do not present an external-loading item in a Failed column. Preserve both reports and use detail-object status plus exact read-back for the CVD result. |
| Process creation returned no durable ProcessId | Do not ask the user to supply the missing ID before checking task-scoped process history against the pre-dispatch snapshot. Do not replay the POST unless reconciliation proves no process was created and a fresh attempt receives fresh approval. |
| A mutation returns 2xx but reconciliation shows unchanged or mismatched state | Do not report success or repeat the write; preserve receipts and block the operation. |
| An Override Usage nested GET assembled from readable IDs returns 404 | Do not claim the usage is absent. Reconcile through the exact-ID payrollOverrideUsageRules finder. |
| A prior create has a confirmed receipt and the user explicitly requests resume for that operation | Do not recreate the same object during that explicit resume; continue from the receipt and current reads. A new Create command remains independent and cannot use the receipt as input. |
| Credentials or session artifacts are requested for task state | Do not collect or persist them; use the configured credential/session mechanism. |
| A response differs from the shipped task contract | Do not normalize the difference away or fabricate missing fields. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.EXECUTION_GATE | decision | 6 | execution_gate | read_only_ready->CVD.DONE_READ_ONLY;mutation_plan_ready->CVD.READY_FOR_CONFIRMATION;blocked->CVD.HANDLE_ERROR | CVD.ENFORCE_DESIGN | stop | Validation, dependency, reference, default, and enforcement checks completed |
| CVD.HANDLE_ERROR | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | continue | A prior node reports invalid, blocked, unsupported, unauthorized, failed, stale, or uncertain |
| CVD.READY_FOR_CONFIRMATION | terminal | 8 | terminal | none | CVD.EXECUTION_GATE | continue | An immutable mutation plan is ready for a separately governed confirmation and execution workflow; no Fusion write occurred here |
| CVD.DONE_READ_ONLY | terminal | 9 | terminal | none | CVD.EXECUTION_GATE | continue | The requested search/read result is complete and safely disclosed; no Fusion write occurred |
| RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Blocking, unsupported, stale, or failure details are safely classified and disclosed |
