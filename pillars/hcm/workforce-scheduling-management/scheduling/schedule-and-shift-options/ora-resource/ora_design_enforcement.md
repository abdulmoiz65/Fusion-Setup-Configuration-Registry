# Schedule and Shift Options Design Enforcement

## Source Basis

- Complete Summary and provider-owned approval handoff, user-provided request

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Confirm the requested operation updates one existing setup-option row. |
| 2 | Identity | Use the read-back SetupParamId, not a user-derived or name-derived ID. |
| 3 | Value | Submit only the normalized ParameterValue after the applicable lookup and validation gates pass. |
| 4 | Complete Summary | Generate the required business-only summary from verified structured values after validation, lookup resolution, defaulting, and design enforcement, then hand off to the unchanged provider-owned approval process. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any operation is requested | Error | resolve_current_schedule_common_setups | The request is create, correct, end-date, delete, batch, child maintenance, history, export, or background-load work | Use this task only for a documented item update | No |
| Any update is prepared | Error | resolve_current_schedule_common_setups | SetupParamId was not obtained from the current collection | Read the current row and retain its provider-returned key | No |
| A lookup-backed parameter is updated | Error | resolve_setup_option_common_lookup | The value is not one exact provider-returned LookupCode or the provider reports a gap | Delegate to hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups with the documented exact lookupType | No |
| An update is handed to an execution workflow | Error |  | Preview, exact approval, or an authorized executor is absent | Complete the selected runbook or Data Loader workflow; do not construct a write from ora-resource guidance | No |
| A provider-owned approval is about to begin | Error |  | The Complete Summary is absent; is not generated only from verified structured values; omits a user-provided business value or an actually applied default; includes blank, unused, metadata-only, diagnostic, or technical information; or presents a populated child record without business labels | Regenerate the Complete Summary using the required business-only format, then continue to the unchanged provider-owned approval process | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_current_schedule_common_setups | Every update | SetupParamId and current ParameterValue | ora_reference_lookups.md |
| resolve_setup_option_common_lookup | A Common Lookup-backed parameter is updated | LookupCode | ora_reference_lookups.md |

## Complete Summary Contract

Always generate the Complete Summary only after validation, lookup resolution, defaulting, and design enforcement have succeeded. Build it solely from verified structured values. Keep technical values internally for validation and provider execution.

- Include every user-provided business value and every default that was actually applied.
- Place actually applied defaults only in Defaults Applied.
- Omit blank, null, unused, and metadata-only values. Add a populated child section only when it has values, and use business labels for its records and values.
- Do not add warnings, diagnostics, or technical notes.
- Never put IDs, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, or technical file names in the summary.
- Translate IDs to resolved business display names; codes to verified business meanings; booleans to Selected or Not selected, Enabled or Disabled, or Yes or No; and internal statuses to business-friendly values such as Draft or Submitted.

Use this exact user-facing structure and no additional user-facing content:

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
| SSO.DESIGN | step | 7 | design_enforcement | pass->SSO.COMPLETE_SUMMARY;blocked->SSO.ERROR | SSO.DEFAULTS | stop | Any update request |
| SSO.COMPLETE_SUMMARY | step | 8 | design_enforcement | generated->SSO.EXECUTION_GATE;blocked->SSO.ERROR | SSO.DESIGN | stop | Generate the Complete Summary from verified structured user values and actually applied defaults before provider-owned approval |
