# Manage Price Adjustments Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | DisplayPreferenceCode | ORA_DET | The implementer does not supply a display preference | Yes; customer confirmation is required before preview |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | ChargeLevelFlag | N | The implementer does not explicitly require charge-level adjustment use | Yes; set Y when the request requires direct subscription-charge adjustments |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | UserEnterableFlag | N | The implementer does not explicitly require manual subscription-user entry | Yes; set Y when manual entry is required |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | AllowAfterActivationFlag | N | The implementer does not explicitly require post-activation adjustment use | Yes; set Y when the request explicitly requires use after activation |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | AllowOverApplicationFlag | N | The implementer does not explicitly approve adjustment amounts above the line amount | Yes; set Y only when negative billing amounts or credits are approved |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | LookupCode ActiveFlag | Y | A new ORA_OSS_PRICE_ADJ_CATEGORY lookup code is created | No; a new lookup code must be active |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | LookupCode StartDateActive | 1991-01-01 | A new ORA_OSS_PRICE_ADJ_CATEGORY lookup code is created | Yes; customer confirmation is required before preview |  |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | ActiveFlag | true | The implementer does not provide the parent active state | Yes; present the default in the approval preview |  |

## Default Meanings

| Task Code | Task Name | Defaulted Field | Meaning to Present Before Confirmation |
|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | DisplayPreferenceCode ORA_DET | The detail preference displays the adjustment in the billing waterfall when detail mode is enabled; summary preference shows the adjustment only when summary mode is enabled. For price elements, the display preference controls whether the element is shown or hidden in the billing waterfall. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | ChargeLevelFlag N | The category is not available for direct subscription-charge adjustments. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | UserEnterableFlag N | Subscription users cannot manually add this adjustment; it is expected to originate from an upstream system. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | AllowAfterActivationFlag N | The adjustment cannot be applied after subscription activation. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | AllowOverApplicationFlag N | The adjustment cannot exceed the applicable line amount, avoiding an unapproved negative bill-line amount. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | New-category confirmation summary | When the implementer has not supplied a sequence, placement, or one or more defaultable fields, present all defaults together before asking for the missing choice: DisplayPreferenceCode ORA_DET (Detailed), ChargeLevelFlag N, UserEnterableFlag N, AllowAfterActivationFlag N, and AllowOverApplicationFlag N. |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | ActiveFlag true | The new variable is active unless the implementer explicitly chooses otherwise. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | PA.DEFAULT | step | 15 | apply_default | defaulted->PA.LOOKUP;confirmed_values->PA.LOOKUP;issues->RETURN_ISSUES | PA.VALIDATE | stop | Preparing a new price adjustment category and its lookup code |
