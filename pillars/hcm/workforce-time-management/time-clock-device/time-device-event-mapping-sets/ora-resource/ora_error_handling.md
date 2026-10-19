# Time Device Event Mapping Set Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Name is missing or empty | Stop and request Name |
| Mappings is missing, empty, or contains an entry without MappingId | Stop and request one or more Event Mappings |
| A supplied MappingId cannot be resolved exactly once | Stop and report the affected MappingId values; do not prepare a create request |
| A create has a blank, nonnumeric, or different MappingSetId on a child mapping | Block preview and import preparation. Generate one unique numeric local MappingSetId and repeat it exactly on the parent and every new child mapping. |
| An update has no verified persisted MappingSetId or an existing child relationship has no verified MappingSetDetailId | Stop before update. Read the selected parent with expand=all; do not infer a parent ID from Name or a child relationship ID from MappingId. |
| A later Fusion create request fails | Stop before retrying, retain sanitized diagnostics, and require review of the failure before another attempt |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not request provider approval. |
| Complete Summary or Defaults Applied is missing, incomplete, technical, or not displayed immediately before approval | Return to summary generation; do not enter the provider-owned approval process. |
| A validated ZIP archive is prepared but its direct link is omitted from the approval response | Return to the approval-artifact disclosure gate. Display the business-only Complete Summary and Defaults Applied, then a direct link to the exact validated ZIP and the approval request; do not upload the archive before that response is shown. |
| A criteria search cannot retrieve every page, evaluate a supplied supported child attribute, or produce an unambiguous required selection | Stop before preview; do not infer an identity or treat a partial result as no match. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation failure | The missing or invalid field and the required correction |
| Mapping lookup failure | The MappingId values that did not resolve exactly once |
| Parent-child ID failure | The missing, mismatched, or unresolved parent or child ID and the required correction |
| Fusion create failure | The operation, affected record identity, sanitized error response, and that no automatic retry occurred |
| Complete Summary is blocked | The missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values. |
| Approval response for a validated ZIP | The completed business-only summary, a direct link to the exact validated ZIP immediately below it, and the approval requirement |
| Criteria search is blocked | The incomplete, unavailable, or ambiguous search condition and one safe corrective action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_PROVIDER_APPROVAL | step | 8 | execution_gate | ready->TDEMSET_READY;blocked->TDEMSET_APPROVAL_BLOCKED | TDEMSET_ENFORCE_SUMMARY | stop | A valid business-only Complete Summary and Defaults Applied are displayed; provider execution and approval ownership remain unchanged |
| TDEMSET_READY | terminal | 9 | terminal | none | TDEMSET_PROVIDER_APPROVAL | stop | Input, criteria search, parent-child relationship, Event Mappings, defaults, and Complete Summary passed for handoff to the provider-owned approval process |
| TDEMSET_INPUT_BLOCKED | terminal | 10 | terminal | none | TDEMSET_VALIDATE_INPUT | stop | Input validation failed |
| TDEMSET_SEARCH_MULTIPLE_MATCHES | terminal | 11 | terminal | none | TDEMSET_SEARCH_MAPPING_SETS | stop | Multiple matching Mapping Sets were shown for user selection |
| TDEMSET_SEARCH_NO_MATCHES | terminal | 12 | terminal | none | TDEMSET_SEARCH_MAPPING_SETS | stop | No Mapping Set met every supplied search criterion |
| TDEMSET_AWAIT_DUPLICATE_CHOICE | terminal | 13 | terminal | none | TDEMSET_SEARCH_MAPPING_SETS | stop | A create request has a matching Mapping Set and awaits the user's use-existing or create-new choice |
| TDEMSET_SEARCH_BLOCKED | terminal | 14 | terminal | none | TDEMSET_SEARCH_MAPPING_SETS | stop | Criteria search is incomplete, unavailable, or ambiguous |
| TDEMSET_PARENT_BLOCKED | terminal | 15 | terminal | none | TDEMSET_RESOLVE_EXISTING_PARENT | stop | Existing Mapping Set could not be resolved |
| TDEMSET_RELATION_BLOCKED | terminal | 16 | terminal | none | TDEMSET_VALIDATE_PARENT_CHILD_IDS | stop | Parent-child IDs are invalid or unresolved |
| TDEMSET_MAPPING_BLOCKED | terminal | 17 | terminal | none | TDEMSET_RESOLVE_MAPPING_IDS | stop | Event Mapping lookup did not resolve |
| TDEMSET_DEFAULTS_BLOCKED | terminal | 18 | terminal | none | TDEMSET_APPLY_DEFAULTS | stop | Defaulting could not complete safely |
| TDEMSET_SUMMARY_BLOCKED | terminal | 19 | terminal | none | TDEMSET_ENFORCE_SUMMARY | stop | Business-only Complete Summary requirements were not met |
| TDEMSET_APPROVAL_BLOCKED | terminal | 20 | terminal | none | TDEMSET_PROVIDER_APPROVAL | stop | Provider approval gate is not ready |
