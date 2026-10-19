# Request Feedback Template Best-Practice Reference

This folder contains the canonical reusable reference for Oracle Fusion HCM
Performance Management Request Feedback Template implementation guidance.

## Canonical source

- [Canonical Markdown reference](oracle_hcm_request_feedback_template_best_practices.md)
- [Source integrity metadata](source-integrity.json)

The Markdown file is a full canonical copy of the supplied source. The supplied
HTML was used only to confirm content/formatting parity and is deliberately not
stored as a duplicate knowledge asset.

## Topic map

| Consultant question | Canonical sections |
| --- | --- |
| Scope, setup versus runtime, navigation | 3–5 |
| General or Performance Goal template design | 6, 14–15, 18 |
| Questionnaire, question, lookup, or DFF design | 7, 10–11 |
| Redwood, profile, TDS, or VBS readiness | 5, 8, 12 |
| Roles, data security, alerts, and notifications | 9, 13 |
| Lifecycle, activation, migration, or environment comparison | 14–18 |
| Preflight, FSCR evidence, testing, and troubleshooting | 19–24 |
| Oracle source links | 25 |

## Consultation and precedence

Consult this reference after request classification and the selected task's
local contract/resources. It is advisory and never authorizes browser,
REST/OAuth, export, import, loader, or other Fusion activity.

When guidance conflicts, use this order:

1. FDOS router and task-level skill contracts, including validation, approval,
   identity, and external-operation safeguards.
2. Authorized evidence of actual target-tenant behavior and capability.
3. Current official Oracle Fusion documentation for the applicable release.
4. This best-practice reference.

Document any discrepancy; do not invent a compatibility route or a
tenant-specific value.

## Integrity verification

Run the following from the repository root after copying or updating the
canonical source:

```bash
shasum -a 256 pillars/hcm/performance-management/requested-feedback-template/best-practice-rules/hcm-requested-feedback-template/oracle_hcm_request_feedback_template_best_practices.md
```

Compare the result with `canonical_markdown_sha256` in
`source-integrity.json`. When the supplied source remains available, also use
`cmp -s` to verify the canonical copy byte-for-byte.
