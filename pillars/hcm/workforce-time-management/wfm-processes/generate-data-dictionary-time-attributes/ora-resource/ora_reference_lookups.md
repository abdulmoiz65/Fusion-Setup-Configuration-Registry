# Reference lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_legislative_data_group | The user chooses specific LDG and must select an available LOV value | User-selected Legislative Data Group display value or current ID | GET {HCM_BASE}/legislativeDataGroupsLOV | Current LOV identity, display value, and ID | Present current available LOV options, then match exactly one selected entry; an ID selection must match that same current entry | submit.argument4: resolved Legislative Data Group ID; display.attribute4.value: resolved Legislative Data Group ID | Block preview and request a unique valid selection |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The user chooses All LDGs | Do not run the lookup. Set display.attribute4.value to null and omit submit.argument4. |
| The user chooses specific LDG | Read the current available LOV options, prompt the user to choose one, then resolve it before payload preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TDL.DDTA.RESOLVE_LDG | decision | 30 | reference_lookup | resolved->TDL.DDTA.ESS_PREVIEW;all-ldgs->TDL.DDTA.ESS_PREVIEW;unresolved->RETURN_ISSUES | TDL.DDTA.APPLY_DEFAULT | stop | The user has selected the mandatory LDG scope |
