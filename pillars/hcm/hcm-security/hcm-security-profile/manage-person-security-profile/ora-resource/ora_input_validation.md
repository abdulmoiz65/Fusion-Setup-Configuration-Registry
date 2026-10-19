# Person Security Profile Input Validation

Source: developer-provided person security profile business rules.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Person security profile name | Name | Stop | Provide a unique Name that does not duplicate an existing person security profile | Creating a new person security profile | find_person_security_profile_by_exact_name |
| Areas of Responsibility configuration | SecureByAreasOfResponsibilityFlag and, when any additional criterion is selected, only AccessToOwnRecordFlag, IncludeFuturePeopleFlag, IncludeSharedPeopleInformationFlag, CandidateWithOfferFlag, ApplyExclusionRulesFlag, or SecureByCustomCriteriaFlag | Stop | Remove every additional criterion not in the permitted set | SecureByAreasOfResponsibilityFlag is true | |
| View All configuration | ViewAllFlag and, when an additional criterion is selected, only AccessToOwnRecordFlag or ApplyExclusionRulesFlag | Stop | Remove every additional criterion other than AccessToOwnRecordFlag or ApplyExclusionRulesFlag | ViewAllFlag is true | |
| Exclusion rules | ApplyExclusionRulesFlag with either SecureByAreasOfResponsibilityFlag or ViewAllFlag, and no more than three associated exclusion rules | Stop | Select Secure By Areas of Responsibility or View All, or remove the exclusion rules; remove excess rules so the associated rule count is three or fewer | ApplyExclusionRulesFlag is true | |
| Person type configuration | One or more System Person Type or User Person Type selections, each with an access value of All or Restricted | Stop | Evaluate AccessTo for each selected person type: set All when that selection has unrestricted access and Restricted only when an applicable criterion limits that selection; mixed access values in one profile are supported | SecureByPersonTypeFlag is true | resolve_person_type_access_from_lookup |
| Person or assignment level | PersonOrAssignmentLevel with value P or A | Stop | Supply P for person-level or A for assignment-level security | A new or updated profile specifies a level | |
| Boolean criteria | EnabledFlag and every listed person-security-profile flag | Stop | Supply a YES_NO value for each explicitly specified flag | A new or updated profile explicitly supplies a flag value | |
| Manager hierarchy configuration | Supervisor type, hierarchy content, and maximum hierarchy levels | Stop | Resolve each input independently. A specific supervisor type derives parent ManagerTypes=SELECTIVE_MGR and exactly one ManagerTypeValue child row; LINE_MANAGER or ALL derive their parent value without a child row. | SecureByManagerHierarchyFlag is true | |
| Lookup-backed profile references | A supplied display value for User Person Type, Exclusion Rule, Department, Business Unit, Legal Employer, Position, LDG, or Payroll Security Profile | Stop | Resolve the supplied display value through its documented exact-match resolver before preview | A new or updated profile references another setup object | |
| CSV import package | Identified person security profile attributes, current supported task template, every template CSV member in matching order and with its exact header, immutable package preview, explicit approval, and process-log verification | Stop before package generation or import | Identify the profile attributes, export the current task template, retain every template CSV member (header-only when no rows apply), approve the exact preview, and use core.data-loader for one task-level import | Generating or importing a person security profile CSV package | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Creating a new person security profile and an existing profile has the same Name | Blocked | Provide a unique Name before preview or CSV package generation | find_person_security_profile_by_exact_name |
| SecureByAreasOfResponsibilityFlag is true and an additional selected criterion is not AccessToOwnRecordFlag, IncludeFuturePeopleFlag, IncludeSharedPeopleInformationFlag, CandidateWithOfferFlag, ApplyExclusionRulesFlag, or SecureByCustomCriteriaFlag | Blocked | Remove the unsupported criterion before preview | |
| ViewAllFlag is true and an additional selected criterion is not AccessToOwnRecordFlag or ApplyExclusionRulesFlag | Blocked | Remove the unsupported criterion before preview | |
| ApplyExclusionRulesFlag is true and neither SecureByAreasOfResponsibilityFlag nor ViewAllFlag is true | Blocked | Select Secure By Areas of Responsibility or View All, or remove the exclusion rules before preview or CSV package generation | |
| More than three exclusion rules are associated with the profile | Blocked | Retain no more than three exclusion rules before preview | |
| SecureByPersonTypeFlag is true and a selected system or user person type has no explicit access value, has an access value other than All or Restricted, or has All while an applicable criterion restricts that same selected person type | Blocked | Evaluate each person-type selection independently: set AccessTo to All for unrestricted access or Restricted only for the selection limited by an applicable criterion; retain valid mixed selections in the same profile | resolve_person_type_access_from_lookup |
| A CSV package is requested without identified profile attributes or a current supported task template | Blocked | Identify the attributes and export the current task template; do not invent CSV columns, package members, or mappings | |
| A generated ZIP omits, duplicates, renames, reorders, or changes the header of any template CSV member | Blocked | Rebuild from the template's ordered CSV-member manifest. Retain each no-data member as its exact template-header-only CSV. | resolve_person_security_profile_csv_context |
| A CSV import is requested without an immutable preview, explicit approval, or process-log verification plan | Blocked | Prepare and approve the exact package before one core.data-loader task-level import | |
| SecureByManagerHierarchyFlag is true and a specific supervisor type is requested, but its parent selection is not SELECTIVE_MGR, the derived manager-type child row is absent or differs, or the supervisor type cannot be exactly resolved | Blocked | Set parent ManagerTypes to SELECTIVE_MGR, create exactly one ManagerTypeValue child row, and supply the exact supervisor-type value before preview | resolve_manager_type_value_from_lookup |
| supervisor_type or requested_manager_type conflicts with legacy manager_type | Blocked | Correct the conflicting input. The legacy manager_type represents only the parent selection mode and cannot replace a specific supervisor type. | resolve_manager_type_from_lookup |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name | Resolve Name against existing person security profiles and reject a duplicate | Creating a new person security profile | find_person_security_profile_by_exact_name |
| SecureByAreasOfResponsibilityFlag | Permit only AccessToOwnRecordFlag, IncludeFuturePeopleFlag, IncludeSharedPeopleInformationFlag, CandidateWithOfferFlag, ApplyExclusionRulesFlag, and SecureByCustomCriteriaFlag as additional criteria | The flag is true | |
| ViewAllFlag | Permit only AccessToOwnRecordFlag and ApplyExclusionRulesFlag as additional criteria | The flag is true | |
| Exclusion rule eligibility and count | Require SecureByAreasOfResponsibilityFlag=true or ViewAllFlag=true, and accept zero through three associated exclusion rules | ApplyExclusionRulesFlag is true | |
| System Person Type | Evaluate each selected system person type independently. Accept AccessTo=All for an unrestricted selection and AccessTo=Restricted only when an applicable criterion limits that selection; allow mixed selections such as EMP=Restricted with CWK=All in one profile | SecureByPersonTypeFlag is true and a system person type is selected | resolve_person_type_access_from_lookup |
| User Person Type | Evaluate each selected user person type independently. Accept AccessTo=All for an unrestricted selection and AccessTo=Restricted only when an applicable criterion limits that selection | SecureByPersonTypeFlag is true and a user person type is selected | resolve_person_type_access_from_lookup |
| PersonOrAssignmentLevel | Accept only P or A | A level is supplied or defaulted | |
| AssignmentsToEvaluate | Resolve a supplied or defaulted display value through ORA_PER_PRSN_ASGS_TO_EVALUATE and write only the exact enabled LookupCode to the CSV field | A work-structure criterion requires assignment evaluation | resolve_assignments_to_evaluate_from_lookup |
| Manager hierarchy | Resolve hierarchy content through PER_PRSN_SEC_PROF_MGR_HIER_FOR independently. For LINE_MANAGER or ALL, derive the parent selection and do not create a manager-type child row. For a specific supervisor type, set parent ManagerTypes to SELECTIVE_MGR, create only the manager-type child row, and resolve its ManagerTypeValue through PER_SUPERVISOR_TYPE. | SecureByManagerHierarchyFlag is true | resolve_manager_hierarchy_configuration |
| Boolean criteria | Accept only YES_NO values for EnabledFlag, AccessToOwnRecordFlag, IncludeFuturePeopleFlag, IncludeSharedPeopleInformationFlag, ViewAllFlag, ApplyExclusionRulesFlag, SecureByDepartmentFlag, SecureByBusinessUnitFlag, SecureByLegalEmployerFlag, SecureByLegislativeDataGroupFlag, SecureByPositionFlag, SecureByPayrollFlag, SecureByCustomCriteriaFlag, EmployeeFlag, ContingentWorkerFlag, NonWorkerFlag, and CandidateWithOfferFlag | The corresponding flag is supplied or defaulted | |
| User Person Type | Resolve UserPersonType to exactly one PersonTypeId; for duplicate results, request the System Person Type | A user person type display value is supplied | find_user_person_type_by_exact_name |
| Exclusion Rule | Resolve Name to exactly one ExclusionRuleId | An exclusion rule display value is supplied | find_exclusion_rule_by_exact_name |
| Organization Security Profile | Resolve Name to exactly one OrganizationSecurityProfileId | A department, business unit, or legal employer security profile display value is supplied | find_organization_security_profile_by_exact_name |
| Position Security Profile | Resolve Name to exactly one PositionSecurityProfileId | A position security profile display value is supplied | find_position_security_profile_by_exact_name |
| Legislative Data Group Security Profile | Resolve Name to exactly one LegislativeDataGroupSecurityProfileId | A legislative data group security profile display value is supplied | find_ldg_security_profile_by_exact_name |
| Payroll Security Profile | Resolve PayrollSecurityProfileName to exactly one PayrollSecurityProfileId using finder=findByWord;PayRestName=Enabled_PayrollSecurityProfilePVO,FilterAttributes=Name,SearchTerms={PayrollSecurityProfileName}; match the returned Name exactly and map ResultValue1 where ResultKey1 is PaySecurityProfileId | A payroll security profile name is supplied | find_payroll_security_profile_by_exact_name |

