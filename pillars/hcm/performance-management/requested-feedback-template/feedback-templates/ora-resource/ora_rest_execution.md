# Feedback Templates REST Execution

Use this REST-only contract for General and Performance Goal Feedback Templates.
Reject template FSM/CSV import/export, HDL/HSDL, and Data Loader requests with
`UNSUPPORTED_EXECUTION_CHANNEL`; no alternate execution channel is declared. The machine-readable authority is
[`ora_rest_execution.json`](ora_rest_execution.json); it is based on the
consultant-supplied REST evidence for the current target tenant, not on the
functional configuration document.

## Operations and routing

| Operation | Method | Route | Scope |
|---|---|---|---|
| `list_templates` | GET | Declared collection path | Read current templates and resolve an exact name or ID. |
| `get_template_by_exact_name` | GET | Declared collection path with exact `q` and `fields` query parameters | Validate exactly one template and request all fields required by the template type. |
| `create_general_feedback_template` | POST | Declared collection path | Create only a General Feedback template. |
| `create_performance_goal_feedback_template` | POST | Declared collection path | Create only a Performance Goal Feedback template. |
| `patch_feedback_template` | PATCH | Fresh canonical item path returned by the exact preceding GET | Update one exact existing template. |

Every request uses `REST-Framework-Version: 9` through
`core.fusion-api.rest-api-client`. The route is target-bound: execute a fresh
collection GET against the declared path before a write. A 404, incompatible
resource shape, target mismatch, or read authorization denial is a transport or
authorization blocker; do not guess a version, UUID, or alternate endpoint.
The collection GET establishes authenticated read access, not POST/PATCH
privilege. No separate read-only write-privilege endpoint is declared. After
approval, Fusion decides write authorization on the single dispatched request;
record 401/403 as auth/authz and retain the attempt marker without retry.

## Tenant-specific route evidence

This route is tenant-specific. Before any write, retain a sanitized record of
the non-secret target environment alias, Fusion release or REST resource
version, resolved base URL identity, proposed method, one capability alternative
from `ora_reference_lookups.md`, and a fresh collection GET timestamp, HTTP
status, and compatible response-shape summary. Require route-owner confirmation
only when explicit project governance requires it. A GET alone does not prove
write capability; technical success does not establish formal vendor support.
This evidence does not substitute for write approval. Exhaust the declared
alternatives before reporting a skill limitation. Do not copy a route UUID,
version, method capability, or compatibility conclusion to another environment.

## Canonical payload integrity

For every POST or PATCH preview, canonicalize the request body with RFC 8785
JSON Canonicalization Scheme (JCS), encode the canonical bytes as UTF-8, and
calculate `SHA-256`. Persist the payload, `canonical_payload_sha256`,
canonicalization name, target environment alias, operation, and relative path.
After the write, persist the same digest with the verification GET timestamp,
HTTP status, and sanitized exact-identity response summary. The approval shown
to the user must name this digest. A digest from an unspecified serializer or
from unavailable historical request bytes is unverifiable evidence and must be
recorded as such rather than reconstructed or asserted as a match.

## Create mapping

| Functional value | REST field/value |
|---|---|
| Template name | `Name` |
| Comments | `Comments` |
| Active / Inactive | `StatusCode`: `A` / `I` |
| General feedback | `TemplateType`: `ORA_GENERAL` |
| Performance goal feedback | `TemplateType`: `ORA_PERF_GOAL` |
| Resolved questionnaire identity | `QuestionnaireId` as returned by the questionnaire provider |
| Resolved specific manager type codes | Comma-separated `ShareWithManagers` |
| Goal Description | `DESC` in `GoalAttributeList` |
| Goal Status | `STATUS` in `GoalAttributeList` |
| Completion Percentage | `COMP_PERCENT` in `GoalAttributeList` |
| Goal Weight | `WEIGHT` in `GoalAttributeList` |

Use only goal attributes supplied in the functional input. Preserve their source
order when joining the mapped codes. Do not add `SUCCESS_CRIT`, `MEASUREMENT`,
or `TASKS` merely because they appear in the technical sample.

