# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Profile identity | Name | Stop | Provide a nonblank target name. An existing exact name is updated; a missing exact name is created. | Always | validate_profile_name |
| Seeded profile protection | Name | Stop | Do not submit View My Team's Requisitions or View All Job Requisitions for update. | Always | validate_profile_name |
| Header flags | EnabledFlag, ViewAllFlag, SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, SecureByRecTypeFlag, AccessSubordinateReqFlag, SecureByTmTypeFlag, SecureByAorFlag | Stop | Provide Y or N for each applicable flag. | Always |  |
| Area of Responsibility responsibility type | ResponsibilityType | Stop | Resolve an exact approved responsibility type code. | SecureByAorFlag is Y | resolve_responsibility_type |
| Area of Responsibility security criterion | SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, or SecureByRecTypeFlag | Stop | Set at least one listed criterion flag to Y. | SecureByAorFlag is Y |  |
| Hiring-team member type | MemberTypeCode | Stop | Resolve an exact approved member type code. | SecureByTmTypeFlag is Y | resolve_member_type_code |
| Collaborator responsibility | CollaboratorRestTypeCode, when supplied | Continue without a value. | When supplied, require MemberTypeCode=ORA_COLLABORATOR and resolve the exact approved collaborator responsibility type code. | CollaboratorRestTypeCode is supplied | resolve_collaborator_rest_type_code |
| Collaborator Type choice | CollaboratorRestTypeCode, when optional | Ask | When MemberTypeCode is ORA_COLLABORATOR and CollaboratorRestTypeCode is absent, ask whether the user wants to specify Collaborator Type. Offer possible values from ORA_IRC_COLLABORATOR_RESP_TYPE; retain the blank value if the user declines. | MemberTypeCode is ORA_COLLABORATOR and CollaboratorRestTypeCode is absent | resolve_collaborator_rest_type_code |
| Requested profile change set | Requested profile Names for create or update | Stop | Supply the exact Names the user intends to change. | CSV import |  |
| Import ZIP | Exactly one ASM_SETUP_CSV_METADATA.xml, ORA_IRC_REQ_SEC_PROFILES.csv, ORA_IRC_REQ_SEC_PROFILES_TMT.csv | Stop | Supply one immutable ZIP that conforms to the full-export structure. | CSV import | verify_fsm_task_csv_metadata |

## User-Facing Field Labels

| Technical Field | User-Facing Label |
|---|---|
| EnabledFlag | Enable |
| SecureByJobFamilyFlag | Secure by job family |
| SecureByJobFunctionFlag | Secure by job function |
| SecureByLocationFlag | Secure by location |
| SecureByOrganizationFlag | Secure by organization |
| SecureByRecTypeFlag | Secure by recruiting type |
| AccessSubordinateReqFlag | Access subordinate's requisitions |
| SecureByTmTypeFlag | Secure by hiring team member type |
| SecureByAorFlag | Secure by area of responsibility |
| ResponsibilityType | Responsibility type |
| ViewAllFlag | View all |
| MemberTypeCode | Hiring Team Member Type |
| CollaboratorRestTypeCode | Collaborator Type |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name format | Name must be nonblank, unique in the target, and no longer than 240 characters. An exact existing target Name is an update unless it is seeded; an absent exact target Name is a create. | Always | validate_profile_name |
| Seeded profile names | View My Team's Requisitions and View All Job Requisitions must not be updated. | Always | validate_profile_name |
| Flag format | Each documented header flag must be Y or N. | Always |  |
| View All exclusivity | ViewAllFlag set to Y must not be combined with restrictive criteria. | ViewAllFlag is Y |  |
| Area of Responsibility responsibility type code | ResponsibilityType must be an exact code from PER_RESPONSIBILITY_TYPES. | SecureByAorFlag is Y | resolve_responsibility_type |
| Area of Responsibility criterion selection | At least one of SecureByJobFamilyFlag, SecureByJobFunctionFlag, SecureByLocationFlag, SecureByOrganizationFlag, or SecureByRecTypeFlag must be Y. | SecureByAorFlag is Y |  |
| Member type code | MemberTypeCode must be an exact code from ORA_IRC_REQ_OWNER_TYPE. | SecureByTmTypeFlag is Y | resolve_member_type_code |
| Collaborator responsibility code | CollaboratorRestTypeCode is optional. When supplied, it must be an exact code from ORA_IRC_COLLABORATOR_RESP_TYPE and MemberTypeCode must be ORA_COLLABORATOR. | CollaboratorRestTypeCode is supplied | resolve_collaborator_rest_type_code |
| Import archive members | Require exactly one metadata member and both parent and child CSV members. The metadata retains the full-export structure, including ProcessType=EXPORT. | CSV import | verify_fsm_task_csv_metadata |
| Parent-child join | Every child ORA_IRC_REQ_SEC_PROFILES.Name must exactly match a Name in the parent CSV. Reject the entire import when a child is orphaned. | CSV import |  |
| Requested-row subset | Every parent and child row in the import ZIP must belong to one requested profile Name. Omit all other profiles from the import ZIP. | CSV import |  |
| Duplicate child row | Reject the entire import when the same Name, MemberTypeCode, and CollaboratorRestTypeCode tuple appears more than once in the child CSV. | CSV import |  |
| Import approval | Require an approval bound to the exact ZIP checksum, target environment, and create/update/merge summary. | Before CSV import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| JRSP.VALIDATE_INPUT | step | 10 | validate_input | valid->JRSP.CHECK_DEPENDENCIES;invalid->JRSP.HANDLE_ERROR | none | stop | Always |
