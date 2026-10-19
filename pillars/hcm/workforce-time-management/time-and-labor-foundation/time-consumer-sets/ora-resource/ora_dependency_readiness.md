# Time Consumer Sets Dependency Readiness

## Source Basis

- Time Consumer Sets authoring pack: 01-functional-specification.md, 06-rest-describe-evidence.md, and 07-ui-field-rest-service-matrix.md.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment release support | Retrieve environment_version_details through shared.baseline-assessment.topology-manager.environment-info. For a release before 27A, inform the user that Time Consumer Sets is not available through this skill and stop. |
| 2 | REST capability | For 27A and later, or unavailable release details, resolve one exact usable current timeConsumerSets Data Loader registration and metadata set. Do not select an FSM or direct REST alternative. |
| 3 | Request identity and selection | Validate parent fields, routing, and at least one selected consumer. |
| 4 | Consumer Set criteria search or duplicate check | Retrieve all pages, apply every supplied search criterion, and complete the required candidate selection or duplicate decision before shaping changes. |
| 5 | Time Categories | Resolve the Time Category for every selected consumer. |
| 6 | Defaults and design checks | Apply documented defaults and verify the parent and child configuration shape before preview. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| environment_release_support | Environment release | Yes | Every Time Consumer Sets request | Verify | environment_version_details from shared.baseline-assessment.topology-manager.environment-info | resolve_environment_release_support | Prevents unsupported pre-27A processing | For a release before 27A, inform the user that Time Consumer Sets is not available through this skill and stop | Release name and version, when available |
| time_consumer_sets_rest_capability | REST capability | Yes | The release is 27A or later, or release details are unavailable | Lookup | Exact target dataLoaderBusinessObjects registration and generated metadata workbook | resolve_time_consumer_sets_rest_capability | Confirms the REST-only route is currently usable | Continue only when one exact usable current registration is available | Confirmed REST route and metadata evidence |
| selected_time_category | Time Category | Yes | Project Costing or Payroll is selected | Lookup | Live Fusion GET collection at {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeCategoriesLOV | resolve_time_category | Every selected consumer requires TimeCategoryId | Provide the displayed Time Category for one exact TcatName match | TimeCategoryId and verified Time Category name |
| time_consumer_set_criteria_search | Consumer Set criteria search or duplicate check | Yes | A search or update provides at least one criterion, or a create provides Name | Lookup | Every supplied search parameter; for create, Name and then supplied non-Name criteria when name matching finds no candidate | search_time_consumer_sets_by_criteria | Search and update results must meet every supplied condition; creates must not silently duplicate a candidate found by name or all supplied non-Name criteria | Provide one or more search parameters; if a matching set is presented for a create, choose use existing or create new | Matching business values, selected complete record when applicable, and a private identity only for an authorized update |
| existing_configuration | Existing configuration identity | Conditional | An existing child configuration is changed or deleted through a separately authorized route | Verify | Parent detail read with expanded configurations | resolve_existing_configuration | Existing child writes require the returned ConfigurationId | Select one current configuration from the loaded Time Consumer Set | ConfigurationId and current child values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required values are already verified and match the selected consumer | No lookup required |
| Lookup | A selected consumer needs a Time Category identifier | Read-only lookup only |
| Verify | An existing child configuration is targeted | Read-only parent detail verification only |
| Blocked | A required value is missing, ambiguous, or unavailable from the documented lookup | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->TCS.RESOLVE_TIME_CATEGORIES;blocked->TCS.HANDLE_ERROR | TCS.SEARCH_TIME_CONSUMER_SETS | stop | A create or update request passed the Consumer Set criteria-search or duplicate-check gate |
