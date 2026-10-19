# Manage Bank Charges — Error Handling

## Error handling policy

This step reports failures and unresolved contracts from the task rule graph. It
must preserve the original input, immutable artifact identity, process identity,
observed status and sanitized diagnostic details. It does not silently correct
values, reinterpret unresolved evidence, retry an uncertain mutation, switch
integration routes or claim persisted success from process completion alone.

Run Book and Data Loader own immutable preview, approval, submission, monitoring
and post-import verification. This resource defines task-specific reporting and
recovery boundaries; it does not authorize a Fusion operation.

Additional reference GET access/endpoint/network failures follow the
availability policy in ora_reference_lookups.md and continue as
UNVERIFIED_API_UNAVAILABLE warnings. The failure classes below are retained
for diagnostics; they are not blockers for those supplemental checks. Required
inputs, local rules, snapshot identity and Data Loader gates remain mandatory.
No match, ambiguity or a known invalid reference remains a blocking outcome.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BKC.EXECUTION_GATE | decision | 60 | execution_gate | pass->BKC.VALIDATION_DONE;fail->BKC.ERROR | BKC.DESIGN | stop | true |
| BKC.VALIDATION_DONE | terminal | 70 | terminal | none | BKC.EXECUTION_GATE | stop | Required checks passed and any unavailable additional REST checks are disclosed as unverified |
| BKC.ERROR | step | 90 | error_handler | reported->RETURN_ISSUES | none | stop | A preceding task node reports a failure or unresolved contract |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Issues have been disclosed |

## Error situations

| Situation | Required handling |
|---|---|
| Missing or unresolved dependency contract | Return `evidence_unresolved` with the exact node, canonical field, limitation and evidence still needed. Do not classify the business request as invalid or unsupported. |
| Bank charge already exists during creation (AP_CHARGE_EXIST) | Report the conflicting header combination and inspect fresh state. If the user's intent is to change the existing definition, retain that update intent and identify its header and affected lines; do not retry the create or silently upsert. If a new definition was intended, resolve the conflicting combination. |
| Bank charge conflicts with an existing definition during update (AP_CHARGE_EXIST) | Compare the requested target and changes with a fresh export to identify the conflicting definition. Preserve the baseline, requested changes and error evidence; do not retry automatically or assume updates are unsupported. |
| Update target is missing or ambiguous in the fresh export | Resolve which existing header and line the user intends to change. Preserve omitted fields and untouched rows; do not apply create defaults or produce a duplicate-create candidate. |
| At least one charge line is required (AP_ONE_RECORD) | Report that the header has no child row at commit. Inspect the intended complete child set and parent assembly. |
| Amount must be zero or greater (FND_CMN_POSITIVE_OR_ZERO) | Identify the negative amount field. Do not silently replace its value with zero. |
| End date must not precede start date (FND_CMN_TO_ERLY_EQ_FRM_DATE) | Report the supplied StartDate and EndDate and require correction when the non-null EndDate is earlier than StartDate. |
| Range To amount must be at least the From amount (AP_TAX_TO_GREATER_THAN_FR) | Report the supplied From and To amounts and require correction when the non-null To amount is less than From. Preserve the product message identifier despite its wording. |
| Charge range validation failed (AP_OVERLAP1, AP_GAPS, AP_NEED_ZERO, AP_END_AMOUNT_OPEN) | Report the predicate that failed when known. Apply the exact range rules in `ora_design_enforcement.md`; message wording alone does not define interval semantics. |
| Resolver returns zero or multiple matches | Stop the applicable route and report the lookup result. Do not guess an identity or invent a product rejection code. |
| Range evaluator returns `-1` or its status is unknown | Report the evaluation limitation. Do not interpret process success as proof that every validation query succeeded. |
| Fusion process fails, times out or has an uncertain outcome | Preserve task, artifact and process identity, last status, elapsed time and sanitized ProcessLog when available. Continue status retrieval for the same attempt; do not resubmit automatically. |
| Correction after a failed or uncertain import | Reconcile the header and complete charge-line set in a fresh exact-task export against the baseline and candidate before preparing a correction. Disclose identity ambiguity, partial effects and changes to unrelated rows. |
| Import reports completion | Obtain a fresh exact-task export and reconcile the complete requested group and preservation assertions before declaring business completion. |

## Error classifications

| Result category | When used | Next action |
|---|---|---|
| `input_validation` | Package, header, field type or child-row shape violates a confirmed contract | Correct the affected input, rebuild and validate. Do not truncate or rewrite silently. |
| `catalog_mismatch` | Task identity, representation or package metadata disagrees with the effective catalog | Stop and reconcile the exact task identity. |
| `evidence_unresolved` | Applicable operation, ownership, identity, resolver, default or field behavior remains unresolved | Gather the missing evidence and recompile. This category does not mean unsupported. |
| `auth_authz` | An authorized read or execution lacks a valid identity or privilege | Return to the owning workflow. Never persist or print credentials. |
| `transport_environment` | Authorized transport fails or its response cannot be trusted | Record availability separately from a successful zero-match result. |
| `Fusion_API` | Fusion rejects the approved request | Preserve the sanitized error and affected requirement; determine the cause before another attempt. |
| `process_timeout` | The original attempt has no authoritative terminal state | Retain its process identity and last status; do not start another attempt. |
| `process_failed` | The original attempt reaches a failed terminal state | Retrieve sanitized logs and reconcile partial effects before another decision. |
| `artifact_persistence` | Required evidence or an immutable artifact cannot be saved | Stop at the persistence boundary and do not claim an auditable success. |
| `approval_blocker` | Approval for the exact current Data Loader candidate is absent or stale | Return to the immutable-preview approval step. |

## Disclosure and refusal rules

| Stage or condition | Required behavior |
|---|---|
| Source readiness | Enumerate each unresolved applicable operation, ownership, identity, field, resolver and default contract, including the exact missing fact. |
| Task validation result | Report the exact task, normalized scope, reached nodes, observed outcomes and remaining blockers. `BKC.VALIDATION_DONE` means task-rule validation only. |
| Before execution | Show the target environment, operation, immutable artifact, completed validations and candidate-bound approval required by Data Loader. |
| After an attempt | Report process status and fresh business-state reconciliation as separate outcomes. Mask secrets and protected data. |
| Reachable incomplete contract | Do not produce an executable plan or treat static generation as execution readiness. |
| Missing task-owned adapter | Do not invent key or lifecycle semantics or build a substitute candidate. |
| Failed or uncertain mutation | Do not retry automatically, switch integration routes, infer rollback or start a new submission. |
| Stale or changed candidate | Do not reuse approval for a different artifact, environment, operation or business scope. |
