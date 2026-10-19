# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A parent collection page, item-detail read, supported child link, or child collection page cannot be completed | Stop and classify the search as unresolved; do not report no matches from incomplete evidence |
| Search or Update returns multiple candidates | Show every matching candidate with sanitized selection details and ask the user to select one; do not continue to Update until exactly one is selected |
| Create finds one or more candidates during exact Name, partial Name, or non-Name-attribute search | Show every candidate found by the first successful phase and ask whether to use a selected existing record or create a new record |
| Mapping-form validation fails | Return without calling REST and leave component validation messages visible |
| A required or dependent LOV search returns partial or multiple candidates | Show up to five closest eligible business display values and require the user to select one; do not submit a parent or child request before that selection. |
| A required or dependent LOV search returns no eligible candidate | Stop and identify the unresolved field and request refined search text; do not submit a parent or child request. |
| A new Event Attribute Detail has a blank, nonnumeric, or different MappingId from its parent | Block preview and upload. For create, generate one unique numeric local parent MappingId and repeat it exactly in every new child row. For update, restore the persisted parent MappingId returned by Fusion on every child row. |
| An update parent or child uses a generated, replaced, or inferred MappingId | Block preview and upload; reload the persisted parent identity from Fusion and use that exact MappingId on the parent and all Event Attribute Detail rows. |
| A new Event Attribute Detail is assigned a MappingDetailId | Remove the child identifier; Fusion assigns MappingDetailId for a new child row. |
| A parent mapping action is UPDATE, a create uses PATCH, or an edit of a verified existing mapping does not use PATCH | Block validation and upload. Use POST only for parent creation and PATCH only for parent update or edit; do not substitute UPDATE. |
| An Event Attribute Detail action was copied, derived, or inferred from the parent mapping action | Block validation and upload until the child action is verified against its own lifecycle. |
| A parent mapping update is attempted | Use the captured parent ETag when available |
| A child-row update or delete is attempted | Use the row ETag when available; a delete sends it in If-Match when available |
| A child row cannot be persisted | Stop and report the parent MappingId and affected child row without retrying the mutation automatically |
| A documented REST path or provider path is incomplete | Stop before live execution and obtain the missing contract; do not infer a composite key or endpoint |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not transition to the provider-owned approval process and do not place a warning, diagnostic, or technical note in the summary |
| Complete Summary and Defaults Applied were not displayed before the provider-owned approval process | Return to the summary gate, display the required business-only summary, and then transition to provider-owned approval; provider execution and approval ownership remain unchanged |
| A validated ZIP archive is prepared but its direct link is omitted from the approval response | Return to the approval-artifact disclosure gate. Display the business-only Complete Summary and Defaults Applied, then a direct link to the exact validated ZIP and the approval request; do not upload the archive before that response is shown. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required mapping field, child-row time attribute, or parent-child MappingId correlation is absent or invalid | Correct the field or ID correlation and validate again |
| Search resolution | Pagination, item detail, a supported child link, or child-resource retrieval is incomplete, or a supplied search field is unsupported | Correct the criterion or complete the read-only retrieval, then rerun the search from the first page |
| Dependency lookup | A supplier, event, application event, time attribute, or default value does not resolve | Correct the source selection; obtain a missing provider path if needed |
| Fusion API | A create, update, delete, or load request fails | Preserve the sanitized response evidence and stop before retry |
| Approval blocker | A live mutation does not have approval bound to its validated preview | Obtain explicit approval for the exact target and operation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Search result | Every matching candidate's sanitized business identifiers and criterion values; when multiple match, the requirement to select one |
| Create duplicate or equivalent-record result | The successful search phase, every matching candidate's sanitized business identifiers and criterion values, and the choice to use a selected existing record or create a new record |
| Before live mutation | Target environment, mapping name, operation, validated parent values, child-row count, and approval requirement |
| On parent-child ID validation failure | Operation, whether the parent identity is local or persisted, affected child-row identity, and the required ID correction without exposing unrelated identifiers |
| On child-row failure | Parent MappingId when available, row identity, operation, and sanitized error details |
| Complete Summary is blocked | Missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values |
| Approval response for a validated ZIP | The completed business-only summary, a direct link to the exact validated ZIP immediately below it, and the approval requirement |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any search page, candidate detail, supported child link, or child page is unread | Do not treat the incomplete candidate set as no match and do not continue to create or update |
| More than one Search or Update candidate matches | Do not choose a candidate automatically or continue to Update without the user's selection |
| Create finds a duplicate or equivalent candidate | Do not create or silently reuse a record until the user chooses a displayed candidate or explicitly chooses to create a new record |
| A write outcome is uncertain | Do not automatically replay POST, PATCH, or DELETE |
| A create child MappingId does not exactly equal the create parent MappingId | Do not preview or upload the archive |
| An update MappingId was not returned by a verified Fusion parent read | Do not generate, replace, infer, preview, or upload it |
| The parent mapping action does not match whether the mapping is being created or edited | Do not preview or upload the archive; use POST only for creation and PATCH only for an edit of one verified existing mapping |
| An Event Attribute Detail action is derived from the parent mapping action | Do not prepare or upload the child row until its action is independently verified against the child lifecycle |
| The selected parent or child ETag is unavailable | Do not invent an ETag |
| A provider request path is TBD | Do not guess a Fusion endpoint or lookup response shape |
| A Complete Summary is presented | Do not expose IDs, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw Boolean values, diagnostics, warnings, or technical notes |
| A validated ZIP awaits approval | Do not omit the direct archive link, hide it behind a separate request, or upload before the required approval response has displayed it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEM.PROVIDER_APPROVAL | step | 70 | execution_gate | ready->TDEM.READY_FOR_APPROVED_EXECUTION;blocked->TDEM.INPUT_ISSUES | TDEM.GENERATE_COMPLETE_SUMMARY | stop | A valid business-only Complete Summary is present; provider execution and approval ownership remain unchanged |
| TDEM.READY_FOR_APPROVED_EXECUTION | terminal | 80 | terminal | none | TDEM.PROVIDER_APPROVAL | stop | Complete Summary, Defaults Applied, and all declared validation, lookup, defaulting, and design gates passed for handoff to the provider-owned approval process |
| TDEM.INPUT_ISSUES | terminal | 90 | terminal | none | none | stop | A required or dependent field is missing or invalid |
| TDEM.SEARCH_MATCH | terminal | 91 | terminal | none | TDEM.SEARCH_TIME_DEVICE_MAPPINGS | stop | Search returns one candidate, or Create uses one selected existing candidate |
| TDEM.SELECTION_REQUIRED | terminal | 92 | terminal | none | TDEM.SEARCH_TIME_DEVICE_MAPPINGS | stop | Search or Update returns multiple candidates and the user must select one |
| TDEM.NO_MATCHES | terminal | 93 | terminal | none | TDEM.SEARCH_TIME_DEVICE_MAPPINGS | stop | Search or Update returns no candidates |
| TDEM.CREATE_MATCH_DECISION | terminal | 94 | terminal | none | TDEM.SEARCH_TIME_DEVICE_MAPPINGS | stop | Create finds one or more candidates and the user must choose an existing record or confirm creation of a new record |
