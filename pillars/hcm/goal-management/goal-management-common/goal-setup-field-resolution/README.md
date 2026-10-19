# Goal Setup Field Resolution

This is an internal support package owned by the catalog-backed
`hcm.goal-management.goal-management-common` functional-area skill. It is deliberately not a
standalone pillar skill because field resolution is not an Oracle setup task.

Use this helper before a Goal Plan or Library Goal preview when consultant
language must be mapped to a UI/API field. Read
[field capability resolution](ora-resource/ora_field_capability_resolution.md)
first.

## Preconditions and outputs

Require an identified Goal Plan or Library Goal object, source-grounded
requirement statements, and current field capabilities supplied by the owning
task workflow. Return machine-readable resolved candidates, ambiguous or
unmapped requirements, and LOV validation results. Do not read Fusion directly,
write project state, or perform configuration changes.

Resolve only explicit configuration intent. A purpose, audience, geography,
or organizational statement is context unless it explicitly requests a
population, worker assignment, Eligibility Profile, availability restriction,
or another field action. Do not create a population route from context alone.
For a regular Goal Plan, classify omitted population, Eligibility Profiles,
and assignment as `not_in_scope`, never as a blocker or a missing input.

Use current field metadata and returned LOV values as the authority. Map a
statement automatically only when it has one supported field and, for LOVs,
one valid value. Mark product defaults as defaults. Return field candidates
for review when the mapping is not unique; do not guess a DFF or restriction
field. This helper does not read Fusion or mutate configuration itself.

When a Library Goal topic is explicit but Goal Name is absent, generate a
review-only candidate. Include it in the same runbook confirmation summary as
`proposed`; use it only after the consultant confirms or edits it. A candidate
collision is a naming decision, never an automatic numeric suffix.

For Goal Setting Info, explain that its post-end restrictions apply to workers
only and are additive to the Goal Plan access-level setting. Map explicit
all-role access/update language to the access-level field. Map an explicit add
requirement to the creation restriction, an explicit edit/cancel/delete
requirement to the update restriction, and language that explicitly includes
both to both restrictions. These mappings are independent and cumulative; do
not report them as conflicting. Ask which worker restriction is intended only
when the source names neither action. When Goal Setting Info is requested but
either date is missing, propose the corresponding Goal Plan boundary as a
review-only candidate and require confirmation before a configuration preview.
In Goal Plan create or update context, resolve these Goal Setting Info phrases
before generic access or HR-assigned-goal action fields. `CanDelHRGoal` is not
the route for date-bound Goal Setting Info restrictions.

## Failure and disclosure boundaries

- Classify missing or malformed inputs as `input_validation` and return the
  exact affected statement or field.
- Classify absent, stale, duplicate, or contradictory field metadata as
  `catalog_or_metadata_mismatch`; stop and require a fresh owning-task preview.
- Never retry or substitute a different field after an ambiguous match.
- Redact credentials, tokens, token-cache contents, private keys, tenant URLs,
  and sensitive payload values from diagnostics.
- This helper has no timeout, rollback, or live-approval behavior because it is
  local and read-only. The owning task skill controls external preflight,
  preview, approval, execution, diagnostics, and recovery.
