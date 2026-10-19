# Manage Disability Organizations Input Validation

## Purpose

Defines required inputs and field checks for Manage Disability Organizations.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, inactivate, or date-effective delete | Block | Provide one supported operation | Every request |  |
| Existing selector | Exact OrganizationId or Name | Block | Provide one exact selector | get, edit, inactivate, or delete | find_manage_disability_organizations |
| Create identity | Name | Block | Provide the organization name | create |  |
| Classification | ClassificationCode `HCM_DISABILITY_ORGANIZATION` | Block | Supply the classification row | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | create, edit, or inactivate |  |
| Delete effective context | Resolved current-row EffectiveStartDate | Block | Resolve the eligible row as of today | delete | resolve_disability_organization_delete_history |
| Edit changes | At least one supported change | Block | Provide the intended change | edit |  |
| Delete confirmation | Explicit confirmation of the displayed eligible current row | Block loader handoff | Show basic details and request confirmation | delete | resolve_disability_organization_delete_history |
| Organization EFF row | `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `OrgInformationContext`, and every configured multirow unique-key segment | Block | Complete the row from the current loader contract | An OrgInformation row is supplied | resolve_disability_organization_eff_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The target does not resolve exactly | Missing | Provide one exact selector | find_manage_disability_organizations |
| A create name already exists | Invalid | Supply a unique name | find_manage_disability_organizations |
| A supplied EFF segment is absent from its resolved context | Unsupported | Correct the context or segment | resolve_disability_organization_eff_context |
| A supplied EFF value does not resolve to one compatible stored value | Invalid | Correct the value | resolve_disability_organization_eff_segment_value |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Normalize an unambiguous date to the loader format; reject an invalid date | A date is supplied |  |
| Classification code | Require `HCM_DISABILITY_ORGANIZATION` | create |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Organization row and every included child row | create, edit, or inactivate |  |
| Set usage | Reject Set, SetCode, or SetId because Disability Organization is not set enabled | Any request |  |
| Mutation source scope | Keep the Organization and OrgUnitClassification rows. Include OrgInformation only when modified, with operation-required identity, parent, date, classification, flex/context controls, multirow identity, and only modified or operation-required segments from the resolved context; exclude other contexts and optional unchanged segments | create, edit, or inactivate |  |
| EFF context discriminator | Require `FLEX:PER_ORGANIZATION_INFORMATION_EFF` and `OrgInformationContext` to contain the same deployed context code | An OrgInformation row is supplied |  |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow OrgInformation context is supplied |  |
| EFF segment value | When the segment declares a value set, require one typed stored value for its declared target attribute; do not write display text when it differs | A Disability Organization EFF segment value is supplied | resolve_disability_organization_eff_segment_value |
| Supported fields | Reject response-only, audit, and unregistered loader fields | A mutation value is supplied |  |
| Date-effective split deletion | Allow deletion of noninitial future splits only with retained-predecessor `Organization` and `OrgUnitClassification` `MERGE` rows plus `SET PURGE_FUTURE_CHANGES Y`. Require the retained predecessor start and the inclusive end of the final split to remove; reject HDL `DELETE`, a missing classification association, first-row deletion, and unbounded ranges. | delete | resolve_disability_organization_delete_history |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DISORG.VALIDATE | decision | 1 | validate_input | valid->DISORG.READ;missing->DISORG.ERROR;invalid->DISORG.ERROR;unsupported->DISORG.ERROR | none | stop | Every Manage Disability Organizations request |
