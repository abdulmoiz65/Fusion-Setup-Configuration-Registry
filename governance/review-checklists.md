# Review Checklists

Use these checklists during merge request review. Select the sections that match
the contribution type and record which checks were run, skipped, or not
applicable.

## Merge Request Intake

- The merge request links the relevant Jira story, task, or work item where
  applicable.
- The summary identifies affected repository layers and skill IDs.
- The branch follows `<pillar-or-area>/<type>/<short-description>`.
- The change is scoped to the requested capability.
- Generated files are intentional and reproducible.
- Validation evidence is included.
- Required reviewers are assigned.
- Security and customer-data statements are included when examples, payloads,
  screenshots, diagnostics, or project artifacts are present.
- When the change affects FSCR skills, a completed
  `core.fusion-dev.fscr-merge-auditor` MR-scope report is attached before
  reviewer approval and covers every MR commit and affected skill.
- The MR audit report identifies the source and target SHAs and is regenerated
  after either changes; stale reports are rejected.

## Approval Baseline

| Change Type | Required Reviewers |
| --- | --- |
| Pillar skill or pillar guidance | Pillar Development Lead or SME plus FSCR A-Team/core reviewer. |
| Framework, `core`, `shared`, `router`, `schemas`, `governance`, `knowledge`, or reusable `project` template | At least two FSCR owner-team reviewers. |
| Automated or hybrid execution | Functional reviewer plus automation/core reviewer. |
| Security-sensitive or publication-sensitive change | Security or designated reviewer, plus program/legal/comms where public-candidate content is involved. |
| QA-impacting change | FSCR QA reviewer. |

Peer review and cross-pillar peer review are recommended when the change affects
shared setup objects, cross-pillar dependencies, or common methodology.

## General Skill Review

- Manifest is named `SKILL.md` and validates against the schema.
- Layer responsibilities and exclusions pass
  `governance/skill-layer-responsibilities.md` for the declared layer.
- Skill ownership and reviewer group are clear.
- Inputs and outputs are explicit.
- Dependencies are declared.
- Execution mode is appropriate.
- Applicability is scoped correctly.
- Best-practice guidance is source-aligned where applicable.
- The skill is placed in the correct repository layer.
- Naming follows `governance/naming-conventions.md`.
- Durable outputs declare project workspace metadata when they are needed by
  later stages.
- The skill uses `core/`, `shared/`, and `router/` capabilities rather than
  duplicating primitives.
- Side effects and required privileges are documented for automated and hybrid
  skills.
- Examples, fixtures, or golden scenarios use synthetic data.
- The reviewer confirms the attached audit verdict, automated evidence,
  semantic layer review, and open findings before approval.

## Pillar Skill Review

- Catalog-backed skills were created with `pillar-skill-gen` where applicable.
- Offering, functional-area, setup-task, and skill-ID naming follow the generated
  hierarchy.
- Every functional-area and nested setup-task skill path matches its pillar,
  offering, functional area, and task entry in
  `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
  and the effective pillar-to-offering mapping; a missing match is a MAJOR
  audit finding.
- Task-specific guidance is modularized at the correct offering, functional
  area, or nested setup-task boundary.
- Generated pillar skills use `ora-resource/ora_*.md` files for source-aligned
  Oracle FusionApps guidance when augmentation is needed.
- Pillar `ora-resource/` files are created or updated only by the resource
  authoring workflow and remain inside the target generated pillar skill folder.
- Shared objects such as enterprise structures, legal entities, business units,
  reference data, security, integrations, reporting, or environment setup
  reference shared/common skills instead of copied logic.
- Unsupported CSV, REST, loader, or setup-task gaps are documented with
  advisory fallback or follow-up issues.

## Automated and Hybrid Skill Review

- Required roles and privileges are documented.
- API endpoints, ESS jobs, loaders, imports, exports, and side effects are
  declared.
- Live execution has preview, dry-run, plan-first, or explicit approval gates
  where supported.
- Retry and error-handling behavior is defined.
- Timeout behavior and polling limits are defined for long-running operations.
- Process IDs, request IDs, ECIDs, job identifiers, and diagnostic artifact paths
  are captured where available.
- Audit and logging expectations are clear.
- Test fixtures, dry-run examples, or preview evidence are provided.
- Live POST, PATCH, DELETE, import, loader, or ESS operations are not retried
  without an idempotency key or explicit user approval.

## Error-Handling Review

Use `governance/error-handling-guidelines.md` as the reference.

- Expected failure modes are classified.
- Preflight checks run before side effects.
- Authentication and authorization failures distinguish expired cached tokens
  from missing privileges.
- Fusion HTTP errors retain status, URL or endpoint path, response body summary,
  and ECID when available.
- Polling timeouts stop with environment, operation, task code or job
  definition, ProcessId/requestId, last status, elapsed time, and retry guidance.
- Failed Fusion jobs retrieve and persist the process log or status payload when
  available.
- Partial progress preserves successful outputs and records failed units in an
  errors array.
- Diagnostics are persisted under `project/{project_id}` when durable output is
  needed.
- Tokens, secrets, private keys, token caches, base64 payloads, and sensitive
  customer details are redacted.
- Fail-closed behavior is used for ambiguous catalog matches, unsupported flags,
  overwrite conflicts, destructive actions, and target paths outside the
  requested workspace.

## Advisory Skill Review

- Guidance is actionable.
- Assumptions are documented.
- Human actions are explicit.
- Risks and decision points are identified.
- References or knowledge sources are listed where applicable.
- Unsupported, uncertain, or source-missing product behavior is marked as a gap,
  follow-up, or `TBD` rather than presented as fact.

## Project Workspace Review

- Skill outputs needed across sessions are written under
  `project/{project_id}/artifacts`, `project/{project_id}/exports`,
  `project/{project_id}/baselines`, `project/{project_id}/decisions`, or
  `project/{project_id}/blueprints`.
- Artifact locations mirror the skill structure.
- Generated artifacts have project artifact metadata and are registered in the
  artifact index.
- Project state updates are explicit and limited to fields affected by the
  skill.
- Revisited skills create new artifact versions for major changes.
- Minor artifact updates require user confirmation before replacing current
  content.
- Failed, timed-out, or partially completed durable runs record diagnostics when
  `project_id` is supplied.
- Public repository templates do not include customer data, credentials,
  secrets, tokens, or production-only sensitive values.

## Security and Data Review

- No credentials, keys, tokens, wallet files, private certificates, or tenant
  secrets are committed.
- No real customer data or identifiable customer configuration is committed.
- Screenshots do not reveal customer, employee, tenant, or environment details.
- Private or unsupported APIs are not documented as externally consumable
  patterns without approval.
- The contribution does not imply unattended production configuration.
- Customer/project-specific outputs stay outside the reusable base repository.

## Release and Public-Readiness Review

- Release readiness follows `governance/release-management.md`.
- Public-candidate content is explicitly labeled and reviewed.
- Support boundaries, limitations, unsupported behavior, and manual fallback are
  clear.
- Publication-sensitive wording is reviewed by FSCR owners and program, legal,
  security, or communications reviewers as needed.
