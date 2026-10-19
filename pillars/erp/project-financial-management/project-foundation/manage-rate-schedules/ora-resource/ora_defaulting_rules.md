# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted header/line group or field | Preserve current values/rows; merge only explicit deltas before validation | Existing-row update; omission is not an instruction to clear/delete and explicit null/blank is a requested clear | No | find_rate_schedule |
| ScheduleType | EMPLOYEE (UI label Person) | New header only, type omitted; never choose a different type from inferred purpose | No | resolve_schedule_type |
| StartDateActive | Current business date supplied by the selected target workflow with its timezone/date authority | New line only, From Date omitted/null/blank; capture date before preview, never hard-code an observed date | No | resolve_rate_current_date |
| EndDateActive (CSV); evidenced end-date field otherwise | Blank | Line create | No |  |
| RateUnit | HOURS | New Person/Job/Project Role line; or Resource Class resolved as Labor/Equipment; source-proven subtype default | No | resolve_rate_lines |
| Person organization | Same assignment organization as selected job | Person job selected, organization omitted, and assignment result proven | No; disclose default | resolve_rate_references |
| Unresolved dependent default | Preserve supplied value; leave unproven default unapplied and warn | Membership/eligibility evidence missing | No | record_unresolved_rate_reference |
| Route | No implicit route replacement; honor the selected runbook/Data Loader route, including requested FSM | Before preview; capability does not choose an executor | No | verify_rate_route |
| Copy percentage | No implicit adjustment | Copy | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE.APPLY_DEFAULTS | step | 2 | apply_default | applied->RATE.FIND_SCHEDULE;warning->RATE.FIND_SCHEDULE;failure->RATE.RETURN_ISSUES | RATE.VALIDATE_INPUT | stop | Apply only already-proven defaults; defer reference-dependent defaults to supported resolution |

Resolve multilingual user intent before defaults; never overwrite a supplied value or infer a name/code from unresolved prose. Nonlabor RateUnit derives from the resolved expenditure type. Material Items/Financial Resources use the separate configurable UOM contract; do not default them to HOURS. A missing optional default authority warns and does not skip supported checks. A missing required From Date authority is needs_input for the affected new line, as specified below.

The manifest's REST preference is only a pre-selection recommendation when no route is requested or selected. It never replaces an explicit/requested FSM route or an approved route. The route dependency and selected Data Loader adapter, not a discovered writable endpoint, determine execution.

The UI prefilled 10/13/26 while the client date was 2026-10-14. This establishes defaulting, not the server clock or timezone. The selected workflow must supply an authoritative current date for omitted From Date; if unavailable, leave the affected new line unresolved and return needs_input before its preview. Do not guess the client day, serialize null as a valid From Date, change an explicit 2009-01-01, or apply create defaults to an omitted update group. A supplied date wins. Freeze the resolved date in the immutable candidate and disclose its authority; date rollover does not silently mutate an approved candidate.
