# Picking Rule Assignments Input Validation

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Normalize approved friendly standard-lookup meanings to their canonical value only when supplied. |
| BO/Data Loader ownership | Resolve the registered BO foreign keys, including Picking Rule from `RuleName`, carrier, category, customer, UOM, and ABC group/class values. |
| Fusion ownership | Enforce required fields, server-side domains, uniqueness, criteria combinations, and final REST validation. |
| REST execution | Do not provide direct REST write guidance; `core.data-loader` owns execution. |

## Accepted Input Alternatives

| Requirement Group | Accepted Fields | Canonical Field | Applies When | Resolver |
|---|---|---|---|---|
| Item Type identity | `ItemType` or `ItemTypeMeaning` | `ItemType` | Either field is supplied | resolve_item_type |
| Date Type identity | `DateTypeCode` or `DateTypeMeaning` | `DateTypeCode` | Either field is supplied | resolve_date_type |
| Transaction Action identity | `TransactionActionId` or `TransactionActionMeaning` | `TransactionActionId` | Either field is supplied | resolve_transaction_action |
| Picking Rule identity | `RuleName` | `PickingRuleId` | The Picking Rule is supplied |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Item Type lookup normalization | Trim outer whitespace and resolve the supplied Meaning or canonical code to one `EGP_ITEM_TYPE` row. | `ItemTypeMeaning` or `ItemType` is supplied. | resolve_item_type |
| Date Type lookup normalization | Trim outer whitespace and resolve the supplied Meaning or canonical code to one `INV_RULES_DATE_TYPE` row. | `DateTypeMeaning` or `DateTypeCode` is supplied. | resolve_date_type |
| Transaction Action lookup normalization | Trim outer whitespace and resolve the supplied Meaning or canonical code to one `INV_TRANSACTION_ACTION` row. | `TransactionActionMeaning` or `TransactionActionId` is supplied. | resolve_transaction_action |
| Omitted values | Preserve blanks; Data Loader and Fusion determine whether the field is required. | A field is omitted. |  |

## Conditional FSM Package Validation

Apply these rules only when an FSM package containing
`INV_RULE_SELECTION_CRITERION.csv` is explicitly selected. They do not apply to
the default REST/Data Loader route.

## FSM Request-to-Criterion Mapping

For an FSM request, derive one proposed `INV_RULE_SELECTION_CRITERION.csv`
row from the supplied native values. Do not apply REST LOV normalization to
these FSM code fields. The exported CSV header determines the final column
order; preserve every unsupported or omitted exported column as blank.

| Request Field | Criterion Column | Required Behavior |
|---|---|---|
| Picking Rule | `ORA_INV_RULE.RuleName` | Preserve the supplied native rule name; together with Sequence Number, it identifies a row to replace when an update is requested. |
| Sequence Number | `SequenceNumber` | Preserve the supplied native value. |
| From Organization Code | `FromOrganizationCode` | Preserve the supplied native code. |
| Rule Type Code | `RuleTypeCode` | Preserve the supplied native code. |
| Return Type Code | `ReturnTypeCode` | Preserve the supplied native code. |
| Enabled | `EnabledFlag` | Preserve the supplied native FSM flag. |
| Date Type | `DateTypeCode` | Preserve the supplied native code. |
| Item Type | `ItemType` | Preserve the supplied native code. |
| Transaction Action | `TransactionActionId` | Preserve the supplied native code. |
| Category | `CategoryName` | Preserve the supplied category name. |

| Check | What Happens | Applies When |
|---|---|---|
| FSM update identity | Require nonblank Picking Rule and Sequence Number to select an existing criterion row for replacement. | A change to an existing FSM assignment is requested. |
| Criterion-row merge | Retain the complete exported `ORA_INV_RULE.csv`, the original `INV_RULE_SELECTION_CRITERION.csv` header, and every non-target criterion row unchanged. When exactly one criterion row matches `(ORA_INV_RULE.RuleName, SequenceNumber)`, replace only the mapped columns for which the request supplies a value; retain all omitted columns unchanged. When no row matches, append one row populated from the supplied native values using the existing terminal line ending, without inserting a blank CSV record before or after it. Do not apply REST LOV normalization or a task-local duplicate rejection. | A criterion row is proposed or changed in an FSM package. |
| Ambiguous replacement target | Stop when multiple exported criterion rows match the supplied `(ORA_INV_RULE.RuleName, SequenceNumber)`; do not select one arbitrarily. | A change to an existing FSM assignment is requested. |
| Archive preservation | Preserve `ASM_SETUP_CSV_METADATA.xml`, required CSV members, exported headers, encoding, and member names. Reject a criterion CSV containing a blank record. Do not prepare a loose-CSV archive or alter metadata. | Before Data Loader validation of an FSM package. |
| FSM archive eligibility | Require exactly one `ASM_SETUP_CSV_METADATA.xml` marker and the assignment baseline's native `ORA_INV_RULE.csv` and `INV_RULE_SELECTION_CRITERION.csv` members and headers. Record the assignment export ZIP fingerprint and process ID in the package receipt. | Before FSM package authoring or Data Loader handoff. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PRA.CLASSIFY_IMPORT_ROUTE | step | 5 | validate_input | rest->PRA.VALIDATE_INPUT;fsm->PRA.VALIDATE_FSM_ARCHIVE;blocked->PRA.HANDLE_ERROR | none | stop | Every request. REST is the default; FSM applies only to an explicitly selected ZIP or an archive containing `ASM_SETUP_CSV_METADATA.xml`. |
| PRA.VALIDATE_INPUT | step | 10 | validate_input | valid->PRA.RESOLVE_ITEM_TYPE;invalid->PRA.HANDLE_ERROR | PRA.CLASSIFY_IMPORT_ROUTE | stop | Classified REST request before Data Loader preparation. |
| PRA.VALIDATE_FSM_ARCHIVE | step | 11 | validate_input | validated->PRA.CHECK_FSM_READINESS;blocked->PRA.HANDLE_ERROR | PRA.CLASSIFY_IMPORT_ROUTE | stop | Classified FSM request/archive. Map supplied native request values to the criterion row; validate update identity when applicable, criterion-row merge, archive eligibility, and replacement-target ambiguity; do not apply REST lookup normalization. |