## Preconditions and approval

1. Declared GET operations are agent-owned read-only validation and do not
   require consultant approval. This includes dependency resolution, conflict
   checks, and post-write verification. Obtain approval only immediately before
   a POST or PATCH.
2. Resolve each questionnaire through the provider and each manager type through
   the declared lookup route; never hard-code their IDs or codes across tenants.
   For POST or questionnaire/type-changing PATCH, run
   `scripts/run_feedback_workflow.py` at `before_association`
   using the reference-lookup contract. Require `eligible`, and compare its
   candidate ID, template type and target to the effective outgoing request.
   Persist the input/result with the preview; rerun if any bound evidence changes.
   A creation-stage pass or an active/latest LOV match cannot replace this gate.
3. Run `list_templates` and resolve a create-name conflict or an update target
   exactly. For PATCH, follow the fresh response's canonical relative self link;
   do not construct an item URL from an example ID. Capture a fresh ETag when
   Fusion returns one and use it as `If-Match`.
4. Enforce the active/in-use and questionnaire-change restrictions before
   mapping the payload. A PATCH with no changed field stops without a request.
5. Evaluate the task-local input, dependency, lookup, design, and error rules
   and persist each result with the REST draft. No Data Loader Task Hook or
   archive preview is used. For POST or PATCH, show the target
   environment alias, operation, resolved path, exact payload, JCS SHA-256
   digest, route-supportability evidence, and all validation results, then
   obtain explicit approval immediately before exactly one write. No automatic
   write retry is permitted.
6. After a successful POST or PATCH, use `get_template_by_exact_name` with
   `q=Name='<exact escaped template name>'` and the contract's explicit
   `fields` projection. Require exactly one result; do not use a default item or
   collection representation to infer that a field is absent. Persist sanitized
   status and identity evidence. For Performance Goal Feedback, compare
   `GoalAttributeList` and `GoalAttributeListCount` with the source-derived
   mapped codes and count. Do not mutate a questionnaire or a runtime
   `FeedbackRequest` through this task.

## Approval binding and execution evidence

Before preview, require one capability alternative defined in
`ora_reference_lookups.md` plus compatible current-run collection GET evidence,
and owner confirmation only when explicitly required by project policy.
Persist the canonical payload bytes and digest with the target alias, resolved
base URL identity (without credentials), HTTP method, relative path, relevant
query and conditional headers, and validation results in an immutable project
preview. Use an available RFC 8785 implementation; if canonicalization cannot be
performed and independently reproduced, stop with a tooling/contract gap.
Do not label ordinary sorted-key JSON serialization as verified JCS.

Immediately before dispatch, canonicalize the actual outgoing body again and
compare its digest and every request-binding field to the approved preview.
Changed payload, environment/base URL, method, path, query, or If-Match header
invalidates approval: rebuild the preview and obtain fresh explicit approval.
Send exactly the approved request through `core.fusion-api.rest-api-client`.
The task wrapper enforces compatibility, request binding, approval, current
identity checks and readback. Referenced policy and preflight evidence still
requires truthful agent review; flags are not authenticated owner assertions.
The generic REST client does not independently enforce this task contract.
Never invent evidence when a check cannot be completed.

After execution, compare the exact-identity response with every requested field
and preserve the template ID and unchanged dependent fields for PATCH. A failed
verification is a failed/partial outcome, not success. Persist sanitized status,
request ID/ECID when returned, verification time, and the approved request digest.
Use bounded client timeouts. An uncertain write outcome requires an exact read
and fresh approval before another write; never automatically retry POST/PATCH.

## Mandatory task entry point

Before creating a plan/runbook, use the offline `plan_requirements` action:

```json
{"action":"plan_requirements","template_type":"ORA_PERF_GOAL","questionnaire_intent":"unspecified"}
```

