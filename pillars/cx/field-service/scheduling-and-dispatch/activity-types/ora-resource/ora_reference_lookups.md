# Reference Lookups

Oracle documentation sources:

- https://docs.oracle.com/en/cloud/saas/field-service/cxfsc/api-metadata-languages.html
- https://docs.oracle.com/en/cloud/saas/field-service/cxfsc/op-rest-ofscmetadata-v1-activitytypegroups-get.html
- https://docs.oracle.com/en/cloud/saas/field-service/cxfsc/op-rest-ofscmetadata-v1-activitytypegroups-label-get.html
- https://docs.oracle.com/en/cloud/saas/field-service/cxfsc/op-rest-ofscmetadata-v1-activitytypes-get.html
- https://docs.oracle.com/en/cloud/saas/field-service/cxfsc/op-rest-ofscmetadata-v1-activitytypes-label-get.html

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_active_languages | Before accepting Translation Matrix rows | Target environment | GET /rest/ofscMetadata/v1/languages | Active language codes and labels | Match each Translation Matrix language code to exactly one returned active language | Language Code, Language Label | Stop before preview and report the unmatched or ambiguous language |
| list_activity_type_groups | Selecting a group from target-environment metadata | Target environment | GET /rest/ofscMetadata/v1/activityTypeGroups?limit={limit}&offset={offset} | items.label, items.name, items.translations, totalResults, limit, offset | Page the collection; choose one group only after an exact stable-label match | Group Label and Group Display Name | Stop before preview when no exact label is selected, the page is incomplete, or the result is ambiguous |
| verify_activity_type_group | Before previewing an activity type | Group Label | GET /rest/ofscMetadata/v1/activityTypeGroups/{label} | label, translations, activityTypes | Match exactly one group by the selected stable label | Group Label and current group fields | Stop before preview when the group is absent, ambiguous, or unreadable |
| list_activity_types | Reviewing target-environment Activity Types | Target environment | GET /rest/ofscMetadata/v1/activityTypes?limit={limit}&offset={offset} | items.label, items.name, items.groupLabel, items.active, totalResults, limit, offset | Page the collection; use only an exact Activity Type Label match | Activity Type Label and collection context | Stop before preview when collection paging fails or the matching result is ambiguous |
| find_activity_type_by_label | Before previewing an activity type | Activity Type Label | GET /rest/ofscMetadata/v1/activityTypes/{label} | label, name, active, groupLabel, features, colors, timeSlots, translations, defaultDuration, segmentMinDuration, segmentMaxDuration | Match zero or one Activity Type by the stable label | Existing optional fields and Activity Type Label | Treat a not-found result as new; stop before preview on an unexpected result or failed read |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A requested translation language is returned exactly once | Permit the Translation Matrix row to proceed to design enforcement |
| A language is not returned or is ambiguous | Stop before preview; do not infer a language code or label |
| A group or type current-state check fails | Stop before preview; do not infer replacement fields or retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.LOOKUP_CURRENT_STATE | step | 2 | reference_lookup | found->AT.DEPENDENCIES;unresolved->AT.RETURN_ISSUES;failure->AT.RETURN_ISSUES | AT.VALIDATE | stop | Before dependency readiness and any REST preview for Activity Types |
