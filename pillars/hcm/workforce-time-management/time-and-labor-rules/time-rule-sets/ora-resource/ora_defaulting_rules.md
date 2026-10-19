# Time Rule Sets defaulting rules

Source: the requested runtime defaults for Time Rule Set parent and member CSV rows, corrected by the observed parent-import and member-verification results.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ViewInstanceName | RuleSetsVO | ViewInstanceName is blank on a parent row in ORA_HWM_RULE_SET.csv | No | |
| GroupingKey | Copy RuleSetName from the same row | GroupingKey is blank on a parent row in ORA_HWM_RULE_SET.csv | No | |
| EffectiveStartDate | Current Date | A user-provided EffectiveStartDate is absent on a new parent row in ORA_HWM_RULE_SET.csv | No; retain the user-provided date when present | |
| EffectiveEndDate | 4712/12/31 | EffectiveEndDate is blank on a new parent row in ORA_HWM_RULE_SET.csv | No | |
| RuleSetUnqId | Leave blank in a new parent input row; Fusion assigns the committed value | A new parent row in ORA_HWM_RULE_SET.csv is prepared | Yes | |
| ViewInstanceName | RuleSetMbrsVO | ViewInstanceName is blank on a member row in ORA_HWM_RULE_SET_MBR.csv | No | |
| RuleSetUnqId | Copy the committed RuleSetUnqId from the matching parent row in the authoritative current Time Rule Sets export | A member row in ORA_HWM_RULE_SET_MBR.csv is prepared after parent commit and export refresh | Yes | resolve_parent_rule_set_unique_id |
| GroupingKey | Concatenate the committed RuleSetUnqId, a comma, and ProcessingOrder with no spaces | A member row in ORA_HWM_RULE_SET_MBR.csv is prepared after RuleSetUnqId is resolved | Yes | |

## Effective Start Date Selection

| Situation | Value to Use | What Must Not Happen |
|---|---|---|
| A user provides an Effective Start Date | Use the user-provided date | Do not apply or retain the Current Date default |
| A user does not provide an Effective Start Date | Apply Current Date as the default | Do not retain a second Effective Start Date value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RULESET.APPLY_DEFAULTS | step | 1 | apply_default | defaulted->RULESET.RESOLVE_MEMBER_PARENT;not_applicable->RULESET.RESOLVE_MEMBER_PARENT;failed->RULESET.DEFAULT_ERROR | none | stop | A Time Rule Set parent CSV row is prepared |
| RULESET.APPLY_MEMBER_DEFAULTS | step | 3 | apply_default | defaulted->RULESET.VALIDATE_INPUT;not_applicable->RULESET.VALIDATE_INPUT;failed->RULESET.DEFAULT_ERROR | RULESET.RESOLVE_MEMBER_PARENT | stop | A Time Rule Set member CSV row is prepared |
