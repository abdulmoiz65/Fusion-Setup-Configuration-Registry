# Custom Catalog Layer

The custom catalog adds custom offerings, custom functional areas, and custom
tasks to the effective catalog. Use `core.fusion-dev.custom-task-gen` rather
than editing these files directly.

Custom offerings are stored in `Offerings_catalog.json` and require a `Pillar`.
Custom functional areas are stored in `Functional_areas_catalog.json` and
require `Pillar`, `OfferingCode`, and `OfferingName`. A custom offering can
contain release, pre-release, or custom functional areas when the effective
catalog validates their context.

Custom tasks are stored in `setupTasksAll.json` using all release task fields
plus this required ownership context:

```json
{
  "TaskCode": "CUST_EXAMPLE_TASK",
  "TaskName": "Manage Example Configuration",
  "AvailableFlag": "Y",
  "ExportImportSupportedFlag": "N",
  "CSVExportImportSupportedFlag": "N",
  "Pillar": "ERP",
  "OfferingCode": "XLE_FINANCIALS_JUR",
  "OfferingName": "Financials",
  "FunctionalAreaCode": "ORA_ASK_LEGAL_STRUCTURES",
  "FunctionalAreaName": "Legal Structures"
}
```

`Pillar`, `OfferingCode`, and `FunctionalAreaCode` are validated against the
effective hierarchy. The name fields must match the corresponding catalog
records. A custom task can target an existing functional area or a custom
functional area. A custom functional area can contain release, pre-release,
or custom tasks when the effective catalog validates their context.

Existing release or pre-release tasks can be associated with a custom offering
or functional area through `Existing_task_associations.json`. These records
retain the source `TaskCode` and `TaskName` and add the same pillar, offering,
and functional-area ownership context; they must not be copied into
`setupTasksAll.json` as custom tasks.

After a change, `core.fusion-dev.custom-task-gen` automatically materializes the
effective offering → functional area → task hierarchy and refreshes the
hierarchy browser's static data bundle. Do not edit the custom catalog files
directly.
