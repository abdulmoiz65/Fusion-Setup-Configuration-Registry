# Organization Structures Design Enforcement

Use blocking rules only where the developer request or Oracle documentation establishes a deterministic condition. Treat recommendations separately.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---:|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | 1 | Identify the Business Unit and Default Set path | Require a Business Unit Name and choose existing set or Create New; resolve or create-and-re-resolve the set |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | 2 | Apply idempotency | Perform an exact existing-BU lookup and classify New, Existing-Identical, Existing-Different, or Ambiguous before import |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | 3 | Resolve optional HCM references | Only when manager or location is supplied, resolve the respective exact active/effective HCM LOV value before import |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 1 | Verify financial-function dependencies | For a function that generates financial transactions, resolve primary ledger and default legal entity and compare both to the selected BU foundation |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | 1 | Validate the directed relationship | Resolve both parties and the directed pair; validate provider/downstream eligibility according to `AnyProvidersFlag`, pair compatibility, then the four-key duplicate |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | 1 | Identify the assignment | Collect Business Unit, reference data object, and set code before design review |

## Design Rules

| Task Code | Task Name | Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.NAME_REQUIRED | A Business Unit is created | Blocking | None | Business Unit Name is absent | Name the unit before preview | Yes |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.DEFAULT_SET_PATH | A Default Set is selected | Blocking | Exact set lookup and approved create route | Neither an exact existing set nor complete New Set Code and New Set Name is supplied | Use an existing set or create a complete new set | Yes |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.DEFAULT_SET_EXISTS | An existing Default Set is selected | Blocking | `setIdSetsLOV` | The supplied set does not resolve to exactly one set | Correct the identifier or use Create New | Yes |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.CREATE_NEW_SET_ROUTE | Create New is selected | Blocking | Native setIdSets create preview, approval, receipt and exact re-lookup; no HCM skill | Set Code or Set Name is absent, creation is not performed, or re-lookup is not exact | Create the set separately and re-validate it | Yes |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.IDEMPOTENCY | A create/import is requested | Blocking | Exact complete finBusinessUnitsLOV; current comparable saved attributes only for an existing candidate | The lookup is ambiguous/incomplete, or an existing candidate differs from the requested comparable fields | Use the no-op result for identical data, explicitly update a differing BU, or use a new name | Yes |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.OPTIONAL_HCM_REFERENCES | Manager or location is supplied | Blocking | `publicWorkers` for manager; `locationsLovV2` for location | A supplied manager/location has zero, multiple, inactive/ineffective, inaccessible, or unavailable candidates | Correct the supplied identity, effective date, or HCM authorization; blank is acceptable only when explicitly requested | Yes |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.FINANCIAL_DEPENDENCIES | A selected Business Function generates financial transactions | Blocking | `finBusinessUnitsLOV`, `ledgersLOV`, and `legalEntitiesLOV` | Assigned Primary Ledger or Default Legal Entity is missing, nonunique, unverified, or does not equal the selected BU's resolved foundation | Provide the compatible primary ledger and default legal entity | Yes |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.MODULE_SEED_MATCH | A Business Function Code is supplied | Blocking | Business Function Seed Data | Code is absent from the controlled seed-data table or cannot derive exactly one Module ID | Supply a listed code or approve a seed-data update | Yes |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.RELATIONSHIP_IDENTITY | A relationship is requested | Blocking | Exact BU and function resolver | Client Business Unit, Provider Business Unit, upstream function, or downstream function is missing or ambiguous | Provide named values and clarify the directed pair | Yes |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.FUNCTION_ROLE_ASSIGNMENT | A directed relationship is requested | Blocking | Fresh target function-assignment and provider-relationship data | `AnyProvidersFlag = N` and provider lacks the downstream function, or `Y` eligibility is not evidenced by the fresh target contract | Assign the downstream function to the provider or clarify the `Y` contract; do not require client/upstream ownership without target evidence | Yes |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.PAIR_COMPATIBILITY | A directed relationship is requested | Blocking | Approved controlled related-function seed evidence for SPR_FSM_ADD_RELATIONSHIP_V1; supported target evidence for other behavior | Exact directed pair has no approved evidence, contradicts known target facts, or requested policy semantics are unresolved | Use the qualified controlled pair without requiring a live table query solely to restate it; never infer opaque policy meaning | Yes |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.DUPLICATE | A complete relationship identity is available | Blocking | SPR_FSM_ADD_RELATIONSHIP_V1 first-submission provenance, or supported current relationship reads outside it | Known existing/conflicting relationship, ambiguous matches, uncertain prior submission, or missing duplicate evidence outside the first-submission profile | Qualified first submission records limited assurance; existing supported identical values are a no-op; do not treat a failed finder as absence or reimport an uncertain link | Yes |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.FUNCTION_IDS | An execution or import contract requires UpstreamFunctionId or DownstreamFunctionId | Blocking | Exact controlled code mapping | IDs are supplied manually, missing, or treated as cross-environment constants | Resolve them from approved reference data; do not assume portability | Yes |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.IDENTITY | A set assignment is requested | Blocking | Exact BU and set resolver | Business Unit, reference data object, or set code is missing or ambiguous | Provide named values; validate internal evidence through the BU determinant mapping only | Yes |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.REFERENCE_GROUPS | A full ReferenceGroupName assignment set is requested | Blocking | Controlled Reference Group Names | Any of the 73 supplied ReferenceGroupName values lacks Business Unit or Set Code | Complete every controlled reference-group assignment | Yes |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.IMPORT_DERIVATION | CSV/import execution is requested | Blocking | Current template and BUSA_FSM_ADD_OVERRIDE_V1 eligibility, otherwise BUSA_FSM_PARENT_KEY_V1 current keys | No supported profile matches the contract or a genuinely required profile-specific value is missing | Select tested additive eligibility before imposing maintenance keys/dates; no omission waiver, populated export or assignment sample required solely for mapping | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.DEFAULT_SET_PATH | `setIdSetsLOV` / approved set-creation route | A Default Set is supplied or created | Exact Set Code or Set Name | ora_reference_lookups.md |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.IDEMPOTENCY | Exact complete finBusinessUnitsLOV; current comparable evidence for existing candidates | A create/import is requested | BU name and comparable requested fields | ora_reference_lookups.md |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.OPTIONAL_HCM_REFERENCES | `publicWorkers`; `locationsLovV2` | Manager or location is supplied | Manager identity or location identity; request effective date | ora_reference_lookups.md |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.FINANCIAL_DEPENDENCIES | BU, ledger, and legal-entity LOV resolvers | Selected function generates financial transactions | Primary Ledger and Default Legal Entity | ora_reference_lookups.md |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.MODULE_SEED_MATCH | Business Function Seed Data | A Business Function Code is supplied | Business Function Code; Module ID | ora_reference_lookups.md |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.FUNCTION_ROLE_ASSIGNMENT | Fresh target function-assignment and provider-relationship data | A directed relationship is requested | AnyProvidersFlag; provider/downstream eligibility | ora_reference_lookups.md |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.PAIR_COMPATIBILITY | Controlled seed-pair mapping for the qualified SPR profile; supported target evidence for other behavior | Directed relationship requested; exact supported pair | Controlled upstream/downstream IDs; opaque policy code; semantics only when needed | ora_reference_lookups.md |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.DUPLICATE | Qualified first-submission evidence or supported current relationship read | Relationship identity complete; select operation-specific SPR profile | Four-key requested identity; workflow receipts/first-submission classification or actual current duplicate state | ora_reference_lookups.md |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.FUNCTION_IDS | Exact controlled code mapping | IDs are required by an approved contract | UpstreamFunctionId; DownstreamFunctionId | ora_reference_lookups.md |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.REFERENCE_GROUPS | Controlled Reference Group Names | A full assignment set is requested | ReferenceGroupName; Business Unit; Set Code | ora_reference_lookups.md |
## Ledger-to-Legal-Entity Association Enforcement

