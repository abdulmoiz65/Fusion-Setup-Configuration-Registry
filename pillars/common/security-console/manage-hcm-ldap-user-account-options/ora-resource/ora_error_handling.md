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
sensitive security configuration.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| HLUO.EXECUTION_GATE | decision | 4 | execution_gate | ready->HLUO.READY; blocked->HLUO.BLOCKED | HLUO.DESIGN_GATE | stop | Before returning a Data Loader approval preview. |
| HLUO.READY | terminal | 5 | terminal | none | HLUO.EXECUTION_GATE | continue | Task validation has passed; Core Data Loader owns approval and execution. |
| HLUO.BLOCKED | terminal | 6 | terminal | none | none | continue | Validation, dependency, design, or approval prerequisite is incomplete. |
