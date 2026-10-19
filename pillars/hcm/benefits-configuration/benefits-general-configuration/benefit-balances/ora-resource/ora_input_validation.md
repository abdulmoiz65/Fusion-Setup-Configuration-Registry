# Benefit Balances Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, Update, Correction, End date, Delete changes, ZAP, or Read/verify | Block before preflight | Supply one supported operation and its explicit effective-date or deletion scope when applicable | Every request | |
| HDL artifact | A nonempty immutable benefitBalances DAT that passed core.data-loader preflight | Block the mutation | Generate a current sample and validate the artifact | Create or merge, Update, or Delete | |
| Target context | Exact target environment and active Run Book context | Block the mutation | Select the target and activate the routed project Run Book | Create or merge, Update, or Delete | |
| Record prerequisites | Balance name, legal employer, source identity, and every other fact required by the current sample | Block the affected record | Correct the source row from authoritative implementation data | Create or merge, Update, or Delete | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A request changes benefit balance data | Continue only after every record has a validated artifact, target context, and active Run Book | Continue to dependency readiness | |
| An identity or prerequisite has more than one candidate | Block the affected record | Provide an exact identifier; do not choose a candidate | |
| A supplied reference field has an authorized LOV lookup | Validate that field for its own benefitBalances row using ora_reference_lookups.md | Record valid, invalid, ambiguous, or unverified_forbidden per field and row | |
| A supplied reference field's LOV returns 403 | Do not fail field validation or mark the value invalid; record unverified_forbidden | Continue independent checks; retain the unverified status for load readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business object | Reject any object other than benefitBalances | Every request | |
| DAT schema | Reject a header, component, action, or attribute not accepted by the current Data Loader sample | Create or merge, Update, or Delete | |
| Per-section effective contract | Confirm date-effectivity, effectiveOf availability, and requested operation separately for every included section from the current sample; reject missing or ambiguous metadata and effectiveOf on any section that does not expose it | Every included DAT section | |
| Date-effective controls | When the current sample marks an included benefitBalances section date-effective and exposes effectiveOf, require the derived value for the exact row operation; parse each required date using its documented source format and require every date component in effectiveOf to be valid YYYY-MM-DD; reject caller-authored, missing, mismatched, invalid, or ambiguous values | Create, Update, Correction, End date, Delete changes, or ZAP | |
| EffectiveEndDate default | After section metadata confirms the field, preserve a supplied valid EffectiveEndDate; for Create, Update, or Correction default an omitted value to the end-of-time date 4712/12/31 and serialize it in the section's required DAT format. Require an explicit EffectiveEndDate for End date; do not default Delete changes or ZAP | A date-effective benefitBalances row is prepared | |
| Record identity | Require current-schema source identity and user keys where the selected operation requires them; do not infer missing values | Create or merge, Update, or Delete | |
| Required prerequisites | Require the balance name, legal employer, source identity, and all other facts when the current sample requires them | Create or merge, Update, or Delete | |
| Conditional reference values | Match each supplied BalanceUsageMeaning, NonMonetaryUnitsMeaning, LegalEmployerName, and CurrencyName through its declared read-only REST resolver; do not infer, translate, or overwrite the supplied value | Any included benefitBalances row that supplies one of these fields | |
| Artifact integrity | Reject an empty, malformed, changed, or unvalidated DAT | Create or merge, Update, or Delete | |
| CSV route | Reject FSM CSV export/import as a substitute route | Every request proposing CSV | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.VALIDATE_REQUEST | decision | 10 | validate_input | valid->BEN_BAL.CHECK_READINESS;invalid->BEN_BAL.HANDLE_ISSUE | none | stop | Validate operation, object, artifact, target context, record prerequisites, per-section date-effectivity and effectiveOf availability, and unsupported CSV routing |
