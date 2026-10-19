# Wage Basis Rules Design Enforcement

## Delivery Boundary

Wage Basis Rules is implemented here, inside Payroll Calculation Information.
Native TaxabilityRule is the mutation BO; it has no children. Core Data Loader
owns preparation, schema validation, Task Hook, approval, upload and initiation.
Product REST is GET-only. No central route, generated manifest or catalog
override is required by these task resources, and no historical proof waiver
is a standing runtime permission.

This delivery is for controlled nonproduction QA. Create, effective-dated
inclusion Update, in-place inclusion Correct, and explicit whole-history Delete
have native-loader plus REST proof. This is contract evidence, not a claim that
every customer combination has been tested. Accept any uniquely resolved live
LOV value with an established field/context mapping; do not whitelist sample
LDGs, jurisdictions, components, classifications, IDs or dates.

End Date and selected-version Delete remain pending future development. Both
tested End Date purge settings retained future applicability despite loader
success. Native DELETE removed every version, including earlier history.
Predefined overrides, identity changes, finite-end Create, and updates through
existing future changes need separate contract coverage; no REST fallback.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify business intent | Distinguish new version, correction, finite applicability and whole-history deletion; refuse unsupported semantics |
| 2 | Resolve current scope | Complete declared read-only lookups and preserve both context representations |
| 3 | Baseline and expected effect | Prove absence or one logical target, complete history and unaffected sibling state; calculate exact expected before/after timeline. Apply Create Preparation Readiness or Existing-Rule Maintenance Gates before core prepares an archive. |
| 4 | Core artifact preparation | Core prepares/validates one immutable native archive and invokes Task Hook before approval |
| 5 | Task contract checks | Evaluate exact ordered attributes, values, row counts, date syntax, shape and semantic safeguards; offline helper is supplemental |
| 6 | Core approval handoff | Return accepted Task Hook result bound to exact artifact, environment and business effect; core renders its authoritative approval report |
| 7 | Governed execution | Core alone performs the authorized upload/initiation lifecycle; no task-local submission or replay |
| 8 | Later business verification | On requested verification after loader success, reconcile complete physical/history state through declared GETs |

## Design Rules

WBR.CHECK_PREPARATION evaluates business readiness before the conversational
flow hands complete selections to core preparation: input/identity completeness,
supported effect, native-key mappings, duplicate/history checks and NO_CHANGE.
It excludes checks whose Applies When requires a prepared archive, Task Hook
or approval preview. Read/reconciliation takes its read_only outcome without
applying mutation gates. WBR.ENFORCE_DESIGN is the later artifact/summary gate.
When core invokes this graph for an already prepared archive, the same
business gates still run before approval; this does not reorder core's loader
lifecycle or invoke a second Task Hook.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any operation | Blocker | | Core has not verified target identity, required privileges and an authenticated session under the caller's auth constraints | Resolve the core preflight; never inspect or copy credentials/session contents | Yes |
| Mutation in this QA delivery | Blocker | | Target lacks explicit verified nonproduction classification | Use the explicitly designated QA target, not a hostname guess | Yes |
| Create | Blocker | read_wbr_history | An expanded logical identity repeats within the request, any exact identity already exists across all history including expired versions, or duplicate/blank-context evidence is incomplete | Stop preparation: confirmed duplicates are CONFLICT; incomplete evidence remains a lookup/readiness blocker. Do not silently deduplicate, omit conflicting rows or convert Create into Update. | Yes |
| Update, Correct or whole-history Delete | Blocker | read_wbr_history | Target absent/nonunique, protected/predefined status unresolved, missing dates or incomplete baseline | Resolve current non-predefined target and every dated version before preparation | Yes |
| Active context | Blocker | find_wbr_context_values | Native helper-key mapping is absent, an active slot is blank, or a REST stored ID is substituted without mapping evidence | Resolve both representations in order; do not guess from a numeric code or translate labels heuristically | Yes |
| Create native component key | Blocker | find_wbr_components | Business selection resolves but PayrollComponent cannot uniquely represent that selected component under the established native contract | Return CATALOG_MISMATCH; retain the selected business code and establish the native mapping before preparation. Never substitute an unproven code, duplicate display name or internal ID. | Yes |
| Prepared mutation | Blocker | verify_wbr_hdl_contract | Current template/schema, selected exact field shape, expected values or immutable artifact disagree | Return CATALOG_MISMATCH and rebuild through core; no silent extra fields or changed bytes | Yes |
| Prepared mutation: core approval handoff | Blocker | | Exact before/after expectation, safe reconciliation plan or approval-bound core envelope is absent | Finish core preparation/Task Hook before requesting approval | Yes |
| End Date or selected-version Delete | Blocker | | Requested effect has no verified native contract | Return WBR_OPERATION_PENDING; do not prepare an equivalent-looking MERGE/DELETE | No |
| Other unlisted write or predefined Override | Blocker | | Shape is not covered by this delivery | Return UNSUPPORTED and record the missing contract for future work | No |

