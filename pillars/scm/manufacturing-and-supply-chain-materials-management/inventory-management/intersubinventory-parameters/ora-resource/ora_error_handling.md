# Intersubinventory Parameters Error Handling

## Error Handling Rules

| Situation | What Happens |
|---|---|
| Approved lookup code or meaning has no exact match | Stop before Data Loader handoff and request a valid documented field value |
| Approved lookup is ambiguous | Stop before handoff; do not select a candidate automatically |
| Code and meaning resolve to different rows | Stop and request one authoritative representation or a consistent pair |
| Organization or subinventory resolution fails in the BO | Preserve the BO/Data Loader diagnostic; do not add or fall back to a task-local REST resolver |
| Required current-run BO metadata preflight fails | Stop before handoff and record selected environment, exact BO discriminator, and sanitized diagnostic |
| Registration exists but metadata evidence is earlier or from another environment | Treat it as stale provenance, run a new read-only preflight, and block until current-run evidence succeeds |
| Sample support, mandatory attributes, or key attributes cannot be confirmed | Stop before handoff and retain sanitized metadata diagnostics; do not declare execution ready |
| Conditional UI-required values conflict | Stop and identify destination type, transfer type, receipt-required flag, and conflicting field; do not silently clear input |
| Start or end date has an unsupported or invalid representation | Stop before handoff; accept only exact `YYYY-MM-DD` or exact `YYYY/MM/DD`, normalize the latter to `YYYY-MM-DD`, and report invalid calendar dates without guessing date order |
| Friendly value or alias is not explicitly accepted | Stop before normalization; do not guess, fuzzy-match, or forward the representation |
| Route-specific fields are mixed | Stop and select the workflow route; do not emit REST `*Code` or Boolean structures in FSM, or FSM columns in REST/Data Loader |
| DFF input is malformed or incompatible with the selected route | Stop before handoff when `DFF` is not an array, contains unknown fields, is flattened into the root row, names an unverified context or segment, or is supplied for FSM |
| Data Loader or Fusion rejects prepared data | Preserve loader status, row identity, failure class, and sanitized message; backend validation remains Data Loader/Fusion-owned |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup no match | Exact Destination Type, Transfer Type, or Receipt Routing lookup returns no row | Provide a valid documented code or meaning field |
| Lookup ambiguity | Exact lookup returns multiple rows | Provide an unambiguous code or meaning |
| Conflicting input | Code and meaning differ, subinventories are equal, dates are inconsistent, or conditional fields conflict | Correct identified input and rerun validation |
| Invalid date representation | `StartDate` or nonblank `EndDate` is ambiguous, contains a timestamp, or is not a valid `YYYY-MM-DD` or `YYYY/MM/DD` calendar date | Supply an unambiguous valid date; REST/Data Loader output is always `YYYY-MM-DD` |
| BO-owned reference | Organization or subinventory is rejected by the BO | Correct the BO-supported value using Data Loader diagnostics |
| BO visibility preflight | Selected environment does not expose `interSubinventoryParameters` or metadata lookup fails | Verify registration and access, then run a new preflight |
| Stale or incomplete metadata evidence | Current-run environment, BO discriminator, sample support, mandatory attributes, or keys are absent | Run a new preflight and retain its sanitized runtime result |
| Unsupported representation | Unapproved alias, mixed-route field, transient checkbox value, or mismatched route value is supplied | Use documented semantic input and let selected route emit its physical representation |
| DFF contract mismatch | DFF input is malformed, flattened, contains an unverified field or context, or is supplied for FSM | Use the REST/Data Loader `DFF` child with `interSubParametersName` and optional blank or null `__FLEX_Context`, or omit DFF for FSM |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct source using reported diagnostic |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is missing, ambiguous, or conflicting | Do not fuzzy-match, guess, or select the first candidate |
| Organization or subinventory needs resolution | Do not invoke an unapproved task-local REST lookup; retain BO ownership |
| Data Loader reports an uncertain failure | Do not resubmit until status and read-only verification clarify outcome |
| Metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as fallback |
| Route selection is absent or conflicting | Do not infer route from supplied physical field names or emit both route representations |
| DFF input is present | Do not flatten the child into the root row, infer another context or segment, pass unknown fields, or emit DFF through the FSM route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.DATA_LOADER_HANDOFF | terminal | 80 | terminal | none | ISP.VALIDATE_EFFECTIVE_VALUES | continue | Current-run metadata, local validation, route normalization, approved lookup resolution, and defaulting passed; hand off to `core.data-loader` |
| ISP.HANDLE_ERROR | step | 90 | error_handler | handled->ISP.RETURN_ISSUES | none | stop | Any lookup, readiness, validation, defaulting, route-normalization, DFF contract, or Data Loader issue |
| ISP.RETURN_ISSUES | terminal | 100 | terminal | none | none | continue | A blocking issue was classified and disclosed |
