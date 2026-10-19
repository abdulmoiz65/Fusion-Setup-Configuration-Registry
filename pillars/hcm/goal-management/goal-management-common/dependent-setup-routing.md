# Goal Management Dependent Setup Routing

## Boundary

Goal Management may read a shared or cross-product dependency when the read is
required to validate a Goal Management object. Goal Management does not own a
create, update, delete, deployment, import, or setup-maintenance operation for
that dependency.

Classify every dependency request as exactly one of these operations:

| Classification | Owner and behavior |
| --- | --- |
| `dependency_read` | The Goal Management task may invoke the owning provider's read interface and use the result only for validation or identity resolution. |
| `dependency_mutation` | Create an independent child route to the owning provider. Preserve that provider's preview, approval, bulk, execution, and verification contract. |
| `goal_management_association` | The applicable Goal Management object task may associate an already resolved dependency with its own object when current metadata supports the association. |

A Goal Management task must never construct a dependency mutation payload,
register the dependency's mutation API as Goal Management-owned, reuse the
Goal Management object approval for the dependency, or replace an unavailable
provider with browser entry, direct REST, or a local loader route.

## Owning routes

| Dependency | Read route | Mutation owner |
| --- | --- | --- |
| Profile options and configured profile values | `core.fusion-api.apps-common.profile-options` | `core.fusion-api.apps-common.profile-options`; configured-value maintenance uses `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES` |
| Common, standard, generic, and set-enabled lookups | `core.fusion-api.apps-common.lookups` | `core.fusion-api.apps-common.lookups` |
| Value sets and supported child values | `core.fusion-api.apps-common.value-sets` | `core.fusion-api.apps-common.value-sets` |
| Descriptive Flexfields | `core.fusion-api.apps-common.descriptive-flexfields` | `core.fusion-api.apps-common.descriptive-flexfields` |
| Extensible Flexfields | `core.fusion-api.apps-common.extensible-flexfields` | `core.fusion-api.apps-common.extensible-flexfields` |
| Key Flexfields | `core.fusion-api.apps-common.key-flexfields` | `core.fusion-api.apps-common.key-flexfields` |
| Reference Data Sets | Owning Common setup read/export workflow | Owning Common task-level setup import workflow; return `PROVIDER_SKILL_UNAVAILABLE` when no executable provider exists |
| Currencies | Owning Common read workflow | Owning Common or `shared.common.manual-tasks` workflow; preserve seed-data safeguards |
| Approval Options | Exact-process read through `hcm.hcm-tool.approval-options` | `hcm.hcm-tool.approval-options` |
| Approval Rules | Owning read workflow | `hcm.hcm-tool.approval-rules` |
| Offering, functional-area, and feature opt-ins | Shared FSM opt-in read | `shared.implementation-planning.fsm-set-optin` and its target-specific child skill |
| Eligibility Profiles | Complete paginated `eligibilityProfilesLOV` read and authoritative criteria verification | Canonical `BEN_MANAGE_ELIGIBILITY_PROFILES` provider |
| Business units, legal employers, departments, jobs, and workers | Owning GHR read provider | Owning GHR setup skill |
| Performance Document Types | Owning Performance Management read provider | Owning Performance Management skill |
| Attachment entities, categories, and formats | `core.fusion-api.apps-common.attachments` | `core.fusion-api.apps-common.attachments` |
| Trees and hierarchy setup | `core.fusion-api.apps-common.trees` | The owning provider; the current advisory provider has no approved live mutation route |
| ESS scheduling | Declared Core ESS read/status provider | `core.fusion-api.ess-job-submitter` |

Approval Options and FSM feature choices are not automatic Goal Management
dependencies. Resolve them only when the source explicitly requests them or an
owning Goal Management rule declares them necessary.

## Association exceptions

The following are Goal Management mutations only after the referenced object
has been resolved through its owner:

- associate an existing Eligibility Profile with a Goal Plan;
- associate an existing Performance Document Type with a Goal Plan;
- associate an existing Library Goal with a Goal Plan;
- add an existing Target Outcome content item to a Library Goal;
- apply an existing Business Unit or other supported availability scope to a
  Library Goal; and
- add Goal or Goal Plan attachment business data when current Goal Management
  metadata advertises that child operation.

These operations do not authorize maintenance of the referenced dependency.

## Single and bulk maintenance

For one dependency change, use the owning provider's exact-current-state
preview, approval, one execution attempt, and fresh verification. For multiple
dependency changes, use only the owner's declared bulk or setup-import route.
Do not simulate bulk maintenance by looping over single-record mutations. If
the owner has no supported bulk route, return an unsupported or
`PROVIDER_SKILL_UNAVAILABLE` result with resume context.

## Registration ownership

Do not include dependency mutation endpoints in the Goal Management Data
Loader/APEX REST registration inventory. Only Goal Management-owned object and
association mutations belong to that inventory. Each dependency owner is
responsible for registering its own state-changing APIs.
