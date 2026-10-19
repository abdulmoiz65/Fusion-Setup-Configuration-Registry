# Input Validation

These validations implement the Oracle Fusion guidance for Item Class Descriptive Flexfields and the supplied FDOS pillar guidance.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Documented business need | Business purpose and the item-class data gap not met by standard attributes | Stop before design review | Provide the business, reporting, integration, or compliance requirement | A segment, context, or existing definition is created or changed | |
| Segment design | Segment name, data type, valid values or value set, owner, requiredness, and reporting or integration use | Stop before design review | Provide the complete proposed segment definition | A segment is created or changed | |
| Context design | Global or context-sensitive design, context value when applicable, and single-context display rationale | Stop before design review | Provide the context design and applicability | A context-sensitive segment is proposed | |
| New context identity | ContextCode, nonblank ContextIdentifier, and Name | Stop before candidate preparation | Provide a reviewed API name in ContextIdentifier. Do not copy ContextCode when it contains underscores or otherwise violates API-name rules. | A new context is created through the EGP_ITEM_CLASS_DFFS task CSV import | |
| New segment identity | SegmentCode, nonblank SegmentIdentifier, Name, and parent ContextCode | Stop before candidate preparation | Provide a reviewed API name in SegmentIdentifier and retain the exact parent context relationship. Do not copy SegmentCode when it contains underscores or otherwise violates API-name rules. | A new context-sensitive segment is created through the EGP_ITEM_CLASS_DFFS task CSV import | |
| Change impact evidence | Affected item classes, active data status, migration approach when active data exists, and test scope | Stop before design review | Provide impact assessment and approved migration approach | An existing segment, context, or definition is changed or removed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DFF suitability | Accept only a small number of shallow, individual fields. Route grouped, repeatable, or complex data requirements to an extensible flexfield design instead. | A new field requirement is proposed | |
| Segment completeness | Require stable segment name, data type, valid-value control, owner, requiredness, and stated downstream use. | A segment is created or changed | |
| Context applicability | Require context-sensitive segments only when one clearly defined context is displayed at a time. | A context-sensitive segment is proposed | |
| Context API name required on create | Require a nonblank ContextIdentifier for every new context row. Existing exported contexts with blank ContextIdentifier are legacy-state evidence only and do not establish that a new row may omit it. | A new context is created through the task-level FSM CSV package | |
| Context API name syntax | Require ContextIdentifier to be at most 30 characters, start with A-Z or a-z, contain only A-Z, a-z, and 0-9, and not be a documented reserved API word. Reject spaces, underscores, multibyte characters, and a leading digit. Treat the identifier as immutable after creation. | ContextIdentifier is supplied or required | |
| Context API name collision | Compare ContextIdentifier case-insensitively with every nonblank exported context identifier and every new context identifier in the candidate. Block a duplicate. Blank identifiers on existing exported rows are unknown legacy values, not reusable names and not proof that the proposed identifier is globally available. | A new context is created | resolve_current_item_class_dff_definition |
| Segment API name required on create | Require a nonblank SegmentIdentifier for every new context-sensitive segment row. Existing exported segments with blank SegmentIdentifier are legacy-state evidence only and do not establish that a new row may omit it. | A new context-sensitive segment is created through the task-level FSM CSV package | |
| Segment API name syntax | Require SegmentIdentifier to be at most 30 characters, start with A-Z or a-z, contain only A-Z, a-z, and 0-9, and not be a documented reserved API word. Reject spaces, underscores, multibyte characters, and a leading digit. Treat the identifier as immutable after creation. | SegmentIdentifier is supplied or required | |
| Segment API name collision | Compare SegmentIdentifier case-insensitively with every nonblank exported segment identifier and every new segment identifier in the candidate. Block a duplicate within the applicable flexfield component namespace. Blank identifiers on existing exported rows are unknown legacy values, not reusable names and not proof that the proposed identifier is globally available. | A new context-sensitive segment is created | resolve_current_item_class_dff_definition |
| Required context CSV attributes | Require ApplicationId, DescriptiveFlexfieldCode, ContextCode, ContextIdentifier, Name, and EnabledFlag for a new context. Preserve valid optional fields as explicitly supplied or blank; never remove required fields because an older exported row leaves its identifier blank. | A new context row is prepared | |
| Required context-sensitive segment CSV attributes | Require ApplicationId, DescriptiveFlexfieldCode, ContextCode, SegmentCode, SegmentIdentifier, ColumnName, Name, Prompt, ShortPrompt, EnabledFlag, DisplayType, RequiredFlag, ReadOnlyFlag, and ValueSetCode. Require the parent context to exist in the baseline or the same candidate. | A new context-sensitive segment row is prepared | resolve_current_item_class_dff_definition |
| Active-data protection | Block repurposing or removal of a segment or context containing active data until an approved migration and reporting-impact plan exists. | An existing segment or context is changed or removed | |

## Validation Evidence

- Oracle documents ContextIdentifier as the context API name with a maximum size of 30 characters in the descriptive-flexfield import format.
- Oracle API-name conventions allow only alphanumeric characters with a nonnumeric leading character, prohibit spaces and underscores, identify reserved words, and warn that API names must not be changed after creation.
- The target EGP_ITEM_CLASS_DFFS task CSV import returned FND-3036, "The context identifier is required," when a new context row supplied a blank ContextIdentifier. This target-observed create contract is stricter than the generic documentation that labels the field optional.
- The same target import subsequently returned FND-3039, "The segment identifier is required," for the new context-sensitive segment after ContextIdentifier was populated. This establishes SegmentIdentifier as required for new segment rows on this task route.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICDFF.VALIDATE_REQUEST | decision | 1 | validate_input | valid->ICDFF.RESOLVE_CURRENT_DEFINITION;invalid->RETURN_ISSUES | none | stop | A create, update, removal, or deployment request is evaluated |
