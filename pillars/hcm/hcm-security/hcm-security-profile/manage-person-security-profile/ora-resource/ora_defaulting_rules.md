# Person Security Profile Defaulting Rules

Source: developer-provided person security profile business rules.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AssignmentsToEvaluate | Active, suspended or most recently terminated | SecureByDepartmentFlag, SecureByBusinessUnitFlag, SecureByLegalEmployerFlag, SecureByPositionFlag, SecureByLegislativeDataGroupFlag, or SecureByPayrollFlag is true and no value is provided | Yes | resolve_assignments_to_evaluate_from_lookup |
| EnabledFlag | true | A new profile omits EnabledFlag | No | |
| EmployeeFlag | true | A new profile omits EmployeeFlag under SecureByAreasOfResponsibilityFlag | No | |
| ContingentWorkerFlag | true | A new profile omits ContingentWorkerFlag under SecureByAreasOfResponsibilityFlag | No | |
| NonWorkerFlag | true | A new profile omits NonWorkerFlag under SecureByAreasOfResponsibilityFlag | No | |
| CandidateWithOfferFlag | true | A new profile omits CandidateWithOfferFlag under SecureByAreasOfResponsibilityFlag | No | |
| All other flags | false | A new profile omits a flag other than the documented Secure By Areas of Responsibility criteria flags | No | |
| PersonOrAssignmentLevel | P | A new profile omits the level | No | |
| ManagerTypes | LINE_MGR | A new profile omits both a supervisor type and the legacy parent manager-type selection | No | |
| EvalMgrHierarchyFor (HierarchyContent) | PER_OWN | A new profile omits hierarchy content | No | |
| Purpose | ORA_PRSN_ACCESS | A new profile omits Purpose | No | resolve_purpose_from_lookup |

## Manager Hierarchy Inputs

Capture the following values independently:

| Input | CSV Mapping | Lookup | Rule |
|---|---|---|---|
| Supervisor type | ManagerTypeValue child row | PER_SUPERVISOR_TYPE | A specific type, such as PROJECT_MANAGER, derives parent ManagerTypes=SELECTIVE_MGR and exactly one manager-type child row. LINE_MANAGER and ALL derive their parent values without a child row. |
| Hierarchy content | EvalMgrHierarchyFor | PER_PRSN_SEC_PROF_MGR_HIER_FOR | Use the exact requested value or default PER_OWN. Delegating manager hierarchy is hierarchy content, not a supervisor type. |
| maximum_levels_in_hierarchy | MaximumLevelsInHierarchy | None | Preserve the explicit numeric level; do not derive it from either manager input. |

For compatibility, accept requested_manager_type as an alias of supervisor_type. Treat legacy manager_type as the parent-selection input only. Reject conflicting explicit values rather than replacing a supervisor type with the LINE_MGR default.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSP.DEFAULT_ASSIGNMENTS | step | 2 | apply_default | applied->PSP.LOOKUP_PROFILE_REFERENCES;not_needed->PSP.LOOKUP_PROFILE_REFERENCES | PSP.VALIDATE | stop | Valid person security profile configuration is available |
