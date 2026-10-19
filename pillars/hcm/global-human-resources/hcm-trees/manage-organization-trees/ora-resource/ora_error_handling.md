# Manage Organization Trees Error Handling

## Purpose

Defines safe stop, disclosure, and common-Trees handoff behavior for Organization Tree failures.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity, structure code, or version details are missing | Stop before routing and request only the missing value |
| Seeded creation parameter tuple is unavailable or differs | Stop with a task-configuration mismatch; do not ask the user for technical identifiers or synthesize values |
| A supplied organization name has zero or multiple exact matches | Stop and request a uniquely identifiable organization; do not select a first match |
| A request attempts a direct or task-local tree action | Stop and route the operation only to core.fusion-api.apps-common.trees |
| An existing version cannot be resolved as one Draft record, or an explicit end date makes its interval invalid | Stop before preview and request a corrected version identity or date |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required business request value is absent | Request the missing business value |
| AMBIGUOUS | A supplied organization name resolves to zero or multiple current rows | Request one unambiguous organization identity |
| UNSUPPORTED | A route other than core.fusion-api.apps-common.trees is requested | Return the supported common-skill route |
| FAILED | The common Trees skill reports validation, execution, or verification failure | Preserve its diagnostic and follow its safe next action |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Blocked request | The missing or invalid business input and the supported next action |
| Common Trees handoff | Exact task code, structure code, requested operation, and core skill route |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A common Trees prerequisite is incomplete | Do not construct a payload, invoke another client, or retry an uncertain mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORGTREE.ERROR | terminal | 6 | terminal | none | none | stop | Validation, dependency, lookup, defaulting, or design failure |
| ORGTREE.CORE_HANDOFF | terminal | 7 | terminal | none | ORGTREE.DESIGN | stop | The resolved ID-based request is ready for core.fusion-api.apps-common.trees |
