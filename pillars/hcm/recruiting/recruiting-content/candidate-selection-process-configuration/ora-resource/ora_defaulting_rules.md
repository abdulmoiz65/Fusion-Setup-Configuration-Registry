# Candidate Selection Process Defaults

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Process type | Standard with technical TypeCode CSW | Every first-version create request | No; reject Pipeline or another supplied value |  |
| Process status | Draft with technical StatusCode ORA_DRAFT | Every first-version create request | No; ignore a supplied status and report it |  |
| Process usage | TEMPLATE | Every first-version create request | No; ignore a supplied value and report it |  |
| Active flag | N | Every first-version create request | No; ignore a supplied value and report it |  |
| CSP_PROCESS_CODE | User-defined CSP_PROCESS_CODE, or outer-trimmed Name uppercased with every whitespace character replaced by `_` | Every first-version create request | Yes; a user-defined value wins |  |
| CSP_SUBPROCESS_CODE | Client-generated CSW_ plus 32-uppercase-hexadecimal characters after the fresh export proves that exact pattern | Every custom and system subprocess row | No; no user override | generate_csp_subprocess_code |
| SettingCode | Client-generated SETTING_CODE_ plus 32-uppercase-hexadecimal characters after the user-authorized successful custom-phase package proves that exact setting-code pattern and the fresh export supplies the collision dictionary | Every custom, Offer, and HR settings row | No; no user override | generate_csp_setting_code |
| SettingItemCode | Client-generated SETTING_ITEM_CODE_ plus 32-uppercase-hexadecimal characters after the user-authorized successful custom-phase package proves that exact setting-item-code pattern and the fresh export supplies the collision dictionary | Every custom, Offer, and HR setting-item row | No; no user override | generate_csp_setting_item_code |
| PHASE_DEFINITION_CODE | No default; retain the Oracle-generated numeric identifier supplied for the custom phase | Every custom phase | No |  |
| STATE_DEFINITION_CODE | No default; when the export shows numeric state-definition codes, retain the Oracle-generated numeric identifier supplied for the custom state | Every custom state | No |  |
| SEEDED_PHASE_OR_STATE_CODE | OFFER, HR, REJECTED_EMPLOYER, or WITHDRAWN_BY_CANDIDATE exactly as seeded | A system phase or terminal state is added | No |  |
| Phase order | One-based textual list position, unless a positive unique sequence is supplied | Multiple user-defined phases | Yes; supplied sequence replaces the default |  |
| State order | One-based textual list position, unless a positive unique sequence is supplied | Multiple user-defined states in a phase | Yes; supplied sequence replaces the default |  |
| Translation SourceLang | `US` | A new description is supplied | Yes; only an explicit `US` is accepted | validate_custom_package_source_language |
| Offer system block | Add an Offer `ORA_IRC_LC` row after all custom phases, with TypeCode `CSW_OFFER_PHASE`, Draft/TEMPLATE/inactive defaults, a generated CSP_SUBPROCESS_CODE, seeded phase code OFFER, required settings, and the source-backed Offer routing block | Offer is omitted or supplied as FYI | Yes; user properties cannot override it | validate_custom_candidate_selection_process_archive |
| HR system block | Add an HR `ORA_IRC_LC` row immediately after Offer, with TypeCode `CSW_HR_PHASE`, Draft/TEMPLATE/inactive defaults, a generated CSP_SUBPROCESS_CODE, seeded phase code HR, required settings, and the source-backed HR routing block | HR is omitted or supplied as FYI | Yes; user properties cannot override it | validate_custom_candidate_selection_process_archive |
| Custom-phase terminal states | Add seeded `REJECTED_EMPLOYER` and `WITHDRAWN_BY_CANDIDATE` terminal-state routing for every custom phase | Every custom phase | No; they are system-owned and are not extra user-defined state inputs | validate_custom_candidate_selection_process_archive |

Only CSP_PROCESS_CODE, a pattern-proven CSP_SUBPROCESS_CODE, and the user-authorized custom-package SettingCode and SettingItemCode profiles are client-derived. PHASE_DEFINITION_CODE and numeric STATE_DEFINITION_CODE are Oracle-generated values and must never be invented. Seeded phase and state codes are literals.

When previewing a custom phase, show its user-defined state count separately from the two seeded terminal states. For example, two supplied custom states produce four states in the Fusion phase UI.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.APPLY_IDENTIFIER_DEFAULTS | step | 47 | apply_default | identifiers_applied->CSP.CHECK_CODE;failure->CSP.HANDLE_ISSUES | CSP.CHECK_SETTING_IDENTIFIER_PATTERN | stop | A process passed baseline validation and subprocess plus setting-identifier patterns are proven |
| CSP.APPLY_DEFAULTS | step | 90 | apply_default | applied_to_all->CSP.CHECK_DESIGN;failure->CSP.HANDLE_ISSUES | CSP.VALIDATE_SOURCE_LANGUAGE | stop | Every process in a supported input list |
