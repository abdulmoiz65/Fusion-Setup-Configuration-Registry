# Input Validation

| Requirement | Required evidence | Applies when | Failure action |
|---|---|---|---|
| Target environment | One exact environment identity | Any live handoff | Stop with `input_validation`. |
| Requested operation | Read, assess, create, update, delete, redesign, template assistance, manual guidance, export, validate, or import | Every request | Resolve the exact intent and owning task; do not reject an individual change or absent input template. |
| Role identity and type | Exact role identity and job, abstract, duty, or data-role classification | Role assessment or change | Do not default; stop. |
| Approved design | Approved role-design artifact, hierarchy impact, duty/privilege changes, and explicit data-security scope | Mutation preview or import planning | Stop with `approval_blocker`. |
| Import archive | Immutable ZIP hash, exact `ASXS_MANAGE_JOB_ROLES` identity, integrity evidence, shared/core validation evidence | Import | Stop before handoff. |
| Approval | Current approval for exact environment, operation, scope/archive, and preview | Mutation or import execution | Stop with `approval_blocker`. |

Validate fields before defaulting or dependency checks. Do not parse an archive, resolve a transport, or call Fusion locally; use the owning shared/core workflow.
