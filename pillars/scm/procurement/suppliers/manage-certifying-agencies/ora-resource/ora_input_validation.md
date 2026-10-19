# Manage Certifying Agencies Functional Rules

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Data Loader record | A complete current Data Loader template row for the requested create or update | Block configuration | Supply the current task-specific Data Loader template and a complete row. | Create or update | |
| Certifying agency identity | CertifyingAgency for parent PATCH; CertifyingAgency and Description for create | Block configuration | For a parent-only PATCH, supply CertifyingAgency directly and leave CertifyingAgencyId unpopulated. Resolve CertifyingAgencyId only when a child PATCH row or child lookup requires it. | Create or update | list_certifying_agency_candidates |
| Agency lifecycle information | EndDate when supplied | Block association maintenance | Supply an end date later than the as-of date, or leave it blank when the approved Data Loader template permits an open-ended agency. | A business classification is added or changed | |
| Business classification association | A complete, nonempty set of BusinessClassificationCode (export alias ClassificationCode), BusinessClassification, or BusinessClassificationName values | Block the update | Reuse supplied codes or names; resolve every classification before preparing the executable workbook. | Create or update | get_business_classification_lookup_code |
| Existing association child PATCH key | BusinessClassificationId from the current association being replaced | Block the update | Resolve the current child row for the existing BusinessClassificationCode or BusinessClassificationName; do not use a generated sample value or a target lookup value. | Update with a child PATCH row | get_existing_business_classification_associations |
| Unsupported association removal | A request or Data Loader row that removes a current business classification | Block configuration | `businessClassifications` DELETE is not supported by this task's Data Loader contract. Stop and route the request to a separately approved functional process. | Association removal | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Certifying agency record | A parent-only PATCH is keyed directly by CertifyingAgency and needs no name-to-ID lookup. For a child PATCH, resolve an exact CertifyingAgency name to one ID, retrieve that item, and use the ID only in the child row and child lookup. For create, use the collection only to disclose candidates; it does not establish a uniqueness rule. | Create or update | list_certifying_agency_candidates |
| End-date lifecycle | Reject a supplied EndDate earlier than or equal to the request as-of date for association maintenance. | A business classification is added or edited | |
| Business classification identity | Reject a supplied classification that does not resolve to one enabled and effective lookup code, or supplied code/name aliases that disagree. | Create or update with business classifications | get_business_classification_lookup_code |
| Business classification uniqueness and minimum | Reject duplicate codes and an empty requested complete association set. | Create or update with business classifications | |
| Existing association child PATCH key | Reject a child PATCH row unless its BusinessClassificationId resolves to exactly one current association of the selected agency. | Update with a child PATCH row | get_existing_business_classification_associations |
| Unsupported child action | Reject every child `RestAction=DELETE` row. Do not treat a resulting Fusion error as evidence that a missing privilege can make the operation supported. | Association removal | |

## Workbook Population for a Supported Create

Populate the current `certifyingAgencies` Data Loader workbook as follows when creating an agency with an initial business-classification association:

| Workbook Section | Populate | Leave Blank | Constraint |
|---|---|---|---|
| `certifyingAgencies` parent row | `RestAction=POST`, `CertifyingAgency`, and `CertifyingAgencyDescription` when a description is supplied | `CertifyingAgencyId` | The parent create is identified by the supplied agency name. |
| businessClassifications child row | RestAction=POST, CertifyingAgency, and the validated BusinessClassificationCode | CertifyingAgencyId and BusinessClassificationId | Retain the parent-name link; omit the BusinessClassification column from the executable child section to avoid server-side name-to-code derivation. |

Do not fabricate IDs. A child PATCH still requires its current BusinessClassificationId and parent identity from the documented lookups; use the separately validated target BusinessClassificationCode. Keep the classification name as lookup evidence, not as BusinessClassification in the executable child section. Confirm that the live loader contract accepts the code-only child shape before preview; a conflicting contract blocks submission rather than authorizing a name-based fallback or a REST write. Do not create a child DELETE row.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Happens |
|---|---|---|---|---|---|---|---|---|
| POZ.CA.VALIDATE_INPUT | step | 10 | validate_input | valid->POZ.CA.LIST_AGENCY_CANDIDATES;invalid->POZ.CA.RETURN_RESULT | none | stop | Before any certifying-agency create, update, or supported classification association add or change is considered | Validate the current Data Loader template, complete association set, lifecycle date, duplicate-free classification codes, and absence of every child `RestAction=DELETE` row. |
