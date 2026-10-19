# Configure Payroll Legislations Input Validation

This task uses the task-level FSM CSV contract identified by PAY_CONFIGURE_PAYROLL_LEGISLATION. It supports only FSM export and FSM import. Package validation checks the task contract; it does not infer a business operation, transform supplied rows, or derive legislation-specific values.

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| Task identity and CSV export/import support | Task SKILL.md and setup-task catalog | Generated task metadata | Confirmed | Repository state 2026-08-13 | Does not define record-level mandatory values or business operations. |
| FSM package file set, headers, types, and import sequencing | Configure Payroll Legislations FSM template package | Target-environment FSM template | Observed | Fusion release 11.13.26.10.0; exported 2026-08-12 | The template does not establish business values, defaults, update semantics, or delete semantics. |
| Import approval and immutable-archive control | User implementation direction and core.data-loader | Implementation policy | Confirmed | 2026-08-13 | Applies only after the import source is complete and validated. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested FSM operation | Export current task data or import a supplied FSM archive | Stop and request one operation | Identify export or import; do not infer a create, update, delete, or restoration operation | Always | |
| Import source archive | One complete ZIP containing ASM_SETUP_CSV_METADATA.xml and the task CSV files | Stop before immutable preview | Supply a completed FSM archive that represents the user's intended configuration | FSM import is requested | |
| Source authority for populated values | User-supplied FSM archive, explicit user-supplied row data, or documented Add defaults | Stop affected package preparation | Supply the values and their functional authority; do not derive them from another legislation or package | A new or changed CSV row is being prepared | |
| HCM-product Add default | User-supplied LegislationCode and no user-supplied ORA_PAY_HCM_PRODUCT rows | Stop affected package preparation | Apply the documented one-row baseline only; do not default LegislationCode or replace user-supplied HCM-product rows | Add is explicitly requested | |
| Relationship-type mapping Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_PAYROLL_RELATIONSHIP_TYPE_MAPPING rows | Stop affected package preparation | Apply the documented nine-row mapping set; do not default LegislationCode or replace user-supplied mapping rows | Add is explicitly requested | |
| Payroll-relationship-rule Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE rows | Stop affected package preparation | Apply the documented eight-row baseline only; do not default LegislationCode or replace user-supplied payroll-relationship-rule rows | Add is explicitly requested | |
| Balance-dimension Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_BALANCE_DIMENSION rows | Stop affected package preparation | Apply the documented 365-row baseline only; do not default LegislationCode or replace user-supplied balance-dimension rows | Add is explicitly requested | |
| Balance-type Add default | User-supplied LegislationCode, user-supplied CurrencyCode, and no user-supplied ORA_LEGISLATION_BALANCE_TYPE rows | Stop affected package preparation | Apply the documented 28-row baseline only; do not default LegislationCode or CurrencyCode, replace user-supplied balance-type rows, or populate the four confirmed blank CurrencyCode cells | Add is explicitly requested | |
| Component-group Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_COMPONENT_GROUP rows | Stop affected package preparation | Apply the documented six-row baseline only; do not default LegislationCode or replace user-supplied component-group rows | Add is explicitly requested | |
| Element-classification Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_ELEMENT_CLASSIFICATION rows | Stop affected package preparation | Apply the documented 119-row baseline only; do not default LegislationCode or replace user-supplied element-classification rows | Add is explicitly requested | |
| Payment-type Add default | User-supplied LegislationCode and no user-supplied ORA_LEGISLATION_PAYMENT_TYPE rows | Stop affected package preparation | Apply the documented four-row baseline only; do not default LegislationCode or replace user-supplied payment-type rows | Add is explicitly requested | |
| FSM package contract | ASM_SETUP_CSV_METADATA.xml and the exact observed file and header set | Stop before immutable package preview | Rebuild from the target task template; do not add, rename, omit, or derive a CSV column | Package validation or FSM import preparation | |
| Import authority | Final immutable ZIP SHA-256 and a later standalone user message exactly approve | Stop before upload or initiation | Complete core.data-loader and Task Hook validation, show the hash, then wait for approval | FSM import is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| FSM export is requested | Verify | Route to shared.setup-export.task-level-export using this task code and name | |
| FSM import is requested | Verify | Route the exact final ZIP through core.data-loader and its Task Hook approval lifecycle | |
| A CSV section is populated | Verify | Confirm that it belongs to the task package and retains its exact header order | |
| A populated value has no user-supplied functional source | Blocked | Request the functional source before packaging | |
| The HCM-product Add default applies | Verify | Require one user-supplied LegislationCode, no HCM-product rows from the user, and the exact documented one-row baseline | |
| The relationship-type mapping Add default applies | Verify | Require one user-supplied LegislationCode, no mapping rows from the user, and all nine documented SystemPersonType values exactly once | |
| The payroll-relationship-rule Add default applies | Verify | Require one user-supplied LegislationCode, no payroll-relationship-rule rows from the user, and the exact documented eight-row baseline | |
| The balance-dimension Add default applies | Verify | Require one user-supplied LegislationCode, no balance-dimension rows from the user, and the exact documented 365-row baseline | |
| The balance-type Add default applies | Verify | Require one user-supplied LegislationCode, one user-supplied CurrencyCode, no balance-type rows from the user, and the exact documented 28-row baseline | |
| The component-group Add default applies | Verify | Require one user-supplied LegislationCode, no component-group rows from the user, and the exact documented six-row baseline | |
| The element-classification Add default applies | Verify | Require one user-supplied LegislationCode, no element-classification rows from the user, and the exact documented 119-row baseline | |
| The payment-type Add default applies | Verify | Require one user-supplied LegislationCode, no payment-type rows from the user, and the exact documented four-row baseline | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Package includes only the observed task files | Accept only ASM_SETUP_CSV_METADATA.xml and the observed task CSV filenames; reject missing or unexpected files | Package validation | |
| CSV headers exactly match the task template | Reject reordered, renamed, added, or omitted columns | Every included CSV | |
| ORA_PAY_HCM_PRODUCT ApplicationId type | Apply 801 only when the documented default applies; reject a non-integer supplied value | An explicitly requested parent-row default is applied | |
| Template value types | Treat all columns other than ApplicationId as strings because the metadata declares string types; do not invent length, enum, or required-value constraints | A CSV value is supplied | |
| Task metadata identity | Require ObjectShortName PAY_CONFIGURE_PAYROLL_LEGISLATION and ObjectType TASK in ASM_SETUP_CSV_METADATA.xml | Package validation | |
| No inferred transformation | Reject an attempt to derive, copy, rename, filter, or replace row values without explicit user-supplied functional authority | Package preparation | |
| HCM-product default shape | Generate exactly one baseline row in the observed header order. LegislationCode must equal the user input; ApplicationId=801, SeededFlag=N, SeededStatus remains blank, InstalledFlag=Y, PayrollLicense remains blank, AddressStyleCode=POSTAL_ADDR, and AddressValidationFlag=Y | The HCM-product Add default applies | |
| Relationship-type mapping default shape | Generate only the documented columns and values: ViewInstanceName=PayRelationshipTypeMapVO; GroupingKey=<SystemPersonType>,<LegislationCode>,<RelationshipTypeName>; supplied LegislationCode; and the documented nine relationship mappings | The relationship-type mapping Add default applies | |
| Payroll-relationship-rule default shape | Generate exactly eight baseline rows in the observed header order. Every LegislationCode must equal the user input; every RuleMode and RuleType value must match the documented baseline | The payroll-relationship-rule Add default applies | |
| Balance-dimension default shape | Generate exactly 365 baseline rows in the observed header order. Every LegislationCode must equal the user input; every GroupingKey must retain the baseline shape with its final component equal to that input; LegislativeDataGroupId, DimensionUsageId, and BalanceDimensionId remain blank | The balance-dimension Add default applies | |
| Balance-type default shape | Generate exactly 28 baseline rows in the observed header order. Every LegislationCode and GroupingKey legislation component must equal the user input; 24 CurrencyCode cells must equal the currency input; the four documented CurrencyCode cells remain blank; LegislativeDataGroupId and BalanceTypeId remain blank | The balance-type Add default applies | |
| Component-group default shape | Generate exactly six baseline rows in the observed header order. Every LegislationCode and GroupingKey legislation component must equal the user input; DeductionGroupId remains blank | The component-group Add default applies | |
| Element-classification default shape | Generate exactly 119 baseline rows in the observed header order. Every LegislationCode must equal the user input; every GroupingKey must retain the baseline shape with its final component equal to that input; LegislativeDataGroupId and ClassificationId remain blank | The element-classification Add default applies | |
| Payment-type default shape | Generate exactly four baseline rows in the observed header order. Every LegislationCode and GroupingKey legislation component must equal the user input; PaymentTypeId remains blank | The payment-type Add default applies | |
| Mutable template metadata | Do not infer whether ProcessName, timestamps, ProcessStatus, export flags, or similar metadata values may be changed for an import | Package preparation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPL.VALIDATE_INPUT | step | 1 | validate_input | valid->CPL.RESOLVE_FSM_READINESS;invalid->RETURN_ISSUES | none | stop | Always |
