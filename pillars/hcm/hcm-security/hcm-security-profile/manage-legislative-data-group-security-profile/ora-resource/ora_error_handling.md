# Legislative Data Group Security Profile Error Handling

Unsupported failures remain blocking.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A profile Name is unavailable or ambiguous | Stop before preview, CSV package generation, or import. For a rename, verify the old exact Name and supplied current ID first, then require zero exact matches for the proposed new Name. |
| A genuine rename has an available new Name | Report `rename CSV identity mapping unverified` and stop before CSV preview or import. Do not infer parent or child update keys from REST IDs or name-based GroupingKey fallbacks. |
| Required Name or child association value is invalid | Classify as input validation and request the corrected value |
| Profile lookup returns zero or multiple matches | Stop and request an unambiguous profile identity |
| Legislative data group lookup returns zero or multiple rows | Stop and request a disambiguating Name; do not invent an identifier |
| CSV package is requested without a current supported template-only export or without unambiguous resolver output for members, headers, mappings, linkage, metadata bytes, and node order | Classify as a blocking CSV-layout gap; do not generate a package or invent a CSV value. A missing ViewInstanceName or GroupingKey pattern alone uses the documented member-specific fallback. |
| CSV import is requested before preview approval | Classify as an approval blocker; do not invoke core.data-loader |
| A live create or update is requested | Require the current target-environment task-template CSV package, immutable ZIP preview, exact approval, one core.data-loader-authorized task-level CSV import, and process-log verification before reporting a result |
| A request or response failure is not documented by the supplied source | Stop and retain only sanitized diagnostics for source-authoring correction |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | A required field violates the describe contract | Correct the supplied input |
| input validation | No legislative data group association is supplied | Supply at least one exact Name |
| artifact persistence | Current supported CSV export or mapped package is missing | Export the task data and prepare a mapped package |
| catalog mismatch | Rename CSV identity mapping is unverified for the existing parent and children | Stop before preview or import; obtain a current target-environment template and author a separate supported rename contract |
| approval blocker | The exact CSV preview has not been approved | Stop before core.data-loader |
| Fusion API | A documented lookup fails | Stop and report sanitized diagnostics |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Blocked result | Task identity, failed rule, missing contract, and sanitized next action |
| Diagnostics | Do not expose credentials, tokens, or protected runtime data |
| Any response | Do not display internal IDs, including profile, child-row, lookup, process, request, content, or data-set identifiers; retain them only in sanitized internal evidence when needed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Legislative data group lookup does not resolve uniquely | Do not invent an identifier or child association |
| Profile identity is ambiguous | Do not select a profile by guesswork |
| Failure or result is uncertain | Do not retry or claim completion from the supplied describe contract alone |
| Current supported CSV layout is unavailable or incomplete | Do not invent CSV columns, keys, or child-row structure. Use the documented member-specific ViewInstanceName and GroupingKey fallback only when the template omits those values. |
| Exact CSV preview is not approved | Do not invoke core.data-loader |
| A direct REST create or update is requested | Do not send POST, PATCH, PUT, or DELETE to legislativeDataGroupSecurityProfiles; prepare and approve a task-level CSV import instead |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.READY | terminal | 9 | terminal | none | LDGSP.ENFORCE | continue | All task-local validation, dependency, and design checks are ready |
| LDGSP.ERROR | step | 10 | error_handler | stopped->LDGSP.BLOCKED | none | stop | Any task-local validation, lookup, or readiness gate fails |
| LDGSP.BLOCKED | terminal | 11 | terminal | none | none | stop | The request is blocked after diagnostics |
