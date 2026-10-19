# Goal Setup Field Capability Resolution

## Classification

Classify each extracted statement as `configuration_intent`, `business_context`,
`population_or_assignment_intent`, or `qualifier`. Only explicit worker,
population, assignment, or Eligibility Profile requests are population intent.
An action verb and population noun may be separated (for example, “assign US
employees working with ...”); resolve the semantics rather than requiring one
literal phrase. Descriptive statements such as “supports employees working
in ...” remain business context.
Explicit negative assignment instructions are `explicit_no_assignment`, not
permission to create population associations or submit an assignment process.

## Resolution contract

The runtime capability input contains field name, UI label, type, writable and
required flags, default state, dependencies, and allowed LOV values. Match
semantic intent to that input, not to a tenant capture or sample value.

Resolve Goal Plan access, dates, Review Period, status, goal-setting controls,
weighting, count limits, evaluation type, HR-assigned-goal actions, subtype,
document types, and DFFs independently. An asserted maximum maps to a number
field and its enforcement switch only when both are advertised. Missing update
access uses the advertised all-role default when it exists and is labelled
`defaulted`.

For a regular Goal Plan, an audience or purpose does not supply population
intent. When no worker-selection, Eligibility Profile, population-rule, or
assignment action is explicit, classify population, Eligibility Profiles, and
assignment as `not_in_scope`; do not ask for them or block planning.

## Goal Setting Info

Goal Setting Info adds worker-only restrictions after its end date; it does
not reduce HR specialist or manager access granted by `GoalAccessLevelCode`.
Treat the access-level LOV and these flags as independent, cumulative controls:

| Explicit source meaning | `RestrictGoalCreationFlag` | `RestrictGoalUpdateFlag` |
|---|---:|---:|
| Workers cannot add goals | `true` | Unspecified; preserve on update |
| Workers cannot edit, cancel, or delete goals | Unspecified; preserve on update | `true` |
| Workers cannot add or edit goals | `true` | `true` |
| Do not restrict creation or update after the period | `false` | `false` |

Map explicit all-role access/update language to `GoalAccessLevelCode`, using
the current advertised all-role value. It remains independent of these flags.
Interpret polarity before mapping action words: "don't allow" imposes a
restriction; "do not restrict" removes it. Never resolve by keyword presence
alone. Preserve unspecified checkbox values on update. Mixed, contradictory,
exception-bearing or unclear language requires confirmation. Do not describe either worker flag as an all-role
restriction or report the combined controls as a conflict.

Goal Setting start and end dates must be a complete ordered pair inside the
Goal Plan dates. If Goal Setting Info is requested and either date is absent,
propose the corresponding Goal Plan boundary as a review-only candidate and
require explicit confirmation. Do not silently default those dates.

For Goal Plan create or update, run this Goal Setting Info resolution before
generic access, evaluation, or HR-assigned-goal action lookup discovery. Do not
evaluate `CanDelHRGoal` for date-bound phrases such as "after the
goal-setting period, no goals can be edited or added"; that phrase maps to
`RestrictGoalCreationFlag=true` and `RestrictGoalUpdateFlag=true` when the
current Goal Plan metadata advertises both fields.
When extraction splits a logical table row, correlate only siblings belonging
to the same object and `goal_setting_info` semantic group. Prefer structured
facts with `object_key`, `semantic_group`, `statement`, and source provenance;
select one object with `object_key`. Never pool a document's unrelated rows.
Legacy string lists must already be a single-object normalized group.
Treat explicit enumeration of
HR specialist, manager, and worker as the all-role access semantic, subject to
current metadata resolution of `GoalAccessLevelCode`.

For a Library Goal, Goal Name is the required business input. Description,
scope fields, DFFs, measures, tasks, outcomes, and other fields remain omitted
unless supplied or metadata-required. A qualifier maps automatically only to
one writable field/LOV match; otherwise return candidate fields for review.

Library Goal lifecycle and role audience are key create invariants, not ordinary
optional qualifiers. Materialize `StatusCode=I` and `Visible=ALL` when omitted
before preview. Map “all employees” and “HR specialist, manager, and worker” to
the writable `Visible=ALL` code even when Describe exposes the field without an
inline enum. `AvailableTo` is read-only verification output. A Business Unit
restriction adds one exactly resolved `BusinessUnitId` while retaining
`Visible=ALL`; it does not change the role-audience meaning. “Required” is an
assignment indicator only and must not submit an assignment from Library Goal
creation.
Explicit restricted audiences, exclusions, departments or legal-employer scope
must resolve through current metadata or remain unresolved. Never convert an
unrecognized explicit audience (for example HR specialists only) into ALL.

## Library Goal Name proposals

When a Library Goal has an explicit variant and topic but no Goal Name, propose
`<Variant> Library Goal - <topic>`. Preserve source-provided names unchanged.
Mark generated values as `proposed`, not source facts, and request one
confirmation response that may accept, edit, or supplement all proposals. If
normalized candidates collide, mark them `naming_decision_required`; do not
invent suffixes or a customer naming convention.
