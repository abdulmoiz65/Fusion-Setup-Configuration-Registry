# Time Layout Sets Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Environment release is before 27A | Inform the user that Time Layout Sets is not available through this skill for environments before release 27A, then stop. |
| REST capability cannot be confirmed | Stop; do not select an FSM or direct REST alternative. |
| Validation, dependency, or lookup failure | Stop before preview, import, retry, or fallback selection. |
| A criteria search, update, or delete has no candidate meeting every supplied condition | State that no matching Time Layout Set was found. |
| A criteria search, update, or delete has multiple candidates meeting every supplied condition | Show all matching candidates and ask the user to select one. |
| A create duplicate check finds a candidate through Name or the non-Name fallback | Present the matching Time Layout Set's business values and ask whether to use it or create a new layout; do not continue to creation without that choice. |
| REST 401 or 403 | Classify as authentication or authorization failure and stop. |
| Uncertain write outcome | Do not retry; reconcile by safe read before a new mutation. |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not enter the provider-owned approval process and do not place a warning, diagnostic, or technical note in the summary. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required data missing or invalid | Request correction. |
| Input validation | Complete Summary source is blank, unverified, unresolved, or metadata-only | Correct the source values before generating the summary. |
| Catalog mismatch | LOV has no exact result | Request supported value. |
| Auth/authz | REST returns 401 or 403 | Restore approved access then rerun only read. |
| Approval blocker | Preview or approval absent | Present target, operation, and artifact. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import | Target environment, operation, business object, and immutable import artifact or preview. |
| On failure | Failure class, stage, sanitized message, and safe next action. |
| Complete Summary is blocked | Missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Opaque key unavailable | Do not construct it from a business ID. |
| POST, PATCH, DELETE, batch, or import uncertain | Do not retry automatically. |
| A Complete Summary is presented | Do not expose identifiers, codes, keys, internal values, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw boolean values, diagnostics, or warnings. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TLS.PROVIDER_APPROVAL | step | 60 | execution_gate | ready->TLS.READY;blocked->TLS.HANDLE_ERROR;unsupported->TLS.HANDLE_ERROR | TLS.ENFORCE_DESIGN | stop | A valid business-only Complete Summary is present; provider execution and approval ownership remain unchanged |
| TLS.RETURN_UNSUPPORTED_RELEASE | terminal | 7 | terminal | none | TLS.CHECK_RELEASE_SUPPORT | stop | The environment release is before 27A and Time Layout Sets is unavailable through this skill |
| TLS.READY | terminal | 70 | terminal | none | TLS.PROVIDER_APPROVAL | stop | All summary, preview, and approval gates pass for handoff to the provider-owned approval process |
| TLS.HANDLE_ERROR | terminal | 80 | terminal | none | none | stop | A declared failure occurs |
| TLS.SEARCH_SINGLE_RESULT | terminal | 81 | terminal | none | TLS.SEARCH_LAYOUT_SETS | stop | One criteria-search match was loaded completely and presented to the user |
| TLS.SEARCH_MULTIPLE_RESULTS | terminal | 82 | terminal | none | TLS.SEARCH_LAYOUT_SETS | stop | Multiple criteria-search matches were presented to the user for selection |
| TLS.SEARCH_NO_RESULTS | terminal | 83 | terminal | none | TLS.SEARCH_LAYOUT_SETS | stop | No candidate met every supplied search condition |
| TLS.AWAIT_DUPLICATE_CHOICE | terminal | 84 | terminal | none | TLS.SEARCH_LAYOUT_SETS | stop | A create request has a matching Time Layout Set and awaits the user's use-existing or create-new choice |
