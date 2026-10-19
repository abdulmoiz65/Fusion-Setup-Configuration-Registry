# Dependency Readiness

| Dependency | Required state | Applies when |
|---|---|---|
| Role design | Approved artifact and exact requested role scope | Mutation preview or import planning |
| Existing role evidence | Current evidence of the exact role, or approved design evidence that it is new | Role change |
| Environment access | Target identity and verified Security Console privileges | Manual guidance handoff or execution preview |
| SoD review | Completed review when the role scope changes access segregation | Applicable role design |
| Import workflow | `shared.setup-import.fsm-csv-import`, `core.data-loader`, immutable archive, and validation readiness | Import |

Return `blocked` until every applicable dependency is evidenced. Dependency failure never authorizes a local fallback.
