# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Geocoding setup | Treat Geocoding Defined as Fusion configuration that controls which countries are processed; do not ask the user to confirm it before submission |
| 2 | Eligible addresses | Treat active and verified status as Fusion selection criteria; do not require a separate user confirmation |
| 3 | ESS access | Use an account with Application Implementation Consultant or Run Geocode Loader privilege; let Fusion enforce access at submission |
| 4 | Core ESS capability | Route submission and status tracking through core.fusion-api.ess-job-submitter |
| 5 | Execution intent | Use the user's direct run request as authorization for one submission |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GEOCODE.SETUP | Country geocoding setup | No | Every new submission | Selection criteria | Manage Geographies configuration | fusion_job_selection | The scheduled process operates only on countries configured for geocoding | Enable Geocoding Defined when a country must be included; no pre-run user confirmation is required | configured_country_scope |
| GEOCODE.ADDRESSES | Active verified addresses | No | Every new submission | Selection criteria | Oracle geocoding process behavior | fusion_job_selection | Inactive or unverified locations aren't selected; zero selected rows is a valid functional outcome | Make addresses active and verified when they need geocoding | selected_location_count |
| GEOCODE.ACCESS | ESS submission privilege | Yes | Every new submission | Runtime enforcement | Fusion authorization response | ess_access_check | The user must be allowed to submit HZ-HZGEOCODER | Use Application Implementation Consultant or a role containing Run Geocode Loader | authorization_result |
| GEOCODE.CORE | ESS Job Submitter | Yes | Submission or tracking | Satisfied | Repository core skill | core_ess_submitter | Avoid duplicate authentication, submission, and polling logic | Use the repository core ESS capability | requestId, status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required readiness and direct execution intent are available | Yes |
| Verify | A prerequisite needs a read-only configured-environment check | Yes for read-only checks |
| Blocked | The target environment is not established or Fusion rejects access | No |
| Execution-intent blocker | The request is advisory, hypothetical, or ambiguous about running | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.READINESS | decision | 4 | resolve_dependency | ready->GEOCODE.PREVIEW;blocked->GEOCODE.BLOCKED;failure->GEOCODE.FAILED | GEOCODE.DEFAULTS | stop | Resolve environment and core capability; disclose country and address selection behavior plus runtime access behavior without asking for setup confirmation |
