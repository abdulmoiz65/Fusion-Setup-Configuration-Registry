# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business outcome | Desired Job Application outcome, affected users, timing, and requested review or mapping change | Return a business-language issue | Ask only for the missing business decision | Every request | |
| Mapping selection | One eligible context, one or more eligible segments, and one eligible Fast Formula per segment | Block artifact creation | Resolve the context and segments from a fresh EFF export and each formula from the delegated direct-read workflow | Mapping creation or replacement | resolve_computed_field_eff_scope |
| Target environment | Exact Fusion environment | Block baseline export and preview | Ask for the target environment | Mapping creation, replacement, import, or verification | |
| Legislative Data Group filter | Optional Legislative Data Group filter for formula discovery | Default to `Global` when omitted; honor an explicitly supplied value | Formula listing or mapping formula discovery | resolve_fast_formula_details |
| Fresh task baseline | Current task-level FSM ZIP containing ASM_SETUP_CSV_METADATA.xml and ORA_IRC_JA_COMPOUND_FIELD_DATA.csv | Block artifact creation | Run shared.setup-export.task-level-export for this exact task | Mapping creation, replacement, or import | export_current_computed_field_mappings |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A context is not enabled, is multi-row, or is outside PER_PERSON_EIT_EFF, PER_EIT, PER_PERSON_EIT_EFF | Blocked | Select an enabled single-row context in the fixed EFF scope | resolve_computed_field_eff_scope |
| A segment is absent from ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_SEGMENT.csv, disabled, date, or number | Blocked | Select an enabled non-date, non-number segment from the authoritative segment-definition file | resolve_computed_field_eff_scope |
| A formula does not resolve to exactly one eligible effective result | Blocked | Correct the formula selection or Fast Formula configuration before building an artifact | resolve_fast_formula_details |
| Existing mapping rows are present | Blocked | Manually delete them in the FSM task, confirm deletion, and run a fresh task export | export_current_computed_field_mappings |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Formula metadata completeness | Require exact FormulaName, BaseFormulaName, FormulaId, FormulaTypeId, effective dates, formula type, Compiled Y, and CompileStatus V | Every proposed formula | resolve_fast_formula_details |
| Formula type | Require the display type Recruiting Job Application Computed Field | Every proposed formula | resolve_fast_formula_details |
| Global formula result | Accept a blank Legislative Data Group returned for a formula as valid global scope; this is distinct from the discovery-filter default | Every proposed formula | resolve_fast_formula_details |
| Mapping uniqueness | Enforce one formula per segment and one segment per formula across the complete proposal; do not use FormulaId or FormulaTypeId as the duplicate key | Every proposed mapping set | |
| Formula Text exclusion | Discard Formula Text; do not display, persist, validate, or place it in the CSV or ZIP | Every formula response | |
| CSV header | Require exactly FlexContextCode, FlexSegmentCode, FormulaBaseFormulaName, FormulaCode, FormulaFormulaTypeId, FormulaBaseFormulaTypeName in that order | Immutable mapping CSV | |
| CSV identity | Set FormulaBaseFormulaTypeName to IRC_JA_COMPUTED_FIELD and never to the display label | Every mapping row | |
| CSV field mapping | Use the selected exact context and segment codes, exact delegated BaseFormulaName as FormulaBaseFormulaName, exact FormulaId as FormulaCode, and exact FormulaTypeId as FormulaFormulaTypeId | Every mapping row | resolve_fast_formula_details |

The exact CSV header is:

```text
"FlexContextCode","FlexSegmentCode","FormulaBaseFormulaName","FormulaCode","FormulaFormulaTypeId","FormulaBaseFormulaTypeName"
```

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JACF.VALIDATE_INTAKE | decision | 1 | validate_input | eff_review->JACF.RESOLVE_EFF;formula_review->JACF.RESOLVE_FORMULAS;mapping->JACF.RESOLVE_EFF;issues->JACF.INPUT_ISSUES | none | stop | Every Job Application computed-field request |
