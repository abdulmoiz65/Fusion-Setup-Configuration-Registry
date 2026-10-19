# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Identity/date invalid | Stop with template identity, cardinality, and date conflict |
| Supplied project/task dates are reversed or violate known bounds | Stop before approval with the exact date conflict; do not invent missing dates or turn an optional project end date into a required input |
| Fusion rejects a supplied reference | Report the exact field/value and Fusion response. Stop without retry or automatic field substitution. |
| Section/child/copy scope invalid | Stop with child family, action, key, prerequisite, and requested-versus-current state |
| REST coverage incomplete | Stop before preview only when a requested field/child action is absent from the published operation schema or an exact operation-required ID cannot be resolved through a proven standalone resolver; a supported root name needs no pre-resolution, and a zero-row GET need not advertise write or future child links |
| Target CUD registration unavailable | Build no executable handoff; the immutable preview may still be prepared from the published schema and authenticated read evidence, but submission waits for the required registered adapter or documented exception |
| Approval-bound payload/target/method/URI/route changed | Stop with approval_blocker before dispatch; preserve the approval record and changed-artifact evidence, then rebuild the preview and obtain new approval. No framework-native checksum option is required. |
| Import/load adapter or active workflow classification missing | Stop the affected write before approval with the exact route gap. Do not bypass core.data-loader using a generic REST POST or relabel the load. |
| Error response or correlation detail unavailable from the client | Persist only exposed sanitized status/error facts in the consuming workflow's receipt and disclose the missing evidence; never invent headers, log output or successful readback. |
| Approved POST returns `401` or `403` | Record the authorization failure and stop without retry, compensation, or payload change |
| Approved POST rejects `ProjectPlanTypeName` | Record that the body used a noncontract attribute. Do not retry. Normalize future input to `ProjectPlanType` (or one resolved `ProjectPlanTypeId`), rebuild the complete payload and checksum, and obtain fresh approval. |
| Approved POST requires ExternalTaskId | Record the target operation discrepancy and stop; a runtime error alone is not reusable required-field metadata. Obtain fresh operation-specific create evidence, rebuild the complete payload if required, and obtain fresh approval; never infer an ID or retry. |
| Approved POST returns `ORA-01403` or another fieldless no-data error | Record it as a downstream target lookup failure and do not retry the body. Retain the exact UTC request window, payload checksum, endpoint, status/body, and only safe correlation headers such as X-Oracle-DMS-ECID or X-Request-ID. Compare the operation with an evidenced successful product test or target record; correct only an identified missing lookup/default. If no correction is identified, require target log diagnostics before another preview. |
| Project plan types fail for the same project unit | Report the target response and context. Do not use another template's contextual LOV or vary fields automatically. |
| A supported customer-supplied root reference name is rejected | Report the exact field/value and Fusion response as a target compatibility result. Do not reinterpret another template's LOV, silently replace the name with an ID, or imply that unmentioned references passed. |
| Payload preflight fails | Stop before approval and report every JSON path and issue. Do not remove fields silently or bypass a runtime overlay because generic metadata marks it optional. |
| A delegated or copied checksum differs from the current task-local file | Treat it as stale internal handoff data, not as missing customer input. Recompute the payload and metadata checksums from the current files, replace the validation record, and continue when validation passes. Never ask the customer to choose between digests. |
| TaskNumber update also changes ExternalTaskId | Report both saved values and any mismatch with the approved preservation expectation. Stop the remaining operation batch; do not retry or compensate automatically. Prepare a revised preview that discloses the coupled ExternalTaskId change and obtain approval before continuing |
| Payload preflight passes | Report structural readiness only. Do not claim target reference eligibility or production success; both are verified only by successful POST plus canonical readback. |
| Boolean value is quoted | Treat it as payload-shape failure. Preserve explicit boolean choices and apply false only to omitted documented create fields; rebuild the normalized artifact and preview. |
| Project priority lookup ambiguity | Zero or multiple enabled effective matches block before preview; retain the redacted request, date, cardinality and safe evidence reference. No guess, fallback or write probe. |
| Generic describe marks a defaulted/response field mandatory | Ignore generic create mandatory flags; use the published create rules plus fresh operation-specific create metadata. Do not force audit/generated fields, currency or external IDs into the body. |
| Create metadata contradicts a documented project-type-derived omission | Stop before preview as catalog mismatch/contract conflict. Reconcile operation evidence with the create contract; preserve omission and never request or insert a value merely to bypass derivation. |
| Missing task inheritance or organization after preparation | Do not ask for or inject omitted nested task organization; let Fusion derive it and verify returned task values. Preserve explicit overrides. Direct-create missing organization or fresh operation-specific requirements remain blockers. A rejected explicit override needs a corrected preview and fresh approval; never retry automatically |
| Output path aliases an input or another output | Reject before any artifact write; preserve every input byte and use separate validation/prepared artifact paths |
| Lookup type/key or UI mapping is unproven | Stop before the lookup or preview with the precise contract gap. Do not guess a lookup type, manufacture a hash key, substitute a project-resource field, or translate an outline label into an option code |
| Multiple local payload issues | Report all locally detectable structural issues together. Do not use a Fusion error to vary fields automatically. |
| Consumer impact unsafe | Stop with template ID, change, consumer counts, and impact |
| REST execution fails | Report target, route, checksum, method/URI, verified earlier operations, and Oracle error; no retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity/date/value/scope failure | Correct input |
| Dependency | Baseline/section/use/route evidence missing | Complete dependency |
| Conflict | Duplicate child, hidden prerequisite, unsafe use | Correct/preserve |
| Unsupported | Root delete, duplicate/copy, unsupported child verb, or FSM/CSV import | Stop |
| Approval blocker | Preview absent/changed/declined | Stop |
| Internal handoff repair | Copied checksum is stale but the current payload, metadata, and regenerated validation record agree | Repair automatically and continue to a customer-readable approval request |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, template/ID, dates, core context, requested sections/children, copy scope, route coverage, use impact |
| Preview | Before/after business fields, explicit child rows, ordered REST operations/URIs, preserved omissions, and uncovered fields; keep technical digests in the internal record unless the customer asks for them |
| Result | Per-operation REST status, canonical URIs/row counts, independent reread, target/checksum, errors |

