---
skill_id: "hcm.recruiting.recruiting-configuration.opportunity-marketplace-jobs-configurations"
name: "Opportunity Marketplace Jobs Configurations Setup Task Guidance"
description: "Provides task-specific setup guidance for Opportunity Marketplace Jobs Configurations under the Recruiting Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_MP_SITE_CONFIGURATION"
task_name: "Opportunity Marketplace Jobs Configurations"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-jobs-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/opportunity-marketplace-jobs-configurations/current/"
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

# Opportunity Marketplace Jobs Configurations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Opportunity Marketplace Jobs Configurations` under `Recruiting Configuration`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MP_SITE_CONFIGURATION`
- task_name: `Opportunity Marketplace Jobs Configurations`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Opportunity Marketplace Jobs Configurations` under `Recruiting Configuration`.

## Setup Task Metadata

- Task name: `Opportunity Marketplace Jobs Configurations`
- Task code: `ORA_IRC_MP_SITE_CONFIGURATION`
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

## FSM-Only Execution Boundary

Use the FSM CSV export/import workflow as the exclusive system interaction
path for this task. This applies to listing, reading, exporting, copying, and
creating Job Configurations.

- Obtain the current configuration inventory and a copy source only from a
  fresh `shared.setup-export.task-level-export` package for
  `ORA_IRC_MP_SITE_CONFIGURATION`.
- Use the exported CSV members, including their parent-child relationships, as
  the sole source of configuration values and package structure.
- Submit changes only as an immutable FSM CSV archive through
  `core.data-loader` and its approval workflow.
- Do not open, query, inspect, create, copy, edit, activate, deactivate, or
  delete a Job Configuration through the Fusion UI. The UI is not a read
  fallback when an export is empty, stale, incomplete, or unavailable. Stop
  and obtain a fresh FSM export for stale, incomplete, or unavailable data;
  a structurally valid fresh export with zero Recruiting Type child rows
  follows the bootstrap rule below.

## Creation Routing

Create Job Configurations only through the task CSV export/import workflow.

1. Export the current task CSV package with `shared.setup-export.task-level-export`.
2. Add the new configuration to that exported CSV structure and validate the
   resulting package, including every create validation below.
3. Before submission, present a two-column `Field`/`Value` table for target
   environment, operation, task, configuration code, configuration name, type,
   sequence, eligibility profile, location, job family, organization, job
   function, and Recruiting Type. Show the resolved LOV display meanings for
   Job function and Recruiting Type, not their internal LookupCode values. Use every copied or supplied value, or
   `None` when no value exists. Do not show translation, availability-context,
   or child-filter candidate rows. Keep generated technical identifiers and
   candidate-row detail internal to archive validation. Identify the archive
   name and SHA-256 fingerprint, then ask: `Do you want to proceed with
   submitting the reviewed archive?`
4. Submit the unchanged, approved immutable FSM CSV archive through
   `core.data-loader` and its approval workflow.

Never create a Job Configuration through the Fusion UI or use the UI as a
create fallback.

## Supported Operations

This skill supports read, list, and export operations through a fresh FSM
export, and creation of a new Job Configuration through FSM import only. A
request to copy a configuration is a creation request. When a copy request
omits both `SiteCode` and `SiteName`, display: `Since Configuration code and
Configuration name values are not provided. Configuration code, Configuration
name, and eligibility profile are mandatory to create a Job configuration. I
am proposing the following values: <source_code>_copy and <source_name>_copy.`
Require the user to approve those proposed values or provide both replacement
values. Apply the normal length and uniqueness validation to the approved or
supplied values. Never copy the source `EligibilityName`. If the eligibility
profile is omitted or is already assigned, list all active unused Opportunity
Marketplace eligibility profiles and require a user selection before preparing
a candidate package. Copy only the source
availability-context business filters—locations, organizations, job families,
job functions, and Recruiting Types—after validating each against its current
LOV. Do not retain the source configuration's technical identifiers. Do not
support a change to an existing Job Configuration, including activation,
deactivation, edit, deletion, or a sequence-number change.

If asked to perform an unsupported operation, state that it is not supported
by this skill and make no UI, CSV import, or REST change.

## Create Validation

Before creating an Opportunity Marketplace Jobs Configuration, require a
nonblank `SiteCode`. Validate its length before any reference, uniqueness,
package, or import step. If it exceeds 200 characters, truncate it to its
first 200 characters, report the truncation, and use that retained value for
all later checks and generated CSV rows. Perform the nonblank and uniqueness
checks against the retained value; if truncation creates a duplicate, stop and
require a different `SiteCode`.

Also require a nonblank `SiteName`. Validate its length before package or
import preparation. If it exceeds 100 characters, truncate it to its first
100 characters, report the truncation, use it in every generated CSV row
including translations, and confirm the retained value remains nonblank.

For a copy request, derive the candidate `SiteCode` and `SiteName` from the
fresh-export source row by appending `_copy` to each source value. When both
identity fields are omitted, stop and display: `Since Configuration code and
Configuration name values are not provided. Configuration code, Configuration
name, and eligibility profile are mandatory to create a Job configuration. I
am proposing the following values: <source_code>_copy and <source_name>_copy.`
Continue only after the user approves those values or supplies both replacement
values. If the requester supplied a code and name, use those supplied values.
Apply normal truncation and uniqueness rules in either case. Require an active,
unused `EligibilityName`; never copy the source eligibility profile. If the
profile is omitted or already assigned, list all active unused Opportunity
Marketplace profiles and require a selection. Copy only the
source location, organization, job-family, job-function, and Recruiting-Type
business values, and validate every copied value using the same current LOV
rules as an explicitly supplied value.

For every create request, derive `SequenceOrder` from the fresh current-task
export. Set it to one greater than the highest existing `SequenceOrder`.
Ignore any value copied from an existing Job Configuration or supplied by the
requester; never reuse the source configuration's sequence. If the current
maximum cannot be established from the fresh export, stop before preparing a
package.

For every new availability context created directly or by copying a Job
Configuration, generate new technical identifiers before preparing the FSM
archive. Use a cryptographically secure 16-byte random value encoded as
exactly 32 uppercase hexadecimal characters, matching the value shape used by
the Fusion UI's `SYS_GUID()` generation. Do not ask the user to supply these
values, leave them blank, derive them from business data, or copy them from a
different configuration.

- Generate one `ObjectCxtCode` for each new
  `ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT` row, and reuse it only where the child
  CSV requires the parent relationship.
- Generate a distinct child identifier for every supplied child row:
  `ObjectCxtLocCode`, `ObjectCxtJobFamCode`, `ObjectCxtJobFuncCode`,
  `ObjectCxtOrgCode`, and `ObjectCxtRecTypeCode` for location, job-family,
  job-function, organization, and Recruiting-Type rows respectively.
- Omit a child CSV row, and therefore its identifier, if the associated
  business filter is not supplied.
- Verify every generated value is unique within the candidate archive and
  that each child row references the new parent `ObjectCxtCode` before
  preview.

Use the fresh Job Configuration export as the package contract. Preserve its
metadata member, exact member names, headers and header order, current rows,
translation rows, and valid parent-child relationships. Do not hand-build an
archive or substitute Gig CSV member names. The Jobs package additionally
contains the `ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT_REC_TYPE.csv` child member;
its `RecruitingTypeCode` must be the LookupCode resolved from the user-supplied
Recruiting Type display meaning. Derive its system-owned `DefaultFlag` using
the Recruiting Type defaulting rule below. The job-function child row likewise uses the LookupCode
resolved from the user-supplied Job function display meaning.

### Availability-context ObjectTypeCode bootstrap

Before adding a row to `ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT.csv`, inspect the
fresh, same-task member after validating its headers and CSV shape.

1. If it contains one or more data rows, retain the established
   `ObjectTypeCode` only when every populated value is `ORA_OM_SITE`. A blank,
   mixed, or different value is a package-contract error: stop before archive
   generation.
2. If it contains valid headers but zero data rows, read the Jobs-specific
   sample-derived bootstrap contract in
   [ora-resource/ora_fsm_bootstrap_contracts.md](ora-resource/ora_fsm_bootstrap_contracts.md)
   and set every new context row's `ObjectTypeCode` to `ORA_OM_SITE`.
3. Never infer `ObjectTypeCode` from the task code, configuration type, CSV
   member name, root FSM object name, or a Gig sample. In particular,
   `ORA_OM_JOB_SITE` and `ORA_IRC_MP_SITE_CONFIG_FILTER` are not permitted
   values.

Before preview, verify each candidate
`ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT.csv` data row has exactly
`ObjectTypeCode=ORA_OM_SITE`. Persist the populated-export or zero-row
bootstrap decision, source export fingerprint, source-row count, and resolved
value in the validation/preflight artifact. If the member is missing,
malformed, stale, or the bootstrap contract is unavailable, stop rather than
guessing a technical value.

### Recruiting Type DefaultFlag Derivation

Before adding candidate rows to
`ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT_REC_TYPE.csv`, inspect that member in the
fresh Jobs Configuration export:

1. If one or more Recruiting Type child rows exist, derive and reuse the
   established `DefaultFlag` value from that fresh package contract. Do not
   replace an established value with a bootstrap default. If the value cannot
   be established unambiguously, stop and resolve the package-contract issue.
2. If the member has valid headers but zero Recruiting Type child data rows,
   automatically set `DefaultFlag` to `N` for each new Recruiting Type row.
   This is the approved initial-configuration bootstrap case, not a preflight
   blocker solely because there is no source row.
3. Never ask the user to provide `DefaultFlag` or accept a user override; it
   is a system-derived FSM value. A missing member, malformed CSV, missing
   `DefaultFlag` column, or stale export does not qualify as zero rows.

Apply [the defaulting rules](ora-resource/ora_defaulting_rules.md) before
design enforcement and immutable preview. Persist the decision in the task
validation/preflight artifact, with the fresh export reference/fingerprint
and source child-row count. For bootstrap, record exactly:

```yaml
DefaultFlag: N
reason: No Recruiting Type rows exist in the fresh Jobs Configuration export; applied approved bootstrap default.
```

For a populated source, record the reused value and its source-row evidence.
If no Recruiting Type filter is supplied, record the rule as not applicable
and do not create a child row. All exact LOV, resolved `LookupCode`, fresh
export, identifier uniqueness, archive validation, immutable approval, and
`core.data-loader` import requirements remain in force.

After the required-field and eligibility validations, verify that the retained
`SiteCode` is unique across current Job Configurations using the fresh export.
If a configuration already has that value, stop and display `This
configuration code : <code> already exists. Enter a unique value.` Require a
different code before package preparation. Do not apply an edit exclusion:
editing is unsupported.

## Recruiting Type Validation

When a Job Configuration creation request supplies one or more Recruiting
Types, validate each value through the public, read-only Common Lookups REST
service before preparing an FSM archive:

`/fscmRestApi/resources/{version}/commonLookupsLOV` using
`LookupTypeFinder;LookupType=ORA_IRC_RECRUITING_TYPE`.

Users supply the exact `Meaning` display value, never a `LookupCode`. Require
exactly one returned row whose `Meaning` matches the supplied Recruiting Type,
then retain that row's `LookupCode` only for the FSM child CSV. If the display
value is absent or ambiguous, stop the create workflow and request a valid
Recruiting Type display value. Do not use the UI or a write operation to
resolve this reference.

## Availability-Context Reference Validation

When a Job Configuration creation request supplies locations, organizations,
job families, or job functions, validate each value through the same public,
read-only REST services and exact-match rules used for Gig Configurations:

| Field | REST service | Validation rule |
|---|---|---|
| Location | `/hcmRestApi/resources/{version}/recruitingGeographyHierarchyLocationsLOV` | Require exactly one `GeographyName` match. |
| Organization | `/hcmRestApi/resources/{version}/recruitingOrganizationsLOV` using `findByWord` | Retain the exact `Name` in Recruiting scope and require exactly one match. |
| Job family | `/hcmRestApi/resources/{version}/jobFamiliesLov` | Require exactly one active, effective `JobFamilyName` or `JobFamilyCode` match. |
| Job function | `/fscmRestApi/resources/{version}/commonLookupsLOV` using `LookupTypeFinder;LookupType=JOB_FUNCTION_CODE` | Users supply an exact active, effective `Meaning`; require one match and use its `LookupCode` only in the FSM child CSV. |

Stop the create workflow when a supplied value has no exact eligible match or
has multiple matches. Do not use the UI or a write operation to resolve these
references.

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

## Eligibility Profile Validation

For every Job Configuration creation request, require a nonblank
`EligibilityName` and validate it through the public, read-only Eligibility
Profiles LOV REST service:

`/hcmRestApi/resources/{version}/eligibilityProfilesLOV`.

Require exactly one profile with an exact `Name`, active status `StatCd=A`, and
profile usage `BnftCagrPrtnCd=ORA_OPP_MARKET_PLACE`. Before package generation,
use the fresh Job Configuration export to confirm that no current Job
Configuration already uses the resolved eligibility profile. If the profile is
omitted or already assigned, list every active Opportunity Marketplace profile
not assigned in the fresh export and require a user selection; do not choose a
profile automatically. Stop when the profile is invalid, ambiguous, inactive,
has a different usage, or no unused active profile is available.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Configuration`
- Setup task name: `Opportunity Marketplace Jobs Configurations`
- Setup task code: `ORA_IRC_MP_SITE_CONFIGURATION`




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
