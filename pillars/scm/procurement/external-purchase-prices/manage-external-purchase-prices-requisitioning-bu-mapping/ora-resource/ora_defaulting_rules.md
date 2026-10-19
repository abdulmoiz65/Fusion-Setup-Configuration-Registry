# External Purchase Prices Requisitioning BU Mapping Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ActivationFlag | true | Parent POST only, when the activation value is absent or blank | No |  |
| ActivationFlag | No default; preserve the supplied value or absence | Parent PATCH, parent DELETE, child-only operations, or read-only requests | No |  |
| requisitioningBusinessUnits | Preserve supplied child values and operations in the representation selected by core.data-loader | When supplied | No |  |

Do not default SourceOrganization. ProcurementBUId, RequisitioningBUId, MappingId, StatusCode, and Status are optional and are preserved when supplied.

An explicit false is a supplied value, not an empty value. Do not add a parent
activation change to a child-only load. The shared loader owns representation
and serialization; this rule does not require an embedded REST collection or
prohibit its registered child sections.

## Golden Scenarios

These are synthetic validation examples, not approved execution payloads.

| Scenario | Requested Operation | Supplied ActivationFlag | Expected Result |
|---|---|---|---|
| create-absent | Parent POST | absent | Default true and disclose the default before approval |
| create-blank | Parent POST | blank | Default true and disclose the default before approval |
| create-true | Parent POST | true | Preserve true |
| create-false | Parent POST | false | Preserve false |
| update-absent | Parent PATCH | absent | Leave absent; do not reactivate the mapping |
| update-false | Parent PATCH | false | Preserve false |
| delete-parent | Parent DELETE | absent | Leave absent |
| create-child | Child POST only | absent | Do not add a parent activation change |
| delete-child | Child DELETE only | absent | Do not add a parent activation change |
| read-only | GET | absent | No default and no mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.APPLY_DEFAULTS | step | 40 | apply_default | applied->EPPBU.ENFORCE_DESIGN;blocked->EPPBU.HANDLE_ERROR | EPPBU.CHECK_DEPENDENCIES | stop | After dependencies are ready |

