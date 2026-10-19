# Defaulting Rules

Do not promote values observed in a sample DAT, FSM export, another subscriber, REST default, database default, or older implementation into an HDL default. Route-required values and product defaults remain target-contract facts and must not be silently materialized.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SubscriberName, QuestionnaireCode, QstnrVersionNum, and QuestionnaireName | No default | Always | No | |
| TemplateQstnrCode and category/folder | No default | Always | No | |
| Status, InUse, privacy, owner, introduction, presentation, layout, scoring, and override values | No default | Always | No | |
| Approved suggestion-capable reference correction | Exact canonical value or complete compatible value set selected from the declared current-target catalog | The original exact resolver returned zero, the user approved the bound candidate, and the original exact resolver plus compatibility checks succeed again immediately before preview | No | propose_reference_value |
| Sections, question placements, answer overrides, and attachments | No content default | Always | No | |
| Existing required values | Preserve the exact approved current target value | A change omits a value that must remain present and preservation is supported by the live operation | No | |
| Omitted existing Section, Question placement, direct Question, or Answer | Preserve the existing target row; emit no delete or replacement instruction | An update does not include that child row | No | |
| Update row intent | No default | A hierarchy-bearing change is requested | No | |
| Existing template linkage | Preserve the exact current TemplateQstnrCode or absence | An update does not include an explicitly proven mutable linkage change | No | |
| New Section and Question placement sequence | Deterministic approved source order | A new hierarchy omits explicit sequence and the live contract permits the value | No | |
| Placement response override | Blank means inherit; do not emit a value | No explicit QstnrQstnResponseTypeName is supplied | No | |
| ScoredFlag, calculation rule, maximum score, and mandatory child behavior | No default | Always | No | |
| LayoutOption | No default | Always | No | |
| Generated IDs, LatestVersion, object version, seed/module provenance, and internal subscriber values | No default | Always | No | |
| Loader or product default | Do not materialize locally | A route-specific default exists but approved intent does not explicitly select a value | No | |
| UpdateAllowed | Preserve the exact approved target value; no create-time default | A supported update includes the field | No | |

Any value copied from current target state is preservation, not a universal default. An approved reference correction is scoped to that one bound field or value set and does not authorize another inferred value. Show inherited, preserved, approved-correction, and supplied values separately in preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QNR.APPLY-DEFAULTS | step | 30 | apply_default | applied_or_not_needed->QNR.ENFORCE-DESIGN;invalid_default_request->QNR.HANDLE-ISSUE | QNR.CHECK-DEPENDENCIES | stop | Dependencies are ready |
