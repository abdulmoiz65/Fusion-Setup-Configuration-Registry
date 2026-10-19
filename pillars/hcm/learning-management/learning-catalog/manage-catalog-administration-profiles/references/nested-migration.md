# Nested task and Run Book compatibility

Canonical ID: `hcm.learning-management.learning-catalog.manage-catalog-administration-profiles`.
The old standalone functional-area ID is historical, not an executable alias.
Invoke the parent Learning Catalog manifest for discovery; invoke this child for
CAP operations. Compiler/planner commands use the parent functional-area path;
runtime Task Hook context selects this child's `SKILL.md`.

The shared Run Book guard owns `runbook_control.active_runbook_ref` (numeric
worker journey ID), `server_url`, and the canonical generated context location
`artifacts/shared/runbook/current/task-context.json`. CAP's additional saved
binding evidence stays at `artifacts/core/runbook/current/active-runbook-binding.json`;
its contents, identity hash, task and target checks are still mandatory. CAP
compares shared identity and server with the selected loader configuration.
Create preparation derives the project-local `config/cap-data-loader.properties`
automatically and passes it to unchanged shared loader interfaces. No shared
`env.properties` edit or manual ID entry is needed. Its path/content hash is part
of the exact preview; submission refuses missing or changed content. This does
not alter the existing update or read/list configuration contracts.
Changing project state invalidates pending approval fingerprints; it never
permits submitting an old preview through the new contract.

Historical project output paths intentionally remain unchanged. Keep immutable
previews, ZIPs, attempts and receipts at their original locations. Unsubmitted
pre-migration previews require fresh evidence, preparation and exact approval;
completed or uncertain operations must never be replayed. Source fingerprints
and existing attempt-key namespaces continue to protect these boundaries.

Environment-property cleanup is not target readiness. Re-establish the intended
target and existing Run Book using supported configuration before live execution;
do not restore a stale token or infer live access from offline regression tests.
