# Opportunity Marketplace Jobs Configurations Input Validation

Source: Opportunity Marketplace Jobs Configurations SKILL.md, adapted from the approved Gig Configuration create and copy contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | SiteCode, SiteName, EligibilityName | Stop | Provide a nonblank configuration code, configuration name, and eligibility-profile name | Creating a Job Configuration directly | |
| Copy identity | Source configuration and EligibilityName; optional SiteCode and SiteName | Stop | When both identity fields are omitted, display the mandatory-values proposal for `<source_code>_copy` and `<source_name>_copy`, then require approval or both replacement values; require a nonblank eligibility-profile name | Copying a Job Configuration | derive_copy_identity_and_filters |
| Configuration values | SiteType value proven by the fresh Jobs export | Stop | Use the SiteType retained by the current Jobs package; the workflow derives SequenceOrder from the fresh export | Creating a Job Configuration | verify_fresh_job_configuration_export |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Required create fields are present | Input identity is complete | Obtain the fresh task export before resolving references or checking identity | verify_fresh_job_configuration_export |
| EligibilityName is omitted or already assigned in the fresh export | Eligibility selection is required | List active unused Opportunity Marketplace eligibility profiles and wait for the user to select one | list_active_unused_opp_marketplace_eligibility_profiles |
| An optional location, organization, job family, job function, or Recruiting Type is supplied | Reference validation is required | Resolve every supplied availability-context value exactly; stop on no or multiple matches | |
| SiteCode and EligibilityName are ready for identity checks | Current configuration rows are required | Compare the values with the fresh export before package generation | verify_fresh_job_configuration_export |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported operation | Accept read, list, export, or creation of a new configuration only. Reject edit, activation, deactivation, delete, and sequence-change requests. | Every request | |
| SiteCode required and length | Require a nonblank SiteCode. When it exceeds 200 characters, retain only its first 200 characters, report the truncation, and use the retained value for all later checks and CSV rows. | Creating a Job Configuration | |
| SiteName required and length | Require a nonblank SiteName. When it exceeds 100 characters, retain only its first 100 characters, report the truncation, use it in all CSV rows including translations, and confirm the retained value remains nonblank. | Creating a Job Configuration | |
| Copy code and name | If both fields are omitted, display: Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Job configuration. I am proposing the following values: `<source_code>_copy` and `<source_name>_copy`. Require approval or both replacement values. If both are supplied, use them. Apply normal length and uniqueness validation. Do not copy the source eligibility profile. | Copying a Job Configuration | derive_copy_identity_and_filters |
| Eligibility profile | Require a nonblank EligibilityName and exactly one active Opportunity Marketplace eligibility profile. | Creating a Job Configuration | resolve_active_opp_marketplace_eligibility_profile |
| Eligibility-profile selection | When EligibilityName is omitted or already assigned, list every active unused Opportunity Marketplace profile and require a selection; do not select one automatically. | Creating or copying a Job Configuration | list_active_unused_opp_marketplace_eligibility_profiles |
| Location | Require exactly one matching location and a proven geography-element serialization tuple when a location is supplied. Do not place the LOV `CountryCode` in an element-value column or use generic `en` in an element-language column. | A location is supplied | resolve_recruiting_location |
| Organization | Require exactly one matching Recruiting organization when an organization is supplied. | An organization is supplied | resolve_recruiting_organization |
| Job family | Require exactly one matching active, effective job family when a job family is supplied. | A job family is supplied | resolve_active_job_family |
| Job function | Require the user-supplied exact active, effective LOV display Meaning to resolve to exactly one job function; retain its LookupCode only for the FSM child row. | A job function is supplied | resolve_active_job_function |
| Recruiting Type | Require the user-supplied exact LOV display Meaning to resolve to exactly one Recruiting Type; retain its LookupCode only for the FSM child row. | A Recruiting Type is supplied | resolve_recruiting_type |
| Availability-context identifiers | Generate a new unique 32-character uppercase hexadecimal identifier for the new context and every supplied child-filter row. Reuse only the new parent ObjectCxtCode in required child relationship columns. | Before package generation | generate_new_job_availability_context_identifiers |
| Copied filters | Copy source locations, organizations, job families, job functions, and Recruiting Types only; resolve each copied business value using the current LOV before package generation. | Copying a Job Configuration | derive_copy_identity_and_filters |
| SiteCode uniqueness | Stop if the retained SiteCode matches an existing configuration. | Before package generation | find_existing_job_configuration_by_site_code |
| Eligibility-profile uniqueness | Stop if the resolved EligibilityName is already assigned to an existing configuration. | Before package generation | find_job_configuration_by_eligibility_profile |
| SequenceOrder derivation | Ignore a copied or supplied SequenceOrder and derive the next value as one greater than the highest current SequenceOrder. Stop if the current maximum cannot be established from the fresh export. | Before package generation | derive_next_job_configuration_sequence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JC.VALIDATE_REQUEST | decision | 10 | validate_input | valid->JC.EXPORT_CURRENT;invalid->JC.RETURN_ISSUES | none | stop | A Job Configuration request is supplied |
| JC.VALIDATE_IDENTITY | decision | 40 | validate_input | valid->JC.DERIVE_REC_TYPE_DEFAULT;invalid->JC.RETURN_ISSUES | JC.VALIDATE_REFERENCES | stop | A new Job Configuration has passed reference validation |
