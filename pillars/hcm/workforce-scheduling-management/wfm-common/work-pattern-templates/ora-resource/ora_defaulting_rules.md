# Work Pattern Templates Defaulting Rules

## Source Basis

- Work Pattern Templates Rest Describe, Confluence page 21510086973, version 3
- Work Pattern Templates Technical Design Document for FSCR, Confluence page 21509588886, version 9
- Work Pattern Page Screen Shots, developer-provided DOCX, received 13 August 2026
- Cumulative DayOfWorkPattern rule for multi-cycle templates, user-provided, received 17 August 2026
- Successful Work Pattern Templates create DAT with parent, Shift, and Break loader correlations, user-provided, received 17 August 2026
- User-facing field-label, defaulting, and Template Name rules, user-provided, received 18 August 2026
- Cycle-week coverage and minute-precision rules, user-provided, received 18 August 2026
- Name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026
- WFM-81615 Recommended Best Practices: unspecified break type default, Jira, reviewed 10 September 2026
- WFM-81615 Recommended Best Practices: Work Pattern Template naming, Jira, reviewed 10 September 2026
- Break Name defaulting from duration, Shift Period Type, and paid or unpaid status, developer-provided, received 18 September 2026

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| RepeatCycle | ORA_HTS_WEEKS | A new template is initialized and no value is supplied | No; the active template UI fixes the unit to Weeks | resolve_repeat_cycle |
| RepeatNumber | 1 | A new template is initialized and no value is supplied | No; preserve an explicitly supplied valid value |  |
| ActiveFlag | true | A new template is initialized and no value is supplied | No; preserve an explicitly supplied boolean |  |
| Break Type | Any time during shift | A Break is included and its type is not supplied | No; preserve a verified explicitly supplied Break Type | resolve_break_type |
| Break Name | Combination of available Duration in Minutes, Shift Period Type, and paid or unpaid status values | A Break is included and no Break Name is supplied | No; preserve an explicitly supplied Break Name |  |
| isNonWorkingWeek | No default | A cycle week has no shift details | No; ask the user whether that entire week is nonworking and preserve the explicit choice |  |
| DayOfWorkPattern | No default | A Shift row is created | No; derive each value from its selected cycle and weekday as (cycle - 1) x 7 + weekday index, where Sunday is 1 and Saturday is 7 |  |
| WorkPatternCode | Fusion-generated value | A template is created | No; do not send a user-created or name-derived value |  |
| TemplateName | WPT <Population or Purpose> <Shift behavior or Pattern> - <Cycle> | A template is created, no explicit Template Name or customer naming convention is supplied, and the relevant naming inputs are available from supplied values, applicable conversation, selected values, and configured defaults | No; preserve an explicit user-provided Template Name or a supplied customer naming convention. When neither is supplied, use the naming-guideline result and include population or purpose, shift behavior, and cycle when useful and available. Only when neither an explicit name nor a derivable result is available, ask for Template Name directly |  |

## Defaulting Boundaries

| Situation | What Happens |
|---|---|
| Shift Period Type is selected on create | Make Add Shift available and retain the displayed Cycles default of 1 and Unit of Measure of Weeks |
| Duplicate template | Clear the persistent parent and child identities, use local child identities, and apply the localized Duplicate name prefix; the user may edit the resulting name before save |
| WorkShiftType changes | Reset RepeatNumber to 1 as documented by the UI flow and revalidate dependent shift and break content |
| WorkDayDefinitionId is absent | Leave it unset; no literal default is documented |
| An entire cycle week has no shift details | Do not infer a nonworking week. Ask the user whether to mark the week nonworking before preview or artifact generation |
| Start Time, End Time, work duration, or break values include minutes | Preserve the user-provided minute-level value. Do not apply a 15-minute rounding default |
| Template Name is evaluated on create | Preserve an explicit Template Name supplied by the user. When a customer naming convention is supplied, align the name to that convention. Otherwise, derive a recognizable name using WPT <Population or Purpose> <Shift behavior or Pattern> - <Cycle>, including each useful available component. Only when neither an explicit name nor a derivable result is available, ask for Template Name directly; do not request missing naming inputs. |
| A field value is resolved | Use this precedence: explicit user value; still-applicable current-conversation or selected-configuration value; configured default; then ask only when the field is required and no valid value or default exists. |
| A documented default applies | Apply it without asking the user. In a proposed or final result, label it Default. Do not label a value Default when the user explicitly supplied it, even when it equals the default. |
| A Break is included without a Break Type | Apply Any time during shift before validation, preview, or artifact generation. Display Break Type: Any time during shift — Default in the proposed configuration before approval. |
| A Break is included without a Break Name | Derive the Break Name from any available combination of the Break's Duration in Minutes, parent Shift Period Type, and paid or unpaid status. Do not request missing naming components or a separate name. Preserve an explicitly supplied Break Name. |
| A new template aggregate is prepared through Data Loader | Allocate a unique local WorkPatternTemplateId correlation value for its parent and reuse it in every new Shift row; it is not an existing Fusion identifier and does not replace the Fusion-generated WorkPatternCode |
| AnchorNumber is absent | Do not invent a selection; the UI generates choices from 1 through RepeatNumber and displays the field only when RepeatNumber is greater than 1 |
| A loaded template contains existing values | Preserve the loaded values unless the user explicitly changes them and the change passes validation |
| A Data Loader update is prepared | Read the current WorkPatternCode explicitly from Fusion; it is not a create-time default to invent or override |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WPT.APPLY_DEFAULTS | step | 40 | apply_default | applied->WPT.ENFORCE_TEMPLATE_DESIGN;not_applicable->WPT.ENFORCE_TEMPLATE_DESIGN;blocked->WPT.HANDLE_ERROR | WPT.CHECK_DEPENDENCIES | stop | Apply only documented defaults whose conditions are satisfied |
