# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required scoped input is missing or structurally invalid | Return the exact missing or invalid field and stop |
| Delete or another unsupported operation is requested | Refuse the request and identify Read, Add, and Update as the supported operations |
| Exclude Subcategory is requested without a selected subcategory | Return a blocking validation issue and stop |
| Category value cannot be resolved to one Category Code for the selected Family | Return a blocking validation issue and stop |
| Subcategory value cannot be resolved to one Subcategory Code for the resolved Family and Category Code | Return a blocking validation issue and stop |
| Subcategory is ALL but the Family and Category prefix is not supported | Return a blocking validation issue and stop |
| Subcategory list has an empty code, duplicate code, or ALL mixed with another code | Return a blocking validation issue and stop |
| Supported combination catalog has no matching family, family-category prefix, ALL prefix, or supplied subcategory code | Return a blocking validation issue and stop |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | View All, Family, Category, or Subcategory rules fail | Correct the supplied values |
| unsupported operation | Delete or an operation other than Read, Add, or Update is requested | Use a supported operation; do not attempt a delete |
| input validation | An Add request selects a Family but no Category, or Exclude Subcategory has no selection | Supply the missing Category or Subcategory selection |
| catalog mismatch | A Category or Subcategory value resolves to no code or more than one code | Supply an exact value or code for the selected parent values |
| catalog mismatch | The supplied Family, Family and Category, ALL prefix, or one or more supplied subcategory codes are absent | Supply a supported value or combination |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | View All state, sanitized supplied field names, and the rule that failed |
| Combination validation failure | Match count only; do not expose unrelated catalog rows |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| View All is enabled | Do not validate, infer, or persist Family, Category, or Subcategory |
| Delete is requested | Do not delete the existing security profile; deletion is not supported by this skill |
| Exclude Subcategory is requested without a selected subcategory | Do not infer an excluded subcategory; require an explicit selection |
| Category or Subcategory value resolves to no code or more than one code | Do not guess or select a code automatically; request a more precise value or code |
| Subcategory is ALL and the Family and Category prefix is unsupported | Do not create or update a profile with ALL; correct the Family or Category |
| ALL is mixed with another code, or a subcategory list is empty or duplicated | Do not infer, expand, or silently deduplicate values; correct the supplied list |
| Scoped tuple is missing, absent, or ambiguous | Do not choose Family, Category, or Subcategory automatically |
| Supported combination catalog has no applicable match | Do not choose Family, Category, or Subcategory automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TSP.DONE_FAMILY_ONLY | terminal | 4 | terminal | none | TSP.RESOLVE_CATEGORY_CODE | stop | Supported operation and Family-only validation are complete |
| TSP.DONE_SCOPED | terminal | 5 | terminal | none | TSP.RESOLVE_SUBCATEGORY_CODE | stop | Supported operation, resolved codes, and scoped validation are complete |
| RETURN_ISSUES | terminal | 6 | terminal | none | none | stop | Input validation, value-to-code resolution, or supported-combination validation fails |
