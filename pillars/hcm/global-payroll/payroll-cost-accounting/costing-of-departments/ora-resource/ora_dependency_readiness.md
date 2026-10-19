# Department Costing Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Identity | Resolve the exact Department and the LDG through LIKE discovery for user text, then exact LDG confirmation, using documented read-only GETs. |
| 2 | Account structure | For Create or Update, resolve runtime Costing KFF metadata, including its segment order and delimiter. Validate populated Segment values and the complete SUSP or DFLT ConcatenatedSegment that will be rendered from them. End Date and Zap skip this dependency. |
| 3 | Current state | For Create, Update, or End Date, resolve query_department_costing for effective state. End Date first requires complete history and the selected last parent; Zap uses complete history and query_department_costing_history_accounts for every selected split. |
| 4 | HDL package | Apply the operation-specific DAT contract in ora_input_validation.md. Create and Update use both DAT members; End Date is parent-only; Zap includes the parent and any resolved account DELETEs. |
| 5 | Approval and handoff | Validate the immutable archive through core.data-loader and Task Hook, then obtain fresh approval. |
| 6 | Verification | After a terminal load, apply the operation-specific read-only verification in ora_reference_lookups.md. End Date and Zap return pending after initiation and verify only on an explicit status/verification request. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| department_identity | Department source | Yes | Create, Update, End Date, Zap, or verification | Lookup | Exact DepartmentCostSearchVO result retained with the handoff for post-delete verification | resolve_department_source | DepartmentName is the HDL key; OrganizationId is read-only lookup context only. | Provide a Department selector that resolves uniquely. | department_name;organization_source_id |
| ldg_identity | Legislative Data Group | Yes | Create, Update, End Date, Zap, or verification | Lookup | Read-only LDG discovery and exact-confirmation responses retained with the handoff | resolve_legislative_data_group | The confirmed canonical LegislativeDataGroupName is an HDL key. | Provide LDG text/name or an exact ID; select a canonical returned Name when discovery produces multiple candidates. | legislative_data_group_name;ldg_id |
| runtime_kff | Costing KFF | Yes | Create or Update | Lookup | Runtime descriptor and LOVs | resolve_runtime_costing_kff | Each account representation and each SUSP or DFLT ConcatenatedSegment must match the target segment order, delimiter, and valid values. | Correct invalid segment values or an incomplete Full KFF combination before preview. | runtime_segment_definitions;runtime_delimiter;validated_segment_values |
| allocation_state | Allocation state | Yes | Create, Update, End Date, or verification | Lookup | Generic Costing GET | query_department_costing | Create requires absence; Update, End Date, and verification require exact state. End Date retains account facts only as a verification baseline. | Resolve one exact Department and LDG scope. | effective_parent;verification_facts |
| effective_history | Complete effective history | Yes | End Date or Zap | Lookup | Read-only PayCostSearchVO history for the resolved Department and LDG | query_department_costing_history | Establishes the operation's complete logical-history scope. | Resolve all history before applying the selected operation's design rule. | complete_effective_history;last_effective_parent;history_comparison_facts;zap_history_keys |
| zap_history_accounts | Historical account identities | Yes | Zap | Lookup | Every bound Generic Costing historical detail response | query_department_costing_history_accounts | Supplies every physical account DELETE target or explicit proof of no children. | Resolve the complete detail set before package preparation. | zap_history_parents;zap_history_accounts;complete_history_account_fanout;zap_no_children_proven |
| hdl_identity | HDL row identity | Yes | Create or effective-dated Update | Satisfied | Resolved Department and LDG names plus generated account sequences | | Official Department rows use ORG, DepartmentName, and LegislativeDataGroupName. | Ignore a supplied sequence, assign 1 to the first supplied row, and increase by 1 for each following account row; do not substitute REST technical IDs for HDL keys. | source_type;department_name;legislative_data_group_name;sub_type_sequence |
| hdl_archive | Immutable HDL archive | Yes | Create, Update, End Date, or Zap | Blocked | Source/schema review, Task Hook result, archive fingerprint, and approval | | A mutation can only use the declared core.data-loader handoff. End Date retains ReplaceLastEffectiveEndDate=Y through validation; a shared-validator rejection is handled as an external validation blocker. | Approve the exact archive immediately before handoff only after validation passes. | archive_fingerprint;approval_fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required value is resolved and matches the requested scope. | Yes |
| Lookup | A documented read-only GET can resolve an exact value. | Yes for lookup only |
| Blocked | Required identity, KFF value, archive review, or approval is missing. | No |
| Unsupported | A mutation other than Create, Update, End Date, or Zap, or a direct REST write, is requested. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->DCP.APPLY_DEFAULTS;blocked->DCP.HANDLE_ERROR;unsupported->DCP.HANDLE_ERROR | DCP.RESOLVE_REFERENCES | stop | After required read-only identities and state are resolved. |
