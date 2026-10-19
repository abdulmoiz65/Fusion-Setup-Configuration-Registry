# Revision Preferences for Sales Orders Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Revision preference request | One or more returned attribute names, each with one preference | Stop before source preparation | Provide the attribute name and Required or Not Required | Any Revision Preferences change request | discover_revision_preference_attributes |
| Redwood feature prerequisite | Successful feature lookup or requester attestation that the feature is enabled | Stop before source preparation | Record the lookup result or requester attestation with its source and timestamp | Any Revision Preferences change request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Attribute name eligibility | Accept only an exact attribute name returned by the current discovery response. Do not accept a code, inferred label, or hardcoded value. | Any requested preference | discover_revision_preference_attributes |
| SunInventoryCode alias | Normalize SunInventoryCode to the returned attribute name Subinventory before eligibility validation. Stop when Subinventory is absent. | The alias is supplied | discover_revision_preference_attributes |
| Preference value | Normalize an unambiguous localized equivalent to Required or Not Required. Reject a third state, boolean literal, Y, N, or ambiguous translation. | Any requested preference | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVISION_PREFERENCES.VALIDATE_INPUT | step | 10 | validate_input | valid->REVISION_PREFERENCES.DISCOVER_ATTRIBUTES;invalid->RETURN_ISSUES | none | stop | Before preparing a Revision Preferences change preview. |
