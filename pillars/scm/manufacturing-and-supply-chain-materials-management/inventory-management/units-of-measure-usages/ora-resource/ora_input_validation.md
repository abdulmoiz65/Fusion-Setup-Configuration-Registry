# Units of Measure Usages Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Generated task skill metadata | Task identity, REST Data Loader route, and unitOfMeasureUsages business object |
| Developer-provided BO registration record and live Data Loader metadata check | Registered business object and metadata visibility |

## Execution Boundary

| Condition | What Happens | Applies When |
|---|---|---|
| A Units of Measure Usages setup-data request is prepared | Route the request to core.data-loader with business object unitOfMeasureUsages. Data Loader and Fusion own field, key, required-value, domain, and server-side validation. | Every execution request |
| A request proposes a direct REST write or an undocumented alternate route | Stop before execution and require the governed Data Loader route. | Every execution request |

## Approved Source Shaping

| Input Field | Rule | Applies When |
|---|---|---|
| `UOMUsageTypeCode` | Do not populate the field unless the requester explicitly supplies a value. | REST/Data Loader source rows only. |
| `UOMUsageType` | Do not populate the field unless the requester explicitly supplies a value. | REST/Data Loader source rows only. |
| `Subinventory` | Populate the field exactly when the requester supplies a subinventory. | Subinventory-level usage requests. |
| `SubinventoryName` | Do not populate the field unless the requester explicitly supplies a value. | REST/Data Loader source rows only. |
| `UOMCode` | The field is optional. Omit it when the requester does not supply a value; do not derive it from the display value. | REST/Data Loader source rows only. |
| `UnitOfMeasure` | Preserve the requester-supplied display value. It may be supplied without `UOMCode`. | REST/Data Loader source rows only. |

Data Loader and Fusion retain all required-value, reference-data, and server-side
validation. These source-shaping rules do not default, infer, or normalize values.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOMUSAGES.VALIDATE_EXECUTION_ROUTE | decision | 10 | validate_input | valid->UOMUSAGES.CHECK_DATALOADER_READINESS;blocked->UOMUSAGES.RETURN_ISSUES | none | stop | Every Units of Measure Usages execution request. |
