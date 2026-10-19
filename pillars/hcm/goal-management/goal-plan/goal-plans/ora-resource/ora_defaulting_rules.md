# Goal Plan Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| Goal `PriorityCode` | `MEDIUM` (Medium), after explicit or inherited priority | Manual/library-derived Performance Goal create via public child REST, existing ADF batch, or HDL `Goal`/`GoalPlanGoal` | No; preserve explicit priority, then fresh library-source priority, otherwise materialize Medium. Never add it to the Goal Plan header or default updates. |
| status | Inactive | Create | No; activation requires separate approval |
| goal_plan_kind | No default | Every create/update | Never infer Primary from plan name |
| Primary ReviewPeriodId | null | Primary create/update | Yes; a Primary plan is not associated with one Review Period |
| Primary child collections | Omit | Primary create/update | Yes; workers, Eligibility Profiles, and plan goals are not applicable |
| Primary technical dates | Current metadata or approved template values | Primary create; preserve on update | Never use captured tenant constants |
| Regular technical dates | Exact resolved Review Period `StartDate` and `EndDate` | Regular create when both plan dates are omitted | No; explicit complete dates take precedence and must fit the period. Reject a single supplied date. |
| Library-goal template dates | Exact existing Goal Plan `StartDate` and `EndDate` | Add Performance Library Goal to a regular Goal Plan when both template dates are omitted | No; explicit complete dates take precedence and must fit the plan. Reject a single supplied date. |
| Primary weighting | Enabled | Primary create | No; honor an explicit supported consultant choice |
| Primary enforce 100-percent total | Disabled | Primary create | No; enabling it is an explicit design choice |
| assignment_intent | None | Create or population maintenance | No; ESS requires a separate request |
| CascadingLevel | `"0"` (Self) | Goal Plan include-worker and Development mass-assign include-worker | No; validate an explicit value against `ora_defaulting_rules.md` |
| omitted update fields | Preserve fresh stored values | Update | No |
| eligibility profile | No default | Eligibility is optional | Resolve one exact supplied business name or one authoritatively verified semantic-criteria match; otherwise present candidates and never select implicitly |
| Goal Plan Eligibility Profile `TalentObjectType` | `"GOAL"` | Only when creating a `perfGoalEligibilityProfiles` child row for a Goal Plan, after current metadata advertises that child create and the profile is resolved | Yes; derive inside the skill from tenant-validated runtime evidence and do not ask the consultant for it |
| Goal Plan Eligibility Profile `RequiredFlag` | `false` | Only when the population requirement does not explicitly say the profile is required, mandatory, or must be enforced | No; set `true` only for explicit requirement language |
| effective date | No default | Worker resolution | Never infer today |
| assignment effective date | Today in user/project timezone, otherwise host local date | Assign Goal Plans ESS only, when omitted | No; disclose and pin the resolved date in the approval preview; reuse at submission |
| assignee scope | No default | Population or assignment | Require one of selected, direct reports, all reports, selected plus direct, or selected plus all |
| minimum/maximum performance goals | No default | Regular or Primary design | Goal Plans contain performance goals; do not invent counts or ask whether the count applies to development goals |
| `EnforceMaximumGoalsInGpFlag` | Omit / preserve returned `null` | Maximum count is present but restrictive enforcement intent is absent | Never default to `false` or `true`; set `true` only for explicit prevent/must-not-exceed/no-more-than intent, and `false` only for an explicit no-enforcement instruction |
| update access | Advertised all-role value | Create when source omits access | Disclose as a validated default; do not infer any other LOV value |

## Task Nodes

For library additions, carry the selected Library Goal's fresh `PriorityCode`
into `goal_fields`, or supply its `GoalId` and `PriorityCode` as
`execution_context.SourceLibraryGoal`; the helper checks the source ID against
`ReferenceContentItemId`. An explicit caller value takes precedence. A source
with no priority falls back to Medium; explicit null/blank in the requested
goal fields is not omission and remains subject to existing validation.
Validate the final code against current `HRG_PRIORITY`, show it in the exact
approval payload, and compare the fresh stored code after creation. HDL uses
the mapping and reconciliation contract in `goal-management-common/hdl-source-generation.md`.
This changes no date, identity, status, assignment, or approval rule.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.DEFAULTS | step | 50 | apply_default | complete->GOAL_PLANS.DESIGN | GOAL_PLANS.LOOKUPS | stop | Lookups are resolved |