Apply `BU.LEDGER_LE_ASSOCIATION` after exact ledger and legal-entity resolution and when both foundation values are supplied for BU creation, or before financial-function import. Run `verify_ledger_legal_entity_association` with `legalEntitiesLOV` `LedgerFinder` for the resolved LedgerId and require exactly one returned LegalEntityId and Name matching the requested legal entity. Block when the pair is absent, repeated, nonexact, incomplete, or unavailable; do not infer association from separate LOV results.

## Optional HCM Reference Enforcement

Apply `BU.OPTIONAL_HCM_REFERENCES` after the request effective date is known and before import generation. Resolve only supplied values: manager to `PersonId` through `publicWorkers`, location to `LocationId` through `locationsLovV2`. Require active/effective, exact-one results and a current template/approved mapping for those identities into BU columns. An API identity alone does not prove a different emitted field uses the same representation. Do not impose a manager-role rule, and do not treat either lookup as evidence of financial-foundation compatibility.

  <!-- -->

## Evidence and Scope Enforcement

| Task Code | Task Name | Check | Required Behavior |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New BU has no exported parent | Use the matching template and exact references; do not fabricate an existing-parent requirement for a complete zero-match create |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New set prerequisite | Keep native creation within BU guidance and core REST; HCM read-only LOV namespace does not create an HCM task/skill dependency |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Dependent stage | Confirm saved BU and needed parent/function evidence; do not declare template-only assignment proven by the new-BU create test |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Requested override scope | Import only selected groups and preserve others; a single override does not require all controlled names |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Dependent stage | Verify party and provider-role prerequisites; do not infer policy meaning, Y handling or duplicate absence from template structure |

