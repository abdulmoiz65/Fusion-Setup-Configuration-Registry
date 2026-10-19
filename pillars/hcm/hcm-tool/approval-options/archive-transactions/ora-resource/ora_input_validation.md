# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Approval process | approval_process | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. | Supply the exact Process Name, then rerun validation. | Every request |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| approval_process is present and nonblank | Continue to the `findByProcessName` REST lookup. | Every request | find_approval_process_by_name |
| archive_period is a supported UI label | Normalize the supplied UI label before preview or Fusion submission: 3 Months maps to ORA_HRC_TXN_3_MONTHS; 6 Months maps to ORA_HRC_TXN_6_MONTHS; 9 Months maps to ORA_HRC_TXN_9_MONTHS; Don't archive maps to ORA_HRC_TXN_DONT_ARCH. Use the mapped value as archivePeriod. | An Archive Transactions mutation receives a UI label |  |
| archive_period is an underlying ArchivePeriod value | Use ORA_HRC_TXN_3_MONTHS, ORA_HRC_TXN_6_MONTHS, ORA_HRC_TXN_9_MONTHS, or ORA_HRC_TXN_DONT_ARCH unchanged as archivePeriod. | An Archive Transactions mutation receives an ArchivePeriod value |  |
| archive_period is neither a supported UI label nor an underlying ArchivePeriod value | Return ARCHIVE_PERIOD_INVALID. Do not submit to Fusion; require one of the documented UI labels or ArchivePeriod values. | An Archive Transactions mutation supplies archive_period |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.VALIDATE_INPUT | decision | 1 | validate_input | valid->APPROVAL_PROCESS.FIND_BY_PROCESS_NAME;missing->APPROVAL_PROCESS.MISSING | none | stop | Every request |
