# Absences Additional: Lifecycle and Acceptance Contract

## Sources and responsibility

This contract applies to the generated Absence Certifications and Leave
Agreements setup task skills. Sources include the 2026-10-01 observed target
Redwood UI, current Oracle UI documentation, task-local adapter metadata,
[WFM-82961](https://jira.oraclecorp.com/jira/browse/WFM-82961), and
[WFM-82962](https://jira.oraclecorp.com/jira/browse/WFM-82962). The user's
instructions and observed target UI determine functional scope; a Jira
acceptance criterion may be obsolete or incorrect.

| Priority | Source | Authority and boundary |
|---|---|---|
| 1 | User instructions | Define the requested objective and source priority. Preserve the requested business intent and authorized scope. |
| 2 | Observed target Redwood UI | Defines available actions and current field behavior for that observed target and session. Refresh observations when the target or UI version changes; do not generalize one pod to every deployment. |
| 3 | Jira story and acceptance criteria | Supply acceptance requirements after the current Redwood page. Mark a conflict superseded by observed UI behavior; an unobserved action stays unverified instead of being enabled from the AC alone. |
| 4 | Latest Oracle UI documentation | Supplies supporting guidance within the target release; it cannot override observed behavior or add a control/action absent from Redwood. |
| 5 | Current adapter metadata | Defines technical read/write contracts for a UI-supported action. API fields or generic date controls cannot expand functional scope. |

This priority classifies functional behavior; an observed UI action does not
invent its Data Loader execution mapping or bypass project, access, protection,
or approval gates. Public HCM REST documentation for worker certifications
does not establish the setup contract.

Start an implementation request at `router.implementation-router`. Use the
selected task's registry and execution guide for declared read-only lookups.
All mutations remain owned by `core.data-loader`, REST mode, the exact task
business object, and its existing immutable preview/approval workflow. Browser
inspection during authoring does not install a runtime browser execution route.

## Lifecycle preflight

Classify the intent against the observed target UI before choosing an execution
route. In the observed single-current-version Leave Agreements UI, View,
Create, Edit, and whole-agreement Delete are available. Dated Update, Correct,
dated child-row deletion, End Date, and History are unavailable. Explain an
unavailable action and offer the applicable supported choices; preserve the
supplied name, legislation, requested changes, and dates as business context.
Do not mark the whole workflow catalog-blocked or seek a dated adapter contract
for an action absent from this UI. Do not silently perform Edit or whole-object
Delete in its place. An ordinary "update the Description" request with no dated-slice intent maps
to current Edit; interpret business meaning rather than a verb alone. Preserve
explicit dated intent as unavailable without conversion. A fresh observation of
another target can establish its own UI scope; this session does not establish a universal server contract.

The observed Absence Certifications UI retains dated maintenance actions and
History. Keep those distinct functional intents. Their automated execution or
history retrieval still needs the current declared adapter contract for the
selected action; current-item reads and generic RangeModes do not establish
date-slice or history support.

Before source preparation, establish environment and authorized access,
requested operation, applicable fields/date semantics, current registered
contract, dependency readiness, and task readiness. Apply evidence requirements
by operation: Create needs the proposed business key, exact existing dependency
references, and a target-key collision check; it does not need an existing
identity for the new parent/children or a deletion-impact resolver. Maintenance
needs the exact existing parent/child and selected row plus its operation-specific
allowed-field and impact evidence. Neither reviewed setup UI exposes upsert/replacement; reject it instead of
using it to evade current action and field checks. A template
containing effectiveOf is not proof that all RangeModes are supported. For a
UI-supported action, missing required adapter evidence is an execution blocker,
never a fallback to another API, UI automation, worker resource, or operation.

For Leave Agreements Edit, collect the requested allowed-field changes and
read the full current before state, including every affected child identity.
Review changes to the current version, with applicable dependencies and impact;
do not demand a new dated slice or operation date. Verify the selected adapter's
current-version Edit mapping before source preparation or execution. Do not
equate Edit with a dated Update or Correction action. The loader's internal
CORRECTION control uses the verified stored Start Date only. A missing Edit mapping
blocks execution of that selected action, while its draft review and other
supported actions remain available.

| Intent | Mandatory evidence before approval |
|---|---|
| View | Exact search or user-selected list filters, full requested parent fields, all requested child pages, and resolved business meanings. Active-only defaults must not hide a requested Pending or inactive record. No result, ambiguity, and missing detail evidence are distinct outcomes. |
| Create | Name, legislation, classification/pattern, effective business date, applicable required rules/children, valid lookup selections, dependency readiness, and target-key collision check. |
| Edit current Leave Agreement | Exact current parent and affected children, full before state, allowed-field evidence from the current UI, proposed changes, applicable dependency/impact evidence, current registered template, and verified current-version adapter mapping. Correct the current record at its stored Start Date; do not create a new dated slice. |
| Update Absence Certification | Exact current identity and selected context, explicit operation date, before/after diff, allowed-field evidence, dependency impact, and verified current adapter mapping. Certification Name, Classification, Legislation, Trigger, and stored Effective Start Date cannot be changed by Update. |
| Correct Absence Certification | Exact existing slice/child and its returned stored dates, current mutable-field evidence, applicable impact, and verified correction mapping. Correct does not unlock read-only identity or hidden creation/date/payment rules. Reuse the selected stored Start Date without asking for a replacement; never create a new slice. |
| Delete dated Absence Certification row | The 2026-10-07 multi-row review exposed Delete Record. Require bound current configuration and History evidence, complete contiguous History, selected non-first ID/range, User-defined protection and physical-row adapter contract; preserve and extend the previous row. No replacement date or child deletions. |
| Delete whole Leave Agreement | Explicit whole-agreement intent, exact identity and full before state, known child inventory and management/protection/reference checks, disclosure of unresolved downstream references, current registered hard-delete contract, and immutable preview. Fusion enforces remaining business restrictions on the single parent DELETE; do not synthesize child deletes or ask for dates. |
| Delete whole Absence Certification | Explicit whole-object intent, exact identity, management/protection/reference checks, all-child and downstream impact, supported delete contract, and immutable preview. Never infer cascade behavior or absence of references. |
| End-date Absence Certification | Supplied End Date or disclosed Redwood current-date candidate, exact selected parent, chosen-date confirmation in core preview, chronology and application-reported impact, and verified END_DATE contract. No configuration edits or synthetic child end dates. |
| Absence Certification History | Exact selected certification, current declared history read contract, complete returned history pages and business meanings. Do not synthesize history from the current record or introduce mutation approval for a read. |
| Unavailable Leave Agreement dated/history intent | Explain that the observed single-current-version UI does not expose that action. Offer View, Create, Edit, or whole-agreement Delete as applicable; ask for a supported business choice without treating it as approval to change scope. No obsolete dated-operation source or preview is prepared. |

When the selected maintenance/destructive operation requires them, application
impact and protection checks must use a declared read-only resolver
or authoritative application evidence selected by the active workflow.
For Absence Certification whole deletion and End Date, use the task-local
known-protection and known-child review with the observed UI impact warning.
Delete Certification covers all date-effective records; End Date warns about
the previous record's end date. Disclose unresolved downstream references in
core's immutable preview and allow Fusion to enforce remaining business
restrictions. Do not invent a complete downstream-impact resolver as an extra
business prerequisite, infer absence of references, or synthesize child actions.
Missing current UI action, selected adapter support or required known-protection
evidence still blocks that action. Approval cannot repair a missing execution
contract. These checks do not block an ordinary Create or View that passes
its own requirements.
For Leave Agreement whole deletion, use the task-local known-protection and
known-child review, disclose unresolved downstream references in the immutable
preview, and allow Fusion to enforce its business restrictions. A separate
complete downstream resolver is not a prerequisite for this supported route.
Successful deletion proves execution and reconciliation, not absence of prior
references. Missing evidence required by the task-local contract still blocks
execution.

## Conversation, approval, and verification

| State | Meaning and permitted next step |
|---|---|
| Draft | Collect and stage business choices; nothing submitted. |
| Validating | Evaluate current task rules, lookup evidence, and source integrity. |
| Unavailable | The requested action is absent from the observed target UI. Explain its availability boundary and offer applicable supported choices; preserve business context. Do not report a workflow-wide catalog blocker or silently substitute another action. |
| Blocked | An available selected action lacks a required input, project/access prerequisite, adapter contract, or applicable protection/impact evidence. Name the field/rule, failure class, evidence gap, and one next action; preserve the safely resumable stage. |
| Pending confirmation | All applicable gates passed; present the exact environment, object/row, operation, dates, before/after values for maintenance or proposed values for Create, all child changes, defaults, and application-reported impact where required for the selected operation through core Data Loader's immutable preview. |
| Submitted | One approved load submitted; retain returned process/request IDs and report current status. Submission is not completion. |
| Completed | Reconcile the requested parent and each child with safe reads after final successful status. Report every partial failure separately and preserve Fusion audit evidence. |

Bind confirmation to the exact artifact/hash through core; changes invalidate
it. Do not add a second approval prompt. Trigger selection and draft choices
are not final mutation approval. Use business labels for user dialogue and the
required technical node handoff in durable artifacts. Never persist secrets or
customer/employee data. Use the existing token logger, artifact registry, and
append-only run record for project outputs.

Classify failures using repository error classes. Refresh a cached-token
401/403 only once at a declared authentication step. Never retry an uncertain
write automatically; reconcile it first. On timeout report environment,
operation, task/job, process/request ID, last status, elapsed wait, and next
check. Persist available failed-job logs with redaction. Approval, missing
operation evidence, and empty country-specific LOVs remain distinct blockers.

## Acceptance traceability

The certification story repeats AC3 and AC5. Suffixes below disambiguate their
titles. Map criteria to authoritative observed UI behavior; a superseded
criterion is not applicable to the current observed UI, not a passing dated
operation or a promise to implement one. Coverage means an authored contract;
it does not mean a successful live mutation was observed.

| Story criterion | Implementation and evidence boundary |
|---|---|
| WFM-82961 AC1 View | Exact discovery plus full-detail presentation including Description; missing detail lookup evidence is reported, not filled by inference. |
| WFM-82961 AC2 Create | Redwood staged intake, explicit Trigger, conditional Rules, live LOVs, portable preparation, core preview/approval/verification. |
| WFM-82961 AC3 Update | Exact identity/date, immutable-field guard in portable source validation, before/after review and application audit. |
| WFM-82961 AC3 Correct | Correct the selected stored slice using only current mutable fields. No new date or read-only identity/creation changes; current operation evidence remains required. |
| WFM-82961 AC4 Delete dated row | Current multi-row UI exposes Delete Record; preparation requires exact non-first row and configuration/History/protection/physical-row adapter evidence. Live loader acceptance remains a QA result. |
| WFM-82961 AC5 Delete | Whole certification and all date-effective records, known-protection/current-child review, unresolved-reference disclosure, core confirmation, Fusion business restrictions and reconciliation. No complete downstream resolver is invented. |
| WFM-82961 AC5 End date | Separate chosen End Date dialog, disclosed current-date candidate when omitted, application chronology warning, confirmation and verification. |
| Absence Certifications History | The 2026-10-06 target History GET/findHistory and initial returned row were observed successfully. Use read_absence_certification_history with exact identity, fresh service/finder evidence and complete pagination; multi-row history and live mutation acceptance were not exercised. |
| WFM-82962 AC1 View | Parent details plus eligibility, entitlements, certifications, descriptions; pagination and unavailable-field disclosure. |
| WFM-82962 AC2 Create | Both patterns, legislation-first choices, drawer dependencies, Pending default, core preview/approval/verification. |
| WFM-82962 AC3 Update | Dated Update criterion is not applicable to the observed single-current-version UI; Redwood Edit supersedes it. Review allowed current-version changes and verify the Edit adapter mapping separately; do not claim dated Update passed. |
| WFM-82962 AC4 Correct | Not applicable: the observed UI has no Correct action. Its single-current-version behavior supersedes this dated criterion; explain supported choices instead of seeking a Correction route. |
| WFM-82962 AC5 Delete dated row | Not applicable: the observed UI has no dated child-row deletion. Offer applicable Edit or whole-agreement Delete choices without inferring that either performs the requested dated deletion. |
| WFM-82962 AC6 Delete | Exact whole-object scope, full before state and known-child/protection review, unresolved-reference disclosure, current date-free hard-delete adapter support, immutable confirmation, and reconciliation required. |
| WFM-82962 AC7 End date | Not applicable: the observed UI has no End Date action. Single-current-version behavior supersedes this criterion; no END_DATE mapping or acceptance pass is claimed. |
| WFM-82962 AC8 Legislation | Scoped lookups, stale dependency invalidation, formula/context applicability, and missing country-prerequisite reporting. |
| Leave Agreements History | Not applicable to the observed single-current-version UI; no history action or synthetic history is claimed. |

Live create/save/update/delete acceptance remains unverified by this authoring
run. Synthetic prompt trials, local behavioral tests, registry validation, and
unsaved UI inspection must be reported with their actual evidence level.
