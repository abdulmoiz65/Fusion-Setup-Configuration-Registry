# Manage Enterprise HCM Information Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Enterprise HCM Information.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, edit, or date-effective delete | Block | Provide one supported operation | Every request |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | get or edit | find_enterprise |
| Delete effective context | Resolved current-row EffectiveStartDate | Block | Resolve the eligible row as of today | delete | resolve_enterprise_delete_history |
| Requested scope | Enterprise parent field, exact EFF context, exact segment, or an explicit request to show all Additional Information contexts | Block | Identify the value to read or edit | get or edit | resolve_enterprise_read_scope |
| Edit changes | At least one exact segment and proposed value | Block | Provide the intended change | edit | resolve_enterprise_context |
| Delete confirmation | Explicit confirmation of the displayed eligible current row | Block loader handoff | Show basic details and request confirmation | delete | resolve_enterprise_delete_history |
| Enterprise EFF structure | Fresh Organization parent, `ENTERPRISE` OrgUnitClassification parent, and OrgInformation row | Block | Resolve the parent and classification before source preparation | edit supplies an OrgInformation row | resolve_enterprise_classification |
| Enterprise EFF row | Fresh existing-row identity, SequenceNumber, `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `OrgInformationContext`, and every configured multirow unique-key segment | Block | Read the current context row and complete it from the current loader contract | edit supplies an OrgInformation row | read_enterprise_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| No Enterprise row covers the requested effective date | Missing | Correct the date | find_enterprise |
| The `ENTERPRISE` classification envelope is absent or ambiguous | Invalid | Stop before building the EFF row | resolve_enterprise_classification |
| The requested context or segment is absent, ambiguous, or belongs to another context | Unsupported | Select one current describe-declared context and segment | resolve_enterprise_context |
| All-context read was not explicitly requested | Unsupported | Select one context or explicitly ask to show all Additional Information contexts | read_all_enterprise_contexts |
| A proposed LOV value does not resolve to one metadata-compatible stored value | Invalid | Correct the value | validate_enterprise_segment_value |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Normalize an unambiguous date to yyyy-MM-dd; reject an ambiguous or invalid date | A date is supplied |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Organization row and every included child row | edit |  |
| Set usage | Reject Set, SetCode, or SetId because Enterprise is not set enabled | Any request |  |
| Effective coverage | Require the date to fall within both the Enterprise and `ENTERPRISE` classification effective ranges | An EFF value is read or edited | find_enterprise |
| Mutation source scope | For an existing Enterprise EFF update, include the Organization row, the freshly resolved existing OrgUnitClassification row, and each changed OrgInformation row. Carry the resolved surrogate identity for every included logical row, use one logical-object effective date, and include the required classification, flex/context controls, and configured context segments | edit | resolve_enterprise_classification |
| Classification identity | Use the freshly resolved OrganizationId and OrgUnitClassificationId with CategoryCode `ENTERPRISE`; reject stale or user-invented IDs | edit | resolve_enterprise_classification |
| EFF controls | In the generated DAT require both `FLEX:PER_ORGANIZATION_INFORMATION_EFF` and `OrgInformationContext` to equal the resolved deployed context, and require `EFF_CATEGORY_CODE=ENTERPRISE` | edit | resolve_enterprise_context |
| Segment ownership | Reject a segment that is not declared under the resolved context | A segment is supplied | resolve_enterprise_context |
| Segment type | Require the metadata-declared native type and stored value; reject a display value when the stored value differs | A segment value is supplied | validate_enterprise_segment_value |
| Context cardinality | Honor the current metadata cardinality; reject an extra row for a single-row context | An EFF row is authored | resolve_enterprise_context |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow OrgInformation context is supplied | resolve_enterprise_context |
| Supported fields | Reject response-only audit fields, links, and fields absent from the current parent or EFF contract | A value is supplied |  |
| Verification boundary | Do not treat source generation, transport, or load acceptance as business verification | edit |  |
| Delete boundary | Reject complete delete or ZAP; allow only the confirmed current date-effective row when it is not the first row | delete | resolve_enterprise_delete_history |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENT.VALIDATE | decision | 1 | validate_input | valid->ENT.READ;missing->ENT.ERROR;invalid->ENT.ERROR;unsupported->ENT.ERROR | none | stop | Every Manage Enterprise HCM Information request |
