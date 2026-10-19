# Time Layout Sets Input Validation

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Use only populated structured business values that completed input validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified business value explicitly supplied by the user | Every Complete Summary | |
| Applied defaults | Include every default that was actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, and metadata-only values | Every Complete Summary | |
| Populated children | Show populated child records using business labels only; do not render an empty child section | A child record has values | |
| Summary readiness | Always generate the Complete Summary before the provider-owned approval process | A create or update request is ready for provider approval | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent identity | Name | Block readiness | Request the layout-set name | Create |  |
| Update hierarchy context | A `PATCH` row for every ancestor of each changed child, using current persisted IDs and the live parent chain | Block readiness | Materialize the root and every intermediate parent as `PATCH` rows before the changed child row | Update through Data Loader | search_time_layout_sets_by_criteria |
| New aggregate loader correlations | One unique numeric-only local timeLayoutSetsV2.TimeLayoutSetId and distinct numeric-only local IDs for each requested timeEntryLayout.TimeEntryLayoutId, webClockLayouts.WebClockLayoutId, and webClockButtons.WebClockButtonId | Block readiness | Repeat the Time Layout Set correlation in each timeEntryLayout.TimeLayoutSetId and webClockLayouts.TimeLayoutSetId; repeat each Time Entry Layout correlation in its fields and totals; repeat each Web Clock Layout correlation in its buttons; repeat each Web Clock Button correlation in its button time-card fields | Create through Data Loader when the live template exposes every requested section |  |
| Entry layout | TimeEntryFormat, DecimalPrecision, DateFormat, and DefaultBlankRows | Apply documented defaults when a new-entry value is blank; block only when it remains blank or invalid after defaulting | Apply TLS.APPLY_DEFAULTS, then validate supported values | Create or update |  |
| Default time card layout totals | Generated default totals rows | Block readiness | Generate and retain the default totals rows before preview | Create |  |
| Time consumers | At least one of PYR, PJC, or TM with PJC | Block readiness | Request selected supports; reject TM without PJC | Time card fields are generated |  |
| Field row | TimeCardFieldTemplateId and ShowInAdditionalAttributesFlag | Block readiness | Resolve field through its LOV | A field row is created or changed | resolve_time_card_field |
| Total row | TimeCategoryId and Label | Block readiness | Resolve category and request Label | A custom total is created or changed | resolve_time_category |
| Web Clock Layout optional child | WebClockLayoutId, WebClockButtonId, ButtonSetId, ButtonId, DisplayLabel, DisplaySequence, and child fields | Allow the Time Layout Set to proceed without a Web Clock Layout; block only an explicitly requested Web Clock configuration | When configured, associate Web Clock Layout, Button, and Button Time Card Field records through their documented ID references, then resolve dependent Button Set, Button, and fields | Web Clock is configured | resolve_button_set |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Project Team Membership is selected without Project Costing | Invalid | Stop and require Project Costing |  |
| A search, update, or delete is requested | Require at least one business search attribute and evaluate every supplied attribute, including supported child attributes | Retrieve all pages, show candidates meeting every supplied condition, and require a selection when multiple candidates match | search_time_layout_sets_by_criteria |
| A create request is prepared | Require the duplicate check to try exact Name, partial Name, and then all supplied non-Name attributes before create readiness | Present a candidate meeting every applicable condition and wait for the user's use-existing or create-new choice | search_time_layout_sets_by_criteria |
| More than three List View fields are selected | Invalid | Stop and reduce selected fields to three or fewer |  |
| Web Clock Layout is omitted | Valid | Continue without Web Clock child records |  |
| Web Clock Layout is configured | Valid only when every child repeats its direct parent ID | Stop and correct the broken parent-child relationship |  |
| A child record is updated | Valid only when the source contains a `PATCH` row for every live ancestor from `timeLayoutSetsV2` to that child | Stop and add the missing parent context rows before preview |  |
| A create or update request is ready for provider approval | Require a Complete Summary formed only from verified structured business values | Generate the summary before the provider-owned approval process | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DefaultBlankRows | Require an integer greater than or equal to zero | Create or update |  |
| TimeEntryFormat | Accept HOUR, TIME, or BOTH | Create or update |  |
| DecimalPrecision | Accept 0, 1, 2, or 3 | Create or update |  |
| DateFormat | Accept only a pattern listed in Date Format Options | Create or update |  |
| Attribute Display | Accept false for Main or true for Additional | A field row is created or changed |  |
| Web Clock Button DisplaySequence | Require a positive integer that is unique within the parent Web Clock Layout | A Web Clock Button is created or changed |  |
| Web Clock Button Time Card Field DisplaySequence | Require a positive integer that is unique within the parent Web Clock Button | A Web Clock Button Time Card Field is created or changed |  |

## Date Format Options

Use these accepted DateFormat values. The preview uses 3 September 2026.

| Date Format | Preview |
|---|---|
| EEEEE, MMMMM dd | Thursday, September 03 |
| EEE, MMMMM dd | Thu, September 03 |
| EEE,MMM dd | Thu,Sep 03 |
| EEEEE | Thursday |
| EEE | Thu |
| MMM dd | Sep 03 |
| MMM dd,EEE | Sep 03,Thu |
| MMMMM dd,EEE | September 03,Thu |
| MMMMM dd, EEEEE | September 03, Thursday |
| EEEEE, dd MMMMM | Thursday, 03 September |
| EEE, dd MMMMM | Thu, 03 September |
| EEE,dd MMM | Thu,03 Sep |
| dd MMM | 03 Sep |
| dd MMM,EEE | 03 Sep,Thu |
| dd MMMMM,EEE | 03 September,Thu |
| dd MMMMM, EEEEE | 03 September, Thursday |
| yyyy-MM-dd | 2026-09-03 |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TLS.VALIDATE_INPUT | step | 10 | validate_input | valid->TLS.SEARCH_LAYOUT_SETS;missing->TLS.HANDLE_ERROR;invalid->TLS.HANDLE_ERROR | TLS.CHECK_REST_CAPABILITY | stop | A Time Layout Sets search, create, update, or delete request passed the release and REST-capability gates |
