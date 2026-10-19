---
skill_id: "hcm.benefits-configuration.benefits-eligibility.eligibility-profiles"
name: "Eligibility Profiles"
description: "Collects an end-user XLSX workbook and converts its participant eligibility, Postal Code Ranges, Service Areas, and maintained derived-factor tabs into a validated Plan Copy package and imports it through an approval-gated Fusion workflow. Use for eligibility-profile setup, eligibility criteria, service-area setup, or Benefits derived-factor imports."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Eligibility"
functional_area_code: "ORA_BENEFITS_ELIGIBILITY"
task_code: "BEN_MANAGE_ELIGIBILITY_PROFILES"
task_name: "Eligibility Profiles"
parent_skill_id: "hcm.benefits-configuration.benefits-eligibility"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "benefitsPlanCopyImports"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM benefits configuration pillar team"
version: "1.19.7"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_elpro_setup_xlsx"
  - "plan_copy_xml_samples_directory"
  - "eligibility_mapping_reference_directory"
  - "fusion_environment_context"
  - "plan_copy_openapi_document"
  - "plan_copy_import_archive"
  - "task_context"
  - "evaluation_person_name"
  - "evaluation_person_number_when_ambiguous"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "plan_copy_import_preview"
  - "plan_copy_import_result"
  - "plan_copy_import_summary"
  - "eligibility_profile_xml"
  - "postal_code_range_xml"
  - "service_area_xml"
  - "age_factor_xml"
  - "compensation_level_factor_xml"
  - "length_of_service_factor_xml"
  - "combined_age_length_of_service_factor_xml"
  - "hours_worked_factor_xml"
  - "full_time_equivalent_factor_xml"
  - "plan_copy_map_xml"
  - "eligibility_evaluation_preview"
  - "eligibility_evaluation_summary"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
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
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/current/"
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
  - "Writes a local BEN_ELIGY_PRFL.xml preparation artifact when conversion succeeds."
  - "Writes local BEN_PSTL_ZIP_RNG.xml and BEN_SVC_AREA.xml preparation artifacts when conversion succeeds."
  - "Writes local BEN_AGE_FCTR.xml and BEN_COMP_LVL_FCTR.xml preparation artifacts when derived-factor conversion succeeds."
  - "Writes local BEN_LOS_FCTR.xml, BEN_CMBN_AGE_LOS_FCTR.xml, BEN_HRS_WKD_IN_PERD_FCTR.xml, and BEN_PCT_FL_TM_FCTR.xml preparation artifacts when derived-factor conversion succeeds."
  - "Writes a local BEN_PL_COPY_MAP.xml preparation artifact when map generation succeeds."
  - "Writes a local ten-batch Plan Copy ZIP when eligibility package generation succeeds."
  - "Performs read-only Fusion lookup GET requests for lookup-backed workbook meanings."
  - "Uses the selected target environment's OAuth configuration for every Fusion lookup and import request."
  - "After immutable Task Hook approval, may create a Plan Copy import with RequestSource FDOS, upload its ZIP enclosure, submit the combined mapping/import action, and monitor its ESS request."
  - "After separate post-import approval, may create and execute one eligibility evaluation request per imported profile."
