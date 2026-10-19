# Algorithm Error Handling

| Situation | Required response |
|---|---|
| Mandatory preflight fails for any advisory, mapping, Groovy, validation, source-resolution, target-resolution, or use-case request | Stop immediately and ask for corrected current attachments before source or target reasoning. |
| `Algorithm_BO.xml`, current Service Mapping source XML, or business requirement is missing | Stop and request both current XML exports with the business requirement; do not continue from chat cache, prior artifacts, remembered paths, or assumptions. |
| The supplied Service Mapping source does not have `contextName="ARInterface"` | Stop and request a copied Subscription AR Integration source XML. |
| The export is for a different algorithm | Reject it and request the correct integration export. |
| Absolute highest `VersionNum` does not have `ActiveFlag` `Y` | Inform the implementer that the highest version is not in In Progress state; do not proceed with advisory, Groovy, or XML editing. |
| A prompt has not been classified as Input Type 1, 2, 3, 4, or 5 | Classify it through Use-Case Resolution before source or target recommendations. |
| The implementer says to go with assumptions | Treat only named, evidence-backed recommendations as assumptions for review; do not bypass mandatory XML validation, source-resolution, deployed DFF/context confirmation, Groovy approval, or XML approval. |
| Existing executable Groovy is present | Ask whether it is replaced or new Groovy is added above it, and whether formatting is wanted. |
| A service-mapping concern is raised | Route to the companion Service Mapping skill and resume only after it returns. |
| Companion describe cannot run because of runtime environment connection, authentication, privilege, transport, or endpoint failure | Stop and tell the implementer describe is not working. Ask whether to resolve the runtime environment connection and rerun describe, or proceed only with explicitly named unconfirmed assumptions for review. Do not draft Groovy from silent assumptions. |
| Groovy is not explicitly approved | Provide reviewable Groovy only; do not create a modified `Algorithm_BO.xml`. |
| XML is created after approval | Instruct the implementer to zip `Algorithm_BO.xml` alone and import it through Manage Algorithms actions. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALG_AR_ADVISORY_GATE | decision | 6 | execution_gate | advisory_ready->ALG_AR_RETURN_ADVISORY;out_of_scope->ALG_AR_OUT_OF_SCOPE | ALG_AR_ENFORCE_DESIGN | stop | Design enforcement passes |
| ALG_AR_MISSING_INPUT | terminal | 7 | terminal | none | none | stop | Required advisory input is missing |
| ALG_AR_BLOCKED | terminal | 8 | terminal | none | none | stop | A dependency or design rule blocks the advisory |
| ALG_AR_OUT_OF_SCOPE | terminal | 9 | terminal | none | none | stop | The request requires external execution or undocumented platform behavior |
| ALG_AR_RETURN_ADVISORY | terminal | 10 | terminal | none | ALG_AR_ADVISORY_GATE | stop | Advisory review is ready |
