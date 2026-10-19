# Development Library Goal Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select one operation and variant | No implicit variant or combined lifecycle stages |
| 2 | Resolve identity, references, and usage | Every code and target is exact |
| 3 | Preserve collections and inactive-first behavior | Payload diff is safe |
| 4 | Bind approval | Final environment, target, variant, state, payload, and fingerprint are fixed |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| GL.VARIANT.CONTRACT | Every operation | Blocker | goal_variant_contract_lookup | Current environment contradicts or omits public fields/operation for the requested variant | Capture mismatch evidence and resume after contract resolution | Yes |
| GL.VARIANT.FIELD | Create or update | Blocker | goal_variant_contract_lookup | A request supplies a non-development field or omits `DevCategoryCode` when current metadata marks it mandatory | Omit an optional `DevCategoryCode`; otherwise map the supplied development code | Yes |
| GL.TYPE.MATCH | Create or update | Blocker | goal_variant_contract_lookup | `TypeCode` is not `DEVELOPMENT` | Reject the request before preview | Yes |
| GL.CREATE.KEY_FIELDS | Create | Blocker | goal_variant_contract_lookup | The canonical payload omits or nulls GoalName, TypeCode, StatusCode, or Visible; sends read-only AvailableTo; or describes a default absent from JSON | Rebuild through the deterministic payload helper and materialize the defaults before preview | Yes |
| GL.AUDIENCE | Create | Blocker | library_goal_availability_lookup | Source audience is unresolved, Visible is absent/nonwritable, AvailableTo is sent, or a Business Unit restriction lacks one exact BusinessUnitId | Resolve role audience and organizational scope independently; send Visible and scope ID only | Yes |
| GL.CREATE.VERIFIED | After create | Blocker | library_goal_lookup | Fresh returned GoalName, TypeCode, StatusCode, Visible, AvailableTo meaning, or an approved scope field is null or mismatched | Return INVALID_CREATED_STATE, retain the created identity, and stop without replacement or Run Book completion | Yes |
| GL.EXISTING.INVALID | Create duplicate control | Blocker | library_goal_lookup | An exact existing name+variant row has null StatusCode or Visible | Return INVALID_EXISTING_LIBRARY_GOAL_STATE and require an explicit repair or replacement decision | Yes |
| GL.MEASURE.CONTRACT | Create or update with a measurement | Blocker | goal_variant_contract_lookup | Quantitative fields are invalid, or `ORA_NONE` does not map to qualitative measurement without target values | Correct the measurement according to the resolved variant metadata | Yes |
| GL.TASK.OUTCOME.INTEGRITY | Create or update with tasks/outcomes | Blocker | library_goal_lookup | Task dates are outside the parent envelope, the child is not owned by this goal, or a target outcome duplicates `TypeItemId` | Correct the child collection before preview | Yes |
| GL.EXTERNAL_ID | Create or update | Blocker | library_goal_lookup | Automated create lacks a writable ID and duplicate-risk controls, or update changes an existing ID | Supply immutable ID when supported or use exact duplicate controls | Yes |
| GL.CHILD.PRESERVE | Update | Blocker | library_goal_lookup | Omitted collections would be dropped | Merge with fresh complete state | Yes |
| GL.DELETE.USAGE | Delete | Blocker | library_goal_usage_lookup | References are nonzero or unknown | Inactivate instead | Yes |
| GL.ACTIVATION.SEPARATE | Create or update | Blocker |  | Activation is chained | Finish inactive and request activation separately | Yes |
| GL.APPROVAL.FRESH | Any mutation | Blocker |  | Fresh state differs from approved fingerprint | Rebuild preview and approval | Yes |
| GL.APPROVAL.TRANSPORT | Multiple updates under one approval | Blocker | goal_variant_contract_lookup | Approval wording is used to infer ADF batch, or any operation lacks a current advertised update contract | Keep one approval group but build ordered item PATCH requests when PATCH is advertised; use batch only when current metadata explicitly enables it | Yes |
| GL.RUNBOOK.SEQUENCE | Run Book task execution | Blocker |  | The task lacks current parent execution control or an earlier applicable task is incomplete | Return to the parent resolver and preview the earliest incomplete task | No |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| GL.VARIANT.CONTRACT | goal_variant_contract_lookup | Every request | Resource, discriminator, operations, fields | ora_reference_lookups.md |
| GL.CHILD.PRESERVE | library_goal_lookup | Update | Complete parent and child state | ora_reference_lookups.md |
| GL.DELETE.USAGE | library_goal_usage_lookup | Delete | Usage count and references | ora_reference_lookups.md |
| GL.AUDIENCE | library_goal_availability_lookup | Create | Visible code, expected Available To meaning, and exact BusinessUnitId when scoped | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.DESIGN | decision | 60 | design_enforcement | passed->GOAL_LIBRARY.REST_DESCRIBE;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.DEFAULTS | stop | A mutation is ready for design checks |


---

# Development Library Goal Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Packaged | Catalog description and approved Development Library Goal functional contract | Consultant planning |
| Runtime | Current describe/OpenAPI, reference values, and usage reads | Variant and operation readiness |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Shared task ownership | Strong | This task serves only Development Library Goals in this Goal Management functional area | Product-variant split implemented in Goal Management |
| Development contract | Strong | Public `libraryGoals` uses `DevCategoryCode`; current metadata confirms operation and updateability | Blanket development-write prohibition or inferred alternate resource |
| Inactive-first | Strong | Create/update can complete without activation | Chained activation |
| Collections | Strong | Preserve omitted measures, tasks, outcomes, translations, and DFF | Destructive replacement by omission |
| Deletion | Strong | Prefer inactivation when references are nonzero or unknown | Unguarded delete |

## Output Rules

| Situation | What Happens |
|---|---|
| Current metadata omits or contradicts development behavior | Return metadata-mismatch plan, missing evidence, and resume context |
| Current metadata verifies development behavior | Use `libraryGoals` with the explicit development contract and a fresh preview |
