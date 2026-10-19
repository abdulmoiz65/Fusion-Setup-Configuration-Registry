# ResourceUser Import and Export Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required attributes, prerequisite values, or parent records are missing | Stop before submission and correct the source, prerequisite setup, or parent-row order. |
| CSV has unmapped columns or data format issues | Correct the source after validation and rerun preview. |
| A BusinessUnit value sampled from the first 10 rows has zero or multiple exact matches | Block before submission. Report the de-duplicated sampled value and affected source row numbers; correct the CSV and rerun the one `hcmBusinessUnitsLOV` lookup. |
| A LegalEntity value sampled from the first 10 rows has zero or multiple exact current-effective matches | Block before submission. Report the de-duplicated sampled value and affected source row numbers; correct the CSV and rerun the one `legalEmployersLov` lookup. |
| ResourceOrgRoleCode or IndividualRoleCode in the first 10 rows is unresolved | Block before submission. Report only the distinct unresolved sampled role codes and whether each was supplied as an organization or individual role; correct or activate the roles, then rerun the sampled live lookup. |
| BusinessUnit, LegalEntity, role code, or manager email appears after the first 10 rows | Do not perform a reference lookup. Inform the user that only the first 10 rows were validated and stop until explicit confirmation is provided to proceed for the remaining rows. |
| Import activity is not complete | Review the Import Status details before any retry. |
| A matching import may already exist | Stop and review the prior activity before resubmission. |
| Resource reporting hierarchy changed | After a successful approved import and readiness validation, present Reporting Hierarchy Generation with the documented internal-resource tree structure, tree code, and Tree Version ID; submit only after fresh post-import approval. |
| Reporting Hierarchy Generation preview handoff is incomplete or rejected | Stop the Reporting Hierarchy branch. Do not create a local CrmEss payload; correct the successful-import evidence, target environment context, exact tree triple, or submit intent and restart the receiving skill's preflight. After a returned preview, obtain fresh approval before passing execution_approval. |
| No or multiple current-effective active tree versions | Stop the Reporting Hierarchy Generation branch. Record the Status, EffectiveStartDate, and EffectiveEndDate for every candidate; do not choose a version arbitrarily. |
| New resource needs Manage Users search visibility | Run Update Person Search Keywords with After Batch Load set to Y. |
| Every imported row explicitly sets CreateUserAccountFlag to N | State that LDAP processing is suppressed because all imported rows set N; do not submit Send Pending LDAP Requests. |
| Any imported row omits CreateUserAccountFlag or has a value other than N | Ignore the suppression rule and, after successful approved import and readiness validation, present Send Pending LDAP Requests using the fixed verified ESS request contract. Submit only after fresh post-import approval; do not emit a flag-specific message. |
| Resource user GUID synchronization is needed after import | Run Synchronize User GUID. |
| Data Loader CX preview, Task Hook verification, metadata lookup, upload, or initiation fails | Stop at the failed stage. Do not substitute an Import Management call, hard-code a UCM account, retry a live upload, or initiate a partial CX file group. |
| Data load was initiated but completion status was not explicitly requested | Return the accepted request ID and direct the caller to request status; do not poll or submit post-import ESS work. |
| A completion check confirms a successful completed ResourceUser import | Do not end the result flow before validating post-import eligibility and readiness. Present every eligible ESS job and request fresh approval to submit it; do not submit a job until that approval is supplied. |
| Fresh post-import ESS approval is absent or declined | Do not submit the eligible ESS job. Present the exact target, application, job definition ID, and parameters again for approval. |
| One of the parallel ESS requests fails or is cancelled | Continue polling the other submitted request, then report both request IDs and terminal statuses; do not automatically resubmit either job. |
| Export activity is incomplete | Review the core job status and result before another request. |
| resource_user_get has zero, multiple, incomplete, unauthorized, or transport-error results | Stop the read-only branch. Do not return a partial result, infer a Resource User identity, or enter Data Loader. |
| Direct reportees manager lookup has zero, multiple, incomplete, unauthorized, or blank-email results | Stop. Do not query ResourceOrgManagerEmail, infer a manager email, or substitute a similarly named resource. |
| Direct reportees lookup is paginated, incomplete, unauthorized, or has a transport failure | Stop and report the read-only lookup failure. Do not return a partial first page, retry automatically, or substitute organization members or hierarchy descendants. |
| Direct reportees lookup returns no current matches | Return an explicit empty list. Do not treat it as a manager-identity failure. |
| One-resource create, update, promotion, demotion, transfer, or end-date is requested without a CSV or CX ZIP source | Stop. Do not use Resource Users REST Data Loader or direct Resource Users POST/PATCH. Request a supported ResourceUser CX Import source for create or update. |
| Standalone one-resource organization-membership change is requested | Stop. Do not recast it as a generic Resource User update; use ResourceUser CX Import only when the caller supplies a CSV source. |
| Permanent Resource User deletion is requested | State that DELETE is unsupported. If the caller instead intends an end-date, request a supported ResourceUser CX Import source with a documented mapping; do not convert the request automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Blocked | Pre-import validation or dependency check fails | Correct the issue and repeat preview. |
| Incomplete | Import activity does not report completion | Review Import Status details before retry. |
| Complete | Import activity reports completion | Determine applicable post-import ESS processes. |
| ESS blocked | An eligible process lacks required inputs, privilege, or fresh post-import approval | Correct the blocked condition before preview. |
| ESS partial failure | One independently submitted ESS request is unsuccessful | Finish monitoring the other request and stop before retry. |
| ESS complete | Every eligible post-import ESS request completes successfully | Record each request ID and terminal status. |
| Export complete | Export job completes and the ZIP file is available | Delegate the requested ZIP download and review the result. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Missing prerequisites, mapping issues, and data-format issues. |
| Conditional HCM guidance | State the Oracle recommendation only as conditional guidance for an environment with full HCM Services implementation. Do not state that the environment has that implementation, and continue to the normal import preview. |
| Result review | Import activity status and data-file totals. |
| Export result review | Export activity status and requested ZIP output location. |
| Post-import ESS audit record | Each eligible job purpose, target environment, job definition ID, exact parameters, fresh approval result, and parallel submission behavior. |
| Post-import ESS result review | Each submitted ESS request ID and terminal status. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Validation or dependency failure | Do not submit or retry the import. |
| An ESS job fails or times out | Do not retry automatically. Preserve the request ID and sanitized diagnostics, then require a new post-import preview and fresh approval before a later submission. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.STOP | terminal | 54 | terminal | none | none | stop | Validation, dependency, approval, execution, or result handling stops the selected workflow. |
