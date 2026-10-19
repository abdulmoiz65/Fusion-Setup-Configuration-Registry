---
task_code: "CUSTOM_ALERTS"
task_name: "Alerts"
parent_skill_id: "hcm.hcm-tool.alert-foundation"
pillar: "HCM"
offering: "HCM Tool"
offering_code: "CUSTOM_HCM_TOOL"
functional_area: "Alert Foundation"
functional_area_code: "CUSTOM_ALERT_FOUNDATION"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/custom/setupTasksAll.json"
---

# Alerts

## Setup Task Metadata

- Task name: `Alerts`
- Task code: `CUSTOM_ALERTS`
- Offering: `HCM Tool`
- Offering code: `CUSTOM_HCM_TOOL`
- Functional area / Setup Object: `Alert Foundation`
- Functional area code: `CUSTOM_ALERT_FOUNDATION`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`

## Runtime Ownership

This flat metadata artifact establishes the catalog identity for the Alerts
setup task. The parent [Alert Foundation skill](SKILL.md) continues to own all
Alert-specific REST execution, batch-create, approval, receipt, validation,
reporting, and replay-protection behavior.

## Usage

Use this metadata file to resolve task-scoped resource authoring and rule-plan
generation for `CUSTOM_ALERTS` under `Alert Foundation`.