## Create Preparation Readiness

These gates connect conversational intake to core preparation; they neither
create a task-owned payload builder nor authorize a Fusion mutation. Recheck
them against the immutable artifact at Task Hook. A partial selection can
reach only the declared choice-discovery reads, never archive preparation or
core approval.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before Create preparation | Blocker | | Scope, secondary intent, component selection, any per-component inclusion/start, or an applicable business clarification is unresolved | Remain collecting and ask only the next meaningful business question under ora_input_validation.md | Yes |
| Before Create preparation | Blocker | find_wbr_classifications | Any date-scoped selection is unvalidated, explicit all is empty or incompletely paginated, or expansion has no rules | Complete the existing date-scoped resolver and input contract; never use a displayed subset or silently change all to none | Yes |
| Before Create preparation | Blocker | find_wbr_context_values | Native expected cells and REST identity expectations lack an established mapping for an active context or differ in their resolved business scope | Complete the existing mapping; HDL helper keys and stored REST codes remain distinct representations of the same selection | Yes |
| Before Create preparation | Blocker | read_wbr_history | Complete absence checks have not passed for every expanded logical identity, including intentional null-secondary and inactive-context identities | Finish complete all-history checks. The duplicate rules above ignore inclusion and effective start; if any row conflicts, the current Create plan is blocked, not partially prepared. | Yes |
| Create Task Hook | Blocker | verify_wbr_hdl_contract | Native rows differ from independently derived expected rows, per-row dates or inclusion; total/included/excluded counts differ; or business summary/readback expectations omit a combination | Reject the artifact and rebuild through core from complete resolved selections; parsing successfully is insufficient | Yes |

## Create Business Summary

Supply the following resolved business facts to core's authoritative preview;
do not introduce another task-owned approval prompt. Keep IDs and native
encodings in core's protected evidence, not in user questions or the business
summary. This summary is complete only after the readiness gates pass.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create preview: target and scope | Blocker | | Target or shared business scope is absent from the summary | Show configured business environment and verified nonproduction status, LDG, component group, reference level and ordered context business values, or explicit No References, plus primary classification. | Yes |
| Create preview: secondary scope | Blocker | | Summary omits secondary membership or represents a filtered subset as All | Show selected secondary labels or explicit None. For All show full expanded membership and count per distinct date scope. Use readable continuation for large summaries without claiming a truncated list is complete. | Yes |
| Create preview: component effects | Blocker | | Any combination lacks its component, decision, date or open-ended effect | Show each component, Included or Excluded, effective start, No end date (open-ended), and applicable secondary combinations. Group repeated shared facts only when every resulting combination remains identifiable. | Yes |
| Create preview: counts and boundaries | Blocker | | Summary counts only Included rules or obscures pending date operations | Show total physical rules and separate Included/Excluded counts after expansion. One secondary with two Included components and one Excluded means three new rules. Explain that Excluded creates a rule too, and that finite-end Create and later End Date remain pending. | Yes |
| Create handoff: verification and approval | Blocker | | Summary implies intake alone authorizes execution or proves successful creation | Disclose the single TaxabilityRule.dat archive shape and expected readback effect through core's authoritative report. Exact native values/counts and independently resolved REST expectations must agree. Use core's existing preparation, schema, Task Hook and approval lifecycle, not an extra task-owned confirmation. | Yes |

