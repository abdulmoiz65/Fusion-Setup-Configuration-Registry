# Values Defined by Criteria HDL Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target HDL metadata | Export Values Defined by Criteria attributes from View Business Objects and retain the target header contract. |
| 2 | LDG and value definition group | Confirm the target LDG and existing value definition group. |
| 3 | Criterion references | Confirm required database items and value sets before criteria reference them. |
| 4 | Calculation references | Confirm calculation type, UOM, currency, periodicity, multiplier or condition, rate definition, and other referenced artifacts as applicable. |
| 5 | Hierarchy design | Build root, criteria, literal, leaf, and CalculationValues rows in dependency order with a tested default path. |
| 6 | Loader readiness | Validate the immutable HDL artifact in nonproduction using the owning core.data-loader workflow before any production load. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| VBC.METADATA | Target Values Defined by Criteria metadata | Yes | Every preparation, validation, or import request | Verify | Target View Business Objects Attributes export and environment-generated template | verify_values_defined_by_criteria_metadata | Target metadata is authoritative for header order, available attributes, and calculation payload fields | Export the object attributes in the target pod before preparing the file | Confirmed component headers and supported fields |
| VBC.LDG | Legislative Data Group | Yes | Every component row | Lookup | Target LDG metadata or configured target LOV | resolve_legislative_data_group | All hierarchy artifacts are LDG scoped | Provide the exact LDG and stop on no match or ambiguity | LegislativeDataGroupName and confirmed LDG identity |
| VBC.GROUP | Value Definition Group | Yes | Every root, criterion, and value | Verify | Target setup evidence | verify_value_definition_group | The group must already exist and organize the calculation value definitions | Provide its exact target code and LDG alignment | ValueDefinitionGroupCode |
| VBC.CRITERION_REFERENCES | Database item and value set | Conditional | A criterion uses a database item or textual value validation | Verify | Target setup evidence and exported metadata | verify_database_item_and_criterion_contract | Criteria require compatible database items and value-set semantics | Confirm each item, value set, operand, and literal datatype | DatabaseItemCode, ValueSetCode, Operand, compatible literal type |
| VBC.CALCULATION | Leaf calculation references and payload | Yes | Every executable calculation leaf | Verify | Target metadata and target setup evidence | verify_calculation_value_contract | Each leaf needs a valid calculation-specific CalculationValues payload | Confirm calculation type, payload field, UOM, currency, periodicity, and related reference before loading | ValueCode, CalculationValues field and value, calculation references |
| VBC.HIERARCHY | Parent-child hierarchy and default path | Yes | Every hierarchy | Verify | Prepared immutable HDL artifact and representative-condition tests | verify_hierarchy_design | Priority and linkage determine the returned value | Order parents before children and test overlapping conditions and fallback behavior | Root and parent codes, sequence, default criterion and value |
| VBC.LOADER | HCM Data Loader execution readiness | Yes | Before import | Verify | Validated immutable HDL artifact, nonproduction diagnostics, and current approval |  | HDL diagnostics and core.data-loader own import, retry, and approval controls | Validate in nonproduction, correct every diagnostic, and obtain approval for the exact production artifact | Artifact reference, target environment, validation evidence, approval fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Validated target evidence or immutable artifact is available | No lookup required; do not create related setup |
| Lookup | A documented read-only target source can resolve a supplied identity | Yes, read-only only |
| Verify | Metadata, a setup reference, or hierarchy evidence must be checked | Yes, through the documented resolver contract only |
| Blocked | A required value, unique match, target contract, diagnostic resolution, or approval is absent | No |
| Create with Approval | A separately routed and approved workflow creates missing related setup | No; outside this task resource |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.RESOLVE_DEPENDENCIES | decision | 20 | resolve_dependency | ready->VALUE_BY_CRITERIA.RESOLVE_REFERENCES;blocked->VALUE_BY_CRITERIA.HANDLE_DEPENDENCY_ERROR | VALUE_BY_CRITERIA.VALIDATE_INPUT | stop | Confirm target metadata, LDG, setup references, hierarchy, immutable artifact, and loader prerequisites. |
