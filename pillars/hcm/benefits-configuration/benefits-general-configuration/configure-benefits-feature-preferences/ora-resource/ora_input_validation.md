# Configure Benefits Feature Preferences Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create preferences or Update preferences | Block before preflight | Supply one supported operation | Every request | |
| HDL object route | Create preferences: initializeBenefitFeaturePreferences; Update preferences: benefitFeaturePreferences | Block before preflight | Select the object mapped to the requested operation | Every request | |
| HDL artifact | The fixed parameterless initializeBenefitFeaturePreferences DAT, or an immutable exact-name benefitFeaturePreferences DAT, that passed core.data-loader preflight | Block the mutation | Use the fixed create DAT or generate and validate the update artifact | Create preferences or Update preferences | |
| Update identity | A complete current-sample user key, or an explicitly supplied PreferenceId when the current sample requires it | Block the mutation | Supply the missing user-key value or PreferenceId | Update preferences | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Create preferences is mapped to initializeBenefitFeaturePreferences | Continue after core.data-loader preflights the fixed parameterless DAT; do not collect preference values or retrieve a sample | Continue to the execution gate | |
| Update preferences is mapped to benefitFeaturePreferences | Continue only after a current-sample preflight validates the immutable exact-name PATCH artifact | Continue to the execution gate | |
| An Update preferences row supplies a named lookup field | Validate each supplied field through its selected read-only LOV | Record valid, invalid, ambiguous, or unverified_forbidden per field and row | |
| A supplied field's LOV returns 403 | Do not fail field validation or mark the value invalid; record unverified_forbidden | Continue independent checks; retain unverified status for load readiness | |
| The operation is not mapped or the object does not match the operation | Block the request | Correct the operation or use its mapped object; do not substitute an object | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation-to-object mapping | Accept initializeBenefitFeaturePreferences only for Create preferences and benefitFeaturePreferences only for Update preferences | Every request | |
| Create load artifact | Reject user-supplied preference values or DAT changes; require the fixed parameterless initializeBenefitFeaturePreferences DAT to pass core.data-loader preflight | Create preferences | |
| DAT filename | Require the case-sensitive filename `benefitFeaturePreferences.dat`; reject suffixes or alternate stems because Data Loader resolves DAT objects from the filename | Update preferences | |
| Update action | Require `RestAction=PATCH`; reject POST, MERGE, DELETE, or a blank action for an update | Update preferences | |
| DAT schema | Reject a header, component, action, or attribute not accepted by the benefitFeaturePreferences current Data Loader sample | Update preferences | |
| User-key identity | When the current sample exposes the FeatureName, FeatureTypeMeaning, and ApplicabilityMeaning user key, permit blank PreferenceId only when every key value is supplied; retain Legislation separately when supplied | Update preferences | |
| Status mapping | Map a supplied status through PreferenceStatusMeaning when available; reject an invented PreferenceStatus code | Update preferences | |
| Feature type meaning | When supplied, require one exact Meaning match from commonLookupsLOV with LookupTypeFinder;LookupType=ORA_BEN_FP_FEATURE_TYPE | Update preferences | |
| Preference status meaning | When supplied, require one exact Meaning match from commonLookupsLOV with LookupTypeFinder;LookupType=ORA_BEN_FP_PREF_STATUS | Update preferences | |
| Applicability meaning | When supplied, require one exact Meaning match from commonLookupsLOV with LookupTypeFinder;LookupType=ORA_BEN_FP_APPLICABILITY | Update preferences | |
| Legislation territory | When supplied, require one exact TerritoryShortName match from territoriesLOV using q=TerritoryShortName | Update preferences | |
| Artifact integrity | Reject an empty, malformed, changed, or unvalidated DAT | Update preferences | |
| Unsupported operation | Reject delete and any operation other than Create preferences or Update preferences | Every request | |
| CSV route | Reject CSV export/import as a substitute route while catalog support is UNKNOWN | Every request proposing CSV | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PREF.VALIDATE_REQUEST | decision | 10 | validate_input | valid->BEN_PREF.LOOKUP_FEATURE_TYPE;invalid->BEN_PREF.HANDLE_ISSUE | none | stop | Validate the requested operation and operation-specific HDL object; require a preflighted immutable artifact for either load while rejecting user-supplied create preference values |
