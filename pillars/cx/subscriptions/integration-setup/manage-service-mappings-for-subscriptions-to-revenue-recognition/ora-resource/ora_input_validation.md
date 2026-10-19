# Subscription to RMCS Service Mapping Input Validation

## Scope

Validates supplied inputs and returned result shapes for an assisted checkpoint with phase intake, analysis or handoff. Current-request files and recorded user choices are authoritative for local analysis, not Fusion publication. Lookup mechanics are owned by [reference lookups](ora_reference_lookups.md); policy predicates are owned by [design enforcement](ora_design_enforcement.md). Detailed identity rules remain in the primary's [input preflight](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md#input-preflight).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Checkpoint scope | rule_phase equals intake, analysis or handoff; exact task identity and requested outcome | Return the missing or invalid checkpoint scope | Obtain rule_phase and distinguish analysis from an unsupported Fusion operation | Every checkpoint | |
| Current input pair | Current raw `Algorithm_BO.xml` and current Service Mapping XML, with preflight identity and fingerprint evidence | Return input validation issue without prior-sample substitution | Apply canonical primary input preflight to the current request | Every checkpoint | resolve_rmcs_service_mapping_contract |
| Request and project context | Business requirement, available record-level meaning, project context and request/continuation identity as applicable | Request missing context without inventing target or source facts | Use the [companion request contract](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-request-record); direct requests have no invented suspended caller | Every checkpoint | |
| Analysis question and candidate working set | Specific source question, stated objects/attributes, current action scope and available source-resolution records; an empty initial candidate set is allowed | Request missing question or scope, not fabricated candidates | Validate the [source-record shape](../resources/ora_service_mapping_guidance.md#source-resolution-record) for records that exist | phase analysis | resolve_rmcs_mapping_bindings |
| Handoff result | Structured outcome, source-record references or explicit unresolved items, evidence/status and caller continuation when present | Return missing handoff fields | Apply the [companion result contract](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-handoff-template) without changing an unresolved outcome to analyzed | phase handoff | verify_rmcs_mapping_handoff |
| Final configuration contribution | Source-owned fields for primary final-operation rows when part of the requested handoff | Identify missing contribution or primary-owned prerequisite | Use the [single final schema](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff), not invented output details | phase handoff with final proposed-operation rows | verify_rmcs_mapping_handoff |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| XML input contract | Check accepted container, parseability, integration identity, absolute highest-version eligibility and current references under canonical preflight; preserve exact names/case | Every checkpoint | resolve_rmcs_service_mapping_contract |
| Source record schema | Check required fields and distinct decision/exposure/publication evidence states; unresolved values stay explicit | Existing records in analysis or handoff | resolve_rmcs_mapping_bindings |
| Candidate metadata shape | Check scalar/object/collection shape and type/queryability evidence under [candidate validation](../resources/ora_service_mapping_guidance.md#candidate-shape-queryability-and-type-compatibility) | A candidate is assessed | resolve_rmcs_mapping_bindings |
| Physical field identity | Compare exact object and column with the [physical ledger](ora_reference_lookups.md#physical-object-identities); shorthand names are not an alternative schema | A database column is named | resolve_rmcs_mapping_bindings |
| Character capacity | Check each evidenced source/target length constraint; report overlength values without truncation | A resolved character binding or literal is checked | resolve_rmcs_mapping_bindings |
| Numeric and temporal shape | Preserve verified types, precision/scale and DATE/TIMESTAMP distinctions; record unavailable representation evidence without invented conversion | A numeric or temporal value is checked | resolve_rmcs_mapping_bindings |
| Coded and satisfaction values | Require accepted-value/model evidence for the selected field; column length is not an enumeration and no percentage bound is inferred | A proposed operation needs an enum or satisfaction constraint | resolve_rmcs_mapping_bindings |
| Stored mandatory values | Do not turn generated keys or audit-column storage constraints into invented request fields | Physical mandatory-column evidence is considered | resolve_rmcs_mapping_bindings |
| Structured outcome | Require canonical analyzed, needs_decision, prerequisite_pending, blocked or declined status and corresponding evidence/unresolved fields | phase handoff | verify_rmcs_mapping_handoff |
| Checkpoint result shape | Return phase, exact task identity, completed checks, structured outcome, missing items, evidence, actual side effects and safe continuation; completion is not publication or source acceptance | At EVALUATE_CHECKPOINT after prior applicable nodes | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current-pair identity or required shape is invalid | Input validation issue | Return exact failed preflight or missing field | resolve_rmcs_service_mapping_contract |
| Source choice is pending but its candidate record is valid | needs_decision | Return the named candidate question, not accepted-source readiness | resolve_rmcs_mapping_bindings |
| Successful scoped source search has no viable candidate | needs_decision with recorded search coverage | Return the missing exact source/object question without treating the completed no-match search as a malformed checkpoint | resolve_rmcs_mapping_bindings |
| Chosen source is unexposed or lacks applicable provider/access evidence | prerequisite_pending, or conditional only when the implementer explicitly accepts the named assumption | Preserve the choice, identify the `_Custom` exposure/provider/access gap for ordinary sources, and keep confirmed exposure/runtime readiness pending | resolve_rmcs_mapping_bindings |
| Handoff accurately reports pending, blocked or declined work | Valid structured outcome, not completed configuration | Return that outcome and continuation; unresolved work is not by itself invalid result shape | verify_rmcs_mapping_handoff |
| Direct mapping-only or pre-Groovy handoff has no primary operation rows yet | Valid source/findings handoff when companion-owned fields are complete | Mark unsupplied primary-owned details not applicable or pending; do not require proposal/approval rows before they exist | verify_rmcs_mapping_handoff |
| Final checkpoint record omits required checks or mislabels the outcome | Checkpoint evaluation issue | Report missing checks or inconsistent result before checkpoint completion | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSSM.VALIDATE_INPUT | step | 10 | validate_input | valid->RMCSSM.RESOLVE_EVIDENCE;invalid->RMCSSM.REPORT_ISSUES | none | stop | Validate current-phase input shape using supplied current files and local choices. |
| RMCSSM.EVALUATE_CHECKPOINT | decision | 70 | evaluate_result | valid->RMCSSM.RETURN_RULE_RESULTS;invalid->RMCSSM.REPORT_ISSUES | RMCSSM.CHECK_EXECUTION_CONTRACT | stop | Evaluate completed applicable checks and structured outcome; valid means checkpoint completion only, not accepted source or deployed mapping. |
