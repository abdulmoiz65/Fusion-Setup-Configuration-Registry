# Candidate Pool Package Dependency Readiness

| Dependency | Mandatory evidence | On failure |
|---|---|---|
| Fresh target baseline | Current unscoped exact-task export and raw collision dictionaries | Stop before archive construction. |
| Pool create graph | Selected source Pool process, reusable phase route, and canonical terminal routes | Stop; do not infer a substitute relationship. |
| Immutable archive | ZIP-valid archive with all Pool joins validated | Stop before approval or upload. |
| Data Loader handoff | Approved Task Hook preview and exact archive digest | `core.data-loader` exclusively owns upload and initiation. |

## Task nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POOL.HANDOFF | decision | 60 | execution_gate | ready->POOL.DONE;blocked->POOL.HANDLE_ISSUES | POOL.VALIDATE_ARCHIVE | stop | Before Data Loader submission |
| POOL.HANDLE_ISSUES | terminal | 70 | terminal | none | none | stop | A Pool validation, export, identity, archive, or handoff issue must be returned without submission |
| POOL.DONE | terminal | 80 | terminal | none | POOL.HANDOFF | stop | The validated Pool package is ready for Core Data Loader handoff |
