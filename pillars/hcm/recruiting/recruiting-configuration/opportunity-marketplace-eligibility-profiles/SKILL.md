---
skill_id: "hcm.recruiting.recruiting-configuration.opportunity-marketplace-eligibility-profiles"
name: "Opportunity Marketplace Eligibility Profiles"
description: "Lists Opportunity Marketplace eligibility profiles and guides profile-only preparation and approved Plan Copy imports using existing shared services. Read the operation scope for validated criteria and migration limits."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_MP_ELIGIBILITY_PROFILE"
task_name: "Opportunity Marketplace Eligibility Profiles"
parent_skill_id: "hcm.benefits-configuration.benefits-eligibility.eligibility-profiles"
available_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "benefitsPlanCopyImports"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM recruiting pillar team"
version: "1.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "opportunity_marketplace_setup_xlsx"
  - "fusion_environment_context"
  - "task_context"
  - "plan_copy_import_archive"
  - "approval_preview"
  - "effective_date"
  - "evaluation_person_name"
  - "evaluation_person_number_when_ambiguous"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "profile_intake_validation"
  - "active_eligibility_profiles"
  - "eligibility_profile_xml"
  - "supporting_object_xml"
  - "plan_copy_map_xml"
  - "plan_copy_import_archive"
  - "plan_copy_import_preview"
  - "plan_copy_import_result"
  - "eligibility_evaluation_preview"
  - "eligibility_evaluation_summary"
depends_on:
  - "hcm.benefits-configuration.benefits-eligibility.eligibility-profiles"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ess-job-submitter"
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
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-eligibility-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-eligibility-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-eligibility-profiles/current/"
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
  - "Writes generated XML, packages, and immutable approval previews in the selected project workspace."
  - "Performs read-only Fusion profile and reference lookups using shared OAuth authentication."
  - "After import approval, creates Plan Copy metadata, uploads the package, submits generateMappings, and monitors the combined import."
  - "After separate evaluation approval, creates and executes eligibility evaluations for imported profiles."
required_privileges:
  - "GET access to eligibilityProfilesLOV and the parent skill's declared target lookup resources."
  - "Parent skill Plan Copy write privileges for benefitPlanCopyParameters and its PackageContent and generateMappings operations."
  - "Parent skill ESS, Plan Copy status, mapping, and log read privileges."
  - "Parent skill personHeaders and formulaEvaluations privileges for separately approved evaluation."
---

# Opportunity Marketplace Eligibility Profiles

## Parent and scope

The behavioral parent is [Benefits Eligibility Profiles](../../../benefits-configuration/benefits-eligibility/eligibility-profiles/SKILL.md),
`hcm.benefits-configuration.benefits-eligibility.eligibility-profiles`.
Read the parent for conversion contracts, reference resolution, design review,
import/recovery and reporting. Benefits files are read-only dependencies.
The task remains ORA_IRC_MP_ELIGIBILITY_PROFILE under Recruiting Configuration.
Keep its own task context and active Run Book binding.

## Execution routes and migration scope

This skill installs no runtime Python and requires no custom Core Data Loader
adapter. Markdown references orchestrate existing shared services and contain
a tested transient XML recipe. Executable code still runs; changing its file
extension does not eliminate that need.

| Operation | Route and current scope |
|---|---|
| List profiles | Shared REST client; all visible OM result pages |
| Workbook validation and XML preparation | [Profile workflow](references/markdown-profile-workflow.md); Participant Eligibility, Person Type and Department only |
| Package assembly | Existing parent package builder; profile-only scope |
| Preview and approved import | [Import workflow](references/markdown-import-workflow.md); core.data-loader orchestration and unchanged parent importer |
| Monitor existing import | Parent resume path with matching retained run identity |
| Other criteria/supporting objects | Migration pending; do not silently omit or claim support |
| Automated person evaluation | Migration pending; parent default usage filter is not an OM route |

