# Manage Collective Agreements Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Collective Agreements.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Existing agreement selector | Exact agreement identifier, IdentificationCode, or name | Block | Provide one exact business selector | get, edit, or delete | find_manage_collective_agreements |
| Create identity | Name and IdentificationCode | Block | Provide both business identity values | create |  |
| Effective context | Optional unambiguous read date, effective start date for create, explicit edit date for edit, or selected effective row for delete | Block when required | Provide the operation-specific effective context | Every request |  |
| Create scope | Status and country or legislation when required by the registered Data Loader object | Block | Provide each required scoped value | create | resolve_status_lookup |
| Edit changes | At least one explicit Data Loader-supported change | Block | Provide the intended supported changes | edit |  |
| Source-key provenance | No source keys, or both SourceSystemOwner and SourceSystemId explicitly supplied | Block | Omit source keys or provide the complete pair | A mutation supplies source keys |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing target does not resolve to exactly one effective agreement | Missing | Request one exact identifier, code, or name | find_manage_collective_agreements |
| A create identity matches an existing agreement | Invalid | Stop the duplicate create | find_manage_collective_agreements |
| A supplied status or configured lookup value does not resolve to one enabled effective stored value | Invalid | Request one exact code or meaning | resolve_status_lookup |
| A supplied Legal Employer, Union, or bargaining unit is unresolved, inactive, ineffective, or incompatible with the legislation scope | Invalid | Correct the organization reference before source preparation |  |
| A requested EFF context or segment is not supported by current metadata | Unsupported | Stop before source preparation | resolve_collective_agreement_eff_metadata |
| An EFF value requiring an LOV does not resolve to one compatible typed stored value | Invalid | Correct the value before source preparation | resolve_collective_agreement_eff_value_set |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Date format | Normalize an unambiguous user date to ISO for reads and to `YYYY/MM/DD` for every Data Loader DAT date column; reject an ambiguous date | A date is supplied |  |
| Effective range | Reject an end date earlier than its start date | Both dates are supplied |  |
| Name and code fidelity | Preserve exact case and characters unless the registered object documents normalization | Name or IdentificationCode is supplied |  |
| Exact-match cardinality | Reject zero or multiple exact targets and never choose a result by position | One agreement must resolve | find_manage_collective_agreements |
| Prohibited supplied values | Reject response-only IDs, audit fields, links, generated keys, and display-only values from a prior run | Any such value is supplied |  |
| Source contract | Reject unsupported columns, partial keys, missing required fields, or an operation unsupported by the registered Data Loader object | Preparing a mutation source |  |
| EFF stored value | Write only the metadata-declared stored code or ID in its declared native type; never write its display companion | An EFF segment value is supplied | resolve_collective_agreement_eff_value_set |
| EFF unique reference | Require the context-specific unique segment and DataType from current metadata; reject blank, duplicate, decorated, concatenated, or non-round-tripping values | An EFF row is requested | resolve_collective_agreement_eff_metadata |
| EFF row identity | Use distinct positive ordinals per parent and context for create; preserve the resolved row value for edit; keep SequenceNumber independently distinct | Multiple EFF rows are authored | resolve_collective_agreement_eff_metadata |
| Parent-child workbook | Include the parent and every requested CollectiveAgreementsExtraInfo row together, repeat IdentificationCode, and leave CollectiveAgreementId blank on create when the code resolves the parent | An EFF row is requested |  |
| Supported headers | Populate only supported headers carrying required or requested values; omit blank template-only columns from METADATA | Preparing a mutation source |  |
| Country-specific EFF context | Validate a context exposed by current describe independently even when its legislation differs from the parent | A country-specific EFF context is requested | resolve_collective_agreement_eff_metadata |
| Verification boundary | Do not treat transport or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.VALIDATE | decision | 1 | validate_input | valid->CA.DEPENDENCIES;missing->CA.ERROR;invalid->CA.ERROR;unsupported->CA.ERROR | none | stop | Every collective agreement request |

## Date-effective Split Deletion

- A delete requires a complete ordered split history and one selected EffectiveStartDate. Fetch and display all splits through hcmDateEffectiveObjectChanges before source preparation.
- Reject REST DELETE, ZAP, permanent deletion, and any Data Loader operation other than MERGE.
- For a middle split, the source contains only the selected split deletion and a predecessor EffectiveEndDate update to the selected split former end date.

## HDL MERGE Split Cases

| Split case | Required Data Loader MERGE rows | Preserved rows |
|---|---|---|
| Only split | Unsupported by the bounded-purge pattern; stop before preview or source generation | N/A |
| First of multiple splits | Unsupported by the bounded-purge pattern; stop before preview or source generation | N/A |
| Middle split | One selected-split deletion row plus one predecessor EffectiveEndDate update to the deleted split former end date | All earlier rows except that predecessor end date; all later splits |
| Last split | One selected-split deletion row plus one predecessor EffectiveEndDate update to the deleted split former end date | All earlier rows except that predecessor end date |
| Multiple selected splits | One approved merge operation at a time, newest to oldest, with fresh split resolution before each operation | Every row not in the current approved operation |

## Mutation Transport Validation

Reject any deletion or effective-date update that targets hcmDateEffectiveObjectChanges. The mutation must be represented only as an HDL/Core Data Loader MERGE source.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

Use exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row, with DAT dates in `YYYY/MM/DD`. The retained predecessor start and final selected end bound the contiguous removal. Reject HDL DELETE, mixed instructions, ISO DAT dates, first/only split deletion, and any REST mutation.
