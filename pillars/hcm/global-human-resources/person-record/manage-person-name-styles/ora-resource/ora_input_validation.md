# Manage Person Name Styles Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Person Name Styles.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, or ordinary field edit | Block | Deletion of a style or component is unsupported; reject requests to remove components, including updates to retain only a subset, before target reads or source preparation | Every request |  |
| Style scope | Country, legislation code, or exact person name style | Block | Provide one precise selector | Every request | find_manage_person_name_styles |
| Existing style selector | Exact country, legislation, or style | Block | Provide one exact selector | get or edit | find_manage_person_name_styles |
| Country-specific structure | Parent name style and requested child name-setup values | Block | Provide supported parent fields and each requested child component | create or edit | resolve_country_context |
| Edit changes | At least one explicit supported parent or child change | Block | Provide the intended change | edit |  |
| FSM source package | Exported package with ASM_SETUP_CSV_METADATA.xml and original scoped object CSV names | Block | Provide the intact reviewed FSM archive | create or edit | validate_parent_before_child |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A required Name Style does not resolve exactly once | Missing | Correct the legislation or style selector | find_manage_person_name_styles |
| Country or legislation does not resolve exactly once | Invalid | Correct the country context | resolve_country_context |
| A Name Component is disabled, incompatible, unresolved, or ambiguous | Invalid | Correct the component | resolve_name_style_component |
| The parent row is missing, follows a child, or has inconsistent child keys | Invalid | Correct the scoped parent and child rows | validate_parent_before_child |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name component | Require one enabled compatible PER_NAME_STYLE_ATTRIBUTES stored code | A Name Component is supplied | resolve_name_style_component |
| Required last name | Reject a component set that removes the required last-name component | create or edit changes components |  |
| Supported fields | Reject fields absent from the current person-name-style contract | A value is supplied |  |
| Component-output completeness | Require every available component column in source order, including `ColumnName`; when approved sources differ, require their identified union and source labels before the result is marked complete | A component read, export, or validation result is presented |  |
| FSM archive shape | Require exact-case ASM_SETUP_CSV_METADATA.xml and original object CSV names; reject conversion to an HCM Data Loader archive | create or edit | validate_parent_before_child |
| Parent grouping key | Require LegislationCode | A parent row is authored | validate_parent_before_child |
| Child grouping key | Require LegislationCode and ColumnName | A child row is authored | validate_parent_before_child |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNS.VALIDATE | decision | 1 | validate_input | valid->PNS.DEPENDENCY;missing->PNS.ERROR;invalid->PNS.ERROR;unsupported->PNS.ERROR | none | stop | Every Manage Person Name Styles request |
