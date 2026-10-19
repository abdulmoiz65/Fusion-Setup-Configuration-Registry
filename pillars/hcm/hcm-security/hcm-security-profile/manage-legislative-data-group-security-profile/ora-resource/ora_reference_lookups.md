# Legislative Data Group Security Profile Reference Lookups

Execute every read-only Fusion REST lookup in this file through
`core.fusion-api.rest-api-client`; do not issue a direct REST request. Replace
`{fusion_environment_host}` and `{version}` at runtime with the live Fusion
environment host and active REST API version.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_current_task_csv_layout | A supported CSV import package is requested | Current target-environment template-only export for PER_MANAGE_LEGISLATIVE_DATA_GROUP_SECURITY_PROFILE | Require exactly one template package. Derive its parent and child CSV member names, exact header arrays and order, parent-child linkage fields, field mappings, ViewInstanceName values, GroupingKey patterns, and metadata node order. When the template omits a ViewInstanceName or GroupingKey pattern, use these member-specific fallbacks: PER_LDG_SECURITY_PROFILES uses LDGSecurityProfileMigration and the LDG Security profile name; ORA_PER_LDG_SECURITY_PROFILES_LDGS.csv uses LDGSecurityProfileLdgMigration and the LDG Security profile name, a comma, and the LDG Name in that order. Retain exactly one ASM_SETUP_CSV_METADATA.xml member byte-for-byte unchanged. | Immutable layout context: member names; exact parent and child header arrays; field mappings; parent-child linkage; template-derived or fallback ViewInstanceName values; template-derived or fallback GroupingKey values; metadata bytes and node order | Missing, ambiguous, or inconsistent member, header, mapping, linkage, or metadata evidence: stop before preview or import and export a fresh template. A missing ViewInstanceName or GroupingKey pattern alone uses the documented fallback. Do not invent columns or other migration values. |
| resolve_ldg_security_profile_csv_context | A legislative data group security profile create or update is prepared | Resolved current task CSV layout, resolved legislative data group values, parent/child CSV rows, immutable preview, approval record, and process log | Require every generated row to use the resolver's exact member, header order, field mapping, parent-child linkage, ViewInstanceName, and GroupingKey output. Bind approval to the immutable ZIP; require exactly one import result with a process log. | Template-backed parent/child context, migration values, grouping-key values, preview fingerprint, approval record, and process-log evidence | Stop; do not derive CSV mappings or migration values from REST payloads, submit a direct REST mutation, reuse stale approval, or generate a row when the template output is incomplete. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_ldg_security_profile_name_unique | A profile is created or a genuine rename is requested after old-profile identity is verified | Proposed Name | GET /hcmRestApi/resources/{version}/legislativeDataGroupSecurityProfiles through core.fusion-api.rest-api-client | LegislativeDataGroupSecurityProfileId, Name | Retain only rows whose Name exactly equals the proposed Name. For a create or genuine rename, zero matches means the Name is available. A proposed Name equal to the verified current Name is an unchanged-name update, not a rename. | Proposed Name availability and exact-match count | One or more exact matches block a create or genuine rename; do not treat an existing other-profile match as available. Multiple matches are ambiguous. A genuine rename with zero matches proceeds only to LDGSP.RENAME_CSV_GATE, never to CSV preview. |
| find_ldg_security_profile_by_exact_name | An existing profile, rename target, or child association must be identified | Current exact Name; supplied current LegislativeDataGroupSecurityProfileId for a rename | https://{fusion_environment_host}/hcmRestApi/resources/{version}/legislativeDataGroupSecurityProfiles | LegislativeDataGroupSecurityProfileId, Name, EnabledFlag, ViewAllFlag | Require exactly one returned profile whose Name exactly equals the current Name; for a rename, require its ID to equal the supplied current ID before checking the proposed Name | Verified current LegislativeDataGroupSecurityProfileId, Name, EnabledFlag, ViewAllFlag | Stop on zero or multiple old-name matches, or a mismatch with the supplied current ID; never use the proposed new Name to identify the old profile |
| resolve_legislative_data_group_by_name | A legislative data group association is required | Name | https://{fusion_environment_host}/hcmRestApi/resources/{version}/legislativeDataGroupsLOV | Name, LegislativeDataGroupId | Require exactly one legislative data group whose Name exactly equals the supplied Name | LegislativeDataGroupId | Stop and request a disambiguating Name |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The profile lookup returns exactly one profile | Use the returned identifier only for the current scoped task operation |
| The profile lookup returns zero or multiple profiles | Stop; do not select a profile by guesswork |
| The legislative data group lookup returns exactly one row | Use LegislativeDataGroupId for the selected legislative data group association |
| The CSV layout resolver succeeds | Use only the resolver-identified parent and child members, exact header arrays, field mappings, and parent-child linkage. Use template-derived ViewInstanceName and GroupingKey values when available; otherwise use LDGSecurityProfileMigration with the LDG Security profile name for PER_LDG_SECURITY_PROFILES, and LDGSecurityProfileLdgMigration with LDG Security profile name,LDG Name for ORA_PER_LDG_SECURITY_PROFILES_LDGS.csv. Retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged. |
| A CSV mutation is prepared | Use resolve_ldg_security_profile_csv_context; the profile and legislative data group REST endpoints remain read-only lookup sources and never supply CSV field mappings |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.FIND_PROFILE | decision | 2 | reference_lookup | found_unchanged->LDGSP.RESOLVE_LDG;found_rename->LDGSP.VERIFY_PROFILE_NAME;not_found_or_ambiguous->LDGSP.ERROR | LDGSP.VALIDATE | stop | An existing profile or rename target is requested; verify the supplied current ID for a rename |
| LDGSP.VERIFY_PROFILE_NAME | decision | 3 | reference_lookup | create_available->LDGSP.RESOLVE_LDG;rename_available->LDGSP.RENAME_CSV_GATE;unavailable_or_ambiguous->LDGSP.ERROR | LDGSP.VALIDATE | stop | A new Name is checked only after the old target is verified for a rename |
| LDGSP.RENAME_CSV_GATE | decision | 4 | resolve_dependency | mapping_unverified->LDGSP.ERROR | LDGSP.VERIFY_PROFILE_NAME | stop | A genuine rename has an available new Name; block with `rename CSV identity mapping unverified` before preview or import |
| LDGSP.RESOLVE_LDG | step | 5 | reference_lookup | resolved->LDGSP.DEFAULT;not_found_or_ambiguous->LDGSP.ERROR | none | stop | A legislative data group association is required |
