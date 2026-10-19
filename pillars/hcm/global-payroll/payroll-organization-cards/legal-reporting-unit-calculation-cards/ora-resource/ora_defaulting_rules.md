# Legal Reporting Unit Calculation Cards Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| Operation | Review only | User asks to inspect cards without requesting a business change | No |
| Effective date | No default | Read-only lookup or HDL create, update, end-date, delete, or LOV resolution requires an effective date | No |
| Tax reporting unit | No default | Every card-specific request | No |
| Calculation card | No default | A specific card operation is requested | No |
| Source type | TRU | Legal Reporting Unit Calculation Cards read-only calculationEntries retrieval | Yes when absent; block if a conflicting value is supplied |
| Legal reporting availability limit | `500` | `findByAdvancedSearchQuery` request omits limit | Yes when absent |
| Legal reporting availability offset | `0` | First `findByAdvancedSearchQuery` request | Yes when absent |
| Legal reporting display fields | Name, RegistrationCodeEtb, RegistrationNumber, IdentifyingFlag, ParentLegalEntity, ParentLeLempFlag, ParentLePsuFlag, ReStatus, TruStatus, EffectiveFrom, EffectiveTo, EstablishmentId | Legal reporting availability is requested | Yes when absent; do not remove fields required by the response contract |
| Legal reporting search fields | Name, RegistrationNumber | Legal reporting availability is requested | Yes when absent |
| LDG availability limit | `500` | Direct LDG advanced search omits limit | Yes when absent |
| LDG availability offset | `0` | First direct LDG advanced-search request | Yes when absent |
| LDG display fields | Name, CurrencyName, TerritoryShortName, CostAllocationStructureName, LegislativeDataGroupId | Direct LDG availability is requested | Yes when absent; do not remove fields required by the response contract |
| LDG search fields | Name | Direct LDG availability is requested | Yes when absent |
| LDG filters | Name mode: empty array; US territory mode: `TerritoryShortName=United States` | Direct LDG availability is requested | Select by intent; never remove the territory filter from “all US LDGs” |
| Global page flag | true | getCardDetails add or drilldown request uses Redwood calculationEntries payload | Yes when absent |
| Association rows | No default | Add association or end-date association is requested | No |
| HDL create/update/correction classification | No verb-based default | Every business change | No; derive per object from complete existence/history state and require user confirmation when data exists |
| HDL date-effective action | No default | Existing data requires Update, Correction, End Date, Delete Record, or Delete History | No; notify the user and require target-template action evidence plus the applicable confirmation |
| Card component values | No default | Edit details are supplied | No |
| Override field list | No default | Every card or component is selected | No |
| Override value | No default | Any override value is supplied or omitted | No |
| HDL CalculationCard.CardSequence | `1` | Complete current/future/history discovery proves the card business key is absent and the user omits CardSequence | No; never apply to an existing card |
| HDL CardComponent.ComponentSequence | `1` | Complete object-level discovery proves the component business key is absent and the user omits ComponentSequence | No; never apply to an existing component |
| HDL EffectiveStartDate | Runtime system date resolved at DAT preview | A new CalculationCard, CardComponent, or ComponentDetail row is created and the user omits its start date | No; apply only when absent and emit as `YYYY/MM/DD` |
| HDL EffectiveEndDate | `4712/12/31` | A new CalculationCard, CardComponent, or ComponentDetail row is created and the user omits its end date | No; apply only when absent |

## Operation Defaults

| Operation | Default Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|---|
| Card summary | expand | Cards | Request body includes dirCardId and effectiveDate only | Yes when absent |
| Legal reporting availability | query | Trimmed user search text | User supplies a name or registration-number fragment | Yes when absent; preserve explicit user wildcards |
| Legislative Data Group availability | query | Trimmed user search text | User supplies a full or partial LDG name | Yes when absent; preserve the text exactly and do not add wildcards |
| Legislative Data Group availability | query | Empty string | User requests all US LDGs and the nonblank `TerritoryShortName=United States` filter is present | Yes when absent; never use an empty query without a restrictive filter |
| Card drilldown | mode | G | Existing card details are requested | Yes when absent |
| Card drilldown | expand | Cards,Components,Overrides,CompAssociation | Existing card component and override details are requested | Yes when absent |
| Card drilldown | showEmptyComponent | N | Existing card component and override details are requested | Yes when absent |
| Add-card template | mode | ADD | Add-card preview is requested before card creation | Yes when absent |
| Add-card template | expand | Cards,Components,Overrides,Associations | Add-card preview is requested before card creation | Yes when absent |
| Create-card list | mode | ADD | Available cards for create are requested | Yes when absent |
| Create-card list | expand | Cards | Available cards for create are requested | Yes when absent |

## Defaulting Notes

| Situation | What Happens |
|---|---|
| Source does not explicitly define a default | Preserve TBD or require user input |
| User supplies a value | Do not override it unless an approved source defines a mandatory replacement |
| User changes one override in the same context | Merge the changed value over the auto-carried value by name and context |
| Runtime derives a display value from lookup | Record the derived value as lookup output, not as a default |
| Parity source shows a context placeholder such as -1 or null | Treat it as read-only UI evidence only; never copy it to HDL unless the live target template and component guidance require the same stored value |
| Creating a new card | Never default or emit dirCardId; HDL links the parent by target-supported user keys |
| Functional request omits technical identifiers | Resolve `dirCardId`, component/definition IDs, override-group IDs, source/LDG IDs, and assignment/association IDs automatically from read-only business-name lookups; do not ask the user for them |
| Complete existence lookup finds no exact leaf business key | Classify that leaf as create and apply only its applicable creation defaults; reuse every existing ancestor |
| Any matching current, future, or historical business key exists | Do not default create or update. Show the business interval/value, recommend Update or Correction from the effective-date matrix, and wait for confirmation |
| Override value is nullable | Preserve an explicit null only when the override metadata says nullable=true |
| Card exposes different overrides than another card | Use the active card's getCardDetails metadata and ignore non-returned fields |
| Dependent LOV parent changes | Clear or revalidate dependent child values before preview |
| LOV has no unique default from metadata | Do not auto-select a value |
| Component Delete Record or Delete History is requested | Do not default an action; require the current target HDL template to prove the delete contract |
| Add association is requested | Do not default association identity or fields; require live target HDL support |
| End-date association is requested | Do not default association identity or action; require live target HDL support |
| HDL card or component creation supplies an explicit sequence or date | Preserve the user value; do not replace it with the HDL creation default |
| HDL component is added to an existing card | Propagate the existing card's resolved CardSequence to CardComponent and ComponentDetail; the new-card CardSequence default does not replace an existing parent key |
| HDL existing component or child value is selected | Preserve returned dates/sequences internally; notify the user and wait for Update or Correction confirmation rather than auto-updating or duplicating it |
| HDL component sequence is omitted | Default ComponentSequence to 1 and propagate it to CardComponent and every related ComponentDetail row; block if sequence 1 conflicts with an existing component |
| HDL start date is omitted | Resolve the runtime system date once when generating the exact DAT preview, format it as `YYYY/MM/DD`, and never write the literal text `SYSDATE` |
| HDL end date is omitted | Use `4712/12/31`; block and request a valid date if it falls outside the parent card interval |
| Approved DAT is created, packaged, uploaded, or loaded | Reuse the concrete date shown in the approved preview; do not recompute the system date during a later stage |
