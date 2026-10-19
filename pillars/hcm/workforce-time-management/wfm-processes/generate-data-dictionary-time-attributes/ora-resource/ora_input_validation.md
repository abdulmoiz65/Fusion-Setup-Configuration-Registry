# Input validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target environment | fusion_environment_context | Block preview | Supply the configured target environment | Every ESS request | |
| Include Payroll Time Type | include_payroll_time_type | Apply default | Use the documented default | Every ESS request | |
| Legislative Data Group scope | ldg_scope equals all or specific | Block preview | Ask: Should I run it for all Legislative Data Groups or a Specific Legislative Data Group? | Every ESS request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Include Payroll Time Type is Y or N | Accept only Y or N; any other supplied value blocks preview | A value is supplied | |
| All LDGs selection | Set display.attribute4.value to null and omit submit.argument4 | ldg_scope is all | |
| Specific Legislative Data Group selection | Prompt the user to select one available LOV option; do not use its display value as the ESS argument | ldg_scope is specific | resolve_legislative_data_group |
| Unsupported Scheduler arguments | Omit submit.argument2 and submit.argument3; do not create blank or additional arguments | Every resolved payload | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TDL.DDTA.VALIDATE_INPUTS | decision | 10 | validate_input | valid->TDL.DDTA.APPLY_DEFAULT;invalid->RETURN_ISSUES | none | stop | Every ESS request |
