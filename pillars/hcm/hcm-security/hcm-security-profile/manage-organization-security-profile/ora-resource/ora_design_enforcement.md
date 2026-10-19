# Organization Security Profile Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm profile identity and proposed Name availability | For a rename, verify old exact Name and current ID, then require zero exact matches for the proposed new Name. An unchanged proposed Name is an update. |
| 2 | Confirm change scope | Confirm whether the request is profile-only or also explicitly authorizes reference-data changes |
| 3 | Select security criteria | Confirm the selected or not-selected state of organization hierarchy, organization classification, and organization list before resolving their reference candidates |
| 4 | Define the intended set | Select the criteria that implement the intended organization access |
| 5 | Evaluate combined criteria | Apply every selected criterion together |
| 6 | Validate top organization | Resolve the named top organization as an effective node of the selected tree, and repeat that check whenever the hierarchy changes |
| 7 | Validate Department Tree parent fields | For a Department Tree hierarchy, map TreeName and OrgHierTreeCode from the same resolved tree and use OrgHierTreeStructCode=PER_DEPT_TREE_STRUCTURE before preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile is created or a genuine rename is requested | Error | find_organization_security_profile_by_exact_name; verify_organization_security_profile_name_unique | A rename old exact Name does not resolve to one profile with the supplied current ID, or the proposed new Name has one or more exact matches; a create has any exact proposed-Name match | Correct the old identity or provide an available new Name; treat an unchanged proposed Name as an unchanged-name update | Yes |
| A genuine rename has an available new Name | Blocker |  | The current template-backed contract does not prove parent and child update identity across the Name change | Stop with `rename CSV identity mapping unverified` before CSV preview or import; do not infer update keys from REST IDs or name-based GroupingKey fallbacks | No |
| A profile is being planned, created, or changed | Error | | The selected or not-selected state of an applicable hierarchy, classification, or organization-list criterion is unknown before reference discovery | Confirm each applicable criterion, then resolve only the values required for every selected criterion | Yes |
| A request names hierarchy, classification, or organization-list inputs | Error | | A criterion-specific lookup would run before the request identifies which criteria are selected | Confirm the selected criteria; resolve all selected criteria together rather than treating them as alternatives | Yes |
| An FSM task CSV export is used as a package baseline | Error | verify_fsm_task_csv_metadata | The export metadata does not confirm the expected task, business objects, field contracts, batch/service, node order, and completed process status; or it reports COMPLETED_WARNINGS without warning review | Export the task again or review and resolve the warnings before building an import package. Keep run-specific export identity values out of reusable guidance. | Yes |
| An Organization Security Profile CSV package is generated or imported | Error | resolve_organization_security_profile_csv_context | A generated row differs from the template-derived member, header order, field mapping, parent-child linkage, metadata bytes, or metadata node order; or its ViewInstanceName or GroupingKey differs from the template output and applicable member-specific fallback | Re-export the current template-only package, rebuild the rows only from its resolver output, use the documented fallback only when the template omits a migration value, and retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged. Do not use a hard-coded CSV column list. | Yes |
| Profile-only scope is selected | Error | | An organization, Department, tree, or other reference-data record would be created or modified | Use existing reference values only; obtain explicit authorization and route to the relevant setup task for any reference-data change | Yes |
| More than one criterion is selected | Error | | Criteria are treated as alternatives | Evaluate their combined result before saving | Yes |
| A named top organization is selected | Error | resolve_top_organization_in_tree_nodes_lov | Page traversal finds no exact effective-dated logical node, more than one distinct logical node, or a supplied ID conflicts with the resolved node | Organization-hierarchy security only: maintain or replace the selection | Yes |
| A hierarchy profile CSV requires top-organization classification | Error | resolve_top_organization_classification_from_lov | The selected hierarchy node has no exact active effective organizationsLOV match with the same ID and a classification | Correct the selected hierarchy node or provide a supported classification through the resolved organization | Yes |
| An organization-hierarchy root is selected from a Department Tree | Error | resolve_department_tree_nodes_from_lov | The selected Department Tree does not return one exact, effective-dated DepartmentName and OrganizationId pair | Maintain or replace the selected Department Tree root | Yes |
| An organization-hierarchy CSV uses a Department Tree | Error | resolve_department_tree_nodes_from_lov | TopOrganizationName or TopOrganizationId is blank, or does not match the selected Department resolver output | Re-resolve the selected Department and regenerate the preview before import | Yes |
| An organization-hierarchy CSV uses a Department Tree | Error | resolve_department_tree_from_hcm_trees_lov | OrgHierTreeCode is blank, differs from the resolved TreeCode, or is populated with TreeName; or OrgHierTreeStructCode is not PER_DEPT_TREE_STRUCTURE | Map TreeName and OrgHierTreeCode from the same resolved Department Tree, set the documented structure code, then regenerate and approve a new preview. Do not retry a failed package. | Yes |
| The requested hierarchy top is the department from the user's assignment | Error | | TopOrgSelection is not U, or the setting is confused with IncludeTopOrganizationFlag | Set TopOrgSelection=U. Set IncludeTopOrganizationFlag separately to the requested access behavior. | Yes |
| The organization tree changes | Error | resolve_top_organization_in_tree_nodes_lov | The existing top organization has not been revalidated against the replacement tree version | Re-resolve or replace the top organization before generating the CSV package | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_organization_security_profile_by_exact_name | An existing profile is updated or renamed | Verified current Name and OrganizationSecurityProfileId | ora_reference_lookups.md |
| verify_organization_security_profile_name_unique | A profile is created or genuinely renamed | Proposed Name availability and exact-match count | ora_reference_lookups.md |
| resolve_top_organization_in_tree_nodes_lov | A named top organization is selected or the organization tree changes | TreeVersionId; TopOrganizationId; TopOrganizationName; RequestedEffectiveDate | ora_reference_lookups.md |
| browse_organization_tree_nodes_from_lov | A user requests top-organization candidates | TreeVersionId; RequestedEffectiveDate; OrganizationName; OrganizationId | ora_reference_lookups.md |
| resolve_top_organization_classification_from_lov | A hierarchy profile CSV requires top-organization classification | TopOrganizationId; TopOrganizationName; TopOrganizationClassificationCode; TopOrganizationClassificationName | ora_reference_lookups.md |
| resolve_department_tree_nodes_from_lov | An organization-hierarchy root is selected from a Department Tree | DepartmentName; OrganizationId; TopOrganizationName; TopOrganizationId | ora_reference_lookups.md |
| resolve_department_tree_from_hcm_trees_lov | A Department Tree hierarchy parent row is prepared | TreeCode; TreeName; TreeStructureCode; parent CSV TreeName; OrgHierTreeStructCode; OrgHierTreeCode | ora_reference_lookups.md |
| verify_fsm_task_csv_metadata | An FSM task CSV export is validated or used as an import baseline | Task identity; process status; business-object names; field contracts; batch/service; batch size; object sequence | ora_reference_lookups.md |
| resolve_organization_security_profile_csv_context | Before generating or importing an Organization Security Profile CSV package | Exact members, headers and order, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, metadata bytes, and node order | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORG.ENFORCE_DESIGN | decision | 18 | design_enforcement | compliant->ORG.EXECUTION_CONTRACT;blocked->ORG.RETURN_ISSUES | ORG.RESOLVE_ORGANIZATION_LOVS | stop | A profile is prepared for save |
