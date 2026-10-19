# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_fsm_task_csv_metadata | A CSV import ZIP is validated | Exactly one ASM_SETUP_CSV_METADATA.xml member and the two CSV members in the supplied ZIP | Require ObjectShortName=ORA_IRC_MANAGE_JOB_REQUISITION_SECURITY_PROFILE, ObjectType=TASK, CreatedByFlow=TASK_CSV_SERVICE, ProcessType=EXPORT, parent business object ORA_IRC_REQ_SEC_PROFILES at NodeSequence 1, child business object ORA_IRC_REQ_SEC_PROFILES_TMT at NodeSequence 2, BatchName=RequisitionSecProfileMigration, ServiceName=oracle.apps.hcm.recruiting.setup.migrationService.RequisitionSecProfileMigrationService, and BatchSize=500. Require the parent and child CSV headers to match the metadata field contracts. | Validated package identity and field contract | Stop if metadata is missing, duplicated, malformed, identifies another task, changes the documented object, sequence, batch, service, or field contract, or if a required CSV member is absent. |
| export_job_requisition_security_profiles | A target comparison or post-import readback is required | Fresh unscoped full export from the same target environment as the pending import; export status COMPLETED | Match parent rows by exact Name and child rows by ORA_IRC_REQ_SEC_PROFILES.Name. Use the full export only as a baseline; do not copy unrequested rows into the import ZIP. | Existing profile names and child rows | Stop if export is not COMPLETED, is scoped, is from another target environment, or cannot be retrieved. |
| validate_profile_name | A profile Name is supplied | Fresh unscoped full export from the same target environment; supplied Name | Match exact incoming Name against the exported parent names. | Create or update status | Reject View My Team's Requisitions and View All Job Requisitions. Otherwise return update for one exact existing Name, create for no exact existing Name, and stop for unknown target state. |
| resolve_responsibility_type | SecureByAorFlag is Y | Approved shared common-lookups route; lookupType=PER_RESPONSIBILITY_TYPES; supplied responsibility type code | Match the supplied code within the exact lookupType. | ResponsibilityType from LookupCode | Stop and request a valid unambiguous responsibility type code. |
| resolve_member_type_code | SecureByTmTypeFlag is Y | Approved shared common-lookups route; lookupType=ORA_IRC_REQ_OWNER_TYPE; supplied member type code | Match the supplied code within the exact lookupType. | MemberTypeCode from LookupCode | Stop and request a valid unambiguous member type code. |
| resolve_collaborator_rest_type_code | CollaboratorRestTypeCode is supplied and MemberTypeCode is ORA_COLLABORATOR, or MemberTypeCode is ORA_COLLABORATOR and CollaboratorRestTypeCode is absent | Approved shared common-lookups route; lookupType=ORA_IRC_COLLABORATOR_RESP_TYPE; supplied collaborator responsibility type code when present | When a code is supplied, match it exactly within the lookupType. When no code is supplied for ORA_COLLABORATOR, return possible LookupCode values for the user to consider. | CollaboratorRestTypeCode from LookupCode when supplied; possible Collaborator Type values from LookupCode when absent | Stop and request a valid unambiguous collaborator responsibility type code when one is supplied. When no code is supplied, present possible values and ask whether the user wants to specify one; retaining a blank value is allowed. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Tenant lookup request details are not documented | Do not guess an endpoint, request shape, response field, or lifecycle behavior. Keep the lookup contract blocked as TBD. |
| A documented value cannot be resolved exactly | Stop and report the unresolved value; do not create or import a profile. |
| Target profile export is requested | Use only the documented unscoped export behavior; scoped export is unsupported. |
| CSV import ZIP is submitted | Use the approved core.data-loader task-level FSM CSV import workflow. Do not use a direct REST create, update, or delete route. |
| Import ZIP is prepared | Retain unchanged metadata, then include only requested profile parent rows and child rows belonging to those parents. Omitted profiles remain unchanged. |
| Import completion is evaluated | Require import status COMPLETED and a subsequent unscoped export readback. Confirm every supplied parent field matches and every supplied child member-type row is present; allow pre-existing target child rows to remain because child rows merge. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| JRSP.RESOLVE_RESPONSIBILITY_TYPE | decision | 21 | reference_lookup | resolved->JRSP.RESOLVE_MEMBER_TYPE_CODE;not_required->JRSP.RESOLVE_MEMBER_TYPE_CODE;unresolved->JRSP.HANDLE_ERROR | JRSP.CHECK_DEPENDENCIES | stop | SecureByAorFlag is Y or not Y |
| JRSP.RESOLVE_MEMBER_TYPE_CODE | decision | 22 | reference_lookup | resolved->JRSP.RESOLVE_COLLABORATOR_REST_TYPE_CODE;not_required->JRSP.RESOLVE_COLLABORATOR_REST_TYPE_CODE;unresolved->JRSP.HANDLE_ERROR | JRSP.RESOLVE_RESPONSIBILITY_TYPE | stop | SecureByTmTypeFlag is Y or not Y |
| JRSP.RESOLVE_COLLABORATOR_REST_TYPE_CODE | decision | 23 | reference_lookup | resolved->JRSP.ENFORCE_DESIGN;not_required->JRSP.ENFORCE_DESIGN;unresolved->JRSP.HANDLE_ERROR | JRSP.RESOLVE_MEMBER_TYPE_CODE | stop | CollaboratorRestTypeCode is supplied and MemberTypeCode is ORA_COLLABORATOR, MemberTypeCode is ORA_COLLABORATOR and CollaboratorRestTypeCode is absent, or CollaboratorRestTypeCode is absent for another member type |
