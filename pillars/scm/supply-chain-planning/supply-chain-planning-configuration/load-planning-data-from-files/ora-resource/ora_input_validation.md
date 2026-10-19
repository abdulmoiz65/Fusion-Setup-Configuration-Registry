# Planning FBDI Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Explicit source system | Nonblank Source System supplied by the user for this request | Ask for the Source System value and wait before preparation or live work | Use the user's request or follow-up reply; never infer from file contents, examples, saved context, configuration or another request | Every prompt, CSV or ZIP request; retain the answer through the same request's approval steps | |
| Prepared archive evidence | Same-run preparation report, immutable ZIP path/SHA-256, member hashes/counts and template provenance | Stop before Core approval | Complete the local preparation workflow in SKILL.md and references/csv-preparation.md | Every load | |
| Business mapping | Resolved required/conditional values, documented enums and coherent rule/assignment references | Stop before CSV generation | Use descriptions in the compact current XLSM/CTL contract; ask only for missing business values | Prompt generation and updates | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Source-system mapping | Map the explicit request value to generated SR_INSTANCE_CODE fields; compare retained supplied rows with that value during the existing content review. A mismatch blocks handoff; never rewrite supplied files silently | Prompt generation, updates and supplied CSV/ZIP members | |
| Current schema evidence | Use the recorded current-run template resolution; each retained member has its own CTL/tab contract and complete position mapping | Local preparation | resolve_planning_fbdi_template |
| CSV shape and values | Validate full field count, header behavior, paired CTL/XLSM positional headers, encoding, quoting, types, lengths and date formats once in prepare_planning_fbdi.py; resolve conditional business rules during mapping | Generated and supplied CSV members | |
| END compatibility | Append END header/value to generated CSVs. Supplied files retain their bytes and may use full CTL width with or without a consistent terminal END | Local preparation | |
| Update semantics | Require a trustworthy full baseline; overlay only requested changes, preserve omitted values, and distinguish explicit null from omission | Prompt updates | |
| Package integrity | Preparation selects unique nonempty root members, rejects unsafe paths/links/encryption, verifies newly written member bytes, and records SHA-256. Do not invoke a separate scope command | Local preparation | |
| Same artifact handoff | Match passing local evidence to Core's verified preflight archive SHA-256 and member manifest; consume recorded checks without rerunning downloads or generation | Core Task Hook | |

## Task Nodes

The Task Hook checks evidence from the completed preparation, not the original
source or workbook. A missing/changed artifact requires fresh preparation;
a valid unchanged artifact does not. Core independently owns live BO routing
and approved-artifact integrity, not CSV schema inference.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALIDATE_FBDI_ARCHIVE | step | 20 | validate_input | valid->CHECK_LOAD_READINESS;invalid->RETURN_ISSUES | CHECK_SUPPORTED_ENTITIES | stop | Core Task Hook evaluates immutable preparation evidence |
