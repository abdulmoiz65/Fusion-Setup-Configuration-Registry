# Change Line DFF Rule Results

Input and design resources own validation conditions and corrections. Return their precise findings rather than repeating those rules here. Core/shared workflows own authentication, approvals, transport, timeouts and retries; this resource retains task-specific diagnosis and verification outcomes. The graph authorizes no import or deployment.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A task-rule check fails | Return the failed rule and sanitized missing or conflicting evidence; do not make a corrective Fusion write |
| Shared artifact validation finds an existing-name conflict, occupied or incompatible column, incompatible value set, or missing metadata | Preserve the original baseline, return the owning shared validation finding and request the missing evidence or reviewed correction; do not overwrite setup, invent capacity, or substitute an unverified lookup |
| Validation, import or deployment reports that a segment or Context being disabled is in use or referenced elsewhere | Show the actual returned error text and error code, if present, including reported dependent objects after necessary sensitive-data redaction. Identify the affected Context/segment, stage and diagnostic evidence. Do not replace it with a generic failure, claim all dependencies were discovered, or invent a cause. Stop the operation; do not force, cascade changes, retry automatically or deploy after a failed/uncertain import. Ask for direction on the reported dependency; any remediation needs its own reviewed scope and approvals |
| Disable import/deployment completed but read-back is absent or differs | Report verification pending or failed separately from job completion. Require the exact selected definitions to remain present with EnabledFlag N and preserved non-target properties; do not claim deletion, runtime verification or historical-data preservation from a job status alone |
| Context disable read-back changes a child's EnabledFlag/definition or leaves the selected Context enabled | Report preservation or intended-state verification failure even if jobs succeeded. Preserve the evidence and stop; do not report successful Context disable, auto-correct the child or automatically re-enable the Context |
| A deployment-job status lookup before baseline export is absent, inconclusive or reports no submitted request | Report the exact response as deployment-job diagnostics, not as proof of current saved-metadata deployment state. In particular, ERROR with no job ID and a not-submitted message must not independently block an approved task-level baseline export or trigger automatic deployment. Apply the shared export's own identity, eligibility, authentication and approval checks; do not add a mandatory status lookup or an override requirement |
| A submitted deployment job fails or its outcome is pending or unknown | Preserve the actual status, message and job evidence through the shared deployment workflow. Do not apply the no-submitted-request interpretation to an actual deployment failure, report deployment success or retry a write automatically |
| Current-data export completes but contains no affected DFF definition or only header rows | Stop before candidate preparation. Retain ProcessId, request ID, package scope, CSV row counts and ProcessLog; verify actual data mode and requested criteria through the existing shared routes. Interpret any available deployment-job diagnostics separately; neither DEPLOYED nor a missing job record establishes current baseline completeness or the cause of missing rows. A completed job or a zero-row result does not prove that the Context was deleted or that the export was a template. Compare a known-good package when available; do not reuse a stale baseline or automatically resubmit |
| All applicable task-rule checks pass | Return validation results to the invoking workflow; this does not mean an import or deployment has run or been approved |
| Shared deployment reports successful completion | Record the result and evidence for the exact imported DFF and environment; verify intended settings before claiming end-to-end success. Attribute any user-supplied evidence to the user rather than claiming independent verification |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLDFF.RETURN_READY | terminal | 50 | terminal | none | CLDFF.DESIGN | stop | All applicable task rules passed; return results without authorizing a mutation |
| CLDFF.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A rule fails or required evidence is missing |
