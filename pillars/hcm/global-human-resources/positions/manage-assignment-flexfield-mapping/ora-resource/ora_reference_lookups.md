# Manage Assignment Flexfield Mapping Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for Manage Assignment
Flexfield Mapping.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_assignment_flex_mappings | Every request | User-visible mapping selector values | Discover the current mapping collection employmentAssignmentFlexSegmentMappings | Source and destination context and segment and mapping identity | Page all mapping rows and apply every supplied predicate conjunctively; list or details may return many, mutation requires exactly one | Business-facing mapping values and transient current identifiers | Details returns zero or all matches; exact mutation stops on zero or multiple matches |
| fetch_assignment_flex_mapping_loader_template | create, edit, or delete | Registered business-object discriminator AssignmentFlexfieldsMapping | Query /hcmRestApi/resources/latest/dataLoaderBusinessObjects with exact BusObjTopDiscriminator, read UcmContentId, then download /documents/files/{UcmContentId}/data | Raw DAT METADATA lines and section order | Require exactly one registered object and a UTF-8 template whose root discriminator matches AssignmentFlexfieldsMapping | Raw template headers, action-section order, and SourceRefTableName plus SourceRef001 through SourceRef010 omission set | Stop on zero or multiple objects, missing UcmContentId, unreadable content, or a discriminator mismatch |
| resolve_assignment_flex_context_segment | Create or edit includes a source or destination value | Requested context and segment | Discover the current getAllFlexContexts and getAllFlexSegments action links from employmentAssignmentFlexSegmentMappings, then invoke them with the ADF action contract | Action-supported context and segment codes | Require one current match for each requested value; accept the global context only when current segment metadata exposes it; reject a context-specific source mapped to a global destination | Action-supported context and segment values | Stop on zero, multiple, invalid-scope, or unavailable matches. Datatype, precision, and value-set compatibility are deferred to Fusion Data Loader when the action does not expose them |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client; do not use core.data-loader for the read. |
| A flex-context or flex-segment action runs | POST to the action link freshly discovered from the current mapping collection, with Content-Type application/vnd.oracle.adf.action+json and a JSON body containing dffCode for the requested flexfield. Treat the action as read-only. Do not store, reuse, or disclose a runtime-generated rv path |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Page the complete declared collection before matching or reporting results. |

### Read Algorithm

1. Page the complete mapping collection.
2. Expose source context and segment, and destination context and segment.
   Keep technical identifiers transient.
3. Apply all user predicates conjunctively. Broad reads return all matches and
   a count; exact mutations require one match.
4. Omit internal synchronization configuration and all Legal Employer names,
   IDs, associations, and resolution statuses from normal details, previews,
   and results; do not fetch Legal Employer data.
5. For a read-only list or details response, render `mapping_details` as a
   Markdown table with these columns, in exactly this order:

   1. `Position Flexfield Context` — `SourceContextCode`
   2. `Position Flexfield Segment` — `SourceSegmentCode`
   3. `Assignment Flexfield Context` — `DestinationContextCode`
   4. `Assignment Flexfield Segment` — `DestinationSegmentCode`

   Do not display mapping IDs, Legal Employer names, legal-employer IDs,
   associations, resolution statuses, or synchronization flags in this table.

   For a mutation approval preview, use the same four-column table when more
   than one mapping is in scope. For exactly one mapping, render the same four
   user-facing values as a compact `Field | Value` table.

6. Treat `FlexSegmentMappingId`, delete-list identifiers, and grouping keys as
   internal execution values. Keep them in the validated DAT source, Task Hook
   state, and durable diagnostic records only. Never show them in user-facing
   commentary, previews, approval prompts, result summaries, or mapping tables
   unless the user explicitly asks for the identifier value. UCM content IDs and
   Data Loader request IDs may be shown in submission and status results.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.MAPPINGS | decision | 2 | reference_lookup | resolved->AFM.TEMPLATE;not_found->AFM.ERROR;ambiguous->AFM.ERROR;duplicate->AFM.ERROR;failed->AFM.ERROR | AFM.INPUT | stop | Page the current mapping collection through read_assignment_flex_mappings |
| AFM.TEMPLATE | decision | 3 | reference_lookup | resolved->AFM.CONTEXT_SEGMENT;not_applicable->AFM.CONTEXT_SEGMENT;not_found->AFM.ERROR;ambiguous->AFM.ERROR;failed->AFM.ERROR | AFM.MAPPINGS | stop | Fetch the raw registered template through fetch_assignment_flex_mapping_loader_template for every CUD operation; skip read-only operations |
| AFM.CONTEXT_SEGMENT | decision | 4 | reference_lookup | resolved->AFM.DEPENDENCIES;not_applicable->AFM.DEPENDENCIES;not_found->AFM.ERROR;ambiguous->AFM.ERROR;incompatible->AFM.ERROR;failed->AFM.ERROR | AFM.TEMPLATE | stop | Resolve supplied source and destination values through resolve_assignment_flex_context_segment |
