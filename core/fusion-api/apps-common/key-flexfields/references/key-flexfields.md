# Key Flexfields (KFF)

## Purpose

Use this reference when a pillar setup-task skill routes a Key Flexfield (KFF)
task to `core.fusion-api.apps-common.key-flexfields`. This route manages
task-level KFF setup data through the supported CSV export and FSM CSV import
workflows; it does not implement its own Fusion REST transport.

Examples include:

| Task code | Task name |
| --- | --- |
| `INV_MANAGE_INVENTORY_ACCOUNT_ALIAS_KEY_FLEXFIELD` | Manage Inventory Account Alias Key Flexfield |
| `FND_MANAGE_KEY_FLEXFIELDS` | Manage Key Flexfields |
| `FA_MANAGE_FIXED_ASSETS_KEY_FLEXFIELDS` | Manage Fixed Assets Key Flexfields |
| `INV_MANAGE_INVENTORY_LOCATOR_KEY_FLEXFIELD` | Manage Inventory Locator Key Flexfield |
| `PAY_MANAGE_KEY_FLEXFIELD_FOR_COST_ALLOCATION` | Cost Allocation Key Flexfield |

## Eligibility Gate

1. Obtain the calling pillar task skill's exact task code, task name, offering,
   functional-area, and a positive task sequence. If any identifier is missing
   or conflicts, stop with `input_validation`; do not choose a task by name
   alone.
2. Use `shared.setup-export.task-level-export` to resolve the authoritative
   task code, functional area, and offering from the calling skill metadata,
   live task lookup when available, or
   `knowledge/setup-task-catalog/release/setupTasksAll.json`.
3. Check the resolved task's `ExportImportSupportedFlag`. If it is not `Y`, do
   not start a KFF setup-data export or import. Report the resolved task
   metadata and that this KFF CSV route is unsupported.
4. The task-level export workflow also enforces its required
   `CSVExportImportSupportedFlag` check before it creates a CSV export. Do not
   bypass that shared-workflow gate.

## Export KFF Setup Data

Delegate export to `shared.setup-export.task-level-export`. That shared skill
owns task-code resolution, CSV setup-task export, polling, download, and
project-workspace persistence.

1. Pass the calling KFF task's exact task code or task name, offering, and
   functional-area context.
2. Let the shared skill confirm the exact task and supported flags.
3. Let it export the CSV setup data and persist the ZIP or process log under:

   ```text
   project/{project_id}/exports/{offering}/{functional-area}/{task-name}
   ```

4. Return the exported artifact reference, `ProcessId`, outcome, and
   diagnostics to the calling pillar skill.

Use normal data-export mode for a configuration baseline. Use template/spec
mode only when the caller explicitly requests a KFF CSV template rather than
current KFF setup data.

## Import KFF Setup Data

Delegate import only to `core.data-loader` using the FSM CSV Import route.
This is a configuration-changing operation.

1. Resolve the task code, task name, offering, functional area, and positive
   sequence from the calling pillar skill context. Reapply the eligibility gate
   before accepting the import.
2. Require a nonempty, valid ZIP produced for the resolved KFF task. It must
   contain the exact-case member `ASM_SETUP_CSV_METADATA.xml` plus the task CSV
   files. Preserve the ZIP bytes unchanged.
3. Route the request to `core.data-loader` with:

   | Data Loader input | Required value |
   | --- | --- |
   | `requested_operation` | `FSM CSV Import` |
   | `task_context` | Resolved task code, exact task name, and positive sequence (in the Task Hook context) |
   | `data_load_source_or_registered_business_object` | The validated FSM ZIP path |
   | `fusion_environment_context` | Confirmed target Fusion environment |

4. Let Data Loader classify the immutable ZIP as FSM, perform its Task Hook
   validation and approval-preview lifecycle, upload the approved archive, and
   initiate the Fusion import. A standalone approval applies only to the exact
   reviewed archive; do not submit it before that confirmation.
5. Return Data Loader's completion result and diagnostics to the calling pillar
   skill. Once the import has completed successfully, enter **REST Deployment
   and Status** for the imported KFF. Do not deploy after an incomplete or
   failed import, and retain the REST deployment approval gate.

## Boundaries

Use only `shared.setup-export.task-level-export` for KFF CSV export and
`core.data-loader` for KFF FSM CSV import. Do not route imports to
`shared.setup-import.task-level-import`, invoke `setupTaskCSVImports` directly,
or duplicate authentication, CSV transport, Task Hook validation, or Data
Loader approval handling. Classify an unsupported flag as
`catalog_or_metadata_mismatch` and an unapproved import as `approval_blocker`.

## REST Deployment and Status

Use this workflow only to deploy an already-configured KFF. Use
`core.fusion-api.rest-api-client` and its standard `fusion_rest_client.py`
route; `/fscmUI/applcoreApi` requires the default Fusion `scope`.

| Operation | Method and endpoint |
| --- | --- |
| Submit deployment | `POST /fscmUI/applcoreApi/latest/flexfields/metadata/deploy/{application_id}/KFF/{url_encoded_flexfield_code}` |
| Get deployment state | `GET /fscmUI/applcoreApi/latest/flexfields/metadata/getDeploymentState/{application_id}/KFF/{url_encoded_flexfield_code}` |

The documented KFF example uses application ID `101`, code `GL%23` (for
`GL#`), and payload `{"forceDeployment":"true"}`. Accept only the documented
string values `"true"` and `"false"` for `forceDeployment` until Oracle
publishes a different contract. If the calling skill does not specify the
value, send `{"forceDeployment":"false"}`.

Obtain explicit approval immediately before the POST. Record `jobId`,
`jobStatus`, `deploymentStatus`, `validationStatus`, `validationReport`, and
`deploymentErrorMessage`. For a status request, invoke the GET endpoint with
the exact same identifiers. When polling is requested, use a 10-second
interval and a 300-second maximum wait; treat `DEPLOYED` as successful and
stop for any terminal non-success status or reported deployment error.
