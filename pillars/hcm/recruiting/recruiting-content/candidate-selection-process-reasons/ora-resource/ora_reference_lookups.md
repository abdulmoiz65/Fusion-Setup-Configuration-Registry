# Candidate Selection Process Reasons Reference Lookups

## Purpose

Defines deterministic local resolution against a current approved task-wide export. This task has no documented live REST lookup contract.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_csp_export_package | Before authoring and during result verification | Intended environment and release, approved task-wide export, ASM metadata, five CSP CSV members, and sanitized ProcessLog when supplied | Require exact task identity, target and release consistency, usable completion evidence, exact member names and headers, and a current fingerprint; treat header-only data as empty rather than missing | Validated baseline, target and release receipt, member inventory, installed Language and SourceLang values, current rows, and fingerprint | Missing, stale, wrong-target, malformed, failed-required-object, partial, or ambiguous evidence blocks |
| resolve_existing_reason | A reason is created, updated, status-changed, translated, or associated | Exact ReasonCode and validated ORA_IRC_CSP_REASON.csv; existing usage rows may also expose seeded SYSTEM-prefixed codes | Compare ReasonCode exactly and case-sensitively; zero base rows means absent, one means present, more than one blocks. Report case-insensitive lookalikes separately. A usage-only seeded code does not prove its status for a new association | ABSENT or PRESENT classification, exact persisted code, current name, status, translations, seeded-reference note, and row fingerprint | Multiple exact rows, incomplete scope, or a usage-only code needed for a new association blocks; never select a case variant |
| resolve_existing_reason_group | A group is created, updated, status-changed, translated, or used by an association | Exact ReasonGroupCode and validated ORA_IRC_CSP_REASON_GROUP.csv | Compare ReasonGroupCode exactly and case-sensitively; zero rows means absent, one means present, more than one blocks. Report case-insensitive lookalikes separately | ABSENT or PRESENT classification, exact persisted code, current name, comments, status, translations, and row fingerprint | Multiple exact rows or incomplete scope blocks; never select a case variant |
| resolve_existing_association | A reason-to-group pair is requested or verified | Exact ReasonCode and ReasonGroupCode plus validated ORA_IRC_CSP_REASON_USAGE.csv | Compare the exact case-sensitive pair; zero rows means absent and one means present. Preserve one existing pair as an idempotent replay | Association ABSENT or PRESENT classification and pair fingerprint | Multiple exact pairs or incomplete scope blocks; omission is never removal |
| resolve_association_context | A new reason-to-group association is authored | Exact ReasonCode and ReasonGroupCode plus validated reason, group, and usage CSVs | Require the exact reason once with status ORA_ACTIVE, the exact group once, and the exact pair zero or one time | Exact Active reason, exact existing group, association ABSENT or PRESENT classification, and source fingerprints | Missing, ambiguous, or non-Active reason; missing or ambiguous group; multiple exact pairs; or incomplete scope blocks |
| resolve_translation_context | A reason or group translation is authored | Validated target translation CSVs, exact parent code, requested Language, export-evidenced SourceLang, target base/source language, and approved translated text | Require the parent exactly once and accept only an installed Language evidenced in the intended target. Use Language to select the translated row. Preserve SourceLang exactly for an existing row; for a new parent, use the target base/source language evidenced by the current export. Never derive or change SourceLang from translation authorship because the FSM migration view marks it non-updateable. Require explicit text for every supplied row | Exact parent, accepted Language, preserved or target-evidenced SourceLang, translated name, and optional translated group comments | Missing parent, unverified language, missing target SourceLang evidence, a requested SourceLang change, blank required text, or ambiguous parent blocks |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Individual-item export requested | Stop and use a current task-wide export; individual-item export is not supported by this contract |
| Exact code absent | Classify as a create candidate only when the requested operation is create and the export is scope-complete |
| Exact code present | Classify as update, lifecycle change, or already-satisfied replay according to explicit intent |
| Case-insensitive lookalike | Disclose every lookalike and require confirmation of the exact case-sensitive code; never normalize or choose automatically |
| Seeded SYSTEM-prefixed usage reference | Preserve existing usage even when the seeded reason is absent from the base-reason CSV; do not infer status or author a new association without Active-status evidence |
| Translation values | Use only explicit approved text and target-installed Language values. Use Language to target the translated row and preserve its exported SourceLang. For a new parent, use the current target's evidenced base/source language. Do not derive or change SourceLang from authorship through CSV |
| Lookup receipt | Record only task identity, target and release labels, exact natural keys, match counts, statuses, language values, source artifact fingerprints, and sanitized evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSPRSN.RESOLVE_REFERENCES | step | 30 | evaluate_result | resolved->CSPRSN.CHECK_DEPENDENCIES;missing->CSPRSN.HANDLE_ISSUES;ambiguous->CSPRSN.HANDLE_ISSUES;failed->CSPRSN.HANDLE_ISSUES | CSPRSN.CLASSIFY_REQUEST | stop | Resolve the current export and every reason, group, translation, or association identity needed by an authoring request |
| CSPRSN.VERIFY_RESULT | decision | 70 | evaluate_result | verified->CSPRSN.DONE_VERIFIED;failed->CSPRSN.HANDLE_ISSUES;partial->CSPRSN.HANDLE_ISSUES;uncertain->CSPRSN.HANDLE_ISSUES | CSPRSN.CLASSIFY_REQUEST | stop | Reconcile a supplied post-import export or sanitized ProcessLog with the intended delta and preserved baseline |
