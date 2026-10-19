# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing setting | Resolve the immutable setting Code through collaborationParameters. |
| 2 | Reference value | Resolve the applicable catalog, user, or generic lookup value. |
| 3 | Related settings | Read the settings required for cross-setting validation. |
| 4 | Design compatibility | Apply the documented dependency and UI selection restrictions. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CCS-CATALOG | External catalog exists | Yes | Code is ORA_VCS_DEFAULT_CATALOG_EXTERNAL | Lookup | collaborationItemCategorySetsLOV | resolve_external_catalog_by_name | The service validates the supplied catalog name and resolves its stored identifier internally. | Select one exact external catalog name and submit that name as Value. | Validated CategorySetName |
| CCS-REQUESTER | Requester user exists | Yes | Code is VMI_DEFAULT_REQUISITION_REQUESTER | Lookup | userAccountsLOV | resolve_user_account_by_username | The service validates the supplied username and resolves its stored person identifier internally. | Select one exact username and submit that username as Value. | Validated Username |
| CCS-REASON-CODES | Reason codes are enabled | Yes | ORA_VCS_SP_DWNLD_MEASURES contains ORA_VCS_COMMIT_REASON_CODE | Verify | collaborationParameters | read_collaboration_parameter_by_code | Commit reason-code measures require SHOW_REASON_CODES=Y. | Set SHOW_REASON_CODES to Y before using the reason-code measure. | SHOW_REASON_CODES |
| CCS-REASON-CODES-DISABLE | Reason-code measure is absent | Yes | SHOW_REASON_CODES is set to N | Verify | collaborationParameters | read_collaboration_parameter_by_code | Reason codes cannot be disabled while the measure is configured. | Remove ORA_VCS_COMMIT_REASON_CODE first. | ORA_VCS_SP_DWNLD_MEASURES |
| CCS-DOWNLOAD-TRIPLET | Download settings are compatible | Yes | Code is ORA_VCS_SP_DWNLD_HORIZON, ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL, or ORA_VCS_SP_DWNLD_VIEW_TYPE | Verify | collaborationParameters | read_collaboration_parameter_by_code | The three values are evaluated together. Their permitted combination depends on the daily/date-range feature. | Correct the incompatible horizon, aggregation, or view type. | Horizon, aggregation level, view type, daily/date-range feature state |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | An exact catalog, user, or generic code must be resolved. | Lookup only |
| Verify | Existing setting values must be compatible. | Lookup only |
| Blocked | A required value is missing, ambiguous, or incompatible. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.RESOLVE_DEPENDENCIES | step | 30 | resolve_dependency | satisfied->CCS.REVIEW_DEFAULT_BASELINE;blocked->CCS.HANDLE_ERROR | CCS.VALIDATE_INPUT | stop | A setting update is prepared. |
