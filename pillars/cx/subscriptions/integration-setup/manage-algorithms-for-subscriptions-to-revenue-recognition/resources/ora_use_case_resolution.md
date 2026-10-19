# RMCS Use-Case Resolution and Companion Handoff

The Algorithms skill owns the requirement, record-level outcome, action selection, computation, Groovy proposal and approved local artifact. The Service Mapping companion owns source/exposure/binding analysis and configuration prerequisites. This file owns the analysis routing and request/result contract; technical rules live in their linked guides.

## Start with current evidence

Apply [input preflight](ora_algorithm_xml_guidance.md#input-preflight) before detailed source analysis or Groovy drafting. Record the requested behavior, source business meaning, target meaning and record level without inventing omitted values. Derive the active action and cardinalities from the current highest eligible version.

## Input type classifier

| Input type | Information supplied | Primary routing decision |
|---|---|---|
| Type 1 | Target and source object/attribute are clear | Continue if current provider/access/binding evidence resolves the source; otherwise ask the companion the unresolved mapping question |
| Type 2 | Target and source object are clear; source attribute is unclear or unexposed | Invoke the companion for attribute/exposure analysis |
| Type 3 | Target and source term are clear; source object is missing | Invoke the companion for functional source-owner analysis; do not default to an alias |
| Type 4 | Source object/attribute and target are unclear | Primary resolves target meaning/level; companion resolves source candidates; combine the decisions on return |
| Type 5 | Only a business outcome is supplied | Clarify the RMCS outcome and record level, then delegate source discovery and resume with the findings |

For any Service Mapping question about source entities, custom attributes, describe metadata, source XML, VO mappings, service access or publication prerequisites, invoke the RMCS companion. Never redirect it to the AR companion. ProductAssociations/BillLines function semantics and action cardinality remain owned by the primary; the companion can resolve their metadata without inventing mapping entities.

## Source-object discovery when no object is named

Provide the companion with the business term, requested record level and any known source/target evidence. Ask for candidates ranked by functional fit, not just matching field names. The result must distinguish source business object, current action alias/provider, actual VO/REST field, type, access/exposure and evidence.

Use the companion's canonical [source-resolution record and decision policy](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record) for every business source used by new Groovy. Carry its record references through analysis, approval and the final handoff; do not create a second source-decision schema here. The current files and recorded implementer choices establish local authoring evidence, not proof of Fusion publication. Keep accepted and rejected choices with their evidence. An optional source remains that owner with null-safe handling; it is not replaced by a required object's same-name attribute. A literal is allowed only when the implementer actually requests a constant.

## Evidence sequence

| Decision | Canonical owner |
|---|---|
| Input identity, highest version, action and current-row scope | [Algorithm XML guidance](ora_algorithm_xml_guidance.md) |
| Source exposure, provider/access and optional describe | [Service Mapping guidance](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md) |
| Target meaning, direct write versus insert, contexts and subline limits | [Data-model guidance](ora_rmcs_data_model_reference.md) |
| Existing code, source nullability, collection behavior, functions and layout | [Groovy guidance](ora_groovy_function_guidance.md) |
| Complete proposal approval and local XML verification | [Approval and local artifact](ora_algorithm_xml_guidance.md#approval-and-local-artifact) |
| Final operation traceability and source configuration handoff | [Final traceability and configuration handoff](#final-traceability-and-configuration-handoff) |

If the target is omitted, follow [target resolution](ora_rmcs_data_model_reference.md#target-resolution-when-omitted). If a required ordinary source exposure is not yet configured, consume the companion's [_Custom exposure handoff](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#custom-source-exposure-for-ordinary-service-mapping-attributes): return the exact configuration prerequisite, including object/entity, proposed `<sourceAttributeName>_Custom` alias, VO attribute and service access. Hold dependent drafting/artifact completion unless the implementer explicitly asks to proceed with that named assumption. When proceeding on assumption, keep the Groovy/XML proposal conditional, include the Service Mapping implementer steps, and request updated current evidence after the implementer completes it. Analysis of a prerequisite is not evidence of deployment.

## Companion request record

Supply service_mapping_analysis_request before delegation and retain the continuation state. This is an internal analysis record, not a Fusion payload.

| Field | Primary supplies |
|---|---|
| request_id | Identifier for this mapping question, echoed in the result |
| caller_skill_id | cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-revenue-recognition |
| resume_stage | Exact primary processing stage to continue after the result |
| requirement_and_scope | Business rule, desired outcome and record level |
| mapping_question | Specific unresolved source, exposure, binding, access or configuration question |
| known_facts_and_evidence_refs | Current validated input references/fingerprints, preflight result, selected version/action, known sources/targets and their evidence |
| source_resolution_record_refs | Existing records under the companion's canonical source-resolution contract, including supplied choices and unresolved recommendations; reuse them without asking for the same decision again |
| prior_decisions | Accepted/rejected alternatives, null/collection decisions and changed requirements |
| describe_scope | If needed, approved project/environment identity and precise metadata question; otherwise supplied-evidence-only |

Unknown facts remain explicitly unresolved, not fabricated to fill a record. Do not include credentials or customer payloads in reusable files.

## Companion handoff template

Return service_mapping_analysis_result to the waiting primary automatically on every outcome. Echo request_id, caller_skill_id and resume_stage.

| Field | Result content |
|---|---|
| outcome | analyzed / needs_decision / prerequisite_pending / blocked / declined |
| source_resolution_record_refs | References to the companion's canonical records for every business source, carrying their actual decision and exposure state; a reference does not promote an assumption to a confirmed source |
| confirmed_sources | Source-record references whose required identity, type, decision and exposure evidence is resolved; render their source summaries from those records |
| bindings_and_access | Current context/consumer, source joins/relationships and access; report action-cardinality evidence separately from describe metadata |
| exposure_and_prerequisites | Existing exposure and exact remaining configuration, deployment or evidence requirement; do not claim it was performed |
| target_findings | Confirmed mapping-side target alias/access and unresolved physical/semantic questions for the primary |
| alternatives_and_assumptions | Named alternatives, uncertainties and accepted/rejected choices |
| unresolved_items | Exact missing fact, decision or contract with a safe next action |
| evidence_refs | Current input fingerprints, relevant XML locations and any permitted redacted metadata evidence |

The companion does not approve Groovy, edit Algorithm_BO.xml or publish mappings.

## Automatic return and further processing

Consume the result at the saved primary stage without asking the implementer to invoke either skill again:

- analyzed: use confirmed findings, retain assumptions separately, recheck target/action prerequisites and proceed to the permitted Groovy proposal.
- needs_decision: present the exact choice in the primary, retain context and continue after the answer.
- prerequisite_pending: explain the missing configuration/evidence and hold only its dependent branch until verified, unless the implementer explicitly accepts a named assumption path; then continue only as conditional and keep runtime readiness pending.
- blocked: report the failed validation or missing contract and safe correction; do not substitute another version or live route.
- declined: retain the rejected candidate and ask whether to revise the requirement, choose a supported alternative or stop that branch.

Do not automatically ping-pong. Another companion pass needs a new question, changed evidence or a new user decision. A returned analyzed status is neither XML approval nor proof of Fusion execution readiness. Use the separate [approval gate](ora_algorithm_xml_guidance.md#approval-and-local-artifact) before creating a local artifact.

During implementation runs, persist durable decisions, handoffs and redacted run/token records through the selected project workflow. Authoring these reusable instructions does not itself create an implementation project.

## Final traceability and configuration handoff

This is the single final handoff contract for both skills. The primary combines the companion's source records and configuration findings with its algorithm/output decisions. Show the complete handoff in chat, with one row per proposed output operation. Distinct conditional writes remain distinct rows even when they share a target. Reuse each row's operation_id across the proposal, approval and conditional local artifact; do not substitute one summary row per source or attribute for operation-level traceability.

| Row field | Content and owner |
|---|---|
| operation_id and requirement | Primary: stable operation reference, requested behavior and expected record-level result |
| source_resolution_record_refs and source_summary | Render each participating source's functional owner, exact attribute, alias/provider, datatype and action scope/cardinality from the canonical records. The companion owns source findings and the primary supplies action/cardinality facts; reusing resolved evidence does not require another companion call. Use N/A for requested literals or supported, approved runtime-derived expressions with no business source; required helper/type evidence remains in value_and_conflict_decisions |
| source_configuration | Companion: entity/alias and mapping type, VO attribute, joins, entity/attribute access, existing versus proposed configuration, publication evidence/prerequisites and remaining implementer actions. For an ordinary unexposed source, include the proposed `<sourceAttributeName>_Custom` alias, exact VO attribute, Services read/write handoff and refreshed-source evidence requirement from the companion. For function-backed inputs, reference the primary's confirmed function-provider facts and mark inapplicable Service Mapping additions N/A |
| algorithm_selection | Primary: exact algorithm identity, selected highest version, structural step/action identity and document/line/subline level |
| target | Primary: named semantic target and supported physical object/column; companion supplies the actual mapped output alias/attribute and access evidence when applicable. Keep physical equivalence unresolved when unproven |
| output_route | Primary: direct assignment, output-control assignment or supported header/line insert, with the approved condition and value expression |
| insert_fields | Primary: actual AttributeName, AttributeValue expression, AttributeContext, SourceId, TransactionType and FlexContext from the approved insert. Distinguish an omitted key from a null value. For direct/control assignments, mark these insert-only fields N/A instead of inventing insert metadata |
| value_and_conflict_decisions | Primary: null/collection handling, required conversion evidence and accepted condition or precedence for overlapping writes, following the Groovy guide |
| evidence_and_acceptance | Both: input fingerprints, source/target decision references, relevant XML/describe/documentation evidence, named assumptions and their accepted review-only scope, proposal version and approval reference |
| prerequisites_and_artifact | Both: unresolved configuration/context/runtime prerequisites, responsible next action, operation status, conditional local XML reference and its comparison result. State explicitly when no XML was created, when an artifact was produced under a named Service Mapping assumption, and when Fusion behavior remains unverified |

Use the [source-resolution record](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record), [output routing](ora_rmcs_data_model_reference.md), [Groovy review](ora_groovy_function_guidance.md) and [approval procedure](ora_algorithm_xml_guidance.md#approval-and-local-artifact) as the owners of the decisions rendered in these fields. The handoff records those decisions; it does not authorize a new mapping change or duplicate their rules.

Keep the chat-visible handoff aligned with the exact proposal version and, when created, the approved local XML. During a runtime implementation, persist its permitted content through the selected project's artifact/version services together with the proposal/approval references and redacted run/token records. An analysis-only or blocked handoff must retain its unresolved statuses. Apply the approval procedure's sensitive-persistence gate when exact proposal or handoff evidence cannot be retained under project policy; do not store customer payloads or treat a redacted approximation as an exact approved artifact. Do not infer manual export/import UI steps from AR; use the [remaining RMCS evidence index](ora_subscription_management_general_reference.md#remaining-rmcs-evidence).

## Documented acceptance cases

These are expected cases for later review, not executed tests, generated customer artifacts or evidence that Fusion accepted a change. Apply the linked canonical rules; skill authoring records these expectations only.

| Case | Expected outcome and evidence |
|---|---|
| Current input missing, wrong integration identity, or highest version inactive | Preflight stops with the exact correction; no older-version fallback or dependent drafting |
| Implementer already supplies an exact source | Source record preserves the supplied decision without asking again; exposure/type/action evidence is checked separately |
| Discovery produces one new semantic candidate or several alternatives | Source record retains the recommendation and requires named acceptance; a sole match or generic assumptions do not count as selection |
| Named object versus objectless business term | Named object is inspected first; objectless discovery records relevant source-family coverage and rejected alternatives under the companion guide |
| Describe returns a scalar, object or collection | Candidate evidence identifies the metadata shape, supported scalar child when applicable, type/queryability and compatibility with the proposed provider operation |
| No match, ambiguity, missing exposure, or unavailable describe | Companion preserves the distinct result and corrective action; primary consumes it without inventing a source or silently choosing an assumption path. If the implementer explicitly accepts a named assumption, the primary may continue conditionally while keeping exposure and runtime readiness pending |
| BillLines or ProductAssociations is supplied by an algorithm function | Function/provider evidence determines availability; no invented mapping entity or sales-credit endpoint |
| Target omitted or direct/insert routes differ | Named target, source type, physical support, output access and deployed context/slot decisions follow the data-model guide; direct-write rows show insert fields N/A and sublines never use insert |
| Optional or collection source, or date/timestamp value | Groovy proposal records the applicable null/collection and conversion/helper evidence from the Groovy guide; no datatype inferred from a name |
| Retained and proposed writes overlap | Operation rows expose the semantic target and row scope; approved exclusive conditions or supported precedence resolve the overlap before approval |
| Exact approved expression is serialized as escaped text or CDATA with different newline encoding | Namespace-aware extraction yields the same decoded expression after CRLF/CR-to-LF normalization only; XML preservation checks still apply |
| Extracted expression differs in spaces, comments, literals or other non-newline text | Artifact handoff stops until the artifact is corrected to the approved expression or a revised proposal is approved |
| Required exact proposal/approval evidence cannot be persisted safely | Local XML creation stops with artifact-persistence status; no silent redaction, substitute destination or bypass of the evidence requirement |
| Line extension context or new subline row identities are unresolved | Only the dependent operation remains blocked; request the exact missing RMCS evidence |
| Companion returns analyzed, needs_decision, prerequisite_pending, blocked or declined | Every outcome returns once to the saved primary stage with record references; another companion pass requires a new question, decision or evidence |
