# Design enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Validate task inputs | Include Payroll Time Type is valid or receives the documented default. |
| 2 | Select LDG scope | Ask whether the request applies to all LDGs or one specific LDG. |
| 3 | Resolve LDG selection | For all LDGs, set display.attribute4.value to null. For a specific LDG, resolve one current LOV ID. |
| 4 | Produce ESS preview | Show the environment and redacted resolved request before approval. The preview must visibly show Job, Include Payroll Time Type, and Legislative Data Group. For all LDGs, show All LDGs; for a specific LDG, show its resolved display value and ID. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every ESS request | Error | | The job definition, application, product, immediate-only schedule, or resolved argument mapping differs from the verified task contract | Rebuild the request from the verified contract | Yes |
| Every ESS request | Error | | The user has not selected all LDGs or specific LDG before preview | Ask for the LDG scope selection | Yes |
| Every ESS preview | Error | | Job, Include Payroll Time Type, or Legislative Data Group is not visibly shown in the preview | Re-render the preview with all three required fields before requesting approval | Yes |
| The user chooses specific LDG | Error | resolve_legislative_data_group | The selection does not resolve to exactly one current LOV ID | Select one current Legislative Data Group from the available LOV options | Yes |
| The user chooses all LDGs | Error | | display.attribute4.value is not null or submit.argument4 is present | Rebuild the all-LDG request with null display.attribute4.value and no submit.argument4 | Yes |
| Immediately before live ESS submission | Error | | The target environment or any editable request value changed after preview, or explicit approval for that exact preview is absent | Revalidate and show a new preview before requesting approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_legislative_data_group | The user chooses specific LDG | Current matched Legislative Data Group ID | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TDL.DDTA.ESS_PREVIEW | decision | 40 | design_enforcement | preview-ready->TDL.DDTA.APPROVAL_GATE;blocked->RETURN_ISSUES | TDL.DDTA.RESOLVE_LDG | stop | Every resolved ESS request |
