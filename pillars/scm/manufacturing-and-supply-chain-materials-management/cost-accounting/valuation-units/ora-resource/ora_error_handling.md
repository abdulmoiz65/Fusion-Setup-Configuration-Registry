# Error Handling

## Source

- Oracle Fusion Cloud SCM, Valuation Units, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required identifier or SegmentValues value is missing | Stop and request the missing value. |
| Fusion returns `CST-2385213` | Treat it as a source-shape error: the submitted manual valuation unit has no segment association. Build a master-and-detail source and create a new preview. |
| The ADF combination validation action returns no value for SegmentValues | Stop before preview; correct the segment value or the valuation structure selection. |
| A Cost Organization, Cost Book, or Valuation Structure lookup returns no match or more than one match | Stop before source preparation and request a more precise business key. |
| The existing master does not resolve exactly once or lacks ValuationUnitId | Stop before detail preparation; correct the code or resolve the data issue. |
| A manual source targets an automatic-generation design | Stop and use the automatic valuation unit or obtain an approved design change. |
| The Data Loader source lacks valid parent-child linkage | Stop, regenerate from the current live template, and correct the source before retrying. |
| Fusion rejects the Data Loader request | Preserve the returned diagnostic, correct the source or design, and create a new preview before retrying. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required input is missing or malformed | Correct the source and revalidate. |
| Reference lookup | A Cost Organization, Cost Book, or Valuation Structure lookup does not resolve exactly one record | Correct the business key and rerun the read-only lookup. |
| Reference lookup | The existing master lookup does not resolve exactly one nonblank ValuationUnitId | Correct ValuationUnitCode or resolve the master data issue. |
| Input validation | The ADF combination action returns no value for SegmentValues | Correct the segment value or valuation structure and revalidate. |
| Design enforcement | Manual creation conflicts with the structure mode or costing attributes | Correct the design or obtain approval for the change. |
| Data Loader validation | The source does not conform to the live template | Generate a new source and validation preview. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup, dependency, or design contract is TBD | Do not invent a lookup, parent-child relationship, or source value. |
| A valuation unit must be created, updated, or deleted | Do not use direct REST mutation; route through core.data-loader. |
| Preview or approval is incomplete | Do not upload, initiate, retry, or bypass the Data Loader workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VU.DONE_CREATE | terminal | 11 | terminal | none | VU.ENFORCE_CREATE_DESIGN | stop | Create-master validation and design checks pass. |
| VU.DONE_EXISTING_MASTER_DETAILS | terminal | 12 | terminal | none | VU.ENFORCE_EXISTING_MASTER_DETAILS | stop | Existing-master detail validation and design checks pass. |
| VU.DONE_EXISTING_MASTER_UPDATE | terminal | 13 | terminal | none | VU.RESOLVE_VALUATION_UNIT_MASTER | stop | Existing-master identity resolution passes; core Data Loader validates the update source. |
| VU.DONE_EXISTING_MASTER_DELETE | terminal | 14 | terminal | none | VU.RESOLVE_VALUATION_UNIT_MASTER | stop | Existing-master identity resolution passes; core Data Loader validates the deletion source. |
| VU.HANDLE_ISSUE | step | 15 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior node reports invalid input, incomplete dependency, or blocked design. |
| RETURN_ISSUES | terminal | 16 | terminal | none | none | stop | Error disclosure is complete. |
