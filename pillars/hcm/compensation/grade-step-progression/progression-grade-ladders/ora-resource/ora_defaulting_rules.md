# Defaulting Rules

## Metadata-Declared Defaults

| Field | Applies When | Default | Source | Resolution Rule | Override Behavior |
|---|---|---|---|---|---|
| `EffectiveEndDate` | A Progression Grade Ladder parent, grade membership, step-rate, or step-rate-value row omits the end date | End of time | Live Data Loader attribute description | Leave the field blank to use the documented end-of-time default | A supplied end date is validated against the current date field contract; it is not overwritten |

## Defaulting Boundaries

- No default is inferred for lookup-backed, foreign-key, required, or optional fields unless current live metadata explicitly documents one.
- The end-date default does not bypass current schema validation or any date-effective dependency contract.