`questionnaire_intent` is `unspecified`, `existing` or `create`;
`requested_questionnaire` optionally contains a `name` and/or portable `code`.
Every result also returns `mandatory_profile_prerequisites` for
`HRA_REQUEST_FEEDBACK_ENABLED = Y` and
`ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Y`, plus one
`conditional_starting_runbook_task` describing the catalog-valid
`Manage Administrator Profile Values` task. These fields declare the parent
Run Book baseline; this Feedback Templates wrapper does not read or write the
profiles. The parent omits that task only when both exact SITE values are
verified as `Y`.
General Feedback requires that reference/design identity. Supported goal intake
returns a seeded selection and lookup/verification steps, never a numeric ID or
questionnaire-creation task. Custom goal intake returns `unsupported_request`,
no executable tasks, and the recommended `not-applicable` disposition. It does
not update a runbook. Use code when available; a name-only request differing from
the delivered name needs identity clarification, not silent substitution.
This action requires no tenant evidence or credentials and rejects live flags.

The example above performs legacy questionnaire-routing checks only. For full
conversational creation intake, always supply `requested_channel` (REST for an
explicit REST request) and `business_values`, including an empty object when
nothing is known. Supported business fields are `name`, `status` (Active/Inactive
or A/I), `manager_types` (labels), and, for Goal Feedback, `goal_attributes`
(labels). Labels still require existing source-backed resolution before payload
mapping. Missing values return `clarification_required`, `missing_business_fields`,
`follow_up_questions`, `confirmed_business_values`, `next_action=ask_user`, and
no executable tasks. Preserve the original input, merge explicit follow-up
replies and rerun offline; the helper does not persist conversation state.
General Feedback also needs questionnaire name/code and an existing/create
decision; new questionnaire content remains a provider input.

`requested_channel` classifies execution intent, not the source document format.
Explicit CSV/FSM import/export, HDL/HSDL and Data Loader requests return
`UNSUPPORTED_EXECUTION_CHANNEL` with supported alternatives and a question
offering a separately requested REST plan or read-only inspection. Do not
substitute REST without a revised user request. Requirements from CSV/BRD may
be retained when REST is explicitly requested. Omitted channel retains legacy
REST behavior; conversational callers must supply the actual classification.

For ordinary updates, collect the exact existing template name and desired
field values, then use `action=update_template`, `stage=before_template_update`,
`operation=patch_feedback_template`. Use the current-template preflight,
canonical route, payload contract, approval and attempt marker. QuestionnaireId
and TemplateType cannot appear in this payload; use `associate` for those fields.
In-use templates accept only Name or Comments; unused templates accept applicable
declared PATCH fields after existing validation. General templates cannot include
goal attributes. Goal activation still needs impact review. No new questionnaire
lookup or content verification is claimed. Completion requires exact update
readback and preservation of all unchanged fields, including the questionnaire.
A changed goal attribute list also requires its derived count to match.
Uncertain outcomes remain partial and require reconciliation before a separately
approved subsequent attempt.

The same seeded-only restriction runs before provider handoff and association.
It rejects unsupported goal intent before any external lookup and before
approval. A missing seed returns `SEEDED_QUESTIONNAIRE_MISSING`, never a creation
fallback. General Feedback follows its existing custom provider workflow.

Use Python 3.10+ for the core-client integration. Run from this task folder:

```sh
python3 scripts/run_feedback_workflow.py --input /absolute/project/spec.json --dry-run
```

The default is offline. `--live-read` refreshes only declared provider GETs;
use it only after the routed workflow permits external reads. Association
execution requires `--execute --preview <saved-preview.json> --approval
<approval.json> --attempt-file <absolute-project-attempt.json>`. Present and
approve that exact preview through the existing runbook/REST approval gate,
not an additional duplicate gate. Never synthesize approval. The wrapper uses
core host validation, cached OAuth and one-shot transport; missing authentication
requires the routed Chrome sign-in handoff, not automatic browser login.

The input contract is:

