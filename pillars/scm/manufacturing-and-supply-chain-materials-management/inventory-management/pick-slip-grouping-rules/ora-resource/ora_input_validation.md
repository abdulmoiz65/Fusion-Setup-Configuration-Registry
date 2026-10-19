# Pick Slip Grouping Rules Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Pick Slip Grouping Rules page and payload builder | Grouping checkboxes emit `Y` when selected and `N` when not selected; the catalog value is a distinct value field. |
| User approval | Accept friendly grouping-option values, emit `Y` or `N`, pass a supplied catalog only as `GroupByCatalogCode`, and normalize only unambiguous dates. |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Data Loader and Fusion own required fields, uniqueness, server-side domains, cross-field validation, and final payload acceptance. |
| Local validation ownership | Normalize only supplied grouping-option representations and unambiguous supplied dates before Data Loader handoff. |
| No local defaulting | Do not add, infer, or replace `StartDateActive`, `EndDateActive`, or any grouping option when it is absent. |
| Catalog handling | Do not request, resolve, retain, or pass `GroupByCatalogId`. A supplied catalog value is passed only as `GroupByCatalogCode`. |

## Supported Grouping Options

`GroupByCatalogCode` is a value field, not a grouping-option flag. The following fields are grouping-option flags:

| Fields | Accepted supplied values | Canonical value | Invalid input |
|---|---|---|---|
| GroupByOrderNumber, GroupByDestSub, GroupByShipmentPriority, GroupByPushVsPull, GroupByCustomer, GroupByItem, GroupByDestLoc, GroupByProject, GroupByShipTo, GroupBySubinventory, GroupByWorkArea | Trimmed, case-insensitive `Y`, `N`, `yes`, `no`, `true`, or `false` | `Y` for `Y`, `yes`, or `true`; `N` for `N`, `no`, or `false` | Stop before handoff and request one supported value. |
| GroupByTask, GroupByCarrier, GroupByLocator, GroupByDepartment, GroupByDelivery, GroupByDestOrg, GroupByOperation, GroupByProductionLine, GroupByProductionLineOperationSequence, GroupByZone, GroupByItemCategory | Trimmed, case-insensitive `Y`, `N`, `yes`, `no`, `true`, or `false` | `Y` for `Y`, `yes`, or `true`; `N` for `N`, `no`, or `false` | Stop before handoff and request one supported value. |

## Catalog Value and Date Contract

| Field | Accepted input | Output contract | If unclear or invalid |
|---|---|---|---|
| GroupByCatalogCode | A supplied, nonblank catalog value | Trim and include the value only as `GroupByCatalogCode`; omit `GroupByCatalogId` even if supplied. | Stop when supplied as blank. Do not look up or ask for a catalog ID. |
| StartDateActive | Any supplied date whose calendar date is unambiguous and includes a year | Format as `YYYY-MM-DD`. | Ask for clarification when the year is missing (for example, `24 Jan`) or the numeric order is ambiguous (for example, `01/02/2026`). Do not guess. |
| EndDateActive | Any supplied date whose calendar date is unambiguous and includes a year | Format as `YYYY-MM-DD`. | Ask for clarification when the year is missing or the numeric order is ambiguous. Do not guess. |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Grouping-option normalization | Normalize each supplied supported grouping-option value to `Y` or `N`; preserve absent options as absent. | Before Data Loader handoff when one or more supported grouping options are supplied. | |
| Catalog-code shaping | Trim a supplied catalog value, set `GroupByCatalogCode`, and remove `GroupByCatalogId` from the handoff input. | Before Data Loader handoff when a catalog value is supplied. | |
| Date normalization | Format a supplied fully specified, unambiguous date as `YYYY-MM-DD`. | Before Data Loader handoff when StartDateActive or EndDateActive is supplied. | |
| Missing-year date | Ask whether the supplied date means the current year; do not continue until the user supplies or confirms the year. | A date such as `24 Jan` is supplied. | |
| Ambiguous date | Ask the user for an unambiguous date; do not choose a date order. | A numeric date can represent more than one calendar date. | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| PICKSLIPGROUPING.NORMALIZE_INPUT | decision | 10 | validate_input | valid->PICKSLIPGROUPING.CHECK_HANDOFF_READINESS;clarification_required->PICKSLIPGROUPING.RETURN_ISSUES;invalid->PICKSLIPGROUPING.RETURN_ISSUES | none | stop | Every task-routed request with supplied grouping options, catalog value, or active dates. |
