# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create label request | A new label name as a non-empty string | Reject the request | Provide a new label name as a non-empty string | Create a label | |
| Update label request | An existing label name and a new label name, each as a non-empty string | Reject the request | Provide both label names as non-empty strings | Update a label | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current Manage Recruiting Labels FSM data is available | Apply the create duplicate, update source-label unique-match, and update-target collision outcomes from the label lookup. | Follow the declared create or update decision path. | export_current_recruiting_labels |
| A supplied LabelCode matches an existing environmental label but the supplied LabelName differs from that label's current LabelName | Show the current and supplied label names and ask whether the user intends to update the label name. Proceed as an update with the existing LabelCode only after explicit confirmation; if the user does not confirm, stop and request corrected input. | Preserve the mismatch as a pending decision. Never interpret it as a create or silently rename the label. | export_current_recruiting_labels |
| Site base-language and enabled-language codes are available | Each supplied translation language must resolve to an enabled Fusion language code. | Stop and inform the user when a supplied translation language is not enabled. | resolve_site_language_configuration |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Label name presence and type | Reject a supplied label name when it is missing, null, non-string, or an empty string. Do not apply trimming, normalization, length, or character-set rules. | Every create or update label request | |
| EntityType create behavior | When EntityType is omitted, allow the default CANDIDATE. When EntityType is supplied as the exact case-sensitive value CANDIDATE, accept it without replacement. For any other supplied value, including blank text, alternate casing, surrounding whitespace, aliases, or another entity type, inform the user that EntityType must be CANDIDATE and ask whether to proceed with CANDIDATE. Reject a create request that supplies EntityType until the value is exact CANDIDATE or the user explicitly confirms proceeding with CANDIDATE; never replace the supplied value without that confirmation. | Create a label request | |
| Existing LabelCode paired with a different LabelName | When a supplied LabelCode exactly matches one exported environmental label but its supplied LabelName differs case-sensitively from the exported LabelName, show both names and ask whether the intended action is to update the label name. Continue as an update using the existing LabelCode only after explicit confirmation. If confirmation is absent, stop pending the decision; if the user declines, stop and request corrected input. Never treat the mismatched pair as a create or silently replace either name. | Every request that supplies both LabelCode and LabelName | export_current_recruiting_labels |
| Supported request intent | Accept only create a label or update a label requests. | Every request | |
| Translation input decision | When more than one Fusion language is enabled and translations are omitted, ask the user whether to provide translations. Do not infer a decline from omission, silence, or an incomplete response. | Create or update request with translations omitted | resolve_site_language_configuration |
| Translation language eligibility | Stop and inform the user when a supplied translation language is not enabled. | User provides translations | resolve_site_language_configuration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LABELS.VALIDATE_LABEL_INPUTS | decision | 10 | validate_input | valid->LABELS.ENSURE_CURRENT_LABEL_EXPORT | none | stop | Every create or update label request |
| LABELS.SELECT_REQUEST_ACTION | decision | 60 | evaluate_result | create->LABELS.CHECK_CREATE_DUPLICATE;update->LABELS.MATCH_EXISTING_LABEL;label-name-update-confirmed->LABELS.MATCH_EXISTING_LABEL;label-name-update-confirmation-required->LABELS.LABEL_NAME_UPDATE_CONFIRMATION_REQUIRED;label-name-update-declined->LABELS.LABEL_IDENTITY_CORRECTION_REQUIRED | LABELS.RESOLVE_SITE_LANGUAGE_CONFIGURATION | stop | Current FSM label and language evidence is available, including any supplied LabelCode and LabelName reconciliation outcome |
| LABELS.CHECK_CREATE_DUPLICATE | decision | 70 | evaluate_result | absent->LABELS.CHECK_TRANSLATION_INPUT;exists->LABELS.DUPLICATE_LABEL | LABELS.SELECT_REQUEST_ACTION | stop | Create a label request |
| LABELS.MATCH_EXISTING_LABEL | decision | 80 | evaluate_result | unique->LABELS.CHECK_UPDATE_TARGET_COLLISION;missing->LABELS.LABEL_NOT_FOUND;multiple->LABELS.LABEL_AMBIGUOUS | LABELS.SELECT_REQUEST_ACTION | stop | Update a label request |
| LABELS.CHECK_UPDATE_TARGET_COLLISION | decision | 85 | evaluate_result | absent->LABELS.CHECK_TRANSLATION_INPUT;same-source->LABELS.CHECK_TRANSLATION_INPUT;exists->LABELS.UPDATE_TARGET_LABEL_EXISTS | LABELS.MATCH_EXISTING_LABEL | stop | Update a label request after the source label resolves uniquely |
| LABELS.CHECK_TRANSLATION_INPUT | decision | 88 | evaluate_result | single-language-create->LABELS.VALIDATE_CREATE_TRANSLATIONS;single-language-update->LABELS.VALIDATE_UPDATE_TRANSLATIONS;translations-provided-create->LABELS.VALIDATE_CREATE_TRANSLATIONS;translations-provided-update->LABELS.VALIDATE_UPDATE_TRANSLATIONS;translations-declined-create->LABELS.VALIDATE_CREATE_TRANSLATIONS;translations-declined-update->LABELS.VALIDATE_UPDATE_TRANSLATIONS;translation-choice-pending->LABELS.TRANSLATION_INPUT_PENDING | none | stop | Create or update request after identity validation and site language resolution |
| LABELS.VALIDATE_CREATE_TRANSLATIONS | decision | 90 | evaluate_result | valid->LABELS.GENERATE_LABEL_CODE;language-not-enabled->LABELS.TRANSLATION_LANGUAGE_NOT_ENABLED | LABELS.CHECK_TRANSLATION_INPUT | stop | Create a label request |
| LABELS.VALIDATE_UPDATE_TRANSLATIONS | decision | 110 | evaluate_result | valid->LABELS.PREPARE_UPDATE_TRANSLATIONS;language-not-enabled->LABELS.TRANSLATION_LANGUAGE_NOT_ENABLED | LABELS.CHECK_TRANSLATION_INPUT | stop | Update a label request |
