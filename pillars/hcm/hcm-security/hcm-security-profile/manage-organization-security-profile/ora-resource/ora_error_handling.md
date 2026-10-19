# Organization Security Profile Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required scope details are missing | Stop and request hierarchy, classification, or organization-list details |
| A profile Name is unavailable or ambiguous | Stop before preview, CSV package generation, or import. For a rename, verify the old exact Name and supplied current ID first, then require zero exact matches for the proposed new Name. |
| A genuine rename has an available new Name | Report `rename CSV identity mapping unverified` and stop before CSV preview or import. Do not infer parent or child update keys from REST IDs or name-based GroupingKey fallbacks. |
| Security-criterion selection or change scope is missing | Stop before reference discovery and request the selected or not-selected state of each applicable hierarchy, classification, and organization-list criterion, plus whether the request is profile-only or authorizes reference-data changes |
| Hierarchy, classification, or organization-list inputs are supplied without their selected criteria | Stop before criterion-specific REST lookup. Confirm which criteria are selected; do not treat multiple selected criteria as conflicting alternatives. |
| A named top organization is invalid | Stop and correct the selection |
| Profile-only scope would create or modify reference data | Stop. Use only existing reference values; do not create or modify an organization, Department, tree, or other reference record from this task. |
| An organization-hierarchy CSV using a Department Tree has a blank or mismatched TopOrganizationName or TopOrganizationId | Stop before preview or import. Re-resolve the selected Department node and rebuild the CSV only from the resolver's complete output. |
| A request describes department from the user's assignment | Use TopOrgSelection=U as the hierarchy-top source. Confirm IncludeTopOrganizationFlag separately because it controls inclusion of the top organization and is not implied by U. |
| FSM export metadata is missing, malformed, identifies another task, or has a changed business-object, field, batch, service, or object-order contract | Stop before package preparation. Export the task again and validate its ASM_SETUP_CSV_METADATA.xml before using it as a baseline. |
| The current template-only export cannot resolve an unambiguous CSV member, header, mapping, parent-child linkage, metadata byte, or node order | Stop before preview or import. Export a fresh template-only package and rebuild every CSV row only from the resolver output. A missing ViewInstanceName or GroupingKey pattern alone uses the documented member-specific fallback. Do not use a hard-coded CSV column list. |
| FSM export ProcessStatus is COMPLETED_WARNINGS | Do not treat the export as an unconditional success. Surface COMPLETED_WARNINGS, review the associated export warnings, and resolve or explicitly accept them before using the export as a package baseline. |
| A Data Loader import is accepted | Report status as Processing, not success. Return the Request ID and data set name, state that completion is unverified, and direct the user to check the process log or import status later. Do not poll automatically. |
| A programmatic create, update, upsert, or delete is requested | Stop: base organizationSecurityProfiles REST is used only to review its input contract, and organizationSecurityProfilesLOV is used only for existing-profile lookup. Prepare the approved task-level CSV package and use core.data-loader; verify the import through its process log. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct REST mutation is requested | Do not submit POST, PATCH, PUT, or DELETE to organizationSecurityProfiles. Do not submit a CSV package until its exact preview has approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORG.EXECUTION_CONTRACT | step | 19 | execution_gate | accepted_processing->ORG.IMPORT_PROCESSING;process_log_success->ORG.DONE;missing_or_direct_rest->ORG.RETURN_ISSUES | ORG.ENFORCE_DESIGN | stop | A create or update uses an approved task-level CSV import through core.data-loader |
| ORG.IMPORT_PROCESSING | terminal | 20 | terminal | none | ORG.EXECUTION_CONTRACT | stop | Data Loader accepted the import and returned a Request ID and data set name, but no successful process log is available yet. Return Processing with those values and the next action: check import status or process log later. |
| ORG.DONE | terminal | 21 | terminal | none | ORG.EXECUTION_CONTRACT | stop | The approved import process log confirms successful completion |
| ORG.RETURN_ISSUES | terminal | 22 | terminal | none | none | stop | A task rule returns an issue |
