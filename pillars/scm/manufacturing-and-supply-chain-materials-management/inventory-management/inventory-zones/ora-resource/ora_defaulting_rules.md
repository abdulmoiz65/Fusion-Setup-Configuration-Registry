# Inventory Zones Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| StartDate | Current local date in YYYY-MM-DD format | A create request omits StartDate. | No |  |
| StatusCode | DRAFT | A create request omits StatusCode. | No |  |
| TasksEnabled | Y | A create or update request contains an Inventory Zones Activity Usages child row after the system-managed field validation passes. | No — user input is rejected |  |
| TaskGroupingLevel | ZONE | A create or update request contains an Inventory Zones Activity Usages child row after the system-managed field validation passes. | No — user input is rejected |  |
| ActivityTypeCode | DEL | A create or update request contains an Inventory Zones Configurations child row that sets DefaultDeliveryCartId after the system-managed field validation passes. | No — user input is rejected |  |
| ConfigurationLevel | A | A create or update request contains an Inventory Zones Configurations child row that sets DefaultDeliveryCartId after the system-managed field validation passes. | No — user input is rejected |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV-ZONES.APPLY-START-DATE-DEFAULT | step | 40 | apply_default | applied->INV-ZONES.APPLY-STATUS-DEFAULT;not_applicable->INV-ZONES.APPLY-STATUS-DEFAULT | INV-ZONES.VALIDATE-SYSTEM-MANAGED-FIELDS | stop | A create request omits StartDate. |
| INV-ZONES.APPLY-STATUS-DEFAULT | step | 50 | apply_default | applied->INV-ZONES.ENFORCE-TASKS-ENABLED;not_applicable->INV-ZONES.ENFORCE-TASKS-ENABLED | INV-ZONES.APPLY-START-DATE-DEFAULT | stop | A create request omits StatusCode. |
| INV-ZONES.ENFORCE-TASKS-ENABLED | step | 55 | apply_default | applied->INV-ZONES.ENFORCE-TASK-GROUPING-LEVEL;not_applicable->INV-ZONES.ENFORCE-DELIVERY-CART-ACTIVITY-TYPE | INV-ZONES.APPLY-STATUS-DEFAULT | stop | Every create or update request for an Inventory Zones Activity Usages child row. |
| INV-ZONES.ENFORCE-TASK-GROUPING-LEVEL | step | 57 | apply_default | applied->INV-ZONES.ENFORCE-DELIVERY-CART-ACTIVITY-TYPE;not_applicable->INV-ZONES.ENFORCE-DELIVERY-CART-ACTIVITY-TYPE | INV-ZONES.ENFORCE-TASKS-ENABLED | stop | Every create or update request for an Inventory Zones Activity Usages child row. |
| INV-ZONES.ENFORCE-DELIVERY-CART-ACTIVITY-TYPE | step | 58 | apply_default | applied->INV-ZONES.ENFORCE-DELIVERY-CART-CONFIGURATION-LEVEL;not_applicable->INV-ZONES.ENFORCE-DELIVERY-CART-CONFIGURATION-LEVEL | INV-ZONES.ENFORCE-TASK-GROUPING-LEVEL | stop | Every create or update request for an Inventory Zones Configurations child row that sets DefaultDeliveryCartId. |
| INV-ZONES.ENFORCE-DELIVERY-CART-CONFIGURATION-LEVEL | step | 59 | apply_default | applied->INV-ZONES.DONE;not_applicable->INV-ZONES.DONE | INV-ZONES.ENFORCE-DELIVERY-CART-ACTIVITY-TYPE | stop | Every create or update request for an Inventory Zones Configurations child row that sets DefaultDeliveryCartId. |
