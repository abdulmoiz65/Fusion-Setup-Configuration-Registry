# Legislative Data Group Security Profile Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Profile identity and Name availability | For a rename, resolve the old exact Name and match its ID to the supplied current ID. Then require zero exact matches for the proposed new Name. An unchanged proposed Name follows the update route. |
| 1 | Official task template | Export and retain the current target-environment template-only package; derive its parent and child members, exact headers and order, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, and node order. When migration values are absent, use the documented member-specific fallbacks; retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged |
| 2 | Profile identity | Validate the profile Name and resolve one existing profile identifier when an update or child operation needs it |
| 3 | Legislative data group identity | Resolve at least one selected Name to one LegislativeDataGroupId before the security profile is ready |
| 4 | Supported CSV layout | Resolve the exact parent, child, and metadata package members, header arrays, field mappings, parent-child linkage, ViewInstanceName values, and GroupingKey patterns before mapping data; use the documented member-specific fallback only when the template omits a migration value |
| 5 | Parent CSV row | Map the profile only to the resolver-identified parent member and its exact header, mapping, ViewInstanceName, and GroupingKey output |
| 6 | Child CSV row | Map every selected legislative data group only to the resolver-identified child member and its exact header, linkage, mapping, ViewInstanceName, and GroupingKey output |
| 7 | Immutable import | Build the CSV ZIP from the current template, obtain approval of the exact preview, submit one task-level import through core.data-loader, and verify its process log |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ldg_security_profile_name_availability | Proposed Name availability | Yes | A profile is created or a genuine rename is requested | Verify | legislativeDataGroupSecurityProfiles through core.fusion-api.rest-api-client | verify_ldg_security_profile_name_unique | The proposed Name must have zero exact matches; a rename first verifies the old profile identity | Supply an available new Name; an existing exact match is a collision, not proof of rename identity | Proposed Name availability and exact-match count |
| LDGSP-PROFILE | Existing profile identity | Conditional | Updating, renaming, or changing a child collection | Lookup | Parent collection response and current template-backed CSV context | find_ldg_security_profile_by_exact_name | Resolve the old exact Name to one profile; for rename require its ID to equal the supplied current ID before checking the proposed Name | Supply the current Name and ID for a rename; stop on no match, ambiguity, or ID mismatch | Verified LegislativeDataGroupSecurityProfileId |
| LDGSP-RENAME-CSV | Rename CSV identity mapping | Yes | A genuine rename has passed proposed-name availability | Blocked | Current target-environment task template |  | The current contract does not prove how the existing parent and children retain update identity across a Name change | Stop with `rename CSV identity mapping unverified`; do not prepare preview or import or infer update keys from REST IDs or name-based GroupingKey fallbacks | No import-ready rename mapping |
| LDGSP-LDG | Legislative data group identity | Yes | Creating or updating a legislative data group security profile | Lookup | legislativeDataGroupsLOV | resolve_legislative_data_group_by_name | At least one legislative data group must be present and each child association requires LegislativeDataGroupId | Supply at least one exact Name | LegislativeDataGroupId |
| LDGSP-CSV-LAYOUT | Supported CSV package layout | Yes | Generating a create or update CSV import package | Verify | Current target-environment template-only export | resolve_current_task_csv_layout | The task supports CSV import only when every generated member, header, mapping, linkage, and metadata byte derives from the current export. ViewInstanceName and GroupingKey use the template when declared, otherwise the documented member-specific fallback. | Export the current template and use its resolved members, header arrays, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, and metadata node order. When the template omits those migration values, use LDGSecurityProfileMigration with the LDG Security profile name for PER_LDG_SECURITY_PROFILES, and LDGSecurityProfileLdgMigration with LDG Security profile name,LDG Name for ORA_PER_LDG_SECURITY_PROFILES_LDGS.csv. Do not derive mappings or other migration values from REST payloads. | Immutable layout context, including exact members, headers, mappings, linkage, template-derived or fallback ViewInstanceName and GroupingKey values, metadata bytes, and node order |
| LDGSP-CSV-PARENT | Parent profile row | Yes | Generating a CSV import package | Verify | Prepared parent row and resolved template layout | resolve_current_task_csv_layout | The parent profile must be represented before its legislative data group children using only the layout resolved from the current template | Map the parent row only to the resolver-identified member, exact header order, field mappings, ViewInstanceName, and GroupingKey pattern | Parent row and its resolver-validated member, header, ViewInstanceName, and GroupingKey |
| LDGSP-CSV-CHILD | Legislative data group child row | Yes | Generating a CSV import package | Verify | Prepared child rows, resolved legislative data groups, and resolved template layout | resolve_current_task_csv_layout | Each child row belongs to one parent profile and requires the selected legislative data group identity and resolver-identified parent linkage | Map child rows only to the resolver-identified member, exact header order, parent-child linkage, field mappings, ViewInstanceName, and GroupingKey pattern | Child rows with resolver-validated linkage, ViewInstanceName, GroupingKey, and legislative data group identity |
| LDGSP-CSV-METADATA | Package metadata | Yes | Generating a CSV import package | Satisfied | Current exported ASM_SETUP_CSV_METADATA.xml |  | The metadata defines the supported migration service and parent-before-child node order | Retain ASM_SETUP_CSV_METADATA.xml unchanged from the current supported export | Metadata file and parent-before-child import order |
| LDGSP-CSV-MUTATION | CSV-only mutation route | Yes | Creating or updating a legislative data group security profile | Verify | Current target-environment task template, immutable preview, explicit approval, and task-level import process log | resolve_ldg_security_profile_csv_context | This task supports mutation only through its core.data-loader-authorized task-level CSV import workflow | Do not use direct REST POST, PATCH, PUT, or DELETE; submit one approved CSV import and verify the returned process log | Immutable CSV ZIP preview; approval record; import process log |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A create has zero proposed-Name matches; an unchanged-name update has one verified old-name match; a genuine rename has a verified old Name and ID plus zero proposed-new-Name matches | Yes; read-only lookup only |
| Blocked | An existing target is missing, ambiguous, or has a different ID; or a create or genuine rename has an exact proposed-Name match | No; correct the target identity or proposed Name |
| Blocked | A genuine rename passes name availability but parent and child CSV update identity across the rename is unverified | No; report `rename CSV identity mapping unverified` before preview or import |
| Lookup | A documented read-only contract is available | Lookup only |
| Blocked | No legislative data group is supplied or Name does not resolve uniquely | No |
| Blocked | Current supported CSV layout is unavailable | No |
| Blocked | Parent or child rows differ from the resolver-identified member, header, mapping, linkage, ViewInstanceName, GroupingKey, or metadata node order | No |
| Blocked | The metadata file is missing or altered | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.RENAME_CSV_GATE | decision | 4 | resolve_dependency | mapping_unverified->LDGSP.ERROR | LDGSP.VERIFY_PROFILE_NAME | stop | A genuine rename has an available new Name but its CSV parent and child update identity is unverified; block before preview or import |
| LDGSP.READINESS | decision | 7 | resolve_dependency | ready->LDGSP.ENFORCE;blocked->LDGSP.ERROR | LDGSP.DEFAULT | stop | Validated values are ready for the task-local execution contract |
