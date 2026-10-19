# Development Library Goal Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 0 | Parent Run Book execution control | Match the approved plan fingerprint and prove this is the earliest incomplete applicable task |
| 1 | Variant contract | Start from the shared public `libraryGoals` resource and verify development fields in current metadata |
| 2 | Exact Library Goal identity | Search/diff for idempotency or resolve one existing target |
| 3 | Code-backed references | Resolve goal type, outcomes, profile data, audience, and restrictions when used |
| 4 | Usage evidence | Prove no references before delete |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GL.RUNBOOK_CONTROL | Parent Run Book execution control | Yes | Any Run Book task execution | Validate | `hcm.goal-management` controlled next-task resolver | resolve_controlled_next_task | Prevents direct entry into a later task | Complete or mark every earlier task Not Applicable and show the next-task preview | Approved plan fingerprint, exact task identity, sequence, execution-control fingerprint |
| GL.VARIANT | Development Library Goal contract | Yes | Every request | Verify | Public `libraryGoals` contract plus current describe/OpenAPI | goal_variant_contract_lookup | Prevents cross-variant payloads | Use the development variant; report an environment mismatch when fields/operation differ | Resource, `DevCategoryCode`, `TypeCode`, children, lifecycle |
| GL.IDENTITY | Library Goal identity | Conditional | Existing operation or create idempotency | Lookup | Current Library Goal read route | library_goal_lookup | Prevents duplicates and ambiguous updates | Supply immutable external ID where possible | ID, external ID, variant, state, references |
| GL.OUTCOMES | Target outcomes and profile data | Conditional | Outcome/profile values are used | Lookup | Owning setup/reference route | target_outcome_lookup | Prevents invented codes | Resolve exact active values outside this task when necessary | Outcome/profile identifiers and labels |
| GL.USAGE | Downstream references | Conditional | Delete | Verify | Current exposed development consumers and any cross-product consumers reported by metadata | library_goal_usage_lookup | Protects referenced templates | Prefer inactivation when usage is nonzero or unknown | Usage count and safe references |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Variant, identity, references, and usage satisfy the operation | Lookup yes; create only after approval |
| Metadata validation | Current environment metadata contradicts or omits the public variant/operation contract | Lookup/read-only planning only |
| Blocked | Ambiguous identity, unresolved codes, unsafe usage, or absent contract | Lookup only |

## HDL DAT Dependency Readiness

Before a Development Library Goal HDL package can be previewed, obtain
structured, timestamped target-tenant evidence for the Content Item template,
its `GOAL`/`GOAL_MEASUREMENTS` mapping, development discriminator, mandatory
fields, supplied code values, relationships, and supplied translation
languages. `ContentItem.dat` is required; `ContentItemTranslation.dat` and
`ContentItemRelationship.dat` are optional as applicable. Do not combine the
archive with Performance Library Goal rows. Missing metadata, mandatory data,
relationship, or a reference is a non-waivable blocker for `core.data-loader`.
Resolve environment, timestamps, operation evidence, template mandatory fields,
and safe defaults internally. For translations, also obtain the current
translation template, base language, enabled languages, and an exact package or
target parent identity. The consultant does not provide an audit manifest.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.DEPENDENCIES | step | 30 | resolve_dependency | ready->GOAL_LIBRARY.LOOKUPS;missing->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | A Development Library Goal mutation is requested |
