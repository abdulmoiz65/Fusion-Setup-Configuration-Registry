# Learning Common dependencies and provider handoffs

Read this reference when planning or regenerating Learning Management Common.
It identifies reusable providers and conditional prerequisites; it is not a
tenant baseline, a new executor, or an executable cross-task sequence.

## Catalog scope

Reconciled against the local effective catalog on 2026-09-23:
`ORA_LEARNING_MANAGEMENT` / `ORA_LEARNING_MANAGEMENT_COMMON` has ten tasks.
Use that exact pair for task matching; a task name alone is insufficient.
The [effective hierarchy](../../../../../knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json)
owns membership, while the [task catalog](../../../../../knowledge/setup-task-catalog/effective/setupTasksAll.json)
owns task identity and support flags. This is not a fresh taxonomy-site or pod read.

## Authoring reference only

[Global Human Resources Common](../../../global-human-resources/global-human-resources-common/SKILL.md)
is a structural example, not a Learning dependency. Its functional-area
manifest, task index, task-level guidance, shared/core service routing and
workspace output declarations provide the authoring pattern. Use Learning's
own catalog identities, supported operations and business rules in that pattern.
Do not route Learning implementation work to GHR or require GHR setup based on
this reference.

Learning retains its ten task files and shared `ora-resource` rules. Structural
reuse does not copy GHR's task membership or alter Learning's execution contracts.

## Shared implementation dependencies

| Dependency | Use only when needed | Required result |
| --- | --- | --- |
| [Offering Task Map Builder](../../../../../shared/implementation-planning/offering-task-map-builder/SKILL.md) and [Task Dependency Resolver](../../../../../shared/implementation-planning/task-dependency-resolver/SKILL.md) | Building an implementation sequence after scope classification | Resolved offering/functional-area/task identities, supported dependency evidence and a persisted sequence with diagnostics. |
| [Functional-area export](../../../../../shared/setup-export/functional-area-export/SKILL.md) or [task export](../../../../../shared/setup-export/task-level-export/SKILL.md) | An eligible setup-data baseline/export is explicitly selected | Verified catalog support and an attributable artifact; a remote export is not a side-effect-free GET. |
| [Setup Data Validator](../../../../../shared/validation/setup-data-validator/SKILL.md) and [Reference Data Validator](../../../../../shared/validation/reference-data-validator/SKILL.md) | Reviewing supported setup artifacts and their references | Validated source shape and resolved references, not permission to import. |
| [Apps Common](../../../../../core/fusion-api/apps-common/SKILL.md) | Profiles, lookups, value sets or DFFs | Select exactly the owning nested provider below. A known nested provider may be invoked directly under the same contract. |
| [Data Loader](../../../../../core/data-loader/SKILL.md) | The selected provider explicitly routes an import or registered-object load | Validated immutable artifact, task checks and its own single approval lifecycle. Do not choose this route merely from a catalog flag. |
| [Role Access Check](../../../../../core/diagnostics/role-access-check/SKILL.md) and [Security Role Guidance](../../../../../shared/best-practices/security-role-guidance/SKILL.md) | Verifying operation access or designing security | Operation-specific evidence; a listed dependency or successful GET does not prove write privilege. |
| Project state, artifact registry and artifact version services declared in the manifest | Durable implementation work | Sanitized, versioned inventory/proposal/results, a run record and token-usage record in the selected project. Developer regeneration does not create a tenant project. |

These are workflow dependencies, not a requirement to run every provider for
every request. Select only the applicable operation and read its full contract.

## Task-to-provider dependency map

| Learning task code | Owning provider or gap | Prerequisite and evidence boundary |
| --- | --- | --- |
| `FND_MANAGE_PROFILE_OPTIONS` | `core.fusion-api.apps-common.profile-options` | Resolve the delivered definition, actual name, supported levels and editability before using it. Definition creation is not a supported value update. |
| `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES` | `core.fusion-api.apps-common.profile-options` | Resolve the definition and the exact configured level/target child before deciding create/update or unchanged. An effective session value is not a configured Site baseline. |
| `FND_MANAGE_COMMON_LOOKUPS` | `core.fusion-api.apps-common.lookups` | Resolve the Common category, exact type/code and seeded/editability/effective-date restrictions. Do not switch category to bypass restrictions. |
| `FND_MANAGE_VALUE_SETS` | `core.fusion-api.apps-common.value-sets` | Resolve the definition, validation type and consuming segment. The provider reads definitions and manages supported child values; root-definition creation requires a separately supported route. |
| `FND_MANAGE_DESCRIPTIVE_FLEXFIELDS` | `core.fusion-api.apps-common.descriptive-flexfields` | Use [DFF verification](dff-verification.md) for approved shared data-export preparation and local provider-evidence assessment. Compatible value sets precede dependent segments; Data Loader FSM import and core deployment remain separate approved actions. |
| `ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS` | Search provider contract unresolved | Resolve feature/persona requirements and current configuration through a declared reader. No registered business object is supplied. |
| `ORA_FND_SUGGESTION_GROUPS` | Search provider contract unresolved | Resolve the exact suggestion group and current definition through a declared reader. This is not index configuration or Search Views. |
| `ORA_FND_MANAGE_INDEX_CONFIGURATION` | Search provider contract unresolved | For requested DFF filters, verify deployment before index publication, applicable ingestion and Search Views acceptance. Blank REST business-object metadata grants no loader route. |
| `FND_MANAGE_AUDIT_POLICIES` | `core.fusion-api.audit-setup`, subject to the incomplete Common evidence binding | Combine supported provider evidence with required implementer UI evidence for the overall switch/current field selections. Confirm exact object/field scope before changes. |
| `ORA_GMS_MANAGE_AUDIT_TYPES` | Catalog-owner clarification required | Preserve the catalog task but resolve its Grants-versus-Learning applicability before any operation; it is not an alias for Audit Policies. |

