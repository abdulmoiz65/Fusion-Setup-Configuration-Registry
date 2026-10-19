# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent balance definition | LegislativeDataGroupName, BalanceCode, BalanceName, ReportingName, BalanceCategoryCode, BalanceUOM | Stop preparation | Provide the parent balance values and validate them in the target LDG | Creating or updating PayrollBalanceDefinition | |
| Monetary balance currency | CurrencyCode | Stop preparation until the target contract confirms the currency requirement | Provide the target currency when the selected balance UOM and design require it | BalanceUOM is Money or target metadata requires currency | |
| Defined balance child | BalanceId or BalanceCode with LegislativeDataGroupName, BalanceDimensionCode | Stop preparation | Provide the parent Balance Type ID or balance code and a valid target-LDG dimension | A DefinedBalance record is included | |
| Classification feed child | BalanceId or BalanceCode with LegislativeDataGroupName, ElementClassificationCode, AddSubtract | Stop preparation | Provide the parent Balance Type ID or balance code and a compatible classification feed | A BalanceClassification record is included | |
| Element feed child | BalanceId or BalanceCode with LegislativeDataGroupName, EffectiveStartDate, ElementCode, InputValueCode, AddSubtract | Stop preparation | Provide the parent Balance Type ID or balance code and a compatible element input-value feed | A BalanceFeed record is included | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A child record supplies BalanceCode with LegislativeDataGroupName instead of BalanceId | Valid | Use the documented alternate parent key and continue with dependency readiness | |
| A child record supplies direct BalanceId and omits SourceSystemOwner and SourceSystemId | Valid | Continue with dependency readiness | |
| A child record uses BalanceId(SourceSystemId) | Conditional | Verify the source-system cross-reference contract before use | resolve_balance_source_system_reference |
| A display name is supplied for an LDG, category, dimension, element, input value, or classification | Lookup required | Resolve exactly one target-LDG value before preparing HDL | resolve_balance_reference_values |
| The load changes seeded and custom balance feeds in one file | Invalid | Split the changes into separate HDL files | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| BalanceName uniqueness | Reject a duplicate balance name in the applicable target scope | PayrollBalanceDefinition is created or renamed | find_balance_by_exact_name |
| BalanceCode child linkage | Accept BalanceCode with LegislativeDataGroupName as the documented alternate child parent key | Any child record is included | |
| Source-system identifiers | Treat SourceSystemOwner and SourceSystemId as optional; do not reject a direct ID-based record because either is absent | All four documented business objects | |
| Balance UOM compatibility | Reject a feed whose input-value UOM is incompatible with the balance UOM | A BalanceFeed or BalanceClassification is included | resolve_balance_reference_values |
| BalanceFeed effective dates | Reject a proposed feed whose first start date or final end date changes an existing feed, or whose start date is after an object that refers to it | A BalanceFeed is created or updated | resolve_balance_reference_values |
| Parent business-object contract | Require the exact PayrollBalanceDefinition discriminator and the validated parent columns before import | A parent balance definition is prepared | resolve_balance_metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BAL.VALIDATE_INPUT | decision | 10 | validate_input | valid->BAL.LOOKUP_EXISTING;invalid->BAL.HANDLE_INPUT_ERROR | none | stop | A Balance Definitions HDL request is prepared |
