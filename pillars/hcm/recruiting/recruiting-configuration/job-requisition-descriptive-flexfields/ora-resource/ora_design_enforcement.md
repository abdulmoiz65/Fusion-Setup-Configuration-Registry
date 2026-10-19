# Job Requisition Descriptive Flexfields Design Enforcement

Apply these task-local gates before preview or any configuration handoff.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm exact task scope | Require the Job Requisition Descriptive Flexfields task under Recruiting Configuration |
| 2 | Resolve current read evidence | For Inspect or list, require a fresh exact-task CSV export and exactly one exported DFF root |
| 3 | Isolate the requested scope | For Global, retain only Global Data Elements segment rows and exclude all context-sensitive rows |
| 4 | Present complete segment details | Sort by SequenceNumber and render the required segment columns without audit or sensitive fields |
| 5 | Confirm change authority | For a change, resolve any LOV or value-set contract, preview the immutable artifact, and obtain approval immediately before mutation through Core Data Loader |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | | The request does not target the exact Job Requisition Descriptive Flexfields task under Recruiting Configuration | Route to the correct task; do not substitute a generic Common DFF task | No |
| Inspect or list | Error | | A fresh exact-task export is unavailable, FileContent was not downloaded and extracted, or the export contains zero or multiple DFF roots | Return the exact failed stage or match count and stop without using an older export or alternate API | No |
| Inspect with scope Global | Error | | The result contains a context-sensitive segment row or a row outside the exact exported DFF root | Retain only Global Data Elements rows for the exact exported DFF | Yes, by correcting the result filter |
| Inspect or list | Error | | The result omits SequenceNumber, Name, SegmentCode, SegmentIdentifier, ColumnName, value-set display value, or RequiredFlag when present in the export | Render the complete required segment table and use an em dash only for a blank supported value | Yes, by correcting the presentation |
| A single-segment or configuration request | Error | | The exact DFF identity, scope, target segment or attribute, or business-change scope is missing or ambiguous | Supply the exact missing target detail and revalidate | Yes |
| A configuration change specifies an LOV or value set | Error | resolve_dff_reference_authority | The authoritative source, match rule, requested fields, or value mapping is absent, incomplete, or unresolved | Complete the authoritative reference contract and resolve it before preview or Fusion access | Yes |
| Before a mutation | Error | | The exact target and delta have not been previewed, approval is absent or stale, or the immutable artifact changed | Re-preview through Core Data Loader and obtain current approval immediately before execution | Yes, by re-previewing |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_dff_reference_authority | A configuration change specifies an LOV or value set | Confirmed source; match rule; requested fields; approved DFF change value mapping | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB_REQ_DFF.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->JOB_REQ_DFF.APPROVAL_GATE;blocked->JOB_REQ_DFF.RETURN_ISSUES;conflict->JOB_REQ_DFF.RETURN_ISSUES;unsupported->JOB_REQ_DFF.RETURN_ISSUES | JOB_REQ_DFF.CHECK_READINESS | stop | Every supported request |