Keep target names, IDs, export receipts, test payloads and run-specific results in the project workspace. Generic guidance contains resolver names, contract fields, controlled seed mappings and bounded behavior, not a hardcoded successful-run profile.

## No Full Data Export Policy

| Task Code | Task Name | Rule ID | Applies When | Blocking Condition | Required Action |
|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.NO_FULL_DATA_EXPORT | Any routed create, review, update, duplicate or verification acquisition | Proposed full populated export or a scoped request returning data outside the selected BU scope | Reject that source; use templates, declared GETs and verified current-workflow facts, or a named authorized genuinely scoped route; report exact remaining gaps |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.NO_FULL_DATA_EXPORT | Any routed function preparation, duplicate or verification acquisition | Proposed full populated export or a scoped request returning data outside the selected BU scope | Reject that source; use templates, declared GETs and verified current-workflow facts, or a named authorized genuinely scoped route; report exact remaining gaps |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.NO_FULL_DATA_EXPORT | Any routed override preparation, duplicate or verification acquisition | Proposed full populated export or a scoped request returning data outside the selected BU scope | Reject the source; select BUSA_FSM_ADD_OVERRIDE_V1 or BUSA_FSM_PARENT_KEY_V1 with templates/current GETs and profile-appropriate parent facts; no assignment-file export solely for mapping |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.NO_FULL_DATA_EXPORT | Any routed relationship preparation, duplicate or verification acquisition | Proposed full populated export or a scoped request returning data outside the selected party scope | Reject that source; use templates, declared GETs and permitted current party/role facts; report exact remaining gaps |

This is a mandatory user policy for the BU skill family and its delegates. Do not request approval for a full export as a workaround, reuse an earlier full export, or qualify one by locally filtering it. Template/spec exports are allowed because they supply shape without populated setup data. A scoped populated route must be specifically declared, authorized, necessary for a named missing fact and verified in its actual returned rows; it is not the default acquisition step. If no permitted source can resolve a required runtime field, return the exact missing fact and supported next action. This policy does not permit guessed keys, unsupported defaults, skipped preservation checks or claims that all variants have been tested.

## Additive Function Profile Boundary

| Task Code | Task Name | Rule ID | Applies When | Blocking Condition | Required Action |
|---|---|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.ADDITIVE_PROFILE | Adding a controlled function | BUF_FSM_ADD_FUNCTION_V1 eligibility fails, relevant current facts conflict or requested operation changes parent/technical state | Identify the exact failed condition and select supported maintenance evidence; do not impose its saved-key/date/status requirements on an eligible additive request |

Do not present an input omission accepted by the additive profile as proof that a saved field is blank, unchanged or independently verified. Absence of unexposed keys/dates/ConfigurationStatus is a disclosure limit on this profile; it becomes a blocker only when the selected operation or an explicit strict verification/preservation request needs that exact evidence.


## Dependent Additive Profile Boundaries

| Task Code | Task Name | Rule ID | Applies When | Blocking Condition | Required Action |
|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.ADDITIVE_PROFILE | Requested group delta after current-workflow BU creation | BUSA_FSM_ADD_OVERRIDE_V1 eligibility fails, current facts conflict or a parent/technical change is requested | Identify the actual failed condition; use supported current-key maintenance only when required; do not block qualified preparation for omitted generated codes/dates |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.FIRST_LINK_PROFILE | First active named-provider relationship in the qualified current workflow | SPR_FSM_ADD_RELATIONSHIP_V1 eligibility fails, previous write is uncertain, known external change exists or requested behavior exceeds the tested pair/N route | Require the exact missing contract/state for that operation; an unavailable saved-row read alone does not block an eligible first submission |

Review evaluated rule results, not just planner readiness. Do not convert an unknown saved value into an invented value or a failed-read absence claim; record permitted omission and first-submission assurance in the normal Task Hook preview. Normal preservation requests use intended parent values and available before/after comparisons; explicitly disclose unexposed-field certification limits.
