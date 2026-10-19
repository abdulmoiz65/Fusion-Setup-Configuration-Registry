# HCM Goal Management Best-Practice Reference

## Purpose

This directory contains the canonical FDOS reference for advisory HCM Goal
Management implementation practices. Its content improves consultant planning,
route selection, dependency discovery, safety controls, testing, and cutover
recommendations. It does not authorize external access or configuration
changes.

## Canonical source

[`oracle_hcm_goal_management_best_practices.md`](oracle_hcm_goal_management_best_practices.md)
is the repository-managed copy of the approved source document. Its provenance
and checksum are recorded in [source-integrity.json](source-integrity.json). It covers
tenant and Redwood route selection; design, security, profile, lookup,
value-set, flexfield, Review Period, Goal Plan, Performance Library Goal, and
Development Library Goal guidance; plus diagnostics, testing, migration, and
cutover.

## How Goal Management skills use this reference

The Goal Management parent skill consults the reference for every
implementation query, then routes object-specific work to the owning task
skill. The following topic map keeps the long-form reference discoverable:

| Consultant topic | Reference sections | Owning skill route |
| --- | --- | --- |
| Tenant mode, implementation design, setup sequence, security, notifications, testing, migration, or diagnostics | 2-7, 12-13, 18-24 | `hcm.goal-management` and the applicable declared dependency |
| Review Periods | 14 | `hcm.goal-management.review-period.review-periods` |
| Goal Plans, populations, assignment, or Performance Document integration | 15 | `hcm.goal-management.goal-plan.goal-plans` |
| Performance Library Goals | 16 | `hcm.goal-management.performance-library-goals.goal-library` |
| Development Library Goals or Career Development prerequisites | 17 | `hcm.goal-management.development-library-goals.goal-library` |
| Profile options and feature controls | 8 | `hcm.goal-management.goal-management-common.manage-profile-options` |
| Lookups and value sets | 9-10 | `hcm.goal-management.goal-management-common.manage-common-lookups` or `hcm.goal-management.goal-management-common.manage-value-sets` |
| Descriptive flexfields | 10 | `hcm.goal-management.goal-management-common.manage-descriptive-flexfields` |

## Authority and maintenance

For a target tenant, current tenant behavior and current Oracle documentation
are authoritative. A current task-level SKILL contract controls routing,
validation, external-operation boundaries, approvals, and error handling. This
reference supplies advisory best practices only. When they conflict, do not
silently merge the recommendations: identify the conflict, follow the higher
precedence source, and record the reference section considered.

Review this reference at least once per Fusion quarterly update and whenever a
relevant Oracle readiness item, implementation guide, REST contract, or HDL
contract changes. Preserve the source-reference section when updating the
canonical document and do not add tenant-specific identifiers, credentials, or
customer data.

## Integrity verification

Run the following from the repository root after copying or updating the
canonical source:

```bash
shasum -a 256 oracle_hcm_goal_management_best_practices.md
```

Compare the result with `canonical_markdown_sha256` in
`source-integrity.json`. When the supplied source remains available, also use
`cmp -s` to verify the canonical copy byte-for-byte.
