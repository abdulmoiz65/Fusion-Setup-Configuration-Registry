# Balance Groups FSM Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task CSV contract | Obtain the exact Balance Groups CSV template/export contract through the declared export workflow |
| 2 | Resolve and prepare complete archive | During routed preparation resolve parent, requested child references and attribute linkage through the declared GETs. Apply matching defaults and prepare every requested row plus any required supporting definition/link. Reuse this evidence in Task Hook validation; do not stop merely because supporting setup is absent |
| 3 | Data Loader preflight | Complete the core.data-loader preflight for the exact immutable archive before Task Hook preview and approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| fsm_csv_contract | Exact task template/specification | Yes | Every import | Satisfied when supplied and task-matched; otherwise Blocked | Supplied local task CSV template/export provenance and applicable ora_defaulting_rules.md parent contract | | XML reference tags do not define CSV headers or import options | Use the task template with the documented minimal parent mapping when applicable; do not require another populated sample for that supported case | Validated task identity and CSV field contract |
| fsm_requested_scope | Complete requested parent and child representation | Yes | Every creation or update | Satisfied when mapped; otherwise Blocked | User's requested scope and prepared archive validated against its supplied template | | A parent-only archive cannot satisfy a request that also includes definitions or default inclusions | Resolve missing template coverage before preparing the load; retain child relationships carried by the archive | Coverage evidence for every requested section |
| fsm_parent_state | Verified LDG and intended parent state | Yes | Creating or updating a named group | Satisfied after exact lookup; otherwise Blocked | Returned exact LDG and group lookup evidence | find_balance_group_by_name_and_ldg | Create must not silently update an existing group | Resolve the LDG first and enforce exact parent cardinality | Parent state and operation evidence |
| fsm_defined_balance | Verified existing balance and dimension | Conditional | Existing balance selections are requested | Satisfied after exact lookup; otherwise Blocked | Returned filtered defined-balance lookup evidence | resolve_defined_balance_by_name_and_dimension | A balance name alone does not identify the requested defined balance | Resolve the full requested pair using the documented filtered search and a verified parent context | Verified defined-balance reference evidence |
| fsm_default_category | Verified restriction or default inclusion category | Conditional | Category restrictions or default-inclusion categories are explicitly requested | Satisfied after exact lookup and category FK derivation; otherwise Blocked | Returned category lookup evidence and confirmed helper mapping in ora_reference_lookups.md | resolve_default_inclusion_balance_category | Category and dimension are distinct reference types | Resolve the requested category through its own lookup and retain its restriction or default-inclusion role | Raw category row/base IDs, derived category FK, base/display names and qualifiers for each requested role |
| fsm_default_dimension | Verified restriction or default inclusion dimension | Conditional | Dimension restrictions or default-inclusion dimensions are explicitly requested | Satisfied after exact lookup; otherwise Blocked | Returned Employee dimension lookup evidence | resolve_default_inclusion_employee_dimension | A category match does not verify the requested dimension | Resolve each complete requested dimension through the Employee lookup; non-Employee scope requires a supplied lookup contract | Returned dimension ID, complete name and qualifiers for each requested restriction or default-inclusion role |
| fsm_attribute_link | Supporting attribute definition and group link | Conditional | Existing-group balance-definition, default-inclusion or restriction additions | Satisfied by an applicable established link or supporting records under the matching supported profile; a populated-group restriction transition still needs its own evidence | Exact parent-linked definition result and supported profiles in ora_reference_lookups.md | find_balance_group_attribute_links | Linkage state determines whether the confirmed empty-group restriction profile applies | Resolve the current links before choosing the profile; prepare matching supporting records in the same archive. Do not silently alter a populated definition or ask for UI prerequisite creation for a supported empty-group case | Existing linkage or new definition/group-link rows with consistent child references |
| fsm_preflight | Exact artifact and environment binding | Yes | Before Task Hook preview | Satisfied when preflight passes; otherwise Blocked | core.data-loader preflight and selected project context | | Preparation success must not be confused with target data validation or completed import | Use the unchanged preflight artifact and its task context | Archive digest, environment, and task-routed preflight evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| FSM_PREPARATION_READY | The archive contract and requested scope are complete | Continue to Task Hook validation and approval; no Fusion mutation at this gate |
| FSM_CSV_ARCHIVE_REQUIRED | No compatible task CSV artifact is available | Use the declared export workflow; no import or alternative route |
| FSM_SCOPE_UNVERIFIED | Any requested section, reference mapping, or parent-child relationship cannot be established from the supplied contract | Stop preparation; do not submit a parent-only subset |
| LOOKUP_PARENT_CONTEXT_REQUIRED | A requested balance selection has no verified parent context for the documented lookup | Stop that lookup; obtain the missing source contract without creating a partial parent |
| LOOKUP_RESULT_INCOMPLETE | Reference results are truncated or paging is inconclusive | Stop identity resolution; do not claim missing setup from partial results |

For an existing Employee group with a complete empty linked-definition result, prepare the supporting definition and group link in the same ZIP as all requested children using the successful combined profile. Do not stop at prerequisite discovery. An attribute definition represented in the FSM package is not required to exist beforehand merely because the old HDL route required an exact existing AttributeCode. Dependencies on target balances, dimensions, categories, and LDGs follow the task CSV specification and Fusion import validation; archive inspection alone does not verify their existence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BG.RESOLVE_DEPENDENCIES | decision | 9 | resolve_dependency | ready->BG.ENFORCE_DESIGN;blocked->BG.HANDLE_ERROR | BG.RESOLVE_ATTRIBUTE_LINK | stop | Every applicable reference lookup resolved and every unrequested optional lookup returned not_required |

## Sources

- Developer request: use FSM setup import with no Data Loader business-object selection, 2026-10-08.
- Developer-supplied FSM configuration-package ZIP, inspected 2026-10-08. Only component and field names are retained here; exported setup values are not repository fixtures.
- The enclosing task SKILL.md owns the FSM CSV import contract and core.data-loader handoff.
- Developer-supplied attribute validation endpoints and HAR category lookup, 2026-10-09; mechanics are owned by ora_reference_lookups.md.
- Developer-confirmed successful minimal parent FSM flow and requested reuse, 2026-10-09; its field defaults do not require a separate sample or mapping waiver.
- Developer restriction category/dimension lookup request, 2026-10-09; shared lookup mechanics and HAR evidence are owned by ora_reference_lookups.md.
- Developer restriction resolver extension, 2026-10-09: category dependencies include the confirmed helper-derived FK; dimension dependencies retain their own returned identity without category transformations.

- Developer-requested automatic combined child preparation, 2026-10-09, backed by the approved FSM CSV archive and retrieved successful component ProcessLog: one BalanceAttributeDefinition, one BalanceAttribute and one BalanceAttributeDefault processed with zero failures/warnings; the archive also contained their BalanceGroupInclusion link. No customer identifiers are retained here.
