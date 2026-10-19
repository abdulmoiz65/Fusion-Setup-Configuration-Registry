# Lot and Serial Attribute Mappings Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| User-approved organization mapping rule | Defines mutually exclusive OrganizationCode and OrganizationId shaping for the task contract. |
| Redwood commonToOrganizationsTemplate | The All option emits OrganizationId -1; the Specific option is scoped to an organization. |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| OrganizationId | -1 | Organization is omitted or blank. | Yes. Leave OrganizationId blank when an organization is supplied. |  |
| OrganizationCode | Supplied organization value | Organization is supplied. | Yes. Leave OrganizationCode blank when OrganizationId is defaulted to -1. |  |

## Defaulting Behavior

| Input Shape | What Happens |
|---|---|
| Organization is supplied | Map the supplied value to OrganizationCode and leave OrganizationId blank. |
| Organization is omitted or blank | Set OrganizationId to -1 for All organizations and leave OrganizationCode blank. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSAM.APPLY_ORGANIZATION_DEFAULT | step | 5 | apply_default | applied->LSAM.NORMALIZE_RADIO_VALUES;not_applicable->LSAM.NORMALIZE_RADIO_VALUES | none | stop | Before Attribute and Level normalization and Data Loader dependency checks. |
