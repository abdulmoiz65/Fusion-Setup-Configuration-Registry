# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM import package | Receive the package proposed for import |
| 2 | Retained FSM export baseline | Use the latest baseline supplied in setup_data_artifacts from core.data-loader FSM export when present; otherwise permit import without comparison |
| 3 | ORA_MSC_APPS_INSTANCE.csv inclusion | When a supplied FSM export baseline is present, require this file when either tracked source-system file changed from the baseline |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MSCPS.APPS_INSTANCE_FOR_ORG_CHANGE | ORA_MSC_APPS_INSTANCE.csv is included | Yes | ORA_MSC_INSTANCE_ORG.csv changed compared with the supplied FSM export baseline | Satisfied or Blocked | FSM import package and optional baseline in setup_data_artifacts |  | Changed instance-organization data requires ORA_MSC_APPS_INSTANCE.csv in the import package | Add ORA_MSC_APPS_INSTANCE.csv to the import package before importing | apps_instance_csv_included |
| MSCPS.APPS_INSTANCE_FOR_FLEX_MAPPING_CHANGE | ORA_MSC_APPS_INSTANCE.csv is included | Yes | ORA_MSC_FLEX_FIELD_MAPPING.csv changed compared with the supplied FSM export baseline | Satisfied or Blocked | FSM import package and optional baseline in setup_data_artifacts |  | Changed flex-field mapping data requires ORA_MSC_APPS_INSTANCE.csv in the import package | Add ORA_MSC_APPS_INSTANCE.csv to the import package before importing | apps_instance_csv_included |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Neither tracked CSV changed, or each applicable change includes ORA_MSC_APPS_INSTANCE.csv | Yes |
| Blocked | A tracked CSV changed and ORA_MSC_APPS_INSTANCE.csv is absent | No |
| Baseline absent | No retained FSM export baseline is supplied in setup_data_artifacts | Yes; permit import without comparison |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSCPS.DEPENDENCIES | decision | 2 | resolve_dependency | satisfied->MSCPS.PACKAGE_GATE;baseline_absent->MSCPS.COMPLETE_WITHOUT_BASELINE;blocked->MSCPS.BLOCKED;failure->MSCPS.FAILED | MSCPS.VALIDATE_PACKAGE | stop | Compare tracked CSV files with the supplied FSM export baseline before importing when it is available |
