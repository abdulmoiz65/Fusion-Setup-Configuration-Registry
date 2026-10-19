# Event Alert execution reporting

Use two levels for CREATE results: a business summary in the final response and
one Markdown technical report with a section for each Alert. Apply to simple
and deep validation, sequential and batch-create. This is presentation only;
the payload/approval contract remains 0.11.0. Do not add any Fusion call to
produce a report or reopen a completed run. Other mutation intents retain their
existing operation-specific reporting.

## Final response

Lead with the actual outcome, then this table in workbook order:

| Alert code | Alert name | Status | HTTP status | Technical details |
| --- | --- | --- | --- | --- |
| DEMO_ALERT_1 | Payment received | Created and verified | 200 (batch) | View details |

Every View details cell must link to that Alert's generated technical section;
never deliver placeholder links. Use the generated summary as the final-answer
content, converting relative report links to absolute local paths for chat.
Keep the same anchor fragment. No separate technical JSON dump in the final.

Show business-action items and Body verification limitations below the table.
Configuration creation does not establish notification delivery. Keep IDs,
fingerprints, environment, object-level checks and diagnostics in the technical
report. Do not conceal failures behind its links.

HTTP status is transport evidence, not business status. For batch show the
outer response as `200 (batch)` on each row, not an invented part status. If a
part explicitly returned a status, it may additionally be shown in technical
details. Sequential uses the actual parent CREATE response, labelled
`201 (Alert POST)`; child HTTP results belong in the technical section. Use
`Not submitted` before a request and `Unavailable` for a submitted request
without an HTTP response. Never infer a status from a missing field.

## Report input and generation

The assisted provider assembles reporting JSON from its approved preview and
sanitized submission/read-back evidence. This is not a new execution adapter,
an approval artifact, or a substitute for actual verification. Never fabricate
evidence to satisfy the renderer. Do not pass raw response payloads, Body text,
Base64 content, expressions, credentials, or authentication headers.

`schema_version: 1`, `execution_mode: batch-create|sequential`, `environment`,
`work_unit_sha256` (or a combined run reference for sequential), and `alerts`
are the top-level fields. Optional `body_verification: deferred` discloses the
current limitation; omit when there are no Bodies. `evidence_files` is an array
of absolute paths to existing sanitized local evidence. The renderer links
these files without copying their contents. They must be safe to share locally.

Each Alert row contains:

- `code`, `name`: exact reviewed intake values; preserve order.
- `stage`: `awaiting_approval`, `not_submitted`, `submitted`, `failed`, or
  `uncertain`. A timeout/ambiguous response stays uncertain until reconciled.
- `http_status`: integer HTTP status or null; batch outer status or sequential
  parent POST status, never a child's status.
- `response_matched`: boolean from actual response checks, not from HTTP 200.
- `expected_objects`: array of `{entity, code}` for the Alert and all included
  Templates and Recipients, derived from the approved hierarchy.
- `objects`: sanitized read-back records `{entity, code, id, status,
  http_status}`. `status` is `verified`, `verification_failed` or `pending`.
  Omit unperformed checks; do not convert them to passed.
- Optional `action`: reviewed, business-friendly correction/reconciliation
  guidance, shown in both summary and details. No raw Fusion error text.

Object codes are compared within each Alert. If repeated Recipient codes
across Templates would make them ambiguous, supply an additional `parent_key`
in both expected and actual object records (TemplateCode for Recipients).
All expected objects must uniquely match actual verified records with IDs before
the renderer says Created and verified. Any uncertainty/failure takes precedence.
Inline Body acceptance remains outside these object counts and is disclosed.

```text
python pillars/hcm/hcm-tool/alert-foundation/scripts/render-alert-report.py --input <report-input.json> --output-dir <new-project-report-directory> --dry-run
python pillars/hcm/hcm-tool/alert-foundation/scripts/render-alert-report.py --input <report-input.json> --output-dir <new-project-report-directory>
```

Persist under the current project's Alert Foundation artifacts. The tool writes
`business-summary.md` and `technical-details.md`, refuses existing outputs, and
has no network/authentication capability. It renders only allowed fields; the
provider still owns sanitization of displayed names and optional action text.
On malformed input stop reporting as input_validation. On write failure record
artifact_persistence and retain the execution outcome separately: never repeat
a Fusion write to regenerate a report. Reports may be regenerated locally in
a new directory without resubmission. Record report paths in the existing run
record/token log. Do not publish or commit project evidence automatically.

Before approval, retain the exact approval phrase and immutable payload link
after the generated business summary. This report does not authorize writes.
After submission, generate from all actual part/object evidence; missing parts
or checks must remain pending, failed or uncertain, not successful.
