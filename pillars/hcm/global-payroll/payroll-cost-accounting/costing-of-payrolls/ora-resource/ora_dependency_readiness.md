# Costing of Payrolls HDL Dependency Readiness

## Authority Boundary

User-supplied account input and an immutable HDL archive support local presence,
shape, and consistency checks only. Create establishes payroll/LDG identity,
flex structure, segment values, and effective allocation state through the
named read-only resolvers. Update resolves and snapshots complete history and current accounts before
applying the requested segment change. End Date resolves the selected latest parent/history and preserves accounts as comparison evidence only. Zap resolves every historical parent and physical account identity; it does not validate account values. Correct remains unsupported.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Payroll and LDG identities | Resolve canonical payroll/LDG identity at the requested start. Require flex for Create/Update only. |
| 2 | Operation-specific state | Create requires no active parent. Update requires complete history and exactly one matching latest open-ended parent and complete account distribution. End Date resolves the latest selected interval; Zap resolves the selected entire logical history and all physical accounts. |
| 3 | Account structure | For Create/Update, resolve the runtime KFF descriptor and validate account values. End Date and Zap skip KFF and segment LOV validation. |
| 4 | Defaults and source assembly | Apply operation-scoped defaults. Prepare operation-specific DAT members using the current loader template: both for Create/Update, parent-only for End Date, parent and conditional resolved accounts for Zap. |
| 5 | Archive validation and approval | Complete source/schema validation and Task Hook preview through core.data-loader, then use its single approval bound to the exact environment and immutable archive. |
| 6 | Result and verification | On an explicit status or verification request after submission, require terminal success for every submitted object and apply the operation-specific comparison or Zap absence verification. Update also verifies the full effective history and preservation of the prior interval. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| create_ldg_identity | Canonical LDG and flex | Yes | Create | Lookup | Exact LDG response | resolve_costing_ldg | The LDG name is an HDL key and the flex discriminator controls account validation. | Select one LDG with a configured costing flex. | ldg_id;legislative_data_group_name;id_flex_num |
| create_payroll_identity | Effective payroll definition | Yes | Create | Lookup | Exact payrollDefinitionsLOV response at requested start | resolve_create_payroll | Resolves the payroll SourceId and canonical HDL identity in the selected LDG. | Supply an exact payroll name or selected PayrollId. | payroll_id;lookup_source_id;payroll_code;payroll_identity_evidence |
| create_absence | No active costing parent | Yes | Create before source preparation | Verify | Complete Generic Costing GET | query_payroll_costing | Create must not act as an implicit update of an active parent. | Select Update or same-start Correct separately if an active parent exists. | create_absence_evidence |
| create_runtime_kff | Current costing flex structure | Yes | Create | Lookup | Runtime KFF descriptor for the selected LDG flex | resolve_runtime_costing_kff | The descriptor determines segment columns, sequence, delimiter, and LOV bindings. | Resolve incomplete metadata before preparing account rows. | runtime_segment_definitions;runtime_segment_columns;runtime_lov_contracts;runtime_delimiter |
| create_segment_values | Validated account components | Yes | Create | Verify | Runtime segment constraints and declared LOV responses | validate_payroll_costing_segments | Every supplied component and full account must match the selected flex context. | Correct invalid or incomplete account values. | validated_segment_values;validated_account_rows |
| costing_foundation | Runtime costing structure and validated target values | Yes | Update | Verify | Current LDG runtime descriptor and declared LOVs | validate_payroll_costing_segments | Carried-forward and changed values must match the selected flex and new effective date. | Resolve all required KFF facts before rendering. | runtime_segment_definitions;validated_segment_values |
| payroll_identity | Canonical payroll identity | Yes | Update | Lookup | Exact payroll definition at the new effective date | resolve_create_payroll | PAY records require canonical PayrollCode and LDG keys. | Resolve one exact payroll in the selected LDG. | payroll_code;legislative_data_group_name |
| account_rows | Complete current account distribution | Yes | Update | Lookup | Effective Generic Costing parent and accounts | query_payroll_costing | Existing values are the source for unchanged fields and accounts. | Retain the full account baseline and apply only the explicit COST segment change. | effective_parent;ordered_accounts;update_expected_accounts |
| hdl_archive | Immutable validated HDL archive and current approval | Yes | Before import handoff | Blocked until approved | core.data-loader validation result | | A loader handoff is a side effect. | Approve the exact preview immediately before submission. | archive_fingerprint;approval_fingerprint |
| update_history | Complete current history | Yes | Update | Lookup | Paginated PAY history | query_payroll_costing_history | The verified contract appends a new split to the latest open-ended interval; it does not insert before future rows. | Resolve every page and preserve the baseline for verification. | complete_effective_history;latest_effective_parent |
| end_date_state | Canonical identity, complete latest history and account baseline | Yes | End Date | Lookup | Exact PAY history and selected-start parent/account reads after payroll/LDG resolution | query_payroll_costing_history | The operation may shorten only the last interval and must preserve its accounts. | Resolve complete state; no account input, KFF validation or account DAT is needed. | complete_effective_history;latest_effective_parent;end_date_baseline |
| zap_history | Complete logical history | Yes | Zap | Lookup | Complete PAY history after canonical payroll/LDG resolution | query_payroll_costing_history | The supplied start identifies the logical allocation, not a lower deletion bound. | Resolve all selected history, including earlier and later splits. | zap_history_keys;complete_effective_history |
| zap_history_accounts | Historical physical account identities | Yes | Zap | Lookup | Every bound historical Generic Costing detail response | query_payroll_costing_history_accounts | DELETE targets require exact child identities or complete proof of no children. | Resolve all historical details before package preparation. | zap_history_parents;zap_history_accounts;complete_history_account_fanout;zap_no_children_proven |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All prerequisites for the current phase are confirmed. Archive approval is evaluated only at the submission gate. | Only the declared operation-specific GETs; no create during dependency checks |
| Missing prerequisite | A required setup or source value is absent. | No |
| Approval required | The archive is valid but has not received current approval. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.HDL.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready_create->COP.CREATE.VALIDATE_SOURCE;ready_update->COP.UPDATE.VALIDATE_SOURCE;blocked->COP.HDL.HANDLE_ERROR | COP.HDL.APPLY_DEFAULTS | stop | Require operation-specific identity, state, KFF and segment facts. Create requires its four preceding lookup nodes; Update requires COP.UPDATE.RESOLVE_STATE, COP.UPDATE.RESOLVE_KFF and COP.UPDATE.VALIDATE_SEGMENTS. Approval remains deferred to the submission gate. |
| COP.ZAP.CHECK_DEPENDENCIES | decision | 35 | resolve_dependency | ready->COP.ZAP.APPLY_DEFAULTS;blocked->COP.HDL.HANDLE_ERROR | COP.ZAP.CHECK_STATE | stop | Require canonical payroll/LDG identity and complete history/detail evidence; skip KFF dependencies. Archive approval remains deferred until execution. |
