# Item Structure Import Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Template-defined optional fields | Template or Oracle-documented default | Only when the latest compatible template or current Oracle guidance explicitly defines the default | No; preserve every supplied nonblank value | |

No item-structure field default is assumed from Item Import. Use only defaults
documented for the Item Structure Import template retrieved for the run.
