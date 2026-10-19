# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Data Loader object | Confirm workOrderStatuses and the requested REST operation through read-only Core Data Loader metadata. |
| 2 | Existing status identity | Resolve the selected status for update, deactivation, or deletion. |
| 3 | Status uniqueness and system status | Confirm unique code and name as applicable, and validate the requested system-status lookup code. |
| 4 | Deletion eligibility | Confirm the status is user-defined and not referenced by work order headers or history. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| registered_loader_object | Registered workOrderStatuses Business Object | Yes | Any REST Data Loader import | Verify | Core Data Loader read-only metadata | confirm_work_order_statuses_loader_object | The requested operation must use the confirmed registered object | Stop and provide the confirmed object or request an approved FSM fallback after REST is proven unavailable | Business Object, supported operation |
| existing_status | Exact existing status | Yes | Update, deactivation, or delete | Verify | workOrderStatuses REST resource | resolve_work_order_status_by_id | Protection and allowed changes depend on the selected status | Supply the exact status ID | WoStatusId, SeededFlag, existing fields |
| valid_system_status | Valid system status lookup code | Yes | Create | Verify | ORA_WIE_WO_SYSTEM_STATUS lookup | resolve_work_order_system_status | A status must be associated to a valid system status | Use an exact lookup code such as UNRELEASED or RELEASED, not an ORA_-prefixed variant | WoSystemStatusCode |
| delete_eligibility | User-defined and unreferenced status | Yes | Delete | Verify | Core Data Loader validation using workOrderStatuses metadata and dependencies | resolve_work_order_status_by_id | Seeded statuses and statuses referenced by headers or history cannot be deleted | Do not request deletion until the status is user-defined and unreferenced | WoStatusId, SeededFlag, reference result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| satisfied | Every applicable object, identity, lookup, and deletion prerequisite is confirmed | Read-only lookup only; no create or import is authorized here. |
| blocked | A required object, status, lookup code, or deletion prerequisite is missing, ambiguous, protected, or referenced | Read-only verification only; stop before preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOSTATUS.DEPENDENCIES | decision | 4 | resolve_dependency | ready->WOSTATUS.DESIGN;blocked->WOSTATUS.BLOCKED | WOSTATUS.LOOKUPS | stop | Applicable work order status dependencies are evaluated. |
