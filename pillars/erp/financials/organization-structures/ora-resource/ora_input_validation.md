# Organization Structures Input Validation

Data-model nullability is persistence evidence only. It does not by itself make an Oracle-generated identifier an end-user input requirement.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Business Unit | Business Unit Name | Block preview | Ask for Business Unit Name |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Default Set | Existing Default Reference Set that resolves uniquely, or New Set Code and New Set Name followed by successful set creation and re-lookup | Block preview | Ask for an existing set or a complete new-set pair, then require exact lookup evidence |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Financial business-function assignment | Existing Business Unit; Assigned Primary Ledger; Default Legal Entity; Business Unit Functions | Block preview when the selected function generates financial transactions | Obtain and exactly resolve the BU, ledger, and legal entity, then compare the resolved IDs for compatibility |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Relationship identity | Client Business Unit; Provider Business Unit; Upstream Business Function; Downstream Business Function | Block preview | Request both named BUs and a directed function pair before attempting a relationship design review |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Set assignment | Business Unit; Reference Data Object; Reference Data Set Code | All three business values are required; technical fields follow the current matching import contract | Request the named assignment values |

## Field Validation

| Task Code | Task Name | Check | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Business Unit Name exceeds 240 characters; source table HR_ORGANIZATION_UNITS_F_TL, column NAME, VARCHAR2(240), Not-null Yes | Reject before preview or save |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Set Code exceeds 30 characters; source table FND_SETID_SETS, column SET_CODE, VARCHAR2(30), Not-null Yes | Reject before preview or save |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Set Name exceeds 80 characters; source table FND_SETID_SETS, column SET_NAME, VARCHAR2(80), Not-null Yes | Reject before preview or save |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Set Description exceeds 2000 characters; source table FND_SETID_SETS, column DESCRIPTION, VARCHAR2(2000), Not-null No | Reject before preview or save |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Set Code or New Set Name is missing when Create New is selected | Reject before preview; both are mandatory for the requested creation path |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Existing Default Set resolves to zero, multiple, or a partial code/name match | Reject before preview; require exactly one active/retrievable set with the supplied exact identifier |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Create New Default Set has not been created by the approved set-management route and re-resolved exactly | Reject before preview; create the set separately, then re-run exact lookup before referencing it in the BU row |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact BU lookup returns more than one candidate, has incomplete paging, or cannot be performed | Reject before preview; do not infer a duplicate state from a partial result |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact BU lookup returns one candidate whose Name, DefaultSetCode, PrimaryLedgerName, LegalEntityName, Status, and every user-supplied comparable field match current saved-state evidence | Classify as `existing-identical`; do not create or import a duplicate. Record a no-op result. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact BU lookup returns one candidate but any comparable desired field differs from current saved-state evidence | Classify as `existing-different`; block creation and require an explicit update decision or a different BU name. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact BU lookup returns zero candidates after complete paging | Classify as `new`; creation/import may proceed only after the Default Set gate passes. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Location is blank | Accept the blank value; do not call `locationsLovV2` or populate `LocationId`. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Location is supplied but does not resolve through `locationsLovV2` to exactly one active/effective `LocationId` for the request date | Reject before preview or import; correct the location name/code or the effective date. Do not select a similarly named location. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Manager is blank | Accept the blank value; do not call `publicWorkers` or populate `ManagerId`. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Manager is supplied but does not resolve through `publicWorkers` to exactly one active `PersonId` | Reject before preview or import; correct the display name/person number. Do not infer a person from a partial name or assignment ID. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Required HCM LOV endpoint is inaccessible, unavailable, incomplete, or lacks the needed REST privilege for a supplied manager or location | Reject before preview or import; obtain the required Public Workers Read Only or Locations List of Values access, or leave the optional field blank by explicit request. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Supplied Business Function Code exceeds 100 characters; source table FUN_BUSINESS_FUNCTIONS_B, column BUSINESS_FUNCTION_CODE, VARCHAR2(100), Not-null Yes | Reject before preview or save |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A Business Function Code does not resolve to exactly one function | Reject as ambiguous or invalid; do not select a function by guesswork. Record target `Enabled`, `GENERATE_FIN_TXN_FLAG`, and `SETUP_API` evidence when the resolver exposes them; do not infer an enabled state. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A supplied Business Function Code is outside the developer-provided seed-data list | Reject before preview; request one of the controlled codes or an approved seed-data update |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Module ID is supplied as user input or differs from the exact seed-data mapping; source table FUN_BU_USAGES, column MODULE_ID, NUMBER(18), Not-null Yes | Reject before preview; derive Module ID from the exact matched code |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Selected BU, primary ledger, or default legal entity resolves to zero or multiple exact matches | Reject before preview; do not derive an ID or select a candidate by name similarity |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Selected function has `GENERATE_FIN_TXN_FLAG = Y` and the resolved BU `PrimaryLedgerId` or `LegalEntityId` does not equal the resolved requested ledger or legal-entity ID | Reject before import; correct the BU foundation or select the compatible ledger and legal entity. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Selected function has `GENERATE_FIN_TXN_FLAG = Y` and either the requested primary ledger or default legal entity is absent | Reject before import; both values are mandatory for this function type. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Same client, upstream function, downstream function, and provider relationship already exists; source table FUN_BU_SERVICE_PROVIDERS, unique key FUN_BU_SERVICE_PROVIDERS_U1 | Identical supported values are a no-op; different values or ambiguous matches block for an explicit maintenance decision. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | `AnyProvidersFlag = N` and the named provider BU does not have the downstream function in current active function-assignment evidence | Reject before import; assign the downstream function to the provider first. Do not require a client/upstream assignment without target evidence. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Exact pair has no approved compatibility evidence, contradicts current target evidence, or requested policy semantics are unresolved | Reject before import. Controlled related-pair seed evidence qualifies SPR_FSM_ADD_RELATIONSHIP_V1; do not require a live table query solely to restate that tested pair. Other behavior must have its own authority; never infer O/M semantics |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | `AnyProvidersFlag` is null, not `Y` or `N`, or the `Y` provider-handling contract is not established by permitted current target evidence | Reject before import; source code supports `Y` and `N` paths only. Do not manufacture a named-provider equality check for `Y`. |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference Data Set Code does not resolve uniquely | Reject as ambiguous or invalid |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | ReferenceGroupName is not in the developer-provided controlled list of 73 names | Reject before preview; request a listed name or an approved list update |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Selected assignment profile does not match the template, or its eligibility/required values fail | Select BUSA_FSM_ADD_OVERRIDE_V1 before demanding maintenance-only keys/dates; otherwise use BUSA_FSM_PARENT_KEY_V1 with exact permitted current values. Block the specific failed condition; no assignment export, guessed suffix or BU recreation |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---:|---:|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.VALIDATE | step | 2 | validate_input | valid->BU.DEFAULT;invalid->BU.BLOCKED | BU.INTAKE | stop | A Business Unit request has been collected |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.IDEMPOTENCY | step | 4 | evaluate_result | new->BU.READY;existing-identical->BU.NOOP;existing-different->BU.BLOCKED;ambiguous->BU.BLOCKED | BU.DEFAULT | stop | Evaluate the exact complete-page Business Unit lookup after set resolution; zero matches require no saved-parent comparison. For an existing candidate compare requested effective attributes using permitted current evidence; enforce the parent no-full-data-export policy. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.VALIDATE | step | 2 | validate_input | valid->BUF.DEPENDENCY;invalid->BUF.BLOCKED | BUF.INTAKE | stop | A Business Unit function request has been collected; validate BUF_FSM_ADD_FUNCTION_V1 eligibility or the selected maintenance contract before treating unexposed parent keys, dates or status as blockers. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.VALIDATE | step | 2 | validate_input | valid->SPR.DEFAULT;invalid->SPR.BLOCKED | SPR.INTAKE | stop | A service-provider request has been collected; select SPR_FSM_ADD_RELATIONSHIP_V1 before technical-key/date and complete relationship-read gates; classify first-submission assurance separately from globally read absence; otherwise require supported maintenance evidence. |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.VALIDATE | step | 2 | validate_input | valid->BUSA.READY;invalid->BUSA.BLOCKED | BUSA.INTAKE | stop | A set-assignment request has been collected; select BUSA_FSM_ADD_OVERRIDE_V1 before maintenance-only key/date gates, verify current group/set/assignment state and preserve requested scope; otherwise validate BUSA_FSM_PARENT_KEY_V1 with its exact current values. |
## Ledger-to-Legal-Entity Association Validation

