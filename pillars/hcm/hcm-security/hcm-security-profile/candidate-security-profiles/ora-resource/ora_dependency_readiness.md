# Candidate Security Profiles Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fresh Candidate Security Profiles export | Run shared.setup-export.task-level-export for ORA_IRC_CAND_SRCH_SEC_PROFILES against the active configured and authenticated Fusion environment as the first step for every configuration request, including missing-name and protected-only requests, before classification, defaulting, configuration questions, or policy checks; do not request an environment URL |
| 2 | Export identity and completeness | Verify the export completed for the active configured environment and task, contains the metadata plus both expected CSV files, and conforms to their documented relationship |
| 3 | Catalog context agreement | Require the authoritative HCM Security / HCM Security Profile context; stop if a source identifies a conflicting hierarchy |
| 4 | Data-role assignment | Confirm the intended data role has the intended Candidate Security Profile only when validating effective visibility after configuration |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CSP-DEP-005 | Fresh Candidate Security Profiles export baseline | Yes | First step for every configuration request | Verify | Current-run task context produced only through shared.setup-export.task-level-export for ORA_IRC_CAND_SRCH_SEC_PROFILES against the active configured and authenticated Fusion environment | verify_candidate_security_profile_export_baseline | Create-or-update classification must use the active configured environment's current authoritative task baseline | Run the declared task-level export route; stop with an environment-configuration or export error if the active configured environment is unavailable, the export is missing or stale, or it belongs to another environment or task; do not request an environment URL | Export metadata, header rows, detail rows, active configured environment association, export completion evidence |
| CSP-DEP-000 | Catalog context agreement | Yes | Always | Satisfied | Developer confirmation: HCM Security / HCM Security Profile is authoritative; the conflicting Confluence hierarchy is not authoritative for task placement | | Task execution must use one explicitly confirmed hierarchy | Use HCM Security / HCM Security Profile and stop if a future source conflicts | Offering: HCM Security; Functional Area: HCM Security Profile |
| CSP-DEP-003 | Intended data-role assignment | Yes | Verifying effective candidate visibility | Verify | Target pod security configuration | | Candidate visibility depends on the assigned data role | Stop and route to the Recruiting security owner | Assignment verification |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Documented dependency is confirmed | No |
| Verify | A documented dependency needs confirmation | No |
| Blocked | A dependency is missing, unresolved, or conflicts with the source contract | No |

## Post-Configuration Behavior Validation

| Check | When to Validate | What Happens |
|---|---|---|
| ORA_IRC_CANDIDATE_SECURITY_ENABLED | After configuration, when validating whether Candidate Security Profiles are effective | Report whether the profile can affect candidate security behavior; the value does not block FSM package creation, preview, or import |
| Candidate Search and Oracle Search configuration | After configuration, when validating restrictive Candidate Search behavior | Report whether restricted search behavior can be tested; search readiness does not block FSM package creation, preview, or import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.CHECK_READINESS | step | 1 | resolve_dependency | satisfied->CSP.PROTECT_SEEDED_PROFILE;read_details->CSP.READ_VALIDATE_NAME;blocked->CSP.HANDLE_ISSUES | none | stop | First step for every configuration request and every read-details request: export and verify the current-run FSM baseline before classification, defaulting, configuration questions, or policy checks; no profile Name is required for this task-level export. After verification, requests to get, show, view, or inspect an existing profile's details select read_details and must traverse the read graph through label resolution and evidence evaluation; export completion alone never completes a details request. Configuration intent retains satisfied. On failure generate no configuration rows |
