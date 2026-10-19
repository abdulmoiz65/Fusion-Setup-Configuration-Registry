# Recruiting Agencies Input Validation

## Purpose

Defines the request, agency-field, identity, and package-input checks that must pass before lookup resolution or candidate package generation.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Retrieve, Create, Update, or Import | Stop with MISSING_OPERATION | State one supported operation | Every request | |
| Agency identity | Agency Name | Stop with MISSING_REQUIRED_AGENCY | Provide the exact Agency Name | Create or Update | verify_agency_identity |
| Create fields | Referral Type and Main Contact | Stop with MISSING_REQUIRED_AGENCY | Provide the missing agency field | Create | resolve_referral_type |
| Update change | At least one supported agency field | Stop with MISSING_UPDATE_VALUE | Provide one field to change | Update | |
| Exclusivity | Exclusivity Length code or meaning | Stop with EXCLUSIVITY_REQUIRED | Provide an enabled Exclusivity Length | Resulting Referral Type is Person Specific | resolve_exclusivity_length |
| Import artifact | Candidate ZIP, target environment, operation, Agency Name, SHA-256, and matching approval | Stop with BLOCKED | Approve the exact immutable preview | Import | verify_candidate_agency_zip |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Retrieve is requested | Inputs accepted | Obtain and verify a fresh task-level export | verify_fresh_agency_export |
| Create or Update fields are present | Inputs accepted | Resolve each applicable lookup and exact Agency Name identity | verify_agency_identity |
| Contract Type is supplied | Conditional input accepted | Resolve one enabled exact code or meaning | resolve_contract_type |
| Create omits Status | Input accepted | Apply the documented ORA_ACTIVE default | |
| Update omits Status | Input accepted | Preserve exported StatusCode | verify_agency_identity |
| Allow Internal Candidate Search is supplied | Unsupported agency option | Return UNSUPPORTED_AGENCY_OPTION and direct the user to Fusion | |
| An agent, deletion, direct REST, or database operation is requested | Unsupported | Return UNSUPPORTED and stop | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Agency Name identity | Compare the supplied name exactly against a fresh target export; do not infer case or whitespace normalization | Create or Update | verify_agency_identity |
| Create identity | Zero exact matches is required; any exact match returns ALREADY_EXISTS | Create | verify_agency_identity |
| Update identity | Exactly one exact match is required; zero returns NOT_FOUND and more than one returns AMBIGUOUS_AGENCY | Update | verify_agency_identity |
| Referral Type | Accept exactly one currently enabled ORA_IRC_AGENCY_TYPE LookupCode or Meaning | Create or supplied Update | resolve_referral_type |
| Contract Type | Accept exactly one currently enabled ORA_IRC_AG_CONTRACT_TYPE LookupCode or Meaning | When supplied | resolve_contract_type |
| Exclusivity Length | Accept exactly one currently enabled ORA_IRC_AG_EMBARGO_PERIOD LookupCode or Meaning; require it for Person Specific | When supplied or required | resolve_exclusivity_length |
| Main Contact | Require a nonblank value for Create; preserve it for Update unless explicitly changed | Create or Update | |
| Agency Email | Require a syntactically valid email address | When supplied | |
| Create job application on behalf of candidate | Accept only Y or blank according to the verified export | When supplied | |
| Notes or Address | Accept optional free text in the verified agency column only | When supplied | |
| Status | For Create, accept a target-proven value or default omitted Status to ORA_ACTIVE; for Update preserve exported StatusCode unless explicitly replaced by a validated value | Create or Update | verify_agency_status |
| Update preservation | Preserve every unmodified exported agency field and all verified package metadata | Update | verify_fresh_agency_export |

## Retrieve Projection

Read values by exact CSV header name, never by column position, visual order, or inferred value type.

| Customer-facing field | Required CSV header | Projection rule |
|---|---|---|
| Agency Name | `AgencyName` | Return the agency name unchanged |
| Main Contact | `AgencyContact` | Return the contact person's name; never substitute `AgencyEmail` |
| Agency Email | `AgencyEmail` | Return the agency email address; never substitute `AgencyContact` |
| Status | `StatusCode` | Return the resolved status meaning when available |
| Referral Type | `AgencyTypeCode` | Resolve the code to its current enabled meaning |
| Contract Type | `ContractTypeCode` | Resolve the code to its current enabled meaning |
| Notes or Address | `AgencyNotes` | Return the text unchanged |
| Exclusivity Length | `EmbargoPeriodCode` | Resolve the code to its current enabled meaning |
| Inactivation Date | `InactivationDate` | Return the exported date when present |
| Deletion Date | `DeletionDate` | Return the exported date when present |
| Create job application on behalf of candidate | `CreateJaFlag` | Display `Y` as Yes and blank as No |

If any requested field's required header is absent or duplicated, return `BLOCKED` and identify the unavailable field. Do not guess, shift columns, or infer a mapping from whether a value resembles a name or email address.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.VALIDATE_REQUEST | decision | 10 | validate_input | retrieve->RA.VERIFY_EXPORT_ROUTE;create->RA.APPLY_STATUS_DEFAULT;update->RA.RESOLVE_REFERENCES;import->RA.RESOLVE_REFERENCES;invalid->RA.HANDLE_ISSUES;unsupported->RA.HANDLE_ISSUES | none | stop | Every Recruiting Agencies request |
| RA.VERIFY_CREATE_IDENTITY | decision | 40 | evaluate_result | unique->RA.CHECK_DEPENDENCIES;existing->RA.HANDLE_ISSUES;ambiguous->RA.HANDLE_ISSUES | RA.RESOLVE_REFERENCES | stop | Create |
| RA.VERIFY_UPDATE_IDENTITY | decision | 45 | evaluate_result | found->RA.CHECK_DEPENDENCIES;not_found->RA.HANDLE_ISSUES;ambiguous->RA.HANDLE_ISSUES | RA.RESOLVE_REFERENCES | stop | Update |
