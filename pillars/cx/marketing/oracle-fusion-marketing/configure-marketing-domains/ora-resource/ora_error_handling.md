# Error Handling

The task graph ends at DOMAINS.VALIDATION_READY before approval. It does not
authorize an upload. After successful Task Hook validation, core.data-loader
owns the immutable preview, explicit approval, upload, and initiation. The
post-validation disclosure and refusal rules below govern that handoff and
its caller continuation; they do not require prior approval during validation.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input validation, catalog mismatch, auth/authz, transport/environment, or Fusion API failure | Preserve the selected domain, disclose the failure class and recommended next action, and do not claim success. |
| Data Loader validation, upload, or initiation failure | Preserve the selected domain, disclose the failure class and recommended next action, and require a fresh immutable source and approval before another load. |
| Post-load read-back mismatch | Wait 30 seconds and read the complete selected record again. If it still differs, prepare a fresh source and obtain explicit approval for one retry only. |
| Declined Data Loader preview | No upload was initiated. Retain the selected domain, return to DOMAINS.COLLECT_CHANGES if the user wants revisions, and repeat preparation and validation for a changed artifact. Cancel the pending update if requested. |
| Ambiguous Data Loader approval | No upload was initiated. Let core.data-loader clarify approval of the same exact preview; do not add a task-local approval gate or reuse approval for a changed artifact. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Selected record | Unredacted Section, Field, Current Value table: Domain (Primary Domain, DNS Status); Domain Settings (every enabled preference); Default Headers (all five header fields). |
| Approval preview | After task validation, core.data-loader presents the proposed user-facing field changes and immutable sparse Data Loader preview and obtains explicit approval exactly once before upload and initiation. |
| Declined preview | No upload was initiated. Retain the selected domain and offer revision of the proposed changes or cancellation of the update. |
| Ambiguous approval | No upload was initiated. Ask for a clear approval or decline of the exact preview. |
| Accepted load | Wait 30 seconds, then render the complete selected record from the read-back GET, including every enabled preference and all five Default Headers fields, in the final response after the unchanged core initiation report and with an explicit verification outcome. Commentary alone is insufficient. |

## Post-load Final Response

The caller applies the task's Marketing Final Response contract after accepted
initiation. Preserve the core initiation report verbatim, then display the
verification outcome and full record in the final response, not only commentary.

| Outcome | Final Response |
|---|---|
| Matched | State "Updated values verified" only when every approved changed field matches the fresh read-back; include the complete record in the final response. This confirms field values, not asynchronous Data Loader job completion. |
| Mismatch | State "Update not yet verified"; include the latest complete record and requested-versus-observed values after the bounded read-back attempts. Do not claim success or retry automatically; at most one mutation retry requires a new immutable preview and fresh approval. |
| Unavailable | State "Verification unavailable"; retain the accepted initiation report and explain the read failure or ambiguous selection. Do not present a stale record as current or resend the load; offer a read-only verification retry. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing approval or a changed preview | Do not upload or initiate a Data Loader request. |
| Declined or ambiguous approval | Do not upload or initiate a Data Loader request, discard the pending preview on cancellation, and retain the selected domain for revision or clarification. |
| Selected-record or read-back display | Do not redact approved response fields or display record IDs, self links, ETags, or If-Match values. Do not persist displayed values in project artifacts. |
| Undocumented execution detail | Do not infer query parameters beyond $limit and $offset, response fields, authentication, endpoints, request fields, or rollback behavior. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOMAINS.AWAITING_SELECTION | terminal | 4 | terminal | none | DOMAINS.LIST_SELECT | stop | The complete domain list is displayed and the required exact primaryDomain selection prompt has been asked |
| DOMAINS.VALIDATION_READY | terminal | 9 | terminal | none | DOMAINS.PREVIEW | stop | All task checks passed for the immutable artifact; return validation evidence to Data Loader for its preview and approval workflow. No upload or initiation is authorized by this terminal. |
| DOMAINS.AWAITING_CHANGES | terminal | 10 | terminal | none | DOMAINS.COLLECT_CHANGES | stop | The complete selected-domain record is displayed and the user has supplied no changes yet |
| RETURN_ISSUES | terminal | 12 | terminal | none | none | stop | A validation, lookup, preview, approval, Data Loader, or read-back issue occurs |
