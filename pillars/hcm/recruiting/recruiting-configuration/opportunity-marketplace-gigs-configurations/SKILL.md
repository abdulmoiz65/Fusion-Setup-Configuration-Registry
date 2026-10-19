---
skill_id: "hcm.recruiting.recruiting-configuration.opportunity-marketplace-gigs-configurations"
name: "Opportunity Marketplace Gigs Configurations Setup Task Guidance"
description: "Provides task-specific setup guidance for Opportunity Marketplace Gigs Configurations under the Recruiting Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_MP_SITE_GIG_CONFIGURATION"
task_name: "Opportunity Marketplace Gigs Configurations"
parent_skill_id: "hcm.recruiting.recruiting-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-gigs-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-gigs-configurations/current/"
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
side_effects: []
required_privileges: []
---

# Opportunity Marketplace Gigs Configurations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Opportunity Marketplace Gigs Configurations` under `Recruiting Configuration`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MP_SITE_GIG_CONFIGURATION`
- task_name: `Opportunity Marketplace Gigs Configurations`
- parent_skill_id: `hcm.recruiting.recruiting-configuration`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Configuration`
- functional_area_code: `ORA_RECRUITING_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Opportunity Marketplace Gigs Configurations` under `Recruiting Configuration`.

## Setup Task Metadata

- Task name: `Opportunity Marketplace Gigs Configurations`
- Task code: `ORA_IRC_MP_SITE_GIG_CONFIGURATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

## Creation Routing

Create Gig Configurations only through the task's CSV export/import workflow.

1. Export the current task CSV package with `shared.setup-export.task-level-export`.
2. Add the new configuration to the exported CSV structure and validate the
   resulting package, including the create validations below.
3. Before submission, present a confirmation summary with a two-column
   `Field`/`Value` table for target environment, operation, task,
   configuration code, configuration name, type, sequence, eligibility profile,
   location, job family, organization, and job function. Use every copied or
   supplied value, or `None` when no value exists. Then present the translation,
   availability-context, and child-filter candidate rows using business values
   only. Keep generated technical identifiers internal to archive validation.
   Identify the archive name and SHA-256 fingerprint,
   then ask for explicit import approval.
4. Submit only the unchanged, approved immutable FSM CSV archive through
   `core.data-loader` and its approval workflow.

Never create a Gig Configuration through the Fusion UI or use the UI as a
create fallback.

## Supported Operations

This skill supports read/list/export operations and creation of a new Gig
Configuration only. A request to copy a configuration is a creation request.
When a copy request omits both `SiteCode` and `SiteName`, display: `Since
Configuration code and Configuration name values are not provided. Configuration
code, Configuration name, and eligibility profile are mandatory to create a Gig
configuration. I am proposing the following values: <source_code>_copy and
<source_name>_copy.` Then ask the user to approve those proposed values before
continuing and to select an eligibility profile. Let the user provide both
replacement values instead. Apply the normal length and uniqueness validation
to the approved or supplied values. Never copy the source
`EligibilityName`. Copy only the source availability-context business filters
(locations, organizations, job families, and job functions), after validating
each against its current LOV. Do not retain the source configuration's
technical identifiers. Do not support any change to an existing Gig
Configuration, including:

- moving a Draft configuration to Active;
- deactivating an Active configuration;
- editing a configuration;
- deleting a configuration; or
- changing its sequence number.

If asked to perform an unsupported operation, state that it is not supported
by this skill and make no UI, CSV import, or REST change.

When a Gig Configuration create or copy request omits `EligibilityName`, or
the supplied eligibility profile is already assigned to a current Gig
Configuration, use `core.fusion-api.rest-api-client` to list every active
Opportunity Marketplace eligibility profile not assigned in the fresh Gig
export. Show the names to the user and require a selection before preparing a
candidate package. Do not select a profile automatically.

## Create Validation

Before creating an Opportunity Marketplace Gigs Configuration, require a
nonblank `SiteCode`. If it is missing or blank, stop the create workflow and
request a `SiteCode` before preparing an import or write.

For a create request, validate the `SiteCode` length before any reference,
uniqueness, package, or import step. When the supplied value exceeds 200
characters, truncate it to its first 200 characters and use that truncated
value as the submitted `SiteCode` for all remaining checks and the generated
FSM CSV package. Report that truncation occurred. Perform the nonblank and
uniqueness checks against the resulting value; if truncation creates a
duplicate, stop and require a different `SiteCode`.

Also require a nonblank `SiteName`. If it is missing or blank, stop the create
workflow and request a `SiteName` before preparing an import or write.

