# Manage Item Classes Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| License, product-model applicability, or consultant approval is missing | Stop before package preparation and disclose the missing applicability evidence. |
| Parent, existing-class identity, or explicit reference resolution returns zero, many, inactive, incompatible, cyclic, or unavailable | Stop and show normalized natural keys, match counts, eligibility result, and safe correction. |
| A required field, flag, integer key, generation method, or NIR parent-child identity is invalid | Classify as input validation, identify the affected row and field, and stop before package preparation. |
| An inherited lifecycle phase or attachment category is supplied as a child override | Preserve inheritance, remove the row from the child delta, and rerun validation. |
| EGO_ITEM_USER_DEF_ATTRS is supplied as a route association | Return Unsupported EFF Association; remove it from this package and route the EFF work to Manage Item Attribute Groups and Attributes followed by EGO_ITEM_EFF deployment. |
| An active class is renamed, repurposed, reparented, disabled, or removed without an approved impact assessment | Return Design Blocker and require downstream impact and migration approval. |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Continue only when every required member completed successfully with no warning or partial rows and every failure is proven outside this task; otherwise block. |
| Baseline, hierarchy, package inventory, preservation, semantic diff, ZIP validity, target identity, or fingerprint evidence is missing or changed | Return Package Contract Gap and rebuild from a fresh same-target task export. |
| Fusion rejects an archive that passed local validation | Persist the redacted primary process error and status, classify the failure, and do not retry automatically. |
| Import completes with a warning or post-import export does not contain an expected supported value | Reconcile with a fresh task export; classify unsupported EFF absence separately and do not replay the package blindly. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required value, type, enum, key, method mapping, or parent-child identity check fails | Correct the exact input and restart validation. |
| Applicability blocker | Licensed offering, customer model, or consultant approval is missing or incompatible | Establish applicability or route to Manage Default Item Class. |
| Design blocker | Hierarchy, item-creation policy, active-class impact, or supported association design is unsafe or unapproved | Correct the design and obtain the required business decision. |
| Reference-data validation | A parent or explicit supported reference cannot be resolved exactly | Refresh evidence or correct the reference; do not guess. |
| Unsupported EFF association | EGO_ITEM_USER_DEF_ATTRS is requested in this package path | Remove it and execute the dedicated attribute-group and EFF-deployment workflow separately. |
| Approval blocker | The final archive changed or is not bound to a current central preview and approval | Revalidate and let core.data-loader create a new preview and approval gate. |
| Package contract gap | Baseline, hierarchy, members, headers, preservation, ZIP, semantic diff, or fingerprint is incomplete | Refresh the export and rebuild locally. |
| Completed with warning | Fusion reaches a terminal warning state or a requested value is absent after import | Persist evidence and reconcile before any retry. |
| Partial success | Some supported rows verify and others do not | Preserve verified rows, report exact differences, and do not replay blindly. |
| Auth or authz | Required read or import privilege is unavailable | Refresh approved cached authentication once for a read, then stop. |
| Transport or environment | Network or target service fails before a side effect | Retry only a known idempotent read with bounded attempts. |
| Fusion API or process failed | Submission or child process fails | Persist redacted log and status and do not replay. |
| Process timeout | Process remains nonterminal beyond the allowed wait | Do not resubmit; report process ID, last state, elapsed wait, and next-check path. |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment, release, and task identity for EGO_MANAGE_ITEM_CLASSES |
| Applicability | Licensed offering, non-Common Product Model design, and consultant approval when a new class is requested |
| Baseline | Fresh same-target successful Manage Item Classes task export receipt |
| Hierarchy and identity | Exact eligible parent plus create, reuse, or explicit update classification |
| Supported scope | Only supported item-class and NIR rows; inherited phases and categories are excluded from the child delta |
| EFF separation | No EGO_ITEM_USER_DEF_ATTRS candidate association; separate attribute-group workflow and EGO_ITEM_EFF deployment are recorded when required |
| Package structure | Current ASM metadata, expected member hierarchy, exact CSV headers, order, and encoding |
| Preservation | Every unrelated row and untouched member is preserved |
| Archive validity | Final immutable archive is a valid ZIP |
| Fingerprint | SHA-256 of the exact final archive |
| Review evidence | Final member inventory and row/member semantic diff against the baseline |
| Freshness | No source, mapping, package member, target identity, or fingerprint changed after validation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or reference failure | Affected row, normalized field or natural key, sanitized value, match count or accepted values, and safe correction. |
| Design failure | Blocking rule, downstream impact, delegated workflow when applicable, and required decision. |
| Broader export exception | Overall process state and ID, every failed object from the exact log, required-member states and row counters, archive fingerprint, and task-scope decision. |
| Package readiness | Target and task, supported delta, inheritance treatment, EFF separation, inventory, semantic diff, and fingerprint. |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that validation and handoff are complete; the central Data Loader preview has not yet been created or approved. |
| Import or verification failure | Failure class, environment, task code, stage, redacted evidence, external IDs, verified partial results, and recommended action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous evidence | Do not fuzzy-match, select the first row, infer physical IDs, or call undocumented endpoints. |
| Inherited setup | Do not copy inherited phases or attachment categories into the child-class delta. |
| Unsupported EFF association | Do not claim that a successful or warning Manage Item Classes import added the EFF attribute group. |
| Uncertain write | Do not replay until read-only reconciliation establishes the actual side effects. |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion. |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate. |
| Final archive changed | Do not reuse the readiness result or central preview; require complete revalidation and a new preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MICS.PACKAGE_PREVIEW_GATE | decision | 50 | execution_gate | ready->MICS.READY_FOR_DATA_LOADER_PREVIEW;blocked->MICS.HANDLE_ERROR;failure->MICS.HANDLE_ERROR | MICS.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow produces the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| MICS.HANDLE_ERROR | step | 60 | error_handler | handled->MICS.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, enforcement, or package-readiness failure |
| MICS.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| MICS.READY_FOR_DATA_LOADER_PREVIEW | terminal | 80 | terminal | none | MICS.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
