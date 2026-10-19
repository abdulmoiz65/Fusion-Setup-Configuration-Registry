# Recruiting Agencies Reference Lookups

## Purpose

Defines the only permitted local-export and enabled common-lookup resolution contracts. Lookup operations are read-only.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_fresh_agency_export | Before Retrieve, Create, Update, package generation, or reconciliation | Intended target, fresh immutable task export, ASM metadata, and ORA_IRC_RECRUITING_AGENCIES.csv | Require exact task identity ORA_IRC_MANAGE_AGENCIES, target consistency, usable completion evidence, one case-sensitive ASM_SETUP_CSV_METADATA.xml member, the verified agency CSV header, and a current fingerprint | Verified target, agency rows, CSV header, metadata, export time, and source fingerprint | Missing, stale, wrong-target, malformed, partial, or ambiguous evidence returns BLOCKED |
| verify_agency_identity | Create or Update | Exact Agency Name and rows from verify_fresh_agency_export | Compare Agency Name exactly without inferred case or whitespace normalization. Create requires zero exact matches. Update requires exactly one | ABSENT or PRESENT classification and the exact exported row for Update | Create match returns ALREADY_EXISTS; Update zero returns NOT_FOUND; Update multiple returns AMBIGUOUS_AGENCY |
| verify_agency_status | Status is supplied or an Update omits Status | Supplied Status or exact exported agency row | Accept only a target-release status value evidenced by the fresh export; preserve exported StatusCode when Update omits it | Validated StatusCode | Unmatched or ambiguous supplied Status returns INVALID_STATUS |
| verify_candidate_agency_zip | A candidate package is previewed or handed to core.data-loader | Immutable candidate ZIP, task identity, target, operation, Agency Name, effective values, SHA-256, and approval | Require exactly one case-sensitive ASM metadata member, the verified agency CSV, no unverified child data, and approval matching the unchanged fingerprint and target | Validated immutable ZIP and approval receipt | Any mismatch, mutation, stale approval, or unverified member returns BLOCKED |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_referral_type | Referral Type is required or supplied | User-provided code or text | core.fusion-api.apps-common.lookups with lookup type ORA_IRC_AGENCY_TYPE | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Match exactly one currently enabled LookupCode or Meaning | Referral Type LookupCode and Meaning | Return INVALID_LOOKUP_VALUE for Referral Type; do not substitute |
| resolve_contract_type | Contract Type is supplied | User-provided code or text | core.fusion-api.apps-common.lookups with lookup type ORA_IRC_AG_CONTRACT_TYPE | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Match exactly one currently enabled LookupCode or Meaning | Contract Type LookupCode and Meaning | Return INVALID_LOOKUP_VALUE for Contract Type; do not substitute |
| resolve_exclusivity_length | Exclusivity Length is supplied or Referral Type is Person Specific | User-provided code or text | core.fusion-api.apps-common.lookups with lookup type ORA_IRC_AG_EMBARGO_PERIOD | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Match exactly one currently enabled LookupCode or Meaning and require it for Person Specific | Exclusivity Length LookupCode and Meaning | Return EXCLUSIVITY_REQUIRED when absent for Person Specific, otherwise INVALID_LOOKUP_VALUE; do not substitute |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| User supplies a key or code | Match it exactly against one currently enabled LookupCode |
| User supplies text | Match it exactly against one currently enabled Meaning |
| Value is disabled, inactive, unmatched, or ambiguous | Reject the named field with a customer-friendly correction; never choose a substitute |
| Common lookup access fails or is unauthorized | Return PROCESS_FAILED or an authorization outcome; do not claim the value is absent |
| Fresh export identity is incomplete | Stop before duplicate checking, package generation, or import |
| Lookup receipt | Keep source, match, mapped code, and sanitized evidence internally; expose only the business result by default |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.VERIFY_EXPORT_ROUTE | decision | 25 | evaluate_result | ready->RA.DONE_RETRIEVE;blocked->RA.HANDLE_ISSUES;failed->RA.HANDLE_ISSUES | RA.VALIDATE_REQUEST | stop | Retrieve |
| RA.RESOLVE_REFERENCES | decision | 30 | evaluate_result | create->RA.VERIFY_CREATE_IDENTITY;update->RA.VERIFY_UPDATE_IDENTITY;import->RA.CHECK_DEPENDENCIES;invalid->RA.HANDLE_ISSUES;ambiguous->RA.HANDLE_ISSUES;failed->RA.HANDLE_ISSUES | none | stop | Create, Update, or Import |
