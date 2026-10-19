# Release Management

## Purpose

FSCR releases promote governed repository content from reviewed internal
development into milestone, release, or public-candidate states. Release
management protects the framework, generated catalogs, pillar skills, schemas,
and project workspace contracts from unreviewed breaking changes.

## Versioning

Skills, schemas, and published reusable artifacts should use semantic versioning:

```text
major.minor.patch
```

Use:

- Major versions for breaking changes to manifests, schemas, skill outputs,
  automation behavior, generated paths, or project workspace contracts.
- Minor versions for new compatible capabilities, new pillar coverage, new
  resource guidance, or additive schema fields.
- Patch versions for corrections, wording fixes, non-breaking metadata updates,
  and backward-compatible examples.

## Branches

Protected branches:

- `main`
- optional `integration`
- `release/<version>`

All developers should use short-lived feature branches and merge through a
reviewed merge request. Milestone and release branches are created from `main`
by the FSCR framework or release owner team. Do not create release branches from
feature branches or local-only state.

Feature branch naming follows:

```text
<pillar-or-area>/<type>/<short-description>
```

## Release Types

| Release Type | Purpose | Owner |
| --- | --- | --- |
| Internal milestone | Aligns active framework, shared, and pillar work for QA or stakeholder review. | FSCR framework owners with Pillar Leads. |
| Release branch | Stabilizes a named repository version from `main`. | FSCR framework/release owners. |
| Public-candidate package | Identifies content that may be reusable outside the internal repository after additional approval. | FSCR owners with program, legal, security, and communications as needed. |

## Release Readiness

A skill or repository area is release-ready when:

1. Manifest metadata is complete and validates against
   `schemas/skill-manifest.schema.json`.
2. Required schemas are satisfied.
3. Naming follows `governance/naming-conventions.md`.
4. Design follows `governance/skill-design-standards.md`.
5. Error handling follows `governance/error-handling-guidelines.md`.
6. Examples, fixtures, golden scenarios, or dry-run evidence are available where
   applicable.
7. Ownership and support expectations are documented.
8. Required reviewers have approved the merge request.
9. QA gates have passed for changes that affect functional behavior.
10. No credentials, secrets, tokens, tenant-specific values, real customer data,
    or sensitive screenshots are included.
11. Generated artifacts are intentional, reproducible, and scoped to the
    correct repository layer.
12. Project-specific outputs remain outside the reusable base repository unless
    they are sanitized templates or examples.
13. Merge requests affecting FSCR skills include a current self-audit report
    from `core.fusion-dev.fscr-merge-auditor`, and the audited commit SHA
    matches the merge-request source-branch head reviewed for approval.

## Approval Gates

| Change Type | Required Approval |
| --- | --- |
| Pillar skill or pillar guidance | Pillar Development Lead or SME plus FSCR A-Team/core reviewer. |
| Core, shared, router, schema, governance, knowledge, or project template | At least two FSCR owner-team reviewers. |
| Automated or hybrid behavior | Required code/skill review plus automation safety review for privileges, side effects, retry, timeout, diagnostics, and approval gates. |
| Security-sensitive behavior | Security or designated reviewer for secrets, customer data exposure, tenant safety, unsupported APIs, and sensitive diagnostics. |
| QA-impacting behavior | FSCR QA review for functional test evidence, golden scenarios, skill completeness, and regression risk. |
| Public-candidate content | FSCR owner approval plus program, legal, security, and communications review as needed. |

## Compatibility

Skills should declare applicability by Fusion release, pillar, offering,
functional area, country, and industry when those constraints matter.

Release reviewers should verify that:

1. Backward compatibility is preserved or the breaking change is versioned.
2. Generated skill paths and skill IDs remain stable unless a migration is
   explicitly documented.
3. Schema changes remain compatible with existing project artifacts unless a
   major version is declared.
4. Automation behavior does not change side effects, privileges, approval gates,
   or retry behavior without review.
5. Public-candidate content does not claim unsupported product behavior or
   unattended production configuration.

## Release Evidence

Release notes or merge request evidence should include:

1. Changed repository layers and affected skill IDs.
2. Jira story, task, or release milestone reference where applicable.
3. Validation commands and results.
4. Dry-run or preview evidence for generated artifacts or live-action skills.
5. QA evidence for affected functional flows.
6. Error-handling, timeout, retry, and diagnostic behavior for automated,
   hybrid, validation, import, export, or generation skills.
7. Known limitations, unsupported cases, and follow-up issues.
8. Confirmation that sensitive data and secrets are not present.

## Changelog Discipline

Use changelog entries or release notes when a contribution changes:

1. Skill IDs, folder layout, or generated paths.
2. Manifest metadata, schema contracts, inputs, outputs, or workspace artifacts.
3. Automation behavior, privileges, side effects, retries, or timeouts.
4. Pillar coverage, setup-task coverage, or task-local guidance.
5. Public-readiness status, limitations, or support boundaries.
