# Configure Barcode Formats Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Barcode Formats data-description overlays | Status and RetainPrefixFlag defaults |
| Redwood Barcode Formats manage-page state | GroupSeparatorFlag and IncludesCheckDigitFlag child defaults |
| User-approved defaulting policy | Apply each documented default only when the user omits the field; preserve explicit user values |

## Default Values

| Business Value | Implementation Field Name | Default | When to Use | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|---|
| Status | Status | Y (Active) | The user omits Status for a barcode-format header | Yes | The Redwood header overlay initializes Status to Y, the canonical Active value. |
| Retain Prefix | RetainPrefixFlag | false | The user omits RetainPrefixFlag for a barcode-format header | Yes | The Redwood header overlay initializes RetainPrefixFlag to false. |
| Group Separator | GroupSeparatorFlag | false | The user omits GroupSeparatorFlag for a data identifier configuration row | Yes | The Redwood manage page initializes a new row with GroupSeparatorFlag false. |
| Includes Check Digit | IncludesCheckDigitFlag | false | The user omits IncludesCheckDigitFlag for a data identifier configuration row | Yes | The Redwood manage page initializes a new row with IncludesCheckDigitFlag false. |

## Defaulting Rules

| Rule | What Happens |
|---|---|
| Explicit value | Preserve an explicit user value; do not replace it with a default. |
| Omitted value | Apply only the documented default for the corresponding header or child row. |
| Blank handling | Treat a missing value as omitted; do not infer a default for any field not listed above. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BCF.APPLY_DEFAULTS | step | 30 | apply_default | applied->BCF.RESOLVE_FIELD_NAME;not_required->BCF.RESOLVE_FIELD_NAME;blocked->BCF.HANDLE_ERROR | BCF.CHECK_READINESS | stop | After the per-run BO metadata preflight and before selected LOV resolution or Data Loader handoff |
