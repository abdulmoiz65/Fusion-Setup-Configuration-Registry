# Event Group HDL Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Group identity, purpose, LDG, effective context, or source technical field is missing | Stop preparation and identify the exact missing field and component. |
| Event Group type or Proration Period is missing or outside its allowed business values | Stop before lookup or HDL mapping; list the applicable permitted values from Input Validation. |
| Target-release metadata or an authoritative lookup contract is unavailable | Stop production mapping and report the unresolved resolver and contract fields. Preserve the explicit gap in ora_reference_lookups.md. |
| Reference resolution returns zero or multiple matches | Report resolver, supplied value, and match count; do not choose a result. |
| Parent and child keys or contexts disagree | Stop before packaging and identify inconsistent records. |
| DAT or ZIP shape is invalid | Stop before upload and identify the affected file, component, and correction. |
| Target identity, loader workflow, immutable preview, or required approval is absent | Stop before upload or initiation and complete the selected workflow gate. |
| Upload or import outcome is uncertain | Preserve redacted diagnostics and reconcile the existing operation before another attempt. |
| HDL process fails or times out | Preserve status and ProcessLog when available; report process identity, last status, elapsed wait, and next-check path. |
| A load succeeds but the expected notification is absent | Check the originating transaction, consuming element setup and eligibility, monitored entity/attribute, and applicable event-action association. Do not present a successful HDL status as proof of the functional outcome. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | A required field, key, date, component, or condition is missing or invalid | Correct the source record and revalidate. |
| catalog_mismatch | Target metadata does not support a proposed technical value | Recheck the target export and design. |
| auth/authz | Metadata or loader access is denied | Verify privileges through the selected workflow. |
| transport/environment | Target cannot be reached or its identity cannot be confirmed | Stop and verify environment before retrying a read-only step. |
| Fusion API | The declared loader returns a documented application error | Preserve redacted response details and use the workflow's correction path. |
| artifact_persistence | DAT, ZIP, or diagnostic artifact cannot be safely written | Stop and repair the workspace path or artifact issue. |
| approval_blocker | Exact preview or approval is absent or stale | Complete the required gate. |
| process_failed | HDL process ends with errors | Preserve available ProcessLog; correct source and use separately approved retry path. |
| process_timeout | Process remains nonterminal after its wait window | Check the existing process; do not resubmit. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Load preview | Task CUSTOM_EVENT_GROUP, target environment, LDG, purpose, operation, immutable ZIP identity, and EventGroupCode. |
| Failed load | Stage, failure class, process identity, last status, redacted log reference when available, and next action. |
| Timeout | Environment, operation, ProcessId or requestId, last status, elapsed wait, and next-check path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A guessed REST endpoint or alternate integration is proposed | Do not substitute it for the declared HDL route. |
| Metadata, lookup, business-object registration, or execution contract is TBD | Do not claim readiness or prepare a production import artifact. |
| The executing identity has event-group access but HDL file-upload or business-object review grants are unverified | Do not infer loader authorization from an OAuth login or payroll role alone. |
| Preview or approval is missing or changed | Do not upload or initiate a ZIP. |
| Upload outcome is uncertain, or process failed or timed out | Do not automatically replay the operation or report success. |
| A DAT or diagnostic contains a credential, token, cookie, or production-only sensitive value | Do not retain it in the repository or project workspace. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENT_GROUP.EXECUTION_GATE | decision | 6 | execution_gate | ready->EVENT_GROUP.READY_FOR_LOADER;blocked->EVENT_GROUP.RETURN_ISSUES | EVENT_GROUP.DESIGN_GATE | stop | Confirm core.data-loader as the selected route, HCM EventGroup business object, exact target/LDG, immutable validated ZIP with EventGroup.dat at root, and passed CUSTOM_EVENT_GROUP Task Hook checks. Return validation results for the loader's preview and approval stage; this node performs no upload and does not require approval before Task Hook completes. |
| EVENT_GROUP.READY_FOR_LOADER | terminal | 7 | terminal | none | EVENT_GROUP.EXECUTION_GATE | continue | Return the exact artifact identity, target, task context and passed checks to core.data-loader. The loader retains its preflight/preview, obtains its required approval once, verifies the approved artifact and context, then owns UCM upload and initiation. Any artifact or target change invalidates this handoff and requires fresh validation. |
| EVENT_GROUP.RETURN_ISSUES | terminal | 8 | terminal | none | none | continue | Return missing or blocked authoring and validation details without a Fusion write. |

## Source

- Developer-supplied EventGroups-HDL.md: HDL operation and payload structure; Setup and validation; Security, authorization, and release behavior; Limitations; Unresolved Items.
- Developer-supplied EventGroups-HDL.md: Troubleshooting decision path, HDL access-guide reference, and the distinction between import status and functional validation.
- core/data-loader/SKILL.md: Mandatory import routing and authorization; Execute a data-loading request; Task Hook routing. Task validation precedes its approval feedback; no duplicate task-level approval is required.
