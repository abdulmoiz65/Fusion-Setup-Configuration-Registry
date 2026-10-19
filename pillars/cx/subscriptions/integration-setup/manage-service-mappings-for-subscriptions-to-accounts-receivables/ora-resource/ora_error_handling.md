# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Business requirement does not state the expected AR outcome | Stop and request the expected header or line result |
| Mandatory preflight fails for any advisory, mapping, validation, source-resolution, or use-case request | Stop immediately and ask for corrected current attachments before source recommendations or describe. |
| Current `Algorithm_BO.xml` or current Service Mapping source XML is missing | Stop and request both current XML exports; do not perform recommendations, describe lookup, source-resolution, or handoff from chat cache, prior artifacts, remembered paths, or assumptions |
| `Algorithm_BO.xml` is for a different algorithm | Reject the export and request `Subscription Management and Account Receivables Integration`. |
| Absolute highest `VersionNum` does not have `ActiveFlag=Y` | Reject the export as not In Progress and request an updated algorithm export. |
| Service Mapping source XML does not have `contextName="ARInterface"` | Stop and request the copied Subscription AR Integration source XML; filename may vary. |
| Prompt is not classified as Input Type 1, 2, 3, 4, or 5 | Classify it through the primary algorithm Use-Case Resolution reference before source recommendation. |
| Flexfield context or Table Column assignment is missing | Stop and request the configured Receivables flexfield detail |
| Source custom attribute is not mapped or not exposed through service access | Block the recommendation until the mapping and access are confirmed |
| Data types differ between the custom Subscription attribute and Service Mapping attribute | Block the recommendation until the types are aligned |
| Test data does not produce the expected AR interface result | Compare target level, _Custom naming, view object mapping, and service access before revising the recommendation |
| PerformanceMode is requested | Stop and request the separate PerformanceMode instructions; Customization Enabled guidance does not apply |
| A request asks to modify algorithm XML or Groovy | Return it to the Manage Algorithms primary skill; this companion owns mapping guidance only |
| A returned source alias is not published in Service Mapping | Require mapping publication before returning the mapping result |
| A permitted describe request cannot run because of runtime environment connection, OAuth/authentication, privilege, transport, or endpoint failure | Stop and tell the implementer describe is not working. Report the failed describe family or URI and ask whether to resolve the runtime environment connection and rerun describe, or proceed only with explicitly named unconfirmed assumptions for review. Do not go with assumptions automatically. |
| A request asks for a REST operation other than the listed `/describe` requests | Refuse it; no general GET, create, POST, action, PUT, PATCH, or DELETE operation is supported |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required business or mapping detail is absent | Request the missing detail |
| Dependency readiness | A prerequisite flexfield, custom attribute, or service mapping is not ready | Resolve the prerequisite before advisory review |
| Design enforcement | A documented type, naming, or access rule is violated | Correct the design before advisory review |
| Verification gap | The observed interface result differs from the stated result | Diagnose mapping configuration and test data; do not make a change automatically |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Source or target mapping detail is undocumented | Do not invent entities, attributes, data types, or AR behavior |
| Describe fails at runtime | Do not silently substitute documentation, generic references, chat cache, or guesses for describe. Ask the implementer to choose runtime connection remediation plus rerun, or named unconfirmed assumptions for review. |
| Implementer says to go with assumptions | Do not treat this as permission to bypass preflight, source-resolution records, service access, publication prerequisites, deployed DFF or target-context confirmation, Groovy approval, or XML approval |
| Advisory recommendation is accepted | Do not treat acceptance as approval to create, publish, or execute a mapping change |
| Verification fails | Do not retry or change mapping logic without a revised requirement and implementer review |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SVC_AR_ADVISORY_GATE | decision | 4 | execution_gate | advisory_ready->SVC_AR_RETURN_ADVISORY;out_of_scope->SVC_AR_OUT_OF_SCOPE | SVC_AR_ENFORCE_DESIGN | stop | Design enforcement passes |
| SVC_AR_MISSING_INPUT | terminal | 5 | terminal | none | none | stop | Required advisory input is missing |
| SVC_AR_BLOCKED | terminal | 6 | terminal | none | none | stop | A dependency or design rule blocks the advisory |
| SVC_AR_OUT_OF_SCOPE | terminal | 7 | terminal | none | none | stop | The request requires Fusion execution or undocumented platform behavior |
| SVC_AR_RETURN_ADVISORY | terminal | 8 | terminal | none | SVC_AR_ADVISORY_GATE | stop | Advisory review is ready |
