# Receiving Document Output Preferences Input Validation

Sources: effective setup-task catalog, task-level FSM CSV export structure, registered Data Loader business object, and the provided Redwood document-output-preferences flow.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Header preference | Job set, job, layout, format, start date, end date, and receiving product context | Stop preparation | Supply the business values and resolve applicable LOV values in dependency order | A header preference is created or changed | |
| Output-line preference | At least one applicable output destination and its corresponding fields | Stop preparation | Supply line fields for the selected output destination | A preference line is created or changed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LOV-backed fields | Accept an approved code or display value. When both are supplied, require the same single resolved record; trim and compare case-insensitively. | Any LOV-backed field is supplied | |
| Effective dates | Normalize `StartDateActive` and `EndDateActive` to ISO `YYYY-MM-DD` before FSM CSV preparation or Data Loader handoff; use the identical normalized start date in every supplied output line. | A header preference is created or changed | |
| Job dependency changes | A changed job clears the UI's layout and format selections. A changed layout clears the UI's format selection. Do not retain stale dependent values. | A header is prepared from UI-equivalent input | resolve_job |
| Organization dependency | Resolve organization before subinventory; changing organization requires a new subinventory resolution. | A subinventory is supplied | resolve_subinventory |
| User selection | A selected user maps its returned PersonId to UserId. | A user is supplied | resolve_user |
| Route ownership | Do not add local required-field, uniqueness, length, server-domain, or final payload validation. The selected FSM import or Data Loader workflow, and Fusion, own those checks. | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCDOP.VALIDATE_INPUT | decision | 10 | validate_input | valid->RCDOP.RESOLVE_LOVS;invalid->RCDOP.RETURN_ISSUES | none | stop | Receiving Document Output Preferences input is prepared for the selected FSM or Data Loader route |
