# Manage Job Families Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Job Families.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Delete mode | effective-split or zap | Block | State whether to delete one future effective split or purge the complete logical Job Family | delete when the resolved Job Family has multiple date-effective records |  |
| Existing job-family selector | Exact JobFamilyId, JobFamilyCode, or JobFamilyName | Block | Provide one exact business selector | get, edit, or delete | find_manage_job_families |
| Create identity | JobFamilyCode and JobFamilyName | Block | Provide both values | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | Every mutation |  |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |
| Delete identity | Exact existing job family; for effective-split delete, selected EffectiveStartDate | Block | Resolve the target and requested split | delete | find_manage_job_families |
| Translation identity | Language, translated JobFamilyName, and a date aligned with the base row | Block | Provide the translation values | A translation is requested |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing target does not resolve to exactly one effective job family | Missing | Request one exact ID, code, or name | find_manage_job_families |
| A create code or name matches an existing job family | Invalid | Stop the duplicate create | find_manage_job_families |
| A supplied Job Subfamily is unresolved, disabled, or ineffective | Invalid | Correct the subfamily value | resolve_job_family_subfamily |
| The resulting association count exceeds a configured numeric limit | Invalid | Reduce the requested associations | resolve_job_family_association_limit |
| Delete mode is absent or ambiguous for a multi-record history | Invalid | Choose effective-split or zap; a resolved single date-effective record is always a zap |  |
| A job references the target job family, the query is incomplete, or the Job Family filter is unsupported | Invalid | Stop the delete; the family must be unreferenced | find_job_references_for_job_family |
| The selected effective-split row is missing, ambiguous, first, nonfinal, nonfuture, or lacks an immediately preceding row | Invalid | Select one final future split with its retained predecessor | read_job_family_delete_history |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Normalize an unambiguous date to the loader date format; reject an ambiguous or invalid date | A date is supplied |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the JobFamily row and every included JobSubFamilyAssociation row | Create or edit |  |
| Effective range | Reject an EffectiveEndDate earlier than EffectiveStartDate | Both dates are supplied |  |
| Name uniqueness | Reject a JobFamilyName already used in the enterprise | create or name change | find_manage_job_families |
| Code and name length | Reject JobFamilyCode or JobFamilyName longer than 240 characters | Either value is supplied |  |
| Active status | Accept only `A` or `I` | Parent or JobSubFamilyAssociation ActiveStatus is supplied |  |
| Translation alignment | Require translation effective dates to match a base-language effective row | A translation is requested |  |
| Job Family EFF | Reject EFF content because Job Family has no EFF object | EFF content is supplied |  |
| Supported fields | Reject response-only IDs, audit fields, links, and fields absent from the registered Job Family loader contract | A mutation value is supplied |  |
| Mutation source scope | Keep the JobFamily worksheet, map entry, and base row for every mutation; include JobSubFamilyAssociation only when explicitly modified. A delete artifact contains only the task-approved JobFamily row. | create, edit, or delete |  |
| Association delta | Omit unchanged JobSubFamilyAssociation rows | edit | read_job_family_associations |
| Zap delete | Author a native JobFamily.dat with one METADATA&#124;JobFamily row and one DELETE&#124;JobFamily row using the freshly resolved supported business key, then require current live Data Loader validation to accept that exact source. Do not add RestAction to the XLSX. Do not author MERGE, child rows, or SET PURGE_FUTURE_CHANGES Y for that logical Job Family. | zap delete | find_manage_job_families |
| Future effective-split delete | Author SET PURGE_FUTURE_CHANGES Y, then one METADATA&#124;JobFamily row and one MERGE&#124;JobFamily row. Set EffectiveStartDate to the immediately preceding row's start and EffectiveEndDate to the selected final future row's end; include only the resolved Job Family key and these boundaries. | effective-split delete | read_job_family_delete_history |
| Verification boundary | Do not treat source generation, transport, or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JF.VALIDATE | decision | 1 | validate_input | valid->JF.READ;missing->JF.ERROR;invalid->JF.ERROR;unsupported->JF.ERROR | none | stop | Every Manage Job Families request |
