# Revision Preferences for Sales Orders Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve live attributes | Use the current discovery response before evaluating group membership. |
| 2 | Normalize request | Resolve the user-facing name and localized preference meaning. |
| 3 | Expand atomic group | Apply one consistent preference to every returned member of the selected group. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A member of the fulfillment, subinventory, supplier site, and supplier group is requested | Error | discover_revision_preference_attributes | The request does not apply the same preference to RequestedFulfillmentOrganizationId, SubInventoryCode, SupplierSiteId, and SupplierId, or a group member is unavailable. | Expand the request to every returned group member, using the same preference. | Yes |
| A member of the override schedule and scheduled dates group is requested | Error | discover_revision_preference_attributes | The request does not apply the same preference to OverrideScheduleDateFlag, ScheduleArrivalDate, and ScheduleShipDate, or a group member is unavailable. | Expand the request to every returned group member, using the same preference. | Yes |
| A member of the ship-to details group is requested | Error | discover_revision_preference_attributes | The request does not apply the same preference to ShipToAddress, ShipToContact, ShipToContactMethod, and ShipToCustomer, or a group member is unavailable. | Expand the request to every returned group member, using the same preference. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| discover_revision_preference_attributes | Before every group expansion and pre-upload approval preview | Exact returned attribute names and RevisionRequiredFlag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVISION_PREFERENCES.ENFORCE_GROUPS | step | 30 | design_enforcement | groups-consistent->REVISION_PREFERENCES.APPROVAL_GATE;group-conflict-or-incomplete->RETURN_ISSUES | REVISION_PREFERENCES.DISCOVER_ATTRIBUTES | stop | A requested attribute belongs to an atomic Revision Preferences group. |
