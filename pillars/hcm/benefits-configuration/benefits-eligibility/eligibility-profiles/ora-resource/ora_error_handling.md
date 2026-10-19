# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Workbook, task-context, effective-date, XML, archive, or conformance validation fails | Stop before a Fusion write; show the failed stage and the smallest corrective action. |
| Target-pod lookup fails, is unauthorized, or is ambiguous | Stop before package generation; identify the resolver and supplied natural key without exposing credentials or protected response data. |
| No supported REST resolver exists for a required mapping | Stop and ask for the corresponding REST API. Do not query the database as a fallback or leave the mapping for manual completion. |
| Combined mapping/import ESS polling times out | Preserve PlCopyId, request ID, stage, last status, and elapsed wait; resume tracking by identifier rather than submitting another action. |
| generateMappings is unsuccessful or a populated source mapping has no TrgId | Report the import as failed; do not call submitImport or submit a replacement action. |
| Mapping/import ESS succeeds but the Plan Copy parent reports ImportPlDesign 10 or a terminally unsuccessful RequestStatus | Retrieve REST processing-log rows and report application failure; ESS success does not override the parent result. |
| Plan Copy parent remains nonterminal after the existing timeout | Preserve identifiers and status and stop; do not report success or submit again. |
| A live POST, PUT, or ADF action returns an error or uncertain outcome | Stop before retry and reconcile the existing Plan Copy and ESS identifiers through read-only REST requests. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Workbook, effective date, XML, mapping, archive, target, or OpenAPI document is invalid | Correct the source or API contract and generate a new immutable preview. |
| Lookup blocker | A maintained target-pod REST lookup cannot uniquely resolve the required value | Correct the natural key, access, or resolver declaration before regenerating the package. |
| Approval blocker | Approval is absent, stale, non-exact, or bound to different immutable inputs | Review the current preview and reply exactly approve in a later message. |
| Transport or authorization | OAuth, TLS, target reachability, REST privilege, or ESS access fails | Preserve sanitized diagnostics; correct the environment or access and rerun only the safe stage. |
| Process timeout | Combined mapping/import ESS or Plan Copy parent exceeds the existing wait | Resume read-only tracking with the preserved identifiers. |
| Process failed | ESS, parent status, mapping completeness, or processing logs indicate an unsuccessful application result | Correct the reported setup or package issue and obtain approval for any new submission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Approval preview | Selected target environment, Plan Copy name, workbook Session Effective Date, package digest, OpenAPI digest, setup-object counts, and the fact that no Fusion change has been made. |
| Mapping blocker | Plan Copy name or ID, mapping request ID, unresolved count, affected source names and object types, and one safe correction. |
| Import completion | One final status plus the user-facing Plan Copy name and count of each setup-object type created; omit mapping details from the normal success summary. |
| Import failure or timeout | Plan Copy name or ID, request IDs, failed stage, last parent or ESS status, elapsed wait, sanitized processing-log messages, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or stale approval | Do not create metadata, upload PackageContent, or submit an ADF action. |
| Lookup or mapping gap | Do not use database data, source-pod IDs, guessed IDs, or manual mapping as an import fallback. |
| Mutation failure or uncertain outcome | Do not automatically retry POST, PUT, or generateMappings; never fall back to submitImport for RequestSource FDOS. |
| Timeout | Do not create a replacement Plan Copy or resubmit an action instead of resuming read-only tracking. |
| Diagnostic output | Do not expose OAuth secrets, bearer tokens, passwords, token-cache content, full ZIP data, or sensitive response bodies. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PLAN_COPY.EXECUTION_GATE | decision | 5 | execution_gate | approved->BEN_PLAN_COPY.READY_FOR_RUNBOOK;approval_missing->BEN_PLAN_COPY.AWAITING_APPROVAL | BEN_PLAN_COPY.ENFORCE_DESIGN | stop | Immediately before the governed REST runbook performs its first Fusion mutation. |
| BEN_PLAN_COPY.READY_FOR_RUNBOOK | terminal | 6 | terminal | none | BEN_PLAN_COPY.EXECUTION_GATE | stop | Validation, dependencies, target-pod reference resolution, immutable preview, and exact approval are complete; the existing runbook may perform one approved REST execution. |
| BEN_PLAN_COPY.AWAITING_APPROVAL | terminal | 7 | terminal | none | BEN_PLAN_COPY.EXECUTION_GATE | stop | The immutable preview is ready but a later standalone approve message has not been supplied. |
| BEN_PLAN_COPY.FAILED | terminal | 8 | terminal | none | none | stop | A validation, dependency, lookup, design, transport, authorization, timeout, or application-result blocker is present. |
