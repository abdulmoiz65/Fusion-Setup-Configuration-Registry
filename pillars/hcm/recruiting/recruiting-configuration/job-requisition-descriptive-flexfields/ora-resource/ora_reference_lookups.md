# Job Requisition Descriptive Flexfields Reference Lookups

Use this read-only lookup only when a configuration change specifies an LOV or value set and the authoritative contract has been supplied. Do not derive valueSets_Id from a value-set name or code.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_dff_reference_authority | A configuration change specifies an LOV or value set and its authoritative contract is supplied | Value-set identity and DFF segment association from exported configuration or the approved change request | /fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}/child/values | Only fields documented by the resolved value-set response and required by the approved DFF change | Use the returned valueSets_Id; do not derive it from a value-set name or code | Approved DFF change value mapping | Stop and obtain the authoritative LOV or value-set contract |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The authoritative LOV or value-set contract is absent or incomplete | Stop before preview, import, export, activation, or Fusion access |
| A value-set name or code is supplied without a returned valueSets_Id | Do not derive the identifier; obtain the authoritative contract |
| The approved read-only route returns no match, multiple matches, or an error | Stop and obtain the authoritative LOV or value-set contract |
