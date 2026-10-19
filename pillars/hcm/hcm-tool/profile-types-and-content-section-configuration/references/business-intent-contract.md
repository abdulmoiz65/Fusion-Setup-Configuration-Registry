# Business Intent Contract

## Intake and Expert Route

Collect business outcome, population or process context, effective date,
constraints, and exceptions. A complete JSON, workbook, CSV, Markdown, or text source is accepted as expert input, but does not skip business intent, proposal
review, technical normalization, exact-match, immutable-preview, or execution
approval gates.

## Resolution Precedence

Apply this order to each missing technical value:

1. Explicit user value.
2. Approved current-project decision.
3. One clearly dominant comparable configuration found by a declared,
   source-backed, read-only resolver.
4. Documented Oracle rule or safe exclusion.
5. Deterministic review-only generation.

Do not select a value when equally supported patterns remain. Record a material
conflict and ask one concise business question. Similarity may support a proposal
but never satisfies the later exact-match rule.

## Assumption Ledger

Record every inferred value with these fields: `value`, `source`, `sanitized evidence`, `confidence`, `materiality`, and `review_status`. Use `proposed`,
`confirmed`, `rejected`, or `not_required` for review status. A material value
must be visibly reviewed before technical normalization; proposal confirmation
does not authorize import or another write.

## Proposal Format

Present only: what will be enabled; for whom or which process; effective date;
important resolved defaults or associations; material assumptions; and important
exclusions. Label it **Prepare configuration** or **Review assumptions** until
an authorized executor creates an immutable preview artifact.

## Clarification Rule

Ask one concise business-language question only if competing answers materially
change business behavior, scope, timing, reuse-versus-new, or downstream impact.
Otherwise continue with the safe review-only proposal and list unresolved,
non-material exclusions.