The selected nested provider is authoritative for supported operations. Preserve
the current DFF provider's explicit FSM workflow; do not infer value-set root
CRUD from generic task wording in a structural example.
Existing Learning guidance, named resolver contracts and approval gates remain
in force. See [provider selection](workflow.md#select-an-existing-provider).

## Profile-option consumer handoffs

The [taxonomy consumer map](taxonomy-and-sources.md#all-common-mappings) records
the Application Profile Option Foundation dependency for Learning Configurations,
Learning Catalog, Learning Assignment, Recommendations and External Providers.
Use `core.fusion-api.apps-common.profile-options` through the existing
[profile definitions](../manage-profile-options.md) and
[administrator profile values](../manage-administrator-profile-values.md) guidance.

The consuming task supplies the applicable option codes, business triggers,
supported values and source evidence. Read the current configured/effective
values required by that task; retain satisfied prerequisites and propose only
applicable differences for approval. The foundation relationship does not require
enabling every Learning profile option or changing a value on every request.

[Learning Catalog](../../learning-catalog/SKILL.md#execution-contract) already
declares this provider and task-specific readiness checks. Keep its CAP child
contract unchanged; Catalog-level dependencies are not blanket CAP prerequisites.
Learning Assignment, Recommendations and External Providers currently have
catalog scope but no dedicated consuming skills in this package. Retain their
profile-option dependency in the [setup inventory](setup-inventory.md), with
the consuming area, known requirement or unresolved option mapping, evidence,
owner and next action. Common may assess supported profile settings through
its existing workflow; a satisfied setting does not establish the missing
consumer's execution readiness.

## Conditional business prerequisites and handoffs

- **Value sets, DFFs and search:** create no custom fields without an agreed
  requirement. Follow the dependency checks in [DFF guidance](../manage-descriptive-flexfields.md#configuration-deployment-and-acceptance)
  and [search guidance](../manage-search-indexes.md#learning-index-readiness).
  Saved settings, deployment, ingestion and persona acceptance are distinct evidence.
- **Security and catalog administration:** person scope belongs to
  [HCM Security Profile](../../../hcm-security/hcm-security-profile/SKILL.md) and
  [HCM Data Role](../../../hcm-security/hcm-data-role/SKILL.md); catalog ownership
  belongs to [Catalog Administration Profiles](../../learning-catalog/manage-catalog-administration-profiles/SKILL.md).
  These are conditional handoffs, not universal prerequisites or automatic grants.
- **Background processes, Redwood extensions and data migration:** use the
  [non-FSM foundation handoffs](setup-capability-handoffs.md#non-fsm-foundation-handoffs).
  A declared ESS service still needs an exact supported job/parameters/schedule
  and approval. A profile flag does not configure an integration or publish an extension.
- **Learning defaults and Talent prerequisites/outcomes:** retain the C7/C8
  [capability handoffs](setup-capability-handoffs.md); do not manufacture missing
  Learning Configurations or Talent execution contracts.

## Sequence and readiness limits

The numbered task index is catalog presentation order, not a verified execution
sequence. During implementation, let Task Dependency Resolver establish the
sequence, then consume it in the task map and Run Book. If FSM discovery fails,
report the failure and obtain explicit acceptance before using its documented
fallback. This repository regeneration makes no FSM or tenant call.

The checked-in [HCM dependency graph](../../../../../knowledge/dependency-graphs/hcm-dependency-graph.json)
contains legacy `hcm.learning.*` nodes, but no exact
`hcm.learning-management.learning-management-common` node. Do not translate
legacy skill names or endpoint labels into current task prerequisites by guesswork.
Record unmatched graph enrichment; missing graph coverage does not by itself
block supported catalog/FSM sequencing.

The current [rule registry](../ora-resource/ora_rule_registry.json) has five
complete validation contracts (profile definitions, profile values, Common
lookups, value sets and bounded DFF export/evidence review) and five incomplete
contracts (the three search tasks and both audit tasks). DFF runtime schema and
evidence must still be verified; missing seeded definitions cannot be created
by this contract. Re-run the planner for the selected task before
execution. This is contract readiness, not tenant readiness or write approval;
regeneration must not turn a `TBD` into a satisfied prerequisite.
