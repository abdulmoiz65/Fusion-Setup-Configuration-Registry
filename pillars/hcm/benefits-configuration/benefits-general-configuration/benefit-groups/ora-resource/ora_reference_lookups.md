# Benefit Groups Reference Lookups

## Conditional Legal Employer Check

Run this read-only check for each included `benefitGroups` row that supplies
`LegalEmployer`, only when the active project workflow selects reference
validation through `core.fusion-api.rest-api-client`. Use the selected
environment and `REST-Framework-Version: 9`. A row that supplies only
`LegalEntityId` does not trigger this name lookup; do not infer a name from its
ID. The lookup validates the supplied name without changing it or authorizing
an HDL load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_legal_employer | `benefitGroups.LegalEmployer` | `GET /hcmRestApi/resources/11.13.18.05/legalEmployersLov?q=Name='<LegalEmployer>'` | Require one distinct returned row whose `Name` exactly equals the supplied LegalEmployer. | Validation status only; preserve `LegalEmployer`. |

Send the supplied name in the `q=Name` equality predicate. URL-encode the
complete query parameter and escape apostrophes using the endpoint's
documented query syntax. Compare each returned `Name` again for exact
equality, including case. Follow all response pages before deciding whether
there are zero, one, or multiple distinct matches. Zero is `invalid`; multiple
distinct matches are `ambiguous`; one exact match is `valid`. Do not select the
first candidate or replace the supplied value with an ID.

An HTTP 403 records `unverified_forbidden` for only the affected row and
field. It does not fail field validation, mark the name invalid, or stop
independent checks. It also does not prove the name valid: resolve access or
use another workflow-approved authoritative check before live load. A 401 may
use the selected client's permitted one-time cached-token refresh; classify
a remaining denial as auth/authz. Classify other request failures separately,
without treating them as zero matches. If no read-only workflow route is
active, record a workflow blocker; do not call REST directly or silently mark
the name valid.

Oracle REST contract: [legalEmployersLov](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-legalemployerslov-get.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.LOOKUP_LEGAL_EMPLOYER | decision | 35 | reference_lookup | matched->BEN_GRP.ENFORCE_DESIGN;skipped->BEN_GRP.ENFORCE_DESIGN;forbidden->BEN_GRP.ENFORCE_DESIGN;invalid->BEN_GRP.HANDLE_ISSUE | BEN_GRP.CHECK_READINESS | continue | Validate each supplied benefitGroups.LegalEmployer against legalEmployersLov Name; 403 records unverified_forbidden |
