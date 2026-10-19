# Error Handling

Creation rules can validate and prepare only. A successful task-rule terminal does not prove a ZIP was generated, accepted by Fusion, imported or read back. Core Data Loader owns its own preview, approval, upload and initiation; later status and post-import export are separate explicitly requested workflows.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing Name, Project Unit, From Date or required resource component | Stop with affected batch row, missing business field and safe correction |
| Existing RBS name or ambiguous target identity | Stop; never overwrite or reinterpret as update |
| Unobserved descendant or actual Organization: Inventory Item resource requested | Stop with the exact requested path; new UI and FSM evidence is required before extending the observed create profile |
| Set, Job or Person conversion lookup absent, ambiguous or incomplete | Stop with resolver, input representation, match count and required canonical output; do not substitute fixture values |
| Actual Job row has no Job Set | Stop that batch row and ask which Job Set to use; do not list or search all Jobs |
| Project Unit or Organization context read unavailable or ambiguous | Stop package preparation because the proven CSV context cannot be copied; do not label the supplied name invalid or substitute fixture values |
| Resolved Named Person has no complete or consistent current-export context | Stop that resource row and request an authoritative person effective-date source; do not guess dates or copy another person's context |
| Organization precedence query returns multiple rows at one level | Stop at that classification and ask for a more precise Organization identity; do not fall through to a lower-precedence class |
| Resource Class defaults or synthesized ancestor missing | Stop before loader handoff with the affected RBS, path and missing row |
| Root Alias retains a source-fixture name | Stop and regenerate preview with Alias equal to the requested Name |
| Any batch row fails | Stop the entire consolidated preparation; show all row-level errors and submit no subset |
| Final package shape, checksum or target differs from preview | Stop and revalidate one complete immutable package |
| Loader initiation fails or is uncertain | Follow Core Data Loader's authoritative result; never replay or poll automatically from this task graph |
| Requested later status or readback incomplete | Report actual stage, external identifier and next safe check; never call in-progress accepted initiation verified completion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing or malformed business input, date, path or row component | Correct the affected row and revalidate the whole batch |
| Catalog mismatch | Task, target, observed format ID or CSV member differs from same-target evidence | Stop and refresh the exact target contract |
| Reference unresolved | Zero/many matches, missing field, truncated lookup or undocumented response mapping | Clarify input or provide the missing lookup contract; no guessed value |
| Artifact persistence | Seven-member ZIP cannot be written or checksum cannot be verified | Preserve source rows and stop before loader preview |
| Approval blocker | Loader preview absent, changed or declined | Stop; use only the loader's own approval process |
| Fusion API or process failed | Later delegated lookup/import reports a failure | Preserve redacted diagnostics and use delegated recovery path |
| Process timeout | Later delegated status remains nonterminal beyond bound | Report last status and next-check path; no automatic resubmission |
| Unsupported | Update, end-date, billing maintenance, delete or untested resource path entered through this create route | Refuse and route only through a separately evidenced workflow |

## Data Loader Handoff

| Stage | Authority | External Operation | Required Outcome |
|---|---|---|---|
| Task validation and preparation | PRBS rules on selected current-target evidence | No mutation from this graph | Complete all rows, resolved lookups, default tree and immutable package checks |
| Upload approval and submission | core.data-loader and its Task Hook | Only loader-approved upload and initiation | Submit one exact SHA-256-bound seven-member ZIP after the loader's approval gate |
| Accepted initiation | core.data-loader | No automatic status, log or fresh export call | Return its complete Data Load In Progress report and stop this request |
| Explicit later status | core.data-loader | Supported status read for the same target/task/artifact/identifier | Report actual status and errors without a second submission |
| Explicit later setup verification | Shared task-level exporter after terminal success | Fresh complete same-task export | Compare every approved header, format and logical resource; disclose element-order normalization separately |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Exact target and task, requested RBS names, required fields, row-level findings, unresolved lookup or format-contract gaps |
| Preview | One package path and SHA-256, all names and counts, seven members, default tree, extra formats/resources, synthesized parents, root Alias, name-to-code conversions and blocked rows |
| Result | Exact stage: authoring incomplete, prepared, loader initiation accepted/in progress, later status, or separately verified post-import readback; never collapse these stages |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unknown descendant or reference contract | Do not guess IDs, response fields, class mapping or child-resource defaults |
| Sparse import package | Do not claim Fusion will create Resource Class defaults or five elements internally |
| Ambiguous Job Set or Job label | Do not copy the display name into SetCode or JobCode |
| Invalid row in a multi-RBS batch | Do not submit only the valid subset or make per-row import ZIPs |
| Missing final immutable artifact or loader approval | Do not upload or initiate import |
| Uncertain or failed submission | Do not retry, compensate or claim success automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RBS.EXECUTION_GATE | decision | 13 | execution_gate | ready->RBS.RETURN_SUCCESS;not_ready->RBS.RETURN_ISSUES;declined->RBS.RETURN_REFUSAL | RBS.ENFORCE_DESIGN | stop | Return task-rule validation/preparation only; loader owns later approval and submission |
| RBS.RETURN_SUCCESS | terminal | 14 | terminal | none | RBS.EXECUTION_GATE | continue | Validated preparation completed; import neither initiated nor verified by this terminal |
| RBS.RETURN_ISSUES | terminal | 15 | terminal | none | none | continue | Correctable input, source, reference, artifact or approval issue |
| RBS.RETURN_REFUSAL | terminal | 16 | terminal | none | none | continue | Unsupported, unsafe or declined action |
