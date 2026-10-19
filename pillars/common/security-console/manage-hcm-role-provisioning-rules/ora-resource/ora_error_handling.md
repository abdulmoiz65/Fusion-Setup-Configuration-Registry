# Error Handling

## Stop Conditions

Stop before upload for missing task support, an archive-hash mismatch,
authorization failure, missing same-environment restore confirmation, missing
Data Loader validation, or a missing/stale Task Hook approval envelope. Do not
retry a Fusion upload, import, overwrite, replacement process, or failed job
without new user approval.

For a timeout or failure, preserve the target environment, task code, process
or request ID when returned, last status, elapsed time, and redacted diagnostic
references. Never persist or expose credentials, tokens, customer data, or
sensitive role-provisioning configuration.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| HRPR.EXECUTION_GATE | decision | 4 | execution_gate | ready->HRPR.READY; blocked->HRPR.BLOCKED | HRPR.DESIGN_GATE | stop | Before returning a Data Loader approval preview. |
| HRPR.READY | terminal | 5 | terminal | none | HRPR.EXECUTION_GATE | continue | Task validation has passed; Core Data Loader owns approval and execution. |
| HRPR.BLOCKED | terminal | 6 | terminal | none | none | continue | Validation, dependency, design, or approval prerequisite is incomplete. |
