# Organization Structures Defaulting Rules

Apply only documented or developer-supplied defaults. Never default ledger, legal-entity, relationship parties, business functions, or set-assignment decisions.

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Classification | FUN_BUSINESS_UNIT | Classification is absent; developer requirement | No | None |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | OrgInformationContext | FUN_BUSINESS_UNIT | OrgInformationContext is absent; developer requirement | No | None |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | ClassificationCode | FUN_BUSINESS_UNIT | ClassificationCode is absent; developer requirement | No | None |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Status | A | Status is absent; developer requirement | No | None |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Default Reference Set | User-provided existing set after exact unique lookup | An existing Default Reference Set is provided | No | None |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | New Reference Set Description | Omit from native POST | Create New is selected and no description is provided | No | No fabricated description |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Assigned Primary Ledger | No default | Always | No; select explicitly or resolve the BU foundation when the user requests its verified foundation | None |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Default Legal Entity | No default | Always | No; select explicitly or resolve the BU foundation when the user requests its verified foundation | None |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Module ID | Exact Business Function seed-data ID | A supplied function code has one exact controlled match | No | None |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | ConfigurationStatus | Y | ConfigurationStatus is absent; developer requirement | No | None |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Provider or client Business Unit | No default | Always | No | None |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | ClientOrganizationCode | No universal default | SPR_FSM_ADD_RELATIONSHIP_V1 permits omission; outside it use exact required saved value from supported evidence | No; preserve an explicit value | Select the tested profile first; never derive a suffix without an independently proven target contract |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | ProviderOrganizationCode | No universal default | SPR_FSM_ADD_RELATIONSHIP_V1 permits omission; outside it use exact required saved value from supported evidence | No; preserve an explicit value | Select the tested profile first; never derive a suffix without an independently proven target contract |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | AnyProvidersFlag | N | AnyProvidersFlag is absent and the fresh task contract exposes the field | Yes; preserve explicit Y or N | None |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference Data Set Code | Business Unit default set is initially assigned to each reference data object | Set-assignment task is opened; Oracle implementation guidance | No; the user may change individual object assignments | None |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OrganizationCode and Name | No default | CSV/import execution; select BUSA profile first | No | BUSA_FSM_ADD_OVERRIDE_V1: exact saved Name and omitted unprovided code; BUSA_FSM_PARENT_KEY_V1: exact saved keys; no generated suffix |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---:|---:|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.DEFAULT | step | 3 | apply_default | ready->BU.IDEMPOTENCY;invalid->BU.BLOCKED | BU.VALIDATE | stop | Input validation passes; apply only an exactly resolved existing Default Set and documented Business Unit defaults when the user did not supply a value. A Create New request remains blocked until it is created through its separate approved route and re-resolved. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.DEFAULT | step | 3 | apply_default | ready->SPR.DEPENDENCY;invalid->SPR.BLOCKED | SPR.VALIDATE | stop | Input validation passes; select SPR_FSM_ADD_RELATIONSHIP_V1 and omit unprovided party keys/dates under its tested contract, or preserve supported maintenance keys. Never guess a suffix. Default omitted AnyProvidersFlag to N only in its matching contract; qualified active first link uses Y. |
  <!-- -->

## New BU Technical Values

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | OrganizationCode | Leave blank | Exact zero-match new BU and current matching template; no explicit code supplied | No | Server resolves the omitted create value; never synthesize a suffix from another task or prior data |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | EffectiveStartDate and EffectiveEndDate | Leave blank | New BU and no user dates supplied; current template exposes these columns | No | Server create behavior; do not promise a particular saved effective date |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Primary ledger and legal entity | No default | No financial functions requested; fields omitted | No | Accept omission; resolve explicit foundation values and verify their association when provided |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Other technical or optional fields | Leave unprovided values blank | New BU with no documented default or selected user value | No | Do not copy flags, currency, short code, audit or segment values from another BU |

These create omissions do not automatically qualify existing-parent maintenance or dependent keys. Each dependent additive profile below has its own independently tested contract. Explicit dates/codes require current contract validation. Template shape alone cannot prove that a user value persisted.

## Additive Function Technical Omissions

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Parent OrganizationCode and effective dates | Leave blank | BUF_FSM_ADD_FUNCTION_V1 eligibility passes and these technical fields were not explicitly supplied | No | Tested omission contract in ora_bulk_intake.md; not a statement of saved values |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Parent DefaultSetCode | Current-workflow explicit set decision after exact set lookup | Eligible profile and no requested parent/default change | No | Current workflow intent; independently saved default-set verification remains limited |

Do not transfer the function omission rule to general maintenance or other dependent tasks; the set and relationship profiles below qualify their omissions independently. Explicit technical/parent changes leave this profile and require their supported contract. ConfigurationStatus Y remains the existing assignment input default; its unexposed saved value is not fabricated.


## Independently Tested Dependent-Task Omissions

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Parent/assignment OrganizationCode and effective dates; SysEffectiveDate | Leave blank | BUSA_FSM_ADD_OVERRIDE_V1 eligibility passes and values were not supplied | No | Independent tested omission contract in ora_bulk_intake.md; not a saved-field claim |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Parent/party organization codes and effective dates; SysEffectiveDate | Leave blank | SPR_FSM_ADD_RELATIONSHIP_V1 eligibility passes and values were not supplied | No | Independent tested omission contract in ora_bulk_intake.md; never manufacture a suffix/date |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | ActiveFlag | Y | Eligible first active named-provider relationship; matching template field | No | Documented intended value; no implicit reactivation or change to an existing relationship |

These omissions have their own evidence and eligibility. They do not originate from copying the BU creation or function contract. Retain active-workflow DefaultSetCode decisions and verified financial foundation; hidden saved attributes remain verification limits rather than universally required defaults.
