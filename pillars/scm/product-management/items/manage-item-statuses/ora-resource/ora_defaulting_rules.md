# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Status Code | First 10 non-space characters of Status Name | An explicit create request supplies Status Name and omits Status Code | No | derive_status_code_from_name |
| Status Code | Exact existing item-status StatusCode | Status Code is omitted and Status Name is provided | No | resolve_item_status_identity |
| Status Name | Exact existing item-status StatusName | Status Name is omitted and Status Code is provided | No | resolve_item_status_identity |
| StatusControl | None | StatusControl is omitted from the StatusAttributeValue child resource | No | |

`derive_status_code_from_name` removes spaces from the supplied Status Name and retains the first 10 remaining characters. It preserves the original case. If no characters remain, validation fails. The derived code is shown in the execution preview and is checked for a case-insensitive target-environment code collision and an exact name collision before submission.

When a derived code collides case-insensitively in the target-environment item-status collection but the exact Status Name does not, `derive_unique_status_code` tries positive numeric suffixes in order. For suffix `n`, it retains the first `10 - len(str(n))` characters of the initial derived code and appends `n`; it checks every candidate with the same case-insensitive collection scan before trying the next one. Thus `VStatusTes` becomes `VStatusTe1`, then `VStatusTe2`, and `VStatusT10`. It never exceeds 10 characters, never replaces an explicitly supplied Status Code, and stops if it cannot find an available candidate. A Status Name collision always blocks the create request; it is never remapped.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IST.DERIVE_CREATE_STATUS_CODE | step | 4 | apply_default | derived->IST.VERIFY_DERIVED_CREATE_STATUS_CODE;not_applicable->IST.RESOLVE_ITEM_STATUS_IDENTITY;invalid->RETURN_ISSUES | none | stop | An explicit create request supplies Status Name and omits Status Code |
| IST.VERIFY_DERIVED_CREATE_STATUS_CODE | step | 5 | reference_lookup | available->IST.CONFIRM_DERIVED_STATUS_CODE;code_collision->IST.DERIVE_UNIQUE_STATUS_CODE;name_collision->RETURN_ISSUES;failure->RETURN_ISSUES | IST.DERIVE_CREATE_STATUS_CODE | stop | A create Status Code was derived from Status Name |
| IST.DERIVE_UNIQUE_STATUS_CODE | step | 6 | apply_default | candidate->IST.VERIFY_DERIVED_CREATE_STATUS_CODE;exhausted->RETURN_ISSUES | IST.VERIFY_DERIVED_CREATE_STATUS_CODE | stop | The initially derived Status Code collides but the Status Name is available |
| IST.CONFIRM_DERIVED_STATUS_CODE | decision | 7 | require_confirmation | confirmed->IST.REVERIFY_CONFIRMED_STATUS_CODE;rejected->RETURN_ISSUES | IST.VERIFY_DERIVED_CREATE_STATUS_CODE | stop | An available derived or numbered Status Code is ready for user confirmation |
| IST.REVERIFY_CONFIRMED_STATUS_CODE | step | 8 | reference_lookup | available->IST.VALIDATE-INPUT;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | IST.CONFIRM_DERIVED_STATUS_CODE | stop | The user confirmed an available derived or numbered Status Code |
| IST.RESOLVE_ITEM_STATUS_IDENTITY | step | 9 | reference_lookup | resolved->IST.VALIDATE-INPUT;missing->IST.VALIDATE-INPUT;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | none | stop | A Status Code, Status Name, or both are supplied before input validation when create-code derivation does not apply |
| IST.DEFAULT_STATUS_CONTROL | decision | 20 | apply_default | defaulted->IST.DETERMINE_OPERATIONAL_ATTRIBUTE_LOOKUP;provided->IST.RESOLVE_STATUS_CONTROL | IST.VALIDATE-INPUT | stop | A StatusAttributeValue child resource is supplied after input validation |
