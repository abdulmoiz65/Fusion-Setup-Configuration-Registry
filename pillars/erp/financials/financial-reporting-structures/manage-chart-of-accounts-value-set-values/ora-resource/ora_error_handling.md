# Value Set Value Error Handling

## Failure Classification

| Failure Class | Examples | Required Response |
|---|---|---|
| Input validation | Missing flags, unreadable image cells, duplicate/invalid values | Report every affected row and make no Fusion call |
| Artifact validation | Unsafe ZIP, wrong member, wrong width, encoding or hash mismatch | Stop before handoff and regenerate only after correction |
| Catalog/target mismatch | Parent lookup has no exact match, multiple matches, or invalid MaximumLength | Stop before package handoff and report the exact mismatch |
| Authentication or authorization | Value-set metadata read or Data Loader access denied | Report the required capability without exposing credentials |
| Transport/environment | Data Loader import transport unavailable | Preserve package and diagnostics; don't retry automatically |
| Submission outcome unknown | The approved Data Loader submission times out or disconnects after the first state-changing request may have begun | Don't resubmit or use a separate status client; report the Data Loader result and primary request identifier when returned |
| Process timeout or failure | Data Loader returns a nonterminal or terminal non-success result | Report the primary request ID, returned status, and sanitized diagnostic when available; don't fetch process-tree or output attachments |
| Outcome detail unavailable | The Data Loader result has no row-level status | Report that row-level counts are unavailable; don't infer them or query values after handoff |
| Artifact persistence | Preview, CSV, ZIP, report, or log can't be saved | Stop before side effects when pre-submit; disclose after submit |

## Retry Rules

- Never retry a Data Loader submission automatically.
- Resume an existing primary request through `core/data-loader`, without resubmitting, only when the user explicitly requests that follow-up.
- Require an explicit retry instruction after a terminal failed import.
- Rebuild the package only when input or defaults change; record a new hash.

## Data Loader Outcome Diagnosis

Treat the result returned by `core/data-loader` as the only outcome. For timeouts, uncertain submissions, or terminal failures, retain and report the primary request ID, returned status, and sanitized diagnostic when supplied. Never launch a separate status, process-tree, child-job, LOG, OUT, or value request to enrich that result.

## Failure Report

Persist environment, Value Set Code, stage, failure class, package hash, Data Loader result, primary request ID, returned status, sanitized diagnostic, and affected values/source rows internally.

Report only the Value Set Code, primary request ID, returned status, affected values, and concise sanitized Data Loader message. State that row-level counts are unavailable when Data Loader did not return them. Don't include documentation links, local artifact links or paths, hashes, UCM document IDs, or internal persistence details. Redact tokens, credentials, authorization headers, base64 content, unrelated sensitive data, and irrelevant stack traces.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MVS.FAILED | terminal | 6 | terminal | none | none | stop | Any blocking validation, lookup, package, Data Loader handoff, or returned terminal failure |
| MVS.READY_FOR_DATA_LOADER | terminal | 5 | terminal | none | MVS.VALIDATE_CLASSIFIED | stop | Validated candidate is ready for package preparation and Data Loader handoff |
