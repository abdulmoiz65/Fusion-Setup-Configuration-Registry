---
skill_id: "scm.order-management.pricing"
name: "Pricing Implementation Guidance"
description: "Provides SCM Order Management implementation guidance for the Pricing functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
type: "planning"
execution_mode: "hybrid"
owner_team: "SCM order management pillar team"
version: "0.5.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "pricing_scope"
  - "pricing_requirements"
  - "pricing_message_update_request"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "pricing_message_inventory"
  - "pricing_message_token_attribute_inventory"
  - "pricing_message_update_preview"
  - "pricing_message_update_result"
  - "pricing_message_token_removal_preview"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_QP_MANAGE_PRICE_ELEMENTS"
  - "ORA_QP_MANAGE_PRICING_BASES"
  - "ORA_QP_MANAGE_PRICING_PARAMETERS"
  - "ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS"
  - "CUSTOM_IMPORT_PRICE_LISTS"
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "ORA_QP_MANAGE_PRICING_LOOKUPS"
  - "ORA_QP_MANAGE_ROUNDING_RULES"
  - "ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS"
  - "CUSTOM_CUSTOMER_PRICING_DEFINITIONS"
  - "ORA_QP_MANAGE_PRICING_MESSAGES"
  - "ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Read-only pricing message and token attribute inventory calls connect to the selected Fusion environment and may refresh the private OAuth cache."
  - "An approved Data Loader operation may add or delete one existing pricing-message token association and change an existing message's text only after each operation has a validated mapping and immutable artifact."
required_privileges:
  - "Read access to Pricing Messages and Pricing Message Token Attribute Definitions for live inventory requests"
  - "Data Loader and Manage Pricing Messages privileges for a validated existing-message update or token-association add/delete load"
---

# Pricing Implementation Guidance

## Purpose

Provides SCM Order Management implementation guidance for the Pricing functional area.

## When to Use

Use this skill after Order Management scope is confirmed and the project needs Pricing setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Order Management` (`DOO_ORCHESTRATION`)
- Functional area / Setup Object: `Pricing` (`ORA_FOM_PRICING`)

## Setup Tasks

1. [Manage Price Elements](manage-price-elements.md) (`ORA_QP_MANAGE_PRICE_ELEMENTS`)
2. [Manage Pricing Bases](manage-pricing-bases.md) (`ORA_QP_MANAGE_PRICING_BASES`)
3. [Manage Pricing Parameters](manage-pricing-parameters.md) (`ORA_QP_MANAGE_PRICING_PARAMETERS`)
4. [Manage Pricing Charge Definitions](manage-pricing-charge-definitions.md) (`ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS`)
5. [Manage Pricing Profile Options](manage-pricing-profile-options.md) (`FND_MANAGE_PROFILE_OPTIONS`)
6. [Import Price Lists](import-price-lists/SKILL.md) (`CUSTOM_IMPORT_PRICE_LISTS`)
7. [Manage Pricing Lookups](manage-pricing-lookups/SKILL.md) (`ORA_QP_MANAGE_PRICING_LOOKUPS`)
8. [Manage Rounding Rules](manage-pricing-rounding-rules.md) (`ORA_QP_MANAGE_ROUNDING_RULES`)
9. [Manage Rounding Rule Assignments](manage-rounding-rule-assignments.md) (`ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS`)
10. [Manage Customer Pricing Definitions](manage-customer-pricing-definitions.md) (`CUSTOM_CUSTOMER_PRICING_DEFINITIONS`)
11. [Manage Pricing Messages](manage-pricing-messages.md) (`ORA_QP_MANAGE_PRICING_MESSAGES`)
12. [Manage Pricing Message Token Attribute Definitions](manage-pricing-message-token-attribute-definitions.md) (`ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS`)

## Implementation Notes

Use the generated flat setup-task metadata files for ordinary task-level
planning and the nested `import-price-lists` skill for its task-specific FBDI
workflow. Track token usage for any generated project artifact or skill-run
record using the manifest policy.

## Read-only Pricing Message and Token Inventory

Use this workflow when the user asks to list or inspect Pricing messages,
tokens attached to messages, or Pricing message token attribute definitions.
This workflow is **GET only**. Do not create, update, delete, import, or submit
token attributes or pricing messages as part of a fetch request. A request to
update an existing pricing message uses the separate workflow below. Token
attribute writes and pricing message creation are outside this skill. These
are three distinct data sets. Use `core.fusion-api.rest-api-client` with
the standard Fusion service and its managed token cache for every GET. Read
`core/fusion-api/rest-api-client/SKILL.md` and its
`references/fusion-rest-api.md` before calling the client. Resolve the target
environment from the selected project workflow and its configured
`restBaseUrl`; a user-provided URL on another host supplies a resource-path
example, not permission to send the configured token to that host.

| Requested data | Collection GET | Child resource | Key result fields |
| --- | --- | --- | --- |
| Pricing messages and their attached tokens | `/fscmRestApi/resources/11.13.18.05/pricingMessages` with `expand=pricingMessageTokens` | `/pricingMessages/{PricingMessageId}/child/pricingMessageTokens` | Parent `PricingMessageId`, `Name`, `PricingEntityCode`, `MessageText`; child `TokenName`, `TokenAttrDisplayName`, `UsedFlag` |
| Pricing message token attribute definitions and their details | `/fscmRestApi/resources/11.13.18.05/pricingMessageTokenAttributes` with `expand=pricingMessageTokenAttributeDetails` | `/pricingMessageTokenAttributes/{MsgTokenAttrDefnId}/child/pricingMessageTokenAttributeDetails` | Parent `MsgTokenAttrDefnId`, `Name`, `EntityTypeCode`, `ActiveFlag`; child `TokenName`, `AttrDisplayName`, `TokenDatatype`, `VoAttributeName`, `AttributeSelectedFlag`, `UsedFlag` |

From the repository root, use the core client for a collection page:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/pricingMessages \
  --method GET --query onlyData=true --query limit=500 --query offset=0 \
  --query totalResults=true --query expand=pricingMessageTokens \
  --token-cache auto

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/pricingMessageTokenAttributes \
  --method GET --query onlyData=true --query limit=500 --query offset=0 \
  --query totalResults=true --query expand=pricingMessageTokenAttributeDetails \
  --token-cache auto
```

