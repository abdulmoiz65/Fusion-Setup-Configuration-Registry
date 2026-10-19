# Input Validation

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Priority and sort pairing | Apply the documented UI defaulting rule; a sort value is cleared when its corresponding priority is cleared | Priority1Code through Priority5Code changes | |
| Priority selection uniqueness | Do not accept a resolved priority code that duplicates another selected priority code | Two or more priority values are supplied | resolve_pick_sequence_rule_type |
| sequenceDFF child content | Preserve DFF values only when the Additional Information section is visible; do not validate or synthesize segment fields locally | sequenceDFF values are supplied | |
| StartDateActive and EndDateActive format | Preserve a blank EndDateActive value. Obtain a generated `releaseSequenceRules` Data Loader sample for the selected Fusion environment through `core.data-loader`, then use its attribute details and editable workbook as the authoritative active-date representation. Preserve a supplied active-date value only when it matches that generated contract; do not infer a timezone, accepted local format, ISO representation, or default from another task. | StartDateActive or EndDateActive is supplied, including an update that changes only a different attribute | `core.data-loader` generated sample |
| FSM package members | Preserve exactly `ASM_SETUP_CSV_METADATA.xml`, `WSH_PICK_SEQUENCE_RULE.csv`, and `WSH_PICK_SEQUENCE_RULE_TRANSLATION.csv` from the export template; preserve member names, CSV headers, column order, and metadata XML | FSM Import is explicitly selected | |
| FSM active-date format | Preserve the exact active-date representation evidenced by the current same-environment FSM export for `WSH_PICK_SEQUENCE_RULE.csv`. If the export does not establish the representation, block preparation and request task-specific export evidence; do not use a REST or another task’s format. | FSM Import is explicitly selected and an active date is supplied | FSM export template |
| FSM priority representation | Populate the exported backend priority/sort columns together with Priority1Rule through Priority5Rule and Priority1Sort through Priority5Sort; resolve friendly values only by an approved resolver or an exact same-environment export | FSM Import is explicitly selected | |
| Empty FSM DFF/attribute columns | Preserve exported DFF/attribute columns as blank when no DFF value is supplied; do not block an FSM import solely because those blank columns exist | FSM Import is explicitly selected and no DFF/attribute value is supplied | |

Fusion and Data Loader own mandatory-field, datatype, uniqueness, server-side, and DFF-schema validation. This task-local file contains only sourced Redwood UI behavior.

### Source and Provenance

The active-date contract is deliberately not derived from Ship Confirm Rules or any other Shipping task. Its authoritative source is the current selected-environment Data Loader metadata and template for the registered `releaseSequenceRules` business object, generated using the Download Fusion Data Loader Sample workflow in `../SKILL.md`. The Data Loader workflow requires live UCM template and attribute validation before preparation or upload (`core/data-loader/SKILL.md`, “Generate a sample XLSX workbook or explicitly requested DAT file” and “Validate a source file before upload”). If the generated sample does not establish an active-date representation, stop the task as `catalog_or_metadata_mismatch` and request the exact task-specific template evidence; do not normalize or synthesize the value locally.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSR.VALIDATE_UI_INPUT | decision | 10 | validate_input | valid->RSR.CHECK_LOV_READINESS;invalid->RSR.HANDLE_ISSUE | none | stop | Release Sequence Rules input is prepared for Data Loader validation |
