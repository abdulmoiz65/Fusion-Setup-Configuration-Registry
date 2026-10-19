# Manage Divisions Input Validation

## Purpose

Defines required inputs and field checks for Manage Divisions.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, inactivate, or delete-effective-split | Block | Provide one supported operation | Every request |  |
| Existing selector | Exact Name | Block | Provide one exact selector | get, edit, inactivate, or delete-effective-split | find_manage_divisions |
| Create identity | Name | Block | Provide one exact unique Name | create |  |
| Classification | ClassificationCode `HCM_DIVISION` | Block | Supply the classification row | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | create, edit, or inactivate |  |
| Effective-split deletion range | Exact existing Division, retained EffectiveStartDate, and last deleted EffectiveEndDate | Block | Resolve the complete affected history and provide the inclusive deletion range | delete-effective-split | resolve_division_delete_history |
| Edit changes | At least one supported change | Block | Provide the intended change | edit |  |
| Delete confirmation | Explicit confirmation of the displayed effective-split range | Block loader handoff | Show basic details and request confirmation | delete-effective-split | resolve_division_delete_history |
| Organization EFF row | `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `OrgInformationContext`, and every configured multirow unique-key segment | Block | Complete the row from the current loader contract | An OrgInformation row is supplied | resolve_division_eff_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The target does not resolve exactly | Missing | Provide one exact selector | find_manage_divisions |
| A create Name already exists | Invalid | Supply a unique Name | find_manage_divisions |
| A supplied EFF segment is absent from its resolved context | Unsupported | Correct the context or segment | resolve_division_eff_context |
| A supplied EFF value does not resolve to one compatible stored value | Invalid | Correct the value | resolve_division_eff_segment_value |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Normalize an unambiguous date to the loader format; reject an invalid date | A date is supplied |  |
| Classification code | Require `HCM_DIVISION` | create |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Organization row and every included child row | create, edit, or inactivate |  |
| Set usage | Reject Set, SetCode, or SetId because Division is not set enabled | Any request |  |
| Mutation source scope | For create, edit, or inactivate, keep the Organization and OrgUnitClassification rows. Include OrgInformation only when the user explicitly requests an Organization Information/EFF change and supplies its resolved context and values; otherwise remove the OrgInformation worksheet and its Data Loader Map row before DAT generation. For delete-effective-split, retain the `Organization` MERGE fields required to identify the resolved range, `SET PURGE_FUTURE_CHANGES Y`, and at least one operation-required `OrgUnitClassification` association; omit OrgInformation and non-key attributes. | create, edit, inactivate, or delete-effective-split |  |
| Date-effective split deletion | Allow deletion of one or more noninitial future effective splits only with `SET PURGE_FUTURE_CHANGES Y`, an `Organization` MERGE row, and at least one operation-required `OrgUnitClassification` association. Require EffectiveStartDate to identify the last record to retain and EffectiveEndDate to identify the final split to delete. Reject HDL DELETE, first-row deletion, and an unbounded, nonadjacent, or misaligned range. | delete-effective-split | resolve_division_delete_history |
| EFF context discriminator | Require `FLEX:PER_ORGANIZATION_INFORMATION_EFF` and `OrgInformationContext` to contain the same deployed context code | An OrgInformation row is supplied |  |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow OrgInformation context is supplied |  |
| EFF segment value | When the segment declares a value set, require one typed stored value for its declared target attribute; do not write display text when it differs | A Division EFF segment value is supplied | resolve_division_eff_segment_value |
| Supported fields | Reject response-only, audit, and unregistered loader fields | A mutation value is supplied |  |
| Delete boundary | Reject complete delete or ZAP; allow only the confirmed noninitial future split range | delete-effective-split | resolve_division_delete_history |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DIV.VALIDATE | decision | 1 | validate_input | valid->DIV.READ;missing->DIV.ERROR;invalid->DIV.ERROR;unsupported->DIV.ERROR | none | stop | Every Manage Divisions request |
