# Remit-to Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or invalid business value | Identify the affected row and ask one focused question; preserve prior answers and repeat clarification as needed |
| Missing product evidence | Identify exact unresolved field/resolver/operation and owning source gap; do not confuse it with invalid customer data |
| Empty address | Surface import deriveLocationId address-is-empty condition with destination details needed |
| Unknown reference set | Surface deriveSetId recoverable row error; do not fall back to COMMON or create a set |
| Multiple address matches | Explain known identity ambiguity; do not choose a first row. Lack of a global HZ export alone is not such a match; see ../references/postal-validation-contract.md |
| Unsupported audit input | Explain service-owned history and ask to remove the input; never override audit protection |
| Upload or process error | Capture process identity, row counts, alerts, logs and diagnostics; do not call upload acceptance success. For postal validation errors ask the specific business correction, retain the rest, and check partial persistence before a new candidate |
| Unknown or failed import outcome | Stop before retry and acquire a fresh read-only export to detect partial persistence |
| Persisted mismatch | Show requested, candidate and exported values with exact entity/key; preserve evidence and investigate before new candidate |
| Data Loader handoff | Require ready applicable rule plan, independently validated candidate and current core-owned approval; this gate does not itself import |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Design | Task, exact set and destination, customer coverage, operation, rows, defaults, preserved values and unresolved items |
| Import handoff | Environment from active project, exact task, candidate identity/hash, validation and core Data Loader routing |
| Final | Verified outcomes only, requirement matrix, warnings, source/process evidence, missing items and safe resume step |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Incomplete graph or adapter | Never generate/import a candidate by skipping missing identity or semantic evidence |
| Direct write request | No direct REST or AR/HZ table writes; use authorized core Data Loader task-level FSM route |
| Retry | Never replay an uncertain request or reuse approval for a materially changed candidate |
| Credentials | Never persist passwords, tokens, cookies or browser profiles in skill, package or reports |
| Evidence | Do not claim a static graph, source review or successful upload is live persisted-state verification |

Sources: SRC-REMIT-AM-IMPL (recoverable errors, XML row removal, commit/error aggregation); core Data Loader and shared task export own execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_HANDOFF | decision | 60 | execution_gate | ready->RMT_DESIGN_READY;issues->RETURN_ISSUES | RMT_DESIGN | stop | Preparation handoff only; no mutation within this graph |
| RMT_DESIGN_READY | terminal | 70 | terminal | none | RMT_HANDOFF | stop | Design checks satisfied, not yet imported or persisted-state verified |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Report unresolved input, source, dependency or execution issue with safe resume context |
