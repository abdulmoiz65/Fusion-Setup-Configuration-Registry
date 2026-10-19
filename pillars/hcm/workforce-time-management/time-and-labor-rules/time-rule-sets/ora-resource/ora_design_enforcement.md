# Time Rule Sets Design Enforcement

Source: User-provided Complete Summary requirements for Time Rule Sets approval.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Complete Summary | Generate the business-only Complete Summary from verified structured values after validation, lookup resolution, and defaulting |
| 2 | Validated package link | Display a clickable link to the exact validated FSM ZIP, outside the Complete Summary |
| 3 | Approval handoff | Transition the completed summary and linked package to the provider-owned approval process |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A validated Time Rule Sets archive is ready for approval | Error |  | A business-only Complete Summary has not been generated from verified structured values, resolved display values, and defaults actually applied | Generate the Complete Summary and Defaults Applied sections before transitioning to the provider-owned approval process | Yes, by regenerating the summary from the verified result set |
| A parent or member archive is ready for approval | Error |  | A clickable link does not identify the exact validated ZIP for this stage | Show the link after the business-only summary and before asking for `approve` | Yes, by rebuilding, validating, and linking the exact ZIP |

## Complete Summary Contract

Generate the Complete Summary only after validation, lookup resolution, and defaulting have produced verified structured values. Always generate it before the provider-owned approval process. Include every user-provided business value and every default actually applied. Omit blank, null, unused, and metadata-only values. Show populated child records only when they have values and use business labels only. Keep implementation-only values internally for validation and provider execution. Do not add warnings, diagnostics, or technical notes.

For Effective Start Date, use exactly one value. When the user supplies a date, show that date in Complete Summary and do not show a default. When no date is supplied, apply Current Date and show it only in Defaults Applied. Never show both values.

Use this exact user-facing structure:

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Display Value Rules

| Value Kind | Display Value |
|---|---|
| Resolved selection | Verified business display name |
| Verified business meaning | Business-friendly meaning |
| Selected setting | Selected, Not selected, Enabled, Disabled, Yes, or No as applicable |
| Lifecycle state | Business-friendly state such as Draft or Submitted |

## Package-Link Approval Gate

For each stage independently, first validate the immutable ZIP against the
fresh export. Then show the business-only Complete Summary. Outside that
summary, display one clickable link to the exact validated ZIP and state the
stage it represents: parent-only or member-only. Request the provider-owned
`approve` only after that link is visible.

The link must identify the same immutable file that Data Loader will upload.
If any row, literal field state, or ZIP member changes, rebuild, revalidate,
and show a new link before requesting approval. Parent approval never covers a
member ZIP.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RULESET.COMPLETE_SUMMARY | step | 6 | design_enforcement | summary_ready->RULESET.PRESENT_VALIDATED_PACKAGE;summary_incomplete->RULESET.DEPENDENCY_ERROR | RULESET.DEPENDENCY | stop | A validated immutable Time Rule Sets archive is ready for the provider-owned approval process |
| RULESET.PRESENT_VALIDATED_PACKAGE | step | 7 | design_enforcement | package_linked->RULESET.IMPORT_HANDOFF_READY;package_missing->RULESET.DEPENDENCY_ERROR | RULESET.COMPLETE_SUMMARY | stop | The exact stage ZIP has passed validation and must be linked before approval |
