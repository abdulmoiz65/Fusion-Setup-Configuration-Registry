# Enrollment Authorizations Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, Update, Delete, or Read or verify | Block a data-changing preflight | Supply one supported operation | Every request | |
| HDL object route | benefitLegalDisclaimers | Block before preflight | Use the task-mapped object; do not substitute another object | Every request | |
| Current HDL sample | Current benefitLegalDisclaimers Data Loader sample | Block artifact preparation | Generate or retrieve the current sample | Create, Update, or Delete | |
| Immutable load artifact | A preflighted DAT or ZIP derived from the current sample | Block upload or initiation | Correct the source and rerun preflight | Create, Update, or Delete | |
| Record identity | User key or identifier accepted by the current sample | Block the mutation | Supply the missing identity values; do not invent an identifier | Update or Delete | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Create, Update, or Delete request names benefitLegalDisclaimers | Continue only after current-sample validation and immutable Data Loader preflight | Continue to the approval gate | |
| The source filename, section, header, action, or attributes differ from the current sample | Block the mutation | Rebuild the artifact from the current sample | |
| The requested operation does not have a supported identity or action in the current sample | Block the mutation | Obtain supported source values or choose a supported operation | |
| The request proposes CSV as a substitute import route | Block the mutation | Use the selected HDL route through core.data-loader | |
| A row supplies ProgramName or PlanName | Validate each supplied field against its selected read-only LOV | Record valid, invalid, ambiguous, or unverified_forbidden per row and field | |
| A supplied name's LOV returns 403 | Do not fail field validation or mark the name invalid; record unverified_forbidden | Continue independent checks; retain unverified status for load readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Object mapping | Accept only benefitLegalDisclaimers for Enrollment Authorizations | Every request | |
| DAT filename | Require the case-sensitive current-sample discriminator filename; reject a suffixed or alternate stem | Create, Update, or Delete | |
| Current schema | Reject a section, header, attribute, action, or record relationship not accepted by the current sample | Create, Update, or Delete | |
| Identity | Require exactly the user key or identifier accepted by the current sample; reject missing or ambiguous identity values | Update or Delete | |
| Date values | Normalize supplied StartDate and EndDate date-only values to YYYY-MM-DD; preserve blank optional EndDate and reject malformed, time-bearing, or timezone-bearing values | Any request with StartDate or EndDate | |
| ProgramName reference | When supplied, require one exact Name match through benefitProgramsLOV using a q=Name predicate; use that row's StartDate as effectiveDate when supplied | Any included benefitLegalDisclaimers row with ProgramName | |
| PlanName reference | When supplied, require one exact Name match through benefitPlansLOV using a q=Name predicate; use that row's StartDate as effectiveDate when supplied | Any included benefitLegalDisclaimers row with PlanName | |
| Artifact integrity | Reject an empty, malformed, changed, or unvalidated DAT or ZIP | Create, Update, or Delete | |
| Unsupported operation | Reject unrecognized operations and unsupported delete or update semantics | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENROLL_AUTH.VALIDATE_REQUEST | decision | 10 | validate_input | valid->ENROLL_AUTH.LOOKUP_PROGRAM;invalid->ENROLL_AUTH.HANDLE_ISSUE | none | stop | Validate the selected operation, mapped HDL object, current-sample artifact, and required record identity before a data-changing load |
