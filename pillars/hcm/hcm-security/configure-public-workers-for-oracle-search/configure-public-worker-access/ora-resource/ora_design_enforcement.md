# Configure Public Worker Access Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm Configuration Name availability | Require no exact existing Name match for a create, or exactly one exact unchanged Name match for an update. |
| 2 | Confirm scenario compatibility | Reject criteria that conflict with the selected inclusion scenario |
| 3 | Confirm enterprise scope | Confirm the design is appropriate for enterprise-wide behavior |
| 4 | Confirm security alignment | Review public person security profile alignment when Connections is used |
| 5 | Confirm one-package workflow | Require the current template, one complete parent-and-child preview, and approval before submission |
| 6 | Apply the requested PWA design | Require an active unassigned role for a role-based package; prohibit roles for an enterprise-level package. A profile lookup may be used to explain the current mode but is not required first |
| 7 | Confirm advanced-filter compatibility | Require a Rule Builder expression or filter and prohibit incompatible security options |
| 8 | Confirm nested FSM structure and linkage | Use the current Fusion task template and documented child view-instance names. Build the parent and child rows in one package, and require each child to reference the exact parent Name before approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A PWA configuration is created, updated, or deleted | Blocker | verify_pwa_configuration_name_availability | A create returns any exact Name match, an update or delete returns zero or multiple exact Name matches, or a rename is requested | Use a unique Name for a create or the exact existing Name for an update or delete. Use a separately supported route for a rename. | Yes |
| A role-based PWA package is prepared | Blocker |  | No active unassigned role is supplied before package preview | Select one active unassigned role, then continue with role-based criteria | Yes |
| A business-unit criterion is requested | Blocker | resolve_business_unit_by_exact_name | The active business unit cannot be resolved to one BusinessUnitId | Supply the approved business unit Name and rerun the resolver | Yes |
| A department criterion is requested | Blocker | resolve_department_by_name_and_set | The active and current department cannot be resolved to one OrganizationId | Supply the approved department Name and SetCode when required | Yes |
| A grade criterion is requested | Blocker | resolve_grade_by_exact_name | The active and current grade cannot be resolved to one GradeId | Supply the approved grade Name and SetCode when required | Yes |
| A person criterion is requested | Blocker | resolve_person_by_workers_finder | The worker finder returns zero or multiple PwaViewAll matches | Supply a display name, person number, or work email that resolves to one row | Yes |
| A job criterion is requested | Blocker | resolve_job_by_exact_name_and_set | The job lookup returns zero or multiple rows | Supply job Name and JobCode and SetName when required | Yes |
| A legal-employer criterion is requested | Blocker | resolve_legal_employer_by_exact_name | The legal-employer lookup does not return one OrganizationId | Supply the approved legal employer Name | Yes |
| An assignment-status criterion is requested | Blocker | resolve_assignment_status_by_user_status | The UserStatus lookup does not return one AssignmentStatusTypeId | Supply UserStatus and AssignmentStatusCode when required | Yes |
| A person-type criterion is requested | Blocker | resolve_person_type_by_user_person_type | The UserPersonType lookup does not return one PersonTypeId | Supply UserPersonType and System Person Type Code when required | Yes |
| A role assignment is requested | Blocker | resolve_assignee_by_exact_role_name | The role lookup does not return one RoleId | Supply role Name and RoleCode when required | Yes |
| An active role is selected for a PWA package | Blocker | verify_role_unassigned_for_pwa | The selected role is assigned to a different PWA configuration | Select another active role before package generation | Yes |
| A role-based PWA package is prepared | Blocker |  | No current Fusion task template is available, or the package does not meet the documented nested-FSM checks | Export the current task template. A Fusion-exported working PWA package is valid regression evidence when available. Use PublicWorkerAccessAssignmentMigration for roles and PublicWorkerAccessDetailMigration for details. Build the parent and child rows in one package, with every child referencing the exact parent Name; validate the package before approval | Yes |
| A new configuration includes detail or role rows | Blocker |  | A child row is missing or does not exactly match the parent Name | Include the parent, detail, and role rows in one current-template package. Set ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name on every child exactly to the package parent Name | Yes |
| A role assignment is included in a package | Blocker |  | The role row uses the parent view-instance name, does not use PublicWorkerAccessAssignmentMigration, or has blank or mismatched ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name | Use the documented nested role structure. Set the fully qualified parent-name field exactly to the package parent Name. Preserve a template-supplied GroupingKey unchanged when present; do not require an exported parent value | Yes |
| A detail criterion is included in a package | Blocker |  | The detail row uses the parent view-instance name, does not use PublicWorkerAccessDetailMigration, or has blank or mismatched ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name | Use the documented nested detail structure. Set the fully qualified parent-name field exactly to the package parent Name. Preserve a template-supplied GroupingKey unchanged when present; do not require an exported parent value | Yes |
| A View All design is prepared | Blocker |  | ViewAll is enabled with a selected exclusion but its supported detail row is absent, or a fabricated unsupported detail row is added | Retain selected exclusion flags, including SecureByUserLegalEmployer when selected, and their supported detail rows. Do not block ViewAll merely because exclusions are retained; use the current-template header-only detail CSV only when no detail criteria are selected | Yes |
| An enterprise-level PWA package is prepared | Blocker |  | More than one enterprise-level configuration is requested or any role is supplied | Retain one enterprise configuration without roles | Yes |
| A DFF attribute is used in a Rule Builder rule | Blocker | verify_dff_search_index_publication | The DFF attribute is not deployed and published in the search index | Publish the attribute and rerun validation | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_pwa_configuration_name_availability | Before package preparation for a create, update, or delete | Configuration Name availability and existing-configuration evidence | ora_reference_lookups.md |
| verify_public_worker_access_profile_option | When the user asks to view or confirm the current PWA mode | Effective and site-level values plus verification status | ora_reference_lookups.md |
| resolve_business_unit_by_exact_name | Before a business-unit package row | BusinessUnitId | ora_reference_lookups.md |
| resolve_department_by_name_and_set | Before a department package row | OrganizationId | ora_reference_lookups.md |
| resolve_grade_by_exact_name | Before a grade package row | GradeId | ora_reference_lookups.md |
| resolve_person_by_workers_finder | Before a person package row | PersonId and AssignmentId when supported by the template | ora_reference_lookups.md |
| resolve_job_by_exact_name_and_set | Before a job package row | JobId | ora_reference_lookups.md |
| resolve_legal_employer_by_exact_name | Before a legal-employer package row | OrganizationId | ora_reference_lookups.md |
| resolve_assignment_status_by_user_status | Before an assignment-status package row | AssignmentStatusTypeId | ora_reference_lookups.md |
| resolve_person_type_by_user_person_type | Before a person-type package row | UserPersonTypeId from PersonTypeId | ora_reference_lookups.md |
| resolve_assignee_by_exact_role_name | Before a role-assignment package row | AssigneeId from RoleId | ora_reference_lookups.md |
| verify_role_unassigned_for_pwa | After exact active-role resolution and before a role-assignment package row | Role assignment availability | ora_reference_lookups.md |
| verify_dff_search_index_publication | Before a DFF-based Rule Builder package change | Published attribute and request ID | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWA.ENFORCE_DESIGN | decision | 6 | design_enforcement | ready->PWA.DATALOADER_GATE;blocked->PWA.BLOCKED | PWA.APPLY_DEFAULTS | stop | Data Loader package values and documented defaults are available |
