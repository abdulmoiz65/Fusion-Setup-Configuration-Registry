# Configure Seniority Dates Input Validation

## Purpose

Validates the operation, required inputs, supported fields, and value shapes before dependency resolution or execution.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | missing | Ask for one supported operation | Always |  |
| Read selector | Exact rule name or code; optional bounded search and paging | valid | Select one scope before reading: active by default, inactive only when explicitly requested, or all only when explicitly requested. Return every matching row and total count for an exact selector. If Fusion cannot filter `Active`, apply the selected scope locally before resolving display lookups, writing an artifact, or composing the response. Parse all bounded pages only for an explicit all-configured-rules request. | get | resolve_seniority_rule |
| Create intake | Exact seniority rule code, attribute, and level | missing | Ask once for all missing required values; apply documented defaults after complete intake | create |  |
| Create rule | Exact seniority rule name or code | missing | Ask as part of the complete create intake | create | resolve_seniority_rule |
| Create level | Exact seniority level name or code | missing | Ask as part of the complete create intake | create | resolve_seniority_level |
| Create attribute | Exact seniority attribute name or code | missing | Ask as part of the complete create intake | create | resolve_seniority_attribute |
| Create Cumulative | Exact Yes or No value when supplied | valid | Default an omitted value to N and resolve it exactly through YES_NO | create | resolve_seniority_cumulative |
| Create Allow Edit | Exact Yes or No value when supplied | valid | Default an omitted value to Y and resolve it exactly through YES_NO | create | resolve_seniority_allow_edit |
| Create scope | Every supplied scope selector | valid | Default omitted scope to `No restriction`; resolve each supplied selector independently | create |  |
| Create authoritative compatibility | A complete create intake and an authoritative current metadata constraint that explicitly binds the supplied values | proven conflict | Stop before source generation; identify the authoritative source and require corrected values | create | validate_authoritative_seniority_compatibility |
| Current target | One exact seniority rule name or code | missing | Ask for one exact current selector | edit or delete | find_configured_seniority_date_rules |
| Requested changes | At least one explicit Data Loader-supported business-field change | missing | Ask for the intended change | edit |  |
| Delete intent | Explicit delete request for one exact current target | missing | Ask the user to confirm the operation and target | delete | find_configured_seniority_date_rules |
| Exact-details read | One exact rule name or code | missing or ambiguous | Report zero or multiple matches clearly; do not select by position | get | resolve_seniority_rule |
| List or search read filters | Explicit filter values, plus the default Active list scope when status is omitted | valid | Combine all supplied filters with AND logic. Filter the returned rows to the selected scope before lookup resolution or presentation. Show inactive rules only for an explicit inactive or all-rules request. | get | find_configured_seniority_date_rules |
| Mutation environment and privileges | Configured environment plus required read and Data Loader privileges | missing or denied | Detect the configured environment without requesting user confirmation; stop only when the preflight is missing or denied | create, edit, delete | validate_mutation_environment |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A complete create intake is supplied | validate each supplied resolver-backed value independently | Resolve the rule, attribute, level, flags, and scope values |  |
| A rule, level, or attribute is supplied for a non-create operation | valid only when it has one exact current match | Resolve the supplied value |  |
| Any optional basis, flag, formula, worker type, or scope value is supplied | valid only when each value has one exact current match | Resolve each value independently through its registered resolver |  |
| create | valid only when the resolved code has no current configuration | Run the create uniqueness check | find_configured_seniority_date_rules |
| edit or delete | valid only when the selector identifies exactly one current configuration | Resolve the current target | find_configured_seniority_date_rules |
| create | valid only when every technical field required by the current operation-specific create template has one supported value | Derive required fields from current template, schema, LOV, and default evidence; omit absent fields and preserve optional blanks | derive_seniority_configuration_tuple |
| edit | valid only when the current technical tuple is preserved unless the registered contract and request support its change | Read and preserve the current tuple | find_configured_seniority_date_rules |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is get, create, edit, or delete | Otherwise unsupported | Always |  |
| Dates use ISO format and end date is not earlier than start date | Otherwise invalid | Any date is supplied |  |
| Lookup display meaning | Never parse a code, suffix, naming pattern, or lookup display meaning as an Attribute/Level compatibility schema | Create |  |
| Create Attribute status | Resolve only one exact enabled `ORA_PER_TRIG_FIELDS` lookup value; never select an inactive Attribute | create | resolve_seniority_attribute |
| Technical create fields | Require and validate only fields that the current operation-specific create template marks required. Omit absent fields; leave optional fields blank or omit them as the template directs. `SeniorityVersion=V3` is valid only when current metadata explicitly allows it. | create | derive_seniority_configuration_tuple |
| Source columns, types, cardinalities, keys, and writable values exist in the registered employmentSeniorityDateConfigurations Data Loader object | Otherwise unsupported | create, edit, or delete |  |
| Technical IDs, audit fields, links, generated values, display-only meanings, partial keys, and unknown multi-value encodings are not user supplied | Otherwise invalid | create, edit, or delete |  |
| Transient IDs are accepted only from a matching live resolver for the exact registered target field | Otherwise invalid | A resolved technical ID is used |  |
| SourceRefTableName and SourceRef001 through SourceRef010 are absent unless the current operation-specific template exposes them | Otherwise unsupported | create, edit, or delete |  |
| Every supplied worker type and scope member is independently resolvable and deduplicated | Otherwise invalid | Worker types or scope values are supplied |  |
| An unqualified list request | Include only returned rows with `Active=Y`; if the collection endpoint cannot filter `Active`, discard all other rows locally before display lookup resolution, artifact generation, or response composition. Do not further exclude DisplayInUI, RecordPresent, worker type, country, legal employer, union, collective agreement, blank, or `N` values | get | find_configured_seniority_date_rules |
| An explicit inactive-rules request | Include only returned rows with `Active=N`; if the collection endpoint cannot filter `Active`, discard all other rows locally before display lookup resolution, artifact generation, or response composition | get | find_configured_seniority_date_rules |
| An explicit all-configured-rules request | Include every returned row; do not exclude Active, DisplayInUI, RecordPresent, worker type, country, legal employer, union, collective agreement, blank, or `N` values | get | find_configured_seniority_date_rules |
| DisplayInUI filtering | Valid only when the caller explicitly requests UI-visible or UI-hidden rules | get | find_configured_seniority_date_rules |
| `No restriction` | Valid as the explicit or defaulted create-scope choice and leaves every scope dimension blank | create | validate_scope_no_restriction |
| System-owned technical fields | Reject user-supplied Object, Source Field, Triggering Field Type, Seniority Basis, Hours per Day, Hours per Month, Hours per Year, or Seniority Fast Formula; derive or preserve them only through the current template | create or edit | derive_seniority_configuration_tuple |
| Scope attributes | Worker Type, Country, Legal Employer, Union, and Collective Agreement are unsupported because the Data Loader DAT route cannot serialize their array values; reject any create or update request that supplies or changes them | create or edit |  |
| Supplied create combination | After intake is complete, reject only when a separate authoritative current metadata source explicitly proves the supplied combination invalid; absence or ambiguity of that source is not a conflict | Otherwise continue with declared validation and report unavailable compatibility evidence diagnostically | validate_authoritative_seniority_compatibility |
| Update | One exact fresh target, at least one explicit delta, and unchanged omitted fields | Otherwise invalid | read_current_seniority_rule |
| Update with evaluated `RecordPresent = Y` | Valid only when every requested change is Active, Allow Edit, or Display in UI | Otherwise invalid | evaluate_seniority_rule_usage |
| Delete | One exact fresh target with evaluated `RecordPresent=N` and a proven registered item-level deletion capability | Otherwise unsupported | confirm_seniority_deletion_capability |
| REST SelectCollAgreementName, SelectLegalEmployerName, SelectLegislationCode, SelectUnionName, and SelectWorkerType are excluded from XLSX unless the registered schema exposes them | Otherwise unsupported; use the resolved ID or code target | create, edit, or delete |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEN.VALIDATE | decision | 1 | validate_input | valid->SEN.DEPENDENCIES;missing->SEN.ERROR;invalid->SEN.ERROR;unsupported->SEN.ERROR | none | stop | Any seniority-date request |
