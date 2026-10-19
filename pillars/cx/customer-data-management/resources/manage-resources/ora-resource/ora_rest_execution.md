# ResourceUser Import and Export Execution

## Runtime Sources

Every delegated Fusion REST request in this execution contract must include
`Rest-Framework-Version: 9` where the selected core contract requires it.

| Source | Purpose |
|---|---|
| `core.data-loader` | Owns ResourceUser CX Import processing only; this task does not route one-resource REST Data Loader writes. |
| `core.data-loader.task-hook` | Owns the task-validation preview, approval, and archive-SHA verification lifecycle for a task-routed load. |
| `core.fusion-api.cx-import-export-management` | Owns ResourceUser Export Management creation, activation, polling, and download only. |
| `core.fusion-api.rest-api-client` | Owns role, parent ResourceUser, active tree-version, direct reportees, and single-resource read-only lookups. |
| `cx.customer-data-management.resources.run-reporting-hierarchy-generation` | Owns Reporting Hierarchy Generation ESS preview, CrmEss contract, final tree validation, submission, and tracking after a structured handoff. |
| `core.fusion-api.ess-job-submitter` | Owns the eligible, separately approved Send Pending LDAP Requests submission. |

## CX Import Execution Contract

| Situation | What Happens |
|---|---|
| CX ZIP or direct CSV group is supplied | Route to `core.data-loader` with `--cx-import`; use one ZIP source or repeated `--ide-file` CSV inputs. Do not call Import Management REST endpoints. |
| Valid CX mapping CSV is present | Use its authoritative `IMPORT OBJECT`; reject a conflicting caller object code. |
| Mapping CSV is absent | Default the Manage Resources CX Import object code to `ResourceUser` and invoke Data Loader with `--cx-import-object-code ResourceUser`. Do not override an explicit different object code; stop for clarification instead. |
| Preview or approval is prepared | Require Data Loader's read-only `objectMetadata/ResourceUser?fields=UcmAccount&onlyData=true` lookup. Use the returned nonblank `UcmAccount`; do not hard-code `crm/employeeResource/import/` or accept a caller UCM account. |
| Task-local rules pass | Use Task Hook `build-data-load-preview`, then, after explicit approval, `approve-data-load-preview` and `verify-approved-data-load-archive`. Pass the returned envelope unchanged with `--task-routed --task-validation-envelope`. |
| Live import is approved | Revalidate the exact immutable source and approved SHA-256, then invoke Data Loader with `--cx-import --approve-upload --approved-sha256`. Upload the mapping CSV first and data files in original order; stop before initiation on any upload failure. |
| Initiation is accepted | Return the Data Loader request ID. Do not poll automatically and do not classify initiation as a completed import. |
| Status, results, counts, or errors are requested | Delegate to Data Loader's status route, which retrieves the data-set and error information. Only a successful completed status may enter post-import ESS evaluation. |
| Import source supplies ResourceOrgRoleCode, IndividualRoleCode, or ResourceOrgManagerEmail | Select the first 10 non-header CSV rows before any REST lookup. Resolve only sampled role codes and external manager emails; block unresolved or inconclusive results and require confirmation before proceeding beyond the sample. |

## Export and Post-Import Execution

| Situation | What Happens |
|---|---|
| Export request is prepared | Delegate to `core.fusion-api.cx-import-export-management` with `ExportObject=ResourceUser`, a unique name, top-level filter, optional fields, activation choice, and optional output path. |
| Export result is complete | Delegate polling and ZIP download to the export core skill, then review the requested output. |
| Reporting Hierarchy Generation is eligible | Resolve exactly one active/current `fndTreeVersions` row, then send a structured preview handoff to `cx.customer-data-management.resources.run-reporting-hierarchy-generation` containing the successful import evidence, target environment context, `tree_structure_code=RESOURCE_ORG_TREE_STRUCTURE`, `tree_code=GLOBAL_SALES_MARKETING`, validated `tree_version_id`, and `submit=true`. Manage Resources must not build or submit a Reporting Hierarchy ESS payload; the receiving skill owns the CrmEss preview, ordered parameters, final validation, submission, and polling. After the preview, pass the fresh approved Reporting Hierarchy item as the receiving skill's `execution_approval`. |
| Send Pending LDAP Requests is eligible | Present the exact post-import ESS preview and require fresh `post_import_ess_execution_approval` before delegated submission and polling. |
| Both ESS processes are eligible | Submit both independently and poll each returned request ID independently. |
| resource_user_get has one exact ResourceEmail or ResourcePartyNumber and no mutation intent | Resolve one complete visible Resource User through core.fusion-api.rest-api-client, return only requested authorized fields, and stop. Do not enter Data Loader, preview, approval, ESS, or hierarchy generation. |
| One-resource create, update, promotion, demotion, transfer, or end-date has no CSV or CX ZIP source | Stop. Do not invoke Resource Users REST Data Loader or direct Resource Users POST/PATCH; request a supported ResourceUser CX Import source for create or update. |
| Direct reportees are requested | Resolve one exact manager ResourceEmail or PartyName, then query Resource Users by the resolved ResourceOrgManagerEmail. Retrieve every page, retain only current matches, and return an empty list when none match. Do not call core.data-loader or initiate any write, preview, approval, ESS, or hierarchy action. |
| ResourceUser DELETE is requested | Stop. Explain that permanent deletion is unsupported. A requested resource end-date also has no one-resource write route; use a supported ResourceUser CX Import source only if its documented mapping covers the intended change. |

