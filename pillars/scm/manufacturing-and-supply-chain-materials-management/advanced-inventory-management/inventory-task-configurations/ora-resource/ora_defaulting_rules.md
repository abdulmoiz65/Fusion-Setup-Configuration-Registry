# Inventory Task Configurations Defaulting Rules

Defaults below are sourced from the Redwood first-load path for an organization with no default zone. They apply only to Create when the caller requests the Redwood-equivalent initial configuration and does not supply the field. Update reads the existing default-zone activity configuration and preserves any setting the caller does not explicitly change.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ZoneName | OrganizationCode plus a space plus Default | A default zone does not exist for the resolved organization and ZoneName is absent. OrganizationCode is consumed after this derivation and is never sent to REST. | No | resolve_inventory_organization_by_name |
| Description | System-defined default zone used for managing tasks and workers when a user-defined zone isn't available. | A default zone does not exist for the resolved organization and Description is absent. | No | |
| StartDate | Current local date rendered in the XLSX as YYYY-MM-DD | A default zone does not exist for the resolved organization and StartDate is absent. | No | |
| StatusCode | ACTIVE | A default zone does not exist for the resolved organization and StatusCode is absent. Redwood REST create source uses StatusCode; do not send Status. | No | |

## Canonical Activity Matrix

| ActivityTypeCode | Default TasksEnabled | TaskGroupingLevel Rule |
|---|---:|---|
| PICK | N | `PICKSLIP` |
| CC | N | `ZONE` by default; allow a resolved CC grouping override. |
| PC | N | `ZONE` by default; allow a resolved PC grouping override. |
| PAR | N | `ZONE` for every emitted row. |
| DEL | N | `DELIVERY_CART` for every emitted row. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV_TASK_CONFIG.APPLY_ACTIVITY_DEFAULTS | step | 30 | apply_default | defaulted->INV_TASK_CONFIG.CHECK_PARENT_CHILD_READINESS;not-applicable->INV_TASK_CONFIG.CHECK_PARENT_CHILD_READINESS | INV_TASK_CONFIG.RESOLVE_TASK_GROUPING | stop | Redwood-equivalent initial configuration only. |