For a requested single record, call the matching child resource using the
parent ID returned by its collection GET. Treat IDs in example URLs as
environment-specific; verify the parent in the selected environment first.

Before claiming a complete inventory, page each parent collection until
`hasMore` is `false`; require `count` to equal the number of returned `items`,
advance `offset` by `count`, and reconcile the accumulated count with
`totalResults` when Fusion returns it. Stop if `hasMore` is `true` but `count`
is zero. Confirm the expanded child field is present for every parent. If child
expansion is missing, appears truncated, or a specific parent's details are in question,
GET that parent's child collection with its own `limit` and `offset`, again
until `hasMore` is `false`. Deduplicate token names only after collecting all
rows. State whether the answer covers **tokens attached to messages** or
**token attribute details**, and report both record and distinct-name counts.
An empty setup-task CSV export does not establish that predefined messages or
token attributes are absent; use the REST inventory for read-only discovery.

Preflight the project, selected environment origin, OAuth scope/cache, expected
resource path, read privileges, output destination, and any sensitive message
text before calling Fusion. GET needs no Data Loader approval. Retain raw
responses containing customer-specific message text only in private temporary
storage unless project persistence is explicitly safe; persist only redacted
summaries or non-sensitive artifacts under `project/{project_id}` and record
token usage there. Never persist or print bearer tokens, authorization headers,
client secrets, or token-cache contents. On 401/403 use the core client's
single refresh behavior; on other failures, missing pages, inconsistent counts,
or truncated children, stop and record a diagnostic rather than report an
incomplete list as all records. No polling or mutation is part of this GET
workflow.

## Change an Existing Pricing Message and Its Token Associations

Use this workflow only when the user explicitly requests an update to an
existing Pricing message. It supports a text-only update, adding one missing
existing-token association before a text update, or deleting one existing-token
association before a text update. **Every association and text write must be
routed through `core.data-loader`; none may use
`core.fusion-api.rest-api-client`, Task REST, a browser save, or an ad hoc REST
adapter.** Read-only discovery may use the inventory GET workflow above. No
parent message or token attribute definition may be created or deleted by this
route. Do not infer permission to remove an association from a text-edit request:
require the user's explicit token-removal intent.

1. Resolve the active project, environment, and exact existing message. GET
   its current text and complete child-token collection. For an add, resolve the
   requested token attribute from the same environment and pricing entity;
   require one active definition and one selected, used detail with an exact
   token name, and prove the association is absent. For a removal, require
   exactly one attached child with the requested `TokenName`, capture its
   `TokenId`, `TokenGUID`, `PricingMessageId`, and `MsgTokenAttrId` from the live
   child response, and verify that it belongs to the resolved parent and
   pricing entity. Stop on missing keys, duplicates, conflicting identities,
   or a changed parent text. Preserve all other child associations and the
   shared token attribute definition.
