---
skill_id: "cx.customer-data-management.trading-community-foundation.import-trading-community-data"
name: "Import Trading Community Data"
description: "Imports user-supplied Trading Community CSV files unchanged through Oracle CX Import Management, without validating their columns or row data. Also generates or validates CSVs when explicitly requested. Supplied CSVs may contain any number and names of columns, including columns absent from the bundled samples."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "CUSTOM_IMPORT_TRADING_COMMUNITY_DATA"
task_name: "Import Trading Community Data"
dataloader_import_mode: "CXIMPORT"
businessObject: ""
type: "import"
execution_mode: "hybrid"
owner_team: "CX Customer Data Management pillar team"
version: "2.5.5"
inputs:
  - "project_context"
  - "target_fusion_environment"
  - "exact_import_object"
  - "exact_import_mode"
  - "optional_parent_object_for_generation_or_explicit_validation"
  - "optional_volume_mode_for_generation_or_explicit_validation"
  - "source_records_or_csv"
  - "requested_record_manifest"
  - "import_activity_name"
  - "execution_approval"
outputs:
  - "unchanged_supplied_csv_or_generated_csv"
  - "optional_redacted_csv_validation_report"
  - "immutable_import_preview"
  - "ucm_upload_summary"
  - "cx_import_activity_result"
  - "import_status_and_diagnostics"
  - "post_import_verification"
  - "request_instance_verification_ledger"
  - "campaign_completion_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.customer-data-management.trading-community-foundation"
  - "core.data-loader"
  - "core.fusion-api.cx-import-export-management"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.data-loader"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ucm-rest-client"
  - "core.fusion-api.cx-import-export-management"
  - "core.fusion-api.ess-job-submitter"
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
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Input and CSV contract checks"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Import dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Object, operation, parent, and volume rules"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Safe import defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Preview, deletion, and live-execution gates"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure classification and recovery"
    location: "ora-resource/ora_error_handling.md"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Creates local CSV files outside the tracked project workspace and may persist redacted validation and run metadata."
  - "Uses the core CX adapter to upload an explicitly approved immutable CSV group and create or activate one Import Management activity."
  - "Creates and may activate one explicitly approved CX Import Management activity with the exact selected ImportMode."
  - "Literal deletion and semantic inactivation/removal require separate destructive approval."
required_privileges:
  - "Access to the exact target Oracle Fusion environment and required OAuth scope."
  - "Privileges to upload to the target-metadata-resolved UCM document account."
  - "CX Import Management privileges for the selected object and operation."
  - "Object-specific delete or update privileges for destructive operations."
---

# Import Trading Community Data

## Purpose

Prepare and execute one governed CX Import Management activity for one exact Trading Community object. Support CSV generation and validation, immutable preview, approved submission, bounded monitoring, diagnosis, and post-import verification. Asset, Asset Contact, and the UI-labeled Asset Team Member object are supported; their exact target codes are `Assets`, `AssetContact`, and `AssetResource`.

## Required reading

1. Read `references/object-profiles.json` only to resolve the exact Import Management object code and post-import verification strategy.
2. Read all six `ora-resource` files and compile/use `ora_rule_registry.json` through Task Hook.
3. Read `core/data-loader/SKILL.md`; it owns source transport review, the canonical immutable digest, Task Hook validation, and approval authorization before any import adapter runs.
4. Read `core/fusion-api/rest-api-client/SKILL.md` and its routed Fusion REST reference before resolving live object metadata or verifying records.
5. Read `core/fusion-api/cx-import-export-management/SKILL.md` and its required reference before mode-aware execution or monitoring.
6. Only when the user asks to generate a CSV or explicitly validate its data, also read `references/column-contracts.json`, `references/field-contracts.json`, and the matching template under `assets/templates/`.

## Selection gates

- For every supplied or generated CSV, select exactly one Import Management
  object code and one exact job-level `ImportMode` without inspecting supplied
  data rows. `ImportMode` is routing metadata, not a CSV field-validation result.
  Do not infer it from the supplied filename, columns, or values.