| Field | Required content |
|---|---|
| action, stage, template_type | questionnaire_handoff/before_questionnaire_creation, associate/before_association or update_template/before_template_update; ORA_GENERAL or ORA_PERF_GOAL |
| context | Exact base_url, resource_version and run_id |
| policy_evidence | Association/handoff only: catalog policy_id plus reviewed provenance |
| candidate | Association/handoff only: normalized identity/design and provenance from ora_reference_lookups.md |
| lookup_evidence | Offline exact declared path/query, complete=true and items; required where the resolver uses a lookup |
| provider_specification | Handoff only: full existing Questionnaire create/MERGE specification, one records entry; candidate carries its specification SHA-256, name, subscriber_name and version |
| questionnaire_task_context | Handoff only: reviewed provenance plus questionnaire_intent=create and ordered task_codes containing HRT_MANAGE_QUESTIONNAIRES once before ORA_HRA_FEEDBACK_TEMPLATES once; source_ref identifies the refreshed mapping |
| requested_component_scope | Handoff only: components in Questionnaire, QuestionnaireAttachment, Section, Question, Answer order as applicable; sorted direct_question_types; boolean attachments_requested, answers_requested and translations_requested. Must match the provider specification; direct question types come from attributes.QuestionType and mode is direct, direct-text or reference. This describes requested content, not live schema readiness. |
| questionnaire_intent, provider_outcome | Association after creation: questionnaire_intent=create requires provider_outcome with reviewed provenance, provider=hcm.hcm-tool.questionnaire.questionnaires, candidate_code and status=verified. Any supplied unverified outcome blocks association before target reads. Preserve exact provider stage, failure class, message and evidence references as additional outcome fields. Existing-questionnaire association does not require a creation outcome. |
| operation, payload | Association or ordinary update: enabled contract operation and exact declared body |
| preflight | Reviewed provenance, environment alias, collection_path and true checks for inputs, identity, authenticated_access, catalog, manager_type, route_capability, artifact_paths, lifecycle; authenticated_access is a current compatible target GET by the same principal with no known denial, not an assertion of write privilege. PATCH current_template complete readback, POST name_available=true; active goals also require goal_activation_impact_reviewed=true |
| attempt_file | Absolute project run path bound into the write preview; retained exclusive dispatch marker prevents automatic retry |
| content_verification | Association after this workflow creates a questionnaire: verified candidate ID/code and provenance, matches_requested_content=true and equal 64-character lowercase expected/observed content SHA-256 values; needed for completion. For `questionnaire_intent=existing`, the workflow did not create questionnaire content, so this milestone is `not_required`; current eligible identity and template association readback remain mandatory. |

Every provenance object contains the same context, source_ref, verified=true,
conflicting_evidence=false, and timezone-aware checked_at/expires_at. Review
and preserve actual source evidence; do not extend timestamps without rechecking.
Approval uses the same provenance plus approved=true and the exact
preview_sha256. Full synthetic input examples and injected-client integration
tests are in `tests/test_questionnaire_workflow.py`; they are not tenant data.

The wrapper recomputes evidence and compares the saved preview before reads,
refreshes identity before one approved write, and verifies exact readback. Its
payload digest implements RFC 8785 only for this contract's flat ASCII-key,
string/boolean bodies; other types fail closed. Internal specification hashes
are not JCS payload hashes. Persist stdout, inputs, preview, approval and sanitized
diagnostics under the active project run before advancing the runbook.

`handoff_ready` authorizes only delegation to the existing Questionnaire provider;
it does not execute a load or mark creation complete. Provider/Data Loader
previews, validation and approval still apply. No changes to those providers
are required by this task wrapper. `association_verified_content_pending` is
not overall completion. `completed` means association readback passed and
content was either verified for a newly created questionnaire or not required
for an existing one. A blocked, partial or uncertain result stops the dependent
task; reconcile its retained attempt marker and obtain a new approved preview
before any explicit retry. Never remove the marker to trigger an automatic retry.

The handoff reports consumer compatibility as passed while provider validation
and import validation remain pending and creation remains not_started. Persist
it before provider execution. When scope changes from existing to create,
refresh the task mapping and design first; a retained existing-reference plan
cannot satisfy questionnaire_task_context. The wrapper validates reviewed
mapping evidence, not the live Run Book; any live merge remains core.runbook's
operation and approval responsibility.

