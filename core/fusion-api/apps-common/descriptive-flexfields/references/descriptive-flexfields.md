# Descriptive Flexfields (DFF)

## Purpose

Use this reference when a pillar setup-task skill routes a Descriptive
Flexfield (DFF) task to `core.fusion-api.apps-common`. This route manages DFF
setup data through task-level CSV export and Data Loader FSM CSV import; it
does not implement its own Fusion REST transport or CSV process handling.

Examples include:

| Task code | Task name |
| --- | --- |
| `HZ_MANAGE_CUSTOMER_ACCOUNT_CONTACT_DESCRIPTIVE_FLEXFIELDS` | Manage Customer Account Contact Descriptive Flexfields |
| `WSH_MANAGE_SHIPPING_DESCRIPTIVE_FLEXFIELDS` | Manage Shipping Descriptive Flexfields |
| `EGP_ITEM_CLASS_DFFS` | Manage Item Class Descriptive Flexfields |

## Eligibility Gate

1. Obtain the calling task skill's exact `task_code`, task name, offering,
   functional-area, and positive task sequence. If any identifier is missing or
   conflicts, stop with `input_validation` rather than choosing a task.
2. Use `shared.setup-export.task-level-export` to resolve the authoritative
   task code, functional area, and offering from the calling skill metadata,
   the live task lookup when available, or the local task catalog at
   `knowledge/setup-task-catalog/release/setupTasksAll.json`.
3. Check the resolved task's `ExportImportSupportedFlag`. If it is not `Y`,
   do not start a DFF export or import. Report the task metadata and that this
   CSV-based DFF route is unsupported.
4. The task-level export workflow also enforces its required
   `CSVExportImportSupportedFlag` check before it creates a CSV export. Do not
   bypass that shared-workflow gate.

Do not infer eligibility from a task name alone. The examples above currently
have both flags set to `Y` in the local catalog, but each routed request must
perform the gate again against the resolved task.

## Export DFF Setup Data

Delegate export to `shared.setup-export.task-level-export`. That shared skill
owns task-code resolution, the CSV setup-task export request, polling,
download, and project-workspace persistence.

1. Pass the calling DFF task's exact task code or task name plus offering and
   functional-area context.
2. Let the shared skill confirm the exact task and supported flags.
3. Let it export the CSV setup data and persist the ZIP or process log under:

   ```text
   project/{project_id}/exports/{offering}/{functional-area}/{task-name}
   ```

4. Return the exported artifact reference, `ProcessId`, outcome, and
   diagnostics to the calling pillar skill.

Use the task-level export skill's normal data-export mode for a configuration
baseline. Use its template/spec mode only when the caller explicitly requests
a DFF CSV template rather than current DFF setup data.

## Import DFF Setup Data

Delegate import only to `core.data-loader` using the FSM CSV Import route.
This is a configuration-changing operation.

1. Resolve the task code, task name, offering, functional area, and positive
   sequence from the calling pillar skill context. Reapply the eligibility gate
   before accepting the import.
2. Require a nonempty, valid ZIP produced for the resolved DFF task. It must
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
   and Status** for the imported DFF. Do not deploy after an incomplete or
   failed import, and retain the REST deployment approval gate.

## Boundaries

Use only `shared.setup-export.task-level-export` for DFF CSV export and
`core.data-loader` for DFF FSM CSV import. Do not route imports to
`shared.setup-import.task-level-import`, invoke `setupTaskCSVImports` directly,
or duplicate authentication, CSV transport, Task Hook validation, or Data
Loader approval handling. Classify an unsupported flag as
`catalog_or_metadata_mismatch`, and an unapproved import as `approval_blocker`.

## REST Deployment and Status

Use this workflow only to deploy an already-configured DFF. Use
`core.fusion-api.rest-api-client` and its standard `fusion_rest_client.py`
route; `/fscmUI/applcoreApi` requires the default Fusion `scope`.

| Operation | Method and endpoint |
| --- | --- |
| Submit deployment | `POST /fscmUI/applcoreApi/latest/flexfields/metadata/deploy/{application_id}/DFF/{url_encoded_flexfield_code}` |
| Get deployment state | `GET /fscmUI/applcoreApi/latest/flexfields/metadata/getDeploymentState/{application_id}/DFF/{url_encoded_flexfield_code}` |

The documented DFF example uses application ID `0`, code `FND_VS_VALUES_B`,
and payload `{"forceDeployment":"false"}`. Accept only the documented string
values `"true"` and `"false"` for `forceDeployment` until Oracle publishes a
different contract. If the calling skill does not specify the value, send
`{"forceDeployment":"false"}`.

Obtain explicit approval immediately before the POST. Record `jobId`,
`jobStatus`, `deploymentStatus`, `validationStatus`, `validationReport`, and
`deploymentErrorMessage`. For a status request, invoke the GET endpoint with
the exact same identifiers. When polling is requested, use a 10-second
interval and a 300-second maximum wait; treat `DEPLOYED` as successful and
stop for any terminal non-success status or reported deployment error.
