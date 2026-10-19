# Defaulting Rules

## Defaults

| Field(s) | Default value | Applies when | Explicit request | Handling |
|---|---|---|---|---|
| Payment Options fields | No inferred default | A field is omitted from a create request | Preserved; never replaced | Do not invent a value; Fusion validates the submitted candidate. |

## Defaulting Boundary

Do not infer a Payment Options default from an observed export value. Preserve
unrelated exported values exactly.
