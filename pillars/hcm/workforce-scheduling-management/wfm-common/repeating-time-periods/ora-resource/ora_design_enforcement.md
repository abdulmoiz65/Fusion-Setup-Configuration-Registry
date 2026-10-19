# Repeating Time Periods Design Enforcement

## Source Basis

- Generic FSM Baseline, developer-provided text, used only for FSM package safety rules and import boundaries.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce delta scope | Use the fresh export as a mapping and validation baseline, support every task-scoped CSV member in it, and include only approved created or updated Repeating Time Period rows in each member. |
| 2 | Preserve edit identity | For edit, use only the exactly matched Current Name row from the fresh same-task export. |
| 3 | Enforce edit field scope | For edit, alter only Name and/or Description; retain PeriodCd, GroupingKey, and every other exported parent and translation field. |
| 4 | Preserve FSM format | Retain the FSM ZIP shape; do not convert it to an HCM Data Loader archive. |
| 5 | Use the declared route | Route the validated FSM ZIP only through core.data-loader; do not use direct Fusion REST mutations. |
| 6 | Confirm creation after functional matches | When one or more exact functional matches exist, show every matching period using UI-exposed values and ask whether the user still wants a new period. |
| 7 | Generate Complete Summary | After validation, lookup resolution, and defaulting, generate the required business-only Complete Summary from verified structured fields. |
| 8 | Bind approval to preview | Present the Complete Summary, then continue to the provider-owned immutable-preview and approval process using only current evidence. |
| 9 | Stop on uncertainty | Do not automatically retry a failed, partial, timed-out, or uncertain import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An FSM package is prepared | Blocker |  | The package includes unrelated exported period rows, omits exact-case ASM_SETUP_CSV_METADATA.xml, omits or fails to support an exported task-scoped CSV member, has invalid keys, or exceeds approved row scope | Rebuild a delta-only FSM package from the fresh same-task export with approved rows in every task-scoped CSV member | Yes |
| Create | Blocker | verify_repeating_time_periods_fsm_export | The derived PeriodCd already exists in the fresh same-task export | Select a distinct Name that derives a PeriodCd absent from the fresh export | Yes |
| Edit | Blocker | verify_repeating_time_periods_fsm_export | Current Name does not match exactly one row in the fresh same-task export | Provide the existing Repeating Time Period Current Name and refresh the export | Yes |
| Edit | Blocker | verify_repeating_time_periods_fsm_export | The change includes a field other than Name or Description, or changes PeriodCd or GroupingKey | Rebuild from the matched fresh-export rows; change only Name and/or Description and retain PeriodCd and GroupingKey | Yes |
| Create with one or more exact functional matches | Blocker | find_functionally_matching_repeating_periods | Matching periods have not all been shown, or the user has not explicitly confirmed that a new period is still wanted | Show every matching period with populated UI-exposed fields only, then obtain the user's explicit continue-or-cancel decision | Yes |
| An import route is selected | Blocker |  | The package is converted to an HCM Data Loader archive or sent through direct Fusion REST mutation | Use the validated FSM ZIP and core.data-loader only | Yes |
| Before the provider-owned approval process | Blocker |  | The Complete Summary is absent; is not generated solely from verified structured UI fields after validation, lookup resolution, and defaulting; omits a populated user value or an actually applied default; includes a non-UI, blank, null, unused, metadata-only, or technical value; or renders an empty child section | Regenerate the business-only Complete Summary, then continue to the existing provider-owned approval process | Yes |
| An import is about to be submitted | Blocker |  | The immutable preview or explicit approval is missing or stale | Obtain approval for the current immutable preview | Yes |
| An import outcome is failed, partial, timed out, or uncertain | Blocker |  | An automatic retry is proposed | Preserve diagnostics, reconcile current state, and stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_repeating_time_periods_fsm_export | Create or edit; edit additionally requires Current Name | Fresh export evidence; for edit, exactly one Current Name match and current exported values | ora_reference_lookups.md |
| find_functionally_matching_repeating_periods | Create after validation and defaulting | Every exact functional match, displayed with populated UI-exposed values, and the user's explicit continue-or-cancel decision | ora_reference_lookups.md |

## Complete Summary Requirements

Generate the Complete Summary only from verified structured UI fields after validation, lookup resolution, and defaulting. Always generate it without warnings, diagnostics, or technical notes. Preserve technical values internally for validation and provider execution; never display them in the summary.

| Requirement | What Must Be Shown or Omitted |
|---|---|
| User-provided values | Include every populated user-provided UI value using its business label and verified business display value. |
| Applied defaults | Include every default that was actually applied in Defaults Applied. Do not render Defaults Applied when no default was applied. |
| Blank and metadata-only values | Omit blank, null, unused, and metadata-only values. |
| UI field boundary | Show only the UI-exposed fields listed below. Do not include any export-only, provider-only, or derived implementation value. |
| Child records | Add a child section only when it contains populated values; use business labels only. |
| Identifiers and technical values | Never display IDs, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, or technical file names. |
| Display translations | Translate an ID to its resolved business display name, a code to its verified business meaning, true or false to Selected or Not selected, Enabled or Disabled, or Yes or No, and an internal status to a business-friendly status such as Draft or Submitted when a verified label is available. |

| UI-exposed field | Include When |
|---|---|
| Name | A value is populated. |
| Description | A value is populated. |
| Period Usage | One or more usages are selected. |
| Period Type | A value is selected or defaulted. |
| Period Length | A value is selected for Daily, Monthly, or Weekly. |
| Number of Days | Daily with More than one day is selected. |
| Number of Weeks | Weekly with More than two weeks is selected. |
| Sample Start Date | A value is populated for the selected period definition. |
| Start Day | A value is populated for a Weekly period definition. |

Render the populated sections in this format:

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RTP.ENFORCE_FSM_SAFETY | decision | 50 | design_enforcement | passed->RTP.GENERATE_COMPLETE_SUMMARY;blocked->RTP.BLOCKED | RTP.CHECK_FSM_READINESS | stop | Before an FSM ZIP is routed for immutable preview or import |
| RTP.CONFIRM_CREATE_AFTER_MATCHES | decision | 36 | design_enforcement | confirmed->RTP.CHECK_FSM_READINESS;declined->RTP.CREATE_CANCELLED;blocked->RTP.BLOCKED | RTP.CHECK_FUNCTIONAL_MATCHES | stop | Create when one or more exact functional matches are found; show every match and ask whether a new period is still wanted |
| RTP.GENERATE_COMPLETE_SUMMARY | step | 55 | design_enforcement | summarized->RTP.FSM_EXECUTION_GATE;blocked->RTP.BLOCKED | RTP.ENFORCE_FSM_SAFETY | stop | After validation, lookup resolution, defaulting, and FSM safety enforcement; before the provider-owned approval process |
