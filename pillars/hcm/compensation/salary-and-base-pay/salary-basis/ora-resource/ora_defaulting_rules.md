# Defaulting Rules

## Salary Basis Defaults

| Field | Applies When | Default | Source | Resolution Rule | Override Behavior |
|---|---|---|---|---|---|
| Status | The user does not supply a status for a create, update, import, or validation request | Active | Enabled `ACTIVE_INACTIVE` lookup value | Resolve exact enabled meaning `Active` and use LookupCode `A` | When the user supplies a value, do not apply the default. Validate the supplied code or exact meaning through `resolve_salary_basis_status`. |
| Code | The user supplies SalaryBasisName and omits Code | Uppercase SalaryBasisName with spaces between words replaced by underscores | Task-local supplied SalaryBasisName | Trim outer spaces, convert letters to uppercase, and replace each run of spaces between words with one underscore. Preserve a supplied nonblank Code unchanged. | A supplied Code takes precedence but must satisfy the current SalaryBasis schema and duplicate check. |
| Annualization Factor | The user supplies a Frequency but does not supply an Annualization Factor | See frequency mapping below | Resolved `CMP_SALARY_BASIS` frequency code | Apply only the exact resolved frequency-code mapping below. | A user-supplied Annualization Factor always takes precedence; validate it against the current SalaryBasis schema and do not replace it. |
| Input Value Name | The user does not supply an Input Value Name | Amount | Current SalaryBasis schema and the selected payroll element context | Use `Amount` as the value, then apply the existing schema and dependency validation. | When the user supplies a value, do not apply the default; validate the supplied value using the existing validation rules. |
| Amount Decimal Precision | The user does not supply a parent precision and the current SalaryBasis schema declares the field | 2; for a rates-based basis, the selected overall rate's read-derived return precision takes precedence when the schema supports that mapping | Current SalaryBasis schema and selected rate-definition read evidence | Apply only after the parent and rate-component metadata validates the field and its supported target. | A user-supplied value takes precedence and must be an integer from 0 through 10 when the current schema accepts the documented numeric rule. |
| Range Error Warning | The user does not supply a range validation behavior and the current SalaryBasis schema declares the field | WARNING | Enabled `ORA_CMP_SAL_RANGE_VALIDATION` lookup value, subject to current lookup metadata | Resolve the enabled exact WARNING code only after current metadata confirms the lookup contract. | A user-supplied valid value takes precedence. Stop if WARNING is unavailable, ambiguous, disabled, or the schema does not support the field. |
| Calculated component type | A new simple-component child is explicitly configured as a calculated amount and current child metadata declares ComponentType | ORA_CALCULATED_AMOUNT | Current SalaryBasis child metadata | Set only the schema-supported ComponentType field for the child. | Do not default a different simple-component type or add an attribute child unless the user requested calculated configuration. |
| Calculated component factor | A calculated-component attribute omits ComponentFactor and current child metadata declares it | 1 | Current SalaryBasis child metadata | Apply after resolving the attribute parent and validating a nonnegative factor. | A user-supplied nonnegative schema-valid factor takes precedence. |

## Annualization Factor Frequency Mapping

| Resolved Frequency Code | Default Annualization Factor |
|---|---:|
| `ANNUAL` | 1 |
| `MONTHLY` | 12 |
| `BIMONTHLY` | 6 |
| `WEEK` | 52 |
| `BIWEEKLY` | 26 |
| `WORKDAY` | 260 |
| `HOURLY3` | 260 |
| `HOURLY2` | 365 |
| `LUNAR_MONTH` | 13 |
| `QUARTER` | 4 |
| `SEMI_YEAR` | 2 |
| `SEMI_MONTH` | 24 |
| `PERIOD` | No default |

For resolved `PERIOD`, the user must provide Annualization Factor. Do not infer a value. For a valid frequency code without a mapping above, also require the user to provide Annualization Factor rather than inventing a default.

## Defaulting Boundaries

- Defaulting a missing status does not bypass the current SalaryBasis schema check or the enabled `ACTIVE_INACTIVE` lookup check.
- Do not default a supplied blank, invalid, disabled, or ambiguous status value; stop with the existing status lookup validation gap.
- The resolved LookupCode, rather than the display meaning, is used in validated configuration data.
- A derived Code is a task-local transformation, not evidence that the current SalaryBasis schema accepts the value or that it is unique within the selected LDG.
- Defaulting Annualization Factor does not bypass the current SalaryBasis schema check. A supplied factor is never overwritten.
- Defaulting Input Value Name does not bypass the current SalaryBasis schema or dependency validation. Do not default a supplied blank or invalid value.
- The documented UI behavior that shows a null range-rounding value as precision 2 is presentation behavior, not an HDL/Data Loader default. Do not write RangeRoundingCode unless the user supplies it or current loader metadata declares an explicit supported default.
- Defaults for precision, range validation, calculated component type, and calculated component factor do not add unsupported parent or child fields. Resolve the current schema before preparing a source or preview artifact.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALB.DERIVE_CODE | step | 23 | apply_default | code_supplied_or_derived->SALB.RESOLVE_STATUS;code_unresolved->SALB.HANDLE_ISSUE | SALB.RESOLVE_LDG | stop | Before validating a Salary Basis code or preparing a create, update, import, or preview request |
