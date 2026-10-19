# Person Security Profile CSV Import Readiness

Source: developer-provided requirement to generate a supported CSV import package for Manage Person Security Profile and load it through core.data-loader.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Profile attributes | Identify all attributes for the person security profile configuration |
| 2 | Exclusion-rule criterion compatibility | When exclusion rules are applied, confirm that Secure By Areas of Responsibility or View All is selected |
| 3 | Similar-profile AOR review | For a new work-structure-based profile, complete the similar-profile lookup and record the AOR-review exception when a match exists |
| 4 | Current task template | Export the current supported Manage Person Security Profile task CSV template from the target environment |
| 5 | CSV resolver layout | Resolve exact members, headers, field mappings, and parent-child linkage from the current template-only export. Use its ViewInstanceName and GroupingKey pattern when declared; otherwise use the documented member-specific view fallback and a distinct uppercase 32-character hexadecimal GUID without separators for each new row |
| 6 | Package construction | Map the identified attributes only to the resolved template layout and retain its supported package structure and metadata |
| 7 | Immutable preview and approval | Produce an immutable ZIP preview and obtain explicit approval for that exact package |
| 8 | Import and verification | Submit one approved task-level import through core.data-loader and verify the returned process log |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| person_security_profile_attributes | Person security profile attributes | Yes | Generating a CSV import package | Satisfied | Identified configuration attributes | | The package cannot be created until the requested profile attributes and criteria are known | Supply the profile name and every selected criterion, including required values and associated rules | Complete profile configuration |
| person_security_profile_exclusion_criterion_compatibility | Exclusion-rule criterion compatibility | Conditional | ApplyExclusionRulesFlag is true | Verify | Identified configuration attributes | | Exclusion rules are valid only with Secure By Areas of Responsibility or View All | Select SecureByAreasOfResponsibilityFlag=true or ViewAllFlag=true, or remove the exclusion rules before preview or CSV package generation | SecureByAreasOfResponsibilityFlag or ViewAllFlag |
| person_security_profile_similar_design_review | Similar-profile review | Conditional | A new profile selects one or more work-structure criteria | Verify | Enabled existing Person Security Profiles | find_enabled_person_security_profiles_by_workstructure_criteria | Existing designs with the same complete criterion set must be reviewed for an AOR alternative before preview | Review matching profile Names and criteria. If a match exists, continue to the AOR scope lookup. | Matching profile Names and criterion set |
| person_security_profile_aor_scope_recommendation | AOR scope recommendation | Conditional | The similar-profile review returns one or more matches | Verify | ORA_PER_PRSN_SEC_AOR_SCOPES | resolve_exact_aor_scope_from_common_lookup | Recommendations must use only scope values currently supported by the Person Security Profile screen | Review the exact AOR scope recommendation when one is available. If continuing the original design, explicitly confirm that AOR was reviewed and intentionally not selected. | Optional ScopeOfResponsibility and ScopeOfResponsibilityMeaning, and explicit exception confirmation |
| person_security_profile_csv_template | Current supported task CSV template | Yes | Generating a CSV import package | Verify | Current target-environment Manage Person Security Profile task template-only export | resolve_person_security_profile_csv_context | The template owns the supported CSV members, columns, mappings, import order, and metadata. Use its ViewInstanceName and GroupingKey pattern when declared; otherwise use the documented fallback. | Export the current template-only package and do not reuse another environment's template or invent a layout | Immutable layout context, template/fallback value source, and metadata evidence |
| person_security_profile_csv_package | Immutable supported CSV package | Yes | Preparing an import | Verify | Resolved template layout plus identified attributes | resolve_person_security_profile_csv_context | The CSV package must be built only from the current supported template layout; a missing ViewInstanceName or GroupingKey declaration uses the documented fallback | Preserve the template package structure and metadata, map only identified attributes through the resolved layout, use an uppercase 32-character hexadecimal GUID without separators as GroupingKey for each new row when required, and retain an immutable preview | Immutable CSV ZIP preview |
| person_security_profile_csv_mutation_route | Core Data Loader-only mutation route | Yes | Creating or updating a person security profile | Verify | Immutable CSV preview, explicit approval, core.data-loader task-level import, and process log | | Person security profile configuration changes are permitted only through core.data-loader after approval and process-log verification | Never use REST POST, PUT, or PATCH to create or update a person security profile; approve the exact package, run one core.data-loader import, and verify the result | Approval record and import process log |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Blocked | Attributes, required similar-profile AOR review, current template layout, immutable preview, approval, or verification plan is missing | No |
| Ready | All CSV layout, package, and import-route dependencies are satisfied | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSP.CSV_READINESS | decision | 8 | resolve_dependency | ready->PSP.READY;blocked->PSP.ERROR | PSP.RESOLVE_CSV_LAYOUT | stop | A supported CSV import package is being generated or imported |