## Environment-Derived FSM CSV Layout

The current target-environment template-only export is the CSV schema
authority. Resolve its members, headers and order, parent and child roles,
field mappings, parent-child linkage, ViewInstanceName values, and GroupingKey
patterns through resolve_person_security_profile_csv_context before generating
any CSV row. When the template omits a ViewInstanceName or GroupingKey pattern,
use the member-specific fallback below. A fallback GroupingKey is a newly
generated, uppercase 32-character hexadecimal GUID with no separators for each
new row. Do not use repository column lists.

| Package Element | Validation and Row Mapping |
|---|---|
| PER_PERSON_SECURITY_PROFILES.csv | Use the resolver-identified header sequence and field mapping. Use the template-declared ViewInstanceName when present; otherwise use PersonSecurityProfileMigration. Use the template-declared GroupingKey pattern when present; otherwise generate a new uppercase 32-character hexadecimal GUID without separators for this row. |
| ORA_PERSON_SECURITY_PROFILE_AOR_SCOPES.csv | Use the resolver-identified header sequence, parent link, and field mapping. Use the template-declared ViewInstanceName when present; otherwise use PersonSecurityProfileAorScopeMigration. Use the template-declared GroupingKey pattern when present; otherwise generate a distinct new uppercase 32-character hexadecimal GUID without separators for this row. |
| ORA_PER_PERSON_SECURITY_PROFILE_EXCLUSION.csv | Use the resolver-identified header sequence, parent link, and field mapping. Use the template-declared ViewInstanceName when present; otherwise use PersonSecurityProfileExclusionMigration. Use the template-declared GroupingKey pattern when present; otherwise generate a distinct new uppercase 32-character hexadecimal GUID without separators for this row. |
| ORA_PER_PERSON_SEC_PROF_MGR_TYPES.csv | Use the resolver-identified header sequence, parent link, and field mapping. Use the template-declared ViewInstanceName when present; otherwise use PersonSecurityProfileManagerTypeMigration. Use the template-declared GroupingKey pattern when present; otherwise generate a distinct new uppercase 32-character hexadecimal GUID without separators for this row. |
| ORA_PER_PERSON_SEC_PROF_PER_TYPES.csv | Use the resolver-identified header sequence, parent link, and field mapping. Use the template-declared ViewInstanceName when present; otherwise use PersonSecurityProfilePersonTypeMigration. Use the template-declared GroupingKey pattern when present; otherwise generate a distinct new uppercase 32-character hexadecimal GUID without separators for this row. |
| CSV member manifest | Include every CSV member from the template-only export exactly once and in the same order. When a member has no applicable configuration rows, include its exact template header only; do not omit it or add placeholder rows. |
| Metadata member | Retain ASM_SETUP_CSV_METADATA.xml exactly once and byte-for-byte unchanged from the template-only export. |

Every generated row must have the resolved member's exact header count and
order. Stop before preview or import when the template cannot establish an
unambiguous ordered CSV-member manifest, parent-child linkage, or field
mapping; when a template CSV member is missing, duplicated, renamed, reordered,
or has a different header; when template ViewInstanceName or GroupingKey
evidence conflicts with the generated row; or when the metadata bytes change.
Missing ViewInstanceName or GroupingKey patterns use the member-specific
fallback above and do not block package preparation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSP.VALIDATE | decision | 1 | validate_input | valid->PSP.DEFAULT_ASSIGNMENTS;invalid->PSP.ERROR | none | stop | A person security profile configuration or CSV import request is supplied |
