# Reference Lookups

All live lookup operations are read-only. The attached source identifies repository-derived UI service evidence but does not authorize its use as a production contract;obtain approved target-pod evidence before relying on an operation.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_ldg_by_exact_name | LDG identity is needed | LegislativeDataGroupId or LDG name | not required for the name-based FSM import: workflow-approved read-only LDG lookup | LegislativeDataGroupId; Name; LegislationCode | ID direct or exactly one name match | LegislativeDataGroupId; LegislativeDataGroupName; LegislationCode | Stop with a field-specific no-match or ambiguity result |
| resolve_consolidation_group_by_ldg | A Consolidation Group restriction is supplied | ConsolidationSetId or name; selected LegislativeDataGroupId | not required for the name-based FSM import: workflow-approved read-only Consolidation Group lookup | ConsolidationSetId; ConsolidationSetName; LegislativeDataGroupId | ID direct or exactly one name match in the LDG | ConsolidationSetId; ConsolidationSetName | Stop with a field-specific no-match, ambiguity, or compatibility result |
| resolve_payroll_by_ldg | Payroll context is supplied or required | PayrollId or name; selected LegislativeDataGroupId | not required for the name-based FSM import: workflow-approved read-only Payroll lookup | PayrollId; PayrollName; LegislativeDataGroupId; effective payroll context | ID direct or exactly one compatible name match | PayrollId; PayrollName | Stop with a field-specific no-match, ambiguity, or compatibility result |
| resolve_report_category | Category is supplied | Category code or display value | Category is not included in this requested import; direct lookup is not required | Lookup code; meaning; active status | Confirmed code or exactly one display-value match | Category; CategoryMeaning | Stop with a field-specific no-match or ambiguity result |
| evaluate_balance_exception_for_fsm | Included exceptions are supplied | UI-supplied exception name; selected LegislativeDataGroupId; LegislationCode | Shared REST client `GET /hcmRestApi/redwood/11.13.18.05/payrollGeneric/payrollGenericQuery` using the HAR-captured `BalanceExceptionUI_BalanceExceptionVO` contract below | BalExceptionId; BaseBalExceptionName; BalExceptionName; BalanceName; DimensionName; LegislativeDataGroupId; LegislationCode; seeded/shared applicability | Exactly one exact-name match that is LDG-owned, or seeded/shared and compatible with the target legislation | BalExceptionId; BaseBalExceptionName; resolution provenance; FSM child binding | Stop on no match, ambiguity, incompatible legislation, or duplicate selection |
| verify_report_task_template_export | FSM import is requested | Task code PAY_MANAGE_BALANCE_EXCEPTION_REPORTS; source/target environment | POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports; current response schema not required for the name-based FSM import until captured | Process ID; FileContent; ProcessLog; ZIP filename; SHA-256 hash; CSV headers | Confirm current task-specific successful template export | Template ZIP hash; CSV schema; process status; ProcessLog | Stop if unavailable, failed, ambiguous, or not task-specific |

