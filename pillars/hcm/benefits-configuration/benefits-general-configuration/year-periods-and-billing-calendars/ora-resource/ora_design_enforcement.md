# Benefit Year Periods Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Object boundary | Keep the source limited to the benefitYearPeriods business object |
| 2 | Metadata boundary | Use current Data Loader metadata for the HDL schema and supported operation |
| 2a | Period type meaning | Record an exact-match result for each supplied PeriodTypeMeaning; a 403 is unverified_forbidden, not an invalid meaning |
| 3 | Import route | Use core.data-loader for validation, preview, approval, upload, and initiation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | | The source names another object or a substitute object | Use benefitYearPeriods only | Yes |
| Every import request | Blocker | | The source attributes, keys, dates, hierarchy, or operation have not been validated by current Data Loader metadata | Correct the source from the metadata validation result; do not guess the HDL contract | Yes |
| Every import request that supplies period type | Blocker | | `PeriodType` contains a display label, inferred code, or value not confirmed by the target lookup | Use the current `PeriodTypeMeaning` user-key alternative or a current-metadata-confirmed foreign-key value | Yes |
| A supplied PeriodTypeMeaning has zero or multiple distinct exact matches | Blocker | commonLookupsLOV | The supplied meaning is invalid or ambiguous | Correct the meaning or resolve the exact target value; do not select a candidate | Yes |
| A supplied PeriodTypeMeaning is unverified_forbidden | Load readiness blocker only; field validation continues | commonLookupsLOV | The meaning remains unverified after a 403 | Resolve access or use another workflow-approved authoritative check before live load | Yes |
| Every request | Blocker | | CSV, direct REST, browser entry, or another non-Data-Loader route is proposed for the HDL import | Use core.data-loader as the sole import route | Yes |
| Update or delete | Blocker | | The exact user keys and intended effect are not established by current metadata and the validated artifact | Correct the source and obtain approval for the exact operation | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_YR.ENFORCE_DESIGN | decision | 30 | design_enforcement | compliant->BEN_YR.GATE_EXECUTION;blocked->BEN_YR.HANDLE_ISSUE | BEN_YR.LOOKUP_PERIOD_TYPE | stop | Enforce the confirmed object boundary, metadata validation, and HDL Data Loader route |
