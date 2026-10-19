# Item Packing Unit Configurations Defaulting Rules

Source: approved Default-field contract, Redwood create-row initialization, and live Data Loader metadata for configureDefaultPackingUnits.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| DefaultFlag | true | A Create operation has no user-facing Default value and the REST/Data Loader route is selected | No | |
| PreferredFlag | Preserve blank | The FSM route is selected and PreferredFlag is blank in the source export | No | |

An explicit supported Default input is normalized for Create or Update before this rule. The REST/Data Loader route retains the string true or false in DefaultFlag. The FSM route retains Y or N in PreferredFlag. Do not default DefaultFlag during Update or Delete; an Update preserves an absent Default value and Delete has no Default processing.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IPUC.APPLY_DEFAULT | decision | 20 | apply_default | applied->IPUC.DONE;not_applicable->IPUC.DONE;failed->IPUC.HANDLE_ISSUE | IPUC.VALIDATE_DEFAULT | stop | A Create operation has no Default value after validation |
