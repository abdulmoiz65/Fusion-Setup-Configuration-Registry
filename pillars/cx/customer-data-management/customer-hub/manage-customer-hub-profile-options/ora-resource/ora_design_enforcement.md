# Design Enforcement

Enforce Customer Hub option ownership, site-only configuration, exact guarded-option warnings, and immutable execution approval. This resource does not write profile values or submit FSM imports.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fix task and scope | Use only Manage Customer Hub Profile Options and an exact supported profile code |
| 2 | Enforce SITE level | Confirm SiteLevelEnabled and, for a change, SiteLevelUpdatable; reject product and user levels |
| 3 | Read target state | Resolve the exact definition, configured SITE value, validation metadata, and level key |
| 4 | Apply option guardrail | Surface and satisfy every warning or prerequisite for a guarded option |
| 5 | Bind execution route | Use core.fusion-api.apps-common for one direct update or core.data-loader for immutable FSM import |
| 6 | Bind exact approval | Invalidate approval after any target, value, artifact, evidence, or preview change |
| 7 | Verify outcome | Re-read the SITE value or reconcile the returned ProcessId without automatic replay |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every run | Error | | Task name or code differs from Manage Customer Hub Profile Options and ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS | Restore the catalog-backed task identity | Yes |
| View or direct update | Error | read_customer_hub_profile_definition | Requested code is outside the enclosing inventory or the definition does not support SITE | Select an exact supported site-level option | Yes |
| Direct update | Error | read_customer_hub_profile_definition | Current SITE value, proposed value, SITE key, enabled/updatable evidence, target, or exact approval is missing or stale | Re-read the definition and rebuild the exact preview | Yes |
| ORA_ZCH_DEBUG update | Error | read_customer_hub_profile_definition | The request does not state that Oracle Support specifically requested debug enablement | Do not enable debug mode without Oracle Support direction | No |
| Disable ORA_ZCH_AGREEMENT_EVALUATION | Error | read_customer_hub_profile_definition | The request lacks explicit acceptance of orphan-data and application-flow risk | Keep agreement-rule evaluation enabled | Yes |
| Enable ORA_ZCH_ALLOW_REMOVE_FEATURE | Error | read_customer_hub_profile_definition | The request lacks explicit acceptance of orphan-record and downstream-process risk | Keep the documented default N | Yes |
| Change ORA_ZCH_SETATTRIBUTE_OPTIONS | Error | read_customer_hub_profile_definition | The request does not explicitly choose whether a highest-confidence null may replace a non-null master value | Record the intended null-survivorship policy before preview | Yes |
| Change ORA_ZCH_ENABLE_DEFAULT_SOURCE | Error | read_customer_hub_profile_definition | Historical default-source calculation is not explicitly intended | Confirm the historical survivorship-source behavior | Yes |
| Enrichment import mapping update | Error | read_customer_hub_profile_definition | The exact mapping value is not returned or accepted by the current profile definition | Select one existing Import Management mapping; do not invent a name | Yes |
| Auto-merge configuration change | Error | read_customer_hub_profile_definition | The preview omits the combined effect of auto-merge threshold, duplicate-set record limit, and survivorship enablement when more than one is affected | Review the options together and show the combined business impact | Yes |
| Import | Error | | ZIP bytes, hash, task metadata, target, or Core Data Loader validation envelope differs from approval | Restart validation and obtain fresh approval | Yes |
| Any uncertain write or accepted process | Error | | Another update or import is proposed before read-only reconciliation | Verify the existing outcome before considering another mutation | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_customer_hub_profile_definition | Before preview for every view, direct update, guarded option, default request, or changed FSM profile row | Exact definition, current SITE value, SITE enabled/updatable flags, SITE key, and validation metadata | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.DESIGN_GATE | decision | 5 | design_enforcement | pass->CHP.VALIDATED;fail->CHP.ERROR | CHP.APPLY_DEFAULT | stop | Before direct-update preview, immutable import preview, approved execution, or outcome reporting |
