# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and privileges | Confirm environment identity, read access, task privileges, existing authentication path, and the current date used when accounting date is omitted |
| 2 | Source COA | Resolve exactly one enabled source COA using chartOfAccountsLOV |
| 3 | Target COA | Resolve exactly one enabled target COA using chartOfAccountsLOV |
| 4 | Mapping header | Find by requested name using supported evidence and compare the parent and all existing child rules |
| 5 | Segment and value-set metadata | Resolve only metadata needed by requested rules; use CoaValueSetIdVO and KFFSegmentVO evidence before structure export |
| 6 | Value-set definition and values | Resolve exact value-set metadata and, when a rule references values, read the returned child-values collection with paging |
| 7 | Hierarchies | For every parent-based rule, verify hierarchy, effective version, association, flattening, audit, active status, and deployment |
| 8 | Import-route selection | Use core.data-loader for every live import; select the compatible FSM package contract or a Data Loader-authorized FBDI adapter before package generation |
| 9 | Current FSM task-CSV contract | For a Data Loader FSM package, export the mapping task and retain task metadata and export-derived CSV headers, including ORA_GL_AFF_MAP_RULE.csv when account rules are requested |
| 10 | Current FBDI contract | Only when a Data Loader-authorized FBDI adapter is available, obtain the current XLSM and derive its required columns, codes, files, and restrictions |
| 11 | Segment and rollup rules | Validate parent linkage, uniqueness, method rules, values, and hierarchy dependencies |
| 12 | Account rules | Validate account-rule identity, source criteria, target combination, FSM task-CSV contract, and overlap after segment-rule design |
| 13 | Verification report | Run the Chart of Accounts Mapping Rules Report or equivalent read-only review |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| source_coa | Source chart of accounts | Yes | Always | Lookup | chartOfAccountsLOV | find_source_coa | Mapping parent integrity and pre-export gate | Supply an exact source Name or StructureInstanceCode; one enabled result is required | Name, StructureInstanceCode, StructureInstanceId, StructureInstanceNumber, Description |
| defaulted_execution_values | SecurityFlag, import mode, and accounting date | Yes | Always | Verify | User input or ora_defaulting_rules.md | resolve_execution_defaults | Preserve user input and establish deterministic defaults before lookup and validation | Supply any override; otherwise use N, Increment, and current preparation date | Resolved values and source: user-supplied or defaulted |
| target_coa | Target chart of accounts | Yes | Always | Lookup | chartOfAccountsLOV | find_target_coa | Mapping parent integrity and pre-export gate | Supply an exact target Name or StructureInstanceCode; one enabled result is required | Name, StructureInstanceCode, StructureInstanceId, StructureInstanceNumber, Description |
| segment_value_set_metadata | Segment and value-set metadata | Conditional | A segment rule requires source or target segment metadata | Verify | CoaValueSetIdVO and KFFSegmentVO evidence | resolve_segment_value_set | Prove the segment belongs to the exact resolved COA before rule generation | Do not export structure metadata unless this metadata cannot be resolved by supported evidence | Structure instance, segment instance, segment code, value set ID, enabled state |
| value_set_definition | Exact value-set definition | Conditional | A constant, copy, or rollup rule uses a verified segment value set | Lookup | GET valueSets by exact ValueSetCode | find_value_set_definition | Validate datatype, validation type, maximum length, and formatting before checking values | Use only the ValueSetCode returned by segment metadata; do not provide or infer a REST item key | ValueSetId, ValueSetCode, ValidationType, ValueDataType, ValueSubtype, MaximumLength, format flags, child-values URI |
| value_set_values | Referenced or copied value-set values | Conditional | A constant, copy, or rollup rule references values | Lookup | GET returned value-set item link child/values | find_value_set_values | Prove value existence, enabled state, effective date, and complete copy-value equivalence | Supply requested value(s) and accounting date; include independent-value context for dependent sets | Value, EnabledFlag, effective-status evidence, IndependentValue when applicable |
| referenced_values | Referenced segment values | Conditional | Constant, rollup, or account rule uses values | Verify | Supported value metadata and same-task evidence | resolve_mapping_values | Date-effective validity | Correct inactive, ambiguous, or missing values | Technical value, value set, effective status |
| hierarchy_version | Effective hierarchy version | Conditional | A parent value is used | Verify | Supported tree metadata | resolve_mapping_hierarchy | Parent expansion uses the accounting-date version | Supply intended accounting date and parent value | Tree, version, start and end dates |
| hierarchy_association | Segment-instance hierarchy association | Conditional | A parent value is used | Verify | Chart instance and deployment metadata | verify_hierarchy_association | Mapping requires the hierarchy associated to the segment instance | Associate, flatten, audit, activate, and redeploy when changed | Association and deployment status |
| mapping_header | Existing mapping | Yes | After both COAs resolve and before export, create, update, or import | Verify | Same-task export, application read-only evidence, report evidence, or confirmed read-only mapping evidence | find_mapping_definition | Idempotency and update safety | Resolve ambiguous names before continuing; identical is terminal and different requires direction | Header, rules, audit metadata |
| import_route | Selected import transport | Yes | Any create or update preparation | Verify | Requested rule composition and core.data-loader capability | select_import_route | Prevent direct FSM submission and an unsupported FBDI handoff | Core.data-loader is mandatory; use its FSM ZIP path when applicable and stop when no Data Loader-authorized adapter supports the requested package | Selected Data Loader route and rationale |
| current_fsm_task_csv | Current same-task FSM CSV export | Conditional | A Data Loader FSM package is selected | Verify | Current same-task export and ASM_SETUP_CSV_METADATA.xml | inspect_current_fsm_task_csv | Prove exact CSV files, headers, hierarchy, and metadata; account rules use ORA_GL_AFF_MAP_RULE.csv | Export only after both COAs, mapping comparison, and Data Loader route selection pass; do not invent row shape or writable audit fields | Metadata, CSV filenames, headers, parent-child paths, import ZIP shape |
| current_fbdi | Current Oracle XLSM | Conditional | A Data Loader-authorized FBDI adapter is selected | Verify | Current Oracle FBDI guide and downloaded XLSM | inspect_current_fbdi | FBDI interface authority must be available through the selected Data Loader route | Do not generate or submit FBDI when no Data Loader-authorized adapter is available | Worksheets, columns, codes, CSV and ZIP shape |
| account_rule_overlap | Rule overlap set | Conditional | Account rules coexist with segment rules | Verify | Requested and existing rule definitions | analyze_rule_overlap | Account rules supersede overlapping segment results | Review each effective-result change | Source combination, segment result, account result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | One valid dependency exists and evidence is current | Lookup yes; create only after preview and approval |
| Business decision | More than one valid design outcome exists | No create until the owner decides |
| Technical lookup gap | Required code, identifier, template field, or hierarchy fact is unresolved | Lookup yes; live mutation no |
| Missing setup | Required chart, segment, value, hierarchy, association, or mapping parent is absent | Create or update only through its supported skill and explicit approval |
| Concurrent change | Current audit or version evidence differs from the baseline | Refresh and compare; no mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAMAP.DEPENDENCIES | step | 6 | resolve_dependency | ready->COAMAP.DEFAULT | COAMAP.LOOKUP | stop | New mapping or approved update |
