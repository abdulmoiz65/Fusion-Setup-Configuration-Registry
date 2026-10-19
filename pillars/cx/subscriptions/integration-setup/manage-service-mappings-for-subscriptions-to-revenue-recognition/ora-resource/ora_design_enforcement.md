# Subscription to RMCS Service Mapping Design Enforcement

## Scope

Assisted checkpoint predicates link to canonical policy owners, not a second runbook. [Mapping guidance](../resources/ora_service_mapping_guidance.md) owns source decisions, protected outputs and metadata interpretation. The [primary data-model guide](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_rmcs_data_model_reference.md) owns output routing. Preserved physical-column policies use the [source ledger](ora_reference_lookups.md#source-catalogue); they establish neither a writable operation nor an integration-execution prerequisite for local analysis.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Check source-policy predicates | Evaluate only claims and recommendations present in the current phase |
| 2 | Protect mapping and physical meaning | Reject schema changes, invented exposure or misleading correspondence |
| 3 | Check handoff fidelity | Preserve decisions, prerequisites and actual evidence status |
| 4 | Retain operation boundaries | Do not upgrade an assisted checkpoint into mutation, publication or integration verification |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| New source recommendation is claimed accepted | Error | resolve_rmcs_mapping_bindings | The [source-resolution record](../resources/ora_service_mapping_guidance.md#source-resolution-record) does not support that decision | Return the named decision, including a sole proposed match; retain exact implementer choices without re-asking | Correct record or request decision |
| Source candidates are assessed | Error | resolve_rmcs_mapping_bindings | [Candidate validation](../resources/ora_service_mapping_guidance.md#candidate-shape-queryability-and-type-compatibility) is contradicted or type/queryability conversion is invented | Record actual shape/operation evidence and affected gap | Correct analysis only |
| Source object or default is selected | Error | resolve_rmcs_mapping_bindings | Search coverage, owner or named-default provenance violates the [source-discovery contract](../resources/ora_service_mapping_guidance.md#resolve-the-functional-source) | Preserve accepted owner and unresolved alternatives | No automatic alternative |
| Output schema or direct-write access is assessed | Error | resolve_rmcs_mapping_bindings | [Protected output rules](../resources/ora_service_mapping_guidance.md#protected-output-schema-and-runtime-access) are violated or a read-only attribute is treated as writable | Keep seeded definitions unchanged and report actual access | No schema or access mutation |
| Function-backed source is used | Error | resolve_rmcs_mapping_bindings | The [function-source boundary](../resources/ora_service_mapping_guidance.md#function-backed-source-objects) is bypassed by an invented mapping entity or scalar cardinality | Return provider evidence for primary function handling | No invented entity/cardinality |
| New custom-source alias is recommended | Error | resolve_rmcs_mapping_bindings | The accepted [`_Custom` exposure contract](../resources/ora_service_mapping_guidance.md#custom-source-exposure-for-ordinary-service-mapping-attributes) is omitted, doubled, applied to function-backed/protected output fields, treated as deployed evidence or missing datatype treatment for a DFF/flex/custom source | Return the proposed object/entity, `<sourceAttributeName>_Custom` alias, exact VO attribute, datatype and service access as a prerequisite or named assumption | No XML mutation or publication claim |
| Physical column is selected | Error | resolve_rmcs_mapping_bindings | Table existence is used as proof of runtime exposure or write permission | Verify binding and supported output route independently | No fabricated mapping attribute |
| Field correspondence is defined | Error | resolve_rmcs_mapping_bindings | Same names or same-index extension slots are treated as automatically bound | Require explicit current correspondence evidence | No guessed binding |
| Header, line and subline objects are linked | Error | resolve_rmcs_mapping_bindings | OSS source identifiers are equated with VRM-generated keys or parent/source keys are confused | Preserve ledger identity distinctions and actual action associations | No guessed join or generated ID |
| Source line extension fields are reused | Error | resolve_rmcs_mapping_bindings | Documented SL meaning or evidenced occupied slots are overwritten silently | Preserve charge, pricing, asset, product, usage and billing meanings; when the primary suggests a next slot under an accepted assumption path, keep the deployed-slot confirmation prerequisite explicit | No confirmed unused-slot allocation |
| Target subline extension is selected | Error | resolve_rmcs_mapping_bindings | Internal-use SRC_ATTRIBUTE groups are proposed as customer slots | Preserve TS26A/TS26C restrictions and primary no-subline-insert rules | No internal-slot use or subline insert |
| Subline satisfaction values are mapped | Error | resolve_rmcs_mapping_bindings | Same-name columns imply a population/write contract without evidence | Confirm supported existing output binding and model-specific meaning | No inferred insert route |
| Item or memo-line identity is mapped | Error | resolve_rmcs_mapping_bindings | Both ITEM_ID and MEMO_LINE_SEQ_ID are proposed for one target source line | Preserve their mutually exclusive meaning in TL25D/TL26C | No automatic identity choice |
| Revision or locking fields are used | Error | resolve_rmcs_mapping_bindings | Revenue VERSION_NUMBER/VERSION_FLAG or OBJECT_VERSION_NUMBER are treated as mapping-definition versions | Keep revenue revision, locking and algorithm/mapping lifecycle distinct | No invented version control |
| Release-specific field is adopted | Error | resolve_rmcs_mapping_bindings | Newer documented field is presumed present without current evidence | Record release applicability; INITIAL_PERF_EVENT_DATE is a ledger example | No automatic compatibility |
| Final proposed-operation handoff rows are supplied | Error | verify_rmcs_mapping_handoff | The [single final contract](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) is contradicted or pending choices/exposure are labelled complete | Return accurate source-owned facts and unresolved outcomes; absent primary proposal/approval fields are not a prerequisite for earlier source-only handoffs | Correct record, not Fusion |
| phase handoff claims publication or deployment | Error | verify_rmcs_mapping_handoff | Supplied files or accepted choices are presented as publication proof | Separate local evidence from unsupported live verification | Remove claim; retain unrelated local analysis |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_rmcs_mapping_bindings | Source or physical-field claims in analysis/handoff | Current binding, candidate, decision and evidence-state findings | ora_reference_lookups.md |
| verify_rmcs_mapping_handoff | Handoff or publication-claim evaluation | Source-owned facts, unresolved outcomes and supporting evidence | ora_reference_lookups.md |

No mapping default is applied except the accepted `<sourceAttributeName>_Custom` handoff for ordinary unexposed source attributes. Algorithm CustomizationFlag belongs to the primary's approval-bound workflow, not this companion. Actual integration setup, lifecycle eligibility, process execution and downstream verification remain separate [unsupported live contracts](ora_reference_lookups.md#unsupported-live-contracts).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSSM.ENFORCE_DESIGN | step | 40 | design_enforcement | passed->RMCSSM.CHECK_EXECUTION_CONTRACT;blocked->RMCSSM.REPORT_ISSUES | RMCSSM.CHECK_DEPENDENCIES | stop | Check current-phase claims against canonical source policies and applicable physical restrictions; execute no mapping or algorithm change. |
