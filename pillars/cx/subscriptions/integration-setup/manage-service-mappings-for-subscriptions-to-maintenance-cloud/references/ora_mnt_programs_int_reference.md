# MNT_PROGRAMS_INT Reference

## Use

Read this reference when a Service Mapping request needs target-field evidence for preventive maintenance program header data.

## Source

- [MNT_PROGRAMS_INT](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntprogramsint-28604.html)

## Key Guidance

- `MNT_PROGRAMS_INT` is the open interface entity for maintenance program header information.
- `INTERFACE_ROW_ID` is the documented primary key.
- `HEADER_NUMBER` links related child interface entities.
- Header fields include action, organization, program identifiers, name, description, type, subtype, global assets flag, active dates, forecast and work-order windows, review details, references, DFF columns, load request, import request, and who columns.

## Boundaries

Use this table reference only as Maintenance Cloud target-field evidence. It does not identify Subscriptions Service Mapping source aliases, source data types, accepted runtime values, import execution method, or direct-write permission.
