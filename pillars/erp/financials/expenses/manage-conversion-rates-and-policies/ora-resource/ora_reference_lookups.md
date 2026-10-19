# Manage Conversion Rates and Policies Reference Lookups

These are required read-only preflights for every candidate row, including
carried parent and sibling rows. They establish destination reference readiness;
they do not predict Oracle's import error text or grant mutation approval.

## Sources

- [Business Units LOV](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-finbusinessunitslov-get.html) (`SRC-ORACLE-26C-REST-BU`).
- [Currency Conversion Types LOV](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-currencyconversiontypeslov-get.html) (`SRC-ORACLE-26C-REST-TYPE`).
- [Preferred Currency](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-preferredcurrencieslov-currencycode-get.html) (`SRC-ORACLE-26C-REST-CURRENCY`).
- `SRC-CODE-EXM-AMIMPL`, `SRC-CODE-BU-PVO`, `SRC-CODE-GL-PVO`, `SRC-CODE-EXM-CURRENCY-LOV`.

Documentation rechecked 2026-10-14. The corresponding 26D REST pages were not
accessible; retain the verified 26C REST contracts. Do not invent newer fields.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches | Evidence |
|---|---|---|---|---|---|---|---|---|
| resolve_business_unit_by_name | Every distinct parent BuName in the candidate | Exact BuName and selected authenticated destination | GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV | BusinessUnitId, BusinessUnitName, ActiveFlag | After complete pagination, require one exact case-sensitive BusinessUnitName with nonblank BusinessUnitId and ActiveFlag=true | Retain verified name and ID as evidence; serialize only BuName; import owns the tenant-aware OrgId mapping | Zero exact matches: reference_not_found; multiple: reference_ambiguous; inactive: reference_inactive; missing fields or incomplete pages: reference_unverified. Stop before preview; correct input/access and rerun preflight, never create a BU implicitly | SRC-CODE-EXM-AMIMPL, SRC-CODE-BU-PVO, SRC-ORACLE-26C-REST-BU |
| resolve_conversion_type_by_name | Every distinct merged parent UserConversionType in the candidate | Exact UserConversionType | GET /fscmRestApi/resources/11.13.18.05/currencyConversionTypesLOV | ConversionTypeId, UserConversionType, Description | After complete pagination, require exactly one case-sensitive UserConversionType with nonblank ConversionTypeId | Retain name and REST identity as evidence; serialize UserConversionType. ConversionTypeId is not proof of the internal ExchangeRateType mapping; the import hook owns it | Zero matches: reference_not_found; multiple: reference_ambiguous; missing identity or incomplete pages: reference_unverified. Stop before preview and correct the destination reference or input | SRC-CODE-EXM-AMIMPL, SRC-CODE-GL-PVO, SRC-ORACLE-26C-REST-TYPE |
| resolve_currency_by_code | Every distinct child CurrencyCode, including carried siblings; skip if no children | Exact CurrencyCode | GET /fscmRestApi/resources/11.13.18.05/preferredCurrenciesLOV/{CurrencyCode} | CurrencyCode, CurrencyFlag, EnabledFlag, StartDateActive, EndDateActive | Require exact code, boolean CurrencyFlag=true and EnabledFlag=true, and active dates covering the run date. Null date bounds are unbounded; absent requested attributes are unverified | Retain CurrencyCode unchanged and the dated readiness evidence separately | HTTP 404 or no item: reference_not_found; disabled/noncurrency/outside active dates: reference_inactive; wrong code, missing fields or ambiguous response: reference_unverified. Stop before preview and correct input/destination setup | SRC-CODE-EXM-CURRENCY-LOV, SRC-ORACLE-26C-REST-CURRENCY |

## Lookup Execution Rules

Use only `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` under
the selected workflow, with core-managed OAuth and REST-Framework-Version: 9.
Do not add direct HTTP, browser, login or alternative write fallbacks.

For collection lookups, retrieve all pages of the chosen result set until
`hasMore=false`; retain offsets and response identities. Do not infer absence
or uniqueness from a truncated first page or estimated totalResults. Apply exact
matching locally. Escape filter values using the client contract, or paginate
without a filter; never interpolate unescaped business input into a query.
For currency item paths encode the exact code as one path segment.

Evaluate core-captured batches with `scripts/validate_references.py` relative
to the task root. Call `validate_references(parents, children, evidence,
environment, candidate_sha256)`, using the complete merged CSV row dictionaries.
Each batch contains `http_status`, `environment`, `candidateSha256`, `captured_at`,
`complete` and `items`. Capture time must have an offset and be within 24 hours;
the workflow must obtain fresh evidence for the run. For paginated collections,
set complete only after the last hasMore=false response. Combine successful
currency item responses into the currencies batch. Failed requests stop before
normalizing a successful batch. Never relabel a failed HTTP response as 200.
The helper validates supplied provenance; the caller owns obtaining it through
core and retains the actual response/request identity. Its result is evidence,
not a Task Hook envelope. Record satisfied entity/field/resolver prerequisites
only for the actual verified BU/type/currency facts. Fixed Y/N flags need no
reference prerequisite.

Bind evidence to the selected environment, task, candidate digest and run.
A transport failure, unavailable path, 401/403, malformed response or missing
attribute is not a missing business reference. Classify auth/authz or
transport/environment separately and stop. Core alone owns bounded auth renewal.
Do not request a reference create or infer any Oracle import error code.

Fixed flags require no lookup: normalize literal Yes/No to Y/N, reject all other
values locally and keep that validation in the input node. An unavailable or
failed lookup never becomes a passed rule or a readiness waiver.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMCR.LOOKUP_BU | step | 3 | reference_lookup | matched->EXMCR.LOOKUP_TYPE;unresolved->EXMCR.BLOCKED | EXMCR.CHECK_DEPENDENCIES | stop | Verify all candidate business units on the exact destination |
| EXMCR.LOOKUP_TYPE | step | 4 | reference_lookup | matched->EXMCR.LOOKUP_CURRENCY;unresolved->EXMCR.BLOCKED | EXMCR.LOOKUP_BU | stop | Verify all merged parent conversion types |
| EXMCR.LOOKUP_CURRENCY | step | 5 | reference_lookup | matched->EXMCR.CHECK_DESIGN;skipped->EXMCR.CHECK_DESIGN;unresolved->EXMCR.BLOCKED | EXMCR.LOOKUP_TYPE | stop | Verify all child currencies; skip only if the candidate contains no children |
