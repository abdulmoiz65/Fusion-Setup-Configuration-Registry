---
skill_id: "erp.financials.legal-structures.manage-legal-jurisdictions"
name: "Manage Legal Jurisdictions Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Legal Jurisdictions under the Legal Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Legal Structures"
functional_area_code: "ORA_ASK_LEGAL_STRUCTURES"
task_code: "XLE_MANAGE_LEGAL_JURISDICTIONS"
task_name: "Manage Legal Jurisdictions"
parent_skill_id: "erp.financials.legal-structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "ERP financials pillar team"
version: "0.1.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "jurisdiction_name_optional"
  - "territory_optional"
  - "legislative_category_optional"
  - "legal_entity_registration_code_optional"
  - "legal_reporting_unit_registration_code_optional"
  - "identifying_flag_optional"
  - "effective_from_optional"
  - "effective_to_optional"
  - "legal_functions_optional"
  - "required_etb_flag_optional"
  - "required_le_flag_optional"
  - "active_optional"
  - "attribute_category_optional"
  - "jurisdiction_code_optional"
  - "legal_function_required_flag_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "territory_lov"
  - "remaining_required_lovs"
  - "guided_clarification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.rest-api-client"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.data-loader.task-hook"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-jurisdictions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-jurisdictions/current/"
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
  - "Reads current Fusion geography and lookup LOVs through the OAuth-backed REST client."
required_privileges: []
---

# Manage Legal Jurisdictions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Legal Jurisdictions` under `Legal Structures`.

## Setup Task Skill Contract

