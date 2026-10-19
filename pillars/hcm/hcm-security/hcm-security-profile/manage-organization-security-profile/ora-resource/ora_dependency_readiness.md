# Organization Security Profile Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Profile identity and Name availability | For a rename, resolve the old exact Name and match its ID to the supplied current ID. Then require zero exact matches for the proposed new Name. An unchanged proposed Name follows the update route. |
| 2 | FSM task CSV export metadata | Inspect ASM_SETUP_CSV_METADATA.xml from the export and validate the reusable task and package contract before using the export as an import baseline |
| 3 | Template-derived CSV layout | Resolve the current template-only export's members, exact headers and order, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, and metadata node order. When migration values are absent, use the documented member-specific fallbacks; retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged |
| 4 | Input validation | Validate the requested profile values and selected criteria |
| 5 | Reference resolution | Resolve only the documented values needed by the selected criteria, including the exact Department Tree code when a Department Tree hierarchy is used |
| 6 | Package integrity | Build the CSV package only after the metadata contract, template-derived layout, resolved values, parent-child linkage, and Department Tree parent-field mapping validate |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ORG-PROFILE-NAME-AVAILABILITY | Proposed Name availability | Yes | A profile is created or a genuine rename is requested | Verify | organizationSecurityProfilesLOV through core.fusion-api.rest-api-client | verify_organization_security_profile_name_unique | The proposed Name must have zero exact matches; a rename first verifies the old profile identity | Supply an available new Name; an existing exact match is a collision | Proposed Name availability and exact-match count |
| ORG-PROFILE-TARGET | Existing profile identity | Conditional | Updating or renaming a profile | Lookup | organizationSecurityProfilesLOV through core.fusion-api.rest-api-client | find_organization_security_profile_by_exact_name | Resolve the old exact Name to one profile; for rename require its ID to equal the supplied current ID | Supply the current Name and ID for a rename; stop on no match, ambiguity, or ID mismatch | Verified OrganizationSecurityProfileId |
| ORG-RENAME-CSV | Rename CSV identity mapping | Yes | A genuine rename has passed proposed-name availability | Blocked | Current target-environment task template |  | The current contract does not prove how the existing parent and children retain update identity across a Name change | Stop with `rename CSV identity mapping unverified`; do not prepare preview or import or infer update keys from REST IDs or name-based GroupingKey fallbacks | No import-ready rename mapping |
| ORG-FSM-CSV-METADATA | FSM task CSV export metadata | Yes | An FSM task CSV export is validated or used as an import baseline | Verify | Generated ASM_SETUP_CSV_METADATA.xml from the exported task package | verify_fsm_task_csv_metadata | The generated export proves the task identity, included business objects, field contracts, migration batch and service, node sequence, and export process status | Use exactly one metadata member from the same export as the CSV files. Preserve it unchanged. Do not retain or reuse environment, submitter, timestamps, ESS request IDs, or process IDs. | Task identity; process status; business-object names; field-contract lists; batch name; service name; batch size; object sequence |
| ORG-FSM-CSV-LAYOUT | Template-derived CSV layout | Yes | Generating or importing an Organization Security Profile CSV package | Verify | Current target-environment template-only export and validated metadata | resolve_organization_security_profile_csv_context | The package can be generated only when members, headers, mappings, linkage, and metadata derive from the current template. ViewInstanceName and GroupingKey use the template when declared, otherwise the documented member-specific fallback. | Use only the resolver's member names, exact header arrays and order, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, and metadata node order. When the template omits migration values, use OrgSecurityProfileMigration with Org Security profile name for PER_ORG_SECURITY_PROFILES.csv, OrgSecurityProfileOrgMigration with Org Security profile name,Organization Name,Organization Classification Name for ORA_PER_ORG_SEC_PROFILE_ORGS.csv, and OrgSecurityProfileClassMigration with Org Security profile name,Classification Name for ORA_PER_ORG_SEC_PROFILE_CLASSES.csv. Do not use a hard-coded CSV column list. Retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged. | Immutable layout context and template-derived or fallback generated-row values |
| ORG-DEPARTMENT-TREE-PARENT-MAPPING | Department Tree parent CSV mapping | Yes | An organization-hierarchy profile CSV uses a Department Tree | Verify | Resolved Department Tree with PER_DEPT_TREE_STRUCTURE | resolve_department_tree_from_hcm_trees_lov | The parent hierarchy fields must identify the same resolved Department Tree. A display name alone cannot satisfy the OrgHierTreeCode foreign-key reference. | Set TreeName from the resolved TreeName, OrgHierTreeStructCode=PER_DEPT_TREE_STRUCTURE, and OrgHierTreeCode exactly to the resolved TreeCode. Stop if any value is missing or inconsistent; rebuild the preview from the resolved values. | TreeName; OrgHierTreeStructCode; OrgHierTreeCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A create has zero proposed-Name matches; an unchanged-name update has one verified old-name match; a genuine rename has a verified old Name and ID plus zero proposed-new-Name matches | Yes; read-only lookup only |
| Satisfied | The metadata identifies PER_MANAGE_ORGANIZATION_SECURITY_PROFILE as a completed task CSV export with the expected objects, field contracts, batch, service, and object order | No |
| Satisfied | The current template-only export resolves unambiguous members, headers, mappings, linkage, and metadata node order; ViewInstanceName and GroupingKey use template values or the documented member-specific fallback | No |
| Satisfied | A Department Tree hierarchy maps the resolved TreeName, PER_DEPT_TREE_STRUCTURE, and the exact resolved TreeCode to the parent CSV fields | No |
| Blocked | The metadata is missing, unreadable, identifies a different task, omits or changes an expected business object or field contract, or has an unsupported export process status | No |
| Blocked | An existing target is missing, ambiguous, or has a different ID; or a create or genuine rename has an exact proposed-Name match | No; correct the target identity or proposed Name |
| Blocked | A genuine rename passes name availability but parent and child CSV update identity across the rename is unverified | No; report `rename CSV identity mapping unverified` before preview or import |
| Blocked | The CSV template lacks an unambiguous member, header, mapping, linkage, or metadata contract | No |
| Blocked | A Department Tree hierarchy has a blank or mismatched OrgHierTreeCode, or its TreeName, structure code, and tree code do not describe the same resolved tree | No |
| Blocked | ProcessStatus is COMPLETED_WARNINGS | No; review the export warnings and resolve or explicitly accept them before using the export as a baseline |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORG.RENAME_CSV_GATE | decision | 13 | resolve_dependency | mapping_unverified->ORG.RETURN_ISSUES | ORG.VERIFY_PROFILE_NAME | stop | A genuine rename has an available new Name but its CSV parent and child update identity is unverified; block before preview or import |
| ORG.VERIFY_FSM_CSV_METADATA | decision | 14 | resolve_dependency | verified->ORG.RESOLVE_CSV_LAYOUT;completed_warnings->ORG.RETURN_ISSUES;invalid->ORG.RETURN_ISSUES | ORG.VALIDATE_INPUT | stop | An FSM task CSV export is validated or used as an import baseline |
