# Manage Channel Claim Types Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| BuySideFlag | false | BuySideFlag is omitted from a parent create candidate | No | |
| SellSideFlag | false | SellSideFlag is omitted from a parent create candidate | No | |

No default is assumed for ClaimType, ClaimTypeCode, SetId, SetCode, SetName, effective dates, BusinessUnitId, BUMappingCode, or AR-related optional fields.

Updates apply no defaults. Return unchanged for PATCH, preserving omitted side flags and every unrequested parent/child value. Do not fill blank update cells with false, empty strings, today's date, or copied current values.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCT.APPLY_DOCUMENTED_DEFAULTS | step | 7 | apply_default | applied->CJMCT.FIND_BY_CODE;unchanged->CJMCT.FIND_BY_CODE | CJMCT.VALIDATE_DESIGN | stop | Apply defaults only on create; update and creates with no missing defaulted field return unchanged |
