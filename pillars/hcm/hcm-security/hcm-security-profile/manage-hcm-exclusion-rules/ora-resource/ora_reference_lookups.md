# HCM Exclusion Rules Reference Lookups

Execute every read-only Fusion REST lookup in this file through
`core.fusion-api.rest-api-client`; do not issue a direct REST request.

Resolve all Common Lookup values through
`hcm.hcm-security.hcm-security-common.manage-common-lookups`; do not call a Common Lookups
REST endpoint directly from this task. The task-specific LOV paths below use
the developer-supplied format
https://{fusion_environment_host}/hcmRestApi/resources/{version}/{lov_resource};
resolve the host and version at runtime. No match blocks import and requires a
corrected value.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_exclusion_type_from_common_lookup | Exclusion Type is supplied | `hcm.hcm-security.hcm-security-common.manage-common-lookups`; lookupType=ORA_PER_EXCLUSION_TYPE; supplied exclusion type code | Match the supplied code within the exact lookupType | Exclusion Type from LookupCode; meaning from Meaning | Stop and request a valid unambiguous exclusion type code |
| resolve_attribute_operator_from_common_lookup | An attribute-based exclusion criterion is configured | `hcm.hcm-security.hcm-security-common.manage-common-lookups`; lookupType=ORA_PER_EXCLUSION_OPERATORS; supplied operator type code | Match the supplied code within the exact lookupType | Operator Type from LookupCode; meaning from Meaning | Stop and request a valid unambiguous operator type code |
| resolve_hcm_exclusion_rule_csv_layout | A CSV import package is prepared | Current target-environment template-only HCM Exclusion Rules export and its ASM_SETUP_CSV_METADATA.xml, plus the task CSV criterion-mapping rules below | Derive every importable CSV member, exact header arrays and order, row relationships, ViewInstanceName values, GroupingKey patterns, and metadata node order from the current template. Apply the documented criterion mappings only to the resolver-identified detail member and headers: a non-country list resolved identifier goes in IdValue; a country-list resolved territory value goes in Value; an attribute criterion uses FlexContext, ColumnName, TableName, Operator, and AttributeValue; a Department Hierarchy or Department Tree criterion uses TreeCode and TopNodeValue; a Position Hierarchy or Supervisor Hierarchy criterion uses TopNodeValue. When the template omits a ViewInstanceName, use ExclusionRuleMigration for ORA_PER_HCM_EXCLUSION_RULE.csv or ExclusionRuleDetailMigration for ORA_PER_HCM_EXCLUSION_RULE_DETAIL.csv. For each new row, generate a distinct uppercase 32-character hexadecimal GUID using only 0-9 and A-F, such as 551F45B6C8A2445BE0534280F50A76B1, and use it as that row's GroupingKey when the template omits the pattern. Retain ASM_SETUP_CSV_METADATA.xml exactly once and byte-for-byte unchanged. | Immutable layout context: member names; exact headers and order; row relationships; documented criterion mappings; template-derived or fallback ViewInstanceName values; template-derived or generated GroupingKey values; metadata bytes and node order | Stop before preview or import if any required member, header, criterion mapping, relationship, or metadata evidence is missing, ambiguous, or inconsistent. A missing ViewInstanceName or GroupingKey pattern alone uses the documented member-specific fallback. Export a fresh template-only package. Do not invent columns, linkage, or migration values beyond the supplied fallbacks. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_business_unit_id_from_hcm_business_units_lov | Business Unit List is selected | Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/hcmBusinessUnitsLOV | BusinessUnitId | Match Name exactly | idValue from BusinessUnitId | Stop and request a correct value |
| resolve_department_id_from_departments_lov | Department List is selected | Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/departmentsLov | OrganizationId | Match Name exactly | idValue from OrganizationId | Stop and request a correct value |
| resolve_grade_id_from_grades_lov | Grade List is selected | Name; Grade Code and Set Name only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/gradesLov | GradeId | Match Name exactly; when multiple matches are returned, require Grade Code and Set Name | idValue from GradeId | Stop and request a correct value when no match or the additional values do not identify exactly one grade |
| resolve_job_family_id_from_job_families_lov | Job Family List is selected | JobFamilyName; Job Family Code only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/jobFamiliesLov | JobFamilyId | Match JobFamilyName exactly; when multiple matches are returned, require Job Family Code | idValue from JobFamilyId | Stop and request a correct value when no match or the additional value does not identify exactly one job family |
| resolve_job_id_from_jobs_lov | Job List is selected | JobName; Job Code and Set Name only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/jobsLov | JobId | Match JobName exactly; when multiple matches are returned, require Job Code and Set Name | idValue from JobId | Stop and request a correct value when no match or the additional values do not identify exactly one job |
| resolve_legal_employer_id_from_legal_employers_lov | Legal Employer List is selected | Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/legalEmployersLov | OrganizationId | Match Name exactly | idValue from OrganizationId | Stop and request a correct value |
| resolve_location_id_from_locations_lov | Work Location List is selected | LocationName; Location Code and Set Name only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/locationsLov | LocationId | Match LocationName exactly; when multiple matches are returned, require Location Code and Set Name | idValue from LocationId | Stop and request a correct value when no match or the additional values do not identify exactly one location |
| resolve_person_id_from_workers_lov | Person List is selected | DisplayName; Person Number only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/workersLov?finder=findByWord;DataSecurityPrivilege=PwaViewAll,FilterAttributes=DisplayName PersonNumber WorkEmailAddress,SearchTerms={DisplayName}&fields=PersonId | PersonId | Partial-match DisplayName; when multiple matches are returned, require Person Number | idValue from PersonId | Stop and request a correct value when no match or Person Number does not identify exactly one person |
| resolve_position_id_from_positions_lov | Position List is selected | PositionName; Position Code only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/positionsLov | PositionId | Match PositionName exactly; when multiple matches are returned, require Position Code | idValue from PositionId | Stop and request a correct value when no match or Position Code does not identify exactly one position |
| resolve_country_territory_code_from_hcm_countries_lov | Country List is selected | CountryName | https://{fusion_environment_host}/hcmRestApi/resources/{version}/hcmCountriesLov | TerritoryCode | Match CountryName exactly | Value from TerritoryCode | Stop and request a correct value |
| resolve_department_tree_code_from_hcm_trees_lov | Department Hierarchy or Department Tree is selected | Tree Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/hcmTreesLOV?finder=findByWord;TreeStructureCode=PER_DEPT_TREE_STRUCTURE | TreeCode | Match Tree Name exactly | TreeCode | Stop and request a correct value |
| resolve_top_department_id_from_departments_lov | Department Hierarchy or Department Tree top department is selected | Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/departmentsLov | OrganizationId | Match Name exactly | TopNodeValue from OrganizationId | Stop and request a correct value |
| resolve_hierarchy_top_position_id_from_positions_lov | HCM Position Hierarchy is selected | PositionName; PositionCode only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/positionsLov | PositionId | Match PositionName exactly; when multiple matches are returned, require PositionCode | TopNodeValue from PositionId | Stop and request a correct value when no match or PositionCode does not identify exactly one position |
| resolve_top_manager_person_id_from_workers_lov | Supervisor Hierarchy is selected | DisplayName; Person Number only when needed | https://{fusion_environment_host}/hcmRestApi/resources/{version}/workersLov?finder=findByWord;DataSecurityPrivilege=PwaViewAll,FilterAttributes=DisplayName PersonNumber WorkEmailAddress,SearchTerms={DisplayName}&fields=PersonId | PersonId | Partial-match DisplayName; when multiple matches are returned, require Person Number | TopNodeValue from PersonId | Stop and request a correct value when no match or Person Number does not identify exactly one manager |
| resolve_exclusion_rule_attribute_from_lov | An attribute-based exclusion criterion is configured | Selected ExclusionType and AttributeDisplayName | https://{fusion_environment_host}/hcmRestApi/resources/{version}/exclusionRuleAttributesLOV?finder=findByExclusionType;ExclusionType={ExclusionType}&fields=FlexfieldContextCode,AttributeDisplayName,ColumnName,TableName,ExclusionType | FlexfieldContextCode, AttributeDisplayName, ColumnName, TableName, ExclusionType | Partial-match AttributeDisplayName within the selected ExclusionType; when multiple results are returned, require an exact attribute | FlexfieldContextCode, ColumnName, and TableName | Stop and request an exact attribute when no match or multiple results remain |
| resolve_set_id_from_set_id_sets | An attribute exclusion maps to ColumnName SET_ID and the supplied comparison is a reference-data SetName or SetCode | SetName or SetCode | https://{fusion_environment_host}/fscmRestApi/resources/11.13.18.05/setIdSets | SetId, SetCode, SetName | Match the supplied SetName exactly or the supplied SetCode exactly. When both are supplied, require both values to identify the same exactly one row. | AttributeSetCode from SetCode; AttributeValue from SetId | Stop and request a valid unambiguous SetName or SetCode; do not substitute a different set, retain the name/code in AttributeValue, or omit the returned SetCode from AttributeSetCode |
| resolve_exclusion_rule_by_name_with_children | An exclusion-rule Name is supplied or derived and its child rows must be reconciled | Name and ExclusionType | https://{fusion_environment_host}/hcmRestApi/resources/{version}/exclusionRules?q=Name={Name}&expand={resolved child collection} | ExclusionRuleId, Name, ExclusionType, and the selected type-specific child collection including ExclusionRuleDetailId and its documented identity fields | Match Name exactly. Select the one child collection mapped from the supplied ExclusionType. If a returned same-name parent has a different ExclusionType, stop. | Existing ExclusionRuleId and selected child rows, including ExclusionRuleDetailId | No matching parent means prepare a new parent and child rows. Multiple exact parents, a mismatched ExclusionType, or an unsupported child collection blocks package preparation. |

