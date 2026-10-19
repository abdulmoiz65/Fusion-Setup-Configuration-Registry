# Inventory Zones Input Validation

## LOV Input Contracts

| Field | Accepted User Input | Canonical Backend Field | Resolver | What Happens |
|---|---|---|---|---|
| Zone status | Status code or status meaning | StatusCode | resolve_inventory_zone_status | Resolve exactly one approved status before Data Loader handoff. |
| Activity type | Activity type code or activity type meaning | ActivityTypeCode | resolve_inventory_zone_activity_type | Resolve exactly one approved activity type before Data Loader handoff. |

## Route-Aware Activity Type Normalization

Scope this section to an Inventory Zones Activity Usages child row. It does not
apply to the Default Delivery Cart configuration default of ActivityTypeCode
equal to DEL.

Trim whitespace and compare lookup codes and meanings case-insensitively for
an exact match. Resolve exactly one row through
resolve_inventory_zone_activity_type; do not fuzzy-match. Preserve an omitted
value for approved defaulting or Data Loader validation.

| Field | Accepted Input | REST/Data Loader Canonical Output | FSM Canonical Output | Applies When |
|---|---|---|---|---|
| ActivityTypeCode | Exact activity-type lookup code or exact lookup meaning | LookupCode | Meaning | An Inventory Zones Activity Usages child row supplies ActivityTypeCode. |

### Route Rules

| Route | Interpretation of ActivityTypeCode | Required Normalization |
|---|---|---|
| FSM import or export | ActivityTypeCode is the activity-type lookup Meaning. | Preserve Meaning for FSM. Before REST Data Loader handoff, resolve Meaning and populate REST ActivityTypeCode with LookupCode. |
| REST/Data Loader | ActivityTypeCode is the activity-type LookupCode. A UI-friendly Meaning is accepted only as an input convenience and must resolve first. | Send LookupCode only. |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Inventory Zone status input | When supplied, accept a code or meaning. When both are supplied, require both to resolve to the same single row. Block a no-match, ambiguous match, or conflict. No status input passes this check and continues to the resolver's not-applicable route. | Every request. | resolve_inventory_zone_status |
| Inventory Zone activity type input | When supplied, accept a code or meaning. For an FSM Activity Usages CSV, interpret ActivityTypeCode as ActivityTypeMeaning; resolve it and write the returned LookupCode to REST/Data Loader ActivityTypeCode. When both code and meaning are supplied, require both to resolve to the same single row. Block a no-match, ambiguous match, or conflict. No activity type input passes this check and continues to the resolver's not-applicable route. | Every request. | resolve_inventory_zone_activity_type |
| Inventory Zone date input | StartDate and EndDate, when supplied, must use the exact YYYY-MM-DD format. Block timestamps, locale-specific formats, and invalid calendar dates. | A request supplies StartDate or EndDate. |  |
| Activity Usages system-managed fields | Block the handoff if a user supplies TasksEnabled or TaskGroupingLevel. These fields are populated by the task rule and users must not provide a value, including the required value. | A create or update request contains an Inventory Zones Activity Usages child row. |  |
| Default Delivery Cart system-managed fields | Block the handoff if a user supplies ActivityTypeCode or ConfigurationLevel when a Configurations child row sets DefaultDeliveryCartId. These fields are populated by the task rule and users must not provide a value, including the required value. | A create or update request contains an Inventory Zones Configurations child row that sets DefaultDeliveryCartId. |  |
| Data Loader schema enforcement | Do not duplicate Business Object required-field, uniqueness, length, domain, or cross-record validation locally. | Every request. |  |

## Golden Scenarios

| Scenario | Expected Result |
|---|---|
| Header-only zone with no status, activity type, or child rows | Pass local validation; both resolvers and all child-only defaults take their declared not-applicable routes; complete at DONE. |
| Zone with an Activity Usages child row and no system-managed values | Pass system-managed validation; populate TasksEnabled as Y and TaskGroupingLevel as ZONE; complete at DONE. |
| Zone with a Configurations child row that sets DefaultDeliveryCartId and no system-managed values | Pass system-managed validation; populate ActivityTypeCode as DEL and ConfigurationLevel as A; complete at DONE. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV-ZONES.VALIDATE-LOV-INPUTS | step | 10 | validate_input | valid->INV-ZONES.RESOLVE-STATUS;invalid->INV-ZONES.RETURN-ISSUES | none | stop | Every request. Validate status and activity type only when supplied; otherwise pass to the resolver not-applicable routes. |
| INV-ZONES.VALIDATE-SYSTEM-MANAGED-FIELDS | step | 35 | validate_input | valid->INV-ZONES.APPLY-START-DATE-DEFAULT;invalid->INV-ZONES.RETURN-ISSUES | INV-ZONES.RESOLVE-ACTIVITY-TYPE | stop | Every request. Reject user-supplied system-managed child fields when their child-row condition applies. |
