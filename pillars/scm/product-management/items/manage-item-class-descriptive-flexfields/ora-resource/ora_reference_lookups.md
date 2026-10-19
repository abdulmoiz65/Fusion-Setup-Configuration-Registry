# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_current_item_class_dff_definition | A create, update, removal, or deployment request has passed input validation | A fresh successful populated export produced in the current run by shared.setup-export.task-level-export for task EGP_ITEM_CLASS_DFFS in the confirmed target environment; candidate FSM ZIP prepared from that exact export | Require exactly one FND_APP_DESCRIPTIVE_FLEXFIELD.csv row matching ApplicationId 10011 and DescriptiveFlexfieldCode EGP_ITEM_CLASS_DFF. Join its context, context-sensitive-segment, global-segment, and selector rows by the complete exported parent keys. For a creation, require zero exact matches for the requested ContextCode and SegmentCode. Compare the proposed ContextIdentifier case-insensitively with all nonblank exported ContextIdentifier values and all candidate context identifiers; compare any supplied SegmentIdentifier with the applicable exported and candidate segment identifiers. Require the requested ColumnName to be absent from every existing enabled or disabled global and context-sensitive segment in the flexfield and from every other new segment in the candidate. Require the candidate to preserve the baseline member inventory, metadata, headers, and all unrelated rows. | Exact current DFF row; existing context and segment codes and nonblank API identifiers; occupied storage columns; value-set references; candidate delta and package-preservation result | Missing, stale, wrong-task, wrong-environment, empty, structurally altered, or ambiguous export evidence blocks preparation. An existing requested identity that differs or a duplicate nonblank API identifier blocks creation. Blank identifiers on existing exported rows do not authorize reuse and do not prove target-wide uniqueness. Any occupied requested storage column or unrelated candidate change blocks preparation; do not silently substitute a column. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Current definition is unavailable or does not resolve exactly | Stop before design enforcement or any configuration action; acquire one fresh populated task export through shared.setup-export.task-level-export. |
| More than one definition matches the supplied identity | Stop and require an unambiguous item-class and flexfield selection. |
| A new context has a blank or invalid ContextIdentifier | Stop before package preparation. Require a reviewed API name that passes the syntax and collision rules; do not derive it automatically from ContextCode. |
| Existing exported contexts have blank ContextIdentifier | Treat them as legacy-state evidence. Do not copy the blank, infer that new contexts may omit the identifier, or treat those rows as proving that a proposed API name is available. |
| A new context-sensitive segment has a blank or invalid SegmentIdentifier | Stop before package preparation. Require a reviewed API name that passes the syntax and collision rules; do not derive it automatically from SegmentCode. |
| Existing exported segments have blank SegmentIdentifier | Treat them as legacy-state evidence. Do not copy the blank, infer that new segments may omit the identifier, or treat those rows as proving that a proposed API name is available. |
| A requested segment column is already assigned | Stop before package preparation and require an explicitly reviewed available compatible column. Disabled segments continue to own their assigned columns. |
| A candidate is prepared from the export | Preserve every member, metadata file, header, baseline row, and unrelated value; only the reviewed context and segment rows may be added or changed. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICDFF.RESOLVE_CURRENT_DEFINITION | decision | 2 | reference_lookup | resolved->ICDFF.ENFORCE_DESIGN;unresolved->RETURN_ISSUES | ICDFF.VALIDATE_REQUEST | stop | A valid request needs the current item-class DFF definition |