- The remaining selection gates apply only to generation or an explicit
  data-validation request. Never infer `Account` from `Organization`, or
  `Contact` from `Person`; ask the user to choose because their generated import
  contracts are functionally different.
- Select exactly one allowed parent for a child object. `Household` is a parent identity only and is not a top-level object supported by this skill.
- Reject missing, ambiguous, or unsupported operations. Treat `update`,
  `create-or-update`, or `create and update` as `CREATE_RECORD`, `create` as
  `CREATE_ONLY`, and
  literal `delete` as `DELETE_RECORD`. Bind the exact code into the immutable
  preview and the live Import Management activity.
- Enforce `fixed-high` for Classification Code, Hierarchy, and Hierarchy Member. Enforce `fixed-low` for Resolution Link and Resolution Link Member. Other profiles may use low or high volume; use the profile default unless the user chooses otherwise.
- Hierarchy and Hierarchy Member generation or explicit data validation support
  create, update, and delete. Their update route uses `CREATE_RECORD`; their
  delete route uses `DELETE_RECORD`, identifier-only rows, exact-target checks,
  destructive approval, and optional post-generation absence reconciliation.
  For an unchanged supplied CSV, do not apply those row-level checks: require
  exact-object `ImportSupport=Y`, bind `DELETE_RECORD` in the approved preview,
  and let Fusion Import Management accept or reject the rows.
- Additional Identifier generation/validation supports create, update, and
  delete. Delete uses the exact `PartyIdentifierId` as its only CSV field and
  routes the activity as `DELETE_RECORD`. Require one exact parent-scoped
  pre-delete match, destructive approval, and zero exact post-import matches.
- Treat Resolution Link `LinkStatus=I` and Resolution Link Member `MemberStatus=I` as semantic destructive actions performed with `CREATE_RECORD`. Treat Source System Reference `DELETE_RECORD` as semantic inactivation rather than physical removal.
- Treat Asset `DeleteFlag=Y` as semantic soft deletion performed with `CREATE_RECORD`; it requires destructive approval independently of literal `DELETE_RECORD`.
- For Asset Contact and Asset Team Member, require the explicit `Asset` parent. Submit the exact target codes `Assets` for Asset and `AssetResource` for Asset Team Member; do not derive either code from its display name.

## Prepare and validate CSV

### Supplied CSV pass-through import

When the user supplies a CSV and asks to import it, treat every data CSV as an
opaque payload. Do not invoke `prepare_tca_import_csv.py`; do not parse, inspect,
normalize, validate, repair, or rewrite its header or row data. Do not compare
its columns with bundled samples, downloaded templates, column contracts, field
contracts, or live attributes. Accept any column count, names, order, and data,
including more columns than a sample, fewer columns, or no overlap with a
sample. Preserve the exact bytes through approval and upload.

For this pass-through branch, check only transport and routing facts: the path
exists, the file is a nonempty `.csv`, group basenames are unique
case-insensitively, at most one file is an authoritative CX mapping CSV, at
least one file is a data CSV, and an exact Import Management object code can be
resolved. Also require the exact job-level `ImportMode` from explicit user
intent or an already reviewed workflow artifact. If the object code is not
explicit and no mapping CSV supplies it, ask for the CX Business Object code.
If the mode is missing or ambiguous, ask whether the job is `CREATE_ONLY`,
`CREATE_RECORD`, or `DELETE_RECORD`. These are routing inputs, not CSV data
validation. Do not ask for a validation waiver. Fusion Import Management is the
authority that accepts or rejects the supplied data after submission.

### Generation or explicit data validation

Only when the user asks this skill to generate a CSV or explicitly asks to
validate its data, use `scripts/prepare_tca_import_csv.py`; do not hand-build the
generated file. The following contracts and examples apply only to that branch
and must never block import of a supplied CSV.

The stored contracts deliberately distinguish three concepts:

- `required_for_create_by_skill` is the minimum requirement enforced for a create operation, supplemented by conditional object rules.
- `identity_set_membership` shows alternative keys used by create-or-update or delete; one complete supported set is required.
- `metadata_required` is Oracle REST/import metadata and is descriptive. Do not blindly require every such field because Fusion can generate some fields or satisfy identity requirements through alternatives.

