# Label Resolution Outcomes

## Error Situations

| Situation | What Should Happen |
|---|---|
| Create request name already exists | Stop and tell the user that a label with the same name already exists. |
| Supplied LabelCode matches an existing environmental label but supplied LabelName differs and update intent is not confirmed | Stop, show the current and supplied label names, and ask whether the user intends to update the label name. Do not treat the mismatch as a create or silently rename the label. |
| User declines the proposed label-name update for a supplied existing LabelCode | Stop and request corrected input. Do not create a new label or change the existing label. |
| Update request existing label name has no exact match | Stop and report that the existing label name was not found. |
| Update request existing label name has multiple exact matches | Stop and report that the existing label name is ambiguous. |
| Update request new label name exactly matches a label with a different LabelCode | Stop and tell the user that the requested new label name already exists. |
| More than one Fusion language is enabled and translations are omitted without an explicit decline | Ask the user whether to provide translations for the enabled languages. Stop pending that choice. |
| Supplied translation language is not enabled | Stop and inform the user that the supplied translation language is not enabled. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LABELS.LABEL_NAME_UPDATE_CONFIRMATION_REQUIRED | terminal | 140 | terminal | none | LABELS.SELECT_REQUEST_ACTION | continue | A supplied LabelCode matches an existing environmental label, the supplied LabelName differs from the current LabelName, and explicit update confirmation is absent |
| LABELS.LABEL_IDENTITY_CORRECTION_REQUIRED | terminal | 150 | terminal | none | LABELS.SELECT_REQUEST_ACTION | continue | The user explicitly declines to update the current LabelName associated with the supplied existing LabelCode |
| LABELS.DUPLICATE_LABEL | terminal | 160 | terminal | none | LABELS.CHECK_CREATE_DUPLICATE | continue | Create request name exactly matches an existing LabelName |
| LABELS.LABEL_NOT_FOUND | terminal | 170 | terminal | none | LABELS.MATCH_EXISTING_LABEL | continue | Update request existing label name has no exact existing LabelName match |
| LABELS.LABEL_AMBIGUOUS | terminal | 180 | terminal | none | LABELS.MATCH_EXISTING_LABEL | continue | Update request existing label name has multiple exact existing LabelName matches |
| LABELS.UPDATE_TARGET_LABEL_EXISTS | terminal | 185 | terminal | none | LABELS.CHECK_UPDATE_TARGET_COLLISION | continue | Update request new label name has a case-sensitive exact existing LabelName match with a different LabelCode |
| LABELS.TRANSLATION_LANGUAGE_NOT_ENABLED | terminal | 190 | terminal | none | none | continue | A supplied translation language is not enabled |
| LABELS.TRANSLATION_INPUT_PENDING | terminal | 195 | terminal | none | LABELS.CHECK_TRANSLATION_INPUT | continue | More than one Fusion language is enabled, translations are omitted, and the user has not explicitly declined to provide translations |
| LABELS.CREATE_INTENT_INTERPRETED | terminal | 200 | terminal | none | LABELS.PREPARE_CREATE_TRANSLATIONS | continue | Create request values, defaults, LabelCode, and translations are interpreted and prepared |
| LABELS.UPDATE_INTENT_INTERPRETED | terminal | 210 | terminal | none | LABELS.PREPARE_UPDATE_TRANSLATIONS | continue | Update request values, resolved LabelCode, and translations are interpreted and prepared |
