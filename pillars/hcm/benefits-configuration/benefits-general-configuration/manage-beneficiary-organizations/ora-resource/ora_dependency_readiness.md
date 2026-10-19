# Manage Beneficiary Organizations Dependency Readiness

| Sequence | Dependency | Applies when | Ready condition |
|---|---|---|---|
| 1 | Active Run Book and selected environment | Mutation | The environment and task context match and the Run Book is active. |
| 2 | Live Organization loader contract | Source preparation or validation | Current metadata exposes the required root and classification association. |
| 3 | Organization identity | Create, update, or inactivate | Create has no exact duplicate; update/inactivate resolves exactly one eligible organization. |
| 4 | Classification LOV | Create or update | The required `HR_BEN` LOV query returns exactly one nonblank `ClassificationName`. |
| 5 | Location resolution | Create or update when location is supplied or required | A complete explicit code pair exists, or the effective-dated locations LOV returns exactly one exact name/set-name match with `LocationCode` and `SetCode`. |

Classify each dependency as `satisfied`, `lookup`, `needs_input`, `unresolved`,
or `not_applicable`. Continue only when all applicable dependencies are
`satisfied`; `needs_input` and `unresolved` are blocking outcomes.
