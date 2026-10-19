# Approval and Error Handling

Do not mutate Fusion before a later standalone exact `approve`. Never retry a
live POST, PUT, or action automatically. Preserve Plan Copy and ESS identifiers
after partial failure. Treat `ImportPlDesign=10`, unresolved mappings, failed
ESS, or timeout as failure; success requires `ImportPlDesign=12`.
After the parent becomes terminal, download `enclosure/RequestLogs`. Treat any
recognized error in this consolidated import log as failure, even when ESS and
the parent report success. Success also requires the log to be non-empty.
After an error with a retained Plan Copy ID, retrieve this same enclosure and
include seeded `JBO-BEN:::BEN_*` errors in the failure details. Empty child logs
do not mean the consolidated log is unavailable. Preserve the original failure
if log retrieval fails, and never resubmit an import to recover its log.
Report only setup-object names and counts present in its Plan Copy Report,
without ZIP comparisons or verification-status commentary. If there are no
per-object rows, state that the import log did not report object counts; keep
the process result and do not substitute source counts.

## Task Nodes

- `BEN_PLAN_CONFIG.EXECUTION_GATE` requires immutable preview approval.
- `BEN_PLAN_CONFIG.READY_FOR_RUNBOOK` permits one approved execution.
- `BEN_PLAN_CONFIG.AWAITING_APPROVAL` performs no write.
- `BEN_PLAN_CONFIG.FAILED` performs no replacement submission.
