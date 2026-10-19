# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EntityType | CANDIDATE | Every create label request when EntityType is omitted, or when the user explicitly confirms replacing a different supplied value with CANDIDATE after validation explains the supported value | Conditional; retain an explicitly supplied exact case-sensitive CANDIDATE. Replace any other supplied value only after explicit user confirmation to proceed with CANDIDATE. | |
| LabelCode | A newly generated uppercase 32-character hexadecimal UUID-style value that does not match an existing LabelCode | Create a label after the current FSM export confirms the new label name is absent | No | export_current_recruiting_labels |
| ORA_IRC_LABEL.LabelCode | The resolved label LabelCode | Every translation row | No | export_current_recruiting_labels |
| SourceLang | Retrieved site base-language code | Every translation row | No | resolve_site_language_configuration |
| Language | Each retrieved enabled Fusion language code | One translation row for every enabled Fusion language code | No | resolve_site_language_configuration |
| LabelName | Input label name | The enabled-language set contains only the site base language, the user explicitly declines to provide translations, or a translation is not supplied for an enabled language after the user provides at least one translation | Yes; use the supplied translated label name for its enabled language | resolve_site_language_configuration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LABELS.GENERATE_LABEL_CODE | step | 100 | apply_default | generated->LABELS.PREPARE_CREATE_TRANSLATIONS | LABELS.VALIDATE_CREATE_TRANSLATIONS | stop | Create a label request after the new label name is confirmed absent |
| LABELS.PREPARE_CREATE_TRANSLATIONS | step | 120 | apply_default | prepared->LABELS.CREATE_INTENT_INTERPRETED | LABELS.GENERATE_LABEL_CODE | stop | Create a label request after LabelCode is generated |
| LABELS.PREPARE_UPDATE_TRANSLATIONS | step | 130 | apply_default | prepared->LABELS.UPDATE_INTENT_INTERPRETED | LABELS.VALIDATE_UPDATE_TRANSLATIONS | stop | Update a label request after LabelCode is resolved |
