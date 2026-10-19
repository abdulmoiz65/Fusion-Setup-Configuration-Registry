# Defaulting Rules

| Field | Default | Rule |
|---|---|---|
| Role identity, type, hierarchy | None | Require explicit approved design evidence. |
| Privilege, duty, and data-role scope | None | Never infer mappings or scope. |
| Import content and route | None | Owning approved workflow selects only after validation. |
| Mutation route | None | Never derive a route from catalog flags. |
| Task identity for a supplied archive | None | Validate exact `ASXS_MANAGE_JOB_ROLES`; do not rewrite or substitute. |

Apply no defaults that broaden security scope. Missing values return issues before dependency readiness.
