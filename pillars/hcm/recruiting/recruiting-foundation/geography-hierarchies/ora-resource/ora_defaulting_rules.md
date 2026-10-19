# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| GeoNodeCode | Unique nonblank package-local source code | Creating a node | No | |
| ParentGeoNodeCode | Immediate parent's GeoNodeCode | Creating a child node | No | |
| Identifier LanguageCode | US | Creating an identifier row when the approved source artifact does not specify another value | Yes, with approved source evidence | |
| Identifier PrimaryFlag | Y | Creating an identifier row when the approved source artifact does not specify another value | Yes, with approved source evidence | |
| Identifier display name | Exact authoritative geography name | Creating an identifier row | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHH.DEFAULTS | decision | 30 | apply_default | applied->GHH.ENFORCE;issues->GHH.DESIGN_ISSUES | GHH.READINESS | stop | A valid hierarchy package is being prepared |
