# Content Types Error Handling and Proposal Gate

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied object or source-to-field mapping is ambiguous | Ask one concise question about the supplied object or mapping and stop |
| Authenticated structured environment checks are unavailable | Report preflight blocked; never request a screenshot, address-bar image, copied URL, exact reply, or user attestation |
| Release metadata is unavailable | Keep the release unknown and continue the declared operation; release metadata is not a gate |
| The fresh customer export or integrity-validated seed catalog is missing or ambiguous | Classify an evidence blocker and stop before exact-match or proposal claims |
| A required provider row, dependency, package, or loader shape is not evidenced | Report the exact failed contract; do not invent or repair it |
| Proposal or package confirmation is presented as execution approval | Apply Core Data Loader's authoritative approval policy to the current immutable preview; proposal/package confirmation alone is never submission authority |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required supplied configuration is absent or invalid | Correct the named object or row input |
| transport_or_environment | Authenticated target identity or required structured capability evidence is unavailable | Restore the declared authenticated context or structured check |
| evidence_blocker | The task export is stale, filtered, target-mismatched, or ambiguous, or the seed catalog is missing, malformed, or changed | Obtain a fresh unfiltered export and validate or regenerate the integrity-validated catalog |
| scope_or_provider_blocker | Work belongs elsewhere, an unsupported mutation is requested, or the create-only FSM contract is incomplete | Route the work or correct the named import gate |
| artifact_persistence | A proposal, evidence record, or fingerprint cannot be persisted safely | Stop and disclose the artifact failure |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Proposal review | Supplied scope and values, source and mappings, evidence fingerprint, exact matched identifiers, omitted optional groups, exclusions and unresolved required values |
| Exact duplicate result | Actual matched identifier and exact evidence; creation is blocked without reuse or updates |
| Blocked result | Failure class, missing evidence or decision, and one safe next action |
| Import handoff | Exact task, package name and SHA-256, approved provider-row and readiness fingerprints, target alias, create-only effect, core.data-loader route, Task Hook result, and approval state |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Proposal or package is accepted | Do not interpret acceptance as approval to upload, import, update, merge, delete, or end-date |
| A direct write route is requested | Do not call Fusion REST, FSM import, HDL, HSDL, browser automation, or another provider; route only through core.data-loader after Task Hook and preview approval |
| Sensitive values are encountered | Do not persist credentials, tokens, employee data, private keys, or sensitive payloads |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CT.BUILD_REVIEW_PROPOSAL | decision | 5 | execution_gate | prepared->CT.RETURN_PROPOSAL;confirmation_or_execution_requested->CT.RETURN_UNSUPPORTED;blocked->CT.RETURN_BLOCKED | CT.ENFORCE_DESIGN | stop | A compliant review-only Content Types proposal is ready to fingerprint |
| CT.RETURN_PROPOSAL | terminal | 6 | terminal | none | CT.BUILD_REVIEW_PROPOSAL | stop | A fingerprinted review-only proposal is returned with no execution authorization |
| CT.RETURN_EXACT_DUPLICATE | terminal | 7 | terminal | none | CT.CHECK_EXACT_EXISTING | stop | An exact existing definition blocks creation; display its matched identifier |
| CT.RETURN_QUESTION | terminal | 8 | terminal | none | CT.CAPTURE_CONFIGURATION | stop | One concise technical-scope clarification is required |
| CT.RETURN_BLOCKED | terminal | 9 | terminal | none | none | stop | Input, evidence, exactness, dependency, design, or persistence is blocked |
| CT.RETURN_UNSUPPORTED | terminal | 10 | terminal | none | none | stop | The request is out of scope, uses an unsupported mutation, or bypasses the approved create-only route |
| CT.RETURN_IMPORT_READY | terminal | 13 | terminal | none | CT.ENFORCE_FSM_IMPORT | stop | Task validation returns the exact create-only package evidence to core.data-loader for immutable preview; no upload is authorized |
| CT.RETURN_IMPORT_BLOCKED | terminal | 14 | terminal | none | none | stop | The create-only package or Data Loader handoff contract is invalid, stale, changed, or incomplete |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Common Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