- task_code: `XLE_MANAGE_LEGAL_JURISDICTIONS`
- task_name: `Manage Legal Jurisdictions`
- parent_skill_id: `erp.financials.legal-structures`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Legal Structures`
- functional_area_code: `ORA_ASK_LEGAL_STRUCTURES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Legal Jurisdictions` under `Legal Structures`.

## Callable Reference Discovery Adapter

This task owns a read-only Fusion REST discovery adapter. It is not dependent
on a separately registered generic lookup adapter and must not claim that no
safe lookup route exists when a create request is missing values.

Use `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` with the
standard OAuth cache. Territory discovery and hierarchy enrichment use only
`addressGeographies`, with explicit `REST-Framework-Version: 9` on every GET.
Follow the projection-safe retrieval protocol in ora_reference_lookups.md;
retain identity and enrichment receipts, with complete pagination.

| Purpose | Route |
|---|---|
| Territory identities, countries, and hierarchy enrichment | `/crmRestApi/resources/11.13.18.05/addressGeographies` |
| Legislative Category | `/fscmRestApi/resources/11.13.18.05/standardLookups/LEGISLATIVE_CATEGORY/child/lookupCodes` |
| Legal Entity Registration Code | `/fscmRestApi/resources/11.13.18.05/standardLookups/XLE_REG_CODE/child/lookupCodes` |
| Legal Reporting Unit Registration Code | `/fscmRestApi/resources/11.13.18.05/standardLookups/XLE_REG_CODE_EST/child/lookupCodes` |
| Optional Legal Function | `/crmRestApi/resources/11.13.18.05/fndStaticLookups` using `LookupTypeIsActiveEnabledFinder` with `BindLookupType=XLE_LE_FUNCTION` |

For a partial create request, retain all valid supplied fields. Territory is a
searchable LOV: when supplied, search it directly; Country is an optional
narrowing attribute, not a prerequisite. When Territory is missing, return the
first bounded LOV page and ask for a Territory search term or optional Country
narrowing. Once one visible Territory row resolves, return all remaining
required choice lists in one response; do not request Legislative Category and
registration codes one at a time. Legal Functions are optional.

## Mandatory Guided-Input Response Contract

This contract applies automatically to every incomplete create request; it
does not require a user to request LOV discovery explicitly. Do not export a
template, generate a package, or ask for a code before returning the required
choice table(s).

Mirror the Territory UI using addressGeographies identity discovery followed
by hierarchy enrichment. Countries and local geographies come from this same
endpoint. When Territory is missing, show the first bounded page and request a
Territory search term; Country remains optional. Do not scan the global
catalogue to answer a supplied search term.

### Projection-Safe Territory Retrieval

Use the complete protocol in ora_reference_lookups.md. The identity projection
is `GeographyIdentifierId,CountryCode,GeographyValue,GeographyType,
PrimaryGeographyFlag,LanguageCode,StartDate,EndDate`, with `onlyData=true`.
Do not request lower hierarchy fields during identity discovery: projecting
those fields can suppress COUNTRY and shorter-hierarchy records.

For a supplied search, use `GeographyValue LIKE '<escaped-territory>%'` and
retrieve all pages through `hasMore=false`. An exact text match never replaces
this prefix retrieval. Do not add CountryCode during automatic discovery,
even if a country can be inferred. Explicit user narrowing of delivered choices
remains supported. Identity-bound enrichment may use the retained country,
exact value, and type to scope its reads; it must not change the discovery set.

Preserve every eligible discovered identity. COUNTRY rows need no lower-level
query; display GeographyValue as the first Name. For non-country rows, probe
levels 2, 3, and 4 separately, then retrieve a coherent tuple using only the
levels proven available for that identity. Do not force level 4 onto a level-3
place. Correlate by GeographyIdentifierId and country/type/value, never by name
alone. A projection that omits an identity does not erase it or establish that
it does not exist. Keep unavailable levels blank with their probe receipts;
never shift levels, invent hierarchy, or combine unrelated level variants.
If populated levels cannot be jointly reconciled, stop with a hierarchy gap.

### Primary Territory Eligibility Gate

Require PrimaryGeographyFlag=true for the identity and its enrichment rows.
For each populated displayed level 2, 3, or 4, require its matching
PrimaryGeographyLevelNFlag=true from the coherent tuple. Request a level flag
only with that level's value. Blank/unavailable levels need no primary flag,
but require the completed level-probe evidence; a failed read is not absence.
Exclude a row with any applicable explicit false flag before delivery,
counting, matching, deduplication, or import. Accept Boolean true/false and
explicit true/false or Y/N strings case-insensitively. Missing, null, or unknown
required flags on an otherwise eligible row require a re-read of the affected
projection and then a metadata-gap stop if unresolved; never infer truthiness.

Preserve existing date eligibility. Retain raw, primary-eligible, excluded,
and unresolved counts and reasons. Keep source IDs internally, not in choices.
Deduplicate eligible coherent visible tuples only after primary filtering;
sharing an identifier is not permission to retain an alternate hierarchy.
An explicitly supplied alternate requires selection from the primary choices,
not silent rewriting. A missing hierarchy result must not downgrade a discovered
non-country identity into a country or a less specific identity.

### Territory Choice Delivery Gate

Discovery requires retrieval and delivery. After required pages and enrichment
complete, display the same five business-visible columns:

| Territory | Geography Type | Name | Name | Name |
|---|---|---|---|---|

Map countries to GeographyValue in the first Name. Map non-country hierarchy
levels 2 through 4 to the three Name columns in their original positions.
Do not expose IDs, CountryCode, primary flags, or technical metadata. Preserve
every eligible discovered identity; exclude only proven alternates or ineffective
rows. Never reduce a multi-candidate result to a preferred country or exact row.

Show all eligible candidates inline through 50. Above 50, show the first 50,
state the total, and write/link the complete Markdown table in this task's
artifact directory. A progress count, malformed five-column header, single-row
confirmation, or omitted list is not delivery. Request selection by visible
Territory, Geography Type, and Name values; never request an internal ID.

### Territory Resolution Gate

Require completed identity pagination and all applicable enrichment receipts,
including q, fields, Framework Version 9, page counts, final hasMore, retrieval
time, source identities, primary decisions, and unavailable-level evidence.
With no search, retain the bounded-page scope explicitly. A read failure,
partial page, unknown primary eligibility, or unreconciled hierarchy blocks
resolution; do not call code LOVs, prepare a package, or substitute an endpoint.

Free text resolves automatically only when the eligible deduplicated set has
one visible candidate and one source identity. Multiple candidates require the
complete table and an explicit visible-row choice; multiple identities behind
a visible tuple require refinement. Never select by list order or country
preference. Reuse valid supplied choices and resolve them against retained
receipts. Preserve eligible exact matches; rank non-exact suggestions by
normalized prefix/token similarity, capped at 20.

`selection_required` is valid only with the eligible candidate count, complete
inline table or required full-list link, and visible-row selection request.
Otherwise record choice-delivery failure and return to discovery.

Only after the Territory Resolution Gate is `resolved`, retrieve **every page**
of every remaining required LOV. Do not use the first item, a cached example,
or a partial endpoint response. If any required LOV is unavailable or partial,
return no remaining LOV table and stop the guided flow.

After the user selects exactly one Territory, return all still-missing choices
in the *same response*, each as a Markdown table:

| Required selection | Required columns |
|---|---|
| Legislative Category | Choice |
| Legal Entity Registration Code | Choice |
| Legal Reporting Unit Registration Code | Choice |
| Legal Function (optional) | Choice |

Populate `Choice` with one row for every eligible UI-displayed dropdown value.
Do not use semicolon- or comma-separated lists. Do not expose
internal codes, duplicate Meaning columns, enabled flags, or effective-date
metadata in the guided response; retain those values internally for lookup
validation and package generation.

### Remaining-LOV Delivery Gate

`LJ.DISCOVER_LOVS` may return `listed` only after all four independent tables
have been delivered: Legislative Category, Legal Entity Registration Code,
Legal Reporting Unit Registration Code, and optional Legal Function. Every
table must state its retrieved eligible count and contain one ordinary Markdown
row per `Choice`; `<br>`-separated values, a single first choice, or one
combined “required list” table is a partial response, not a successful list.

Display every choice inline through 50 rows per table. If any table has more
than 50 choices, display its first 50 rows inline, state the total, and write
and link a complete Markdown table for that specific LOV in the current task's
Legal Jurisdictions artifact directory. The linked artifact supplements the
inline rows; it does not allow omission of a required table. A failure to
retrieve, page, render, or link any required table is `lov_delivery_failed`:
stop and do not ask the user to choose, validate the request, or prepare an
import.

If Identifying Flag is missing, include this required table in the same
response. Do not default it or infer it from current setup data:

| # | Identifying Flag | Meaning | Required |
|---|---|---|---|
| 1 | Y | Identifying jurisdiction | Yes |
| 2 | N | Non-identifying jurisdiction | Yes |

If either effective date is missing, include this optional-date prompt in the
same response: _Effective From and Effective To are independently optional.
Provide either or both in `YYYY/MM/DD` format, or explicitly confirm that a
missing date should remain blank. When both are supplied, Effective From must
not be later than Effective To._ Do not synthesize a date or require a date
solely because it was omitted.

Only after the user supplies the remaining required selections may the task
export a template, validate package readiness, or prepare an import. Optional
dates may remain blank only after the user has supplied them or explicitly
confirmed omission. A template-export failure must not replace, suppress, or
defer a complete LOV response.

## Reusable Technical Defaults

Apply `ora-resource/ora_defaulting_rules.md` for creates: RequiredEtbFlag and
RequiredLeFlag blank, Active Y, AttributeCategory blank, JurisdictionCode equal
to the exact Name, and Legal Function RequiredFlag Y. Explicit valid user values
take precedence, including explicit blanks where permitted. These defaults do
not depend on existing jurisdiction data and do not overwrite omitted update
attributes. Verify current FSM structure and validate overrides before preview.

## Independent Create Preparation

A fresh same-target template/spec export, including a header-only package, is
sufficient for the package baseline when its metadata and structure pass. Do
not require a populated full-data export or an existing jurisdiction to derive
the documented defaults or populate new business values. Live reference and
name checks remain mandatory; the two geography-dependent checks follow the
conditional exclusion policy below. These are validation, not default sources.

## FSM Geography Carrier Handling

Use the selected Territory hierarchy and retained endpoint receipt to populate
the current FSM template. Preserve those values and the template fingerprint in
the readiness record. Missing canonical geography-code, geography-use, or first-level hierarchy fields
from addressGeographies must be recorded as a warning, not a
blocker: continue package preparation, validation, and the normal explicitly
approved import path. Do not copy business values from existing jurisdiction
data rows in an export.

## Error Handling and Redaction

Apply `ora-resource/ora_error_handling.md` and the repository error-handling
guidelines to every lookup, export, validation, import, poll, and failure path.
Persist or report only the minimum diagnostic metadata needed to investigate a
run: environment identity, endpoint path, HTTP status, retrieval time, result
count, page state, request/process identifiers, artifact path, and a redacted
error summary.

Never print, place in a project artifact, package into a ZIP, or commit OAuth
access or refresh tokens, token-cache contents, credentials, client secrets,
cookies, Authorization headers, private keys, or full base64 `FileContent` /
archive payloads. Redact sensitive Fusion response fields and customer setup
values from diagnostics; preserve only safe identifiers and field names where
they are necessary for remediation. This documentation adds no new side effect
and does not alter the existing approval, validation, or import flow.

## Setup Task Metadata

- Task name: `Manage Legal Jurisdictions`
- Task code: `XLE_MANAGE_LEGAL_JURISDICTIONS`
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

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Legal Structures`
- Setup task name: `Manage Legal Jurisdictions`
- Setup task code: `XLE_MANAGE_LEGAL_JURISDICTIONS`

