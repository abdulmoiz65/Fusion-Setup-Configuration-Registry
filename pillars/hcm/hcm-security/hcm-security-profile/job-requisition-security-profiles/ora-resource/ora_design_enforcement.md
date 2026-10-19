# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | View All review | Confirm ViewAllFlag is not combined with restrictive criteria. |
| 2 | Area of Responsibility code review | Confirm ResponsibilityType resolves through the approved common-lookups route when SecureByAorFlag is Y. |
| 3 | Area of Responsibility effectiveness review | When SecureByAorFlag is N, explain that enabled Area of Responsibility criteria and a supplied ResponsibilityType are ignored. |
| 4 | Hiring-team review | Confirm every related child row is included when SecureByTmTypeFlag is Y. |
| 5 | Create and update behavior | Create a profile when the exact Name is absent; update it when the exact Name exists. Merge supplied child rows with existing child rows. |
| 6 | Requested-row subset | Build the import ZIP from only requested profile parent rows and their child rows; omitted profiles remain unchanged. |
| 7 | Validated package preview | Present the validated ZIP content in a user-friendly form before requesting import approval. |
| 8 | Import outcome | Do not report success until the import status is COMPLETED and the required post-import readback matches. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| ViewAllFlag is Y | Error |  | View All is combined with restrictive criteria. | Use unrestricted visibility intentionally or remove conflicting restrictive criteria. | Yes |
| SecureByAorFlag is Y | Error | resolve_responsibility_type | ResponsibilityType is unresolved. | Supply an exact approved responsibility type code. | Yes |
| SecureByAorFlag is Y | Error |  | SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, and SecureByRecTypeFlag are all N. | Set at least one listed Area of Responsibility security criterion flag to Y. | Yes |
| SecureByAorFlag is N and any of SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, or SecureByRecTypeFlag is Y, or ResponsibilityType is not blank | Warning |  | None. This configuration is allowed, but the enabled Area of Responsibility criteria and Responsibility type are ignored. | Inform the user that Secure by job family, Secure by job function, Secure by location, Secure by organization, Secure by recruiting type, and Responsibility type are not taken into account until Secure by area of responsibility is Y. | Yes |
| Communicating with a user about Area of Responsibility | Error |  | The response uses AOR even though the user has not used that acronym. | Use Area of Responsibility in prompts and responses. Recognize AOR as an internal synonym and mirror it only after the user explicitly uses it. | Yes |
| Communicating with a user about a documented field | Error |  | A prompt or response uses a technical field name when a user-facing label is available. | Use the exact corresponding label in User-Facing Field Labels. Retain the technical field name only when discussing CSV columns or technical implementation. | Yes |
| SecureByTmTypeFlag is Y | Error | resolve_member_type_code | A related child row is missing or MemberTypeCode is unresolved. | Include every related child row. | Yes |
| CollaboratorRestTypeCode is supplied | Error | resolve_collaborator_rest_type_code | MemberTypeCode is not ORA_COLLABORATOR, or the supplied CollaboratorRestTypeCode is unresolved. | Remove CollaboratorRestTypeCode unless MemberTypeCode is ORA_COLLABORATOR; when retained, supply an exact approved code. | Yes |
| Target Name already exists | Error | validate_profile_name | The import is not prepared as an update of the exact existing Name, or an explicit replace or new-only decision would override the documented update behavior. | Prepare the parent row as an update; do not create a duplicate profile. | Yes |
| Target Name is View My Team's Requisitions or View All Job Requisitions | Error | validate_profile_name | A seeded profile is included in an update request. | Remove the seeded profile from the requested change set. | No |
| Supplied child member type already exists | Error |  | The import would treat a supplied child row as replacement or deletion. | Merge the supplied child row with existing child rows; do not remove existing child rows. | Yes |
| CSV import is requested | Error | verify_fsm_task_csv_metadata | The ZIP is not immutable, does not conform to the full-export contract, lacks approval, or lacks required privilege evidence. | Validate the ZIP, bind approval to its checksum and target, and require Manage Recruiting Administration privilege. | Yes |
| CSV import is requested | Error |  | The ZIP includes an unrequested profile or a child row for an unrequested parent profile. | Rebuild the ZIP from only the requested profile Names and their child rows. | Yes |
| A CSV import ZIP is ready and validated | Error | verify_fsm_task_csv_metadata | The validated ZIP content has not been presented to the user in a user-friendly form. | Before requesting import approval, show each requested profile Name, its create or update outcome, its field values using User-Facing Field Labels, and each related Hiring Team Member Type and Collaborator Type row. | Yes |
| Import is reported successful | Error | export_job_requisition_security_profiles | Status is not COMPLETED or unscoped readback does not match supplied parent fields and child-row presence. | Stop without retry and correct the package or import issue. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_responsibility_type | SecureByAorFlag is Y | ResponsibilityType | TBD |
| resolve_member_type_code | SecureByTmTypeFlag is Y | MemberTypeCode | TBD |
| resolve_collaborator_rest_type_code | CollaboratorRestTypeCode is supplied and MemberTypeCode is ORA_COLLABORATOR | CollaboratorRestTypeCode | TBD |
| validate_profile_name | Before create or update determination | Create or update status | TBD |
| verify_fsm_task_csv_metadata | Before CSV import | Validated package identity and field contract | Full export ZIP |
| export_job_requisition_security_profiles | After import status is COMPLETED | Parent-field readback and supplied child-row presence | TBD |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| JRSP.ENFORCE_DESIGN | step | 30 | design_enforcement | compliant->JRSP.EXECUTION_GATE;blocked->JRSP.HANDLE_ERROR | JRSP.RESOLVE_COLLABORATOR_REST_TYPE_CODE | stop | Always |
