# Defaulting Rules

| Field | Value | Ownership |
|---|---|---|
| Execution route | core.data-loader | Sole import workflow |
| CX object code | GeoTerritoryInterface | Task identity |
| Source type | ORA_CX_IMPORT | Core CX preflight |
| Canonical UCM account | Live metadata `UcmAccount` | Resolve from the selected target object; no fixed account default |
| Documents UCM account | Live account with `$` appended to each path segment | Core conversion of live metadata; require preflight agreement |
| High-volume load | Omitted by default | Set during preflight only for explicit user high-volume/bulk intent |
| Upload references and Run Book parameters | Core-managed | Never synthesize or replace |

Do not default `ImportMode`, `Activate`, `Schedule`, a security-group override,
or a task-local upload profile. The current native initiation action does not
expose a server-enforced create-only setting. Keep source new-record intent
separate from that unavailable guarantee. Apply defaults before preview only;
any changed bound option requires fresh validation and approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.DEFAULTS | step | 5 | apply_default | applied->TG.DESIGN;invalid->TG.ERROR | TG.UCM_METADATA | stop | Before preview; retain core native routing and user-requested options. |