## Existing-Rule Maintenance Gates

Apply these gates before core preparation and against the resulting immutable
archive at Task Hook. Derive the expected timeline from the original complete
baseline and explicit requested effect, not from the DAT or observed result.
The offline helper checks that supplied expectation; it does not select intent
or prove that the live reads are complete.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before maintenance preparation | Blocker | read_wbr_history | Existing-Rule Maintenance Intake is incomplete, target/history changed without revalidation, or the exact non-predefined rule and full physical timeline are not established | Finish only the missing input or lookup; preserve accepted business answers. Show the selected logical rule and history before core approval, not a new Create questionnaire. | Yes |
| Update | Blocker | read_wbr_history | Boundary is not strictly after the selected last slice start, last slice is not open-ended, a later slice already exists beyond the selected slice, or fields other than inclusion would change | The supported effect splits only the last open-ended slice: its old inclusion remains through boundary minus one calendar day; a new slice begins at the boundary with requested inclusion and the original open end. Preserve all earlier history. Do not purge future changes, move the boundary or substitute Correct. | Yes |
| Correct | Blocker | read_wbr_history | An exact existing version is not selected, either physical date would change, identity would change, or a version would be added/removed | Change only the selected slice's inclusion; retain its start, end and the number of slices. Preserve predecessor and future versions, even when correcting an older period. A user as-of selector is not a new effective start. | Yes |
| Update or Correct with unchanged inclusion | Blocker | read_wbr_history | Selected applicable slice already has the requested inclusion | Report NO_CHANGE with the existing period and decision; do not prepare or submit a redundant MERGE or claim a new successful change. | Yes |
| Whole-history Delete | Blocker | read_wbr_history | Intent is ambiguous or version-limited, complete history is unavailable, or the summary hides any past, current or future version | Require explicit removal of every version of this one logical rule. Disclose each full-year period and inclusion plus the version count; expected target history is empty. Native identity dates do not narrow deletion, and no extra task-owned approval is needed when core presents its authoritative approval. | Yes |
| Maintenance scope | Blocker | read_wbr_history | More than one logical target is included in a single archive, or any unrelated component, secondary, jurisdiction or legislative identity would change | One logical rule and one native data row per supported maintenance operation. Keep all observed siblings unchanged, even if they share the same aggregate UI row, component label or classification. Separate explicitly requested additional rules into their own reviewed operations. | Yes |
| Maintenance Task Hook | Blocker | verify_wbr_hdl_contract | Native identity, helper keys, operation, dates or inclusion differ from the selected rule and expected effect, or the independent readback expectation omits prior/sibling state | Reject and rebuild through core. Update uses the new boundary and retained open end; Correct uses both original selected-slice dates; Delete uses verified anchor dates and the whole-history profile. Do not reinterpret a mismatched archive as another operation. | Yes |
| Maintenance preview | Blocker | | Core summary omits target business identity, selected operation, before/after periods and inclusion, affected logical-rule/version counts, or unchanged sibling scope | Supply business environment, LDG, component, classifications and ordered contexts plus the complete expected timeline to core. Distinguish one loader row from versions affected: Update adds one, Correct adds none, whole-history Delete removes every target version. Keep internal keys out of the business summary. | Yes |