## Preview and Live Gates

| Step | Requirement |
|---|---|
| 1 | Complete mapping, first-10-row role/manager validation, and dependency-order validation before the Data Loader preview. |
| 2 | Run the Data Loader CX Import preview without `--approve-upload`, then build the Task Hook preview from the exact final archive SHA-256 and ordered rule results. |
| 3 | Present the target environment, object code, metadata-derived UCM account, immutable source digest, and exact Data Loader route. Obtain explicit approval immediately before approving the Task Hook preview. |
| 4 | Verify the approved Task Hook envelope against the final archive, then execute one approved Data Loader initiation. A changed source, mapping, or archive requires a new preview and approval. |
| 5 | Do not automatically poll. On an explicit status request, use the Data Loader status route; only a confirmed completed success may be evaluated for post-import ESS work. |
| 6 | For export, retain the existing Export Management dry-run, approval, activation, polling, and ZIP-download gates. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_PREVIEW | step | 11 | preview_gate | reviewed->MR.IMPORT_APPROVE | MR.IMPORT_DESIGN | stop | The Data Loader CX preview and Task Hook preview use the exact immutable source and final archive SHA-256. |
| MR.IMPORT_APPROVE | decision | 13 | approval_gate | approved->MR.IMPORT_SUBMIT;declined->MR.STOP | MR.IMPORT_PREVIEW | stop | A live Data Loader initiation is requested. |
| MR.IMPORT_SUBMIT | step | 15 | execution_gate | submitted->MR.IMPORT_RESULT | MR.IMPORT_APPROVE | stop | The approved source, SHA-256, and task-validation envelope are revalidated immediately before one Data Loader initiation. |
| MR.EXPORT_PREVIEW | step | 12 | preview_gate | reviewed->MR.EXPORT_APPROVE | MR.EXPORT_DESIGN | stop | Export name, filter, fields, and output settings are reviewed. |
| MR.EXPORT_APPROVE | decision | 14 | approval_gate | approved->MR.EXPORT_SUBMIT;declined->MR.STOP | MR.EXPORT_PREVIEW | stop | A live export action is requested. |
| MR.EXPORT_SUBMIT | step | 16 | execution_gate | submitted->MR.EXPORT_RESULT | MR.EXPORT_APPROVE | stop | Explicit approval was obtained for export. |
| MR.POST_IMPORT_PREVIEW | step | 24 | preview_gate | ready->MR.POST_IMPORT_APPROVE | MR.LDAP_VALIDATE | stop | Every eligible post-import process has passed validation and readiness; obtain the Reporting Hierarchy ESS preview from its receiving skill and show the local LDAP preview. |
| MR.POST_IMPORT_APPROVE | decision | 25 | approval_gate | approved->MR.POST_IMPORT_SUBMIT;declined->MR.STOP | MR.POST_IMPORT_PREVIEW | stop | Fresh post_import_ess_execution_approval identifies the eligible post-import ESS job or jobs to submit. |
| MR.POST_IMPORT_SUBMIT | step | 26 | execution_gate | submitted->MR.POST_IMPORT_RESULT | MR.POST_IMPORT_APPROVE | continue | Pass an approved Reporting Hierarchy handoff to its receiving skill and submit only the currently approved local LDAP ESS job; track returned requests independently. |
| MR.DONE_REPORTEES | terminal | 34 | terminal | none | MR.REPORTEES_LOOKUP | stop | The complete current direct-reportees list, including an explicit empty list when no current match exists, is returned from the read-only branch. |
| MR.DONE_GET | terminal | 53 | terminal | none | MR.GET_LOOKUP | stop | One complete exact Resource User was found and only the requested authorized fields were returned from the read-only branch. |
| MR.DONE_IMPORT_NO_ESS | terminal | 28 | terminal | none | MR.POST_IMPORT_ROUTE | stop | The import is complete and no post-import ESS process is eligible. |
| MR.DONE_IMPORT_ESS | terminal | 29 | terminal | none | MR.POST_IMPORT_RESULT | stop | The import and all eligible ESS processes completed successfully. |
| MR.DONE_EXPORT | terminal | 30 | terminal | none | MR.EXPORT_RESULT | stop | The export result is complete and the requested ZIP is downloaded. |