required_privileges:
  - "GET access to /fscmRestApi/resources/11.13.18.05/commonLookupsLOV"
  - "GET access to /fscmRestApi/resources/11.13.18.05/genericLookups for secured HCM_LOOKUPS types"
  - "GET access to /hcmRestApi/resources/11.13.18.05/assignmentStatusTypesLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/hcmBusinessUnitsLOV"
  - "GET access to /hcmRestApi/resources/11.13.18.05/legalEmployersLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/unionsLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/actionsLOV"
  - "GET access to /hcmRestApi/resources/11.13.18.05/salaryBasisLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/fastFormulas"
  - "GET access to /hcmRestApi/resources/11.13.18.05/departments"
  - "GET access to /hcmRestApi/resources/11.13.18.05/jobFamiliesLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/collectiveAgreementsLov"
  - "GET access to /hcmRestApi/resources/11.13.18.05/personTypesLOV"
  - "GET access to /hcmRestApi/resources/11.13.18.05/benefitGroupsLOV"
  - "GET access to /fscmRestApi/resources/11.13.18.05/currenciesLOV"
  - "GET access to /hcmRestApi/resources/11.13.18.05/benefitBalancesLOV"
  - "OAuth write access to /hcmRestApi/resources/latest/benefitPlanCopyParameters, its PackageContent enclosure, and the generateMappings ADF action"
  - "GET access to /ess/rest/scheduler/v1/requests/{requestId}"
  - "GET access to /hcmRestApi/resources/11.13.18.05/eligibilityProfilesLOV and personHeaders"
  - "POST and GET access to /hcmRestApi/resources/11.13.18.05/formulaEvaluations, its evaluateEligibility action, result child, and MessageDetails enclosure"
---

# Eligibility Profiles

## Purpose

Converts the end-user-supplied XLSX workbook, using the `Fusion_Elpro_Setup.xlsx` template structure, into the ten batches required by the eligibility Plan Copy workflow and—only after explicit approval—creates eligibility profiles, Postal Code Ranges, Service Areas, and all maintained derived factors in Fusion. The import uses an explicit effective date and defaults to the current date. Benefit Group and Benefit Balance references must already exist in the target pod.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_ELIGIBILITY_PROFILES`
- task_name: `Eligibility Profiles`
- parent_skill_id: `hcm.benefits-configuration.benefits-eligibility`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits Eligibility`
- functional_area_code: `ORA_BENEFITS_ELIGIBILITY`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `benefitsPlanCopyImports`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when an eligibility-profile workbook must be validated, converted, packaged, previewed, or imported through Benefits Plan Copy.

### Required end-user workbook intake

Before workbook-based creation, conversion, or package generation, obtain
`fusion_elpro_setup_xlsx` from the end user:

1. Accept an uploaded `.xlsx` attachment or an explicit, accessible local file
   path. If neither is supplied, link the included
   [sample workbook](references/Fusion_Elpro_Setup.xlsx) and say: "Make a copy
   of this sample workbook, replace its example rows with your own data, then
   upload your completed copy or provide its full local path." Stop workbook processing
   until the file is available; do not start Fusion lookups or generate a package.
2. Use the file already supplied for the current request without asking for it
   again. Reuse a previous workbook only when the user explicitly requests it
   (for example, "same worksheet"). If several files could match, ask which one.
   Do not search for and silently select a workbook from Downloads, a previous
   run, or the bundled references.