End Date and single-version Delete remain pending under Delivery Boundary.
They must not be represented as inclusion Excluded, Correction or whole-history
Delete. An already supplied explicit lifecycle request does not need another
operation-selection question; ambiguous or conflicting intent does.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_wbr_history | Create duplicate check and every existing-rule mutation | Exact complete logical history, sibling baseline and prior values | ora_reference_lookups.md |
| read_wbr_physical_rules | Resolve full-year physical dates and verify outcome | Full identity, ISO date ranges, inclusion and stored contexts | ora_reference_lookups.md |
| find_wbr_classifications | Create readiness and applicable maintenance date-sensitive eligibility | Validated selections at the relevant dates; complete secondary membership for explicit Create all only | ora_reference_lookups.md |
| find_wbr_components | Create native component identity | Selected component business identity and evidence that its native PayrollComponent user key is unambiguous | ora_reference_lookups.md |
| find_wbr_context_values | Context-sensitive native mutation | HDL business keys and corresponding REST values with mapping evidence | ora_reference_lookups.md |
| verify_wbr_hdl_contract | Task Hook | Current native contract and same immutable archive validation | ora_reference_lookups.md |

## Core Handoff and Persistence

WBR.READY_FOR_CONFIRMATION is validation acceptance, not execution or approval.
Pass task code PAY_MANAGE_PAYROLL_DEDUCTIONS, exact skill identity, normalized
operation, expected business effect/row count, schema and baseline fingerprints,
artifact integrity evidence and Task Hook results to core/data-loader. Do not
recursively invoke Task Hook inside a task node. Do not override core's current
approval wording, approved-artifact revalidation or status lifecycle with older
instructions copied from another skill. Approval is bound to the particular
artifact and context; a new operation never inherits a prior proof waiver.

Core owns protected transport artifacts, IDs, receipts and loader diagnostics.
Task summaries use business labels and sanitized results only. Follow the
selected project's artifact/run and token-usage contracts; do not create a
parallel task-owned ledger of credentials, raw payloads or protected IDs.
Reusable skills/tests contain synthetic data only. A lost/uncertain mutation
response requires reconciliation of the original request, never automatic replay.

## Evidence Basis and Pending Work

The developer-supplied internal evidence record
WAGE_BASIS_RULES_UI_REST_HDL_EVIDENCE.md, sections Date-format locality,
Native HDL Effective-Dated Update Proof, Correction and End Date Proofs, Delete
Proofs, and Operation Status, is the authoring source (September 2026 campaign).
Its retained native DATs and REST readbacks establish the profiles here. Earlier
notes proposing a separate Wage Basis Rules skill are superseded by the owner's
instruction to house this work in Payroll Calculation Information. Runtime
must not depend on the author's absolute filesystem, test identities or pod.

Future development: prove true End Date, prove selected-version DELETE_CHANGES
semantics through a governed contract, cover predefined Override and other
identity/date shapes, and expand localization QA where helper-key mappings are
unresolved. Do not claim these operations lack all possible HDL/REST support;
only the current tested native contracts are insufficient.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.CHECK_PREPARATION | decision | 4 | design_enforcement | ready->WBR.APPLY_DEFAULTS;read_only->WBR.APPLY_DEFAULTS;blocked->WBR.HANDLE_ERROR | WBR.RESOLVE_REFERENCES | stop | Evaluate only pre-preparation business readiness as scoped in Design Rules; block conflicts, unresolved native keys, pending effects and NO_CHANGE before native-archive validation; no prepared artifact or approval is required for this check; read/reconciliation returns read_only |
| WBR.ENFORCE_DESIGN | decision | 7 | design_enforcement | compliant->WBR.EXECUTION_GATE;noncompliant->WBR.HANDLE_ERROR | WBR.VALIDATE_NATIVE_CONTRACT | stop | Supported mutation passed exact Task Hook archive validation and the applicable Create readiness/summary or Existing-Rule Maintenance Gates; incomplete input, ambiguous intent or a mismatched timeline is never compliant |
