# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Double Opt In Locations | Remove all locations | Mode is null or GLOBAL on Save and Close | Yes, select LIST_OF_REGIONS before Save and Close | |
| Enable when candidate location cannot be determined | N | Mode is null or GLOBAL on Save and Close | Yes, select LIST_OF_REGIONS before Save and Close | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.APPLY_MODE_DEFAULT | step | 40 | apply_default | enabled->DOI.INFORM_NOTIFICATION_LIBRARY;disabled->DOI.RETURN_NO_OPT_IN | DOI.ENFORCE_REGION_DESIGN | continue | Before Save and Close |
