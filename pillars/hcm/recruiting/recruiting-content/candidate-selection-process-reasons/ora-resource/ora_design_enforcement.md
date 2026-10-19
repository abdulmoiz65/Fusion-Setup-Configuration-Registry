# Candidate Selection Process Reasons Design Enforcement

## Purpose

Defines mandatory identity, lifecycle, translation, association, package, omission, and scope gates before a validated authoring package can be returned.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm exact identity and intent | Use the current task-wide export to classify each exact code or association as absent, present, or ambiguous |
| 2 | Enforce lifecycle and reference policy | Require supported status transitions, post-activation code locking, an Active reason, and an existing group where applicable |
| 3 | Enforce translation policy | Use explicit approved text and a target-installed Language; preserve the exported SourceLang or, for a new parent, use the target-evidenced base/source language |
| 4 | Build the minimal package | Preserve ASM metadata, all five CSV members, exact headers, nested translations, reason then group then usage order, and unrelated rows by omission |
| 5 | Confirm execution boundary | Return only a validated package and reconciliation plan; route any approved live import through core.data-loader |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| CSPRSN-DESIGN-REASON-IDENTITY | Reason create, update, replay, lifecycle, translation, or association | Blocking | resolve_existing_reason | Operation intent conflicts with exact ABSENT or PRESENT classification, exact identity is ambiguous, or a case-insensitive lookalike is unconfirmed | Correct the operation or confirm the exact case-sensitive ReasonCode | Lookup fix |
| CSPRSN-DESIGN-GROUP-IDENTITY | Group create, update, replay, lifecycle, translation, or association | Blocking | resolve_existing_reason_group | Operation intent conflicts with exact ABSENT or PRESENT classification, exact identity is ambiguous, or a case-insensitive lookalike is unconfirmed | Correct the operation or confirm the exact case-sensitive ReasonGroupCode | Lookup fix |
| CSPRSN-DESIGN-ASSOCIATION-IDENTITY | Association create, replay, or verification | Blocking | resolve_existing_association | Operation intent conflicts with exact ABSENT or PRESENT classification or the exact pair is ambiguous | Correct the operation or confirm the exact case-sensitive ReasonCode and ReasonGroupCode pair | Lookup fix |
| CSPRSN-DESIGN-REASON-CODE-LOCK | Existing reason update | Blocking | resolve_existing_reason | A ReasonCode change is requested after activation or through CSV; the code remains locked while Active or Inactive | Preserve the exact persisted ReasonCode and update only supported non-code fields | No |
| CSPRSN-DESIGN-GROUP-CODE-LOCK | Existing group update | Blocking | resolve_existing_reason_group | A ReasonGroupCode change is requested after activation or through CSV; the code remains locked while Active or Inactive | Preserve the exact persisted ReasonGroupCode and update only supported non-code fields | No |
| CSPRSN-DESIGN-REASON-LIFECYCLE | Reason create or status change | Blocking | resolve_existing_reason | Requested state is outside create as Draft or Active, Draft to Active, Active to Inactive, or Inactive to Active | Correct the requested initial state or transition | Input fix |
| CSPRSN-DESIGN-GROUP-LIFECYCLE | Group create or status change | Blocking | resolve_existing_reason_group | Requested state is outside create as Draft or Active, Draft to Active, Active to Inactive, or Inactive to Active | Correct the requested initial state or transition | Input fix |
| CSPRSN-DESIGN-ASSOCIATION | New association | Blocking | resolve_association_context | The reason is missing or not Active, the group is missing, the pair is ambiguous, or a replay would create more than one pair | Resolve an exact Active reason and exact existing group; preserve an existing exact pair as already satisfied | Lookup fix |
| CSPRSN-DESIGN-TRANSLATION | Translation create or update | Blocking | resolve_translation_context | Parent, installed Language, export-evidenced SourceLang, target base/source language for a new parent, or required translated text is missing or inconsistent; any CSV SourceLang change is requested | Supply explicit approved text, target the exact Language row, and preserve its exported SourceLang; for a new parent, use the current target's evidenced base/source language | Input fix |
| CSPRSN-DESIGN-PACKAGE | Any authoring package | Blocking | verify_csp_export_package | Metadata, a required member, exact header, nesting, reason-group-usage order, current-source fingerprint, or target/release evidence is missing or stale | Rebuild the smallest package from the validated current task-wide export | Source rebuild |
| CSPRSN-DESIGN-OMISSION | An update omits unrelated rows, comments, translations, or associations | Blocking | verify_csp_export_package | Omission is interpreted as deletion or an existing value is cleared without a separately supported explicit operation | Preserve omitted values and unrelated rows; absence is not deletion | Source rebuild |
| CSPRSN-DESIGN-DELETE | Delete or removal is requested | Blocking |  | CSV deletion, association removal by omission, translation removal by omission, or deletion of an Active or Inactive record is proposed | Do not generate deletion. Route an approved Draft reason or group deletion to the authorized UI | No |
| CSPRSN-DESIGN-SCOPE | Any task request | Blocking |  | The request changes candidate-selection-process states, requisitions, offers, notifications, formulas, candidate data, taxonomy, or unrelated setup | Keep the package limited to the five CSP Reasons objects | No |
| CSPRSN-DESIGN-HANDOFF | A package is ready | Blocking | verify_csp_export_package | The immutable package, exact delta, preserved values, validation result, fingerprint, target, and reconciliation plan are not disclosed | Rebuild the complete authoring handoff; core.data-loader owns any later preview and approval | Re-preview |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_csp_export_package | Every authoring and verification request | Target, release, task identity, member/header inventory, languages, current rows, and fingerprint | ora_reference_lookups.md |
| resolve_existing_reason | Reason create, update, lifecycle, translation, or association | Exact code, ABSENT or PRESENT result, current status, translations, and row fingerprint | ora_reference_lookups.md |
| resolve_existing_reason_group | Group create, update, lifecycle, translation, or association | Exact code, ABSENT or PRESENT result, current status, comments, translations, and row fingerprint | ora_reference_lookups.md |
| resolve_existing_association | Association create, replay, or verification | Exact pair and ABSENT or PRESENT result | ora_reference_lookups.md |
| resolve_association_context | New association | Exact Active reason, exact existing group, exact pair classification, and source fingerprints | ora_reference_lookups.md |
| resolve_translation_context | Translation create or update | Exact parent, target-installed Language, existing SourceLang or target base/source language, and approved translated values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSPRSN.CHECK_DESIGN | decision | 50 | design_enforcement | passed->CSPRSN.VALIDATE_PACKAGE;blocked->CSPRSN.HANDLE_ISSUES | CSPRSN.CHECK_DEPENDENCIES | stop | Every supported authoring request after dependency readiness |