For a create request, validate the `SiteName` length before package or import
preparation. When the supplied value exceeds 100 characters, truncate it to
its first 100 characters and use that truncated value as the submitted
`SiteName` in all generated FSM CSV rows, including translations. Report that
truncation occurred, then confirm that the resulting `SiteName` is nonblank
before continuing.

For a copy request, derive the candidate `SiteCode` and `SiteName` from the
fresh-export source row by appending `_copy` to each source value. If the
requester omitted both fields, stop and display: `Since Configuration code and
Configuration name values are not provided. Configuration code, Configuration
name, and eligibility profile are mandatory to create a Gig configuration. I
am proposing the following values: <source_code>_copy and <source_name>_copy.`
Ask for approval of those values and continue only after approval or after the
requester supplies both replacement values. If the requester supplied a code
and name, use those supplied values. Apply normal truncation and uniqueness
rules in either case. Require the user to provide an active, unused
`EligibilityName`; never copy the source eligibility profile.
Copy only the source location, organization, job-family, and job-function
business values, and validate every copied value using the same current LOV
rules as explicitly supplied filters.

For every create request, derive `SequenceOrder` from the fresh current-task
export. Set it to one greater than the highest existing `SequenceOrder`.
Ignore any `SequenceOrder` copied from an existing Gig Configuration or
supplied by the requester; never reuse the source configuration's sequence.
If the current maximum cannot be established from the fresh export, stop the
create workflow before preparing a package.

For every new availability context created directly or by copying a Gig
Configuration, generate new technical identifiers before preparing the FSM
archive. Use a cryptographically secure 16-byte random value encoded as exactly
32 uppercase hexadecimal characters, matching the value shape returned by
Fusion's `SYS_GUID()` generation used by the UI. Do not ask the user to supply
these values, leave them blank, derive them from business data, or copy them
from another configuration.

- Generate one `ObjectCxtCode` for each new
  `ORA_IRC_MP_SITE_GIG_CONFIG_AVAIL_CXT` row.
- Reuse that new `ObjectCxtCode` only where the child CSV requires its parent
  relationship.
- Generate a distinct child identifier for every newly added child row:
  `ObjectCxtLocCode` for location rows, `ObjectCxtJobFamCode` for job-family
  rows, `ObjectCxtJobFuncCode` for job-function rows, and `ObjectCxtOrgCode`
  for organization rows.
- Omit a child CSV row when its corresponding business filter is not supplied;
  never generate an unused child identifier.
- Verify all generated values are unique within the candidate archive and that
  every child row references its new parent `ObjectCxtCode` before preview.

### Availability-context ObjectTypeCode bootstrap

Before adding a row to `ORA_IRC_MP_SITE_GIG_CONFIG_AVAIL_CXT.csv`, inspect the
fresh, same-task member after validating its headers and CSV shape.

1. If it contains one or more data rows, retain the established
   `ObjectTypeCode` only when every populated value is `ORA_OM_GIG_SITE`. A
   blank, mixed, or different value is a package-contract error: stop before
   archive generation.
2. If it contains valid headers but zero data rows, read the Gig-specific
   sample-derived bootstrap contract in
   [ora-resource/ora_fsm_bootstrap_contracts.md](ora-resource/ora_fsm_bootstrap_contracts.md)
   and set every new context row's `ObjectTypeCode` to `ORA_OM_GIG_SITE`.
3. Never infer `ObjectTypeCode` from the task code, configuration type, CSV
   member name, root FSM object name, or a Jobs sample. In particular,
   `ORA_IRC_MP_SITE_GIG_CONFIG_FILTER` is not a permitted value.

Before preview, verify each candidate
`ORA_IRC_MP_SITE_GIG_CONFIG_AVAIL_CXT.csv` data row has exactly
`ObjectTypeCode=ORA_OM_GIG_SITE`. Persist the populated-export or zero-row
bootstrap decision, source export fingerprint, source-row count, and resolved
value in the validation/preflight artifact. If the member is missing,
malformed, stale, or the bootstrap contract is unavailable, stop rather than
guessing a technical value.

Also require a nonblank `EligibilityName` before package generation. Before
creating the configuration, use the public, read-only Eligibility Profiles LOV/REST endpoint
`/hcmRestApi/resources/{version}/eligibilityProfilesLOV` to resolve an exact
profile `Name`. Require exactly one profile with active status (`StatCd=A`) and
Profile Usage (`BnftCagrPrtnCd`) equal to `ORA_OPP_MARKET_PLACE`. If no such
profile exists, stop the create workflow and display `Eligibility profile: <provided_eligibility_profile_name> is invalid. Enter an active Opportunity Marketplace eligibility profile.`

