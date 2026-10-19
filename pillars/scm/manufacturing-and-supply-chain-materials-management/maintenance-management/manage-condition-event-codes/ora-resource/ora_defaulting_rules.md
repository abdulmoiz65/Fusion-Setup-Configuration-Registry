# Defaulting Rules

## Documented Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Condition Event Code Disable Flag | false | A new code is created and no disable value is supplied | Yes | |
| Active End Date | System-maintained | The disable flag is true | No | |
| Condition Event Category Code | No value | Category is not supplied | Yes | |

## Defaulting Rules

| Rule | What Happens | Applies When | User Guidance |
|---|---|---|---|
| Description-only update | Preserve type, category, active status, and end date from the resolved source row | A description-only change is approved | Include only the identity and description change in the approved source data |
| End-date request | Do not supply the system-maintained Active End Date | A code must become inactive | Use only the supported disable input field |
