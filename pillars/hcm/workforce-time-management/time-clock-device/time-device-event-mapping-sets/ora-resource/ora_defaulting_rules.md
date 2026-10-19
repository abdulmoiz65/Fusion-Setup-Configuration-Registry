# Time Device Event Mapping Set Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Description | No default | Description is omitted | No | |
| Event Mappings | No default | A Mapping Set is prepared | No; at least one user-selected Event Mapping is required | |

## Defaulting Boundaries

| Situation | What Happens |
|---|---|
| Description is omitted | Preserve the omission; do not invent a description. |
| Event Mappings are absent | Do not default a mapping. Stop because one or more user-selected Event Mappings are required. |
| No default is applicable | Continue to Complete Summary generation with an empty Defaults Applied table body. |

## Complete Summary Default Presentation

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Applied defaults | Include every user-facing default that was actually applied in Defaults Applied using its business label and verified business display value | A Complete Summary is generated | No | |
| Identifier display | Replace an identifier with its resolved business display name | A populated identifier would otherwise be shown | No | |
| Code display | Replace a code with its verified business meaning | A populated code would otherwise be shown | No | |
| Boolean display | Use Selected or Not selected, Enabled or Disabled, or Yes or No when a verified business label is available | A populated Boolean is shown | No | |
| Status display | Use a verified business-friendly status such as Draft or Submitted | A populated internal status is shown | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_APPLY_DEFAULTS | step | 6 | apply_default | applied->TDEMSET_ENFORCE_SUMMARY;not_applicable->TDEMSET_ENFORCE_SUMMARY;blocked->TDEMSET_DEFAULTS_BLOCKED | TDEMSET_RESOLVE_MAPPING_IDS | stop | A request passed input, criteria search, parent-child, and Event Mapping validation |
