# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_dff_export_model | Before a filtered read, Create, Update, Preview, Import, Deploy, or Verify path | Fresh immutable task-level FSM export for IRC_OFFERS_DFF | Require one exact canonical task match; use case-sensitive technical identity for global segment, context, and context-sensitive segment | Package contract, target identity, keys, headers, sequences, storage columns, translation behavior, and current before-values | Stop as BLOCKED; do not infer package shape, values, or target identity |
| resolve_value_set_authority | A requested segment creates or changes a value set or LOV | Explicitly named approved value-set authority and identifier | Require one exact approved value-set identifier only for a value-set or LOV change; otherwise this lookup is not required | Exact identifier, data-type compatibility, display-component compatibility, and allowed mapping | Stop as INVALID_VALUE_SET or AMBIGUOUS_VALUE_SET; do not derive from a display label |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Fresh task-level export is unavailable, stale, or lacks a complete package contract | Stop before package preparation, import, deployment, or verification. |
| A context code or segment code has zero or multiple exact matches | Stop as NOT_FOUND or AMBIGUOUS_TARGET. |
| A value-set authority has no approved source or contract | Block only the mutation that creates or changes that value set or LOV. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.RESOLVE_EXPORT | step | 20 | reference_lookup | resolved->IRC_OFFER_DFF.RESOLVE_VALUE_SET;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.VALIDATE_SCOPE | stop | Every supported path requiring DFF state |
| IRC_OFFER_DFF.RESOLVE_VALUE_SET | decision | 30 | reference_lookup | resolved_or_not_required->IRC_OFFER_DFF.CHECK_DEPENDENCIES;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.RESOLVE_EXPORT | stop | A value set or LOV is created or changed |

## Existing export authority and validation route

An unchanged value set requires no new lookup. An exact exported ValueSetCode already used on a character segment supplies identity and demonstrated character compatibility when reusing that same value set; never create or modify the value set through this task. During internal validate_import, read the preserved completed baseline and prepared candidate locally without starting another export.

## Verified export model

Require unique ZIP member names and valid CRCs, ASM_SETUP_CSV_METADATA.xml with the
exact task, selected ProcessEnv, EXPORT type and COMPLETED status, plus the following
CSV members. Reject duplicate headers, malformed row widths or ambiguous keys.

| Member | Identity and scope |
|---|---|
| FND_APP_DESCRIPTIVE_FLEXFIELD.csv | Exactly one root: DescriptiveFlexfieldCode IRC_OFFERS_DFF and ApplicationId 821 |
| ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_GLOBAL_SEGMENT.csv | Unique SegmentCode under that DFF/application; global segments only |
| ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT_SEGMENT.csv | Context selector definition, distinct from context-sensitive segments; preserve unchanged unless explicitly targeted |
| ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT.csv | Unique ContextCode under that DFF/application |
| ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_SEGMENT.csv | Unique ContextCode plus SegmentCode; parent context must exist |

Every child row must retain FND_APP_DESCRIPTIVE_FLEXFIELD.DescriptiveFlexfieldCode
and FND_APP_DESCRIPTIVE_FLEXFIELD.ApplicationId. Context segments join through
ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT.ContextCode. Keep the context-selector definition distinct from
the global segment list. Report globals, contexts and context-sensitive segments
separately with their names, codes, columns, sequences, value sets and requested
default/required/enabled details; do not expose audit fields.

For new-row presentation, select one enabled, optional, editable character segment
in the same context using the same exact ValueSetCode and having no default. Its
presentation fields supply only the documented defaults; unresolved or conflicting
peer evidence blocks defaulting. Retain exact exported headers and resolve any
new or unknown required field before preparing a row.

The [Oracle IRC_OFFERS table definition](https://docs.oracle.com/en/cloud/saas/human-resources/oedmh/ircoffers-15039.html)
documents ATTRIBUTE_CHAR1 through ATTRIBUTE_CHAR90 as VARCHAR2(1000) DFF columns
(reviewed 2026-09-11). Availability still requires the global and selected-context
ownership check. A matching exported value-set code proves existing compatibility
for reuse; a display label alone does not.

Preserve all additional exported validator, label, usage, category, page and task-flow members unchanged. Their presence and headers come from the exact export metadata; the list above identifies the configuration views, not the full ZIP inventory.
