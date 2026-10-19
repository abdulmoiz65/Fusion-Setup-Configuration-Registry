# RMCS Algorithm Design Enforcement

## Scope

Owns checkpoint policy predicates; detailed RMCS behavior has one canonical owner in the linked supporting guides. [Reference lookups](ora_reference_lookups.md#source-catalogue) retains the physical-source ledger. AR similarities are not evidence for RMCS Groovy, contexts, defaults or operations.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish request and action scope | Use the validated current inputs and structural action selection |
| 2 | Check source and target decisions | Apply accepted source evidence and RMCS output eligibility |
| 3 | Review final behavior | Apply runtime, null/cardinality, collision and existing-code policies |
| 4 | Enforce approval/artifact boundary | Allow only the exact supported local proposal and disclose remaining live-state uncertainty |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every checkpoint | Error | resolve_rmcs_algorithm_contract | Wrong input identity, stale evidence or fallback to a lower eligible version | Follow the [canonical preflight](../resources/ora_algorithm_xml_guidance.md#input-preflight) | Request corrected current input only |
| proposal, approved_change or artifact_result | Error | resolve_rmcs_mapping_contract | A recommended source is treated as accepted, metadata as scalar/queryable without evidence, or a function-backed input is incorrectly treated as a missing mapping entity | Apply the companion's [source decisions and analysis](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md) | Resolve only affected evidence/decisions through the primary |
| Selecting or validating a proposal's target | Error | resolve_rmcs_mapping_contract | A target bypasses source type, standard-first candidate review when the target is omitted, capacity, writable-output, supported-extension or deployed-slot/context evidence | Apply the [target recommendation and eligibility procedure](../resources/ora_rmcs_data_model_reference.md); a supplied exact target requires eligibility checks, not a repeated recommendation decision | Named evidence-backed proposal only; next-slot suggestions for DFF/flex requests must remain conditional assumptions |
| Selecting or validating a line DFF/flex target | Error | resolve_rmcs_mapping_contract | A new line DFF/flex requirement writes directly to an existing mapped `RmcsDocLines.SrcAttribute*` slot, or fails to skip mapped line slots when selecting an assumption-backed next slot, unless the implementer explicitly requested modification of that exact slot | Apply the [line DFF/flex routing rule](../resources/ora_rmcs_data_model_reference.md#direct-assignment-or-additional-detail-insertion): mapped line slots are occupied; new line DFF/flex values use the next compatible SRC_ATTRIBUTE slot not present in Service Mapping and the line `RMCSInterface.insert` contract | Revise to a documented insert proposal or capture exact-slot modification approval |
| Drafting or validating Groovy | Error | resolve_rmcs_algorithm_contract | Unsupported helper, scope/cardinality assumption, unsafe optional dereference, invented type conversion or inherited AR runtime behavior | Apply [RMCS Groovy guidance](../resources/ora_groovy_function_guidance.md), including the user-specified DATE versus TIMESTAMP policy | Revise the proposal with supported behavior, then renew approval when required |
| Drafting or validating DATE/TIMESTAMP comparisons | Error | resolve_rmcs_algorithm_contract | A DATE field or DATE-derived expression is compared without `toDate(<derived date value>)`, or is compared to `now()` for present-date logic; a TIMESTAMP value is unnecessarily wrapped in `toDate` | Apply [DATE and timestamp value handling](../resources/ora_groovy_function_guidance.md#date-and-timestamp-value-handling): DATE comparisons use `toDate(...)` and `today()`, while implementer-confirmed TIMESTAMP comparisons stay unwrapped and may use `now()` | Revise the temporal comparison, then renew approval when required |
| Retaining or adding operations | Error | resolve_rmcs_algorithm_contract | Overlapping writes to the same semantic field/row/context lack accepted exclusivity or evidence-backed precedence | Complete the Groovy guide's collision review for retained and new operations | No assumed last-write-wins |
| Producing a final proposal | Error | | Code-treatment choice, complete chat-visible expressions, exact scope or configuration handoff is missing | Follow [use-case resolution and final handoff](../resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) | Resolve choices before final approval |
| Proposing a missing subline step or physical output | Error | resolve_rmcs_algorithm_contract | Step 2 is missing/duplicated/structurally ambiguous, unresolved insert context, protected-definition edit or direct subline insert is proposed | Use [XML structure guidance](../resources/ora_algorithm_xml_guidance.md#missing-subline-step) and the data-model guide; when subline logic is needed and Step 3 is absent, clone the unambiguous highest-version Step 2 locally, add the `RmcsDocSublines` data set, generate new row UUIDs and add approved subline Groovy | Supported local XML clone after explicit approval |
| approved_change or artifact_result | Error | verify_rmcs_approval_evidence | Exact proposal, fingerprints, scope, destination or approval reference changed or cannot be retained safely | Follow the [approval/artifact procedure](../resources/ora_algorithm_xml_guidance.md#approval-and-local-artifact) | Stop artifact creation pending correction or renewed approval |
| artifact_result | Error | verify_rmcs_artifact_result | Decoded expressions or semantic XML changes differ from the approved scope | Apply the XML guide's exact comparison and correction/reapproval procedure | Never rewrite the approval snapshot to match unintended edits |
| Claiming publication, deployment, setup readiness or integration success | Error | | Current local files, user choices or a passed checkpoint are used as proof of live Fusion state | Disclose what is locally evidenced and keep unsupported operations separate | No inferred live success |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_rmcs_algorithm_contract | Current input, action and runtime-scope checks | Current structural preflight and selected-action evidence | ora_reference_lookups.md |
| resolve_rmcs_mapping_contract | Source and target checks | Current mapping/source decisions and distinct exposure/publication evidence | ora_reference_lookups.md |
| verify_rmcs_approval_evidence | Approved local change gates | Exact persisted approval linkage and scope | ora_reference_lookups.md |
| verify_rmcs_artifact_result | Local artifact-result gates | Actual approved-expression and XML-delta comparison | ora_reference_lookups.md |

## Separate integration policies and unresolved contracts

These physical/integration facts remain applicable if a separately supported workflow reaches them; they are not requirements to query Fusion before local authoring.

| Preserved fact or boundary | Evidence and limit |
|---|---|
| Subscription eligibility | S1 requires both header and associated product Active for integration; current local algorithm files do not establish those lifecycle states |
| Extraction Start Date | S2C says it is disabled and unnecessary for the Oracle Subscription Management source document type; no automatic setup change |
| Physical extension meanings | S5 source slots may already carry charge/pricing/asset/product meanings; never assume unused slots or same-number source/target correspondence |
| Subline satisfaction | Source/target columns alone do not establish a transformation, permitted bounds or a direct insert |
| Remaining RMCS authoring evidence | See [one evidence-gap list](../resources/ora_subscription_management_general_reference.md#remaining-rmcs-evidence); each gap blocks only its affected operation |
| Future live operations | See [unsupported live contracts](ora_reference_lookups.md#unsupported-live-contracts); no currently declared local node implements them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.ENFORCE_DESIGN | step | 40 | design_enforcement | passed->RMCSALG.CHECK_EXECUTION_CONTRACT;blocked->RMCSALG.REPORT_ISSUES | RMCSALG.CHECK_DEPENDENCIES | stop | Apply only policy predicates relevant to rule_phase and requested operations; linked guides own detailed behavior. |
