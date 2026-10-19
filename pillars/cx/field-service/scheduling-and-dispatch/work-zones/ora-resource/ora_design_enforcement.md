# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate workbook candidates | Validate each populated Work Zone row and reject duplicate keys. |
| 2 | Enforce Work Zone design | Apply every WZ design rule before preview. |
| 3 | Enforce REST readiness | Do not use Data Loader. Proceed only through the documented `ora_rest_execution` contract after target identity, current-state, immutable-preview, and approval gates pass. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| WZ.GEOGRAPHIC_ELIGIBILITY | A Work Zone is created or changed | Error |  | The zone does not represent a defined geographic eligibility boundary, or it is so small that too few resources remain eligible | Use Work Zones for geographic eligibility; size them to preserve a practical routing pool | Yes, before preview |
| WZ.STABLE_KEY | A Work Zone key is defined | Error |  | The key is unstable, incoming activities cannot reliably resolve it, or one activity can resolve to multiple zones | Use a stable key, typically ZIP or postal code, and ensure every incoming activity resolves to exactly one Work Zone | Yes, before preview |
| WZ.NO_OVERLAPPING_KEYS | Keys are assigned to multiple Work Zones | Error |  | The same key belongs to more than one zone | Do not create overlapping keys; each key belongs to only one Work Zone | Yes, before preview |
| WZ.SUPPORT_AND_GOVERNANCE | Work Zone Support or the key definition is enabled or changed | Error |  | Work Zone Support is not enabled before configuration, or the key-definition change is uncontrolled | Enable Work Zone Support before configuration and tightly control changes to the key definition | Yes, before preview |
| WZ.COMPOUND_KEY | A compound key is proposed | Error |  | No clear business reason exists for adding key complexity | Use compound keys only for a documented business need; otherwise use the simplest stable key | Yes, before preview |
| WZ.ASSIGNMENT_MODEL | Zones are assigned to resources | Error |  | Direct assignments are used as the normal model, or short-term coverage is modeled as a permanent assignment | Assign normal zones through the organization structure. Use direct assignments only for intentional overrides and temporary assignments only for short-term coverage | Yes, before preview |
| WZ.TEMPORARY_COVERAGE | A temporary Work Zone assignment is proposed | Error |  | Dispatchers have not accounted for the resource becoming exclusively eligible for that temporary routing zone | Use temporary assignments only for short-term coverage and configure dispatcher views for the resulting exclusive routing-zone effect | Yes, before preview |
| WZ.IMMEDIATE_OVERRIDE | Immediate-routing Work Zone overrides are proposed | Error |  | The work is not genuinely urgent, or normal geographic controls are being bypassed for convenience | Use immediate-routing overrides only when urgency outweighs normal geographic eligibility controls | Yes, before preview |
| WZ.TRAVEL_AREA_ALIGNMENT | Work Zones are assigned to Travel Areas | Error |  | A zone has no Travel Area, or a large or diverse area is kept together despite poor travel-estimation accuracy | Assign every Work Zone to a Travel Area. Split large or diverse coverage where it improves travel-estimation accuracy | Yes, before preview |
| WZ.NEW_TERRITORY_LEARNING | A new territory is introduced | Error |  | The design assumes reliable travel estimates exist without sufficient independent travel data | Consider a temporary Travel Area, seed it with activities or approved travel-time overrides, then merge only after reliable data accumulates | Yes, before preview |
| WZ.POST_CHANGE_VALIDATION | Work Zone keys or assignments are changed | Error |  | No validation proves every key maps to a zone and the intended resources are eligible | Validate key-to-zone resolution and representative routing eligibility after every material change | Yes, before preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WZ.ENFORCE_DESIGN | decision | 2 | design_enforcement | pass->WZ.RETURN_SUCCESS;blocked->WZ.RETURN_ISSUES | WZ.VALIDATE_WORKBOOK | stop | After workbook validation and before previewing a Work Zone configuration. |
