# Reference Lookups

## Contents

- Lookup Operations
- Country Matching Rules
- Documented Country Values
- Lookup Execution Rules

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| core_ess_submitter | Submitting or tracking an ESS request | jobDefinitionId or requestId | core/fusion-api/ess-job-submitter | execution_result, diagnostics, audit_summary | Use the exact new-request or tracking mode | requestId, terminal, success, status, ECID | Stop and classify the core result; do not submit through another route |
| country_code_reference | country name, alias, or code is supplied | Current Oracle country reference represented below | https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/list-of-available-countries-with-loqate-geography-reference-data.html | Country Name, Country Code | Apply the deterministic matching rules below and require exactly one result | country_name, country_code, correction_disclosed | Ask the user to select from close documented candidates when no unique high-confidence result exists |

## Country Matching Rules

1. Trim input, compare case-insensitively, collapse repeated whitespace, and
   ignore punctuation that does not distinguish documented names.
2. Accept an exact two-letter code or exact canonical country name first.
3. Accept these unambiguous aliases: `UK` and `United Kingdom` as
   `Great Britain (GB)`; `USA`, `US`, and `United States of America` as
   `United States (US)`; and `UAE` as `United Arab Emirates (AE)`.
4. For a remaining input of at least five letters, allow a common spelling
   correction only when exactly one canonical country name has the smallest
   case-insensitive Damerau-Levenshtein distance of at most 2 and every other
   candidate is at least 2 edits farther away. This permits a unique adjacent
   transposition such as `austraila` to `Australia`.
5. Disclose every alias or spelling correction in the informational execution
   summary, for example `Resolved austraila as Australia (AU)`. Do not ask for
   confirmation when the match satisfies these rules.
6. If there is no match, more than one equally close match, or insufficient
   separation from the next candidate, stop and ask the user to choose from the
   closest documented values. Never let model memory alone invent a code.

## Documented Country Values

| Country Name | Country Code |
|---|---|
| Andorra | AD |
| Angola | AO |
| Argentina | AR |
| Australia | AU |
| Austria | AT |
| Belgium | BE |
| Bolivia | BO |
| Bosnia and Herzegovina | BA |
| Brazil | BR |
| Bulgaria | BG |
| Canada | CA |
| Cayman Islands | KY |
| Chile | CL |
| China | CN |
| Croatia | HR |
| Cuba | CU |
| Cyprus | CY |
| Czech Republic | CZ |
| Denmark | DK |
| Dominican Republic | DO |
| Ecuador | EC |
| Estonia | EE |
| Finland | FI |
| France | FR |
| Germany | DE |
| Great Britain | GB |
| Greece | GR |
| Guadalupe | GP |
| Guam | GU |
| Guernsey | GG |
| Hungary | HU |
| Iceland | IS |
| India | IN |
| Indonesia | ID |
| Ireland | IE |
| Isles of Man | IM |
| Israel | IL |
| Italy | IT |
| Jamaica | JM |
| Japan | JP |
| Jordan | JO |
| Kenya | KE |
| Latvia | LV |
| Liechtenstein | LI |
| Lithuania | LT |
| Luxembourg | LU |
| Malaysia | MY |
| Malta | MT |
| Martinique | MQ |
| Mexico | MX |
| Netherlands | NL |
| New Zealand | NZ |
| Norway | NO |
| Oman | OM |
| Peru | PE |
| Poland | PL |
| Portugal | PT |
| Puerto Rico | PR |
| Qatar | QA |
| Reunion Island | RE |
| Romania | RO |
| Russia | RU |
| San Marino | SM |
| Singapore | SG |
| Slovakia | SK |
| Slovenia | SI |
| South Africa | ZA |
| South Korea | KR |
| Spain | ES |
| Sri Lanka | LK |
| Swaziland | SZ |
| Sweden | SE |
| Switzerland | CH |
| Taiwan | TW |
| Thailand | TH |
| Tunisia | TN |
| Turkey | TR |
| United Arab Emirates | AE |
| United States | US |
| Uruguay | UY |
| Vatican City | VA |
| Vietnam | VN |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| No country name, alias, or code is supplied | Do not run a country lookup; use parameterless mode unless another optional filter was supplied |
| An exact documented country code is supplied | Normalize it to uppercase and retain its canonical country name in the preview |
| An exact documented country name or alias is supplied | Resolve its uppercase two-letter code and disclose alias normalization when applicable |
| `austraila` is supplied | Resolve uniquely to `Australia (AU)`, disclose the spelling correction, and pass `AU` to ESS |
| A country input is unknown or ambiguous | Stop before submission and ask the user to choose from close documented candidates |
| A new ESS submission returns a request identifier | Persist and use that requestId for all subsequent tracking |
| Tracking returns a nonterminal status | Retain the requestId and allow resume without resubmission |
| A cached OAuth token receives 401 or 403 | Allow the shared core skill's one refresh attempt; stop if access is rejected again |
