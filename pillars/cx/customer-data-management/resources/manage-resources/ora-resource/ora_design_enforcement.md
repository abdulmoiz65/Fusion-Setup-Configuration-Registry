# ResourceUser Import and Export Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Conditional HCM guidance | State the Oracle guidance as conditional guidance for an environment with a full HCM Services implementation; do not infer the implementation scope. |
| 2 | HCM guidance display | Display the conditional guidance as information, then continue to import preview without a separate confirmation. |
| 3 | Prerequisite check | After mapping, verify BusinessUnit and LegalEntity values from only the first 10 non-header rows through their documented exact live lookups, then verify supplied resource role codes through the active Resource Roles REST lookup. |
| 4 | Unsupported import scope check | Stop requests for documented unsupported Resource Users scopes. |
| 5 | Export scope check | Confirm the export has a top-level ResourceUser filter and caller-selected fields. |
| 6 | Post-import ESS scope check | Determine independently whether successful import rows changed hierarchy data or created resources with user accounts. |
| 7 | Post-import ESS approval check | Present each eligible process with its exact target, job definition, application, and parameters; require fresh approval after the import result. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| MR.HCM_SCOPE | Resource Users import is requested | Warning | None | Do not infer whether the environment has a full HCM Services implementation. If it does, Oracle recommends using Resource Users import or REST only to convert existing HR workers into resources. The Resource Users REST API supports only basic HR person/worker attributes and does not support HCM custom attributes defined on HR Person/Worker. | Display the conditional guidance as information and continue to import preview. The existing import approval remains required before submission. | Yes |
| MR.PREREQUISITES | Source CSV contains resource setup references | Blocker | Sampled BusinessUnit, LegalEntity, and active Resource Roles verification | A BusinessUnit value lacks exactly one exact `hcmBusinessUnitsLOV` match, a LegalEntity value lacks exactly one exact current-effective `legalEmployersLov` match, a ResourceOrgRoleCode or IndividualRoleCode from the first 10 rows is not returned by the active Resource Roles lookup, or prerequisite setup is absent | Complete prerequisite setup, activate the Resource Role, or correct the CSV. Inspect only first-10 sampled values, use no word search or closest-match selection, and record that later rows are outside the reference-validation sample. | Yes |
| MR.ROLE_ROUTING | Source CSV supplies Role | Blocker | Organization, role, and role-designation review | Role is supplied without Organization or explicit individual-role designation | Provide Organization to map Role to ResourceOrgRoleCode, or explicitly designate the role as individual to map it to IndividualRoleCode. | Yes |
| MR.PARENT_ORDER | Source CSV contains parent and dependent ResourceUser rows | Blocker | Source row-order review | A parent row is absent or appears after a row that references it | Add the parent record or move its row before every dependent row. | Yes |
| MR.UNSUPPORTED_IMPORT_SCOPE | Resource Users import is requested | Blocker | Requested change-scope review | Request creates a standalone worker, loads a worker only, loads Resource Team membership, or relies on automatic re-parenting | Use the documented HCM or supported resource process, or change the request scope. | Yes |
| MR.EXPORT_FILTER | ResourceUser export is requested | Blocker | Export activity review | A unique activity name, top-level-object filter, or caller-selected field scope is missing | Supply the missing export definition before preview. | Yes |
| MR.EXPORT_VISIBILITY | ResourceUser export selects fields | Warning | Existing role and data-security review | Requested objects or PII fields are not visible to the caller | Export only fields available under the current roles and data-security policy; do not change security configuration from this task. | No |
| MR.RH_ESS_APPROVAL | Reporting Hierarchy Generation is eligible | Blocker | fndTreeVersions review, complete receiving-skill preview handoff, and fresh post-import approval before execution | Required privilege is unavailable, no Tree Version row is both ACTIVE and current-effective, more than one row is eligible, the preview handoff lacks required current-request values, or the returned preview lacks fresh post_import_ess_execution_approval at execution time | Resolve the unambiguous current-effective Tree Version and hand off the exact target, tree triple, import evidence, and submit intent to Run Reporting Hierarchy Generation. Obtain fresh approval only after its preview, then pass it as execution_approval. Do not construct a local CrmEss payload or perform a Scheduler active-instance lookup. | Yes |
| MR.LDAP_ESS_APPROVAL | Send Pending LDAP Requests is eligible | Blocker | Fixed ESS request-contract review and fresh post-import approval | Required privilege is unavailable, the fixed ESS request contract is incomplete, or fresh post_import_ess_execution_approval is absent | Restore the fixed request contract and obtain approval for the exact target, job definition, application, and parameters. Do not perform a Scheduler active-instance lookup. | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| MR.HCM_SCOPE | Informational guidance | Before Resource Users import preview | Conditional full-HCM Services guidance text | Oracle Import Your Resource Data guide |
| MR.PREREQUISITES | Sampled BusinessUnit and LegalEntity exact REST lookups and sampled active Resource Roles REST lookup | Before preview | First-10 mapped BusinessUnit and LegalEntity values, sampled IndividualRoleCode, sampled ResourceOrgRoleCode, active RoleCode values | Caller-supplied first-10 sample-validation contract, Oracle Import Your Resource Data guide, HCM LOV REST APIs, and Resource Roles REST API |
| MR.ROLE_ROUTING | Role-routing review | Before import preview | Organization, Role, and explicit individual-role designation | Caller-supplied ResourceUser role-routing rule |
| MR.PARENT_ORDER | Parent-row order review | Before import preview | Parent references and source row order | Caller-supplied ResourceUser dependency-order rule |
| MR.UNSUPPORTED_IMPORT_SCOPE | Requested change-scope review | Before import preview | HCM implementation status and requested Resource Users scope | Oracle Import Your Resource Data guide |
| MR.EXPORT_FILTER | Export activity review | Before export preview | Activity name, ResourceUser top-level filter, selected fields | Oracle Export Data guide |
| MR.EXPORT_VISIBILITY | Existing role and data-security review | Before export preview | Visible ResourceUser fields and requested PII fields | Oracle Export Data guide |
| MR.RH_ESS_APPROVAL | fndTreeVersions review and post-import approval review | Before post-import submission | Status, EffectiveStartDate, EffectiveEndDate, Tree Version ID, configured job definition, caller privilege, and post_import_ess_execution_approval | `ora_reference_lookups.md` and Oracle Reporting Hierarchy Generation guide |
| MR.LDAP_ESS_APPROVAL | Fixed ESS request-contract and post-import approval review | Before post-import submission | Configured job definition, fixed ESS request contract, caller privilege, and post_import_ess_execution_approval | Oracle Send Pending LDAP Requests guide |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_DESIGN | decision | 9 | design_enforcement | pass->MR.IMPORT_PREVIEW;blocked->MR.STOP | MR.IMPORT_BULK | stop | A validated ResourceUser import is ready for preview. |
| MR.EXPORT_DESIGN | decision | 10 | design_enforcement | pass->MR.EXPORT_PREVIEW;blocked->MR.STOP | MR.EXPORT_VALIDATE | stop | A validated ResourceUser export is ready for preview. |