2. Enter `core.data-loader` before preparing either write. Select
   `pricingMessages` as the top-level Data Loader Business Object and
   `pricingMessageTokens` as its registered child component for the token
   association. Do not resolve or submit `pricingMessageTokens` as a standalone
   top-level Business Object: its registration is under `pricingMessages`, and
   both components use `pricingMessages.dat`. Check live parent and child
   metadata, user/surrogate keys, requested operation support, and UCM DAT
   template sections. For an add, require a child `POST` mapping that creates
   only the missing association. For a removal, require live child delete
   support and a child-only `DELETE|pricingMessageTokens` mapping that uniquely
   identifies the existing association by its live key and parent, with
   `RestAction=DELETE` when that field is in the selected source schema. Never
   issue `DELETE|pricingMessages`, delete the token attribute definition, or
   use a child `MERGE` as a substitute for deletion. Require a separate parent
   `PATCH` mapping that updates only that message's `MessageText`. A child-only
   loader source omits a parent data row, and its
   `METADATA|pricingMessageTokens` section must match the downloaded template,
   unless a separately validated Data Loader adapter explicitly supports the
   missing-template case. Child registration or REST method support alone does
   not prove that a Data Loader source is accepted.
   If either mapping or operation is absent, ambiguous, or unsafe, record a
   `catalog_or_metadata_mismatch` diagnostic and stop before any load.
3. Only when every required loader path is proven, prepare separate source files
   and immutable upload artifact(s) through `core.data-loader`. Validate the
   exact target keys, requested text, expected child presence or absence,
   source syntax, privileges, and no-create/no-other-row behavior. For removal,
   verify that the resulting text contains no reference to the removed token.
   Require the selected task's registry plan to be ready and every applicable
   rule resource to pass for each final artifact. Stop if Task Hook reports
   skipped validation or unavailable task guidance.
   Run Data Loader's task validation and preview on each final artifact. Follow
   its own approval workflow for each exact artifact; an approval of an earlier
   add or text update does not approve a new delete. Do not add a separate pillar
   approval or treat an earlier direct-REST preview as loader approval.
4. After Data Loader approval, submit the child add or delete first. A successful
   initiation is terminal for that request: return Data Loader's report and
   wait for a separate user status request before checking completion. Confirm
   the child load succeeded with zero failures and read back the complete child
   collection. For an add, require exactly one matching attached token; for a
   removal, require zero matching tokens and unchanged other associations.
   Re-read the parent before the second load and stop if its text or identity
   changed since preflight. Prepare and validate the parent stage separately
   against that confirmed child state, then obtain its own Data Loader approval
   and submit the parent `PATCH` artifact. A text-only request submits just the
   parent artifact.
   Follow Data Loader's status, timeout, retry, and reporting contract. On
   partial success or uncertain status, stop, preserve returned data-set and
   request identifiers, and do not auto-retry, compensate, or continue to the
   second load.
5. On a later user status request after the parent initiation, confirm its load
   completed and read back the parent and complete child collection through
   the declared read-only route. Verify the exact text, expected token presence
   or absence, and unchanged unrelated fields. Persist the skill run and
   redacted diagnostic under `project/{project_id}` with environment, stage,
   failure class, artifact references, and Data Loader IDs. Do not persist
   customer-sensitive message text, credentials, headers, or token-cache
   contents.

Recheck the selected environment's current template for every new load. An old
template or child registration alone never authorizes an add or delete.
A read-only "get", "list", "show", or "fetch" request never authorizes a load.

## Mandatory Execution Routing

Apply this routing rule to every Pricing setup task listed above.

1. Treat the Pricing pillar and its flat task metadata as business guidance and task-routing inputs only. Do not invoke Fusion import endpoints, loader jobs, or mutating REST calls directly from this pillar skill.
2. For task-routed imports, resolve the task context and run the applicable Run Book task validation, immutable preview, and approval gates before live execution.
3. Route every FSM, FBDI, HDL, or other Fusion data import through `core.data-loader`. Use a task-specific import adapter only after Data Loader has authorized the validated source and execution.
4. Route direct Fusion REST `POST`, `PUT`, `PATCH`, and `DELETE` calls through `core.fusion-api.rest-api-client` when a task permits them. Imports use `core.data-loader` and its declared clients/adapters and approval gates. The Pricing message update above permits no direct REST write.
5. A read-only Fusion REST `GET` may use `core.fusion-api.rest-api-client` without Data Loader, while still applying task-specific validation and redaction rules.
6. Do not retry a live import or REST write after an uncertain, timed-out, or failed result unless the user explicitly approves the retry and the applicable core workflow permits it.
7. For `ORA_QP_MANAGE_PRICING_MESSAGES`, route an existing-message text update and an explicitly requested add or delete of one existing-token association through `core.data-loader` only, subject to proven operation-specific mappings and its approval gates. Never use direct REST writes for these changes or create/delete a parent message or token attribute definition. For `ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS`, this skill permits GET only; do not create or update definitions or details. These task-specific limits take precedence over generic import and REST method availability.
