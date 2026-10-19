# Landed Cost Reference Types Defaulting Rules

Source: User-supplied Landed Cost Reference Types Data Loader rule.

## Default Values

| Business Value | Default | When to Use | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|
| InactiveFlag | false, stored as N | The user omits InactiveFlag and does not state an active or inactive status | Yes | The user explicitly requires omitted values to be treated as false. |

## Conversion Rules

| Supplied or Default Value | Data Loader Source Value | Applies When | What Must Happen |
|---|---|---|---|
| true | Y | InactiveFlag is supplied as true or the business user states Inactive | Write the literal Y in the Data Loader source. |
| false | N | InactiveFlag is supplied as false, the business user states Active, or the value is omitted | Write the literal N in the Data Loader source. |

## Defaulting Rules

| Rule | What Happens |
|---|---|
| Omitted InactiveFlag | Apply false, then write N to the Data Loader source. |
| Supplied InactiveFlag | Preserve the supplied Boolean meaning, then write only its literal Y or N representation to the Data Loader source. |
| Invalid source representation | Stop before preview when the prepared Data Loader field is any value other than Y or N. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.DEFAULT_INACTIVE_FLAG | step | 15 | apply_default | defaulted->LANDED_COST_REFERENCE_TYPES.RESOLVE_SET_ID;converted->LANDED_COST_REFERENCE_TYPES.RESOLVE_SET_ID;invalid->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.VALIDATE_INPUT | stop | Before preparing the Landed Cost Reference Types Data Loader source. |
