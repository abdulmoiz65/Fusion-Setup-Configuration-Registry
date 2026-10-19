# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Record decisions | Complete each applicable Design Decisions workbook row before preview; leave unassessed decisions blank rather than inferring them |
| 2 | Preserve replacements | Preserve existing optional fields when a current-state check identifies a replacement |
| 3 | Enforce Activity Type baseline | Confirm duration, slot, routing, and feature decisions are supported by the intended operating model before preview |
| 4 | Enforce business design | Apply the applicable Activity Type design rules before preview |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| AT.GROUP_STRATEGY | Selecting an Activity Type Group | Error | verify_activity_type_group | No genuine business need is recorded for a new group and no suitable seeded group is selected | Reuse a suitable seeded group; create a group only for a genuine business need | Yes, before preview |
| AT.DEFAULT_DURATION | Every Activity Type | Error | | Default duration is absent or not a realistic scheduling baseline | Set a realistic default duration | Yes, before preview |
| AT.DURATION_LEARNING | Statistical or learned duration is proposed | Error | | The activity has immature or unrepresentative history, a fixed or case-specific duration, or duration-driving attributes are not captured | Use a realistic manual or fixed default duration. Enable statistical learning only after reliable history exists and its duration-key attributes distinguish materially different work | Yes, before preview |
| AT.SEGMENTATION | Segmentation or extended-duration work is proposed | Error | | The work is not genuinely multi-day or interruptible, statistical duration is enabled, or the integration and back end cannot process multiple activity updates | Reserve segmentation for genuinely multi-day or interruptible work, define sensible segment durations, disable statistical duration, and prove the update-handling design | Yes, before preview |
| AT.TIME_SLOTS | Time-slot support or an Activity Type-to-slot association is proposed | Error | | No appointment-window, booking, routing, assignment-ordering, or quota-management need is documented; an all-day slot is used although the work is time-bounded; or the selected slots are not eligible for the type | Enable only valid operating slots. Use all-day only for work that can occur at any time; for quota-based booking, avoid overlapping or intersecting slots and size slots at least as long as typical work | Yes, before preview |
| AT.ROUTING_CAPABILITIES | Customer work is intended to be routable or an eligibility capability is proposed | Error | | The decision to create work in buckets, move it between resources, or enable zones, skills, travel, preferred resources, links, inventory, API creation, or search is undocumented; or Calculate Travel is disabled for work that requires travel | Record each capability's business effect. Treat bucket creation as durable, enable Calculate Travel for travel-requiring work, and enable zones, skills, preferences, links, inventory, API creation, and search only when the process requires them | Yes, before preview |
| AT.SKILL_AND_ZONE_ELIGIBILITY | Work-skill, work-zone, or preferred-resource support is enabled | Error | | The required eligibility model, level semantics, geographic coverage, or continuity requirement is not documented | Define the activity attributes and routing effect. Use required levels as eligibility thresholds, preferable levels only to rank eligible resources, and do not enable support merely because the related master data exists | Yes, before preview |
| AT.INVENTORY_ROUTING | Required inventory or inventory-aware routing is proposed | Error | | The material requirement, source of truth, and routing impact are not documented | Enable inventory only where material is genuinely required; document how inventory-aware routing changes the assignment process | Yes, before preview |
| AT.NOTIFICATIONS_AND_TIME_ZONE | Message triggers, delivery windows, or customer time zones are proposed | Error | | Notification scenarios, recipients, timing, or cross-time-zone SLA and service-window requirements are not documented | Enable notifications only after the communication design is complete; use customer time zones for SLA or service-window scheduling across time zones | Yes, before preview |
| AT.PRIVACY_AND_PRESENTATION | A color convention or resource-tracking change is proposed | Error | | The status-color convention is inconsistent or undocumented, or tracking is disabled without a privacy, policy, regulation, or labor-agreement basis | Maintain a consistent color and status-color convention, publish its user-facing meaning when changed, and disable tracking only for a documented privacy or policy reason | Yes, before preview |
| AT.INTERNAL_ACTIVITY_PATTERNS | Mass, repeating, or teamwork activities are proposed | Error | | The type is not internal group or recurrent work for mass or repeating behavior, or teamwork does not represent a contributor or assistant working on an activity owned by another resource | Use mass and repeating activities mainly for internal events such as meetings or breaks; use teamwork only for the documented contributor or assistant model | Yes, before preview |
| AT.OPTIONAL_FEATURES | An optional feature, color, time slot, mobility, bucket, duration, segmentation, notification, time-zone, inventory, or tracking setting is proposed | Error | find_activity_type_by_label | The applicable Design Decisions row is unassessed, an applicable specific rule fails, or an optional feature is enabled without a documented business need | Record the business decision and enable only features required by the business process; preserve existing optional fields for replacements | Yes, before preview |

## Source Basis

| Source | Activity Type guidance incorporated |
|---|---|
| 2925263.1-SDD_IMPLEMENTER-OracleFieldService_SDD_Guidelines.docx | Activity settings, travel, skill levels, routing, inventory, and duration-learning constraints |
| 2925263.1-SDD_CUSTOMER-OracleFieldService_Customer_SDD_Guidelines.docx | Activity duration, service-window, time-slot, routing, inventory, and measurable operating requirements |
| fusion_field_service_best_practices.docx | Consolidated direct guidance for activity groups, duration, slots, routing, optional capabilities, segmentation, notifications, time zones, inventory, and tracking |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| AT.GROUP_STRATEGY | verify_activity_type_group | Before preview for each selected group | Group Label and current group state | ora_reference_lookups.md |
| AT.OPTIONAL_FEATURES | find_activity_type_by_label | Before preview for a replacement | Activity Type Label and existing optional fields | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.DESIGN | decision | 4 | design_enforcement | pass->AT.PREVIEW_GATE;fail->AT.RETURN_ISSUES | AT.DEPENDENCIES | stop | Before any REST preview for Activity Types |
