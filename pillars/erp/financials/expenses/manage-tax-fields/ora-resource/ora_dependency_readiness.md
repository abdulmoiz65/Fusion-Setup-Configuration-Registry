# Manage Tax Fields dependencies

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TAX.BU | Active target business unit | Yes | create or update | Lookup | Target Fusion enterprise | resolve_tax_business_unit | Import resolves BU in enterprise context | Resolve exact target BU before candidate construction | Validated BU identity |
| TAX.COUNTRY | Country or territory | Conditional | TerritoryCode is not OTHER | Lookup | Target Fusion territories | resolve_tax_territory | Entity existence validation | Supply valid country code | Validated territory |
| TAX.BEHAVIOR | Enabled behavior lookup codes | Yes | rule field change | Verify | EXM_FIELD_BEHAVIOUR | resolve_tax_behaviors | FSM entity list validation | Supply an explicit supported code; target membership is checked during approved import | Exact supplied codes; target acceptance remains pending import result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAX.DEPENDENCIES | step | 3 | resolve_dependency | success->TAX.DEFAULTS;failure->TAX.ISSUES | TAX.LOOKUPS | stop | create or update |
