# Remit-to Reference Lookups

Evaluate the validated exact-task FSM export locally. Acquire exports and perform
imports only through the shared FSM route. No SOAP, direct entity API or database
lookup is permitted. A current export proves its rows, not all shared locations,
reference sets, country/state choices or deployed flexfields. Unresolved checks
remain explicit business questions or evidence gaps, never invented defaults.

## Local Lookups

| Resolver | Runs When | Source Values | Local Evidence Source | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_remit_set | Every location and child scope | User-selected SetCode or unambiguous set label | Validated FSM current export; import SetIdSetPVO SetIdSetCodeKey mechanism | SetCode, SetName and exported scope | Exact exported set is positive existence evidence only; export access does not prove import authorization | AR_REMIT_TO_LOCATION.SetCode; AR_REMIT_TO_ADDRESS.SetCode; preserve SetName as display evidence only | Ask precise set; no exported match means unproven, not nonexistent; do not create a prerequisite set |
| validate_postal_destination | New or matched postal location | Country and postal destination, including external reference if provided | Validated FSM current export plus scripts/remit_identity.py import-match inspection | Seven parent references; six service match inputs; copied-only-on-create postal fields | Preserve nullable components; detect known first-match and ignored-value hazards; exported cardinality is not global HZ cardinality | Reviewed parent-reference tuple only; never manufacture a database ID or OrigSystemReference | Ask for missing address values or known match conflicts; normal application-owned checks remain pending_import, not prevalidated (../references/postal-validation-contract.md) |
| resolve_criteria_country | Receipt-from country supplied | Country code or business label | Validated FSM child rows plus reviewed CountryVVO source | Receipt-from Country and special REMIT choices | Exact exported code is observed evidence only, not a complete current domain or label resolver | AR_REMIT_TO_ADDRESS.Country | Ask exact coverage; do not equate receipt-from DEFAULT with a postal destination country |
| resolve_criteria_state | State-restricted receipt-from coverage | Selected criteria Country and State | Validated FSM child rows plus reviewed StateVVO source | Country-bound State | An observed Country/State pair does not prove all valid states; blank restriction is intentional coverage, not a missing identifier | AR_REMIT_TO_ADDRESS.State | Ask one coverage question; never silently broaden to the whole country |
| resolve_criteria_status | Criteria state requested or defaulted | Requested business state | Reviewed UI create default, CODE_STATUS seed data, migration criteria VO/EO and current export; references/lifecycle-contract.md | Status and requested operation | Active maps to A; Inactive maps to I for an exact existing criterion only. New criteria use A. The adapter deliberately excludes D even though it is a lookup code | AR_REMIT_TO_ADDRESS.Status | Clarify immediate activation/inactivation versus future end-date or physical deletion; never convert between those intents silently |
| resolve_remit_flexfields | Regional information or DFF requested | Business context/segment labels and values | Task export is insufficient deployment evidence; retain explicit conditional evidence request | Deployed context, physical fields, types, requiredness and accepted values | Not applicable when no flexfield is requested and no mandatory context is evidenced; otherwise require authoritative deployment evidence | Only proven physical context and segment fields | Ask business intent and request the missing deployment evidence; never guess AttributeN mappings |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Missing public GET | Not a prerequisite failure and not permission to use SOAP or direct entity APIs; this node evaluates local FSM evidence |
| Missing export or invalid export | Use the shared exact-task FSM export capability; report authentication, process or package errors separately from an empty data set |
| Export references | scripts/remit_identity.py checks all seven parent reference columns and nullable criteria identity; failed checks prevent further preparation |
| Import matching | RemitToServiceAMImpl searches global locations using six optional inputs and takes one result; SetCode and Address2 are not discriminator predicates in that hook |
| Import reuse | Extra postal fields copied on new location creation are not applied when the hook reuses a location; reject known conflicts locally and verify every requested value after import |
| Source versus target | FPHDEV proves implementation mechanisms, not target customer-created values or installed patch parity |
| Resolver ownership | Local evaluation is read-only; prerequisite/master-data creation remains outside this task |

Sources: SRC-REMIT-AM-IMPL; SRC-REMIT-COUNTRY-LOV; SRC-REMIT-STATE-LOV; SRC-REMIT-UI-STATUS; SRC-REMIT-CDM-CREATE-FLOW; SRC-REMIT-CDM-UPDATE-FLOW. Reviewed public guidance: Oracle 26C Implementing Receivables Credit to Cash, remit-to addresses chapter.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_LOOKUPS | decision | 20 | evaluate_result | resolved->RMT_DEPENDENCIES;issues->RETURN_ISSUES | RMT_VALIDATE | stop | Evaluate applicable FSM evidence and return unresolved business questions |
