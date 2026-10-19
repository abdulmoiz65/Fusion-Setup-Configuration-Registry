# RMCS Algorithm Input Validation

## Scope

Validate the assisted checkpoint's input/output contract. The [XML guide](../resources/ora_algorithm_xml_guidance.md) owns detailed preflight and artifact procedures; [design enforcement](ora_design_enforcement.md) owns policy. Local evidence authority and resolver mechanics are in [reference lookups](ora_reference_lookups.md#local-lookups). Stored table NOT NULL constraints do not turn system-generated identifiers or audit columns into required user inputs.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Checkpoint context | rule_phase is intake, proposal, approved_change or artifact_result; request identity, business requirement and selected project context | Stop this checkpoint; never infer approval or a later phase | Caller supplies the actual workflow stage and request context | Every checkpoint | |
| Current input pair | Current raw `Algorithm_BO.xml` and current Service Mapping source XML, including XML-bearing txt; current fingerprints and preflight evidence | Stop before source analysis or drafting | Apply the canonical XML-guide input preflight to the actual current files | Every checkpoint | resolve_rmcs_algorithm_contract |
| Proposal contract | Selected action identities; complete proposal version; source-resolution record references; target decisions; canonical final handoff | Return the missing facts/choices to the primary's saved stage | Complete the [handoff contract](../resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) without inventing source facts | proposal, approved_change or artifact_result | resolve_rmcs_mapping_contract |
| Exact approval evidence | Persisted complete proposal and approval reference, selected actions, current input fingerprints and approved local change/destination scope | Block local artifact preparation | Follow the XML-guide approval procedure; analysis/source-selection acceptance is not this approval | approved_change or artifact_result | verify_rmcs_approval_evidence |
| Actual local result | Already-created output path, output fingerprint, expression-comparison findings and approved XML delta | Block artifact handoff without claiming success | Caller supplies the actual local artifact; checkpoint reads and validates it only | artifact_result | verify_rmcs_artifact_result |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Identity, version and input shape | Require a passed current [input preflight](../resources/ora_algorithm_xml_guidance.md#input-preflight), including identity, highest-version and context checks | Every checkpoint | resolve_rmcs_algorithm_contract |
| Action and scope shape | Require the structurally selected action record and its dataset/cardinality evidence under [action selection](../resources/ora_algorithm_xml_guidance.md#select-the-action-by-structure) | proposal, approved_change or artifact_result | resolve_rmcs_algorithm_contract |
| Source decision record shape | Validate referenced records against the companion's [single source schema](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record), keeping unavailable evidence explicit | proposal, approved_change or artifact_result | resolve_rmcs_mapping_contract |
| Type and capacity evidence | Check each selected source and target against its evidenced scalar/complex shape, type, precision and capacity under the [target guide](../resources/ora_rmcs_data_model_reference.md); keep DATE distinct from TIMESTAMP and do not silently truncate or coerce | A proposal uses a typed source or physical target | resolve_rmcs_mapping_contract |
| Operation handoff shape | Require one row per retained/replaced/prepended/new operation in the [canonical handoff](../resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff), including applicable source/configuration and output fields | proposal, approved_change or artifact_result | |
| Exact approval linkage | Validate version, action and fingerprint linkage to the complete persisted proposal and approval evidence | approved_change or artifact_result | verify_rmcs_approval_evidence |
| Result expression and scope | Require the canonical decoded-expression comparison and allowlisted XML delta evidence, including unchanged earlier versions and unselected content | artifact_result | verify_rmcs_artifact_result |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An applicable input or output contract is missing | Blocked | Return missing fields and current phase; caller resolves them before a new checkpoint | |
| Intake passes without a Groovy proposal or approval | Valid for intake only | Return intake findings; later phases still require their own evidence | |
| Phase-applicable validation, dependency, design and execution gates pass | Checkpoint passed | Return phase, findings, evidence/decision references and remaining unverified claims; this is not Fusion validation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.VALIDATE_INPUT | step | 10 | validate_input | valid->RMCSALG.RESOLVE_EVIDENCE;invalid->RMCSALG.REPORT_ISSUES | none | stop | Validate only required groups and input shapes applicable to the declared rule_phase. |
| RMCSALG.EVALUATE_CHECKPOINT | step | 70 | evaluate_result | valid->RMCSALG.RETURN_RULE_RESULTS;invalid->RMCSALG.REPORT_ISSUES | RMCSALG.APPLY_DEFAULT | stop | Validate the phase result and applicable output fields after all reached gates; artifact_result includes the actual expression/delta comparison, not an artifact write. |
