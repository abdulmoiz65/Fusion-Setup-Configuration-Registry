# Enrollment Authorizations Reference Lookups

## Conditional Read-Only Checks

For each included `benefitLegalDisclaimers` row, check only the names actually
supplied. Use `core.fusion-api.rest-api-client` against the selected environment
only when the active project workflow selects read-only reference validation.
Send `REST-Framework-Version: 9`. These checks validate names without changing
the supplied values, selecting HDL IDs, or authorizing a load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_program_name | `benefitLegalDisclaimers.ProgramName` | `GET /hcmRestApi/resources/11.13.18.05/benefitProgramsLOV?q=Name='<ProgramName>'` | Require one distinct returned row whose `Name` exactly equals the supplied ProgramName. | Validation status only; preserve ProgramName. |
| resolve_plan_name | `benefitLegalDisclaimers.PlanName` | `GET /hcmRestApi/resources/11.13.18.05/benefitPlansLOV?q=Name='<PlanName>'` | Require one distinct returned row whose `Name` exactly equals the supplied PlanName. | Validation status only; preserve PlanName. |

Send each supplied name as the `q=Name` equality predicate. URL-encode the
complete query parameter and escape apostrophes using the endpoint's
documented query syntax. When that exact row has a supplied, validated
`StartDate`, send it as the endpoint's `effectiveDate` parameter in
`YYYY-MM-DD`; do not borrow a parent or sibling date or substitute today's
date. Compare every returned `Name` again for exact equality, including case.
Read all result pages before deciding zero (`invalid`), one (`valid`), or
multiple distinct exact matches (`ambiguous`). Do not select the first
candidate or overwrite a supplied name.

If a name is absent, skip its lookup without an error. An HTTP 403 records
`unverified_forbidden` for only the affected row and field: do not fail field
validation, mark the value invalid, or stop the other lookup. It does not
prove the name valid; obtain access or another workflow-approved authoritative
verification before live load. A 401 may use the selected client's permitted
one-time cached-token refresh; classify a remaining denial as auth/authz.
Classify other request failures separately, without turning them into no
matches. If no read-only lookup route is active, record a workflow blocker;
do not call REST directly or silently mark a name valid.

Oracle REST contracts: [benefitProgramsLOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-benefitprogramslov-get.html) and [benefitPlansLOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-benefitplanslov-get.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENROLL_AUTH.LOOKUP_PROGRAM | decision | 12 | reference_lookup | matched->ENROLL_AUTH.LOOKUP_PLAN;skipped->ENROLL_AUTH.LOOKUP_PLAN;forbidden->ENROLL_AUTH.LOOKUP_PLAN;invalid->ENROLL_AUTH.HANDLE_ISSUE | ENROLL_AUTH.VALIDATE_REQUEST | continue | Validate supplied benefitLegalDisclaimers.ProgramName against benefitProgramsLOV Name; 403 records unverified_forbidden |
| ENROLL_AUTH.LOOKUP_PLAN | decision | 14 | reference_lookup | matched->ENROLL_AUTH.GATE_EXECUTION;skipped->ENROLL_AUTH.GATE_EXECUTION;forbidden->ENROLL_AUTH.GATE_EXECUTION;invalid->ENROLL_AUTH.HANDLE_ISSUE | ENROLL_AUTH.LOOKUP_PROGRAM | continue | Validate supplied benefitLegalDisclaimers.PlanName against benefitPlansLOV Name; 403 records unverified_forbidden |
