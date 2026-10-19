# Content Type Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Content type identity | Content Type Name and description for every active Knowledge locale, Reference Key, Article ID Prefix, Department | Block the change | Resolve active Knowledge locale codes through Manage Knowledge Locales. Use the exact locale code, such as en_US, and obtain each locale's name and description or customer confirmation that the provided name may be used for every active locale. Provide the remaining identity values before preparing the FSM package. | Create content type | resolve_active_knowledge_locales |
| Content schema title | Title field name and required setting | Block the change | Define the required title field | Create or update content schema | |
| Additional schema attribute | Name, Reference Key, Field Type, Required setting, parent content-type Reference Key | Block the attribute change | Provide the attribute definition and its parent linkage | Adding or updating an attribute | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Attribute field type | Accept only TEXT_AREA, WYSIWYG_EDIT, TEXT_FIELD, FILE, BOOLEAN, LIST, COUNTER, DATE, DATETIME, TIME, INTEGER, or FLOAT | Adding or updating an attribute | |
| Content type localized values | A nonblank Content Type Name and localized description row exist for every active Knowledge locale; localeId is the exact active locale code, such as en_US, not a GUID or display-name inference | Creating or updating a content type | resolve_active_knowledge_locales |
| Schema attribute localized values | Name and description can be supplied for each required locale; localeId is the exact active locale code, such as en_US, not a GUID or display-name inference | Locales are enabled for the content type or attribute | resolve_active_knowledge_locales |
| New schema attribute xpath | Generate xpath from the attribute referenceKey and ORA_CSO_CONTENT_TYPE_OBJECT.referenceKey parent | Adding a schema attribute | |
