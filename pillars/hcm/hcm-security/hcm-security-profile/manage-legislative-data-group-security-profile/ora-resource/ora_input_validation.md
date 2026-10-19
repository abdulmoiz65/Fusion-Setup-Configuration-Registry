# Legislative Data Group Security Profile Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Security profile identity | A supplied Name or a Name derived from validated configuration, current target-environment task template, resolved legislative data group values, and CSV context | Stop | Preserve a supplied Name exactly as provided (up to the source-schema limit of 240 characters), or derive LDGSP plus a compact geographic scope inferred from the configured validated LegislativeDataGroupName values: use one shared region when clearly indicated, otherwise use distinct country scopes in configured order; retain only ASCII letters and digits and limit a derived Name to 119 characters, then export the current template, resolve legislative data group values, and prepare the template-backed CSV package | Creating a security profile | verify_ldg_security_profile_name_unique |
| Existing profile identity | Current Name and LegislativeDataGroupSecurityProfileId; proposed new Name for a rename | Stop | Resolve the old exact Name to one profile and require its returned ID to equal the supplied current ID before checking the proposed new Name | Updating or renaming an existing profile | find_ldg_security_profile_by_exact_name |
| Legislative data group association | One or more LegislativeDataGroupName values and their derived LegislativeDataGroupId values | Stop | Provide at least one legislative data group name; resolve each identifier through the documented LOV mapping | Creating or updating a legislative data group security profile | resolve_legislative_data_group_by_name |
| Existing profile target | LegislativeDataGroupSecurityProfileId and current target-environment template-backed CSV context | Stop | Resolve one current profile by exact Name, export the current template, and resolve exact parent-child CSV linkage before an update | Updating a profile or its child collection | find_ldg_security_profile_by_exact_name |
| Supported CSV package layout | Current template-only export with resolver-identified parent and child members, exact headers and order, parent-child linkage, template-derived or fallback ViewInstanceName and GroupingKey values, and ASM_SETUP_CSV_METADATA.xml | Stop | Start from the current supported package; generate rows only from the resolver output. A missing migration value uses the documented parent or child fallback; retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged | Generating a CSV import package | resolve_current_task_csv_layout |
| CSV-only mutation package | Current target-environment task template, immutable ZIP preview, exact approval, one task-level import, and process-log verification | Stop before any create or update | Use the core.data-loader-authorized task-level CSV import workflow; do not construct or submit a direct REST mutation | Creating or updating a legislative data group security profile | resolve_ldg_security_profile_csv_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A supplied Name is empty or exceeds the source-schema limit of 240 characters | Blocked | Supply a valid Name of no more than 240 characters; preserve its supplied characters and length |  |
| A derived Name has no reasonably inferred country or regional scope, is empty, contains a character other than an ASCII letter or digit, or exceeds 119 characters | Blocked | Derive LDGSP plus one shared inferred region or distinct inferred country scopes, retaining only ASCII letters and digits and truncating it to 119 characters, or request a user-supplied Name |  |
| No legislative data group association is supplied | Blocked | Supply at least one LegislativeDataGroupName and resolve its identifier | resolve_legislative_data_group_by_name |
| A child association is requested but the legislative data group name cannot be resolved to one identifier | Blocked | Supply a disambiguating name or the documented lookup contract | resolve_legislative_data_group_by_name |
| An existing profile is required but Name resolves to zero or multiple profiles | Blocked | Supply an unambiguous profile identity | find_ldg_security_profile_by_exact_name |
| A CSV package is requested without a current supported task package | Blocked | Export the task data; do not invent CSV columns, keys, package members, or child-row structure | resolve_current_task_csv_layout |
| Parent or child CSV rows differ from the resolver-identified member, header, mapping, linkage, ViewInstanceName, or GroupingKey output | Blocked | Rebuild the rows from the current template resolver output or the documented member-specific fallback before preview | resolve_current_task_csv_layout |
| A create or update lacks template-backed CSV context, immutable preview, exact approval, one import, or process-log verification | Blocked | Export the current target-environment template and use the approved CSV-only workflow; do not derive CSV mappings from a REST payload | resolve_ldg_security_profile_csv_context |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Profile Name availability | For a create or genuine rename, require zero exact matches for the proposed Name. An exact match with another profile or multiple matches blocks. If proposed Name equals current Name, use the unchanged-name update route. | A profile is created or a genuine rename is requested | verify_ldg_security_profile_name_unique |
| Rename CSV identity mapping | Block with `rename CSV identity mapping unverified` before CSV preview or import; never infer update keys from REST IDs or name-based GroupingKey fallbacks | A genuine rename passes name availability |  |
| Name | For a supplied Name, preserve the value exactly as supplied and accept up to 240 characters. For a new profile without a supplied Name, derive LDGSP plus the geographic scope inferred from validated LegislativeDataGroupName values: append one shared region when clearly indicated; otherwise append distinct country scopes in configured order; do not concatenate full LDG names; remove all non-alphanumeric characters and truncate to 119 characters | Always |  |
| EnabledFlag | Accept a boolean; it is updateable and defaults to true | The flag is supplied |  |
| ViewAllFlag | Do not accept a user-supplied value because the describe contract marks it non-updateable | Always |  |
| LegislativeDataGroupName | Require one or more strings of at most 240 characters and use the LOV mapping to derive each LegislativeDataGroupId | Always | resolve_legislative_data_group_by_name |
| LegislativeDataGroupId | Require an integer derived from the selected legislative data group name | A child association is supplied | resolve_legislative_data_group_by_name |
| RemoveRow | Accept Y only when removing an existing child association | Removing a child association |  |
| Parent CSV layout | Use only the resolver-identified parent member, exact header order, field mappings, ViewInstanceName, and GroupingKey pattern | A CSV package is supplied | resolve_current_task_csv_layout |
| Child CSV layout | Use only the resolver-identified child member, exact header order, parent-child linkage, field mappings, ViewInstanceName, and GroupingKey pattern | A CSV package is supplied | resolve_current_task_csv_layout |
| Package metadata | Retain ASM_SETUP_CSV_METADATA.xml unchanged from the current supported package | A CSV package is supplied | resolve_current_task_csv_layout |
| CSV mapping source | Derive parent and child CSV fields only from the current task template and resolved lookup values; never derive them from a REST payload | Always for a create or update | resolve_ldg_security_profile_csv_context |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.VALIDATE | decision | 1 | validate_input | new_profile->LDGSP.VERIFY_PROFILE_NAME;existing_or_renamed_profile->LDGSP.FIND_PROFILE;invalid->LDGSP.ERROR | none | stop | A profile request is supplied; a proposed Name equal to current Name is an unchanged-name update |
