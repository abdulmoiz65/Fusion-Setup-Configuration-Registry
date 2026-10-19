# Dependency Readiness

| Dependency | Required state | Applies when |
|---|---|---|
| Role design | Approved artifact and exact requested role scope | Mutation preview or import planning |
| Existing role evidence | Current evidence of the exact role, or approved design evidence that it is new | Role change |
| Environment access | Target identity and verified Security Console privileges | Manual guidance handoff or execution preview |
| SoD review | Completed review when the role scope changes access segregation | Applicable role design |
| Import workflow | `common.security-console.manage-job-roles` handoff, its `shared.validation.setup-data-validator` evidence, immutable archive, and `core.data-loader` session readiness | Import planning and handoff |

Core Data Loader owns the final preview and execution approval. Missing import
approval does not block input preparation or a validation-only session handoff;
it blocks the session's live import step.

Return `blocked` until every applicable dependency is evidenced. Dependency failure never authorizes a local fallback.
