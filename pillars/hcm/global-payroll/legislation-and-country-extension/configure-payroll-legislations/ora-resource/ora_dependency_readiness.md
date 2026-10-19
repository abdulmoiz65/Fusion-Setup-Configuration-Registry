# Configure Payroll Legislations Dependency Readiness

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| Target task and importable objects | Configure Payroll Legislations FSM template metadata | Target-environment FSM template | Observed | Fusion release 11.13.26.10.0; exported 2026-08-12 | The template identifies package order, not business dependency semantics for individual values. |
| Export and import routing | Task SKILL.md | Generated task metadata | Confirmed | Repository state 2026-08-13 | The task routes FSM export and import only. |
| Final import approval | User implementation direction and core.data-loader | Implementation policy | Confirmed | 2026-08-13 | Approval does not supply missing business values. |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Requested FSM operation | Identify export or import without inferring the user's business change. |
| 2 | Import source authority | For an import, obtain the completed user-supplied FSM archive or explicit user-supplied values before packaging; documented Add defaults may fill only their declared values. |
| 3 | Exact FSM contract | Preserve the task metadata XML, filenames, column headers, declared types, and metadata-defined ordering. |
| 4 | Import gate | Validate the final immutable ZIP through core.data-loader and Task Hook, display its SHA-256, then wait for the standalone approval message. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CPL-DEP-OPERATION | FSM operation selection | Yes | Always | Verify | User implementation request | | The task has two FSM capabilities and must not infer a business mutation | Specify export or import | Requested FSM operation |
| CPL-DEP-SOURCE | Import source authority | Yes | FSM import is requested | Verify | User-supplied FSM archive or explicit user-supplied functional values | | Prevents unrequested data manipulation or derived configuration | Supply the complete archive or the exact authorized values | Source archive or authorized values |
| CPL-DEP-HCM-PRODUCT-DEFAULT | HCM-product Add default | Conditional | Add is explicitly requested and no ORA_PAY_HCM_PRODUCT rows are supplied | Satisfied | Confirmed one-row baseline and user-supplied LegislationCode | | Provides the confirmed HCM-product values without defaulting the legislation | Supply LegislationCode; user-supplied HCM-product rows override the complete default set | LegislationCode, ApplicationId=801, SeededFlag=N, blank SeededStatus, InstalledFlag=Y, blank PayrollLicense, AddressStyleCode=POSTAL_ADDR, AddressValidationFlag=Y |
| CPL-DEP-REL-TYPE-MAPPING-DEFAULT | Relationship-type mapping Add default | Conditional | Add is explicitly requested and no mapping rows are supplied | Satisfied | Developer-provided JSON mapping set and user-supplied LegislationCode | | Provides the confirmed nine-row mapping set without defaulting the legislation | Supply LegislationCode; user-supplied mapping rows always override the default set | LegislationCode, nine RelationshipTypeName/SystemPersonType pairs, ViewInstanceName, GroupingKey |
| CPL-DEP-RELATIONSHIP-RULE-DEFAULT | Payroll-relationship-rule Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_PAYROLL_RELATIONSHIP_RULE rows are supplied | Satisfied | Confirmed eight-row baseline and user-supplied LegislationCode | | Provides the confirmed payroll-relationship-rule values without defaulting the legislation | Supply LegislationCode; user-supplied payroll-relationship-rule rows override the default set | LegislationCode, eight baseline RuleMode/RuleType rows |
| CPL-DEP-BAL-DIMENSION-DEFAULT | Balance-dimension Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_BALANCE_DIMENSION rows are supplied | Satisfied | Confirmed 365-row baseline and user-supplied LegislationCode | | Provides the confirmed balance-dimension values without defaulting the legislation | Supply LegislationCode; user-supplied balance-dimension rows always override the default set | LegislationCode, 365 baseline rows, GroupingKey with its final component set from LegislationCode |
| CPL-DEP-BAL-TYPE-DEFAULT | Balance-type Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_BALANCE_TYPE rows are supplied | Satisfied | Confirmed 28-row baseline, user-supplied LegislationCode, user-supplied CurrencyCode, and developer-confirmed blank currency rows | | Provides the confirmed balance-type values without defaulting legislation or currency | Supply LegislationCode and CurrencyCode; user-supplied balance-type rows always override the default set | LegislationCode, CurrencyCode on 24 rows, 28 baseline rows, GroupingKey with its legislation component set from LegislationCode |
| CPL-DEP-COMPONENT-GROUP-DEFAULT | Component-group Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_COMPONENT_GROUP rows are supplied | Satisfied | Confirmed six-row baseline and user-supplied LegislationCode | | Provides the confirmed component-group values without defaulting the legislation | Supply LegislationCode; user-supplied component-group rows always override the default set | LegislationCode, six baseline rows, GroupingKey with its legislation component set from LegislationCode |
| CPL-DEP-ELEMENT-CLASSIFICATION-DEFAULT | Element-classification Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_ELEMENT_CLASSIFICATION rows are supplied | Satisfied | Confirmed 119-row baseline and user-supplied LegislationCode | | Provides the confirmed element-classification values without defaulting the legislation | Supply LegislationCode; user-supplied element-classification rows always override the default set | LegislationCode, 119 baseline rows, GroupingKey with its final component set from LegislationCode |
| CPL-DEP-PAYMENT-TYPE-DEFAULT | Payment-type Add default | Conditional | Add is explicitly requested and no ORA_LEGISLATION_PAYMENT_TYPE rows are supplied | Satisfied | Confirmed four-row baseline and user-supplied LegislationCode | | Provides the confirmed payment-type values without defaulting the legislation | Supply LegislationCode; user-supplied payment-type rows always override the default set | LegislationCode, four baseline rows, GroupingKey with its legislation component set from LegislationCode |
| CPL-DEP-SEQUENCE | Import ordering | Yes | More than one FSM section is populated | Satisfied | ASM_SETUP_CSV_METADATA.xml | | Fusion template metadata establishes the observed batch order | Preserve metadata ordering; do not reorder from guessed business relationships | Metadata batch order |
| CPL-DEP-PACKAGE | Target task FSM package | Yes | FSM import preparation | Verify | Target-environment template and final ZIP | | Prevents use of another task's package or invented file layout | Use PAY_CONFIGURE_PAYROLL_LEGISLATION files and metadata only | File set, headers, types, ObjectShortName |
| CPL-DEP-IMPORT | Immutable approval envelope | Yes | FSM import is requested | Blocked until approved | core.data-loader and Task Hook output | | Import may not start without exact archive validation, displayed SHA-256, and current approval | Do not send the archive until the user later replies exactly approve | Immutable ZIP, SHA-256, approval envelope |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Requested FSM operation, applicable source, package contract, and approval stage are satisfied | Yes for the selected FSM export or import route |
| Missing | Requested operation, import source, or final archive is absent | No |
| Blocked | Current approval is absent, or data transformation lacks explicit functional authority | No |
| Package Contract Mismatch | Metadata, file, header, type, or ordering differs from the observed template | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPL.RESOLVE_FSM_READINESS | step | 2 | resolve_dependency | ready->CPL.APPLY_DEFAULTS;blocked->RETURN_ISSUES | CPL.VALIDATE_INPUT | stop | Always |
