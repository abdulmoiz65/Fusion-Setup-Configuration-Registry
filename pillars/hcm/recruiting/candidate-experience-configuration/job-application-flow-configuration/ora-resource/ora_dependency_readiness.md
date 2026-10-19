# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task route and environment | AF.VERIFY_TASK_ROUTE verifies task identity, selected environment, routed Auth readiness, catalog CSV support and safe persistence destinations. |
| 2 | Current export | AF.LOAD_EXPORT_CACHE delegates to shared.setup-export.task-level-export for ORA_IRC_APPLY_FLOW_CONFIGURATION, obtains current data when absent/stale, verifies downloaded evidence and retains immutable cache identity. |
| 3 | References | AF.RESOLVE_REFERENCES uses verified export roots; source/parent selection then occurs on its operation branch before any creation defaults. |
| 4 | Approved import handoff only | The owning core.data-loader FSM workflow revalidates selected environment, authorization, task/catalog support, final package and exact environment/artifact approval immediately before its one submission. Preview preparation and Retrieve do not authorize import. |

Operation selects the declared branch; an available token or reference does
not authorize an alternate workflow. These task-local dependencies do not
replace the owning export or Data Loader preflight and approval checks.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| task_route | Exact task export route | Yes | AF.VERIFY_TASK_ROUTE; every operation | Verify | Existing task metadata and routed task catalog; shared.setup-export.task-level-export owns catalog discovery and CSVExportImportSupportedFlag=Y preflight | verify_apply_flow_route | Retrieve needs current configuration; creation needs identity/source evidence | Require ORA_IRC_APPLY_FLOW_CONFIGURATION under Recruiting / Candidate Experience; refuse unsupported catalog export flags | Task identity, route and support evidence |
| environment_auth | Selected environment and authorization | Yes | AF.VERIFY_TASK_ROUTE; every operation | Verify | Selected workflow environment and core.auth.fusion-oauth-authentication readiness; task exporter enforces export privileges | verify_apply_flow_environment | Export must use the selected environment and authorized account | Show environment identity; invoke routed Auth only if login/refresh is needed at runtime; never expose secrets | Environment, authorization result |
| export_persistence | Immutable current export | Yes | AF.LOAD_EXPORT_CACHE | Lookup | shared.setup-export.task-level-export output, project exports destination, checksum and environment/release evidence | resolve_apply_flow_export | A missing cache must trigger the declared export route rather than a permanent missing-cache stop | Invoke the routed exporter when absent, stale or wrong environment/release; verify complete download and safe durable destination before consuming; preserve safe errors if export fails | Immutable ZIP reference, checksum, export timestamp, release and root evidence |
| language_evidence | Installed languages | Conditional | AF.RESOLVE_TRANSLATIONS; creation only | Lookup | Immutable target task export cached by environment/release | resolve_apply_flow_languages | Required for translated target rows | Obtain evidence from one routed export when absent; reuse matching cache and refresh when environment/release changes | Base and installed languages |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact route checks and applicable evidence pass | Continue along the declared graph; no configuration submission authorization implied. |
| Lookup | Export/cache or supported reference is needed | Invoke only the named export workflow or resolver and its normal preflight; no substitute endpoint. |
| Blocked | Auth, catalog, environment, export support or persistence fails | Stop affected operation with diagnostics; never bypass checks. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.VERIFY_TASK_ROUTE | decision | 20 | resolve_dependency | success->AF.LOAD_EXPORT_CACHE;failure->AF.HANDLE_ISSUES | AF.VALIDATE_REQUEST | stop | All. Verify task, selected environment, authorization, catalog support, safe destinations and declared export route; failure blocks the selected operation. |
| AF.LOAD_EXPORT_CACHE | decision | 30 | resolve_dependency | success->AF.RESOLVE_REFERENCES;failure->AF.HANDLE_ISSUES | AF.VERIFY_TASK_ROUTE | stop | All. Obtain immutable task export via the declared route when absent or unsuitable; validate environment and archive evidence. |
