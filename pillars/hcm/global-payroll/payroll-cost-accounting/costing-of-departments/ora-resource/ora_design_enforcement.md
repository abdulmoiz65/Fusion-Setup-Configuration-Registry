# Department Costing Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm scope | Support Create, Update, End Date, and Zap; return unsupported for other mutations. |
| 2 | Confirm identity | Resolve DepartmentName and the canonical LegislativeDataGroupName through read-only GETs. |
| 3 | Confirm account rows | For Create and effective-dated Update, use official ORG parent and account identities, valid KFF values, fractions, and consecutive positive SubTypeSequence values starting at 1. |
| 4 | Confirm date operation | Prefix both Update DAT members with SET PURGE_FUTURE_CHANGES N. End Date instead changes only the selected last parent's end date using the parent-only contract; preserve its start date, prior history, and account distribution. |
| 5 | Confirm live gate | Validate source/schema and Task Hook, present immutable archive fingerprint, and obtain fresh approval. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create | Blocker | query_department_costing | An allocation already exists, an HDL key is missing, or an account row is invalid. | Build the two official HDL DAT members only after the zero-parent check. | No |
| Update | Blocker | query_department_costing | Current state, requested effective date, update retain instruction, or HDL account identity is missing. | Build the two official HDL DAT members with SET PURGE_FUTURE_CHANGES N. | No |
| End Date | Blocker | query_department_costing_history | History is incomplete, the supplied start date does not identify the latest effective parent, a later split exists, or the requested end date precedes that parent's start or exceeds its current end. | End-date only that last parent with its existing EffectiveStartDate and the requested inclusive EffectiveEndDate. If the end date already matches, report the verified state without submitting another load. | No |
| End Date schema boundary | Blocker | | End Date is rejected solely because ReplaceLastEffectiveEndDate is absent from the ordinary template/Attributes list, the attribute is removed to pass validation, or a rejected wrapper result is treated as passed. | Oracle documents this special attribute outside the ordinary attribute list. Keep it in the parent-only DAT and submit the source to core.data-loader validation. A wrapper rejection blocks live handoff, not authoring support for End Date. Component Details, Date Effectivity is the documented authority for actual component capability; do not infer unsupported capability from template omission. | No |
| Zap scope | Blocker | query_department_costing_history | The supplied start date does not identify exactly one logical allocation, or the requested deletion is limited to one effective split. | Zap deletes that CostAllocationId's complete history and accounts, including periods before and after the supplied selector date. That date identifies the record; it does not bound deletion. Never reinterpret Delete (ED Split), an account-only delete, or an ambiguous Delete as Zap. | No |
| Zap readiness | Blocker | query_department_costing_history_accounts | Historical parent/account evidence is incomplete or changed, an account target was supplied instead of resolved, or Data Loader cannot validate DELETE support, keys, or the package. | Prepare the complete identity-only DELETE archive after resolving every history detail. Use core.data-loader for schema review and dependency processing; ZIP member order alone does not establish load order. Do not assume that deleting CostAllocationV3 alone removes the separate account business object. | No |
| Create, effective-dated Update, End Date, or Zap preparation | Blocker | | A successful lookup, render, archive, or validation step is treated as an intermediate pause. | Continue through applicable defaults, state checks, DAT render, source/schema validation, immutable ZIP, and Task Hook preview before requesting fresh approval. Stop at an actual validation failure and disclose its owning layer. | Yes |
| End Date or Zap approval freshness | Blocker | query_department_costing_history | The target environment, complete history, selected parent/account baseline, requested dates, or archive fingerprint changed after preview. | Refresh the history and operation-specific detail evidence before the one approved handoff. If facts differ, invalidate the preview and approval and recompute the scope. | No |
| Zap execution approval | Blocker | | At the execution gate, approval is absent or does not cover the complete logical history and all resolved accounts. | Use the single core.data-loader approval for the exact validated archive as destructive confirmation. Prepare and show the full scope before requesting it; this check does not block source preparation or Task Hook validation. | No |
| Any mutation | Blocker | | A direct REST write, raw UCM/import request, browser replay, FSM, or Business Object route is proposed. | Use only core.data-loader after the HDL gates. | No |
| Unsupported operation | Blocker | | Correct, account-only Delete, or Delete (ED Split) is requested. | Stop and record the bounded scope gap; the supported Delete Record And History alias uses Zap. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_department_source | Create, Update, End Date, Zap, or verification. | DepartmentName and read-only source context. | ora_reference_lookups.md |
| resolve_legislative_data_group | Create, Update, End Date, Zap, or verification. | Canonical LegislativeDataGroupName and LDG ID after LIKE discovery or exact ID resolution. | ora_reference_lookups.md |
| resolve_runtime_costing_kff | Create or Update. | Current segment metadata and validated values. | ora_reference_lookups.md |
| query_department_costing | Create pre-check, Update or End Date preflight, or verification. | Current parent and account facts. | ora_reference_lookups.md |
| query_department_costing_history | End Date or Zap preflight, approval freshness, or verification. | Complete history and selected logical allocation. | ora_reference_lookups.md |
| query_department_costing_history_accounts | Zap preflight or approval freshness. | Every historical parent and physical account identity, or complete proof of no children. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.ENFORCE_DESIGN | decision | 50 | design_enforcement | query_only->DCP.VERIFY_QUERY;ready_create->DCP.HDL_GATE_CREATE;ready_update->DCP.HDL_GATE_UPDATE;ready_end_date->DCP.HDL_GATE_END_DATE;ready_zap->DCP.HDL_GATE_ZAP;blocked->DCP.HANDLE_ERROR | DCP.APPLY_DEFAULTS | stop | Select exactly one query, Create, Update, End Date, or Zap branch before package handoff. An End Date whose requested end already matches takes query_only and returns the verified current state without a load. |
