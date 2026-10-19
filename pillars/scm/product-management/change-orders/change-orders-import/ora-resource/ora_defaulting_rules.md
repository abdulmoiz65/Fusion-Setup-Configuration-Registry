# Change Order FBDI Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Any template field | Only an explicit current-template default | Customer value is blank and the template authorizes it | No | |
| Status Name | No default | Every Change Order header | No; the source must supply it exactly and it must be valid for the current template | |
| Batch ID | No generic default | Template requires a Batch ID but customer has not supplied a valid value | No; return an issue | |