The first stage does not replace every former adapter operation. Expand tests
and mappings before enabling additional criteria or supporting-object tabs.
No fresh live import is implied by local test success. Do not use removed
adapter command lines or the Benefits-only wrapper as a fallback.

Retain `shared.setup-export.task-level-export` for declared setup export,
`shared.validation.setup-data-validator` and
`shared.validation.reference-data-validator` for validations, and
`core.data-loader` for import orchestration and its single approval workflow.
Do not infer CSV import support from catalog flags or route Plan Copy ZIPs to
a generic FSM/DAT uploader. No general PATCH/delete route is supplied.

## Listing Existing Profiles

Listing uses `core.fusion-api.rest-api-client` directly and needs no task-specific
adapter, workbook, Run Book, or import approval. Read that skill and its
`references/fusion-rest-api.md` before execution. Use the selected/default
OAuth environment in `core/auth/fusionEnv.properties`; resolve an ambiguous
target before connecting. Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /hcmRestApi/resources/11.13.18.05/eligibilityProfilesLOV \
  --method GET --header 'REST-Framework-Version=9' \
  --query "q=BnftCagrPrtnCd='ORA_OPP_MARKET_PLACE'" \
  --query 'fields=EligyPrflId,Name,Description,ProfileType,BnftCagrPrtnCd,StatCd,AsmtToUseCd' \
  --query onlyData=true --query orderBy=EligyPrflId \
  --query limit=200 --query offset=0 --token-cache .fusionaim_token.json
```

The shared client returns one page. Inspect each response and repeat with the
next offset (current offset plus the number of returned items) while `hasMore`
is true. Require an object response, an `items` array and boolean `hasMore`.
Require every requested field except nullable Description, unique nonblank
EligyPrflId values across pages, and usage ORA_OPP_MARKET_PLACE. Stop on malformed
responses, duplicate IDs, a nonterminal empty page, or a failed request; never
present partial results as a complete inventory. Retain the same query and
ordering on every page. Do not follow response links to another host.
For an exact-name lookup, add an escaped `Name` predicate to the same `q`
parameter (double embedded apostrophes); retain pagination and usage checks.

Report the target, total returned count, name, description, status, type and
assignment. Translate A/I to Active/Inactive, PRTP to Participant and APS to
Specific assignment; retain unknown codes. Report statuses actually returned.
The LOV is documented for active profiles but can return inactive rows in a
target environment. Describe results as profiles visible to the current account;
do not claim complete enterprise or inactive-profile coverage. Zero results
means no matching visible profiles, not proof that a name is globally unused.
No profile writes occur. Persist only a sanitized summary if a project is selected.

## Workbook and review requirements

Use the supplied workbook unchanged. Offer the local
[template](references/Opportunity_Marketplace_Eligibility_Setup.xlsx) when
needed; never import its examples automatically. The template includes
supporting examples beyond the initial Markdown route: explain this limit and
require explicit scope or a corrected file. Blank profile cells continue the
previous profile; conflicting values are errors. New profiles require
Participant, Opportunity Marketplace and Specific assignment (PRTP/ORA_OPP_MARKET_PLACE/APS).
Do not substitute values, rename duplicates or discard data automatically.

Apply the parent's numbered best-practice review; show every finding and
missing business/owner/consumer/test evidence before approval. The user must
see target, operation, date, archive identity, every profile, counts and design
findings. Wait for the later standalone message `approve` for that preview.

## Persistence and maintenance

Use existing project artifact and state services. Keep source data and secrets
out of tracked files; retain sanitized run records and token estimates in the
selected project. No new project is required for listing alone. On errors,
record failure class, stage and next action; never turn a failed lookup into
an empty inventory. No automatic live write retries.

Run tests under tests/ for the Markdown recipe and parent regression tests
when dependent contracts change. Tests are not runtime adapters. The historical
[feasibility trial](references/adapter-free-feasibility.md) predates this route;
its existing-XML result must not be described as fresh workbook conversion.
