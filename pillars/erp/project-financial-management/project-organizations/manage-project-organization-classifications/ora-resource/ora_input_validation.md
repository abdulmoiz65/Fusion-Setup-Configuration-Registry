# Input Validation

**Omitted classification input means preserve existing state.**

Input shape is validated here; state-dependent policy belongs to ora_design_enforcement.md after the governed REST baseline resolves.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Identity | organization_name | Block | Enter exact organization name | Every request | find_existing_project_organization |
| Classification intent | Optional requested_target_classification as PTO, PEO, BOTH or unique nonempty list | Preserve omitted scope | Apply only explicitly requested targets; supplied PTO permissions also express PTO intent | Every request | |
| PTO permissions | Optional indirect, capitalization, billing | New PTO omissions default N; existing PTO omissions preserve through omitted HDL columns | Resolve user Enable/Enabled/Y to Y and Disable/Disabled/N to N; Boolean values remain supported | PTO intent | |
| REST baseline | Complete fresh target-bound exact identity and all classifications | Block | Run organizations REST baseline, never infer absence from a failed read | Every request | find_existing_project_organization |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name | Nonblank max 240; exact name; reject HDL delimiters/control characters | Every request | |
| Permission types | Boolean, Y/N, Enable/Enabled or Disable/Disabled; reject null/unknown names/unsupported values | Supplied permissions | |
| Scope | Bulk existing organizations allowed; no parent creation, date overrides, deletion, replacement or declassification | Every request | |
| Bulk envelope | Exactly target_environment and a nonempty organizations array; each entry uses the single-request fields plus Boolean update_existing_pto_permissions | Bulk request | |
| Bulk uniqueness | Reject duplicate exact organization names, selected parent IDs, baseline references and component source keys | Bulk request | |
| Existing update opt-in | Default false; true requires supplied PTO permissions and REST-confirmed existing PTO; creation values do not implicitly update existing PTO | Bulk request | |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.VALIDATE_INPUT | step | 1 | validate_input | valid->PORGCLASS.APPLY_DEFAULTS;status_requested->PORGCLASS.STATUS_REQUEST_GATE;invalid->PORGCLASS.RETURN_ISSUES | none | stop | For preparation validate single or bulk inputs before reads; for a later explicit status/results/verification request validate the saved project, target, task and per-archive receipt context without requiring a new mutation request |