3. Accept any `.xlsx` filename; `Fusion_Elpro_Setup.xlsx` names the template,
   not a required upload filename. Check that the selected file is readable and
   validate its worksheets, headers, and populated rows against
   [Eligibility Reference](references/eligibility-reference.md#eligibility-profiles)
   and the applicable conversion rules. Unused tabs may be deleted or left blank
   (including header-only Postal Code Ranges); they contribute zero objects and
   must not block generation or preview. Keep the sample's tab names and headers
   for populated sections. Require at least one setup row across the workbook.
   Validate every populated row and referenced dependency; removing a tab does
   not waive references to objects it would have supplied. Report invalid input and ask
   for a corrected workbook; do not fill gaps with sample data.
4. Pass the exact selected file path explicitly as `--input` to every workbook
   conversion or generation command. All examples below use
   `<end-user-workbook.xlsx>` for this path. Keep the source workbook unchanged.

Tell the end user to use the included sample workbook as the starting point,
make a copy, and enter their own data. For an already supplied workbook that
matches this structure, continue without asking for another copy. The bundled sample is not an import
source unless the user explicitly requests a sample-data demonstration.
Providing a workbook is not import approval; retain the existing validation,
preview, and approval gates. This intake does not require a new workbook for
monitoring an existing import or submitting an already approved immutable ZIP.

### Script entry points

All conversion, package generation, preview, and import logic is in
`scripts/eligibility.py`:

- `eligibility.py`: governed preview and approved import.
- `eligibility.py generate`: eligibility package generation only.
- `eligibility.py import`: immutable approval preview, import, and monitoring.
- `eligibility.py evaluate`: read-only person/profile resolution, evaluation preview,
  separately approved execution, and result summary.

The file keeps conversion and REST compatibility components in named isolated
namespaces. Plan Configuration imports those components
from this same file. Focused conversion subcommands are documented below.

## Reference guide

Use the maintained [Fusion Eligibility Profile Setup workbook](references/Fusion_Elpro_Setup.xlsx)
as the reference for the supported worksheet structure and sample setup values.
Offer it to the end user as a template when needed; use their completed copy
as the input selected above. Do not modify the packaged reference workbook or
automatically import its sample setup values.

All supporting Markdown guidance is consolidated in
[Eligibility Reference](references/eligibility-reference.md). Its contents
links separate conversion, import/recovery, mapping, lookup, and evaluation
guidance. Follow the section links below for the current operation.
Runtime contracts are consolidated in `references/eligibility-contracts.json`:
`lookup_mappings`, `map_rules`, `mapping_catalog`, and `openapi`.
Legacy file and mapping-directory paths in commands below remain supported
logical aliases resolved by the shared reader; they are not separate files.
Loose custom contract files and CSV overrides still take precedence.

### Best-practice evaluation

When evaluating profiles for import, read
[Eligibility best practices and evaluation](references/eligibility-reference.md#eligibility-best-practices).
It contains the supplied Oracle Benefits document's 30 practices and the review
procedure. Review the exact input workbook and available business/test evidence
before requesting import approval. Report profile/row-specific findings with
practice numbers; distinguish recommendations and missing evidence from
converter errors. Do not change configuration automatically or claim that an
API success proves eligibility outcomes. Keep the existing approval gate.
In the approval response, show the generated import preview and the design
findings directly to the user; artifact links alone do not satisfy this step.
Include the target environment, operation, effective date, immutable archive
identity, every profile to be imported, setup-object counts, and all review
findings with their dispositions and recommended actions. Call out missing
source or test evidence explicitly. Link the saved preview and review artifacts
as supporting records, then request approval only after this information is
visible. If validation blocks the preview, show the blocker instead of an
approval request.

## Task Resource Rules

Before preview or execution, resolve the task-local plan from
`ora-resource/ora_rule_registry.json` and evaluate its source files in planned
order. The v3 resource package owns input validation, dependency readiness,
read-only REST lookups, design enforcement, and error gates. The mutating
`benefitPlanCopyParameters` POST, enclosure PUT, and single `generateMappings`
ADF action remain
owned by `references/eligibility-reference.md#import-and-recovery` and `scripts/eligibility.py import`.

The host-neutral REST definition is the OpenAPI 3.1.2 document
`references/plan-copy.openapi.json`. It declares the reviewed
`benefitPlanCopyParameters` and ESS paths, operations, media types, parameters,
responses, and schemas. It contains no environment URL, runtime date,
credential, token, script, or workstation file path. The importer validates
and hashes this document before preview and approved execution.

## Final import summary and optional person evaluation

After the native Data Loader route verifies a terminal `SUCCESS`, end the
user-facing response with an import summary assembled from the verified result
and the immutable approval preview. Show the target environment, Plan Copy
name, effective date, final status, each imported profile and its criterion
count, and total setup-object count and counts by object type. Link the approved
package, preview, and project result record when available. Include outstanding
design findings or missing expected-versus-actual test evidence; a successful
import does not establish eligibility outcomes or activation readiness. Do not
stop at the route's short `planCopyName`/`status` JSON result or display internal
Plan Copy IDs, ESS request IDs, or raw statuses. On failure, timeout, or an
unverified result, report the failure and recovery action instead of a success
summary.

If eligibility profiles were imported, close the successful response with an offer to evaluate the imported
profiles for a person, asking for the person's display name if they want that
follow-up. The import approval does not authorize evaluation. If the user
accepts, read [Post-import eligibility evaluation](references/eligibility-evaluation.md),
obtain the display name if it was not already supplied, and run
`eligibility.py evaluate` without `--approve-evaluation`. Show the resolved
person, primary assignment, effective date, and profile names, then obtain
separate explicit approval before evaluator POSTs. Rerun with
`--approve-evaluation` only after that approval. If the name is ambiguous, ask
for the person number and rerun with `--person-number`.

After `evaluation_completed`, report the person, primary assignment, effective
date, overall eligible/ineligible counts, and every profile's outcome. For each
returned `criteriaResults` entry, show its criterion, `expectedValue`, and
`actualValue` together in the user-facing report; a reason alone is not a
substitute. Preserve returned values such as `No value found`. For a profile
with no returned criterion comparisons, show that none were returned instead
of inventing expected or actual values. Use the completed evaluator result to
render the report without repeating evaluation POSTs. Do not persist raw person
or diagnostic data in the project workspace.

## REST-Only Mapping Resolution

- Resolve every workbook lookup and every `SrcId`/`TrgId` mapping through the maintained REST resource or resolver declaration on the selected target pod.
- Use a database connection only for explicit, read-only debugging or root-cause analysis. Never call it from the normal import, lookup, mapping, polling, or success path, and never use database results to populate, default, or validate an import mapping.
- If the maintained resolver catalog does not identify a REST collection that returns the required target identifier, stop before package creation and ask the user for the corresponding REST API. Do not query the database as a fallback, copy an ID from another pod, guess an ID, or leave a mapping for manual completion.
- Keep the REST endpoint, natural-key filter, returned ID field, ambiguity policy, and target-pod identity in the maintained resolver catalog so the same contract is used by preview and approved import.

## Setup Task Metadata

- Task name: `Eligibility Profiles`
- Task code: `BEN_MANAGE_ELIGIBILITY_PROFILES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `benefitsPlanCopyImports`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using benefitsPlanCopyImports as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Benefits`
- Functional area / Setup Object: `Benefits`
- Setup task name: `Eligibility Profiles`
- Setup task code: `BEN_MANAGE_ELIGIBILITY_PROFILES`


## Convert Eligibility Excel to Plan Copy XML

Use this local preparation workflow when the source is the `Participant Eligibility` worksheet in `Fusion_Elpro_Setup.xlsx` and the target is the Plan Copy `BEN_ELIGY_PRFL.xml` structure.

The ten Oracle-exported XML templates are stored in `assets/plan-copy/templates.zip`.
Readers load named members directly without extraction. XML sample paths in the
commands below identify members of that sibling archive when no loose file exists.
A supplied loose XML file takes precedence, preserving reviewed custom overrides.
Keep `--samples-dir` pointed at the directory containing `templates.zip`.
This template archive is not the generated import package `benefits_eligibility.zip`.

1. Use the bundled Oracle-exported structural sample at `assets/plan-copy/BEN_ELIGY_PRFL.xml`. Override it only when a reviewed replacement sample is required for a changed Plan Copy contract.
2. Review the supported columns and value mappings in `references/eligibility-reference.md#eligibility-profiles`.
   Profile Usage accepts every enabled product in the ADE-backed
   `BEN_BNFT_CAGR_PRTN` list, by display name or code, including Opportunity
   Marketplace. Preserve the selected usage; do not substitute Benefits or
   reject a supported product because this skill is in the Benefits folder.
3. Use the selected target environment's OAuth properties and token cache. The workflow derives the target origin from `restBaseUrl`; it is not tied to a named environment or host. Do not place credentials or access tokens in the workbook, command, mappings, diagnostics, or project artifacts.
4. Generate the XML:

   ```bash
   /usr/bin/python3.11 \
     pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py convert-profiles \
     --input "<end-user-workbook.xlsx>" \
     --sample "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy/BEN_ELIGY_PRFL.xml" \
     --output "<project-artifact-directory>/BEN_ELIGY_PRFL.xml"
   ```

5. The converter reads `references/criterion-lookup-mappings.json`, which encodes the reviewed XML-field, common-lookup, and HCM object-LOV contracts for the supported workbook criteria. It accepts an exact lookup meaning or code for common lookups and writes the target code. Object LOVs populate paired XML values where Plan Copy requires both label and code, including termination reason, job family, collective agreement, and person type. Age, Compensation, Length of Service, Age and Service, Hours Worked, Full-Time Equivalent, Postal Code Range, and Service Area references must exactly match objects defined in their workbook tabs. Benefit Group criteria resolve as pre-existing target-pod dependencies through `benefitGroupsLOV`. There is no `--map-value` option.
6. Validate the generated XML and persist it as a preparation artifact before any package or mutating REST workflow.

Lookup resolution follows pagination, requests only active person types, applies the current active date to common lookups, exact-filters object names where supported, and retries authentication once on HTTP 401/403 through the shared OAuth client. Resolve Department from the date-effective `departments` collection with an exact `Name` query; do not use `departmentsLovV2`, whose contextual finder can omit otherwise visible departments. Resolution requires exactly one matching row unless the maintained declaration explicitly selects another policy. Department alone uses `multiple_match_policy: first`: duplicate exact active department names select the first row in Fusion response order and emit a warning. All other ambiguous or missing lookups fail closed before writing output. Person Type candidates are restricted to `SystemPersonType=EMP`; the workbook value is exact-matched against `UserPersonType`, and both fields are written from that lookup row. Duplicate active EMP rows remain ambiguous; `DefaultFlag` is not used.

This individual workflow writes XML and performs lookup-only Fusion GET requests. It does not create a Plan Copy ZIP, generate or validate `checksum.txt`, or invoke a mutating Fusion operation. Use the eligibility package workflow below for local package assembly. Live import remains a separate approval-gated activity.

## Convert Postal Code Ranges and Service Areas to Plan Copy XML

Read `references/eligibility-reference.md#postal-ranges-and-service-areas` before conversion.
The visible `Postal Code Ranges` tab creates a unique package-local range for
each `From Value` / `To Value` pair. The visible `Service Areas` tab groups
rows by Name and creates the child postal-range associations. Every child range
must be present in `Postal Code Ranges`; dates must be valid and fall within
both the parent Service Area and referenced postal range effective dates.

Use `BEN_PSTL_ZIP_RNG.xml` and `BEN_SVC_AREA.xml` only as structural samples.
The converter keeps the primary-key helpers null, writes the natural range and
service-area names, and resolves Service Type through the target pod's active
`BEN_PRDCT` `HCM_LOOKUPS` rows via read-only `genericLookups`. There are no
Plan Copy mapping rows for these package-local objects.

## Convert Age and Compensation Derived Factors to Plan Copy XML

Read `references/eligibility-reference.md#derived-factors` before converting
the maintained `Derived Factors - Age` and `Derived Factors - Comp` worksheets.
Use the byte-for-byte Oracle export samples at
`assets/plan-copy/BEN_AGE_FCTR.xml` and
`assets/plan-copy/BEN_COMP_LVL_FCTR.xml`.

Age to use, time unit, determination rule, and rounding rule resolve from their
exact active Fusion common lookups. Compensation source and determination
rules resolve from secured `HCM_LOOKUPS` types through the read-only
`genericLookups` REST resource, while Unit of Measure resolves through
`currenciesLOV`. Formula names and Benefit Balance names are validated as exact
target-pod dependencies before output. Missing or
ambiguous external dependencies fail closed before package creation; no guessed
IDs, manual mapping rows, or cross-pod values are emitted.

The converter creates `BEN_AGE_FCTR-converted.xml` and
`BEN_COMP_LVL_FCTR-converted.xml`, keeps the new-object primary keys null, and
preserves the exported flag contracts. Formula and Benefit Balance references
are written by their validated natural names with null key-helper ID fields.

## Convert Additional Derived Factors to Plan Copy XML

Read `references/eligibility-reference.md#derived-factors` before converting
the maintained `Derived Factors - LOS`, `Derived Factors - Age and LOS`,
`Derived Factors - Hours Worked`, and `Derived Factors - FTE` worksheets. Use
the convention-named Oracle-exported samples in `assets/plan-copy`.

Resolve Length of Service units and rounding plus Hours Worked rounding through
active `commonLookupsLOV` rows. Resolve the HCM-owned `BEN_LOS_DET`,
`BEN_LOS_DT_TO_USE`, `BEN_HRS_WKD_SRC`, `BEN_FREQ`, and `BEN_HRS_WKD_DET`
types through active `genericLookups` `HCM_LOOKUPS` rows. Validate every formula
and every Benefit Balance dependency through the
corresponding read-only REST collection. Age and Service factors must reference
package-local Age and Length of Service factor names. Full-Time Equivalent `Assignment to Use` accepts only
`Primary Assignment` or `Sum of all assignments`, which deterministically
populate the two exported assignment flags. Missing, ambiguous, or cross-tab
dependencies fail before any artifact is written.

## Generate the Eligibility Plan Copy Map

Generate `BEN_PL_COPY_MAP.xml` after the eligibility workbook passes the same lookup preflight. Read `references/eligibility-reference.md#plan-copy-map` for the complete mapping-row contract.

1. Supply the end-user workbook selected during intake. Use the bundled structural sample at `assets/plan-copy/BEN_PL_COPY_MAP.xml` and maintained mapping references at `references/eligibility-profile-mapping-reference/`.
2. Keep the sample immutable and write a separate output file.
3. Run:

   ```bash
   /usr/bin/python3.11 \
     pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py convert-map \
     --input "<end-user-workbook.xlsx>" \
     --sample "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy/BEN_PL_COPY_MAP.xml" \
     --mapping-reference-dir "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/references/eligibility-profile-mapping-reference" \
     --output "<project-artifact-directory>/BEN_PL_COPY_MAP.xml"
   ```

4. The generator joins `mapping-reference.json:criteria_mapping`, `mapping-reference.json:criteria_resolver_links`, and `mapping-reference.json:rest_api_resolvers` to derive `TableName`, `ColumnName`, `SrcTableName`, and the exact REST ID field. It emits rows for populated eligibility criteria classified `REQUIRED`, deduplicates shared logical sources, and fails closed on catalog disagreement. Benefit Group and Benefit Balance references are resolved as existing target-pod dependencies and are not created by this skill.
5. `SrcId` and `TrgId` use the exact ID returned by the selected target pod. `SrcName` and `TrgName` use its display name. Pre-resolve both target fields so the import requires no manual mapping, while deduplicating shared logical sources before packaging. `CompObjId` defaults to the maintained static value, and `CompObjType` is always `ELIG`.

This map workflow is also lookup-only. It does not modify the source map sample, eligibility XML, ZIP package, or checksum.

## Generate All XML Files and the Plan Copy Package

Use the eligibility generator when the validated `Fusion_Elpro_Setup.xlsx` and convention-named Oracle-exported XML samples are available. Supply one `--samples-dir`; it defaults to this skill's `assets/plan-copy` directory. The generator creates Eligibility Profile, Postal Code Range, Service Area, Plan Copy Map, Age, Compensation, Length of Service, Age and Service, Hours Worked, and Full-Time Equivalent XML, then creates `benefits_eligibility.zip`.

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py generate \
  --input "<end-user-workbook.xlsx>" \
  --samples-dir "pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/assets/plan-copy" \
  --output-dir "<work-directory>"
```

The outer ZIP contains ten ordered batch ZIPs plus `MIGRATOR_PROPERTIES.xml`: PlanCopyMap, PostalCodeRange, ServiceArea, AgeFactor, LengthOfServiceFactor, CombinedAgeLosFactor, CompensationLevelFactor, HoursWorkedFactor, FullTimeEquivalentFactor, and EligibilityProfile. The generator cross-validates every workbook-local factor, Postal Code Range, and Service Area dependency. Benefit Group and Benefit Balance references must already exist on the target and resolve through their REST resources. It validates every XML root, nested ZIP CRC, outer ZIP CRC, and exact member layout before atomically replacing output. Package creation performs read-only lookup GET requests only and sends no Plan Copy write.

## Submit and Monitor the Eligibility Plan Copy Import

The Benefits-owned native adapter is
`pillars/hcm/benefits-configuration/benefits-common/scripts/benefits_plan_copy.py`.
This skill declares that adapter as its Benefits Plan Copy project import
route after package generation. The adapter delegates task-context and
package validation to this skill and the core Data Loader Task Hook, and
uses the maintained core OAuth, REST, and ESS clients for execution.
Do not require a native Plan Copy route in the ordinary core Data Loader
uploader or report its absence as a catalog or metadata mismatch. This is
a Benefits-owned REST import route, not an HDL/DAT upload route. Retain
the preview, immutable-artifact checks, and existing import approval gates.
Pass the existing `--zip`, explicit `--effective-date`, generated
`--task-context` and its `--sequence`, OAuth `--properties` and `--token-cache`,
and `--preview-output`. This route supplies the maintained OpenAPI contract
and delegates native package validation and Task Hook preview to this skill.
Do not send the nested package through the ordinary DAT/UCM uploader.
After a later standalone approval, use the same native route and unchanged
archive/date with `--approve-upload --approval-preview <saved-preview>`.
Do not regenerate the package or use the combined workbook launcher for that
approved submission. The native route verifies approval-bound integrity and
Run Book context without repeating reference lookups. The legacy standalone
launcher examples below remain compatibility documentation, not an alternate
project import entry point.

Read `references/eligibility-reference.md#import-and-recovery` and the
`references/plan-copy.openapi.json` OpenAPI document before execution. Invoke
`scripts/eligibility.py` for the combined generation and import
workflow, or invoke `scripts/eligibility.py import` in preview mode when the ZIP
already exists.

The reusable launcher accepts the workbook directly:

```bash
/usr/bin/python3.11 \
  pillars/hcm/benefits-configuration/benefits-eligibility/eligibility-profiles/scripts/eligibility.py \
  --input "<end-user-workbook.xlsx>" \
  --effective-date "<YYYY-MM-DD; defaults to today>" \
  --work-dir "<work-directory>" \
  --properties "core/auth/fusionEnv.properties" \
  --token-cache auto \
  --task-context "<existing-task-context.json>"
```

The launcher requires `--work-dir` (or `BENEFITS_WORK_DIR`) and writes all
generated artifacts beneath that caller-selected directory. It consumes the bundled convention-named XML sample directory, mapping
references, and Plan Copy OpenAPI document from this skill. The launcher
derives the target origin from the OAuth properties `restBaseUrl`. An optional
`--target-origin` must match that configured origin. Existing generated artifacts block replacement unless the caller
supplies `--force` after reviewing the overwrite.

The importer validates the OpenAPI document,
the exact nested ZIP, OAuth target identity, and the existing Run Book task
context, then routes through the required Data Loader Task Hook to write an
immutable local approval preview. Preview mode sends no Fusion request.

Stop after preview and require a later standalone user message exactly
`approve`. Only then rerun with `--approve-upload` and the exact saved preview.
Because the approved run deterministically regenerates the local package, add
`--force` to authorize replacement of the previously generated local XML and
ZIP files. Reuse every target, input, and authentication argument from the
preview command.
The importer revalidates the OpenAPI and archive hashes before its first
write. It then displays a concise summary containing the exact target, ZIP name,
size and SHA-256, import name, effective date, eligibility profile, Postal Code
Range, Service Area, Age factor, and Compensation factor names,
per-profile criterion counts, criterion object types and counts, supporting
Plan Copy mapping-row count, all six derived-factor inventories, and complete import action. The same object
inventory is stored in the immutable preview. The importer requires the user to
type exactly `approve`; any other input stops before any Plan Copy POST or PUT.
After approval it creates metadata with `RequestSource: "FDOS"`, uploads the
ZIP enclosure, and submits `generateMappings`. For this request source, that
single ESS request performs mapping generation and the import; never call
`submitImport`. After the ESS request completes, verify that no source mapping
is unresolved and refresh the final Plan Copy parent through REST. ESS success
is necessary but is not the final application result. The
importer reports success only when the REST parent reaches
`ImportPlDesign=12`; `ImportPlDesign=10` is an application error even when the
ESS request says `SUCCEEDED`. After the parent is terminal, it downloads
`enclosure/RequestLogs`, which exposes the consolidated import log stored in
`BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2`. Any recognized log error overrides
ESS or parent success, and an empty log cannot confirm success. User-facing
progress and results show the approved Plan Copy name instead of its internal
ID, omit the ESS request ID and status, and expose only a `SUCCESS` or `ERROR`
status derived from `MappingRequestStatus`. Failed results also include the
sanitized error details extracted from `RequestLogs`. Server-issued IDs and
raw statuses remain internal recovery evidence. The importer sends REST
framework version 9 on all Fusion requests.

The selected target environment's OAuth `restBaseUrl` supplies the runtime origin; the REST
contract is deliberately host-neutral. The ZIP must have been generated using
lookups from that same environment. Mapping PATCH is not part of the contract:
unresolved mappings are a blocking catalog mismatch and are never auto-patched.

### Import Error Handling

The importer classifies failures using the repository taxonomy, preflights all
inputs before the first write, preserves every available Plan Copy and ESS
request ID, and reports a recommended recovery action. Its default wait is 1800
seconds with a 10-second poll interval; timeout exits without resubmission.
Live POST and PUT calls are never retried automatically. A read-only GET may
refresh a rejected cached OAuth token once. Output redacts authorization,
password, client-secret, and access-token values and never emits the ZIP body.

On an application error, retrieve the consolidated log through the Plan Copy
`RequestLogs` REST enclosure and show its recognized error lines with the final
error. Use the REST child log collection as supplemental detail. If REST does
not expose enough evidence, a configured read-only database diagnostic connector may be used
only as an explicit diagnostic follow-up. It must be a strict read-only connection,
not an import dependency. In `BEN_PL_COPY_PARAMS`, `PARAM_ATTRIBUTE_BLOB1` is
the uploaded ZIP package and `PARAM_ATTRIBUTE_BLOB2` is the consolidated import
log; never attempt to change either value.

ESS terminal and success states are normalized case-insensitively. Preserve the
Plan Copy ID and mapping/import ESS request ID internally after a partial
failure, but do not display them in conversational progress or results. Do not
create a replacement import without a new preview and explicit approval.

Exit codes are `0` for preview/live success, `1` for validation, auth,
transport, Fusion API, approval, or persistence failure, `2` for OpenAPI or
mapping mismatch, `3` for polling timeout, and `4` for terminal process
failure. After any partial live failure, retain the reported IDs and do not
submit a replacement without a new immutable preview and approval.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_elpro_setup_xlsx`: end-user-supplied `.xlsx` attachment or accessible local path, required for workbook-based preparation.
- `plan_copy_xml_samples_directory`
- `eligibility_mapping_reference_directory`
- `fusion_environment_context`
- `plan_copy_openapi_document`
- `task_context`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `eligibility_profile_xml`
- `age_factor_xml`
- `compensation_level_factor_xml`
- `length_of_service_factor_xml`
- `combined_age_length_of_service_factor_xml`
- `hours_worked_factor_xml`
- `full_time_equivalent_factor_xml`
- `plan_copy_map_xml`
- `plan_copy_import_archive`
- `plan_copy_import_preview`
- `plan_copy_import_result`
- `plan_copy_import_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.benefits-configuration.benefits-eligibility` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