### Customer-Facing Capability Blockers

When a requested setting cannot be saved through the current supported workflow,
explain the limitation using the customer's requested setting names. State which
parts can be prepared, which settings the current skill cannot yet save, and
that creation is paused to avoid leaving requested settings missing. Offer
skill enhancement or an explicit scope revision; never silently omit a setting.
Do not imply that Fusion itself lacks the feature or that the customer's clear
input is invalid. List every gap actually present in this request, including
explicit outline numbers when requested; do not add gaps for unrequested settings.

Use this pattern, replacing the bracketed content with the current request:

> I can prepare [supported parts]. However, the current skill cannot yet save
> [requested settings] through its supported REST workflow. I have paused
> creation so your template is not created with those settings missing. These
> capabilities need to be added to the skill, or you can approve creating the
> template without them.

Keep phrases such as "no verified write mapping", "unsupported surface",
"complete REST coverage", "scope diagnostic", and "FSCR contract needs to be
extended", along with schema gaps, field names, mapping-file paths and endpoint
details, in the redacted diagnostic artifact;
explain them to the customer only when technical detail is requested. If no
Fusion write occurred, state that the template has not been created. If earlier
operations succeeded or their outcomes are uncertain, report that actual state
instead of claiming that nothing was created.

Do not ask for a helpfulness rating when creation is blocked, failed or incomplete.
Use the active task rule version; if an earlier run's diagnostic uses older
wording, preserve its technical evidence and render the current customer-facing
explanation rather than copying that diagnostic verbatim or claiming a new run.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous/reference/section/use state unknown | Do not guess |
| Partial REST coverage | Do not write a partial template or claim whole-template success |
| Target CUD unavailable | Do not substitute an alternate route |
| Delete/duplicate/copy/FSM/CSV import | Do not infer support |
| Preview/approval absent | Do not execute |
| Failure | Do not retry, compensate, switch route, or claim success |
| Invalid-attribute correction | Do not edit and resend the rejected body under its old checksum or approval |
| Missing runtime field correction | Do not change supplied identifiers or regenerate approved IDs. Use the declared nested-create missing-ID policy only during preparation; discard rejected approval, validate the complete corrected body and obtain fresh approval before another write |
| Fieldless lookup failure | Do not guess which field passed, preserve metadata-only cardinality claims, or retry by removing fields one at a time |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.EXECUTION_GATE | decision | 8 | execution_gate | ready->PTMPL.RETURN_SUCCESS;not_ready->PTMPL.RETURN_ISSUES;declined->PTMPL.RETURN_REFUSAL | PTMPL.ENFORCE_DESIGN | stop | Return validation or require approved preview |
| PTMPL.RETURN_SUCCESS | terminal | 9 | terminal | none | PTMPL.EXECUTION_GATE | continue | Validation complete/write independently verified |
| PTMPL.RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Correctable issue |
| PTMPL.RETURN_REFUSAL | terminal | 11 | terminal | none | none | continue | Unsupported/unsafe/declined action |