## Exclusion-Type Child Collection Mapping

| ExclusionType | Child Collection | Child Identity for Reconciliation |
|---|---|---|
| ORA_EXCL_BU_LIST | businessUnits | BusinessUnitId |
| ORA_EXCL_CNT_LIST | countries | CountryCode |
| ORA_EXCL_DEPT_LIST | departments | DepartmentId |
| ORA_EXCL_GRD_LIST | grades | GradeId |
| ORA_EXCL_JOBFAM_LIST | jobFamilies | JobFamilyId |
| ORA_EXCL_JOB_LIST | jobs | JobId |
| ORA_EXCL_LE_LIST | legalEmployers | LegalEmployerId |
| ORA_EXCL_LOC_LIST | locations | LocationId |
| ORA_EXCL_PER_LIST | persons | PersonId |
| ORA_EXCL_POS_LIST | positions | PositionId |
| ORA_EXCL_DEPT_ATTR, ORA_EXCL_GRD_ATTR, ORA_EXCL_JOB_ATTR, ORA_EXCL_LOC_ATTR, ORA_EXCL_PER_ATTR, ORA_EXCL_POS_ATTR | attribute | FlexfieldContext, TableName, AttributeName |
| ORA_EXCL_DEPT_HIER | departmentHierarchy | DepartmentTreeCode, TopDepartmentId |
| ORA_EXCL_HCMPOS_HIER | positionHierarchy | TopPositionId |
| ORA_EXCL_MGR_HIER | supervisorHierarchy | SupervisorId |

