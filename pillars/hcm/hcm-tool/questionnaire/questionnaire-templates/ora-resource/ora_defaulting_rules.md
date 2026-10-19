# Defaulting Rules

Do not promote values observed in a sample DAT, FSM export, another subscriber, REST default, database default, or older implementation into an HDL default. TemplateFlag Y is a translation/backing discriminator where the live contract requires it, not permission to synthesize unrelated internal values.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SubscriberName, QuestionnaireCode, Name, and version identity | No default | Always | No | |
| Status, privacy, owner, presentation, page, response-format, scoring, and override controls | No default | Always | No | |
| Approved suggestion-capable reference correction | Exact canonical value or complete compatible value set selected from the declared current-target catalog | The original exact resolver returned zero, the user approved the bound candidate, and the original exact resolver plus compatibility checks succeed again immediately before preview | No | propose_reference_value |
| Sections, question placements, answers, and attachments | No content default | Always | No | |
| Existing required values | Preserve the exact approved current target value | A change omits a value that must remain present and preservation is supported by the live operation | No | |
| Omitted existing Section, Question placement, or Answer | Preserve the existing target row; emit no delete or replacement instruction | An update does not include that child row | No | |
| Update row intent | No default | A hierarchy-bearing change is requested | No | |
| New Section and Question placement sequence | Deterministic approved source order | A new hierarchy omits an explicit sequence and the live contract permits the value | No | |
| Embedded question version, status, category, response type, answers, and scoring | No default | An embedded question is intentionally created | No | |
| Calculation rule and maximum score | No default | Scoring is enabled | No | |
| Internal questionnaire version, LatestVersion, generated IDs, and seed/module provenance | No default | Always | No | |
| Loader or product default | Do not materialize locally | A route-specific default exists but the approved design does not explicitly select a value | No | |
| UpdateAllowed | Preserve the exact approved target value; no create-time default | A supported update includes the field | No | |

Any value copied from current target state is preservation. An approved reference correction is scoped to that one bound field or value set and does not authorize another inferred value. Any value inherited by a derived questionnaire is downstream behavior and is not a default emitted into QuestionnaireTemplate.dat unless the live contract and approved design require it.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QTPL.APPLY-DEFAULTS | step | 30 | apply_default | applied_or_not_needed->QTPL.ENFORCE-DESIGN;invalid_default_request->QTPL.HANDLE-ISSUE | QTPL.CHECK-DEPENDENCIES | stop | Dependencies are ready |
