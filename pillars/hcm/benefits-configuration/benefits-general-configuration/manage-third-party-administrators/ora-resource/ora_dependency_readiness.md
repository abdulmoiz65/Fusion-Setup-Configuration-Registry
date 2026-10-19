# Manage Third-Party Administrators Dependency Readiness

| Sequence | Dependency | Ready condition |
|---|---|---|
| 1 | Active Run Book and selected environment | Task context and environment match. |
| 2 | Live Organization loader contract | Required root and classification association are available. |
| 3 | Organization identity | Create has no exact duplicate; update/inactivate resolves one eligible target. |
| 4 | Classification LOV | `BEN TPA` returns one nonblank `ClassificationName`. |
| 5 | Location resolution | Complete explicit code pair exists, or the effective-dated names lookup returns one exact match with codes. |

Classify each dependency as `satisfied`, `lookup`, `needs_input`, `unresolved`,
or `not_applicable`. Continue only when every applicable dependency is
`satisfied`.
