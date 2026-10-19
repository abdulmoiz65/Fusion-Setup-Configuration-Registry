# Time Device Event Mapping Set Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Mapping Set criteria search or duplicate check | Retrieve every collection page and evaluate every supplied parent and supported child attribute. |
| 2 | Parent and child IDs | Validate or resolve the parent MappingSetId before preparing child relationships. |
| 3 | Event Mappings | Validate every selected MappingId against the documented mapping LOV. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| mapping_set_criteria_search | Mapping Set criteria search or duplicate check | Yes | A search or update provides at least one criterion, or a create provides Name | Lookup | Every user-provided business attribute, including supported child-resource attributes | search_time_device_mapping_sets_by_criteria | A candidate matches only when every supplied criterion is met | Provide one or more search attributes; when multiple candidates match, select one; when a create duplicate is found, choose use existing or create new | Matching business values and a selected complete record when applicable |
| parent_child_mapping_set_id | Parent Mapping Set and child mapping relationship | Yes | Create or update with child mappings | Satisfied for create after one numeric local MappingSetId is generated and copied to every new child; Verify for update | Create: generated Data Loader local correlation. Update: verified Fusion parent read. | resolve_existing_time_device_mapping_set | Every child mapping must belong to exactly one parent Mapping Set | For create, retain one generated local parent ID for the parent and all new children. For update, select one existing Mapping Set. | Parent MappingSetId; existing child MappingSetDetailId and MappingId where applicable |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | A search, update, or create duplicate check has criteria | Read-only paginated collection and detail lookup only |
| Satisfied | A create has one generated numeric local MappingSetId copied to every new child mapping | No lookup required |
| Verify | An update targets an existing Mapping Set or existing child relationship | Read-only parent detail verification only |
| Blocked | Parent or child IDs are missing, mismatched, ambiguous, or unavailable | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_VALIDATE_PARENT_CHILD_IDS | step | 4 | resolve_dependency | ready->TDEMSET_RESOLVE_MAPPING_IDS;blocked->TDEMSET_RELATION_BLOCKED | TDEMSET_RESOLVE_EXISTING_PARENT | stop | Create or update with child mappings |
