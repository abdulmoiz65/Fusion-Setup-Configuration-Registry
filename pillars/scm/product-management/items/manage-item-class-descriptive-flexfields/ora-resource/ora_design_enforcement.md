# Design Enforcement

Oracle guidance for Item Class Descriptive Flexfields supports shallow individual attributes. It does not support attribute groups, and it displays only one context at a time.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate request | Confirm the business need, complete segment design, context design, and active-data impact evidence. |
| 2 | Retrieve current definition | Resolve the exact current item-class DFF definition before assessing a change. |
| 3 | Enforce design | Apply the design rules and block unsupported, unsafe, or incomplete changes. |
| 4 | Validate after configuration | Confirm field visibility and behavior, then test representative data entry, validation, imports, integrations, and reporting before production deployment. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new field requirement is proposed | Error | resolve_current_item_class_dff_definition | The requirement is grouped, repeatable, complex, or not supported by a documented business need | Use a descriptive flexfield only for a small number of shallow individual fields. Use extensible flexfields for grouped, repeatable, or more complex data. | Yes |
| A context-sensitive segment is proposed | Error | resolve_current_item_class_dff_definition | More than one context must display at the same time or context applicability is undefined | Define one clearly applicable context at a time; use global segments when the field applies across all item classes in scope. | Yes |
| A new context is prepared for task CSV import | Error | resolve_current_item_class_dff_definition | ContextIdentifier is blank, exceeds 30 characters, does not start with a letter, contains a nonalphanumeric character, is a reserved API word, or duplicates another nonblank context API name case-insensitively | Supply a reviewed immutable API name. Do not reuse ContextCode when it contains underscores or silently generate an identifier after preview. Existing exported blank identifiers do not waive this create requirement. | Yes, before a new immutable preview and approval |
| A new context-sensitive segment is prepared for task CSV import | Error | resolve_current_item_class_dff_definition | SegmentIdentifier is blank, exceeds 30 characters, does not start with a letter, contains a nonalphanumeric character, is a reserved API word, or duplicates another nonblank segment API name case-insensitively in the applicable namespace | Supply a reviewed immutable API name. Do not reuse SegmentCode when it contains underscores or silently generate an identifier after preview. Existing exported blank identifiers do not waive this create requirement. | Yes, before a new immutable preview and approval |
| A context-sensitive segment is created or its storage assignment changes | Error | resolve_current_item_class_dff_definition | The requested ColumnName is already assigned to any global or context-sensitive segment in the flexfield, is duplicated in the candidate, or is not compatible with the requested value set and display type | Select an available compatible column using the fresh populated export and retain the reviewed selection literally. Do not treat a disabled segment as releasing its column or silently substitute a different column. | Yes, only after explicit review of the replacement column |
| A context or context-sensitive segment is created | Error | resolve_current_item_class_dff_definition | The requested ContextCode or SegmentCode already exists with different settings, a supplied ContextIdentifier or SegmentIdentifier collides in its applicable namespace, the segment does not reference the requested context, or its sequence conflicts within that context | Require new exact identities, preserve the parent relationship, and use a sequence number not already assigned within the selected context. A matching existing definition is a no-op rather than a repeated create. | Yes |
| A candidate FSM package is prepared | Error | resolve_current_item_class_dff_definition | The candidate changes the metadata, member inventory, headers, baseline rows, or unrelated values beyond the reviewed context and segment additions | Rebuild from the exact fresh export and preserve every unrelated byte-level value and row. | Yes |
| A segment or context is changed or removed | Error | resolve_current_item_class_dff_definition | Active data exists and no approved migration and reporting-impact plan is supplied | Preserve the existing definition until the approved migration plan is ready. | Yes |
| A configuration is ready for deployment | Error | resolve_current_item_class_dff_definition | Current definition, downstream impact, deployment verification, or representative test plan is missing | Assess item-class maintenance, item creation, imports, integrations, search, reporting, and security before deployment. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_current_item_class_dff_definition | Before design enforcement for any change | Current DFF definition, context and segment identities, occupied storage columns, value-set references, and exact candidate delta; active-data and deployment evidence additionally when an existing definition is changed or removed | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICDFF.ENFORCE_DESIGN | decision | 3 | design_enforcement | compliant->ICDFF.ALL_GOOD;blocked->RETURN_ISSUES | ICDFF.RESOLVE_CURRENT_DEFINITION | stop | The current definition and proposed change are available |
