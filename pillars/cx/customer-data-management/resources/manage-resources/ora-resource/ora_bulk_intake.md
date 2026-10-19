# ResourceUser Import Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| CX ZIP or direct CSV group | Resource attributes mapped to Resource object attributes, with an optional CX mapping CSV | Data Loader validates, uploads, and initiates the submitted ResourceUser CX import. |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| New resource identity | FirstName, LastName, BusinessUnit, LegalEntity, ResourceEmail | Required values are validated before import. |
| Existing resource key | ResourcePartyNumber | Identifies an existing resource for update. |
| Organization membership role | Organization and Role | Map Role to ResourceOrgRoleCode unless the role is explicitly individual. |
| Explicit individual role | Role marked individual | Map Role to IndividualRoleCode. |
| Ambiguous role | Role without Organization or explicit individual designation | Block the row until role-routing context is supplied. |
| Phone detail | RawWorkPhoneNumber, RawMobilePhoneNumber, RawFaxNumber and matching country code | Require the matching country code when the raw number is provided. |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Mapping review | Review automatic source-to-target mapping and edit it when required. |
| Data validation | Validate data for unmapped columns and format issues before submission. |
| Sampled BusinessUnit lookup | After mapping, inspect only the first 10 non-header rows. Collect distinct nonblank values from the source column mapped to `BusinessUnit` and submit one exact `hcmBusinessUnitsLOV` `Name IN (...)` lookup. Require exactly one result per value; do not validate later rows. |
| Sampled LegalEntity lookup | After mapping, inspect only the first 10 non-header rows. Collect distinct nonblank values from the source column mapped to `LegalEntity` and submit one exact current-effective `legalEmployersLov` `Name IN (...)` lookup. Require exactly one result per value; do not validate later rows. |
| Role routing | Confirm each Role maps to ResourceOrgRoleCode when Organization is supplied, or to IndividualRoleCode only when explicitly designated individual. |
| Active role-code lookup | Use only the first 10 non-header CSV rows. Query active Resource Roles and require every distinct ResourceOrgRoleCode or IndividualRoleCode in that sample to match a returned RoleCode. Report only unresolved sampled codes and routing context; do not submit when any are unresolved. |
| Parent dependency order | Keep parent ResourceUser rows before rows that reference them; a correctly ordered dependency chain may remain in one CSV. |
| Live submission | Submit only after review and explicit approval. |
| Post-import processing | Only after an explicitly requested Data Loader status check confirms completion, classify reporting-hierarchy changes and new resources with user accounts before preparing eligible ESS requests. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_BULK | step | 8 | process_bulk | prepared->MR.IMPORT_DESIGN;invalid->MR.STOP | MR.IMPORT_DEPENDENCIES | stop | A CSV import source is ready for mapping and data validation. |
