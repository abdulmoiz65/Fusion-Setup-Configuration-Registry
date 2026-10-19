# Manage Tax Fields input validation

Evidence: FSM-EXPORT, SRC-CS-EO, SRC-CS-TAX-SETUP-VO, SRC-CS-UI-AM. See ../references/evidence.md.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target and business intent | Environment, operation, BuName, requested field behaviors | Return issues | Request the missing scope; no global fallback | create or update | |
| Tax rule identity | BuName and TerritoryCode | Return issues | Country/territory or explicit OTHER | tax rule change | resolve_tax_territory |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Field behavior codes | Accept DISABLED, ENABLED, REQUIRED; reject other supplied codes | six Enable*Code attributes | resolve_tax_behaviors |
| EnabledFlag | Accept Y or N when supplied; no inferred default | flag supplied | |
| Tax switch | OptionCode must be ENABLE_TAX and ValueCode Y or N | setup option change | |
| Duplicate identities | Reject conflicting changes for the same BU/territory or BU/option | multiple requested rows | |
| Package shape | Preserve exact headers and metadata from same-task template | FSM preparation | |
| Business-field serialization | On create require every task business field explicitly; on update preserve unspecified business values from the fresh baseline. Do not support blank-as-clear or omission-as-default | create or update | |
| Audit serialization | Preserve audit headers and serialize empty cells for CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy and LastUpdateLogin using the builder adapter convention; never accept user audit values (BUILDER-AUDIT-CONTRACT) | candidate preparation | |
| Single setup-option member | Populate requested ENABLE_TAX rows only in EXM_SETUP_OPTION.csv. Keep EXM_CASH_ADV_SETUP_AND_POLICY.csv header-only; reject any data rows in that member. Retain EXM_VAT_FIELD.csv for requested tax rules and preserve every package member and exact header | create or update | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAX.INPUT | step | 1 | validate_input | success->TAX.LOOKUPS;failure->TAX.ISSUES | none | stop | create or update |
