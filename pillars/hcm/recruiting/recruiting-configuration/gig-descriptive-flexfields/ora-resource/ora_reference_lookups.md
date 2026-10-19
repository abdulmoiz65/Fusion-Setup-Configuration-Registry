# Gig Descriptive Flexfields Reference Lookups

For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md.

Global create, copy, update, and disable may use the [verified fallback export contract](ora_gig_global_segment_archive_contract.md), after a selected-environment exact-task export attempt fails, times out, or returns unusable rows. Confirm the complete design and disclose unavailable current-state checks as `UNVERIFIED`. Verification and context-sensitive work require a validated populated current-definition package. Global copy/update/disable use the confirmed fallback rules when fresh evidence is unavailable. Standalone list/inspect still requires a fresh export.

These contracts use the exact Gig setup-task CSV export as the authoritative current-definition source for `IRC_MP_GIGS_DFF`. They do not authorize a direct DFF REST call, browser probing, database access, or reuse of a Referral export.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_gig_dff_segments_from_task_export | An explicit Inspect/list request or a copy or duplicate request without a source segment has produced an export | Downloaded and extracted output from shared.setup-export.task-level-export for task ORA_IRC_MANAGE_OM_GIG_DESCRIPTIVE_FLEXFIELDS | Require the exact task export; require DFF code IRC_MP_GIGS_DFF and application 821 on every segment row; read Global rows only from ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_GLOBAL_SEGMENT.csv and context-sensitive rows only from ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_SEGMENT.csv; join contexts through ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT.csv; reject the hidden selector in ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT_SEGMENT.csv | Export identity; Global segments; exact Gig contexts; context-sensitive segments grouped by context; segment name, code, API name, column, sequence, enabled state, data/display properties, and value-set code when present | Return MISSING if required members or rows are absent; return AMBIGUOUS if a context join is not unique; return INVALID for another DFF/application or malformed headers; stop without partial cross-DFF substitution |
| verify_gig_dff_current_definition | A create, update, copy, disable, or verification decision requires current state | Fresh validated exact-task export for this copy/update/disable request; validated matching package for new create or verification | Require exact DFF code IRC_MP_GIGS_DFF and application 821 when the source is a DFF artifact; require one unique row per scope and segment code; reject mismatched, malformed, unrelated, or insufficient evidence | Exact DFF identity; segments; contexts; occupied columns and sequences; current properties; capture time and environment when present | Return MISSING, AMBIGUOUS, or BLOCKED when the available evidence is insufficient after the matching package check and permitted fresh export |
| verify_gig_context_identity | A context-sensitive request uses an exact context and a validated current Gig export or approved local baseline is available | Context rows and context-segment rows from the validated IRC_MP_GIGS_DFF artifact | Require one exact context code and displayed label belonging to IRC_MP_GIGS_DFF; reject Referral identities and the hidden context selector | Verified context code; displayed label; enabled state; segments in that context | Return MISSING or AMBIGUOUS; keep Global scope separate and do not create, rename, or substitute a context |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_gig_value_set_compatibility | A segment uses an existing value set  | Target environment; exact displayed value-set code or name; proposed segment data type and display use | GET /fscmRestApi/resources/11.13.18.05/valueSets through core.fusion-api.apps-common.value-sets | Returned value-set identifier and displayed code/name; validation type, value data type, module, and enabled metadata when exposed | Filter the returned collection to one exact displayed code or name and require enough returned metadata to prove compatibility; never derive an internal identifier | Verified value-set identity and the returned compatibility metadata | Return MISSING or AMBIGUOUS for zero or multiple exact matches; return BLOCKED if the resource does not expose enough metadata to prove compatibility |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| An Inspect/list request is received | Run a fresh shared.setup-export.task-level-export from the selected environment, validate and extract the ZIP, then execute resolve_gig_dff_segments_from_task_export; do not substitute a prior local export |
| A create, update, or copy request is received | For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md. |
| A copy or duplicate request omits its source | Run a fresh exact-task export and require one exact source selection; use the qualified Global fallback proposal if unavailable or empty |
| An export contains another DFF, application, task, or an unjoinable context | Reject it and do not return or map those rows |
| The export contains the hidden context-selector row | Exclude it from the user-facing segment list; it is transport metadata, not a configurable Gig business segment |
| A browser, direct database query, undocumented API, or Referral artifact is proposed as fallback | Refuse the substitution and retain the routed exact-task export boundary |
| A 401 or 403 occurs on an approved read-only route | Allow one cached-token refresh only when the selected workflow permits it; otherwise return AUTHORIZATION |
