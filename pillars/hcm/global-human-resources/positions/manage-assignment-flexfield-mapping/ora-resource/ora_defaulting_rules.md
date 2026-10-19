# Manage Assignment Flexfield Mapping Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Assignment Flexfield Mapping. This file does not own input validation,
lookup mechanics, design policy, payload construction, or execution routing.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and user override is allowed | Preserve the supplied value | preserved |
| 2 | An edit omits a current value and no Standard Defaults row applies | Preserve the freshly read current value | preserved |
| 3 | Exactly one Standard Defaults row applies | Apply that default | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | A required resolver is unresolved, ambiguous, or failed | Apply no value and stop | blocked |

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| Edit values | Preserve every current mapping value not explicitly changed | Every edit | No |  | Block if the current mapping cannot be read |
| Global context | Use the current global-context representation only when live segment metadata proves it | User explicitly selects the global context | No | resolve_assignment_flex_context_segment | Block when metadata does not expose the global context |
| Legal-employer input | No value | Every request | No |  | Block if a legal-employer name, identifier, or association delta is supplied; Legal Employer operations are unsupported in this task |
| Internal execution configuration | Use only an explicit value or a default proven by current runtime metadata; preserve it on edit | Required by the current action contract | No |  | Block when no supported value is available |
| Child-grouping key | For each independent child CUD request, generate one fresh nonblank FlexSegmentMappingGroupKey unique within the DAT source and repeat it only in that request's root row and child action row or rows; it is the internal parent surrogate and is not sent in the custom-method payload | Every child CUD source | No |  | Block when the grouping key is absent, is reused by another independent request, differs between its root and child rows, or appears in the custom-method payload |
| Create grouping key | Generate one FlexSegmentMappingGroupKey per independent create request as current UTC epoch milliseconds, incremented on a same-source collision; do not generate FlexSegmentMappingId | A child business object is created | No |  | Block when a create source generates FlexSegmentMappingId or reuses another request's grouping key |
| Update child mapping ID | Preserve the exact FlexSegmentMappingId returned by read_assignment_flex_mappings in each update child row; do not use it as the root grouping key | A child business object is updated | No | read_assignment_flex_mappings | Block when the exact current mapping cannot be read |
| CUD template headers | Use the current raw UCM DAT template; omit only SourceRefTableName and SourceRef001 through SourceRef010 and retain all other headers and section order | create, edit, or delete | No | fetch_assignment_flex_mapping_loader_template | Block when the registered raw template cannot be fetched |
| Update child directive and action | Use MERGE; retain the raw-template update-column order; set FlexSegmentMappingId to the exact current mapping ID; retain RestAction with an empty value | edit | No | read_assignment_flex_mappings | Block when the update row omits the fetched ID, changes the template order, uses another directive, or sets a nonblank RestAction |
| Delete child identifiers | Set DeleteFlexSegmentMappingIdList to the exact current mapping ID and use only the FlexSegmentMappingGroupKey of that delete request's matching root group | delete | No | read_assignment_flex_mappings | Block when the delete list differs from the fresh read, the grouping key differs from its root row, or the key is reused by another independent request |
| Delete child directive and action | Use MERGE and preserve the template RestAction column with an empty value | delete | No |  | Block when a DELETE directive or a nonblank Delete-row RestAction is proposed |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing mapping value | Preserve the fresh current value | preserved |
| FlexSegmentMappingId | A child create row is authored | Do not generate a mapping ID | not_required |
| FlexSegmentMappingGroupKey | A child CUD source is authored | Generate one documented fresh grouping key per independent request and repeat it only in that request's root and child rows | applied |
| No applicable default | No Standard Defaults row applies | Make no change | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.DEFAULTS | decision | 6 | apply_default | applied->AFM.DESIGN;preserved->AFM.DESIGN;not_required->AFM.DESIGN;blocked->AFM.ERROR | AFM.DEPENDENCIES | stop | After validation and applicable read-only resolution |
