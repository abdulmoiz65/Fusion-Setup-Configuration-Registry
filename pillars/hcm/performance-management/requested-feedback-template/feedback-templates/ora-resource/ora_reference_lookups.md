# Feedback Templates Reference Lookups

Source: Request Feedback Template Best-Practice Reference, sections 7–9 and 14–15.

The Feedback Templates task delegates tenant reads to declared provider routes.
It does not own questionnaire lifecycle or invent product endpoints.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_questionnaire_readiness | A template is created or its questionnaire changes | Requested questionnaire name or portable key | `GET /hcmRestApi/resources/11.13.18.05/questionnairesLOV` through `hcm.hcm-tool.questionnaire.questionnaires` and `core.fusion-api.rest-api-client`; conditional provider identity read below | Exact identity, context, status, latest/effective state, and eligibility evidence | One exact eligible LOV match supplying the required reference, or one eligible provider identity match resolving missing evidence | Sanitized questionnaire identity and readiness result | Exhaust the declared alternatives below; do not ask the consultant to collect ordinary evidence first. |
| resolve_specific_manager_type | A template create or manager-type change is proposed | Specific Manager Types display label or code | `core.fusion-api.apps-common.lookups` against `/fscmRestApi/resources/11.13.18.05` with `LookupType=PER_SUPERVISOR_TYPE` | LookupCode, Meaning, and available enabled/effective fields | One exact match plus one eligibility alternative below | Sanitized canonical code and eligibility basis | Do not guess codes; exhaust supported reads before classifying an unresolved technical dependency. |
| resolve_feedback_templates_route_supportability | A task-declared REST write is proposed | Configured target, declared route and method, capability evidence | Inspect retained evidence, then fresh GET through `core.fusion-api.rest-api-client` | Target base-URL identity, version, method, path, capability source and compatible GET | Same target and method with one capability alternative below; governance confirmation only when explicitly required | Sanitized capability and governance results | Stop the dependent action only when alternatives are exhausted or contrary evidence exists; never reuse another environment's route UUID. |
| resolve_tenant_runtime_readiness | Redwood, goals, notifications, TDS, VBS, or security behavior is in scope | Requested runtime scenario and tenant | TBD | UI mode, relevant configuration, authorization evidence | Exact scenario and target tenant | Readiness evidence and gaps | Stop with dependency blocker; do not infer a value from release number. |
| resolve_goal_activation_impact | Performance Goal Feedback activation is proposed | Exact target template and tenant | TBD | Current active template state and activation impact | Exact target identity | Impact summary for preview and approval | Stop with dependency blocker; do not activate or assume singular state. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A caller asks to resolve and validate a source-supplied dependency | Use the declared REST/provider route as an agent-owned read-only validation step without consultant approval; do not defer the read to the consultant. |
| The provider reports a documented discovery-contract gap | First apply the evidence alternatives below using declared reads. If unresolved, record the exact missing capability as a skill limitation; do not ask the consultant to collect ordinary tenant evidence or invent an endpoint. Block only the dependent action. |
| An identifier is partial, missing, or ambiguous | Resolve source-supplied names through declared lookups first. Ask for the intended business identity only if the source is insufficient or several valid candidates remain; never choose a likely match or ask for an agent-resolvable ID. |
| A tenant-specific Feedback Templates REST write is proposed | Resolve and persist `resolve_feedback_templates_route_supportability` before showing a preview or seeking write approval. Route evidence does not authorize the write. |

## Resolution procedure

Read configured environment properties through the selected core workflow;
do not print credentials. Inspect the exact provider contract and supported
filters, field projections and pagination before interpreting an empty or
partial result. Use only declared endpoints through the selected client.
Record attempted reads, target identity, timestamps, returned facts, missing
fields, chosen alternative, contrary evidence and outcome. Do not repeat the
same failed query or use a POST/PATCH as a capability probe.

Inspect retained same-target records when relevant. Match the resolved base URL
(an alias alone is insufficient), resource version, relative path, method and
affected reference. Historical evidence must include successful response and
verification readback; it never replaces current identity/eligibility reads,
current authorization checks, approval, or an explicit restriction. Reject
evidence invalidated by a route, release, security or configuration change.

