# Review Period Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve identity and operation | One deterministic route |
| 2 | Validate dates and usage | Unsafe changes stop |
| 3 | Validate metadata and payload | Only updateable current attributes pass |
| 4 | Bind approval | Environment, target, usage, payload, and fingerprint are final |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| RP.DATE.RANGE | Create or date update | Blocker |  | Start is after end | Correct the inclusive range | Yes |
| RP.USAGE.DELETE | Delete | Blocker | review_period_usage_lookup | Usage is nonzero or unknown | Inactivate or establish zero usage | Yes |
| RP.DELETE.CONTRACT | Delete | Blocker | review_period_describe | Current authoritative metadata does not explicitly advertise DELETE | Use guided UI/inactivation; do not infer DELETE | Yes |
| RP.LOV.READONLY | Any write | Blocker | review_period_lookup | LOV is selected as write endpoint | Use current management contract or guided FSM/UI | Yes |
| RP.APPROVAL.FRESH | Any mutation | Blocker |  | Fresh state differs from preview | Rebuild preview and approval | Yes |
| RP.APPROVAL.TRANSPORT | Multiple updates under one approval | Blocker | review_period_describe | Approval grouping is treated as transport evidence | Resolve the supported method for every operation; use ordered PATCH requests when advertised and batch only when explicitly enabled | Yes |
| RP.RUNBOOK.SEQUENCE | Run Book task execution | Blocker |  | Current parent execution control is absent, stale, or names a different task | Return to the parent resolver and preview the earliest incomplete task | No |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| RP.USAGE.DELETE | review_period_usage_lookup | Delete or risky change | Usage count and references | ora_reference_lookups.md |
| RP.DELETE.CONTRACT | review_period_describe | Delete | Relative item action, DELETE capability, concurrency contract | ora_reference_lookups.md |
| RP.LOV.READONLY | review_period_lookup | Any write | Exact management identity | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.DESIGN | decision | 60 | design_enforcement | passed->REVIEW_PERIODS.REST_DESCRIBE;blocked->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.DEFAULTS | stop | A mutation is ready for design checks |


---

# Review Period Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Packaged | Catalog identity and approved Review Period functional contract | Planning and design explanations |
| Runtime | Current authenticated UI/runtime action metadata, LOV, approved OpenAPI, and usage reads | Environment-specific readiness |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Date envelope | Recommended | Review Period contains the related Goal Plan dates | Invented overlap prohibition |
| In-use change | Strong | Prefer a replacement period and inactivation when dependencies exist | Delete without usage evidence |
| Lifecycle | Strong | Read, create, update, inactivate, metadata-gated delete, and CSV routes are independent | Treating captured create/update calls as DELETE proof |

## Output Rules

| Situation | What Happens |
|---|---|
| Environment metadata differs | Report the difference and follow current supported metadata |
| Management endpoint is not exposed | Provide guided FSM/UI plan and mark REST write blocked |
