# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_service_mapping_assessment | Every FOM-to-OSS algorithm recommendation or change request | Validated service_mapping_assessment supplied by the companion Service Mapping task in the normalized request context | Companion task output supplied as an Algorithm input; no remote operation | XML context, source and target entities and attributes, availability and permissions, direct-assignment evidence, metadata status, mapping_status, algorithm_recommendation, assumptions, and prerequisites | Context must be OMIntegration and the assessment must be complete, validated, and applicable to the requested outcome. Preserve the assessment conclusion; do not infer a source, target, alias, assignment, or script | Validated mapping assessment fields for algorithm-necessity assessment and draft preparation when applicable | Stop when the assessment is absent, incomplete, uses another context, or does not cover the requested outcome |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Every algorithm recommendation or change request | Validate the supplied mapping assessment locally; do not invoke the companion task or REST from this task |
| The assessment evidences an existing direct mapping and no independent logic requirement | Return algorithm_not_required; do not inspect, draft, or alter Algorithm_BO.xml solely to duplicate the mapping |
| The assessment reports source-and-target availability without direct assignment evidence | Prepare the reviewable declarative action proposal directly in chat from the confirmed source, target, and preserved baseline RUN_SCRIPT. Put source in a fenced Groovy code block; state `ZeroOrOne` cardinalities, joins, null, string-blank, overwrite, amendment, and cancellation behavior; do not create a human-readable Markdown draft or an artifact before explicit approval |
| The assessment identifies an XML-evidenced interface-table bridge | Start the action from OSSTransactions and use the documented bridge keys in `contain(...).as(...).cardinality('ZeroOrOne').on(...)` clauses. Do not select a first or arbitrary duplicate, infer a direct assignment, or change Service Mapping configuration |
| The assessment identifies an XML-evidenced direct product-to-fulfillment-line relation | Treat it as supplementary evidence only. Preserve the baseline RUN_SCRIPT and use a separate OSSTransactions-first ConditionalAction; a direct key may add a consistency check but must not replace interface-table traversal |
| The desired conditional or nested action is not represented in the current Algorithm_BO.xml export | Treat the absent action as a creation case. Preserve the delivered RUN_SCRIPT unchanged and add a new separate CONDITIONAL_ACTION with the next available sequence number, using `references/ora_conditional_action_serialization.md`. Do not request a structural sample from the user, create a human-readable Markdown draft, or append the cross-entity rule to RUN_SCRIPT |
| The assessment reports a metadata blocker or incompatibility | Return the Service Mapping prerequisite; do not use an Algorithm as a substitute |
| The assessment reports a mapping gap with a complete exact Entities/Sources/Services UI change plan | Prepare a clearly labelled provisional source-level draft from that plan. A `service_mapping_validation_skipped=true` marker is valid only after the Service Mapping task asked its explicit validation-skip question and the user answered yes. State the skipped validation in the draft. After approval, show the prescribed warning and ask whether to continue before creating a local provisional artifact; do not claim the mapping is applied or validated |
| The assessment reports a mapping gap without a complete exact Entities/Sources/Services UI change plan | Return the Service Mapping prerequisite. If the user explicitly requests code, also return a clearly labelled placeholder-only Groovy source draft and a mapping-information request for every literal placeholder. After responses are supplied, require the companion task's revalidated assessment before creating an approval-ready draft; do not request approval or create an artifact beforehand |
| The requested behavior uses a custom indicator | Require the companion assessment to identify every source and target technical value, with XML or documented describe evidence. Block an implementation-ready draft until the complete contract is revalidated. |
| The assessment is incomplete or context-incompatible | Stop before draft preparation and return the missing or corrected assessment requirement |

## Sources

- User-approved FOM-to-OSS operating model: pass a validated service_mapping_assessment as an Algorithm input or dependency instead of using a cross-task handoff action.
