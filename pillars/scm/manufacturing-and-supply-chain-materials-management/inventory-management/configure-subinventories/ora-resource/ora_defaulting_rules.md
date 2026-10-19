# Configure Subinventories Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| User-approved Subinventory Code and Translatable Subinventory Name mapping rule | Defines the permitted local identity copy before Data Loader handoff. |
| Redwood Configure Subinventories flow | Uses SecondaryInventoryName as the subinventory-code attribute and SubinventoryName as the translatable subinventory-name attribute. |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| subinventories.SecondaryInventoryName and subinventories.SubinventoryName | Copy the one supplied logical subinventory identity value to both attributes | The user supplies only Subinventory, Subinventory Code, or Subinventory Name and does not explicitly supply distinct values for both target attributes | Yes. Preserve each explicitly supplied target attribute, including two different values. |  |

## Defaulting Behavior

| Input Shape | What Happens |
|---|---|
| Only Subinventory is supplied | Populate SecondaryInventoryName and SubinventoryName with that value. |
| Only Subinventory Code is supplied | Populate SecondaryInventoryName and SubinventoryName with that value. |
| Only Subinventory Name is supplied | Populate SecondaryInventoryName and SubinventoryName with that value. |
| Both SecondaryInventoryName and SubinventoryName are explicitly supplied | Preserve the supplied code in SecondaryInventoryName and the supplied name in SubinventoryName; do not overwrite either value, even when they differ. |
| Neither logical identity value nor target attribute is supplied | Do not apply a default; Data Loader and Fusion own required-field enforcement. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSUBINV.APPLY_SUBINVENTORY_IDENTITY_DEFAULT | step | 5 | apply_default | applied->CSUBINV.VALIDATE_LOOKUP_INPUTS;not_applicable->CSUBINV.VALIDATE_LOOKUP_INPUTS | none | stop | Before Configure Subinventories normalization, validation, and LOV resolution. |