`BU.LEDGER_LE_ASSOCIATION` is a blocking rule for Business Unit creation and financial-function assignment. When both ledger and legal entity are selected, or a financial function requires them, resolve both exactly, then require `verify_ledger_legal_entity_association` to find exactly one item matching the resolved LegalEntityId and requested legal-entity name in the complete `legalEntitiesLOV` `LedgerFinder` response for the resolved LedgerId. A valid individual ledger LOV result, legal-entity name lookup, or stored BU foundation is insufficient by itself.

## Optional Manager and Location Validation

`BU.OPTIONAL_HCM_REFERENCES` applies only when a Business Unit manager or location is supplied. Resolve manager to one active `PersonId` through `publicWorkers` and location to one active/effective `LocationId` through `locationsLovV2`, using the request effective date. These endpoints are identity lookups only: they do not establish manager-role eligibility, reporting ownership, location-to-ledger compatibility, or ledger-to-legal-entity association. Blank values are valid and remain blank.

  <!-- -->

## New BU and Sequential Handoff Validation

| Task Code | Task Name | Check | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact complete-name lookup is zero and a fresh matching template/default set are available | Allow the template-based New BU path; no populated BU export, existing parent row or historical create profile is required |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | OrganizationCode or effective dates are omitted on a New BU | Leave them blank under the create contract; do not invent the emitted key convention or a saved date; explicit values still require contract validation |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | No financial functions requested and ledger/legal entity omitted | Accept omission; do not default a financial foundation or require an association export |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | A ledger or legal entity is supplied | Resolve each supplied identity exactly; verify the LedgerFinder association when both are present; financial-function stages require both compatible values |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Existing candidate has a requested attribute not exposed by available evidence | Block an identical/no-op or update claim for that field; current LOV identity alone is not a complete comparison |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Earlier BU create is in-progress, failed, uncertain or not verified | Stop this dependent stage; finish/reconcile the recorded request and exact BU lookup without duplicate creation |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Earlier BU create has not been verified | Stop the override stage; resolve a saved BU before mapping assignments |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Party creation or a required provider/downstream function assignment is not verified | Stop the relationship stage; preserve earlier completed stages and report the actual missing dependency |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Read used setIdAssignmentsSet or a default set to infer BU override absence | Reject the inference; use setIdAssignmentsBusinessUnit with determinant BU and exact group/BU matching |

