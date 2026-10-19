# Benefit Balances Reference Lookups

## Conditional Read-Only Checks

Run a resolver only when its field is supplied in a `benefitBalances` row and
the active project workflow selects read-only reference validation through
`core.fusion-api.rest-api-client`. Use the selected environment and
`REST-Framework-Version: 9`. These checks validate values; they do not change
the supplied value, choose an HDL key, or authorize a load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_balance_usage | `benefitBalances.BalanceUsageMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_BNFTS_BAL_USG` | Require one distinct row with `LookupType=BEN_BNFTS_BAL_USG` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve `BalanceUsageMeaning`. |
| resolve_nonmonetary_units | `benefitBalances.NonMonetaryUnitsMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_NNMNTRY_UOM` | Require one distinct row with `LookupType=BEN_NNMNTRY_UOM` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve `NonMonetaryUnitsMeaning`. |
| resolve_legal_employer | `benefitBalances.LegalEmployerName` | `GET /hcmRestApi/resources/11.13.18.05/legalEmployersLov?q=Name='<LegalEmployerName>'` | Require one distinct row whose `Name` exactly equals the supplied value; use the row's effective start date when the endpoint supports an effective-date parameter. | Validation status only; preserve `LegalEmployerName`. |
| resolve_currency | `benefitBalances.CurrencyName` | `GET /fscmRestApi/resources/11.13.18.05/currenciesLOV?q=Name='<CurrencyName>'` | Require one distinct row whose `Name` exactly equals the supplied value. | Validation status only; preserve `CurrencyName`. |

## Execution and Result Rules

- For `commonLookupsLOV`, send only the declared `LookupTypeFinder` request; do
  not add a `q` predicate. Compare the returned `Meaning` exactly, including
  case, within the requested lookup type.
- For `legalEmployersLov` and `currenciesLOV`, send the supplied name in the
  `q=Name` equality predicate. URL-encode the complete query parameter and
  escape apostrophes using the endpoint's documented query syntax. Compare
  returned `Name` again for exact equality; do not rely on server filtering
  alone. If effective-date filtering is supported, use the exact row's
  `EffectiveStartDate`, never a parent or sibling row's date.
- Follow every response page before deciding whether there are zero, one, or
  multiple distinct matches. Zero means `invalid`; multiple distinct matches
  mean `ambiguous`; one exact match means `valid`. Do not coerce names into
  codes or pick the first returned candidate.
- If a field is omitted, skip its lookup without an error. An HTTP 403 means
  `unverified_forbidden` for that field: do not fail field validation, mark the
  value invalid, or stop other independent checks. It is not proof of a valid
  value. Require another workflow-approved authoritative verification before
  live load.
- An HTTP 401 may use the selected client's permitted one-time cached-token
  refresh. Classify a remaining denial as auth/authz. Classify other request
  failures separately; do not turn them into a no-match result. If no active
  read-only route exists, record a workflow blocker and do not call REST
  directly or silently mark a value valid.

Oracle REST contracts: [common lookups](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html), [legal employers](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-legalemployerslov-get.html), and [currencies](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-currencieslov-get.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.LOOKUP_USAGE | decision | 21 | reference_lookup | matched->BEN_BAL.LOOKUP_UNITS;skipped->BEN_BAL.LOOKUP_UNITS;forbidden->BEN_BAL.LOOKUP_UNITS;invalid->BEN_BAL.HANDLE_ISSUE | BEN_BAL.CHECK_READINESS | continue | Validate supplied BalanceUsageMeaning through BEN_BNFTS_BAL_USG; 403 records unverified_forbidden |
| BEN_BAL.LOOKUP_UNITS | decision | 22 | reference_lookup | matched->BEN_BAL.LOOKUP_LEGAL_EMPLOYER;skipped->BEN_BAL.LOOKUP_LEGAL_EMPLOYER;forbidden->BEN_BAL.LOOKUP_LEGAL_EMPLOYER;invalid->BEN_BAL.HANDLE_ISSUE | BEN_BAL.LOOKUP_USAGE | continue | Validate supplied NonMonetaryUnitsMeaning through BEN_NNMNTRY_UOM; 403 records unverified_forbidden |
| BEN_BAL.LOOKUP_LEGAL_EMPLOYER | decision | 23 | reference_lookup | matched->BEN_BAL.LOOKUP_CURRENCY;skipped->BEN_BAL.LOOKUP_CURRENCY;forbidden->BEN_BAL.LOOKUP_CURRENCY;invalid->BEN_BAL.HANDLE_ISSUE | BEN_BAL.LOOKUP_UNITS | continue | Validate supplied LegalEmployerName against legalEmployersLov Name; 403 records unverified_forbidden |
| BEN_BAL.LOOKUP_CURRENCY | decision | 24 | reference_lookup | matched->BEN_BAL.DERIVE_EFFECTIVE_OF;skipped->BEN_BAL.DERIVE_EFFECTIVE_OF;forbidden->BEN_BAL.DERIVE_EFFECTIVE_OF;invalid->BEN_BAL.HANDLE_ISSUE | BEN_BAL.LOOKUP_LEGAL_EMPLOYER | continue | Validate supplied CurrencyName against currenciesLOV Name; 403 records unverified_forbidden |