Classify outcomes as `RESOLVED`, `CUSTOMER_DECISION_REQUIRED`,
`SKILL_LIMITATION`, or `VALIDATION_FAILED`. Only a missing business value,
ambiguous user intent/target, or an explicitly required governance decision
belongs to the customer. A permission failure remains auth/authz; a missing
field or unavailable technical route is not a request for customer evidence.
Continue independent tasks. Persist the selected resolution with the preview
and reuse it unless a relevant change or freshness requirement invalidates it.

## Questionnaire reference alternatives

These alternatives establish identity and lifecycle readiness, not by themselves
eligibility for the selected feedback-template type. Also apply the
[association compatibility gate](#template-type-association-compatibility).

This consumer selects an existing questionnaire; it does not inherit the
questionnaire provider's lifecycle/CRUD validation requirements.

1. Accept exactly one exact-name or exact-key `questionnairesLOV` match when
   it returns the `QuestionnaireId` required by the Feedback Templates payload,
   active/eligible status, applicable latest/effective version evidence, and
   enough context to identify the intended questionnaire. Resolve subscriber
   ambiguity when present; do not require a field irrelevant to this reference.
2. If evidence is missing or conflicting, inspect the provider's declared
   `/questionnaires` query using actual returned `SubscriberCode`,
   `QuestionnaireCode` and `VersionNumber`. Do not substitute a surrogate ID
   for a portable code, invent a missing key, or guess filter fields.
   Use supported projections/pagination to distinguish omitted data from no match.
3. A zero-row secondary query does not negate a complete eligible LOV result.
   Record the query discrepancy and accept alternative 1 when it independently
   passes. An explicit inactive, wrong-context or conflicting-identity result
   does block; do not choose the more permissive response.

Use the currently resolved target ID in the payload, never one copied from a
previous run. Multiple exact matches or an ineligible selection remain failures.
If neither alternative establishes eligibility, report a skill limitation or
the observed validation failure with the attempted queries.

## Manager-type eligibility alternatives

Require one exact current label/code match under `PER_SUPERVISOR_TYPE`.
Accept either documented eligible-LOV semantics, explicit enabled/effective
fields, or (when these fields are absent) current exact lookup resolution plus
retained same-target verified template acceptance of that canonical code.
Inspect provider-supported detail reads if these alternatives are insufficient.
An explicit disabled/expired value or conflicting code blocks regardless of
history. `LINE_MANAGER` is not a hard-coded default.

## Route capability alternatives

A fresh compatible collection GET is required but cannot establish route
write capability by itself. Combine it with one of:

- Target-bound declared method metadata or an applicable supported operation
  contract establishing the method on the selected route/version.
- Retained successful same-target, same-method execution and exact verification
  readback on this route/version, with no intervening invalidating change.
- An existing affirmative route-owner artifact matching the selected target,
  route, version and proposed method.

The reusable sample route and a GET alone are insufficient. A prior POST does
not prove PATCH capability. Evidence of technical success does not establish
formal vendor support or waive governance. Check applicable project policy:
require owner confirmation only when it explicitly requires it; do not invent
a policy or ask for a new artifact when existing valid evidence suffices.

## Conditional route-owner confirmation evidence

First inspect existing project/onboarding evidence. When formal confirmation
is explicitly required and absent, the designated owner supplies an artifact
through normal source intake. It must identify `target_environment_alias`,
`collection_relative_path`, `resource_version`, `owner`, `confirmed_at`,
`supportability_confirmation`, and `source_reference`, with
`resolved_base_url` and `method` binding. Require an affirmative
confirmation for the exact target, route and method and retain its provenance under the
project workspace. Do not store tenant-specific confirmation in reusable skills.

A collection GET proves current compatibility only. Match the artifact to
the resolved base URL and contract path/version/method, then combine it with
current-run GET evidence. Missing confirmation blocks only when policy
requires it or no other capability alternative resolves the operation.
Withdrawn or conflicting evidence must be resolved, not bypassed by history.

## Template-type association compatibility

This is a local evaluation of retained, provider-verified evidence, not a new
Fusion endpoint.
Use it before the parent delegates new-questionnaire preview/submission and
before template POST or questionnaire/type-changing PATCH. Resolve the effective
template type from the requested create or the current exact PATCH target plus
proposed changes. Do not impose this gate on unrelated name/description edits.

1. Obtain identity, subscriber, status and current version from the existing
   provider alternatives above. For a proposed questionnaire, its provider must
   validate the intended lifecycle values, source questionnaire template and
   requested question design before marking `provider_ready` true.
2. Apply the declared type-specific policy to current target-bound provider checks.
   For new General Feedback, the agent assembles `provider_validation` from actual
   subscriber, strict live schema, references, design, lifecycle and identity
   validation, bound to the complete specification. The resolver generates
   policy provenance; no existing questionnaire ID/history or user attestation
   is needed. Explicit contrary restrictions still block. For other evidence
   modes, establish a type-specific rule using an applicable target-bound contract
   or an authoritative owner confirmation. Evidence must state the permitted
   subscriber and whether eligibility is limited to exact questionnaire IDs,
   requires derivation from specified questionnaire templates, or (for General
   Feedback only) permits eligible questionnaires of the specified subscriber.
   Generic Questionnaire creation documentation is not association evidence.
3. As an alternative for an existing reference only, retained successful
   association plus exact verification readback on the same target/type/version,
   revalidated in this run with no invalidating change, proves that exact ID.
   A genuinely type-filtered, provider-declared eligible LOV can likewise prove
   exact IDs; the generic `questionnairesLOV` is not such a LOV. Do not invent
   a type filter or infer an exclusive list from a sample of existing templates.
4. For Performance Goal Feedback, resolve only the seeded questionnaire with
   code `PERF_GOAL_QSTNR_V1` under HRA. Custom questionnaires and derivatives are
   unsupported for this association. Positive history, owner assertions or a
   same-family questionnaire template cannot override this product rule. Reject
   custom intent during intake; never probe support using a POST/PATCH. General
   Feedback remains eligible for custom questionnaire creation and association.
5. Normalize the evidence below, run the validator, and persist its input/output
   with the project dependency specification or immutable REST preview. Rerun
   after questionnaire creation using current readback. Check every dependent
   template type separately. An `eligible` result permits only the next existing
   workflow gate, never a write without its provider/REST approval checks.

Run from this setup-task folder:

```sh
python3 scripts/validate_questionnaire_compatibility.py --input /absolute/project/evidence.json
```

The command is offline/read-only, prints JSON, exits 0 only for `eligible`, and
exits 2 for `ineligible` or `unresolved`. It does not collect or authenticate
evidence; the executing agent must inspect the referenced authoritative source,
normalize it truthfully, and resolve contradictions before marking it verified.
For execution, use `scripts/run_feedback_workflow.py`, which calls the resolver
and validator internally at both declared gates. The standalone validator is a
diagnostic, not an execution route. Generic REST and standalone Questionnaire
providers remain unchanged. Never fabricate attestations to pass.

### Type-specific selection resolver

`scripts/resolve_questionnaire_compatibility.py` reads the selection policies in
`ora_rest_execution.json`. General Feedback uses an active/latest HRA candidate;
new General Feedback questionnaires require a provider-validated design.
The Performance Goal Feedback policy requires the seeded `PERF_GOAL_QSTNR_V1`;
it resolves the tenant ID through the declared LOV, never an example ID. The
[QuestionnaireSD.xml seed record](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBHCMBRONZE_LINUX.X64/fusionapps/hcm/hrt/db/data/HcmProfileTop/HcmProfileQstnrTop/HcmProfileQstnrLibrary/QuestionnaireSD.xml#2850)
establishes its seeded identity. The captured goal-selection rule and recorded
Fusion validation establish the association restriction; seeded status alone
does not imply that every seeded object has the same restriction. Apply this
known rule during intake without requiring a live rejection first. Current
target evidence remains required to resolve the seed ID and readiness. Missing
seed data blocks setup; do not create a replacement or change policies to pass.

An unknown ID outside non-exhaustive successful history is `unresolved`, not
`ineligible`. Only an authoritative exhaustive rule mismatch or a reviewed,
same-target exact rejection proves that negative conclusion. Rejection records
are separate from positive history and invalidate reuse of that candidate.
Creation, question-content verification, association and association readback
are separate milestones; creating a questionnaire never completes association.

## Local Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_questionnaire_association_compatibility | Before dependent creation or association | Reviewed provider evidence and applicable association contract | Local scripts/validate_questionnaire_compatibility.py; no external call | Normalized evidence below | Exact context, type, stage and candidate satisfy the evidenced rule | status, gate_passed, input_sha256 and errors | Fail closed; resolve unknown or conflicting evidence through declared providers only |

### Normalized evidence contract

All IDs/codes are nonempty strings resolved in the selected target, never
hardcoded in reusable rules. Boolean fields require JSON booleans, not strings.

| Field | Contract |
|---|---|
| template_type | ORA_GENERAL or ORA_PERF_GOAL |
| stage | before_questionnaire_creation or before_association |
| context | base_url, resource_version and current run_id; non-secret exact identity |
| candidate | code, subscriber_code, active, latest, provider_ready; id required for association; template_code required for derived-template rules or when the provider marks template_required=true |
| candidate provenance | context matching the root, source_ref, verified=true, conflicting_evidence=false; creation uses verified provider design, association uses current exact readback |
| association_rule | template_type, mode, subscriber_codes and provenance as below |
| rule provenance | context matching the root, source_ref, source_kind, verified=true, conflicting_evidence=false |
| source_kind | target_contract, owner_confirmation, verified_association or type_specific_lov |
| mode=exact_questionnaire | questionnaire_ids; known eligible exact IDs, not necessarily an exhaustive set; cannot authorize creating another identity |
| mode=derived_template | General Feedback only; template_codes from provider rules, not inferred template similarity; never eligible for Performance Goal Feedback |
| mode=eligible_subscriber | General Feedback only; explicit association contract, not generic subscriber membership |
| new_questionnaire_supported | Must be explicitly true for creation under a supported rule; false blocks, absent is unresolved |

`verified_association` and `type_specific_lov` support only `exact_questionnaire`.
For `derived_template` or `eligible_subscriber`, require `target_contract` or
`owner_confirmation` that actually establishes that rule. A new-questionnaire
gate never permits an exact-existing-ID-only rule. Performance Goal Feedback
always uses exact seeded identity evidence and never permits new creation.
Active/latest fields before
creation describe provider-validated intended values, not existing Fusion data.

Output includes status, gate_passed, stage, target context, candidate identity,
structured errors and input_sha256. This digest detects changed evidence input
using sorted JSON; it is **not** the REST contract's JCS payload digest or approval.
Keep the actual outgoing QuestionnaireId and TemplateType bound to the evaluated
candidate/type; changed target, type, candidate or rule requires reevaluation.
Any goal-association rejection such as HRA-960540 invalidates the corresponding
eligibility evidence; resolve it before reuse, never choose a permissive source.

This contract overrides the canonical best-practice reference's generic
questionnaire creation/replacement guidance where that guidance does not cover
type-specific constraints. It does not modify that integrity-protected source.

## All and specific manager selection

All maps directly to `ShareWithManagers: "ALL"`, as confirmed by the implementation owner. Do not look up ALL or expand it. For specific selections use GET `/fscmRestApi/resources/11.13.18.05/commonLookupsLOV` with `fields=LookupCode,Meaning`, `finder=LookupTypeFinder;LookupType=PER_SUPERVISOR_TYPE`, `onlyData=true`, and complete limit/offset pagination through the core client with framework version 9. Match exact normalized names/codes, reject ambiguous/missing/duplicate selections, and join codes in source order. All mixed with specific selections is invalid. The previously declared richer lookup remains available for required enabled/effective checks.

## Provider-generated General policy evidence

When `policy_evidence` is absent for ORA_GENERAL, the resolver consumes a fresh reviewed `provider_validation` receipt: provider identifier, matching context and source provenance, candidate_code, subscriber_code HRA, checks for subscriber/schema/references/design/lifecycle/identity, restrictions_resolved, and (before creation) specification_sha256. The agent must obtain each fact through the owning provider's declared read-only workflow. Never create a passing receipt from the policy file alone. Current identity/readback and the independent before_association gate remain required after creation. This local receipt is reviewed evidence, not authenticated vendor certification.

## Provider design option discovery

For agent-selected questionnaire settings, use live Questionnaire attribute metadata LookupName values with the core commonLookupsLOV LookupTypeFinder read to retrieve supported privacy, layout, section presentation/order, question order/type and lifecycle choices. This read-only delegation validates exact target options; it does not introduce a mutation route. Direct-question category discovery uses the provider questionnaireFoldersLOV read, same subscriber, ContainQuestions=Y; root category uses ContainQuestionnaires=Y. Select supported values under the user's delegated design authority, then validate the complete specification through the unchanged provider.
