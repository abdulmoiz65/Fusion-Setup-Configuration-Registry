# Events Defaulting Rules

Defaults are row-scoped and never make an incomplete Draft activation-ready.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Lifecycle intent | Draft | A create row has no explicit supported lifecycle intent | No; preserve an explicit activation request and apply its stricter gates | |
| learningItemStatus | ORA_DRAFT | A create row follows FDD version 5 Draft behavior | No; send ORA_DRAFT explicitly after live-value validation | resolve_event_lifecycle_values |
| learningItemType | ORA_EVENT | A create row omits the type and current target metadata still confirms its Event default | No; never turn another learning-item type into an Event | |
| Activation behavior | Separate approved operation | Every create or update | No | |
| Course linkage | Standalone | The row explicitly states that no course linkage is required | No; never discard or invent a supplied course | |
| Omitted optional mutation fields | Preserve current value or omit from create payload | A field is optional and the user did not request a change | No; never copy a sample or read-only response value into the write | |

## No-Default Rules

| Field or Decision | Why No Default Is Allowed |
|---|---|
| Event number and title | They are business identity and must be supplied explicitly |
| Visibility | It is REST-required and can change audience exposure |
| Activity dates, times, and time zone | An inferred window can create conflicts or learner impact |
| Capacity, waitlist, and enrollment behavior | Defaults could change learner access or overbook a resource |
| Instructor, classroom, supplier, webinar account, or ad hoc resource | Every resource reference needs exact request-specific evidence |
| Lifecycle target, cancel reason, close reason, or closed-activity status | Enabled values and transitions are target- and state-specific |
| DFF context segments | Only live target metadata can define portable segment contracts |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVT.APPLY_DEFAULTS | decision | 4 | apply_default | applied->EVT.ENFORCE_DESIGN;preserved->EVT.ENFORCE_DESIGN;blocked->EVT.HANDLE_ERROR | EVT.RESOLVE_REFERENCE | stop | A validated row omits only a documented safe default |
