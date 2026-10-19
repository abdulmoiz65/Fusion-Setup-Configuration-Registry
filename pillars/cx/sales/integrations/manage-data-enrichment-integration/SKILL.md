---
skill_id: "cx.sales.integrations.manage-data-enrichment-integration"
name: "Manage Data Enrichment Integration Setup Task Guidance"
description: "Guides setup users through Manage Data Enrichment Integration and performs a qualified, read-only DaaS Smart Data configuration-status check."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Integrations"
functional_area_code: "ORA_ZCA_INTEGRATIONS"
task_code: "ORA_MANAGE_DATA_ENRICHMENT_INTEGRATION"
task_name: "Manage Data Enrichment Integration"
parent_skill_id: "cx.sales.integrations"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.1.0"
inputs:
  - "operation"
  - "configuration_scope"
  - "fusion_environment_context"
  - "project_id"
outputs:
  - "configuration_guidance"
  - "configuration_checklist"
  - "smart_data_status_result"
  - "validation_checkpoints"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.sales.integrations"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/integrations/manage-data-enrichment-integration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/integrations/manage-data-enrichment-integration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May read DaaS Smart Data configuration through the Fusion CRM REST API when the user requests a status check."
  - "May refresh the local gitignored OAuth token cache through core.fusion-api.rest-api-client."
  - "May persist redacted guidance, status, diagnostic, run, and token-usage artifacts in the selected project workspace."
required_privileges:
  - "Fusion setup access for the Manage Data Enrichment Integration task when following configuration guidance"
  - "DATASERVICE_CLIENT_API_APPID role for the DaaS integration user"
  - "Fusion privileges appropriate to read the daaSSmartData CRM REST resource"
---

# Manage Data Enrichment Integration

## Purpose

Guide a setup user through Oracle Account and Contact Enrichment integration configuration and, when requested, read the visible Smart Data configuration from Fusion without changing it.

## Setup Task Contract

- Task code: `ORA_MANAGE_DATA_ENRICHMENT_INTEGRATION`
- Offering: `Sales`
- Functional area: `Integrations`
- Export/import supported: `N`
- CSV export/import supported: `N`
- REST scope in this skill: read-only status lookup only

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Data Enrichment Integration` under `Integrations`.

The catalog-generated `dataloader_import_mode: REST` value does not authorize a Data Loader or REST write. Do not generate a Data Loader workbook, call `core.data-loader`, or use POST, PATCH, PUT, or DELETE for this task.

## Supported Operations

Normalize the request to exactly one operation:

- `configure`: return the current source-aligned manual configuration procedure and a review checklist. Do not navigate the UI or enter credentials on the user's behalf unless a separately selected workflow explicitly authorizes that interaction.
- `check_status`: execute the read-only lookup in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md) through `core.fusion-api.rest-api-client` and return a qualified status result.

If the operation is unclear, ask whether the user wants configuration guidance or a read-only status check.

## Configuration Guidance

Use the current Oracle Account and Contact Enrichment documentation as the product source. Do not derive provider, credential, role, endpoint, or grant-type behavior from memory.

1. Confirm that the customer has an active Oracle Account or Contact Enrichment subscription and an activated data-service instance.
2. Confirm that the DaaS integration user has the `DATASERVICE_CLIENT_API_APPID` role.
3. In Setup and Maintenance, open Offering `Sales`, Functional Area `Integrations`, Task `Manage Data Enrichment Integration`.
4. Enable DaaS for the requested enrichment scope. Enable Smart Data only when it is part of the approved design.
5. Select OAuth Authentication. Basic authentication is deprecated or unsupported in later releases and must not be recommended for a new configuration.
6. Configure the confidential application with the grant types required by the current Oracle guide for the customer's service generation. Current Oracle sources consistently identify Resource Owner, Client Credentials, and Refresh Token; some current CDM guidance also identifies Authorization Code. Surface that source difference and verify the applicable guide instead of silently adding or removing a grant.
7. Enter the data-service URL after removing the trailing `/data/ui`. Do not change the scheme, hostname, region, or identity-domain portion.
8. Enter the client ID and client secret only in the Fusion setup page. Never request, display, log, or persist either value.
9. Save and close, then use `check_status` if the user wants the Smart Data configuration visibility checked.

For batch enrichment, identify `Manage Administrator Profile Values` and the currently documented `DAAS_PRODUCTION_MODE` requirement as a separate dependent setup step. Do not imply that the Smart Data REST lookup verifies that profile option or complete batch-enrichment readiness.

## Status Check

Read [ora_input_validation.md](ora-resource/ora_input_validation.md), [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md), [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md), [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md), and [ora_error_handling.md](ora-resource/ora_error_handling.md), then use the compiled task plan.

The lookup uses:

```text
GET /crmRestApi/resources/11.13.18.05/daaSSmartData
```

Return these sanitized fields:

- `api_reachable`
- `configuration_record_count`
- `account_smart_data_enabled_raw`
- `account_suggestion_endpoint_configured`
- `address_suggestion_endpoint_configured`
- `configuration_visibility`
- `status_limitations`

Return the enablement value exactly as Fusion provides it. Oracle documents `AccountSmartDataEnabled` as an enablement indicator but does not document its complete value domain on the GET operation page, so do not invent Boolean normalization.

A successful GET proves only that the authenticated user can read the visible `daaSSmartData` representation. It does not by itself prove that credentials are valid against the external data service, enrichment jobs will succeed, batch enrichment is ready, or the end-to-end integration is healthy.

## Security and Persistence

- Never accept or persist DaaS passwords, client secrets, OAuth tokens, Authorization headers, or token-cache contents.
- Reduce returned endpoint fields to present/not-present indicators in persisted artifacts unless the user explicitly needs the non-secret URL for troubleshooting.
- If `project_id` is supplied, persist redacted configuration guidance and status evidence under the declared workspace output paths and append the skill-run and token-usage records.
- Without `project_id`, return the result in-session and do not create a project workspace implicitly.

## Sources

- Oracle Help Center, *Integrate with Oracle Sales or Fusion Service*: `https://docs.oracle.com/en/cloud/saas/social-data-insight-cloud/csdsr/integrate-with-oracle-sales-or-b2b-service.html`
- Oracle Help Center, *Configure Oracle Account and Contact Enrichment by Dun & Bradstreet (D&B)*: `https://docs.oracle.com/en/cloud/saas/customer-data-management/fagcd/configure-oracle-account-and-contact-enrichment-by-dun.html`
- Oracle REST API, *Get all smart data*: `https://docs.oracle.com/en/cloud/saas/sales/faaps/op-daassmartdata-get.html`
