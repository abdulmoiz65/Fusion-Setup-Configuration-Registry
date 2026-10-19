# Input Validation

Validate each requested item structure type before it is handed to the next authorized process. These rules cover the requested design; they do not authorize a Fusion write.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Structure name identity | Display name; optional internal name; optional description; existing parent structure type identity and its matching exported EGP_STRUCTURE_TYPE row | Stop before validation when the display name, parent identity, or matching parent row is missing | Supply a display name and use a fresh populated export to retain the parent identity. For FSM child additions, copy the exact matching parent EGP_STRUCTURE_TYPE row into the archive. When the internal name is omitted, use the display name. Allow an empty description. | Every new item structure name request | |
| Effective-date handling | UI: supplied effective start date. FSM: a current template field when one is available; otherwise no date value in the archive. | Stop only when the UI route is selected and no date is supplied | Inspect the current FSM template before preparation. For UI, require the date in the runbook. For FSM, use an explicit template field only when present and supplied; when absent, continue the FSM import without adding a column, requesting a date, or inferring a default. | Every new item structure name request | |
| Reference designator behavior | Reference Designator Range Indicator value selected from lookup type ORA_EGP_COMP_REF_DES_RANGE_IND; comma-separated individual values or a range using the selected character | Stop before validation | Supply a code or meaning that resolves uniquely to one enabled, effective value from ORA_EGP_COMP_REF_DES_RANGE_IND; provide examples that use the selected character for ranges | A Reference Designator Range Indicator value or a reference-designator range is requested | resolve_rd_range_indicator_lookup_value |
| Structure header attachments | Supplied attachment categories, or a target requirement for attachment categories | Stop before approval only when a supplied category is invalid or the target requires a category and none is supplied | Validate supplied categories against the exact target CategoryName values. When neither a category nor a target requirement exists, continue without an attachment-category row. | A category is supplied or the target structure type requires attachment categories | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The requested structure name has a display name, parent identity, effective-date handling, validation settings, and any attachment categories that are supplied or required by the target | Validated | Default an omitted internal name from the display name; allow an empty description; apply design enforcement and hand off the validated result | |
| An FSM archive includes a child structure-name row | Validated | Include the exact matching parent EGP_STRUCTURE_TYPE row from the same fresh export, using the same StructureTypeId. Keep it unchanged unless requested parent controls are also being changed. | |
| An FSM archive includes a child row but no matching parent EGP_STRUCTURE_TYPE row | Blocked | Rebuild the archive from a fresh export with the matching parent row. Do not generate a parent ID. | |
| The request proposes deleting, repurposing, or changing the seeded parent structure type | Blocked | Keep the seeded parent active; add or maintain a child structure name for the business need | |
| Enable Lifecycle Validation or Use Primary for Expansion is omitted | Validated | Default the omitted value to false (unchecked) | |
| Lifecycle validation is supplied | Validated | Normalize and use the supplied LifecycleValidationFlag; do not request a separate business justification | |
| Quantity Related is enabled | Validated | Confirm the business need requires reference-designator quantity to match component quantity | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Reference designator range lookup value | Reject a requested indicator unless it exactly matches one enabled, effective code or meaning from lookup type ORA_EGP_COMP_REF_DES_RANGE_IND | A Reference Designator Range Indicator value is supplied | resolve_rd_range_indicator_lookup_value |
| Reference designator range format | Accept comma-separated entries as individual values. For a range, require the validated range character between the lower and upper values, for example RX01-RX05 when hyphen is selected; reject a comma as the range indicator | A range is requested | resolve_rd_range_indicator_lookup_value |
| Enable Lifecycle Validation / LifecycleValidationFlag | When supplied, accept `true`, `Y`, `Yes`, or `1` and normalize to `1` (enabled). Accept `false`, `N`, `No`, or `2` and normalize to `2` (disabled). Treat text input case-insensitively and reject every other supplied value. When omitted, default to `2` (disabled). | A structure name is created or changed through FSM CSV | |
| Use Primary for Expansion | When supplied, accept a Boolean value. When omitted, default to `false` (unchecked). | A structure name is created or changed through FSM CSV | |
| Parent StructureTypeId | Preserve the identifier supplied for the existing seeded parent structure type. For an FSM child row, include its exact matching parent EGP_STRUCTURE_TYPE row in the same archive. Do not generate or require a new identifier. | A structure name is added or maintained | |
| Internal Name | Use the supplied value when present. When absent, set it to the display name; do not request a separate value. | Every new structure name request | |
| Description | Accept a supplied description or an empty value; do not request a description. | Every new structure name request | |
| Effective start date | For UI, require a supplied date. For FSM, populate a date only when the current template explicitly carries it and the user supplies it. If the field is absent, treat the omission as supported FSM behavior: continue without a date value in the archive, do not invent a CSV field, do not request a UI date, and do not infer a default date. | Every new structure name request | |
| Attachment category spelling | When a category is supplied or required, compare it against the exact CategoryName values in the populated setup-data export. Do not create a duplicate row when the canonical category already exists. When neither condition applies, skip category validation and do not add an attachment row. | A category is supplied or the target requires one | |
| No attachment category is supplied and the target does not require one | Treat the empty attachment list as valid and continue without an attachment-category row. | Neither condition applies | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| STRUCTURE_DETAILS.VALIDATE_REQUEST | decision | 10 | validate_input | valid->STRUCTURE_DETAILS.RESOLVE_RD_RANGE_INDICATOR;invalid->STRUCTURE_DETAILS.INVALID_REQUEST | none | stop | Any request to create, retire, or change an item structure type |