## Resolver Audit Crosswalk

| Retired Resolver Name | Replacement Resolver | Reason |
|---|---|---|
| check_exclusion_rule_name_duplicate | resolve_exclusion_rule_by_name_with_children | Same-name rules now reconcile the returned parent and selected child collection rather than blocking solely because the parent exists. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A required value belongs to a Common Lookup | Invoke `hcm.hcm-security.hcm-security-common.manage-common-lookups` with the exact lookup type before using the value. Do not substitute a direct Common Lookups REST request. |
| No matching LOV row is returned | Block import and ask for a correct value |
| A documented duplicate result requires a disambiguator | Stop and request the documented code, set name, or person number; do not select a row by guesswork |
| An attribute lookup returns duplicate results | Stop and request an exact attribute; do not select an attribute by guesswork |
| An exact exclusion-rule Name is returned by exclusionRules with its selected child collection expanded | Reconcile the existing parent and child rows through resolve_exclusion_rule_by_name_with_children; do not create a duplicate parent. |
| An exact existing parent is reconciled | Populate the parent CSV ExclusionRuleId with the returned ExclusionRuleId before reconciling detail rows. |
| A list-exclusion child row has the same documented child identity as a returned child row | Do not add a new detail CSV row for that child. |
| An attribute, Department Hierarchy, Position Hierarchy, or Supervisor Hierarchy child row is returned | Populate ExclusionRuleDtlId with the returned child identifier and update that same detail row; do not create another child row. |
| The HCM exclusion-rule CSV layout cannot resolve a member, header, mapping, row relationship, or metadata contract | Stop before package preparation. Require a fresh task export and do not fabricate members, headers, mappings, or row relationships. A missing ViewInstanceName or GroupingKey pattern alone uses the documented fallback. |
| A non-country list exclusion is prepared for the detail CSV row | Place its resolved identifier in IdValue; do not place it in Value, TreeCode, TopNodeValue, or an attribute field. |
| A country-list exclusion is prepared for the detail CSV row | Place its resolved TerritoryCode in Value; do not place it in IdValue. |
| An attribute exclusion is prepared for the detail CSV row and its resolved ColumnName is not SET_ID | Populate FlexContext, ColumnName, TableName, Operator, and literal AttributeValue. Use Global Segment for FlexContext when the selected attribute is a global segment. |
| An attribute exclusion maps to ColumnName SET_ID and a SetName or SetCode is supplied | Resolve the supplied set through setIdSets; populate the returned SetCode in AttributeSetCode and the returned SetId in AttributeValue. Do not retain the supplied SetName or SetCode in AttributeValue. |
| A Department Hierarchy or Department Tree exclusion is prepared for the detail CSV row | Populate TreeCode and TopNodeValue; do not use IdValue for either hierarchy value. |
| A Position Hierarchy or Supervisor Hierarchy exclusion is prepared for the detail CSV row | Populate TopNodeValue; do not use IdValue for the top position or manager. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMEX.RESOLVE_REFERENCES | step | 30 | reference_lookup | resolved->HCMEX.ENFORCE;missing->HCMEX.RETURN_ISSUES | HCMEX.APPLY_DEFAULTS | stop | An HCM exclusion rule has supplied a name, exclusion type, list, hierarchy, or attribute value requiring resolution |
