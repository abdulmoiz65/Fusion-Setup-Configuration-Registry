# Selection Criteria Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required read identity is missing or invalid | Stop and request only the missing exact identity; never invent an identifier. |
| The collection GET returns zero, multiple, or incomplete results | Report no caller-visible match only after a complete zero-result read; otherwise disclose the ambiguity or incomplete evidence and stop. |
| The REST GET fails | Classify the issue as authentication or authorization, transport or environment, or Fusion API; retain only sanitized diagnostics and stop. |
| A requested action would change setup | Stop this read-only resource workflow. A separate selected and approved execution workflow is required; do not construct a direct REST write. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | The supplied SelectionId or RequisitioningBUName is absent or invalid | Correct the exact supplied input. |
| Lookup blocker | The criterion is ambiguous or pagination is incomplete | Correct the identity or complete the read scope; do not choose a result. |
| Auth or authz | The caller cannot read the required criterion | Correct access and retry only the read if appropriate. |
| Transport or environment | The read-only service request fails before a response | Retry only a known idempotent read within the core client's bounds. |
| Fusion API | The GET returns an HTTP 4xx or 5xx response | Record a sanitized diagnostic; do not treat the error as not-found. |
| Approval blocker | A mutation is requested through this read-only guidance | Select the declared execution workflow and obtain its required approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read completion | Exact task code and name, supplied identity, resolved criterion or no caller-visible exact match, and the documented selection-precedence interpretation. |
| Failure | Stage, failure class, redacted evidence, affected identity, and one safe next action. |
| HTTP failure diagnostics | Operation, HTTP status, sanitized endpoint path, Oracle error code and redacted message summary when supplied, ECID when supplied, and recommended next action. Never retain full URLs, raw response bodies, authorization headers, tokens, or cookies. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A GET result is partial, ambiguous, or unauthorized | Do not report not-found or infer a criterion. |
| A caller asks to create, update, or delete a criterion | Do not construct, submit, replay, or retry a write from this resource set. |
| A selection preference is undocumented | Do not substitute a source-type, party-type, or price value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.HANDLE_ERROR | step | 90 | error_handler | handled->EPPSEL.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, defaulting, or design failure |
| EPPSEL.RETURN_READ_RESULT | terminal | 60 | terminal | none | EPPSEL.ENFORCE_DESIGN | stop | A criterion review is complete without a setup mutation |
| EPPSEL.RETURN_NOT_FOUND | terminal | 70 | terminal | none | EPPSEL.RESOLVE_CRITERIA | stop | A complete collection read finds no caller-visible exact criterion |
| EPPSEL.RETURN_ISSUES | terminal | 100 | terminal | none | EPPSEL.HANDLE_ERROR | stop | A blocking issue was classified and disclosed |
