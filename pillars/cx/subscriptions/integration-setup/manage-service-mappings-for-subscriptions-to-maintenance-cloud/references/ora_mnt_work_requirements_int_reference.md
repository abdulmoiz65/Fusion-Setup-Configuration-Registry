# MNT_WORK_REQUIREMENTS_INT Reference

## Use

Read this reference when a Service Mapping request needs target-field evidence for preventive maintenance work requirement data.

## Source

- [MNT_WORK_REQUIREMENTS_INT](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntworkrequirementsint-16187.html)

## Key Guidance

- `MNT_WORK_REQUIREMENTS_INT` is the open interface entity for maintenance program work requirement information.
- `INTERFACE_ROW_ID` is the documented primary key.
- `HEADER_NUMBER` links related interface entities.
- `REQUIREMENT_TYPE_CODE` supports documented asset and item requirement categories.
- `STATUS_CODE` supports documented draft and active statuses.
- Work requirement fields include requirement identifiers, organization, program linkage, item and asset context, route, schedule, meter, condition, day rules, effective dates, work-order options, forecast and work-order windows, references, load request, import request, and who columns.

## Boundaries

Use this table reference only as Maintenance Cloud target-field evidence. It does not identify Subscriptions Service Mapping source aliases, source data types, accepted runtime values beyond documented comments, import execution method, or direct-write permission.
