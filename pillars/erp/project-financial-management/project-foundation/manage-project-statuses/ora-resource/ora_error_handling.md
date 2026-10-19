# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Explicit or implicit unsupported operation | Return the scope guard reason before external lookups when possible; after baseline resolution refuse implicit rename, persisted clear, mode reinterpretation or child removal. Do not collect unrelated create fields or silently execute a partial request |
| Valid control input with unavailable current inheritance | Retain the valid control request and expose controls_request_validation passed plus workflow_gap/catalog_or_metadata_mismatch. Full request validation and import readiness remain separate gates |
| Capability or identity invalid | Name the object, classification, status, requested field and permitted action; distinguish nonaddable from read-only |
| Partial/seed-filtered baseline | Report identity coverage; do not call zero exported matches proof of nonexistence |
| Lifecycle/workflow invalid | List conflicting named targets and separate product requirements from FSCR workflow-loop safeguards |
| Next type change removes edges | Show exact old/new type and edge diff; do not execute an unverified CSV removal |
| Missing controls or progress weight | PROJECT create may use documented standard rows under prefer-current-else-standard with explicit disclosure; exact-inheritance, existing update preservation and progress weight still need current evidence |
| Seeded PROJECT classification controls excluded from export | Under prefer-current-else-standard, prepare standard source rows with controls_basis=standard_source and inheritance_verified=false; show this limitation and all values before Data Loader approval. Under exact-inheritance, retain valid input and block as workflow_gap / catalog_or_metadata_mismatch. No live control lookup is declared; do not ask for valid input again or require UI access |
| Malformed, inconsistent or ambiguous source-control evidence | Block; do not hide the error by switching to standard defaults |
| Clearing disabled workflow outcomes | Distinguish UI selector reset from unverified persisted CSV clearing |
| S classification confused with a custom status | Report the parent-object classification code and exact native bridge; do not ask the consultant to pick a custom status in that classification |
| Required status-code map missing | Run the declared read-only identity lookup after target/schema checks, or identify why its supplied response is incomplete; no UI-code collection fallback |
| Lifecycle target missing or unexpected extra target after import | Fail independent verification; compare parent mode and complete child key set with the business request, including preserved baseline rows |
| Enable Workflow or outcome differs from readback | Compare the flag and both verified stored codes in both parent CSVs; distinguish editable outcomes from fixed milestone/SOV mappings |
| Existing legacy lifecycle value | Preserve unchanged raw baseline values; do not reject an unrelated update or convert Y into S/U by assumption |
| Already matching request | Report no change after current-state comparison; do not upload a redundant package |
| Unsupported control | Reject the named object/action; explain if Allow is protected |
| Requested Allow differs from native readback, or an explicitly requested authoring UI comparison differs | Do not declare success or assume caching. Compare AllowOverridesFlag and the preserved EnabledFlag against the approved intent. Authoring review may inspect the EnabledBool getter/setter mapping; routine consultant execution uses native readback without opening the setup UI. If the wrong flag was changed, disclose the failure, preserve the evidence and prepare a separately approved correction |
| Authentication or environment failure | Report stage and sanitized failure; no tokens, secrets or properties content |
| Package/import fails | Report target, checksum, member/row and Oracle error; preserve partial results and do not resubmit automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing or malformed fields | Correct input |
| Dependency | Required identity/inheritance/target/package evidence absent | Complete the named dependency |
| Workflow gap / catalog_or_metadata_mismatch | Exact-inheritance requires unavailable PROJECT classification-control evidence | Establish and verify the missing read contract before claiming current default parity; standard-source configuration is a separate disclosed create policy, not evidence of current values |
| Design conflict | Invalid date range, forbidden field or proven workflow recursion | Correct the conflict |
| Warning/deferred | Ordinary cycle, affected use or unobserved downstream mapping | Disclose separately; do not mark passed or silently block |
| Unsupported | Direct setup REST or unverified rename/delete/clear/removal | Stop affected operation |
| Auth/authz | OAuth client or privileges fail | Correct target authentication/privilege; never change credentials on the user's behalf |
| Transport/environment | Target unavailable or process timeout | Report process ID and last state; resume only through the declared workflow |
| Approval blocker | Exact preview/checksum absent, changed or declined | Stop |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, exact object/name identity, classification, editability, defaults and inheritance, date/use findings, passed/deferred/blocked checks |
| Preview | Before/after base fields, controls, lifecycle and translations; native members; clear/remove holds; warnings; checksum. For PROJECT creates show controls_policy, controls_basis and inheritance_verified for each status; explicitly identify standard-source values as chosen configuration with current inheritance unverified |
| Result | Completed Data Loader status/process log plus fresh export; compare both parent representations, exact Allow values and preserved EnabledFlag values, complete S/U target sets, and both workflow outcome codes against the original business request. Include unchanged-baseline comparison, target/checksum and errors; initiation alone is in progress |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous identity or capability | Do not guess or treat classification as part of name uniqueness |
| Missing required evidence | Do not relabel it as a deferred downstream graph check |
| Unverified import presence semantics | Do not claim omitted/blank child rows preserve, clear or delete data |
| No approved live route/artifact | Do not save in the browser or import through a substitute route |
| Failure or partial result | Do not retry automatically or claim success |
| Local planner/package pass | Do not report a successful Fusion create/update |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.EXECUTION_GATE | decision | 9 | execution_gate | ready->PSTATUS.RETURN_SUCCESS;not_ready->PSTATUS.RETURN_ISSUES;declined->PSTATUS.RETURN_REFUSAL | PSTATUS.ENFORCE_DESIGN | stop | Return validation/read guidance or require the exact Data Loader approved preview |
| PSTATUS.RETURN_SUCCESS | terminal | 10 | terminal | none | PSTATUS.EXECUTION_GATE | continue | Local validation complete or package approved; not proof of a successful Fusion write |
| PSTATUS.RETURN_ISSUES | terminal | 11 | terminal | none | none | continue | Correctable issue |
| PSTATUS.RETURN_REFUSAL | terminal | 12 | terminal | none | none | continue | Unsupported/conflicting/declined action |