List the supported profile matrix:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py profiles
```

Inspect all fields, types, lengths, and requiredness for one object:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py fields \
  --object "Contact"
```

Inspect only the skill-required create fields or one exact column:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py fields \
  --object "Hierarchy" --required-only

python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py fields \
  --object "Account" --column PartyNumber
```

Generate a minimal child-object template:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py template \
  --object "Address" --parent-object Organization --operation create-or-update \
  --volume high --output /secure/work/address.csv
```

Prepare a validated file from synthetic-shaped JSON records:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/prepare_tca_import_csv.py prepare \
  --object Organization --operation create --records-json /secure/input/organizations.json \
  --output /secure/work/organization.csv --report /secure/work/organization.report.json
```

Use `--full` only when every downloaded-template column is needed. For `prepare`, include optional exact-header fields in the source records; for `template`, use `--column ExactHeader`. The redacted report contains no row values; it records object, parent, operation, derived import flags, file metadata, headers, SHA-256, destructive status, verification strategy, and warnings.

For `LinkedParty`, resolve the exact target-active `LinkType` codes before preparing or validating rows and pass them through `--target-values-json`. The file must remain outside `project/` and use this redacted contract:

```json
{
  "objectCode": "LinkedParty",
  "source": "fusion-runtime",
  "fields": {"LinkType": ["target-active-code"]}
}
```

Do not translate a business label into a code from memory or preserve a previously observed environment's value as a universal default. The validator rejects a `LinkedParty` file when runtime `LinkType` evidence is absent or the row value is not in the supplied target-active set. Its report records only the validated field names, not the allowed-value payload.

## Preflight

For a supplied CSV pass-through import, preflight only the exact environment,
OAuth session and upload privileges, explicit object and `ImportMode` routing,
current UCM account, authoritative `ImportSupport=Y`, immutable ordered
CSV-group SHA-256, mode-aware adapter readiness, and approval freshness. Do not
inspect or validate headers, fields, row values, lookups, identities, parents,
duplicate risk, or volume. Selecting the job-level mode does not authorize
inspection of the supplied CSV.
In particular, never require, inspect, or request a waiver for
`PartyUsageCode`. A field that is absent from the CSV is not a local blocker.
Present that the data content was not inspected and will be evaluated by Fusion.

For an explicit supplied `Hierarchy` or `HierarchyNode` delete, do not inspect
the CSV for PartyId, PartyNumber, parent identity, AsOfDate, identifier-only
rows, or a pre-delete match. The exact object, `DELETE_RECORD` mode, immutable
file group, environment, UCM account, activity, and destructive approval define
the authorized scope. Fusion Import Management evaluates the row data.

For generated CSVs or an explicit data-validation request, apply the remaining
object-specific checks in this section before execution.

If the user reports that their login, roles, or privileges changed, force one fresh OAuth login before interpreting a successful-but-empty Import Management object lookup. Retry only that read-only lookup once. Treat a still-empty result as a catalog or authorization blocker; do not substitute a neighboring object code. Access to CRM object metadata or the Import Management object picker does not prove authorization to upload through ERP Integration Service to the resolved UCM account.

For `LinkedParty` create, verify the main party has `SALES_PROSPECT` or `SALES_ACCOUNT` usage and the related party has the distinct financial `CUSTOMER` usage. Resolve `LinkType` from the exact target and validate it through `--target-values-json`; a user-facing label is not submission evidence. Do not treat Account type `ZCA_CUSTOMER` or usage `SALES_ACCOUNT` as evidence of financial `CUSTOMER` usage. If the financial usage is absent, stop and route creation of the financial customer account through its owning workflow before preparing or submitting the link.

For Account create/update, pass active lookup codes such as `ZCA_PROSPECT` and `ZCA_CUSTOMER`, never display meanings such as `PROSPECT` or `CUSTOMER`. Permit an existing Account identified by PartyNumber or source-system keys to change type without repeating an unchanged address. If any address field is being changed, require the complete address bundle. Explain that `ZCA_CUSTOMER` results in sales `SALES_ACCOUNT` usage and does not establish financial `CUSTOMER` usage.

For Source System Reference create/update, omit `Status`; the target import contract rejected a populated `Status` even though the downloaded template exposed the column. Use the selected profile's `DELETE_RECORD` path for semantic inactivation. Before retrying any source-system reference create, query the exact party, source system, and reference value because an earlier submission may already have succeeded.

For Asset create, require `AssetNumber` plus an existing asset-owner identity: `CustomerId`, `CustomerPartyNumber`, or `AccountSourceSystem` with `AccountSourceSystemReference`. Also require either `ProdGroupId` or the complete `InventoryItemId` plus `InventoryOrgId` pair; resolve the chosen product identity from the exact target. Validate all supplied source-system pairs together. For Asset Contact create, require `AssetId` or `AssetNumber` plus a contact identified by `ContactPartyId`, `ContactPartyNumber`, or the complete contact source-system pair. For Asset Team Member create, require `AssetId` or `AssetNumber` plus `ResourceId` or `ResourcePartyNumber`. Resolve asset, contact, resource, product, product-group, business-unit, currency, UOM, status, and function codes against the exact target when supplied.

## Core-service boundary

Keep Trading Community object selection, optional CSV generation/validation,
metadata interpretation, approval orchestration, verification rules, and result
redaction in this skill. Supplied data CSVs cross this boundary unchanged and
receive no pillar data validation. Use `core.fusion-api.rest-api-client` for
authenticated read-only metadata and verification calls. Use
`core.data-loader` for mandatory source review, canonical digest, Task Hook
validation, and approval authorization. After those gates pass, use
`core.fusion-api.cx-import-export-management` as the mode-aware execution and
monitoring adapter; it must create the activity with the exact approved
`ImportMode`.

This skill uses `core.data-loader` as the governing preview and approval
workflow, not as the generic live `initiateDataLoad` adapter. Trading Community
templates and field catalogs remain local and are consulted only for generation
or an explicit data-validation request.

Core Data Loader resolves the CX UCM account from the exact target object's live metadata. Retain `scripts/resolve_tca_ucm_account.py` only for read-only reconciliation or diagnostics that must compare slash and dollar forms. Store raw service responses only in a secure temporary location and never display or persist encoded document content.

## Preview and execution workflow

1. Resolve the exact environment, Import Management object code, exact
   `ImportMode`, supplied CSV group, import activity name, and privileges. Do
   not parse supplied data CSVs to infer these values. Refuse a missing or
   ambiguous mode.
2. For supplied CSVs, freeze the exact bytes without data inspection or transformation. For generation or explicit validation, run the applicable helper and then freeze the result. Any byte, source order, mapping, object, mode, or environment change invalidates approval.
3. Resolve current object metadata and `UcmAccount` with the core REST client from `GET /crmRestApi/resources/11.13.18.05/objectMetadata/{ObjectCode}?fields=UcmAccount&onlyData=true`. Separately confirm the same exact code through the `importExportObjectMetadata` `objectRowFinder` and require `ImportSupport=Y`; do not substitute a neighboring code when it is absent. Normalize the metadata UCM account's slash form to UCM `$` form with the skill-local resolver. Do not ask the user to supply or override it.
4. Skip data-dependent lookup, parent, mapping, and volume checks for supplied
   CSVs. Select and validate only the job-level `ImportMode`; do not inspect CSV
   data to infer or confirm it. Apply object dependencies only when generating
   data or when the user explicitly requests data validation. Do not add a
   hierarchy member target-resolution exception for supplied CSV deletes.
   For a new Resolution Link campaign, create and verify `DedupLink` first, capture its generated `LinkNumber`, then prepare a separately approved `LinkMember` activity. Require exactly one master across the new link's requested members. Use `Y`/`N` in the import CSV and verify the REST `MasterFlag` as boolean `true`/`false`.
5. Enter `core.data-loader` and run `upload_and_initiate.py <csv>
   --cx-import --cx-import-object-code <ObjectCode>
   --preflight-envelope-output <secure-temp>/preflight.json`, omitting
   `--task-routed`, `--approve-upload`, and `--task-validation-envelope`.
   Core owns source transport review and may persist its reviewed ZIP outside
   `project/`. Its `archiveSha256` identifies that ZIP, not the ordered CSV
   group. Preserve source basenames and bytes; do not upload this ZIP or use its
   digest as the CX execution digest. Mapping CSVs remain unsupported by the
   protected adapter: record the gap and stop before approval.
6. Run the Core CX adapter's `prepare-import` with the exact ordered local CSVs
   and settings shown below, saving its review output outside `project/`.
   Reconcile the two Core review artifacts with the skill-local helper:

   ```bash
   python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/reconcile_tca_import_preview.py \
     --preflight <secure-temp>/preflight.json \
     --adapter-preview <secure-temp>/adapter-preview.json \
     --object-code <ObjectCode> --import-mode <CREATE_ONLY|CREATE_RECORD|DELETE_RECORD>
   ```

   The helper checks the Data Loader envelope and ZIP digest, exact ordered
   filenames and file bytes against the protected adapter manifest, and target,
   object, mode, and UCM account. It never parses data CSV headers or rows,
   extracts a ZIP, computes a replacement group digest, or grants approval.
   Treat a failed reconciliation as an `approval_blocker`; rerun the applicable
   Core previews after correcting the mismatch. Different ZIP and group digests
   are expected because they identify different representations.
   After reconciliation, use only the adapter-returned `manifest.groupSha256`
   in Task Hook's compatibility `finalData.archiveSha256` field. Retain the
   Data Loader ZIP digest separately as `finalData.dataLoaderArchiveSha256`.
   `finalData` must also bind the exact environment, object code, `ImportMode`,
   import activity name, ordered filenames, UCM account, activation, schedule,
   and `core.fusion-api.cx-import-export-management` execution adapter. Include
   the protected manifest, `approvalId`, and `reviewSha256` in the review.
   Present the ordered filenames, group digest, target, object, mode, and
   activity. For supplied CSVs, state that data content was not inspected.
   Never invoke the physical-archive verifier for the CSV group, independently
   reconstruct its digest, or submit through generic `initiateDataLoad`.
   Stop once for exact-artifact execution approval, showing destructive effects
   for `DELETE_RECORD` or semantic inactivation/removal. This approval authorizes
   both the matching Task Validation envelope and the protected Core adapter
   approval; do not ask again for the same execution.
7. Record that explicit approval using
   `cx_import_export_job.py approve-import --approval-id <id> --review-sha256 <reviewed-digest>`.
   The authority is the owner-private store outside the project, not mutable
   `finalData`, a self-hash, or an editable Task Validation envelope. Approvals
   expire after 15 minutes by default and cannot be reused or renewed.
8. Invoke the supported Core CX adapter; do not call or wrap its Python
   implementation. Use the exact approved ordered data CSVs, object, mode,
   activity name, UCM account, activation, and schedule; `--import-mode` is required.
   Never call the generic Core Data Loader `initiateDataLoad` route because it
   does not bind the Import Management `ImportMode`.
   Bare `create-import --execute` and `upload-ucm --execute`
   are disabled. Core owns OAuth, UCM transport, diagnostics, and returned IDs.

   ```bash
   python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py execute-approved-import \
     --approval-id <approved-id> \
     --name <approved-activity-name> \
     --object-code <ObjectCode> \
     --import-mode <CREATE_ONLY|CREATE_RECORD|DELETE_RECORD> \
     --upload-file <approved.csv> \
     --ucm-document-account '<resolved-account>' \
     --activate YES \
     --schedule ONE_TIME_IMMEDIATE \
     --token-cache auto
   ```

   Use `prepare-import` with these same arguments (without `--approval-id`)
   for the step-6 preview. Repeat `--upload-file` in the approved order for
   multiple data CSVs. Mapping CSVs remain unsupported: record the workflow gap
   and stop, without substituting another upload route. Execution opens each
   source once, compares bytes/order/settings against the protected approval,
   consumes that approval atomically, confirms the current fixed environment
   and exact object account, and uploads only the verified in-memory bytes.
   Any byte, membership, order, object, mode, activity name, environment, UCM
   account, activation, or schedule change invalidates approval.
   Capture the redacted receipt in the project workspace. A failed attempt
   spends the approval; reconcile partial uploads and activity status before
   seeking new authorization, and never replay an uncertain write.
9. Capture the returned UCM document name and `ImportActivityId`, then stop after
   accepted activity creation/activation. Return a compact import receipt with
   activity ID and name, exact object and mode, activation, schedule, filename,
   UCM document name, and current data-file status. Persist that receipt under
   the project workspace so the user can say `check status` later without
   repeating an ID. Never display the adapter's raw upload response, encoded
   source content, UCM search metadata, or null-filled REST payload.

   When the user subsequently requests status, resolve the latest applicable
   activity ID from project state when the request omits it. Run the CX
   adapter's `get-import --import-activity-id` route and require its parent
   activity response to report the same exact `ObjectCode` and `ImportMode`.
   Then run
   `scripts/get_tca_import_status.py` with the approved object code and
   `ImportMode`. This task-local helper uses the existing core REST client to
   fetch both the parent activity and its `child/DataFiles` collection. The
   parent must report the same exact `ObjectCode` and `ImportMode`; a missing or
   mismatched value is not successful evidence of the requested operation.
10. For a supplied CSV, report Fusion's activity mode, status, and counts without
    parsing the CSV to discover verification keys. Report the child data-file
    `Status`, `ReadFromFile`, `LoadedSuccessfully`, `ErrorsReported`, `Warnings`,
    and `Unprocessed` values, plus start/end timestamps. Include available error,
    exception, and success report content IDs for terminal outcomes. Never infer
    status from a parent-only response that omits these fields. When errors are
    nonzero and `ErrorReportContentId` is available, immediately run
    `scripts/get_tca_import_report.py --content-id <ErrorReportContentId>` and
    include every distinct Fusion business diagnostic in the same status
    response. The report helper returns only error type, message, and diagnostic
    comment; it does not expose or persist source rows.
    `ImportMode=DELETE_RECORD`
    plus a successful activity proves that Fusion processed the job in delete
    mode; it does not by itself prove that a specific target record is absent.
    Perform record-level verification only when the user supplied the needed
    identities separately. For generated or explicitly validated records,
    verify by the profile strategy and exact identities. Do not equate a loaded count,
    generic Data Loader success, or UI-search visibility with target
    verification, and do not resubmit without exact reconciliation.
11. Build the request-instance ledger only when request identities were supplied independently or the skill generated the records. Never inspect an opaque supplied CSV to manufacture that manifest. Every manifest entry must end as `completed_and_verified`, `failed_no_record_created`, `deferred`, `not_submitted`, or `unknown_requires_reconciliation`.

Build and validate the ledger from redacted request and outcome files:

```json
{
  "environment": "nonproduction-environment-alias",
  "requests": [
    {
      "request_id": "address-account-1",
      "object_code": "Address",
      "intended_mutation": "created",
      "parent_ref": "account-request-1",
      "source_reference_supplied": true,
      "expected_match_count": 1
    }
  ]
}
```

Each outcome uses the same `request_id` and exact `object_code`. A `completed_and_verified` outcome supplies `mutation`, `import_activity_id`, `ucm_content_id`, `process_counts`, and `verification` with `exact_match_count`, `target_record_ids`, `state`, plus `parent_identity` or `source_reference` when the request requires them. Non-completed outcomes require a reason. The utility rejects duplicate outcomes and outcomes for unknown or semantically different requests; a request with no outcome becomes `unknown_requires_reconciliation`.

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/import-trading-community-data/scripts/build_tca_verification_ledger.py \
  --request-manifest /secure/work/requests.json \
  --outcome /secure/work/outcomes.json \
  --output /secure/work/verification-ledger.json
```