---

# Cascading Level — Local Goal Plan Domain Contract

`CascadingLevel` is a local UI/domain value for Goal Plan include-worker and
Development mass-assign include-worker flows. It is **not** resolved through a
CascadingLevel LOV REST endpoint.

## Authoritative values

| String value | Meaning | Use when |
|---|---|---|
| `"0"` | Self | Include only the selected worker. This is the default. |
| `"1"` | Direct reports | Include only the selected worker's direct reports. |
| `"2"` | Self and direct reports | Include the selected worker and direct reports. |
| `"999999"` | All reports | Include every worker in the selected worker's hierarchy, excluding the selected worker. |
| `"1000000"` | Self and all reports | Include the selected worker and every worker in that hierarchy. |

The Goal Plan UI sources these local values from `CascadingLevelADP` /
`CascadingLevelArrayList`; the Development mass-assign UI uses
`cascadingLvlADP` / `cascadingLvlList`.

## Normalize and validate

1. Preserve CascadingLevel as a string.
2. When the consultant omits it, normalize to `"0"` before payload preview.
3. When supplied, accept only one value from the table above; otherwise return
   the table as the validation error's allowed-value list.
4. `newIncludeWorker.CascadingLevel` defaults to `"0"`; the UI initialization
   also sets `GoalPlanBusinessObject.perfGoalIncludedWorkers.CascadingLevel`
   to `"0"`.
5. The create include-worker body maps the normalized
   `newIncludeWorker.CascadingLevel` directly. An unchanged request therefore
   sends `"CascadingLevel":"0"`.

## Consultant-prompt labels

Match these labels case-insensitively before payload generation:

| Consultant wording | Normalized string value |
|---|---|
| Self | `"0"` |
| Direct reports; Directs only | `"1"` |
| Self and direct reports; Self and Directs | `"2"` |
| All reports | `"999999"` |
| Self and all reports | `"1000000"` |

`All` by itself is ambiguous: it might mean `"999999"` (All reports) or
`"1000000"` (Self and all reports). Do not choose a code. Ask the consultant
to provide one valid code and return this complete list:

```text
0 = Self
1 = Direct reports
2 = Self and direct reports
999999 = All reports
1000000 = Self and all reports
```

Use the same response for any unsupported label or code.

## Goal Plan Eligibility Profile Association Defaults

Tenant-validated runtime evidence confirms this Goal Management child contract
for associating an Eligibility Profile to a Goal Plan:

```json
{
  "EligibilityProfileId": "<resolved active Goal Management profile id>",
  "RequiredFlag": "<derived boolean>",
  "TalentObjectType": "GOAL"
}
```

Apply `TalentObjectType="GOAL"` only to the Goal Plan
`perfGoalEligibilityProfiles` child collection. Do not reuse it for Check-In,
Performance Management, or any other eligibility-profile association unless
that product's contract is separately verified.

Derive `RequiredFlag` from the business requirement. Set it to `true` only
when the requirement explicitly says the profile is required, mandatory, or
must be enforced. If the requirement merely describes the population, default
`RequiredFlag` to `false`.

## Worker and hierarchy evidence

`workersLov` / `getall_workersLov` may select the worker and active assignment
only. They never supply or derive CascadingLevel values.

When a current, verified worker read advertises direct-report or hierarchy
evidence, use it to validate the requested scope: no direct reports permits
only `"0"`; direct reports permit `"1"` and `"2"`; verified descendants are
required for `"999999"` and `"1000000"`. Do not invent a worker hierarchy
endpoint or call an unproven CascadingLevel LOV. If hierarchy evidence is not
advertised, default `"0"` remains executable; a requested non-Self scope is
blocked pending verified hierarchy evidence.
