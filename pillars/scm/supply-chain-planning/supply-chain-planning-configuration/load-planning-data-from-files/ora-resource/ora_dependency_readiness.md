# Planning FBDI Load Readiness

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| planning_execution_context | Validated source-system intake and supported collection mode | Yes | Requested load | Satisfied or Blocked | Explicit request input validated by ora_input_validation.md; Net Change default from SKILL.md and policy result from ora_design_enforcement.md | | Carries the current request's source system and supported collection mode into Core | Carry the validated values and source-input evidence; no saved-source fallback or collection-mode approval question | Source System and Collection Type |
| planning_task_context | Matching saved task, Run Book and environment context | Yes | Task-routed load | Satisfied or Blocked | Canonical project task context selected by the router | | Prevents a late route failure after preparation | Resolve missing context through the routed workflow; do not create or merge a Run Book automatically | Exact task and selected context |
| planning_core_preflight | Verified Core preflight for the immutable ZIP | Yes | Core Task Hook | Satisfied or Blocked | Core Data Loader preflight envelope | | Core owns live route, authentication and execution approval | Require Planning Common FBDI routing with adapter 135 and the existing account; underlying MSC descriptions need not be renamed | Matching archive digest, BO, adapter, account and environment |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required context and matching Core preflight evidence exist | No repeated lookup |
| Blocked | Missing/mismatched context or preflight | No fallback route or automatic Run Book change |

## Task Nodes

For a load request, check saved context early before template preparation.
Prepare-only work does not authenticate or require live preflight. During Core
Task Hook evaluation, consume the single verified preflight; do not initiate
another lookup. Core's first-match FBDI routing does not validate every CSV's
schema; that is covered by the local package evidence.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHECK_LOAD_READINESS | decision | 30 | resolve_dependency | ready->RETURN_READY;missing->RETURN_ISSUES | VALIDATE_FBDI_ARCHIVE | stop | Core Task Hook before Core's approval preview |
