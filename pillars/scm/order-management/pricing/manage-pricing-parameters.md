---
task_code: "ORA_QP_MANAGE_PRICING_PARAMETERS"
task_name: "Manage Pricing Parameters"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "qpParameterValues"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---
# Manage Pricing Parameters
## Setup Task Metadata
- Task name: `Manage Pricing Parameters`
- Task code: `ORA_QP_MANAGE_PRICING_PARAMETERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `qpParameterValues`
## Read-Only Parameter Lookup
Use `core.fusion-api.rest-api-client` for all read-only Pricing Parameter Value
requests. Use the standard Fusion REST path
`/fscmRestApi/resources/11.13.18.05/qpParameters/{pricingParametersUniqID}/child/qpParameterValues`.
Resolve the parent `pricingParametersUniqID` before the request; do not upload
or initiate a load for this read request.

## Route Enforcement

For this task, route all reads through `core.fusion-api.rest-api-client`; do not
use Data Loader for a standard Fusion REST GET. Resolve the parent Pricing
Parameter identifier and request its `qpParameterValues` child collection. Do
not use a direct client or bypass the selected core workflow.
## Export, Data Loader, and Validation Workflow
`CSVExportImportSupportedFlag` is `Y` for this task. Use the REST API client for
reads and Data Loader for create and update work:
1. Read current task data with `core.fusion-api.rest-api-client` using the
   parameterized `qpParameterValues` child path.
2. For a create or update, use `core.data-loader` with the registered
   `qpParameterValues` REST Data Loader business object. Do not prepare an FSM
   export/import ZIP as the default create/update route.
3. Have Data Loader validate the live business-object schema, prepared source,
   immutable upload artifact, task rules, and approval gates before execution.
Use this task metadata when invoking those skills:
- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Parameters`
- Setup task code: `ORA_QP_MANAGE_PRICING_PARAMETERS`
## Mandatory Route
Use these routes for Pricing Parameter operations:

- `core.fusion-api.rest-api-client` for get/read operations at
  `/fscmRestApi/resources/11.13.18.05/qpParameters/{pricingParametersUniqID}/child/qpParameterValues`.
- `core.data-loader` with `qpParameterValues` for create and update operations.

Before a Data Loader submission, confirm that `qpParameterValues` is registered
in the target environment, then show the exact target environment and immutable
upload artifact. Require explicit approval immediately before submission. Do
not retry a failed or uncertain import without an idempotency-safe recovery path
and new approval.

## Download Fusion Data Loader Sample

1. Confirm that `qpParameterValues` is the exact registered Data Loader business object.
2. Generate the editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "qpParameterValues" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the editable, attribute-details, and key-fields workbooks together and
   use the editable workbook as the source for the later Data Loader workflow.
## Usage
Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Pricing Parameters` under `Pricing`.
