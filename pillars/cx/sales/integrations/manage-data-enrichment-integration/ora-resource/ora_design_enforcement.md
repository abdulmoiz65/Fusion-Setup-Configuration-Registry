# Manage Data Enrichment Integration Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect credentials | Secrets remain in the authorized Fusion or identity-provider UI and never enter chat, repository files, logs, or project artifacts. |
| 2 | Use supported authentication | New guidance uses OAuth and does not recommend deprecated Basic authentication. |
| 3 | Preserve the service URL identity | Remove only the trailing /data/ui from the provisioned data-service URL. |
| 4 | Qualify status claims | A daaSSmartData GET is reported as Smart Data configuration visibility, not end-to-end enrichment health. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| operation=configure | Error | | A credential or token would be requested, displayed, logged, or persisted | Have the user enter credentials directly in the authorized setup page; retain only a redacted completion checkpoint | Yes |
| operation=configure | Error | | New configuration guidance proposes Basic authentication | Use OAuth Authentication and the current Oracle grant-type requirements | Yes |
| operation=configure | Error | | The proposed data-service URL changes any component other than removing the trailing /data/ui | Recopy the provisioned service URL and remove only /data/ui | Yes |
| operation=check_status | Error | | The result would describe a successful GET as proof of credential validity, batch readiness, enrichment-job success, or end-to-end health | Report only API reachability, visible record count, raw enablement, endpoint presence, and limitations | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEI.DESIGN_GATE | decision | 3 | design_enforcement | configure_ready->DEI.DONE_GUIDANCE;status_ready->DEI.READ_SMART_DATA;blocked->DEI.HANDLE_ERROR | DEI.READINESS | stop | Enforce credential, authentication, URL, and status-claim boundaries for the selected operation. |