The ledger distinguishes `created`, `updated`, `deleted`, `inactivated`, and
`none`. Never count an update as a create or a physical deletion as an
inactivation. Never use a Relationship or Account Contact outcome to satisfy a
Linked Party request, and never use an Account-to-Contact association to
satisfy an Account-to-Account link. Account/Organization and Contact/Person
remain distinct functional objects. Account type `ZCA_CUSTOMER` or usage
`SALES_ACCOUNT` remains distinct from financial `CUSTOMER` usage.

## Verification branches

- `sales-account`: confirm exact party identity plus active sales profile, `PromotedFlag`, owner, and address state.
- `sales-contact`: confirm exact party identity, sales-contact state, and intended Account/Household association.
- `party-usage`: confirm exact party identity and intended Organization/Person usage without treating it as Account/Contact.
- `child-with-parent` or `relationship`: confirm the child/relationship and its exact parent, subject, and object identities.
- For an Additional Identifier delete, query the selected party's
  `AdditionalIdentifier` child by the approved `PartyIdentifierId` and require
  zero exact matches. A completed activity or loaded row is not deletion proof.
- `asset`: confirm the exact `AssetId`/`AssetNumber`, owner identity, product or product-group identity when supplied, status, and `DeleteFlag` state.
- `asset-child`: confirm the exact Asset parent plus the Asset Contact or Asset Team Member record ID, referenced contact/resource identity, function, and primary/owner flag.
- `hierarchy-post-process`: when separately requested and the necessary
  identities are supplied, run and verify Party Hierarchy Generation after a
  successful Hierarchy or Hierarchy Member import, then reconcile
  tree/version/member state. For delete, zero exact target matches provide
  record-level absence evidence; loaded-row counts alone do not.
