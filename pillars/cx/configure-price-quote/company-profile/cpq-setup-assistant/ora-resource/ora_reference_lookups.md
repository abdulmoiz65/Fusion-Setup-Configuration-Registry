# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_cpq_deployment | Before a configuration workflow enters Setup Assistant initialization | Selected environment host | GET https://<host>/cpq/rest/v1/site/version, without OAuth credentials, an Authorization header, or any other authentication material | HTTP response status only | `404` means CPQ is not deployed; every other HTTP response means the deployment endpoint is present | CPQ deployment result | On `404`, show “CPQ is not dpeloyed in this instance and hence cannot proceed with Setups now.” and stop. For other responses, continue with Setup Assistant initialization. |
| resolve_cpq_preinitialization_status | After deployment validation and before initialization | Selected environment and OAuth authentication | GET /crmRestApi/resources/latest/setupAssistants/SA_SETUP_ASSISTANT?expand=SetupProgress&onlyData=true | Assistant status and CPQ-owned progress | Resolve one readable assistant status. `SETUP_NOT_DONE` permits initialization approval; complete, processing, error, and indeterminate results stop the configuration workflow. | Pre-initialization status result | An unreadable, missing, contradictory, or unknown result is indeterminate; report the safe status outcome and do not initialize. |
| resolve_cpq_setup_assistant_record | Immediately after assistant initialization and after each successful child mutation | Assistant identity after initialization | GET /crmRestApi/resources/latest/setupAssistants/SA_SETUP_ASSISTANT?expand=CPQRoleMappings,CPQUsers,CPQStarterDataImport,CompanyProfiles,SetupProgress&onlyData=true | Assistant status; Company Profile ID and existing-data state; CPQ administrator user IDs from `CPQUsers`; role mappings; starter-data child presence; setup progress | Resolve one readable assistant and use only child references returned by that response. In this Setup Assistant contract, every returned `CPQUsers` record is a CPQ administrator. | Assistant status, child IDs, existing-admin presence, and progress reference | An unreadable record blocks execution or verification; report the safe diagnostic and do not construct a substitute write |
| resolve_cpq_setup_progress | Immediately once after submission, after an uncertain submission outcome, or when the user later explicitly requests status | CPQ setup-assistant identity | GET /crmRestApi/resources/latest/setupAssistants/SA_SETUP_ASSISTANT?expand=SetupProgress&onlyData=true | Setup progress and status | Read the status for the selected CPQ setup assistant only | Verified progress and completion state | Read failure or indeterminate state blocks success reporting; do not replay the submission |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Setup-assistant record resolves exactly once | Use the resolved identity and child-record references only to prepare the documented Data Loader source. |
| Setup-assistant record is missing, ambiguous, or unreadable | Stop before preview or verification and return a sanitized diagnostic. |
| Setup-progress lookup is incomplete or fails | Mark the outcome indeterminate and reconcile through safe reads; do not resubmit automatically. |
| Company Profile reports existing data | Preserve the discovered state in the redacted change summary; prepare and validate the immutable Data Loader source with approval pending, then build and present the exact stage preview before requesting approval. |
| CPQ users are already present | Reconcile every requested current or additional administrator against the discovered users. Do not create a duplicate; create an additional administrator only when the request is validated and explicitly approved. |
| A role mapping or starter-data child is returned | Treat it as read-only evidence for this skill; do not call an unverified write endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPQ.PREINITIALIZATION_STATUS_LOOKUP | step | 4 | reference_lookup | setup_not_done->CPQ.INITIALIZATION_READINESS;in_progress->CPQ.RETURN_ISSUES;error->CPQ.RETURN_ISSUES;completed->CPQ.RETURN_ISSUES;unknown->CPQ.RETURN_ISSUES;failure->CPQ.FAILED | CPQ.INITIALIZATION_PREFLIGHT | stop | Use the standard authenticated read-only client to read status once after the separate runtime deployment preflight. Only `SETUP_NOT_DONE` proceeds to initialization readiness; this node never initializes CPQ. |
| CPQ.CONFIGURATION_DISCOVERY_LOOKUP | step | 5 | reference_lookup | ready->CPQ.CONFIGURATION_READINESS;in_progress->CPQ.RETURN_ISSUES;error->CPQ.RETURN_ISSUES;completed->CPQ.RETURN_ISSUES;unknown->CPQ.RETURN_ISSUES;failure->CPQ.FAILED | CPQ.CONFIGURATION_PREFLIGHT | stop | Use the standard authenticated read-only client to discover the assistant, Company Profile, CPQ Users, role mappings, starter data, progress, and LOV values. Core Data Loader performs initialization and mutations; this node only supplies current discovery evidence. |
| CPQ.READ_STATUS_ONLY | step | 6 | reference_lookup | reported->CPQ.STATUS_REPORTED;indeterminate->CPQ.RETURN_ISSUES;failure->CPQ.FAILED | CPQ.REQUEST_SELECTION | stop | Use the standard authenticated read-only client for exactly one explicit status request with the documented 30-second timeout and no retry. Do not initialize, collect configuration, mutate, poll, or enter a readiness handoff. |


## Complete Child Verification Reads

Within the explicit initialization/child completion continuation, existing-state
verification, final pre-upload verification, or requested recovery/inspection,
the guard's `resolve_cpq_setup_assistant_record` verification may use these fixed
read-only paths through the existing Core REST client:

1. GET `/crmRestApi/resources/latest/setupAssistants/SA_SETUP_ASSISTANT` with `onlyData=true` to bind assistant Id, Name and Status.
2. GET that fixed path plus `/child/CompanyProfiles` and `/child/CPQUsers`, each with `onlyData=true`, `limit=500`, and an offset advanced by the number of returned records until `hasMore=false`.
3. GET the same fixed assistant identity again and reject a changed Id, Name or Status.

Each collection is limited to 10,000 records. Reject malformed count/offset/limit
metadata, nonadvancing/repeated pages, duplicate identities and incomplete reads.
Never follow a response-provided URL. Fetching pages completes one bounded
verification; it does not poll a job or retry a mutation. Assistant identity/status
bracketing detects parent drift but does not provide a server-side transactional
snapshot or eliminate external-change races. Existing complete-outcome checks
remain mandatory. The separate user-facing one-shot setup-progress lookup keeps
its existing request and timeout behavior.
