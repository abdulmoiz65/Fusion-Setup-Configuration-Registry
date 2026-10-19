# Payroll Definitions Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| PlannedSubmissionFixedDate | Append 00:00:00 to the valid supplied YYYY/MM/DD date, producing YYYY/MM/DD HH24:MI:SS | A valid date without a supplied time is provided | No; preserve a supplied time only when it exactly matches HH24:MI:SS | |
| ConsolidationSetCode | Use the same exact value supplied in ConsolidationSetName, Name, Consolidation Group, or Consolidation Group Name | ConsolidationSetCode is absent and one listed name alias is supplied | No; derive automatically, continue execution, and do not prompt for the code | resolve_consolidation_group_or_set_by_ldg |
| OrganizationPaymentMethodCode | Use the same exact value supplied in Organization Payment Method Name, OrgPaymentMethodName, or BaseOrgPayMethodName | OrganizationPaymentMethodCode is absent and one listed name alias is supplied | No; derive automatically, continue execution, and do not prompt for the code; use the resolved target-supported code or ID reference form for the final HDL field | resolve_organization_payment_method_by_ldg_and_date |

Do not default invalid dates or invalid times. The final value must be in YYYY/MM/DD HH24:MI:SS format.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PD.APPLY_DEFAULTS | decision | 4 | apply_default | applied->PD.ENFORCE_DESIGN;skipped->PD.ENFORCE_DESIGN;invalid->PD.HANDLE_ERROR | PD.RESOLVE_REFERENCES | stop | PlannedSubmissionFixedDate needs start-of-day defaulting, or ConsolidationSetCode or OrganizationPaymentMethodCode is absent while its documented name alias is supplied |

## Sources

- Developer-provided Planned Submission Fixed Date defaulting requirements, accessed 2026-08-14.
