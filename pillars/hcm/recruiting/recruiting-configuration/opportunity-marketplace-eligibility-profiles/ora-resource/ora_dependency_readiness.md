# Dependency Readiness

Apply the parent supporting-object and target-dependency contract. Read the parent resource linked below before generation. Require the maintained parent assets and contracts and the selected target OAuth configuration. Import requires the child task context and active Run Book; listing requires neither a workbook nor a Run Book.

Parent contract: [Dependency Readiness](../../../../benefits-configuration/benefits-eligibility/eligibility-profiles/ora-resource/ora_dependency_readiness.md). Load it for this node; the child overrides above take precedence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_ELIG.DEPENDENCIES | step | 2 | resolve_dependency | ready->OM_ELIG.LOOKUPS;blocked->OM_ELIG.FAILED | OM_ELIG.INPUT | stop | After input checks and before target lookups. |
