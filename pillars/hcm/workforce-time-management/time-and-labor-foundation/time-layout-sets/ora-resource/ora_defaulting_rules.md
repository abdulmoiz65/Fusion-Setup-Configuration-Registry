# Time Layout Sets Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TimeEntryFormat | BOTH | New or incomplete entry layout is prepared for Data Loader preview | No |  |
| DecimalPrecision | 2 | New or incomplete entry layout is prepared for Data Loader preview | Yes |  |
| DateFormat | EEEEE, MMMMM dd | New or incomplete entry layout is prepared for Data Loader preview | Yes |  |
| DefaultBlankRows | 5 | New or incomplete entry layout is prepared for Data Loader preview | Yes |  |
| Default time card layout totals | Generated default totals rows | New layout is prepared for Data Loader preview | No | resolve_default_time_card_layout_totals |
| Time card fields | Generated fields for the selected Time Consumer Sets, with DisplaySequence from 1 in returned row order | New Time Entry Layout has selected consumers | No | resolve_default_time_card_fields |
| ButtonLogicCode | FOLLOW_SEQ_RESTART | New Web Clock layout is prepared for Data Loader preview | Yes | resolve_button_sequence |
| AllowManualEntryOfMissingInEventFlag | false | New Web Clock layout is prepared for Data Loader preview | Yes |  |
| AssociateTimecardFieldsToInEventForInOutPairFlag | false | New Web Clock layout is prepared for Data Loader preview | Yes |  |

## Default Materialization

Apply every applicable Standard Defaults value to the prepared source and final
Data Loader archive before preview. A user-supplied value takes precedence only
when Override User Value? is Yes. Do not treat a UI default as documentation
only or leave a default-eligible archive field blank.

When a Time Consumer Set is selected, obtain the default timeCardFields from
resolve_default_time_card_fields and materialize every returned row as a child
of the new timeEntryLayout. Retain the returned TimeCardFieldTemplateId, Name,
Label, and Description and assign DisplaySequence from 1 in returned row order.
The generated collection replaces an empty field collection; do not derive it
from a previous layout or a static sample.

## Complete Summary Default Presentation

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Applied defaults | Include every default that was actually applied in the Defaults Applied section, using its business label and verified business display value | A Complete Summary is generated | No | |
| Boolean display | Use Selected or Not selected, Enabled or Disabled, or Yes or No when a verified business label is available | A populated boolean is shown in the Complete Summary | No | |
| Status display | Use a verified business-friendly status such as Draft or Submitted | A populated internal status is shown in the Complete Summary | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TLS.APPLY_DEFAULTS | step | 40 | apply_default | applied->TLS.ENFORCE_DESIGN;not_applicable->TLS.ENFORCE_DESIGN | TLS.RESOLVE_LOOKUPS | stop | New or incomplete layout is prepared |