## Mandatory Task Hook Submission Contract

Before any Legal Jurisdiction archive is uploaded or initiated, invoke
`core.data-loader.task-hook` for the active task context and sequence. The
Task Hook validation envelope is mandatory; a successful ZIP or workbook
preflight does not replace it.

- Obtain the planned rule resources from the active Task Hook task plan at
  submission time. Do not hard-code, manually assemble, filter, or reorder the
  list.
- Create exactly one `ruleResults` object for every planned resource, in the
  plan's returned order. Each object must contain `source`, `status`, `issues`,
  and `changes`; its `source` must exactly match the corresponding planned
  resource filename.
- Build the preview with the final Data Loader preflight data, including the
  exact archive hash. Approve and verify that preview through Task Hook before
  passing its raw validation envelope to `core.data-loader` for upload.
- If Task Hook reports a rule-resource mismatch, stop before upload and
  regenerate the complete ordered `ruleResults` set from the current active
  plan. Never bypass the hook, reuse a stale envelope, or submit a partial
  result set.

This rule governs orchestration only; it does not change Legal Jurisdiction
field values or import content.

## Two Checks Deferred When Canonical Geography Mapping Is Unavailable

For a create with a uniquely selected, primary-eligible Territory, defer only
these two pre-import checks when the supported read-only endpoint cannot verify
the selected source identity's relationship to a canonical GeographyId:

