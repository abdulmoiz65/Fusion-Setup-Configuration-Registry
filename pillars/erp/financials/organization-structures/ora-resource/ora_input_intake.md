# Organization Structures Input Intake

Collect named configuration fields. Do not accept vague phrases such as “ABC details” or “PQR details” as configuration.

## Accepted Input Formats

| Task Code | Task Name | Input Format | What Must Be Provided | Applies To |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Form or named field list | Create or update intent; Business Unit Name; an existing Default Reference Set, or Create New with Set Code and Set Name; optional new-set Description; optional Active choice, ledger/legal entity, manager/location and explicitly supplied effective dates or organization code | Create or update Business Unit |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Form or named field list | Business Unit; Business Function Code; selected primary ledger/legal entity or an instruction to use the BU's verified foundation for financial functions; use explicit active-workflow parent decisions for BUF_FSM_ADD_FUNCTION_V1 | Assign a function to a Business Unit |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Form or named field list | Client Business Unit; Provider Business Unit; upstream Business Function Code; downstream Business Function Code; `AnyProvidersFlag` only when supported by the inspected import contract | Define a service-provider relationship |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Form or named field list | Business Unit; Reference Data Object; Reference Data Set Code | Assign a set to a reference data object |

## Canonical Concepts and Accepted Aliases

| Task Code | Task Name | Canonical Concept | Accepted Aliases | Handling |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Business Unit Name | Business Unit; BU Name | Resolve by name only after an exact unique match; do not ask for an Oracle-generated ID |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Default Reference Set | Default Set; Reference Data Set; Set Code | Treat an existing-set selection and a new-set request as different choices |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Reference Set Code | New Set Code | Require with New Reference Set Name only when Create New is selected |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Reference Set Name | New Set Name | Require with New Reference Set Code only when Create New is selected |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Create or Update Intent | Request Type; Action | Use Create only after the exact-name idempotency lookup returns New; do not infer an update route |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Assigned Primary Ledger | Primary Ledger; Ledger | Do not treat a secondary ledger or reporting currency as the primary ledger |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Default Legal Entity | Legal Entity; Default LE | Resolve by exact unique business name; do not ask for a generated ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Business Unit Functions | Business Functions; Enabled Functions | Collect the function code as a list; derive Module ID from the supplied Business Function seed data only after an exact code match |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Module ID | Business Function ID | Do not collect as free-form input; derive from the matched Business Function seed-data code |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Client Business Unit | Client BU | Resolve by exact unique name |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Provider Business Unit | Service Provider BU; Provider BU | Resolve by exact unique name |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Upstream Business Function | Upstream Function | Resolve an exact controlled function code; do not infer a client-BU assignment requirement from the reviewed source. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Downstream Business Function | Provider Function; Downstream Function | Resolve an exact controlled function code. When `AnyProvidersFlag = N`, this function must be assigned to the named provider BU. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Any Providers Flag | AnyProvidersFlag | Accept only `Y` or `N` when the fresh task contract exposes the field. Default only an omitted flag to N after the matching contract exposes it; preserve explicit Y/N and do not manufacture a named-provider equality rule for Y. |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference Group Name | Reference Data Object; Object; Reference Object | Require one of the supplied controlled ReferenceGroupName values for each requested assignment |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference Data Set Code | Set Code; Reference Set | Resolve only if exactly one documented set matches |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Organization Code | OrganizationCode | Select BUSA_FSM_ADD_OVERRIDE_V1 for an eligible current-workflow override and leave unprovided technical codes blank; otherwise BUSA_FSM_PARENT_KEY_V1 uses exact permitted saved keys; never infer a suffix |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Name | Assignment Name | Use the resolved BU name when the matching task template confirms its parent-BU Name mapping; do not solicit an unrelated assignment-name value |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---:|---:|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.INTAKE | step | 1 | collect_input | complete->BU.VALIDATE | none | stop | A Business Unit create or update is requested |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.INTAKE | step | 1 | collect_input | complete->BUF.VALIDATE | none | stop | A Business Unit function assignment is requested |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.INTAKE | step | 1 | collect_input | complete->SPR.VALIDATE | none | stop | A service-provider relationship is requested |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.INTAKE | step | 1 | collect_input | complete->BUSA.VALIDATE | none | stop | A Business Unit set assignment is requested |

## Body Field Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | A user supplies an Oracle-generated identifier instead of a resolvable name or code | Treat it as optional evidence; use the documented business field and flag an ambiguous match |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Create New Default Reference Set is selected | Collect Set Code and Set Name; Description remains optional |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | An existing Default Reference Set is selected | Collect the exact Set Code; collect Set Name when supplied and require it to match the same resolved set |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | A new Default Reference Set is requested | Route set creation as a separate prerequisite, then verify the created set before it is used by the BU; do not embed unverified set creation in the BU request |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A user supplies a phrase rather than named function, ledger, and legal-entity fields | Stop intake and request the named fields |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | A user supplies only a provider or only a client, or supplies only one function direction | Stop intake and request both Business Units plus named upstream and downstream functions |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A supplied Business Function Code exactly matches the developer-provided seed data | Derive the corresponding Module ID; do not ask the user for the generated/internal ID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Matching assignment layout or runtime parent value is unavailable | Select the operation-specific packaged BUSA profile before identifying actual unsupported columns or missing required values; eligible additive omissions are not blockers; no full-export fallback |
  <!-- -->

## Independent and Combined Requests

| Task Code | Task Name | Requested Stage | Intake and Handoff |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Create only | Require name and a resolved existing set or new code/name pair; do not require business functions, provider relationships, all reference groups, generated IDs or a populated data export |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Assign after creation | Accept the saved BU name and requested controlled function codes; resolve the BU now and collect compatible financial foundation values when required |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Set overrides after creation | Accept saved BU name, requested reference group/object and set code; resolve only those requested groups |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Relationship after prerequisites | Accept saved party names and directed controlled functions; select SPR_FSM_ADD_RELATIONSHIP_V1 for its eligible first current-workflow link, otherwise supported maintenance evidence; do not repeat BU creation |

For a combined request, the parent skill sequences these stages. Carry explicit user decisions and verified receipts within the current workflow, while re-reading any saved keys/attributes needed by a later contract. Do not import values from historical runs or assume every initially supplied value is the saved value.

For dependent stages, do not solicit generated keys or dates solely because their columns appear in a template. Select the independently tested task profile in ora_bulk_intake.md first. Carry explicit parent business decisions and reviewed stage receipts in the active workflow; missing user choices or conflicting fresh facts remain real gaps.
