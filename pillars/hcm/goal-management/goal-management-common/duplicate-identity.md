# Duplicate identity

For both HDL and standard create flows, use `goal-management-common/scripts/duplicate_identity.py`.
For Performance and Development Library Goals, duplicate means exact GoalName
(outer whitespace removed, case preserved) within the same goal type; dates do not
distinguish Library Goals. Performance and Development remain separate types.
Review Periods use exact `ReviewPeriodName` only. Goal Plans use exact
`GoalPlanName` within the associated Review Period. Resolve and compare the
Review Period by returned ID when both rows have it, or by exact
`ReviewPeriodName` when both rows have that value. Start and end dates remain
create-validation fields, but they never distinguish duplicates for either
object. Fusion reports a repeated Goal Plan name and Review Period as
`HRG-3120299`.

For Goal Plan comparisons, a resolved `ReviewPeriodId` is authoritative when
both rows provide it, even when their period-name labels differ. Compare exact
trimmed names only when the pair cannot compare IDs but both names are present.
If two same-named Goal Plans have neither a shared ID nor a shared name field,
the identity is unresolved and preparation must stop; do not assume the rows
refer to different Review Periods.

Search names to discover candidates. Finish pagination and hydrate the library type
through the current core read contract before calling
`assess_duplicates(expected, rows, kind=..., pagination_complete=..., environment=...,
expected_environment=...)`. Accept `clear` only with complete evidence; `duplicate`
requires explicit reconciliation, never automatic reuse. `unresolved` requires
missing evidence to be resolved. A Library Goal name hit becomes a duplicate only
after its Performance or Development type is known. Review Period and Goal Plan
dates must still be validated by their owning create workflows, but are not
required by this duplicate check. The shared library search wrapper applies this
same helper.

Call `validate_incoming(rows, kind)` for canonical incoming rows before preparing
HDL or REST payloads, including Review Period and Goal Plan batches. For raw DAT
input, map template semantic date attributes to these canonical fields first;
ContentItem uses ItemDate1/ItemDate2, not effective DateFrom/DateTo.
Repeated Library Goal names with different ranges are duplicates within the same
type. Repeated Review Period names are duplicates even when their dates differ.
Repeated Goal Plan names are duplicates when their associated Review Period is
the same, even when plan dates differ; the same Goal Plan name in a different
Review Period is allowed. Preserve source-key and External-ID collisions as
distinct validation errors.

Generated ContentItem keys include goal type and business dates. Previously issued
source keys must be retained on updates/reruns; never regenerate an existing key
under the new algorithm. Supplied keys are never rewritten.
