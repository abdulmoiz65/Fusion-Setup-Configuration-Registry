# Payroll Costing Value Sets Defaulting Rules

No observed test value is a universal Payroll Costing Value Set default. Preserve a user-supplied value only when it is confirmed for the target package contract, and do not synthesize unspecified attributes.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ModuleId | No global default | Every new or modified root Value Set | No | verify_target_module_evidence |
| ValueSetIdentifier | No generated or code-derived default | ValueSetIdentifier is needed by the target contract | No | |
| ValidationType | No global default; INDEP is allowed only for an explicit Independent request | ValidationType is supplied | No | |
| ValueDataType and ValueSubtype | No global default; VARCHAR2 and TEXT are allowed only for an explicit Character/Text request | ValueDataType or ValueSubtype is supplied | No | |
| MaximumLength, Precision, Scale, flags, ranges, security fields, and active dates | No default from the observed test record | The field is absent or a new root or child row is authored | No | |
| Relationship EnabledFlag | Do not enable a new relationship before all mappings are complete | A new related Value Set relationship is created | No | resolve_related_value_pair |
| Audit attributes | Fusion-managed; no authoring default | Any CSV row is prepared | No | |

## Observed Values That Are Not Defaults

| Observed Value | Status | Required Treatment | Evidence |
|---|---|---|---|
| ModuleId = 61ECAF4AAAEAE990E040449821C61C97 | Release-specific observation | Revalidate against the target environment before any use | SUP-TEST-EXPORT, 11.13.26.10.0 |
| MaximumLength = 3 | Example-only observation | Require a compatible requested length; do not copy it | SUP-TEST-EXPORT, 11.13.26.10.0 |
| UppercaseOnlyFlag = N; ZeroFillFlag = N; SecurityEnabledFlag = N | Example-only observation | Do not infer flag values for another Value Set | SUP-TEST-EXPORT, 11.13.26.10.0 |
| Value = 001; Description = Test Value 001; EnabledFlag = Y | Example-only observation | Do not treat as seeded configuration or a template value | SUP-TEST-EXPORT, 11.13.26.10.0 |

## Defaulting Boundaries

| Situation | Treatment |
|---|---|
| A user asks for an unconfirmed CSV enum, datatype, subtype, relationship orientation, mutability rule, or required field | Treat the item as TBD and stop before authoring it |
| A user omits an audit value | Leave it unsynthesized; do not infer Fusion-generated data |
| A user omits a CSV file from a downloaded package | Retain the file with its header row; omission is not a defaulting mechanism |
| A user asks to delete by omitting a record | Refuse the operation; absence is not a delete contract |
