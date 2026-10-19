# Manage Grades Design Enforcement

## Purpose

Defines the blocking Grade design gates evaluated before routing.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one target or confirm create availability |
| 2 | Validate dependencies | Resolve the Set and any supplied Action Reason |
| 3 | Validate mutation scope | Require the Grade row and only applicable child rows |
| 4 | Decide readiness | Continue only when no blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_grades | The Grade identity is absent, ambiguous, or duplicated | Supply GradeId or the complete GradeCode and SetCode key | Input fix |
| GRADE_SET | create | Blocking | resolve_grade_set | The Set is unresolved or inconsistent | Resolve one Set | Lookup fix |
| EFF_SHAPE | A GradeLegislative EFF row is supplied | Blocking |  | Its context discriminator, child key, or configured multirow unique key is incomplete | Correct the EFF row | Input fix |
| DELETE_MODE | Delete targets the Grade parent | Blocking |  | Zap versus effective-split intent is absent or ambiguous | Require the user to choose the destructive scope; never infer zap | Input fix |
| ZAP_DELETE | Zap delete | Blocking | find_manage_grades | The exact logical Grade is unresolved, the artifact uses `MERGE`, contains child rows, or mixes `DELETE` and `MERGE` for that Grade | Author one Grade `DELETE` row using GradeId or GradeCode and SetCode and disclose complete logical-object purge | Input or payload fix |
| DATE_EFFECTIVE_SPLIT_DELETE | Effective-split delete | Blocking | resolve_grade_split_deletion_range | The selected row is the first split, has no predecessor, is unresolved or ambiguous, or the final artifact does not use `SET PURGE_FUTURE_CHANGES Y` plus one Grade `MERGE` whose start is the predecessor start and whose end is the selected row end | Rebuild the bounded `MERGE` from complete fresh Grade history; never use `DELETE` for a split | Lookup or payload fix |

| GRADE_CONFIGURATION | Create or edit | Warning |  | Grade code or name is unclear, or legislative, type, or progression settings are not confirmed | Use a simple identifying code and confirm configuration before activation | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_grades | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_grade_set | create | One SetId and SetCode | ora_reference_lookups.md |
| resolve_grade_action_reason | An Action Reason is supplied | One ActionReasonCode | ora_reference_lookups.md |
| resolve_grade_split_deletion_range | Effective-split delete | Complete ordered history, non-first eligibility, predecessor start, selected-row end, and verification evidence | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every blocking rule is satisfied | Continue to routing |
| not_required | No design rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.DESIGN | decision | 6 | design_enforcement | passed->GRD.ROUTE;not_required->GRD.ROUTE;blocked->GRD.ERROR | GRD.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting |
