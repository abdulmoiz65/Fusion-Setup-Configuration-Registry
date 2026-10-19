# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Activity type identity | Group Label, Activity Type Label, English Display Name | Stop before preview | Extract clear equivalents from a free-format workbook, then request only the missing or ambiguous stable labels and display name | Every proposed activity type | |
| Required activity type configuration | Active, Default Duration (min) | Stop before preview | Extract clear equivalents from a free-format workbook, then request only a missing or ambiguous active value or duration | Every proposed activity type | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Labels are stable identifiers | Require each group and activity type label to be unique and stable; do not use a display name as a label | Every proposed group or activity type | |
| Active is boolean | Accept only TRUE or FALSE after normalization from the workbook Yes or No value | Every proposed activity type | |
| Group alignment | Require groupLabel to equal the selected group label and verify that group before a type write | Every proposed activity type | |
| Default duration range | Require an integer from 1 through 1440 minutes | Every proposed activity type | |
| Translation language eligibility | Accept a translation only when its language code is returned by the target-environment active-language lookup | Every translation row | resolve_active_languages |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.VALIDATE | step | 1 | validate_input | valid->AT.LOOKUP_CURRENT_STATE;invalid->AT.RETURN_ISSUES | none | stop | Before any current-state check or REST preview for Activity Types |
