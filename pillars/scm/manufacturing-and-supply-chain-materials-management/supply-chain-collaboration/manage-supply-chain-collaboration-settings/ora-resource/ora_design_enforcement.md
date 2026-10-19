# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve REST resource boundary | Use the registered collaborationParameters business object only for existing parameter reads and Data Loader routing. |
| 2 | Resolve LOV values | Resolve catalog, username, and generic values through their documented read-only LOV resources. |
| 3 | Enforce UI restrictions | Exclude ORA_VCS_INPUT_VAL and ORA_VCS_CP_AGGR_PERIOD from the UI-supported selections. |
| 4 | Enforce cross-setting compatibility | Validate reason-code and download-triplet rules before preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Code is ORA_VCS_SP_DWNLD_MEASURES and Value contains ORA_VCS_COMMIT_REASON_CODE | Error | read_collaboration_parameter_by_code | SHOW_REASON_CODES is not Y | Enable reason codes before selecting the reason-code measure. | Yes |
| Code is SHOW_REASON_CODES and Value is N | Error | read_collaboration_parameter_by_code | ORA_VCS_SP_DWNLD_MEASURES still contains ORA_VCS_COMMIT_REASON_CODE | Remove the reason-code measure before disabling reason codes. | Yes |
| A download horizon, aggregation level, or view type is changed | Error | read_collaboration_parameter_by_code | The submitted combination violates DownloadTimeAggregationLevelValidator rules | Correct the incompatible setting combination. | Yes |
| Code is ORA_VCS_SP_DWNLD_COMMIT_QTY | Error | resolve_vcs_lookup_code | Value is ORA_VCS_INPUT_VAL | Use an allowed plan edit option; NO_CHANGE is UI-only and is not a REST value. | Yes |
| Code is ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL | Error | resolve_vcs_lookup_code | Value is ORA_VCS_CP_AGGR_PERIOD | Use an aggregation level supported by the settings UI. | Yes |
| The daily/date-range feature is disabled | Error | read_collaboration_parameter_by_code | ORA_VCS_SP_DWNLD_VIEW_TYPE is horizontal and ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL is ORA_VCS_CP_AGGR_DAY | Select a permitted aggregation level or view type. | Yes |
| The daily/date-range feature is disabled | Error | read_collaboration_parameter_by_code | ORA_VCS_SP_DWNLD_HORIZON is ORA_VCS_CP_DL_DAYS or ORA_VCS_CP_DL_BETWEEN | Select a permitted horizon. | Yes |
| The daily/date-range feature is enabled | Error | read_collaboration_parameter_by_code | The aggregation is ORA_VCS_CP_AGGR_DAY, the view is horizontal, and the horizon is ORA_VCS_CP_DL_FORECAST or ORA_VCS_CP_DL_COMMIT | Correct one of the three download settings. | Yes |
| Code is COLLAB_BOUNDARY_DAYS | Error | | COLLAB_BOUNDARY_TYPE is not ORA_VCS_BOUNDARY_DAYS and a boundary-day value is supplied | Set the boundary type to days or omit the unrelated boundary-day change. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_collaboration_parameter_by_code | Cross-setting compatibility is evaluated | Current Value for the related setting Code | ora_reference_lookups.md |
| resolve_vcs_lookup_code | A UI-restricted generic lookup is selected | LookupCode, Meaning | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.ENFORCE_DESIGN | decision | 50 | design_enforcement | compliant->CCS.ALL_GOOD;blocked->CCS.HANDLE_ERROR | CCS.REVIEW_DEFAULT_BASELINE | stop | A setting update has passed validation and dependency readiness. |
