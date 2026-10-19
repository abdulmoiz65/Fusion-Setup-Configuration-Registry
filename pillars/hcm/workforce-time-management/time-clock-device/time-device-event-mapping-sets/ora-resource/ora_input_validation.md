# Time Device Event Mapping Set Input Validation

## Source Basis

- Time Profiles Technical Design Document for FSCR, Confluence page 21722044713, read 2026-09-22.
- Developer-provided Mapping Set field and create-payload reference, 2026-09-22.
- Developer-provided business-only Complete Summary requirements, 2026-09-22.

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Generate the summary only from populated structured business values that completed validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified user-provided business value | Every Complete Summary | |
| Applied defaults | Include every user-facing default that was actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, and metadata-only values | Every Complete Summary | |
| Populated children | Show populated child mappings using business labels only; do not render an empty child section | A child mapping has values | |
| Summary readiness | Always generate and display the Complete Summary and Defaults Applied immediately before requesting provider-owned approval | A create or update request is ready for provider approval | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Mapping set identity | Name | Block the create request | Provide a non-empty Name | Always | |
| Event mappings | Mappings with one or more MappingId values | Block the create request | Select at least one Event Mapping | Always | resolve_time_device_mappings |
| Parent-child ID correlation | MappingSetId on the parent and every new child mapping | Block preview and import preparation | For create, generate one unique numeric local MappingSetId and repeat it in every new child mapping. For update, use only the persisted MappingSetId returned by Fusion. | Create or update with child mappings | resolve_existing_time_device_mapping_set |
| Summary readiness | Complete Summary and Defaults Applied | Block provider approval | Generate the required business-only summary from verified structured values | Create or update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is mandatory | Reject a missing or empty Name | Always | |
| Description is optional | Accept Description when supplied; omit it when not supplied | Always | |
| Mappings is a non-empty collection | Reject a missing or empty Mappings collection | Always | resolve_time_device_mappings |
| Each Mappings entry has MappingId | Reject an entry without MappingId | Mappings is supplied | resolve_time_device_mappings |
| New child MappingSetId | Require a nonblank numeric value that exactly equals the parent MappingSetId; treat both as Data Loader local correlations, not persisted Fusion IDs | Create | |
| Update MappingSetId | Accept only the persisted ID returned by the verified Fusion parent read; do not generate, replace, or infer an ID | Update | resolve_existing_time_device_mapping_set |
| Existing child MappingSetDetailId | Retain only a child relationship ID returned by the verified parent read; do not derive it from MappingId | Update of an existing child mapping | resolve_existing_time_device_mapping_set |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A search or update is requested | Require at least one user-provided business attribute and evaluate every supplied attribute as a conjunctive criterion | Retrieve every page, show all matching candidates, and request a selection when multiple candidates match | search_time_device_mapping_sets_by_criteria |
| A new Mapping Set is prepared | Check exact Name, then case-insensitive partial Name, then every supplied non-Name attribute when neither name check finds a match | If a match is found, present it and wait for the user's use-existing or create-new choice | search_time_device_mapping_sets_by_criteria |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_VALIDATE_INPUT | step | 1 | validate_input | valid->TDEMSET_SEARCH_MAPPING_SETS;invalid->TDEMSET_INPUT_BLOCKED | none | stop | Always |
