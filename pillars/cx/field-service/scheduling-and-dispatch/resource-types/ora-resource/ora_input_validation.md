# Resource Types Workbook Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Resource Types workbook | A supplied workbook containing a Resource Types worksheet | Stop before preview | Provide the configuration workbook and select the Resource Types worksheet | Always | |
| Resource Type identity | One non-empty Resource Type label for each proposed type | Stop before preview | Supply a unique label for every proposed Resource Type | A Resource Type is created or changed | |
| Configuration selection | Active state and documented selections for the configuration areas that apply | Stop before preview | Complete the applicable workbook selections and document omitted areas as not applicable | A Resource Type is created or changed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Duplicate Resource Type label | Block preview and require a unique Resource Type label | More than one proposed type has the same label | |
| Empty Resource Type label | Block preview and require a non-empty Resource Type label | A proposed type has no label | |
| Contradictory mutually exclusive selection | Block preview and require one documented configuration choice | A proposed type selects incompatible workbook options | |
| Workbook row-to-REST payload mapping | Keep the workbook as design input and block REST mutation until the documented payload mapping exists | A REST import is requested | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RT.VALIDATE_WORKBOOK | step | 1 | validate_input | valid->RT.CHECK_OPERATING_MODEL;invalid->RT.RETURN_ISSUES | none | stop | A Resource Types workbook is supplied for preview |
