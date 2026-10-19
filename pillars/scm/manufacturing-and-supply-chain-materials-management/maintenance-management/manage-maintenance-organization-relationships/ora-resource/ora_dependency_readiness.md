# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Organization eligibility | The contextual organization must be maintenance-enabled; relationship-type constraints must be satisfied. |
| 2 | Work-order prerequisites | Before creating work orders in a related organization, inventory organization access and the asset source item enabled in that organization must be available. |
| 3 | Maintenance-program prerequisites | For cross-organization maintenance-program work orders, work definitions must be duplicated across organizations with a common work definition code. |
| 4 | Data Loader source | Before the Task Hook and preview, core.data-loader must have generated a live-schema sample or validated the supplied setup-data artifact. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MMOR_ORGANIZATION_ELIGIBILITY | Contextual and related organization eligibility | Yes | Every create or remove request | Verify | Requested relationship and Oracle relationship constraints | | Relationship types are constrained by whether each organization is maintenance-enabled. | Provide the contextual and related organizations and select a permitted relationship type. | Contextual organization, related organization, relationship type |
| MMOR_WORK_ORDER_ACCESS | Inventory organization access and source item availability | Yes | Creating work orders in a related organization | Verify | Fusion security and item setup | | Oracle requires access to every work-order organization and the asset source item enabled for each one. | Confirm access and item enablement before relying on the relationship for work-order creation. | Work-order organizations and source item readiness |
| MMOR_PROGRAM_WORK_DEFINITION | Common work definition | Yes | Creating work orders across organizations in a maintenance program | Verify | Maintenance program and work-definition setup | | Oracle requires duplicated work definitions with a common code; otherwise work orders are not created. | Duplicate work definitions across the organizations and use the same work definition code. | Work-definition readiness |
| MMOR_SOURCE_ARTIFACT | Data Loader source artifact | Yes | Every create or remove request | Verify | core.data-loader result | | The Task Hook runs only after the exact immutable upload artifact is prepared. | Generate the live sample from Maintenance Organization Relationships or validate the supplied artifact through core.data-loader. | Generated or validated artifact fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every mandatory dependency is verified and the source artifact is prepared. | No |
| Blocked | An organization, access, source item, work definition, or source artifact is missing or incompatible. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MMOR.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->MMOR.ENFORCE_RELATIONSHIP_DESIGN;blocked->MMOR.DEPENDENCY_BLOCKED | MMOR.VALIDATE_INPUT | stop | Maintenance organization relationship create or remove |
