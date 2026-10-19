# Candidate Selection Process Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm first-version applicability | Accept only new Standard processes authored in Draft; do not update, rename, duplicate, activate, inactivate, or delete an existing process |
| 2 | Apply identifier authority | Default CSP_PROCESS_CODE only when omitted, prove the CSP_SUBPROCESS_CODE pattern from the fresh export, prove SettingCode and SettingItemCode patterns from the user-authorized successful custom-phase package plus export collision dictionaries, and require Oracle-generated definition codes without inventing them |
| 3 | Validate custom blocks | Validate phase, state, and candidate-status blocks before package construction, including code authority, names, descriptions, and ordering |
| 4 | Reject unsupported phase/state reuse | Use the current export only to prove generated-code uniqueness and custom definition-code collisions. Do not reuse an existing phase or state until a clean completed reuse package establishes that contract. |
| 5 | Add and protect system-owned entries | Add the source-backed Offer then HR system blocks after custom phases; preserve seeded phase/state codes OFFER, HR, REJECTED_EMPLOYER, and WITHDRAWN_BY_CANDIDATE verbatim without user overrides |
| 6 | Protect package and execution route | Preserve required package members and exact parent/child joins, then hand any validated final archive exclusively to `core.data-loader`, which owns immutable preview, SHA-256 binding, standalone approval, upload, initiation, and result verification |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every first-version process | Blocker | check_candidate_selection_process_code_unique | Effective CSP_PROCESS_CODE already exists or repeats in input | Correct the user-defined code, or correct Name when using the documented default; never convert an item to update | Yes |
| A custom or system subprocess is needed | Blocker | verify_csp_subprocess_code_generation_pattern | The fresh export does not prove the exact CSW_ plus 32-uppercase-hexadecimal pattern, or a generated CSP_SUBPROCESS_CODE collides | Do not generate a subprocess code; obtain a source-backed pattern or correct the collision | Yes, after a fresh proof or collision-free generation |
| A custom, Offer, or HR settings block is needed | Blocker | verify_csp_setting_identifier_generation_pattern | The user-authorized successful custom-phase package does not prove the exact SETTING_CODE_ or SETTING_ITEM_CODE_ plus 32-uppercase-hexadecimal pattern, a required export collision dictionary is unavailable, or a generated identifier collides | Do not reuse a setting identifier from the example package. Generate a fresh identifier only after the profile and collision checks pass. | Yes, after the authorized-profile proof and collision-free generation |
| A custom phase is supplied | Blocker | check_custom_candidate_selection_phase_available | PHASE_DEFINITION_CODE is missing, nonnumeric, a numeric scientific-notation token, repeated, or collides with the current export; generated CSP_SUBPROCESS_CODE or Name collides | Supply the Oracle-generated definition code verbatim and retain the generated subprocess code; never derive either from Name or convert this path into reuse | Yes, by user-supplied Oracle-generated definition code |
| A custom state is supplied where the export shows numeric state-definition codes | Blocker | check_custom_candidate_selection_state_available | STATE_DEFINITION_CODE is missing, nonnumeric, a numeric scientific-notation token, repeated, or collides with the current export; or Name collides | Supply the Oracle-generated definition code verbatim; never derive it from Name or convert this path into reuse | Yes, by user-supplied Oracle-generated definition code |
| A candidate status is supplied | Blocker | resolve_candidate_status_by_name | The current export is unavailable, its dictionary is absent, or the status match is zero or ambiguous | Use exactly one export-backed candidate-status identity; candidate-status creation is outside this source-backed custom package profile | Yes, after a completed export or identity clarification |
| Multiple user-defined phases are supplied | Blocker |  | Effective sequence is noninteger, nonpositive, duplicate, or reserved entries are not trailing | Use list order or unique positive sequence; sort by effective sequence | Yes |
| Multiple user-defined states are supplied | Blocker |  | Effective sequence is noninteger, nonpositive, duplicate, or reserved entries are not trailing | Use list order or unique positive sequence; sort by effective sequence | Yes |
| A seeded phase or state is included | Blocker |  | Code differs from OFFER, HR, REJECTED_EMPLOYER, or WITHDRAWN_BY_CANDIDATE exactly | Use the seeded code verbatim; do not transform or generate it | Yes, restore the exact seeded code |
| Offer or HR is omitted or supplied | Warning | validate_custom_candidate_selection_process_archive | User-supplied Offer/HR properties would override a system-owned phase | Ignore any supplied properties, add the canonical Offer then HR blocks after custom phases with the generated CSP_SUBPROCESS_CODE and seeded codes OFFER and HR, and disclose the automatic addition | No user fix is required |
| A state named Rejected by Employer or Withdrawn by Candidate is supplied | Blocker |  | Its code is not the matching terminal seeded value, or it is not one of the final two FYI entries in that order | Treat it as FYI only, preserve the matching terminal seeded value, and warn; its properties cannot override a system-owned state | Yes, remove or reposition |
| An unsupported property, context, action, or object is supplied | Warning |  | The request would process unsupported data | Skip and disclose it; leave existing setup unchanged | Yes, remove it |
| Package construction starts | Blocker | validate_custom_candidate_selection_process_archive | Metadata or an expected CSV member would be removed; a custom row has no exact parent; Offer/HR blocks are absent or malformed; or a resolved candidate-status mapping is absent | Retain metadata and expected members, repair the exact joins, add the validated system blocks, and re-preview | Yes, restore and re-preview |
| Import is proposed | Blocker |  | The archive has not passed local package validation or has not been handed to `core.data-loader` | Block a direct pillar submission; use the mandatory `core.data-loader` handoff | Yes, through `core.data-loader` only |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_csp_subprocess_code_generation_pattern | A custom or system subprocess is needed | Export fingerprint, raw Code pattern proof, and matching identities | ora_reference_lookups.md |
| verify_csp_setting_identifier_generation_pattern | A custom, Offer, or HR settings block is needed | Authorized custom-package pattern proof, export fingerprint, raw setting collision dictionaries, and generated identity results | ora_reference_lookups.md |
| check_candidate_selection_process_code_unique | Every process before package generation | Effective CSP_PROCESS_CODE, export fingerprint, raw-exact and case-insensitive match counts, and matched identity | ora_reference_lookups.md |
| check_custom_candidate_selection_phase_available | A custom phase is supplied | Export fingerprint, PHASE_DEFINITION_CODE, CSP_SUBPROCESS_CODE, Name, and collision result | ora_reference_lookups.md |
| check_custom_candidate_selection_state_available | A custom state is supplied | Export fingerprint, STATE_DEFINITION_CODE, Name, numeric-shape result, and collision result | ora_reference_lookups.md |
| resolve_candidate_status_by_name | A candidate-status name is supplied | Export fingerprint and candidate-status identity, Name, `PublicStatesCode`, and `PublicStatesTypeCode` | ora_reference_lookups.md |
| validate_custom_candidate_selection_process_archive | A local archive is assembled | Member inventory, raw joins, system-block result, candidate-status mappings, and fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.CHECK_DESIGN | decision | 100 | design_enforcement | all_passed->CSP.VALIDATE_PACKAGE;blocked->CSP.HANDLE_ISSUES | CSP.APPLY_DEFAULTS | stop | The complete supported input list |
