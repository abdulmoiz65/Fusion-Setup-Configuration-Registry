# Planning FBDI Errors and Core Handoff

## Error Situations

| Situation | What Should Happen |
|---|---|
| Unsupported request or no supported ZIP member | Stop preparation and show the supported table from SKILL.md; do not broaden scope from BO metadata |
| Mixed ZIP | Prepare a new supported-only ZIP, preserve source/retained bytes and order, and disclose exclusions in the final Core preview |
| Missing current template, CTL, tab or mismatched contract | Stop local preparation; resolve the reported source/column issue without substituting remembered layouts |
| Invalid row, date, field count or generated END | Report member/row/column without dumping sensitive data; correct the mapping and prepare a new artifact |
| Existing/unwritable output or persistence failure | Preserve source and existing outputs. Report any successfully created artifact and stop before live work; choose a new destination |
| Missing load context or Core evidence | Stop at readiness; use the selected project/Core workflow, never a direct REST/browser/ESS fallback |
| Changed artifact or execution context | Invalidate the preview and approval; return through Core's fresh validation workflow |
| Upload/initiation failure or timeout | Use Core's diagnostics and retry policy; retain immutable evidence for reconciliation and never resubmit automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Unsupported entity, malformed CSV/ZIP, unknown mapped field or invalid value | Correct inputs before preparing again |
| catalog mismatch | Current public contract or live Core BO route differs | Resolve through the owning template/Core workflow |
| artifact persistence | Output conflicts, unavailable destination or report write failure | Preserve source and report partial local artifacts |
| approval blocker | Missing or stale Core approval | Obtain approval through Core only |
| auth/authz, transport/environment, Fusion API, process timeout, process failed | Core reports a live failure | Return Core's prescribed diagnostics; no independent retry |

## Task Nodes

RETURN_READY means read-only task validation completed and Core may present its
approval preview. It is not approval and never authorizes upload by itself.
There is no separate pillar approval prompt, authentication, submission, or
automatic status poll.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_READY | terminal | 40 | terminal | none | CHECK_LOAD_READINESS | stop | Task rules passed; return evidence to Core for approval |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Input, policy or readiness blocks the Core preview |
