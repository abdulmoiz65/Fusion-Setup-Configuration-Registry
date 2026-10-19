# Candidate Selection Process Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Process list | Nonempty processes list with one or more process objects | Fail the complete request; do not produce a package | Provide the complete process list | Every create-authoring request |  |
| Process identity | Trimmed nonblank Name of 1-100 characters and optional user-defined CSP_PROCESS_CODE of 1-256 characters | Fail the complete request only when Name is missing or overlength; derive CSP_PROCESS_CODE when it is omitted | Supply a valid Name and, optionally, a user-defined CSP_PROCESS_CODE | Every process |  |
| Standard process type | Omitted type or Standard | Fail; do not coerce Pipeline or another value | Supply Standard or omit the property | Every process |  |
| Custom phase block | Nonempty phases list with a trimmed nonblank Name and an Oracle-generated numeric PHASE_DEFINITION_CODE for each custom phase | Fail the affected request | Supply the Oracle-generated PHASE_DEFINITION_CODE verbatim. Do not derive or invent it. Offer and HR are optional in the request because the package adds their system blocks. | Every process | check_custom_candidate_selection_phase_available |
| Custom state block | Nonempty states list with a trimmed nonblank Name and candidate-status Name for each state; include STATE_DEFINITION_CODE when the fresh export shows numeric state-definition codes | Stop after the export classification when a required STATE_DEFINITION_CODE is absent | Supply the Oracle-generated STATE_DEFINITION_CODE verbatim when the export shows that numeric shape. Do not derive or invent it. | Every custom phase | check_custom_candidate_selection_state_available |
| Candidate-status block | Trimmed nonblank candidate-status Name of 1-100 characters | Fail the affected request | Supply a candidate-status name for every supported user-defined state | Every supported user-defined state |  |
| Translation source language | Omitted `sourceLanguage`, or explicit `US` | Fail the affected request | Omit the field to use the source-backed `US` default, or supply `US` exactly | A new description is supplied | validate_custom_package_source_language |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Descriptions | Allow optional process, phase, state, and candidate-status descriptions up to 1000 characters; reject an overlength description for a new object | A description is supplied |  |
| CSP_PROCESS_CODE | Use the user-defined value when supplied. When omitted, outer-trim Name, uppercase it, and replace every whitespace character with `_`; preserve all other characters. | Before process-code uniqueness validation |  |
| Process code uniqueness | Reject duplicate effective CSP_PROCESS_CODE values in the supplied list and reject the complete list when the fresh export finds any effective code under the documented case-insensitive comparison; never convert to update | After identifier defaults and export baseline validation and before package generation | check_candidate_selection_process_code_unique |
| CSP_SUBPROCESS_CODE | Accept no user-supplied replacement. Generate a `CSW_` plus 32-uppercase-hexadecimal value only after the fresh export proves that exact pattern; preserve it as text and reject any generated collision. | A custom or system subprocess is needed after export validation | generate_csp_subprocess_code |
| SettingCode and SettingItemCode | Accept no user-supplied replacement. Generate SETTING_CODE_ or SETTING_ITEM_CODE_ plus 32-uppercase-hexadecimal characters only after the user-authorized successful custom-phase package proves the exact corresponding pattern and the fresh export supplies the collision dictionary; preserve them as text and reject any generated collision. | A custom, Offer, or HR settings row or setting-item row is needed after export validation | verify_csp_setting_identifier_generation_pattern |
| PHASE_DEFINITION_CODE | Require the Oracle-generated numeric identifier, preserve it verbatim, and reject blanks, nonnumeric values, numeric scientific-notation tokens such as `3.001E+14`, duplicates, or an exported collision. Do not derive or invent it. | A custom phase is supplied after export validation | check_custom_candidate_selection_phase_available |
| STATE_DEFINITION_CODE | When the fresh export shows numeric state-definition codes, require the Oracle-generated numeric identifier and preserve it verbatim. Reject blanks, nonnumeric values, numeric scientific-notation tokens such as `3.001E+14`, duplicates, or an exported collision. Do not derive or invent it. | A custom state is supplied after export validation | check_custom_candidate_selection_state_available |
| SEEDED_PHASE_OR_STATE_CODE | Use seeded values verbatim: OFFER, HR, REJECTED_EMPLOYER, and WITHDRAWN_BY_CANDIDATE. Do not transform, regenerate, or allow a user override. | A source-backed system phase or terminal state is added |  |
| Candidate-status reuse | Reuse only one export-backed candidate-status-name match. Ignore the supplied description with a warning when reusing; fail on ambiguity or an unavailable export dictionary | A candidate-status name is supplied after export validation | resolve_candidate_status_by_name |
| Translation language | Use `US` when `sourceLanguage` is omitted. If supplied, require `US` exactly. This constrained behavior is the one established by the successful custom-phase package; no broader language-resolution contract is asserted. | A new description is supplied | validate_custom_package_source_language |
| Unsupported properties | Omit the property and return an ignoredFields warning; do not fail solely for its presence | An unsupported property is supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.VALIDATE_INPUTS | decision | 10 | validate_input | valid->CSP.CLASSIFY_REQUEST;invalid->CSP.HANDLE_ISSUES | none | stop | Every create-authoring or verification request |
| CSP.CLASSIFY_REQUEST | decision | 20 | evaluate_result | authoring->CSP.EXPORT_BASELINE;verification->CSP.VERIFY_RESULT;unsupported->CSP.HANDLE_ISSUES | CSP.VALIDATE_INPUTS | stop | After input validation |
| CSP.VALIDATE_SOURCE_LANGUAGE | decision | 85 | validate_input | valid_or_not_applicable->CSP.APPLY_DEFAULTS;invalid->CSP.HANDLE_ISSUES | CSP.RESOLVE_STATUSES | stop | A new description is supplied |
| CSP.VERIFY_RESULT | decision | 120 | evaluate_result | verified->CSP.DONE_VERIFIED;failed->CSP.HANDLE_ISSUES | CSP.CLASSIFY_REQUEST | stop | A post-import export and status evidence are supplied |
