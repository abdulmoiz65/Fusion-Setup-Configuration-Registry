# Manage Grades Dependency Readiness

## Purpose

Defines the conditional references required by Manage Grades. This task never creates or infers dependencies.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Grade identity | Resolve the target or confirm create availability |
| 2 | Delete history | Resolve the retained start and inclusive deletion end against complete Grade history for delete with mode effective-split |
| 3 | Reference-data set | Resolve one Set for create |
| 4 | Action Reason | Resolve a supplied Action Reason |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| grade_identity | Existing Grade or create-availability evidence | Conditional | Read, edit, inactivate, delete, or create duplicate check | Lookup | Grade resource | find_manage_grades | Prevents ambiguity and duplicates | Provide one exact Grade selector | Grade identity and current values |
| grade_set | Reference-data Set | Yes | create | Verify | Reference-data validator | resolve_grade_set | Places the Grade in one valid Set | Provide one exact Set | SetId and SetCode |
| action_reason | Action Reason | Conditional | A mutation supplies ActionReasonCode | Verify | Current loader contract | resolve_grade_action_reason | Preserves one supported reason | Provide one exact code | ActionReasonCode |
| grade_split_deletion_range | Complete Grade history | Conditional | delete with mode effective-split | Lookup | hcmDateEffectiveObjectHistory | resolve_grade_split_deletion_range | Prevents logical-record deletion or an unintended history range | Provide one exact non-first EffectiveStartDate | Confirmed retained start and deletion end |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact evidence | No |
| Lookup | A declared resolver can resolve the dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed | No |
| Not Applicable | The dependency condition is false | No |
| Needs Input | A required selector is missing | No |
| Unresolved | Resolution is absent, ambiguous, or incompatible | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.DEPENDENCIES | decision | 4 | resolve_dependency | ready->GRD.DEFAULTS;not_required->GRD.DEFAULTS;needs_input->GRD.ERROR;unresolved->GRD.ERROR | GRD.HISTORY | stop | After target and delete-history resolution and before defaulting |
