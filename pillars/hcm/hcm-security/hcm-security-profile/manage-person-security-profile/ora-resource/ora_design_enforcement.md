# Person Security Profile Design Enforcement

Source: developer-provided person security profile business rules.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce unique profile name | Do not create a person security profile whose Name duplicates an existing profile |
| 2 | Enforce Areas of Responsibility compatibility | When Secure By Areas of Responsibility is selected, allow only the documented additional criteria |
| 2 | Enforce View All compatibility | When View All is selected, allow only access to own record and apply exclusion rules as additional criteria |
| 3 | Enforce exclusion-rule criterion compatibility | Allow exclusion rules only when Secure By Areas of Responsibility or View All is selected |
| 4 | Enforce exclusion rule limit | Limit the profile to three associated exclusion rules |
| 5 | Default assignment evaluation | Default Assignments To Evaluate when a department, business unit, legal employer, position, legislative data group, or payroll criterion is selected and no value is supplied |
| 6 | Enforce person type access | Evaluate AccessTo per selected person type: require All for an unrestricted selection and Restricted only when an applicable criterion limits that selection; permit mixed selections in one profile |
| 7 | Review similar work-structure profiles | When an enabled profile uses the same complete work-structure criterion set, show the AOR alternative and require an explicit exception confirmation before preview |
| 8 | Resolve FSM CSV layout | Derive an ordered manifest of every CSV package member, its exact header, field mappings, and parent-child linkage from the current target-environment template-only export. Include every manifest member exactly once in that order. Write data only where applicable; retain no-data members as exact template-header-only CSVs. Use declared ViewInstanceName and GroupingKey patterns when available; otherwise use the documented member-specific view fallback and a unique uppercase 32-character hexadecimal GUID without separators for each new row. Retain ASM_SETUP_CSV_METADATA.xml unchanged |
| 9 | Enforce Core Data Loader-only mutation route | Generate the package only from the resolved current template layout and create or update the profile only through one approved immutable core.data-loader import |
| 10 | Enforce independent manager hierarchy inputs | Resolve supervisor type, hierarchy content, and maximum levels independently. A specific supervisor type derives parent ManagerTypes=SELECTIVE_MGR and one manager-type child row; hierarchy content always maps to EvalMgrHierarchyFor. |
| 11 | Advise on specific work-structure access | Explain that access to a specified legal employer, business unit, department, position, LDG, or payroll is configured through Areas of Responsibility and requires the appropriate AOR assignments; continue with CSV package creation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating a new person security profile | Blocker | find_person_security_profile_by_exact_name | An existing person security profile has the same Name | Provide a unique Name before preview or CSV package generation | Yes |
| SecureByAreasOfResponsibilityFlag is true | Blocker | | A criterion other than AccessToOwnRecordFlag, IncludeFuturePeopleFlag, IncludeSharedPeopleInformationFlag, CandidateWithOfferFlag, ApplyExclusionRulesFlag, or SecureByCustomCriteriaFlag is also selected | Remove the unsupported criterion; retain only the permitted criteria with Secure By Areas of Responsibility | Yes |
| ViewAllFlag is true | Blocker | | A criterion other than AccessToOwnRecordFlag or ApplyExclusionRulesFlag is also selected | Remove the unsupported criterion; retain only access to own record or apply exclusion rules with View All | Yes |
| ApplyExclusionRulesFlag is true | Blocker | | Neither SecureByAreasOfResponsibilityFlag nor ViewAllFlag is true, or more than three exclusion rules are associated with the profile | Select Secure By Areas of Responsibility or View All, or remove the exclusion rules; retain no more than three associated rules | Yes |
| SecureByDepartmentFlag, SecureByBusinessUnitFlag, SecureByLegalEmployerFlag, SecureByPositionFlag, SecureByLegislativeDataGroupFlag, or SecureByPayrollFlag is true | Blocker | resolve_assignments_to_evaluate_from_lookup | AssignmentsToEvaluate is blank, unresolved, or contains a display meaning rather than the exact enabled lookup code after defaulting | Resolve Active, suspended or most recently terminated, or the supplied value, through the lookup and write its exact code | Yes |
| SecureByPersonTypeFlag is true | Blocker | resolve_person_type_access_from_lookup | A selected system person type or user person type has no explicit AccessTo value, AccessTo is not All or Restricted, or AccessTo=All is used while an applicable criterion restricts that same selected person type | Evaluate selections independently: retain All for unrestricted selections and use Restricted only for selections limited by an applicable criterion. A valid functional requirement may combine EMP=Restricted under a two-level LINE_MGR hierarchy with CWK=All in one profile. | Yes |
| A new profile selects one or more work-structure criteria and the similar-profile lookup returns one or more enabled exact matches | Preview blocker | find_enabled_person_security_profiles_by_workstructure_criteria | Matching enabled profiles have not been shown, or the consultant has not explicitly confirmed that AOR was reviewed and intentionally not selected | Show the matching profile Names and shared criteria before allowing preview. | Yes |
| A new profile selects one or more work-structure criteria and the similar-profile lookup returns one or more enabled exact matches | Preview blocker | resolve_exact_aor_scope_from_common_lookup | The current AOR scope candidates have not been reviewed, or the consultant has not explicitly confirmed that AOR was reviewed and intentionally not selected | Show the one exact current AOR scope when available. If no exact scope is available, state that no automatic suggestion is available. Record the explicit exception confirmation before allowing preview. | Yes |
| A person security profile CSV package is generated or imported | Blocker | resolve_person_security_profile_csv_context | The profile attributes are incomplete; the current template-only export cannot establish an unambiguous ordered CSV-member manifest, headers, field mapping, or parent-child linkage; a template CSV member is missing, duplicated, renamed, reordered, or has a different header; a template-declared ViewInstanceName or GroupingKey pattern conflicts with a generated row; ASM_SETUP_CSV_METADATA.xml is changed; the exact package preview is not approved; or the import does not use core.data-loader with process-log verification | Identify all attributes, export a current template-only package, rebuild the immutable package from the resolved ordered manifest with every no-data member retained as its exact template-header-only CSV, without changing ASM_SETUP_CSV_METADATA.xml; obtain exact approval, submit one core.data-loader task-level import, and verify the process log | Yes |
| A person security profile create or update is requested | Blocker | | The requested route is a direct REST POST, PUT, or PATCH request | Use the current template-backed CSV package and core.data-loader only; direct REST create and update requests are not supported | Yes |
| Parent manager selection is supplied or derived | Blocker | resolve_manager_type_from_lookup | The derived parent ManagerTypes value does not exactly resolve from PER_PRSN_SEC_PROF_MGR_TYPES | Default LINE_MGR only when no supervisor type or parent selection is supplied; otherwise use the exact derived parent value | Yes |
| A specific supervisor type is requested | Blocker | resolve_manager_type_value_from_lookup | Parent ManagerTypes is not SELECTIVE_MGR, the derived manager-type child row is missing or differs, or the supervisor type does not exactly resolve from PER_SUPERVISOR_TYPE | Set parent ManagerTypes to SELECTIVE_MGR and generate exactly one ManagerTypeValue child row | Yes |
| hierarchy_content is supplied or defaulted | Blocker | resolve_hierarchy_content_from_lookup | EvalMgrHierarchyFor does not exactly resolve from PER_PRSN_SEC_PROF_MGR_HIER_FOR | Resolve and write the exact hierarchy-content code independently of supervisor type | Yes |
| supervisor_type conflicts with legacy manager_type | Blocker | resolve_manager_type_from_lookup | The explicit legacy parent selection cannot represent the supervisor type's required parent selection | Correct the conflict before preview; do not silently apply LINE_MGR | Yes |
| A profile-reference or lookup-backed value is supplied | Preview blocker | | The value does not pass its documented exact-match resolver | Stop before preview and ask the user to provide the correct value | Yes |
| Access is requested for a specific legal employer, business unit, department, position, LDG, or payroll | Advisory | | None | Explain that Areas of Responsibility is the access configuration and appropriate AOR assignments are required; proceed with CSV package creation | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_person_security_profile_by_exact_name | Creating a new person security profile | Existing matching Name | ora_reference_lookups.md |
| find_enabled_person_security_profiles_by_workstructure_criteria | A new profile selects one or more work-structure criteria | Matching profile Names and criterion set | ora_reference_lookups.md |
| resolve_exact_aor_scope_from_common_lookup | A similar enabled profile exists | ScopeOfResponsibility and ScopeOfResponsibilityMeaning | ora_reference_lookups.md |
| resolve_manager_type_from_lookup | Parent ManagerTypes is supplied or derived | Permitted parent selection | ora_reference_lookups.md |
| resolve_manager_type_value_from_lookup | A specific supervisor type is requested | Exact ManagerTypeValue child value | ora_reference_lookups.md |
| resolve_hierarchy_content_from_lookup | hierarchy_content is supplied or defaulted | Exact EvalMgrHierarchyFor value | ora_reference_lookups.md |
| resolve_person_type_access_from_lookup | SecureByPersonTypeFlag is true | AccessTo value of All or Restricted | ora_reference_lookups.md |
| resolve_assignments_to_evaluate_from_lookup | A work-structure criterion requires assignment evaluation | Exact enabled LookupCode for AssignmentsToEvaluate | ora_reference_lookups.md |
| resolve_person_security_profile_csv_context | Before a CSV package is generated or imported | Ordered template CSV-member manifest, exact headers, field mappings, parent-child linkage, template/fallback ViewInstanceName, template/per-row-uppercase-hexadecimal-GUID GroupingKey, and metadata contract | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSP.ENFORCE | decision | 6 | design_enforcement | compliant->PSP.RESOLVE_CSV_LAYOUT;blocked->PSP.ERROR | PSP.DEFAULT_ASSIGNMENTS | stop | A valid person security profile configuration is being prepared for preview or CSV package generation |