## Task Nodes

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| resolve_ldg_by_exact_name | LDG ID is absent and an LDG display name is supplied | LegislativeDataGroupId or LDG name | FSM name-based import accepts the LDG name; direct lookup is not required;repository evidence names LDGLOV/getall_legislativeDataGroupsLOV | LegislativeDataGroupId;Name;LegislationCode | ID is accepted directly;otherwise Name must return exactly one match | LegislativeDataGroupId;LegislativeDataGroupName;LegislationCode | Stop with a field-specific no-match or ambiguity result | BEXR.RESOLVE-LDG | step | 3 | reference_lookup | resolved->BEXR.RESOLVE-CONSOLIDATION-GROUP;unresolved->RETURN-ISSUES | BEXR.CHECK-DEPENDENCIES | stop | LDG identity must be established |
| resolve_consolidation_group_by_ldg | A Consolidation Group restriction is supplied | ConsolidationSetId or name;selected LegislativeDataGroupId | FSM name-based import accepts the Consolidation Group name; direct lookup is not required;repository evidence names ConsolidationSet/getAllConsolidationSet | ConsolidationSetId;ConsolidationSetName;LegislativeDataGroupId | ID is accepted directly;otherwise exact name must return one match in the selected LDG | ConsolidationSetId;ConsolidationSetName | Stop with a field-specific no-match, ambiguity, or LDG-compatibility result | BEXR.RESOLVE-CONSOLIDATION-GROUP | step | 4 | reference_lookup | resolved->BEXR.RESOLVE-PAYROLL;unresolved->RETURN-ISSUES | BEXR.RESOLVE-LDG | stop | A definition-level Consolidation Group restriction is requested |
| resolve_payroll_by_ldg | A Payroll restriction is supplied or the report will be run | PayrollId or name;selected LegislativeDataGroupId | FSM name-based import accepts the Payroll name; direct lookup is not required;repository evidence names Payroll/getAllPayroll | PayrollId;PayrollName;LegislativeDataGroupId;effective payroll context | ID is accepted directly;otherwise exact name must return one compatible match in the selected LDG | PayrollId;PayrollName | Stop with a field-specific no-match, ambiguity, or LDG-compatibility result | BEXR.RESOLVE-PAYROLL | step | 5 | reference_lookup | resolved->BEXR.RESOLVE-CATEGORY;unresolved->RETURN-ISSUES | BEXR.RESOLVE-CONSOLIDATION-GROUP | stop | Payroll context is required or supplied |
| resolve_report_category | A Category is supplied | Category code or display value | Category is not included in this requested import; direct lookup is not required;repository evidence names BalanceDefinitionUI_HcmLookupPVO | Lookup code;meaning;active status | Code is accepted only when confirmed;otherwise display value must return exactly one allowed code | Category;CategoryMeaning | Stop with a field-specific no-match or ambiguity result | BEXR.RESOLVE-CATEGORY | step | 6 | reference_lookup | resolved->BEXR.EVALUATE-BALANCE-EXCEPTION;unresolved->RETURN-ISSUES | BEXR.RESOLVE-PAYROLL | stop | Category is supplied |
| evaluate_balance_exception_for_fsm | Included Balance Exceptions are supplied | UI-supplied exception name;selected LegislativeDataGroupId;LegislationCode | Use the shared REST client with the contract below; do not use an existing-report or LDG-owned FSM export | BalExceptionId;BaseBalExceptionName;BalExceptionName;BalanceName;DimensionName;LegislativeDataGroupId;LegislationCode;seed/shared applicability | Exactly one exact-name match that is LDG-owned or seeded/shared and compatible with the target legislation | BalExceptionId;BaseBalExceptionName;resolution provenance;FSM child binding | Stop on no match, ambiguity, incompatible legislation, or duplicate selection | BEXR.EVALUATE-BALANCE-EXCEPTION | step | 7 | reference_lookup | resolved->BEXR.APPLY-BASE-NAME-DEFAULT;unresolved->RETURN-ISSUES | BEXR.RESOLVE-CATEGORY | stop | A report definition contains included exceptions |
| verify_report_task_template_export | FSM import is requested | Task code PAY_MANAGE_BALANCE_EXCEPTION_REPORTS;source/target environment | POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports and documented status retrieval;exact current response schema is not required for the name-based FSM import until template export is captured | Process ID;FileContent;ProcessLog;ZIP filename;SHA-256 hash;CSV headers | Confirm task code, current release, successful process, and task-specific ZIP;reject the adjacent Balance Exceptions task template | Template ZIP hash;CSV schema;process status;ProcessLog | Stop if unavailable, failed, ambiguous, or not task-specific | BEXR.VERIFY-FSM-TEMPLATE | step | 8 | reference_lookup | verified->BEXR.APPLY-BASE-NAME-DEFAULT;not_required->BEXR.APPLY-BASE-NAME-DEFAULT;unresolved->RETURN-ISSUES | BEXR.EVALUATE-BALANCE-EXCEPTION | stop | FSM import is requested |

## Lookup Execution Rules

## Balance Exception Resolver Contract

This resource is the shipped resolver specification. It replaces the former
pillar-local helper script.

When `BEXR.EVALUATE-BALANCE-EXCEPTION` applies, use the workflow-approved
shared REST client with a read-only `GET` and retain the response as redacted
project validation evidence:

```text
Endpoint: /hcmRestApi/redwood/11.13.18.05/payrollGeneric/payrollGenericQuery
Header: REST-Framework-Version=9
finder: findByWord;PayRestName=BalanceExceptionUI_BalanceExceptionVO,
  DisplayAttributes=BalExceptionId||DefinedBalanceId||BalExceptionName||ComparisonType||ComparisonValue||BalanceGroupId||BalanceGroupName||BalanceTypeId||BalanceName||DimensionName||VarianceType||FormulaId||VarianceOperator||VarianceValue||SeverityLevel||LegislativeDataGroupId||CreatedBy||CreationDate||LastUpdatedBy||LastUpdateDate,
  AdditionalViewCriteria=searchCriteria,
  ParameterKeys=pLegislativeDataGroupId||pLegislationCode,
  ParameterValues={resolved LDG ID}||{legislation code}
limit: 500
onlyData: true
orderBy: BalExceptionName
```

Evaluate only exact, case-sensitive `BalExceptionName` matches. A match is
eligible when either:

- `LegislativeDataGroupId` equals the resolved target LDG ID (`ldg_owned`); or
- `LegislativeDataGroupId` is empty and `CreatedBy` is
  `SEED_DATA_FROM_APPLICATION` (`seeded_shared`).

Require exactly one eligible match and a nonblank `BalExceptionId`. Record
`BaseBalExceptionName` as the returned `BalExceptionName`, the internal
`BalExceptionId`, the binding type, source LDG ID, balance name, and dimension
as validation provenance. Emit the name as the FSM child natural key and the
resolved ID only in the importer binding field. If an exact case-insensitive
candidate exists but there is no exact-case eligible match, report that as a
case mismatch; otherwise stop for zero or multiple eligible matches. Never ask
the user to provide `BalExceptionId`.

| Situation | What Happens |
|---|---|
| A valid identifier/code is supplied | Retain it and its returned display value;do not perform another lookup solely for display when a denormalized name is already returned. |
| Only a display value is supplied | Require exactly one authoritative match and retain both identifier/code and display value. |
| The selected exception is seeded/shared | Evaluate name and legislation applicability independently of LDG-owned export rows. Retain its seeded/shared provenance and use the evaluator's FSM child binding; never ask the user for `BalExceptionId`. |
| A lookup is undocumented or target-pod evidence is absent | Keep the contract as not required for the name-based FSM import and stop before planning a live operation. Do not use an undocumented UI endpoint as a production API. |
| A reference cannot be resolved for display | Render Unresolved (ID/Code: value);do not invent a display name. |
