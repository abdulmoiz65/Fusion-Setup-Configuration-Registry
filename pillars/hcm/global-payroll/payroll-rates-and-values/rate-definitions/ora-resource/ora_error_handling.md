# Rate Definitions HDL Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context, rate identity, category design, contributor, or effective-date data is missing | Stop before preparation; identify the missing field and required setup action; do not require optional source-system identifiers. |
| Parent MERGE identity or contributor linkage is ambiguous | Stop before preparation; report the supplied code, LDG, effective date, source-system context, and match result without selecting a substitute. |
| Target metadata is missing, release-mismatched, or does not confirm an attribute code or behavior | Stop before preparation; export the target-pod attributes and do not infer a code, length, key, or update rule. |
| A target reference has zero or multiple matches | Stop before preparation; report the supplied value, LDG, effective date, and match result without selecting a substitute. |
| The proposed route is not HDL through core.data-loader | Stop before any Fusion interaction; do not construct a substitute REST or FSM request. |
| Core Data Loader business-object discovery or template retrieval fails | Stop before HDL preparation; preserve sanitized diagnostics and resolve the configured target environment, access, or registered-business-object issue. |
| Preview, approval, upload, import initiation, or process status is failed or uncertain | Preserve redacted diagnostics and stop; do not automatically retry a production import. |
| An import process fails | Preserve the object, source ID, line or record reference, process status, and log when available; correct only the identified issue before a separately approved retry. |
| An import process times out | Preserve environment, operation, task or job ID, last status, elapsed wait, and safe next-check route; do not resubmit. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required input, rate identity, reference, format, or category data is missing or invalid | Correct the source and revalidate; optional source-system identifiers are not a failure. |
| catalog_mismatch | Target metadata or a category-specific reference does not match the supplied design | Export or resolve authoritative target evidence; do not substitute a similar record. |
| metadata_blocker | Target business-object metadata is unavailable or incomplete | Export and verify target metadata before preparing HDL. |
| lookup_transport_auth_fusion_api | A read-only lookup cannot establish exactly one value or cannot be completed | Stop before retry and resolve the sanitized diagnostic. |
| design_blocker | A rate category, contributor, currency, periodicity, FTE, or merge-safety rule is violated | Correct the design and rerun the applicable gates. |
| approval_blocker | The HDL route, immutable artifact, or current explicit approval is absent or stale | Complete the owning core.data-loader approval workflow before a live load. |
| process_failed | The HCM Data Loader process returns an error | Preserve diagnostics, correct the source, and obtain separate approval before retry. |
| process_timeout | The import remains nonterminal after its wait window | Use the authorized status-check route; do not resubmit. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input, identity, lookup, or metadata failure | Target environment, affected parent or contributor identity, resolver purpose, failure class, sanitized message, and one safe next action. |
| Design blocker | Affected rate component, LDG, effective context, blocking condition, and correction required. |
| HDL preview | Task code, target environment, RateDefinitionV2 and RateContributorV2 scope, source-system identity, effective context, and immutable import artifact. |
| Live import approval | Exact target environment, operation, and immutable import artifact or payload, immediately before the declared live action. |
| Import failure or timeout | Failure class, stage, sanitized process evidence, last status, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct REST, FSM, or undocumented loading route is proposed | Do not generate a substitute payload or perform the load through that route. |
| The target HDL template or a required reference field is unavailable | Do not claim the HDL file is ready or use an unconfirmed code translation. |
| Parent MERGE identity or contributor linkage is not unique | Do not select a rate definition or contributor automatically, or produce a MERGE record. |
| The core Data Loader contract cannot resolve exactly one RateDefinitionV2 business object and target template | Do not prepare, upload, submit, or retry an import. |
| Approval is missing, changed, or stale | Do not initiate a live load. |
| Upload, initiation, or process result is uncertain | Do not repeat the action automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE_DEFINITION.EXECUTION_GATE | decision | 60 | execution_gate | ready_for_approved_import->RATE_DEFINITION.DONE_READY;approval_or_readiness_missing->RATE_DEFINITION.HANDLE_APPROVAL_BLOCKER | RATE_DEFINITION.DESIGN_GATE | stop | Require the documented core.data-loader execution contract, immutable artifact, and current approval before a live HDL import. |
| RATE_DEFINITION.HANDLE_INPUT_ERROR | step | 70 | error_handler | handled->RATE_DEFINITION.RETURN_ISSUES | RATE_DEFINITION.VALIDATE_INPUT | stop | Input validation is invalid. |
| RATE_DEFINITION.HANDLE_LOOKUP_ERROR | step | 80 | error_handler | handled->RATE_DEFINITION.RETURN_ISSUES | RATE_DEFINITION.ASSESS_MERGE_IDENTITY | stop | Parent identity, contributor linkage, metadata, or reference lookup is unresolved. |
| RATE_DEFINITION.HANDLE_DEPENDENCY_ERROR | step | 90 | error_handler | handled->RATE_DEFINITION.RETURN_ISSUES | RATE_DEFINITION.RESOLVE_DEPENDENCIES | stop | A required dependency is blocked. |
| RATE_DEFINITION.HANDLE_DESIGN_BLOCKER | step | 100 | error_handler | handled->RATE_DEFINITION.RETURN_ISSUES | RATE_DEFINITION.DESIGN_GATE | stop | A design rule blocks the request. |
| RATE_DEFINITION.HANDLE_APPROVAL_BLOCKER | step | 110 | error_handler | handled->RATE_DEFINITION.RETURN_ISSUES | RATE_DEFINITION.EXECUTION_GATE | stop | HDL readiness or explicit approval is absent. |
| RATE_DEFINITION.DONE_READY | terminal | 120 | terminal | none | RATE_DEFINITION.EXECUTION_GATE | stop | Resource validation is complete and the separate approved core.data-loader workflow may proceed. |
| RATE_DEFINITION.RETURN_ISSUES | terminal | 130 | terminal | none | none | stop | A validation, lookup, dependency, design, approval, or process-readiness issue is handled. |
