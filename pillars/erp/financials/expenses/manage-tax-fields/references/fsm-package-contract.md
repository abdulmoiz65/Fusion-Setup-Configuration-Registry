# FSM package contract

Use a fresh same-task export and template through the routed export workflow. Preserve metadata, column order and package membership. This document describes observed structure; it is not a payload generator.

## EXM_CASH_ADV_SETUP_AND_POLICY.csv

```csv
BuName,OptionCode,ValueCode,CreationDate,CreatedBy,LastUpdateLogin,LastUpdateDate,LastUpdatedBy,OtherOrgId
```

## EXM_SETUP_OPTION.csv

```csv
BuName,OptionCode,ValueCode,CreationDate,CreatedBy,LastUpdateLogin,LastUpdateDate,LastUpdatedBy,OtherOrgId
```

## EXM_VAT_FIELD.csv

```csv
BuName,TerritoryCode,EnableMerchantNameCode,EnableMerchantReceiptCode,EnableMerchantTaxRegCode,EnableMerchantReferenceCode,EnableMerchantTaxpayerCode,EnableTaxClassificationCode,EnabledFlag,CreationDate,CreatedBy,LastUpdateDate,LastUpdatedBy,LastUpdateLogin
```

## ASM_SETUP_CSV_METADATA.xml

## Ownership and identity

- EXM_VAT_FIELD is the tax-rule target. The source entity alternate key is OrgId plus TerritoryCode; the FSM service resolves BuName in the current enterprise context before updating primary keys. Do not carry database IDs across environments.
- EXM_SETUP_OPTION contains the business-unit ENABLE_TAX switch. This task changes only ENABLE_TAX for explicitly selected business units. Other option codes are outside this task.
- EXM_CASH_ADV_SETUP_AND_POLICY is an observed package member sharing the setup-option service, XML file and node path. Its bytes match EXM_SETUP_OPTION.csv in both collected exports (FSM-DUPLICATE-CHECK); recheck rather than assuming that for future packages. Use the user-selected single setup-option member policy (DOC-CSV-EMPTY-MEMBER): retain this member with its exact header and zero data rows. Populate requested ENABLE_TAX rows only in EXM_SETUP_OPTION.csv. Never copy the populated setup-option rows into both members or remove the cash-advance member. This avoids requiring duplicate populated-member merge semantics; verify persisted scope after import.
- Audit columns are exported transport context, not business inputs. Preserve their headers and serialize empty cells for candidate rows under BUILDER-AUDIT-CONTRACT. Never fabricate or copy audit identities/timestamps into candidate rows. Retain original export bytes as baseline evidence. This defines adapter serialization, not proof of target runtime acceptance.
- OtherOrgId has special negative-ID fallback behavior in the shared import hook. Do not use that fallback to turn a business-unit request into global setup. Missing or unresolved BuName is a task issue.

## Field dispositions

| Fields | Meaning | Evidence boundary |
|---|---|---|
| BuName | Business-unit business key | Resolve in target enterprise; name alone across enterprises is insufficient |
| TerritoryCode | Country/territory or OTHER | Territory existence validator exempts literal OTHER; duplicate BU/territory is invalid |
| Six Enable*Code columns | Field behavior | DISABLED, ENABLED, REQUIRED; enabled EXM_FIELD_BEHAVIOUR lookup validates values |
| EnabledFlag | Tax-rule flag | Literal Y/N validation; not a substitute for the ENABLE_TAX setup option |
| OptionCode | Setup option identity | ENABLE_TAX for this task |
| ValueCode | Task switch | Y/N from task UI application-module logic; generic setup entity allows broader values |
| CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, LastUpdateLogin | Audit context | Import VO marks these non-updateable; candidate cells are empty under BUILDER-AUDIT-CONTRACT; target audit generation remains subject to live reconciliation |
| OtherOrgId | Shared service transport fallback | Not an implementor tax-field control; retain source context pending verified candidate construction |

Create and update are the supported planning operations under this package contract; selected target executions are recorded in the dated [coverage summary](evidence.md#validation-coverage--2026-10-07), without complete E2E certification. Physical delete, implicit rename, blank-as-clear, and omission-as-default semantics are not established. Preserve supplied values and surface these gaps before preview or execution.
