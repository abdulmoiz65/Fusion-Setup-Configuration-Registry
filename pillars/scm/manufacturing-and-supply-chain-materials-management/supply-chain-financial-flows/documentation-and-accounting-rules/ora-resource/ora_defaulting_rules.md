# Defaulting Rules

Source: DAR create-input policy supplied by the implementation owner.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TrackProfitsFlag | false | Every create when TrackProfitsFlag is not supplied | Conditional: true is allowed only when TradeDistributions is Y | |
| EffectiveEndDate | Leave blank for Fusion defaulting | Every create when EffectiveEndDate is omitted or explicitly none | No; retain resolved source dates for Correct and EndDate | |

## Defaulting Outcomes

Evaluate this node for every supported operation. For creation, return applied
after setting an omitted TrackProfitsFlag to false and leaving an omitted
EffectiveEndDate blank, unchanged when a supplied value is eligible, or
invalid_override when a supplied true value is not eligible. For Correct and
EndDate, preserve the resolved existing values, apply no create defaults, and
return not_applicable. The not_applicable outcome is a completed no-change
evaluation, not a skipped prerequisite.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FO.DAR.DEFAULT-TRACK-PROFITS | step | 3 | apply_default | applied->FO.DAR.CONFIRM-BO-CONTRACT;unchanged->FO.DAR.CONFIRM-BO-CONTRACT;not_applicable->FO.DAR.CONFIRM-BO-CONTRACT;invalid_override->RETURN-ISSUES | FO.DAR.VALIDATE-INSERT-RECORD | stop | Always; apply create defaults only for creation and preserve existing values for Correct and EndDate |
