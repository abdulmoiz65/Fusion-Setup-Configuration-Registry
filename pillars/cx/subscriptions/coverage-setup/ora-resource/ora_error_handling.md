# Standard Coverage Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Required coverage, entitlement, prerequisite, or charge-discount information is missing | Stop and show the missing values; do not prepare a create request. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | The exact-name lookup returns one existing coverage | Return the existing coverage for review and stop before a create request. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | The exact-name lookup returns multiple records, is unauthorized, or fails | Stop and report the resolved error category; do not infer an absent coverage. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | The StandardCoverageYn=Y collection lookup is unauthorized or fails | Stop and report the API, authorization, or transport error; do not retry automatically. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | The detailed coverage or entitlement-rule lookup is absent, unauthorized, or fails | Stop and report the API, authorization, or transport error; do not infer missing related details. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | A documented create attempt fails or has an uncertain outcome | Preserve safe diagnostics and reconcile through the documented read-only lookup before considering another request; never automatically retry. |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | SchedulePuid or ExceptionPuid is missing for an item request, or a read-only lookup does not return a record | Return an actionable issue and stop; do not retry or attempt a write. |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | A schedule or exception collection lookup fails | Report the API, authorization, or transport failure and stop; do not retry automatically. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Required default level, Standard Coverage, start date, or customer selection is missing | Stop Data Loader preflight and show the missing value. An empty End Date is valid for an open-ended coverage. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | The Default Coverage collection lookup is unauthorized or fails | Stop and report the API, authorization, or transport error; do not retry automatically. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | No Default Coverage is returned for a listing or default-resolution request | Return the empty result; do not infer a Global or Customer default. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | A create, update, or delete is requested | Use `core.data-loader` and its immutable artifact and approval workflow. Do not construct a direct REST write or substitute a manual UI save. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Data Loader metadata, source validation, or preflight fails | Stop and report the Data Loader diagnostic. Do not fall back to direct REST or a manual UI route. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Upload, initiation, or delete outcome is partial or uncertain | Preserve the approved artifact and reconcile through the Data Loader status route; do not retry automatically. |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | input_validation | Required values or documented field limits are invalid | Correct the values and restart validation. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | dependency_blocker | An entitlement or prerequisite is not ready | Complete or verify the dependency, then restart validation. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | duplicate_review | An exact CoverageName already exists | Review the existing coverage and use a separately approved update workflow if required. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | auth_authz | The documented read-only lookup is rejected | Restore the required access; do not classify the result as absent. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | transport_or_fusion_api | The documented read-only lookup cannot complete | Preserve the error summary and stop before retrying a write. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | related_detail_lookup_failure | A coverage detail or entitlement-rule lookup is absent, unauthorized, or fails | Preserve the safe diagnostic summary and stop; do not retry automatically. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | unverified_success | A future create request may have completed but verification is unavailable | Reconcile with the documented read-only lookup; do not repeat the write. |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | input_validation | Schedule or exception identity, required TimezoneCode, or required exception availability object values are missing or invalid | Correct the missing documented values and restart validation. |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | lookup_failure | A documented schedule or exception lookup is absent, ambiguous, unauthorized, or fails | Preserve the safe diagnostic summary and stop before a write. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | input_validation | Required Default Coverage values are absent or Default Level is invalid | Correct the values and restart validation. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | dependency_blocker | Registered Data Loader template, Standard Coverage, or customer selection is absent | Resolve the template or correct the Data Loader source, then restart validation. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | lookup_failure | The developer-provided Default Coverage lookup is unauthorized or fails | Preserve the safe diagnostic summary and stop; do not retry automatically. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | no_applicable_default | The collection lookup returns no applicable Default Coverage | Return the empty result; do not infer an applicable default. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | direct_rest_write_blocked | A direct REST create, update, or delete is requested | Use the Data Loader route; do not construct a direct REST write. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | data_loader_preflight_failure | Data Loader metadata, source validation, or approval preflight fails | Preserve the safe diagnostic summary and stop; do not substitute another route. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | unverified_success | A Data Loader submission outcome is partial or uncertain | Reconcile through Data Loader status; do not automatically retry the upload, initiation, or delete. |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Readiness result | Exact CoverageName, lookup outcome, prerequisite status, and the fact that these resources do not execute a REST write. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Collection-listing result | StandardCoverageYn=Y filter, collection outcome, and the fact that this resource lookup is read-only. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Related-detail result | CoverageName, lookup outcome, MatrixId presence, and the fact that these related-resource lookups are read-only. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Failure | Error category, redacted diagnostic summary, and the safe next action. |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | Readiness result | Requested resource type, supplied PUID or collection parameters, lookup outcome, and the fact that these resources do not execute a REST write. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Data Loader readiness result | Requested operation, Default Level, Default Level Value when Customer is selected, selected Standard Coverage, effective dates, and the Data Loader preflight/approval route. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Lookup or default-resolution result | Collection outcome, the evaluated Global or Customer precedence rule, and the fact that the collection lookup is read-only. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Failure | Error category, redacted diagnostic summary, and the safe next action. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.READY_FOR_DOCUMENTED_CREATE | terminal | 50 | terminal | none | STDCOV.DESIGN_GATE | continue | The request is complete for the separate documented create workflow; this resource set performs no write |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.INPUT_ISSUES | terminal | 60 | terminal | none | none | continue | Input validation did not pass |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DEPENDENCY_ISSUES | terminal | 70 | terminal | none | none | continue | A required dependency is not ready |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.LOOKUP_ISSUES | terminal | 80 | terminal | none | none | continue | The exact-name lookup failed, was ambiguous, or could not be authorized |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DUPLICATE_REVIEW | terminal | 90 | terminal | none | STDCOV.LOOKUP | continue | An exact-name standard coverage exists and must be reviewed before any update workflow |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DESIGN_ISSUES | terminal | 100 | terminal | none | STDCOV.DESIGN_GATE | continue | A documented design requirement is not satisfied |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.LIST_RESULTS | terminal | 110 | terminal | none | STDCOV.LIST | continue | The StandardCoverageYn=Y collection lookup returned one or more Standard Coverages |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.LIST_EMPTY | terminal | 120 | terminal | none | STDCOV.LIST | continue | The StandardCoverageYn=Y collection lookup returned an empty result set |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.LIST_ISSUES | terminal | 130 | terminal | none | none | continue | The StandardCoverageYn=Y collection lookup was unauthorized, failed, or did not return a usable result |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DETAIL_WITHOUT_ENTITLEMENT_RULE | terminal | 140 | terminal | none | STDCOV.DETAIL_HEADER | continue | The coverage details returned but no MatrixId was available for an entitlement-rule lookup |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DETAIL_RESULTS | terminal | 150 | terminal | none | STDCOV.ENTITLEMENT_RULE | continue | The coverage details and requested entitlement rule returned |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DETAIL_ISSUES | terminal | 160 | terminal | none | none | continue | A required detail input is missing or a detailed coverage or entitlement-rule lookup did not return a usable result |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.SCHEDULE_LIST_RESULTS | terminal | 60 | terminal | none | AVAIL.SCHEDULE_LIST | continue | The availability-schedule collection lookup returned one or more rows |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.SCHEDULE_LIST_EMPTY | terminal | 70 | terminal | none | AVAIL.SCHEDULE_LIST | continue | The availability-schedule collection lookup returned an empty result set |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.SCHEDULE_SUCCESS | terminal | 80 | terminal | none | AVAIL.SCHEDULE_LOOKUP | continue | The item lookup returned one availability schedule |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.EXCEPTION_LIST_RESULTS | terminal | 90 | terminal | none | AVAIL.EXCEPTION_LIST | continue | The availability-exception collection lookup returned one or more rows |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.EXCEPTION_LIST_EMPTY | terminal | 100 | terminal | none | AVAIL.EXCEPTION_LIST | continue | The availability-exception collection lookup returned an empty result set |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.EXCEPTION_SUCCESS | terminal | 110 | terminal | none | AVAIL.EXCEPTION_LOOKUP | continue | The item lookup returned one availability exception |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.ISSUES | terminal | 120 | terminal | none | none | continue | Availability inputs are missing or a read-only schedule or exception lookup did not return a usable result |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.READY_FOR_DATA_LOADER | terminal | 70 | terminal | none | DEFCOV.DESIGN_GATE | continue | The Default Coverage is ready for the governed Data Loader preflight and approval workflow |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.INPUT_ISSUES | terminal | 80 | terminal | none | none | continue | Default Coverage input validation did not pass |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.DEPENDENCY_ISSUES | terminal | 90 | terminal | none | none | continue | A required Standard Coverage or customer selection is not ready |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.DESIGN_ISSUES | terminal | 100 | terminal | none | DEFCOV.DESIGN_GATE | continue | A required Default Coverage design requirement is not satisfied |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.LIST_RESULTS | terminal | 110 | terminal | none | DEFCOV.LIST | continue | The Default Coverage collection lookup returned one or more rows |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.LIST_EMPTY | terminal | 120 | terminal | none | DEFCOV.LIST | continue | The Default Coverage collection lookup returned an empty result set |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.LOOKUP_ISSUES | terminal | 130 | terminal | none | none | continue | The Default Coverage collection lookup was unauthorized, failed, or did not return a usable result |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.NO_DEFAULT | terminal | 140 | terminal | none | DEFCOV.RESOLVE_DEFAULTS | continue | No applicable Default Coverage was returned from the collection lookup |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.CUSTOMER_DEFAULT_APPLIED | terminal | 150 | terminal | none | DEFCOV.APPLY_DEFAULT | continue | A customer-level Default Coverage overrides the global default for the customer |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.GLOBAL_DEFAULT_APPLIED | terminal | 160 | terminal | none | DEFCOV.APPLY_DEFAULT | continue | A global Default Coverage applies because no customer-level default applies |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.NO_APPLICABLE_DEFAULT | terminal | 170 | terminal | none | DEFCOV.APPLY_DEFAULT | continue | Returned Default Coverage data did not contain an applicable Global or Customer default |