- Treat Party Hierarchy Generation as a separate ESS mutation routed through `core.fusion-api.ess-job-submitter`. Resolve and preview the exact job definition and parameters after the hierarchy import succeeds, and obtain a fresh approval; approval of the CSV import does not authorize an as-yet-unresolved ESS request.
- `resolution-link` and `resolution-link-member`: confirm link status, membership, and master/member semantics, including inactive status after a semantic removal. Verify Link Members through REST-supported fields `LinkNumber`, `PartyId`, `PartyNumber`, `MasterFlag`, and `MemberStatus`; `DedupLinkMemberId` is an import/update identity and must not be requested from the Link Member REST collection.
- `exact-identity`: query the exact imported identifier and verify the intended field state.

Apply the exact locator and identity requirements in `references/object-profiles.json` for every branch. A terminal import activity with loaded rows is process evidence only. Completion requires the exact expected target match count, generated target identifier evidence, and the intended created, updated, or inactivated state. If exact target reconciliation is ambiguous, use `unknown_requires_reconciliation`; do not claim completion or submit another mutation.

For `LinkedParty`, resolve the parent from `hubOrganizations` by `PartyNumber` and use that returned item key in `/hubOrganizations/{PartyNumber}/child/LinkedParty`. Do not substitute the numeric `PartyId` in that item-key position. Verify the related party, target-resolved `LinkType`, `MainLink`, status, and active dates before changing the ledger entry to `completed_and_verified`.

## Diagnostics and persistence

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`. Treat an uncertain Core adapter result as an approval blocker, not as permission to replay a write. On timeout, report environment, object, activity ID, last status, and elapsed wait; use the Core adapter's read-only status route rather than resubmitting.

Keep source rows, generated CSVs, downloaded reports containing row data, credentials, and tokens outside `project/`. When a project exists, persist only redacted validation reports, immutable-preview metadata, run status, external IDs, diagnostics, verification evidence, and token usage at the declared workspace paths.

## Maintain the field catalog

When Oracle changes the Import Management templates, download all 25 supported object ZIPs from the exact target-family environment and regenerate the local assets and contracts with `scripts/build_tca_field_contracts.py`. Supply the current CRM REST describe plus current Account and Contact object-metadata attribute payloads. For objects whose REST describe doesn't cover every import field, supply UI metadata captured from Import Objects with `--ui-metadata-dir`. Use repeatable `--object` arguments for a scoped incremental refresh. The generator validates every ZIP, preserves each Oracle two-row CSV under `assets/templates/`, records SHA-256 values, and fails if any template column has no authoritative data type. Review generated diffs and rerun all skill tests before handoff.