Templates prove layout only. A log proves processing of reported rows, not every unreported business value. Never mark a rule passed from registry readiness, an HTTP error, a partial page, a simulation or a different environment's data. Label controlled simulations and unverified variants explicitly.

## Additive Function Versus Maintenance Readiness

| Task Code | Task Name | Check | What Happens |
|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF_FSM_ADD_FUNCTION_V1 eligibility passes | Accept its name-linked parent and technical omissions without a missing-field/readiness waiver; do not require a populated parent export solely to prepare this route |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | ConfigurationStatus is not exposed by module discovery | Do not block eligible new assignment solely for this missing read; validate requested/default Y as input and disclose saved-value verification limits |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Existing function presence but complete comparable status unavailable | Do not claim identical/no-op or silently change an existing configuration; select a supported explicit maintenance decision and its relevant evidence |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Missing active-workflow business decision, nonmatching template, technical change or explicit strict preservation request | Report the specific contract/input/state gap outside the additive profile; never fabricate a value or fetch a full export |


## Set Override and Relationship Profile Readiness

| Task Code | Task Name | Check | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA_FSM_ADD_OVERRIDE_V1 eligibility passes | Accept its minimal matching parent and name-linked assignment with blank unprovided keys/dates; no missing-field waiver or populated export required; run current assignment/no-op and before/after preservation checks |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR_FSM_ADD_RELATIONSHIP_V1 eligibility passes | Accept tested named-provider pair and blank technical keys/dates; record bounded first-submission assurance and independent saved-row limits without inventing empty-state evidence or requiring a read-gap waiver |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Existing parties/relationship, uncertain prior write, known external change, different pair/flag or strict global verification requested | Leave the first-submission profile; obtain the exact required current-state/contract evidence before mutation; a failed read cannot qualify a duplicate no-op or arbitrary maintenance |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Requested assignment is already saved with the intended set | Record current-read no-op and do not import a duplicate delta; unavailable/unexposed status is not equality evidence |

A standard instruction to preserve the default set and other assignments is handled by the bounded parent payload plus available state comparisons. Do not interpret it as a demand for independent certification of every unexposed technical field; disclose exact verification limits. Explicit field-level certification or an actual conflicting fact still requires that evidence.