Do not treat get_key_attributes.py or a sample schema fallback as import
validation. Confirm fallback support in the current Questionnaire provider and
the actual Data Loader import route. An empty unused optional component is a
provider limitation to investigate, not proof that the tenant needs repair.
This folder does not implement or override Questionnaire schema validation.

## Questionnaire metadata recovery

Apply this procedure only to General Feedback custom questionnaire creation
after consumer compatibility and the refreshed Questionnaires task handoff
are ready. The existing Questionnaire provider owns every metadata and build
step below; this wrapper does not invoke a loader or parse DAT files.

| Situation | What Happens |
|---|---|
| A supplied Questionnaire DAT contains METADATA | Treat it as dated reference evidence. Preserve its artifact identity and hash in the project; obtain the current target contract through the provider before generation. Do not embed its path, columns, names, defaults or UCM ID in reusable code. |
| A prior inspection or sample helper failed | Preserve the exact diagnostic, then have the provider evaluate the existing strict core Data Loader metadata path with attribute-schema fallback disabled. Resolve the exact Questionnaire business object and freshly retrieve the UCM template referenced by its current detail. Do not require sample generation to succeed before this check. |
| Fresh strict metadata validation passes | Record the resolved target and release, business-object identity, current UCM content ID, template filename and SHA-256, retrieval time, schema source UCM_TEMPLATE, requested components, and applicable attribute, key and operation evidence in a new provider run. Continue provider validation from that evidence; retain the older failure as history. A schema pass alone does not verify creation or authorize import. |
| An unused optional component has no attribute rows | Preserve the observed response and requested scope. With a valid current UCM template, let the strict provider/import checks determine applicability; do not synthesize its schema or make an earlier sample-fallback exception the creation result. Missing evidence for any requested or target-required component remains blocking. |
| The current UCM template has no METADATA, has the wrong root, or fails strict validation | Stop generation and report the current provider/core failure. A supplied local DAT cannot override this failure. Record any returned Oracle generation error and route remediation to the provider owner; do not refresh the business object, upload, retry a write, or change execution routes here. |
| The design does not request a questionnaire template or translation | Resolve those dependencies only if the current provider contract requires them. Do not make QuestionnaireTemplate or its translation generation a prerequisite solely because reference files were supplied. If a template is requested or target-required, its exact active compatible identity remains mandatory. |

Once all provider gates pass, use its existing DAT construction procedure with
the selected attributes in current-template order. Include only requested and
target-required components and values; retain portable keys and approved
business values. The core Data Loader still validates the immutable artifact,
task context and approval before submission. Creation readback and the separate
before_association compatibility check remain required before Feedback Template
preview. Preserve existing attempt markers and approval boundaries when resuming.

Source: [Oracle HCM Data Loader: Generate and Use Template Files](https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/generate-and-use-template-files.html).
Regression coverage: tests/test_questionnaire_metadata_recovery.py exercises
the existing strict core reader with synthetic target responses and no live calls.

## Reference resolution inputs

Optional `manager_selection` is All or an ordered list of specific meanings/codes. All produces ALL; specific selections require the declared live LOV through the core client. The outgoing ShareWithManagers must equal the resolved value.

For General Feedback, omit manually assembled policy_evidence and supply provider_validation from actual current provider checks. The resolver derives policy applicability and provenance from the receipt as documented in ora_reference_lookups.md. The provider receipt is bound to the complete create specification; absent, stale, mismatched or incomplete checks block handoff. No future questionnaire ID or prior association is required for creation.

## ETag transport formatting

ADF @context.headers.ETag may expose the raw opaque token. Format If-Match as a quoted strong entity-tag, preserving an already quoted value without double quoting. Reject malformed, weak or unsafe tags before preview. Bind the final formatted header into approval and recheck the fresh raw ETag before dispatch. A changed header after a dispatched attempt needs a new preview, a new attempt marker and fresh approval; never replay automatically.