After that eligibility-profile validation, perform a read-only lookup to
confirm that no existing configuration uses the supplied `EligibilityName`. If
the request omitted an eligibility profile, or the profile is already in use,
list all active Opportunity Marketplace profiles that are not assigned in the
fresh Gig export, then require the user to select one. If the list is empty,
stop and report that no unused active Opportunity Marketplace eligibility
profile is available. Do not prepare a package until the user selects a listed
profile and it passes exact active-profile validation.

When a location value is supplied for a new configuration, validate each value
before preparing the import. Use the public, read-only Recruiting Geography
Hierarchy Locations LOV/REST endpoint
`/hcmRestApi/resources/{version}/recruitingGeographyHierarchyLocationsLOV` to
resolve an exact `GeographyName`, which is the value displayed by the Gig
Configuration UI Location control. Do not invoke the Manage Locations skill or
perform a write for this reference read. Require exactly one geography match.
If a supplied value has no match or is ambiguous, stop the create workflow and
display `Location: <provided_location_value> is invalid. Enter a valid location value.`

### Location CSV serialization

`GeographyName` is a display value used to resolve the geography hierarchy; do
not write its `CountryCode` directly to
`GeographyElement1IdentifierValue`, and do not substitute a generic language
such as `en` for a geography-element language code. Before package generation,
derive each populated `GeographyElement<N>IdentifierValue` and its paired
`GeographyElement<N>LanguageCode` from the resolved geography hierarchy and
the current same-task FSM export contract. Preserve the hierarchy from country
to its more specific elements.

For example, the exact display value `United States` serializes as
`GeographyElement1IdentifierValue=United States` and
`GeographyElement1LanguageCode=US`. The exact display value
`FL, United States` serializes as `United States`/`US` in element 1 and
`FL`/`US` in element 2. Do not emit a location child row if this hierarchy
mapping cannot be proven from current task data; stop and report the mapping
gap instead.

When an organization value is supplied for a new configuration, validate it
before preparing the import. Use the public, read-only Recruiting Organization
LOV/REST endpoint
`/hcmRestApi/resources/{version}/recruitingOrganizationsLOV` with its
`findByWord` finder to resolve an exact `Name`. The finder is scoped to
organizations available to Recruiting; require exactly one matching result. Do
not invoke an organization-management skill or perform a write for this
reference read. If a supplied value has no eligible match or is ambiguous, stop
the create workflow and display `Organization: <provided_organization_value> is invalid. Enter a valid organization value.`

When a job family value is supplied for a new configuration, validate it before
preparing the import. Use the public, read-only Job Family LOV/REST endpoint
`/hcmRestApi/resources/{version}/jobFamiliesLov` to resolve an exact
`JobFamilyName` (or an exact `JobFamilyCode` when that is the supplied value).
Require exactly one active, effective job family match. If there is no eligible
match or the value is ambiguous, stop the create workflow and display `Job family: <provided_job_family_value> is invalid. Enter a valid active job family.`

When a job function value is supplied for a new configuration, validate it
before preparing the import. Use the public, read-only Common Lookups REST
endpoint `/fscmRestApi/resources/{version}/commonLookupsLOV` with
`LookupTypeFinder;LookupType=JOB_FUNCTION_CODE`, and resolve an exact active,
effective `LookupCode`. If there is no eligible match or the value is
ambiguous, stop the create workflow and display `Job function: <provided_job_function_value> is invalid. Enter a valid active job function.`

After the required-field and `EligibilityName` validations, validate that the
supplied `SiteCode` is unique across existing configurations.

- Perform a read-only lookup using the same `SiteCode` comparison behavior as
  the target configuration service or UI.
- If a configuration already has that `SiteCode`, stop the create workflow and display `This configuration code : ` followed by the submitted `SiteCode`, then ` already exists. Enter a unique value.` Require a different `SiteCode` before preparing an import or write. For example, a submitted `SiteCode` of `NYC01` displays: `This configuration code : NYC01 already exists. Enter a unique value.`
- For an edit, exclude the configuration being edited from the `SiteCode` and
  `EligibilityName` uniqueness checks.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Configuration`
- Setup task name: `Opportunity Marketplace Gigs Configurations`
- Setup task code: `ORA_IRC_MP_SITE_GIG_CONFIGURATION`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.recruiting.recruiting-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
