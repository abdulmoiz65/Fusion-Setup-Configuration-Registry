# Configure Public Worker Access Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Configuration identity | Configuration Name and requested create, update, or delete operation | Stop | Supply a unique Name for a create, or the exact existing Name for an update or delete. This task does not support configuration renames because the documented lookup contract has no stable configuration identity other than Name. | Creating, updating, or deleting a configuration | verify_pwa_configuration_name_availability |
| Access design | One documented access scenario | Stop | Select an enterprise, legal-employer, business-unit, or other-inclusion scenario | Creating or updating a configuration | |
| Role-based FSM package structure | A current Fusion task template; use a Fusion-exported working PWA package as additional structural reference when one exists | Stop | For a first configuration with no existing PWA, use the current template and the documented PublicWorkerAccessAssignmentMigration and PublicWorkerAccessDetailMigration child structure. A working export may inform package review but is not required | Creating or updating a role-based configuration | |
| Child parent linkage | Parent Name and child rows in the same current-template package | Stop | Build the parent, detail, and role rows in one package. Populate ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name on every child with the exact parent Name. When the current template supplies a GroupingKey value, preserve that supplied value on the parent and every child; do not require an exported parent or generate a value independently | Creating or updating a package with detail or role rows | |
| Criteria values | Criterion type and one or more approved values when criteria are used | Stop | Obtain approved values and map only fields supported by the current template | Creating or updating criteria | |
| Business-unit criterion | Approved business unit Name and supported current-template row | Stop | When needed, browse active business-unit candidates, select one, then resolve the exact active business unit before package generation | A business-unit criterion is used | resolve_business_unit_by_exact_name |
| Department criterion | Approved department Name and, when needed, SetCode | Stop | Resolve the exact active and current department before package generation | A department criterion is used | resolve_department_by_name_and_set |
| Grade criterion | Approved grade Name and, when needed, SetCode; GradeCode only when Name is absent | Stop | Resolve the exact active and current grade before package generation | A grade criterion is used | resolve_grade_by_exact_name |
| Person criterion | Approved DisplayName, PersonNumber, or WorkEmailAddress | Stop | Resolve one PWA-scoped person before package generation | A person criterion is used | resolve_person_by_workers_finder |
| Job criterion | Approved job Name and, when needed, JobCode and SetName | Stop | Resolve exactly one job before package generation | A job criterion is used | resolve_job_by_exact_name_and_set |
| Legal-employer criterion | Approved legal employer Name | Stop | When needed, browse current legal-employer candidates, select one, then resolve exactly one legal employer before package generation | A legal-employer criterion is used | resolve_legal_employer_by_exact_name |
| Assignment-status criterion | Approved AssignmentStatusCode and selected UserStatus label | Stop | Browse suspended candidates when needed, then resolve exactly one assignment status by code before package generation | An assignment-status criterion is used | resolve_assignment_status_by_user_status |
| Person-type criterion | Approved UserPersonType and, when needed, System Person Type Code | Stop | Resolve exactly one person type before package generation | A person-type criterion is used | resolve_person_type_by_user_person_type |
| Role assignment | Approved role Name and, when needed, RoleCode | Stop | Resolve one active role before package generation | A role assignment is used | resolve_assignee_by_exact_role_name |
| Role availability | Approved active RoleName, RoleCode, and target configuration Name | Stop | Verify the selected role is not assigned to another PWA configuration before package generation | A role assignment is used | verify_role_unassigned_for_pwa |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|---|---|
| A profile option value is optionally retrieved as N, M, or Y | Informational | Present the returned mode and its supported design. Continue package preparation using the requested design and its applicable role, criterion, and package validations | verify_public_worker_access_profile_option |
| The effective profile value is unavailable | Valid | Continue package preparation. Do not infer a profile value or block solely because the optional lookup did not return an effective-session value | verify_public_worker_access_profile_option |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Configuration Name availability | For a create, require no exact configuration Name match. For an update or delete, require exactly one exact existing Name match. Reject a rename request. | Creating, updating, or deleting a configuration | verify_pwa_configuration_name_availability |
| Duplicate criterion rows | Reject duplicate rows that use the same criterion in one exclusion set | Creating or updating criteria | |
| Inclusion and exclusion overlap | Reject a design that uses the same criterion type in both sets | Creating or updating criteria | |
| Parent criterion flag | Allow N, I, or E only; match the selected criterion and intended scope | Preparing supported criterion data | |
| Child scope | Allow I or E only; use the approved intended scope | Preparing supported criterion data | |
| FSM package members | Require ASM_SETUP_CSV_METADATA.xml plus the PWA parent, detail, and roles CSV members; use the current task-template metadata | Preparing a Data Loader ZIP | |
| FSM export metadata evidence | Inspect ASM_SETUP_CSV_METADATA.xml before using an FSM task CSV export as the current template. Confirm that the exported task identity, task object type, and export process type match this task; confirm every exported business object, its ordered field and type contract, child-node sequence, and the batch and service contract | Validating an FSM task CSV export | |
| FSM export process status | Accept COMPLETED as export evidence. When the metadata reports COMPLETED_WARNINGS, surface every warning and require review before using the export as a package template; do not treat it as unconditional success | Validating an FSM task CSV export | |
| FSM export evidence scope | Retain only reusable contract evidence from ASM_SETUP_CSV_METADATA.xml: task identity, business objects, field contracts, node sequence, batch/service contract, and process status. Do not copy environment, submitter, timestamps, ESS request IDs, process IDs, or generated identifiers into reusable guidance or a new package | Validating an FSM task CSV export | |
| Current-template CSV mapping | Build every parent, detail, and role row by the current task template's header names, then emit cells in that exact header order. Preserve every template column and emit one empty cell only when that documented field is optional and intentionally blank. Reject a missing, extra, or positional-only column, including an omitted trailing empty cell | Preparing a Data Loader ZIP | |
| CSV header and row field count | Require each CSV header to match its current task-template member and every parsed data row to contain exactly the same number of fields as that header. Report the member, row, expected count, actual count, and affected header name before ZIP creation | Preparing a Data Loader ZIP | |
| Role child view instance | Require every role row to use PublicWorkerAccessAssignmentMigration, not the parent PublicWorkerAccessMigration view-instance name | A role assignment is included | |
| Detail child view instance | Require every detail row to use PublicWorkerAccessDetailMigration, not the parent view-instance name | A detail criterion is included | |
| Child parent linkage fields | Require every detail and role row to populate ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name with the exact parent Name. Reject a blank or mismatched parent Name before ZIP creation. When the current template supplies a GroupingKey value, preserve it identically on the parent and every child; do not block a new one-package configuration because no exported parent GroupingKey exists | A role or detail row is included | |
| Empty detail file | Permit the current-template header-only detail CSV for View All when no detail criteria are selected; do not fabricate a dummy child criterion | A View All package has no detail criteria | |
| Own-legal-employer CSV flags | Require the verified pair SecureByLegalEmployer=N and SecureByUserLegalEmployer=Y; reject either value or the pair when it differs before ZIP creation | An own legal employer scenario is prepared | |
| SecureBy parent-field domains | For every populated parent CSV field named SecureBy, validate it against its documented field domain before ZIP creation. Criterion-scope fields allow N, I, or E only; SecureByAsgnStatus is a criterion-scope field and must be N, I, or E, not Y or N. Boolean and scenario-specific SecureBy fields must match their documented field-specific mapping; reject an unknown field domain | Preparing a Data Loader ZIP | |
| Parent-link validation evidence | Validate a one-package parent-and-child example built from the current task template. Cover a valid linked child row and the negative blank or mismatched parent-name cases; when the template supplies GroupingKey, also cover preservation of that value. Do not require an authoritative mapping or a successful same-environment export | Maintaining PWA linkage validation | |

## Scenario CSV Field Mapping

| Scenario | SecureByLegalEmployer | SecureByUserLegalEmployer | Parent Scope | Required Detail Row | If Incomplete or Inconsistent |
|---|---|---|---|
| Own legal employer | N | Y |  |  | Reject the package before ZIP creation. Correct both CSV fields to this verified mapping, then rebuild the preview and obtain fresh approval if the ZIP changed |
| Assignment-status exclusion |  |  | SecureByAsgnStatus=E | One PublicWorkerAccessDetailMigration row using ORA_SEC_CRIT_ASGN_STATUS and the selected resolved assignment-status value | Reject the package before ZIP creation. Correct the parent scope and detail row together, then rebuild the preview and obtain fresh approval if the ZIP changed |
| Other inclusion |  |  | Use only the selected current-template parent fields | Add only the detail rows supported by the current template and selected criteria | Do not block pending an authoritative Other Inclusion CSV mapping. Validate the current-template headers, field domains, row counts, and parent-child linkage before ZIP creation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWA.VALIDATE_INPUT | decision | 1 | validate_input | valid->PWA.VERIFY_CONFIGURATION_NAME;invalid->PWA.BLOCKED | none | stop | A Data Loader create, update, or delete package is prepared |
