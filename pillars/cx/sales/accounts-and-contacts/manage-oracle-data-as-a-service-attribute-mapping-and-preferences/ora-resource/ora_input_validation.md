# Input Validation

Validate the selected-row request and fresh task export before package
preparation. The supplied complete seeded-row catalog is the local authority for
rows that a pod export omits because they remain unchanged.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export, prepare, import, status, or verify | Stop before the next stage | Select exactly one supported operation | Every run | |
| Task identity | task_code=ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES | Stop before preview | Use the fixed identity from the enclosing skill; do not accept an override | Every run | |
| Row selection | AttributeCategory, DaasAttributeName, and nonempty set object | Stop before package preparation | Ask preference questions with their UI labels; normalize the confirmed answer to the documented FSM field/value | Prepare or import | |
| Fresh export | One task-level FSM ZIP exported for the fixed task | Stop before package preparation | Run the shared unfiltered task exporter and retain its ProcessId and ZIP | Prepare or import | |
| Live attribute metadata | Complete target-pod `objectMetadata/{FusionObjectName}/child/attributes` response for every effective nonblank object | Stop before package preparation | Route the documented GET through `validate_fusion_mapping_attributes`; required only when either mapping field changes | Prepare or import mapping change | validate_fusion_mapping_attributes |
| Target environment | fusion_environment_context | Stop before Data Loader preview | Select one exact configured target | Import | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Every requested composite key has exactly one baseline row | Satisfied | Continue to fresh-export overlay and package preparation | |
| A requested key is absent or duplicated in the seeded catalog | Blocked | Correct the key or update the source catalog through reviewed skill authoring | |
| The fresh export contains the row | Satisfied | Preserve that current row and apply only requested fields | |
| The fresh export omits the row | Satisfied | Copy the exact row from the complete seeded catalog and apply only requested fields | |
| A mapping field changes and all effective pairs match complete target-pod metadata | Satisfied | Record exact-match evidence and continue to package preparation | validate_fusion_mapping_attributes |
| Live metadata is missing, incomplete, or lacks an effective object/attribute pair | Blocked | Correct the mapping or metadata-access gap; do not build the ZIP | validate_fusion_mapping_attributes |
| The prepared ZIP hash matches the latest validation preview | Satisfied | Route the immutable ZIP to core.data-loader | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Composite key | Require nonblank AttributeCategory and DaasAttributeName; reject duplicates in one request | Prepare | |
| Editable fields | Accept only `AutofillBlank`, `AutoupdateNonBlank`, `FusionObjectName`, and `FusionAttributeName`; call the preference fields **Don't Apply Blank Values** and **Don't Overwrite** when asking the user | Prepare | |
| Fusion object and attribute | For mapping-field changes, require a nonblank attribute to have a nonblank object; validate each nonblank object against its complete target-pod response and each nonblank attribute by exact case-sensitive `AttributeCode` match. Allow both fields blank as an explicit unmapping. | Prepare | validate_fusion_mapping_attributes |
| Don't Apply Blank Values | Normalize on to `AutofillBlank=Y` and off to `AutofillBlank=N` | Prepare | |
| Don't Overwrite | Normalize on to `AutoupdateNonBlank=N` and off to `AutoupdateNonBlank=Y` | Prepare | |
| Display During Real-time Enrichment | Treat as a separate UI-only control; it is not an editable selected-row FSM field | Prepare | |
| Immutable columns | Reject changes to key, original-value, description, group, mandatory, bundle, and simplified-import columns | Prepare | |
| ZIP safety | Reject absolute paths, parent traversal, duplicate members, unreadable members, or invalid UTF-8 CSV | Prepare or import | |
| Metadata task binding | Require exactly one ObjectShortName equal to ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES | Prepare or import | |
| CSV members | Require both fixed Oracle CSV names and schemas matching the 20-column seeded catalog | Prepare or import | |
| Output scope | Require each output CSV to contain exactly the explicitly selected keys and no other rows | Import | |
| Archive fingerprint | Require the lowercase SHA-256 of the exact ZIP submitted to Data Loader | Import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| DAAS.VALIDATE_REQUEST | step | 1 | validate_input | valid->DAAS.RESOLVE_ROW_SOURCE;invalid->DAAS.ERROR | none | stop | Before export, package preparation, import, status, or verification |
