# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing Name, duplicate child tuple, or a non-Y/N flag | Correct the source input and reject the entire import. |
| SecureByAorFlag is Y and all Area of Responsibility security criterion flags are N | Correct the parent row by setting at least one of SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, or SecureByRecTypeFlag to Y; reject the entire import. |
| View My Team's Requisitions or View All Job Requisitions is included for update | Reject the entire import. Seeded profiles cannot be updated. |
| CollaboratorRestTypeCode is supplied with a MemberTypeCode other than ORA_COLLABORATOR | Correct the child row and reject the entire import. |
| Missing archive member, duplicate metadata, changed full-export metadata contract, or broken parent/child name join | Reject the entire import. Rebuild and validate the archive. |
| Import ZIP includes an unrequested profile or a child row for an unrequested parent profile | Reject the entire import. Rebuild the ZIP from only the requested profile Names and their child rows; omitted profiles remain unchanged. |
| Unobserved child code | Block for evidence. |
| 401/403 during import authorization or execution | Route to the security owner. Do not reclassify a completed, matching technical import as failed. |
| Scoped export request | Explain that version 1 export is unscoped. |
| Import authorization is missing | Stop before import until Manage Recruiting Administration privilege evidence and approval bound to the exact ZIP checksum, target, and create/update/merge summary are available. |
| Import status is not COMPLETED or post-import readback mismatches | Stop without automatic retry. Correct the package or import issue, obtain a new approval for a changed ZIP, and resubmit only through the approved CSV import workflow. |
| Direct REST create, update, or delete is requested | Stop. Use core.data-loader task-level FSM CSV import only. |
| Package authoring is mistaken for execution approval | This resource authoring run does not authorize import, REST writes, or profile creation. Require the separate core.data-loader import workflow, exact approval, and verification gates. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required input is missing or invalid, or a duplicate child tuple is present. | Correct the source input and reject the entire import. |
| Artifact validation | Archive member or parent/child join is invalid. | Rebuild and validate the archive. |
| Catalog mismatch | Child code is unobserved or catalog support is unavailable. | Block for evidence. |
| Auth/authz | Access is denied during import authorization or execution. | Route to the security owner without retrying the completed technical import. |
| Import processing | CSV import is submitted but status is not yet COMPLETED. | Report Processing; do not report success or retry automatically. |
| Import verification | Import status fails or post-import readback mismatches. | Stop without retry and correct the package or import issue. |
| Unsupported request | Scoped export, direct REST write, or undocumented lifecycle behavior is requested. | Stop and explain the supported boundary. |
| Authoring gap | A lookup contract or privilege is TBD. | Stop until the contract is documented. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before retry | Failure class, safe next action, and whether the request is unsupported or blocked. |
| Before import | Exact ZIP checksum, target, create/update/merge summary, Manage Recruiting Administration privilege evidence, and approval record; otherwise stop. |
| Before import success | Import status COMPLETED and unscoped post-import readback that matches supplied parent fields and contains every supplied child row. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup request details are not documented | Stop; do not guess an endpoint, request body, lookup source, or response mapping. |
| Required tenant value is unresolved | Do not create, import, or modify a profile. |
| Direct REST create, update, or delete is requested | Do not call a direct REST write. Use core.data-loader task-level FSM CSV import only. |
| Import status fails or readback mismatches | Do not automatically retry or report success. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| JRSP.EXECUTION_GATE | step | 40 | execution_gate | authorized_boundary->JRSP.DONE;blocked->JRSP.HANDLE_ERROR | JRSP.ENFORCE_DESIGN | stop | A CSV import uses core.data-loader task-level FSM workflow and has exact ZIP approval, required privilege evidence, status COMPLETED, and matching post-import readback |
| JRSP.HANDLE_ERROR | step | 50 | error_handler | classified->JRSP.RETURN_ISSUES | none | continue | Any declared failure transition |
| JRSP.DONE | terminal | 60 | terminal | none | JRSP.EXECUTION_GATE | stop | CSV import has status COMPLETED and unscoped readback matches all supplied parent fields and contains every supplied child row |
| JRSP.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A validation, dependency, lookup, design, or boundary error occurs |