1. Existing jurisdiction with the same GeographyId and LegislativeCategoryCode.
2. Existing identifying jurisdiction for that GeographyId and the impact of
   the supplied IdentifyingFlag.

Record each excluded check as not_applicable with a warning and reason
canonical_geography_mapping_unavailable. Disclose that Fusion will enforce the
geography/category rule and apply identifying behavior during import. Do not ask
for a separate waiver, require allowReadinessOverride, or label the checks passed.
Retain the source receipts and exact selected primary hierarchy; never guess a
GeographyId, equate it with GeographyIdentifierId, or use unrelated jurisdictions
to infer the selected geography. Do not scan the entire geography catalogue or
require a full-data export merely to make these two checks executable.

When verified mapping is available, run both checks normally; known conflicts
still block under existing rules. The exclusion is caused by mapping capability,
not automatically by the addressGeographies source. Missing/ambiguous Territory,
unknown primary flags, failed or incomplete lookup requests, name uniqueness,
input/code validation, dates, immutable-field and active-registration checks,
package structure, Task Hook preview, and import approval are not excluded.
This create policy does not authorize an unverified update to existing records.

Task Hook must retain both warnings in the applicable dependency/design resource
results and preview. A resource may be passed only when all its other applicable
checks pass; keep the two individual excluded checks explicitly not_applicable
in its evidence. Do not mark the entire resource not_applicable or overridden.
After submission, review the actual Data Loader errors and FSM ProcessLog before
quoting success or failure. Reconcile any rejected or indeterminate import before
preparing a separately validated and approved retry; never replay automatically.

## Geography Verification Limits

Territory text can name different geography records in the same endpoint.
Resolve the selected visible tuple and source identity, preserving its country,
type, and hierarchy; never convert a selected local geography to a same-named
country. addressGeographies supplies country and local identities; use the projection-safe
protocol without losing countries or shorter hierarchies.

GeographyIdentifierId from addressGeographies and GeographyId from
legalJurisdictionsLOV are different kinds of identifiers. Never substitute one
for the other, assume they are equal, or infer an ID by arithmetic. Use only a
verified relationship for ID-based duplicate checks. If that relationship is
unavailable for a valid create, apply the two-check exclusion policy above.

legalJurisdictionsLOV can verify existence and the persisted GeographyId. It
does not expose geography code, usage, or hierarchy carriers, so it cannot prove
that an omitted import field was stored blank rather than derived by Fusion.
Report successful omission as observed import behavior, not a universal schema
rule or a claim about stored values.

## Post-Import Status Verification

When the user asks for the status, outcome, errors, or completion result of a
Manage Legal Jurisdictions FSM import, retrieve the FSM ProcessLog along with
the Data Loader status. Do not report the jurisdiction as created solely from
successful-looking data-set counters. A ProcessLog status of `Completed with
warnings`, any `error` or CSV parsing message, or zero processed objects is a
failed or warning-blocked import: quote the reviewed actionable log finding and do
not claim that configuration was created.




Review the retrieved log file contents before reporting success or failure.
Quote a short exact outcome or actionable error line, with its log link, using
the task-local reviewed-log evidence format in ora-resource/ora_error_handling.md. Do not rely solely on a helper
status icon. When counters lag a completed log, perform one read-only status
refresh; disclose any remaining mismatch without resubmitting the import.

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

Use the parent functional-area skill `erp.financials.legal-structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
