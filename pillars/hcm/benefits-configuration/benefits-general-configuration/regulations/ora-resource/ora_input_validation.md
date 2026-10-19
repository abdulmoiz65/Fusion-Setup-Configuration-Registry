# Benefit Regulations Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Requested operation | Create, Update, Correction, End date, Delete changes, ZAP, or Read/verify | Block before artifact preparation | Supply one supported operation | Every request | |
| HDL object route | `benefitRegulations` | Block before preflight | Use the task-mapped object only | Every request | |
| Current HDL sample | Current `benefitRegulations` Data Loader sample | Block artifact preparation | Retrieve the current sample through `core.data-loader` | Any mutation | |
| Date-effective context | Explicit operation-specific ISO date, or explicit ZAP intent | Block | Provide the required date or destructive intent | Any mutation | |
| Record identity | Exact user key or identifier accepted by the current sample | Block | Resolve the identity; do not infer a candidate | Non-create operation | |
| Immutable load artifact | Preflighted DAT or ZIP derived from the current sample | Block upload or initiation | Rebuild and preflight the artifact | Any mutation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| Date format | Reject blank, malformed, time-bearing, or timezone-bearing range dates; accept only `YYYY-MM-DD` | Any supplied effective date | |
| EffectiveEndDate default | After section metadata confirms the field, preserve a supplied valid ISO EffectiveEndDate; for Create, Update, or Correction emit 4712-12-31 when it is omitted. Require an explicit EffectiveEndDate for End date; do not apply the default to Delete changes or ZAP | A date-effective benefitRegulations row is prepared | |
| Per-section effective contract | Confirm date-effectivity, effectiveOf availability, and supported operation separately for every included section from the current sample; reject missing or ambiguous metadata and effectiveOf on a section that does not expose it | Every included DAT section | |
| Effective context | Derive `effectiveOf` from the operation; require every date component in the final value to be valid `YYYY-MM-DD`; reject free-form or mismatched values | Any date-effective row | |
| Create default | Permit the target current date only after explicit confirmation when create start date is omitted | Create | |
| Existing slice | Require an exact existing identity and applicable slice date before Update, Correction, End date, or Delete changes | Non-create, non-ZAP | |
| ZAP | Require explicit destructive intent and current-sample support | ZAP | |
| DAT contract | Reject a filename, section, header, relationship, key, action, or attribute not accepted by the current sample | Any mutation | |
| Final artifact | Inspect the final immutable DAT member; require derived `effectiveOf` on every row whose section exposes it and verify it is absent from every section that does not expose it | Before preflight or approval | |
| CSV route | Reject CSV as a substitute route because catalog support is `N` | Every request proposing CSV | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BEN_REG.VALIDATE_REQUEST | decision | 10 | validate_input | valid->BEN_REG.APPLY_DEFAULTS;invalid->BEN_REG.HANDLE_ISSUE | none | stop | Validate the operation, object, current per-section date-effectivity and effectiveOf contract, identity, date context, and immutable artifact |
