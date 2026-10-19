---
task_code: "CUSTOM_MANAGE_ASSET_LIFECYCLE_MANAGEMENT_DEFAULTS"
task_name: "Manage Asset Lifecycle Management Defaults"
parent_skill_id: "cx.subscriptions.integration-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "subscriptionAssetIntegrationDefaultValues"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Asset Lifecycle Management Defaults

## Setup Task Metadata

- Task name: `Manage Asset Lifecycle Management Defaults`
- Task code: `CUSTOM_MANAGE_ASSET_LIFECYCLE_MANAGEMENT_DEFAULTS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `subscriptionAssetIntegrationDefaultValues`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Asset Integration Default Values REST Workflow

The task's resource is:

```text
/crmRestApi/resources/latest/subscriptionAssetIntegrationDefaultValues
```

Use the active Fusion environment's base URL. The URL supplied by a requester is
an environment-specific example, not a value to copy into runbooks or source
data.

### Supported Methods

- `GET` is allowed to retrieve the currently configured subscription asset
  integration default values.
- `PATCH` is allowed only to update existing default values.
- `POST`, `PUT`, and `DELETE` are not allowed for this task. Do not use them to
  create, replace, or remove asset-integration defaults.

### Read Existing Defaults

For a read-only review, route the request through
`core.fusion-api.rest-api-client`:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /crmRestApi/resources/latest/subscriptionAssetIntegrationDefaultValues \
  --method GET
```

Treat the response as the live source of truth for the available attributes,
their current values, and the resource's patch shape. Do not infer attributes,
keys, or a PATCH body from this metadata file or from another environment.

### Resolved Default Display

When displaying an Asset Lifecycle Management default, show the stored code and
its live display value. Resolve lookup-backed values; do not display an opaque
code as its only value and do not retain a previously resolved display label as
the source of truth.

1. GET the default-value resource and retain its `DefaultValueCode`. This is
   the item identifier for the LOV routes; do not substitute `DefaultValueId`.
2. GET the resource `describe` endpoint before first use in an environment and
   stop if the expected LOV mapping is absent or has changed.
3. For every populated field below, GET
   `/crmRestApi/resources/latest/subscriptionAssetIntegrationDefaultValues/{DefaultValueCode}/lov/{LOV resource}`
   and filter by the matching source attribute. Render the returned display
   attribute alongside the stored code.

| Stored field | LOV resource | Match field | Display field |
| --- | --- | --- | --- |
| `BusinessUnitName` / `BusinessUnitId` | `BusinessUnitVA` | `BuId` | `BuName` |
| `SubscriptionProfileId` | `SubscriptionProfileVA` | `SubscriptionProfileId` | `SubscriptionProfileName` |
| `CloseReason` | `CloseReasonVA` | `LookupCode` | `Meaning` |
| `CancelReason` | `CancelReasonVA` | `LookupCode` | `Meaning` |
| `CloseCreditMethod` | `CloseCreditMethodVA` | `LookupCode` | `Meaning` |
| `TransferOption` | `AssetTransferOptionVA` | `LookupCode` | `Meaning` |
| `WarrantyUpgradeOption` | `WarrantyUpgradeOptionVA` | `LookupCode` | `Meaning` |
| `CoverageUpgradeOption` | `CoverageUpgradeOptionVA` | `LookupCode` | `Meaning` |

If a stored value is null, display `Not set` and do not call its LOV. If a LOV
response does not return exactly one matching active value, show the stored code
with `Lookup label unavailable`, record a redacted diagnostic, and do not infer
or substitute a label. The lookup routes are read-only and do not authorize a
PATCH.

### Update Existing Defaults

Use `PATCH` only for an explicitly requested update of an existing value.

1. Retrieve the current defaults with `GET` and confirm the target environment,
   resource identity, patchable attributes, and current values.
2. Build the smallest valid PATCH body from the live representation. Do not
   include a field that is not present and patchable in that representation.
3. Persist an immutable preview containing the exact endpoint, redacted body,
   target environment, and before/after values under the active project
   workspace.
4. Obtain explicit approval immediately before the PATCH request.
5. Invoke the request only through `core.fusion-api.rest-api-client`. Record a
   redacted result or diagnostic; do not automatically retry a failed PATCH.

This REST route does not authorize Data Loader upload, CSV task import, or any
create/delete operation for Asset Lifecycle Management.

## Usage

Use this metadata file when planning, reviewing, or updating existing asset
integration default values for `Manage Asset Lifecycle Management Defaults` under `Integration
Setup`.
