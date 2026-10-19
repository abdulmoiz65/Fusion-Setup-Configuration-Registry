# Error Handling

## Stop Conditions

Stop before upload for missing task support, hash mismatch, authorization
failure, absent same-environment confirmation, missing Data Loader validation,
or a missing/stale Task Hook approval envelope. Never retry a Fusion upload,
import, overwrite, replacement process, or failed job without new approval.

For timeout or failure, preserve target, task code, returned process/request ID,
last status, elapsed time, and redacted diagnostic references. Never expose or
persist credentials, tokens, customer data, or sensitive policy details.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MDSP.EXECUTION_GATE | decision | 4 | execution_gate | ready->MDSP.READY; blocked->MDSP.BLOCKED | MDSP.DESIGN_GATE | stop | Before returning a Data Loader approval preview. |
| MDSP.READY | terminal | 5 | terminal | none | MDSP.EXECUTION_GATE | continue | Task validation has passed; Core Data Loader owns approval and execution. |
| MDSP.BLOCKED | terminal | 6 | terminal | none | none | continue | Validation, dependency, design, or approval prerequisite is incomplete. |
