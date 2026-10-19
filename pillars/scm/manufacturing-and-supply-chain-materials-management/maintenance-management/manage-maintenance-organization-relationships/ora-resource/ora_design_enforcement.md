# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce relationship eligibility | Apply the organization and relationship-type restrictions before preview. |
| 2 | Enforce reciprocal direction | For a reciprocal relationship between maintenance organizations, define the relationship from each organization's context when work orders must be created for either organization. |
| 3 | Enforce Data Loader ownership | Route the request through core.data-loader; this task skill must not select a REST endpoint, construct a REST payload, or submit a Fusion write. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Supports as primary is requested | Error | | The related organization is maintenance-enabled, or more than one primary maintenance organization is defined for an organization not enabled for maintenance. | Use supports as primary only from a maintenance organization to a non-maintenance organization, with one primary maintenance organization. | Yes |
| Work orders must be created for either of two maintenance organizations | Warning | | A reciprocal relationship is defined from only one organization's context. | Define the reciprocal relationship from the context of each maintenance organization. | Yes |
| Assets routinely require maintenance across organizations | Warning | | The implementation does not consider the documented recommendation for the Consider Organization Relationships When Creating Maintenance Work Orders parameter. | Set the parameter to No for routine cross-organization maintenance; retain Yes when only selected organizations should provide maintenance to one another. | Yes |
| Maintenance organization relationship create or remove | Error | | The request bypasses the active Run Book or core.data-loader, or the business object is not Maintenance Organization Relationships. | Correct the Run Book task and route before preview. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MMOR.ENFORCE_RELATIONSHIP_DESIGN | decision | 30 | design_enforcement | compliant->MMOR.DATALOADER_GATE;blocked->MMOR.DESIGN_BLOCKED | MMOR.CHECK_DEPENDENCIES | stop | Maintenance organization relationship create or remove |
