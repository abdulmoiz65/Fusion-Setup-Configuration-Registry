---
task_code: "CUSTOM_MANAGE_USER_GROUPS"
task_name: "Manage User Groups"
parent_skill_id: "hcm.learning-management.learning-audience"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Audience"
functional_area_code: "ORA_LEARNING_AUDIENCE"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningOrganizations"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage User Groups

## Setup Task Metadata

- Task name: `Manage User Groups`
- Task code: `CUSTOM_MANAGE_USER_GROUPS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `learningOrganizations`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `learningOrganizations` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "learningOrganizations" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Create, update and duplicate review

A new root POST omits `learningOrganizationId`,
`learningOrganizationNumber` and `status`; do not ask for generated values or
an existing-parent no-match result. Title is not a documented uniqueness key,
so this skill does not claim to prove that two new groups have distinct business
purposes. Never silently switch POST to upsert or replay an uncertain load.

For existing groups, resolve the supplied ID or number and retain the returned
opaque parent item key. Child reads and duplicate checks use that exact key,
not the numeric ID. Loader linkage remains governed by live loader metadata.

Handle the input the user provides: a name/Username reference resolves to
PersonId through the core client; a supplied PersonId is validated through core.
Neither has precedence. If both were independently supplied without an explicit
selection, ask which to use; do not compare them or choose automatically. A
PersonId returned by name resolution is output, not a second user input. The
existing name route accepts exact Fusion Username; request that identifier if
the supplied name is only a display name. Show the selected input's final
PersonId with `ORA_PERSON` in preview. Invalid or mismatched IDs prompt a
correction; unverified reads require clarification, not a guessed person. Resolver mechanics live in
[reference lookups](ora-resource/ora_reference_lookups.md).

Check proposed criteria within the request and, for existing parents, against
all returned child pages. Duplicate identity is the same parent, child role,
sourceType and sourceId. Manager and participant roles remain distinct; PATCH
excludes only its own criteriaId. New parents require no pre-create child GET;
verify the returned parent and children after the approved load. These checks
do not provide a server-side uniqueness constraint against concurrent writes.
Release/build is optional, not an intake gate.

## Existing-Parent Criteria Loads

Use `core.data-loader` first. Resolve the existing parent and retain its exact
returned `@context.key`; never assume that the numeric
`learningOrganizationId` is the complete item key.

If both a child-only load and a parent-PATCH-plus-child load fail with
object-level `Not Found`, and read-only verification proves that the numeric
item route fails while the returned composite item route succeeds, classify
the result as a Data Loader registration mismatch. Do not retry another loader
artifact with the same key registration.

Only after that mismatch is established and the user explicitly requests the
fallback, create a new `managerCriteria` or `participantCriteria` row by sending
`POST` through `core.fusion-api.rest-api-client` to the exact returned composite
parent's child collection. A create is not a PATCH: PATCH requires an existing
`criteriaId`. Before the POST, re-resolve the parent, re-run the applicable
duplicate check, show the exact environment, method, relative path and JSON
body, and obtain explicit approval for that payload. Stop after the first
response and verify the child collection with GET; never retry an uncertain
POST automatically.

If Fusion rejects that POST with `Person doesnot have the required privilage`
or another authorization denial, classify it as auth/authz. Do not retry or
alter the payload. Read the same child collection to verify whether anything
was created, then ask for the calling Fusion identity to receive the required
Learning user-group criterion create privilege or for an already-authorized
identity to be selected. A subsequent retry requires a fresh duplicate check,
payload preview and approval.



## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage User Groups` under `Learning Audience`.
