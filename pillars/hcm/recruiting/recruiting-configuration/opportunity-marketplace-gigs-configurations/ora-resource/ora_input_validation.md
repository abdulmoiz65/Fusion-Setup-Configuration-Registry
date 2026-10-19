# Opportunity Marketplace Gigs Configurations Input Validation

Source: Opportunity Marketplace Gigs Configurations SKILL.md and FSCR — Opportunity Marketplace Gigs Configuration.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | SiteCode and SiteName | Stop | Provide a nonblank configuration code and configuration name | Creating a Gig Configuration directly | |
| Copy identity | Source configuration; optional SiteCode and SiteName | Stop | When both identity fields are omitted, display `Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Gig configuration. I am proposing the following values: <source_code>_copy and <source_name>_copy.` Require approval or both replacement values, then require an eligibility-profile selection | Copying a Gig Configuration | derive_copy_identity_and_filters |
| Eligibility profile selection | EligibilityName | List unused profiles | When omitted or already assigned, list active unused Opportunity Marketplace eligibility profiles and require the user to select one | Creating a Gig Configuration | list_active_unused_opp_marketplace_eligibility_profiles |
| Configuration values | SiteType with value GIG | Stop | Provide SiteType GIG; the workflow derives SequenceOrder from the fresh export | Creating a Gig Configuration | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Required create fields are present | Input identity is complete | Obtain the fresh task export before resolving references or checking identity | verify_fresh_gig_configuration_export |
| EligibilityName is omitted or already assigned in the fresh export | Eligibility selection is required | List active unused Opportunity Marketplace eligibility profiles and wait for the user to select one | list_active_unused_opp_marketplace_eligibility_profiles |
| An optional location, organization, job family, or job function is supplied | Reference validation is required | Resolve every supplied availability-context value exactly; stop on no or multiple matches | |
| SiteCode and EligibilityName are ready for identity checks | Current configuration rows are required | Compare the values with the fresh export before package generation | verify_fresh_gig_configuration_export |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported operation | Accept read, list, export, or creation of a new configuration only. Reject edit, activation, deactivation, delete, and sequence-change requests. | Every request | |
| SiteCode required and length | Require a nonblank SiteCode. When it exceeds 200 characters, retain only its first 200 characters, report the truncation, and use the retained value for all later checks and CSV rows. | Creating a Gig Configuration | |
| SiteName required and length | Require a nonblank SiteName. When it exceeds 100 characters, retain only its first 100 characters, report the truncation, use it in all CSV rows including translations, and confirm the retained value remains nonblank. | Creating a Gig Configuration | |
| Copy code and name | If both fields are omitted, derive `<source_code>_copy` and `<source_name>_copy`, display `Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Gig configuration. I am proposing the following values: <source_code>_copy and <source_name>_copy.`, then require approval or both replacement values and an eligibility-profile selection. If both are supplied, use them. Apply normal length and uniqueness validation. Do not copy the source eligibility profile. | Copying a Gig Configuration | derive_copy_identity_and_filters |
| SiteType | Accept only GIG. | Creating a Gig Configuration | |
| Eligibility profile | Require exactly one active Opportunity Marketplace eligibility profile before package generation. When omitted or already assigned, list active unused profiles and require a selection. | Creating a Gig Configuration | list_active_unused_opp_marketplace_eligibility_profiles |
| Location | Require exactly one matching location and a proven geography-element serialization tuple when a location is supplied. Do not place the LOV `CountryCode` in an element-value column or use generic `en` in an element-language column. | A location is supplied | resolve_recruiting_location |
| Organization | Require exactly one matching Recruiting organization when an organization is supplied. | An organization is supplied | resolve_recruiting_organization |
| Job family | Require exactly one matching active, effective job family when a job family is supplied. | A job family is supplied | resolve_active_job_family |
| Job function | Require exactly one matching active, effective job function when a job function is supplied. | A job function is supplied | resolve_active_job_function |
| Availability-context identifiers | Generate a new unique 32-character uppercase hexadecimal identifier for the new context and every supplied child-filter row. Reuse only the new parent `ObjectCxtCode` in required child relationship columns. | Before package generation | generate_new_gig_availability_context_identifiers |
| Copied filters | Copy source locations, organizations, job families, and job functions only; resolve each copied business value using the current LOV before package generation. | Copying a Gig Configuration | derive_copy_identity_and_filters |
| SiteCode uniqueness | Stop if the retained SiteCode matches an existing configuration. | Before package generation | find_existing_gig_configuration_by_site_code |
| Eligibility-profile uniqueness | Stop if the resolved EligibilityName is already assigned to an existing configuration. | Before package generation | find_gig_configuration_by_eligibility_profile |
| SequenceOrder derivation | Ignore a copied or supplied SequenceOrder and derive the next value as one greater than the highest current SequenceOrder. Stop if the current maximum cannot be established from the fresh export. | Before package generation | derive_next_gig_configuration_sequence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GC.VALIDATE_REQUEST | decision | 10 | validate_input | valid->GC.EXPORT_CURRENT;invalid->GC.RETURN_ISSUES | none | stop | A Gig Configuration request is supplied |
| GC.VALIDATE_IDENTITY | decision | 40 | validate_input | valid->GC.GENERATE_PACKAGE;invalid->GC.RETURN_ISSUES | GC.VALIDATE_REFERENCES | stop | A new Gig Configuration has passed reference validation |
