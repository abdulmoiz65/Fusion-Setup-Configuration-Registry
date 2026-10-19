# Location Costing Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Operation | Select Query, Create, Update, Correct, End Date, or Zap before any network call. |
| 2 | Legislative Data Group | Discover candidates and confirm one exact returned LDG with its costing context. |
| 3 | Location | Resolve one exact LDG-filtered Location and classify Create presence when applicable. |
| 4 | Operation branch | Run only the branch-specific reads listed below; skipped branches perform no lookup. |
| 5 | Import readiness | For a mutation, require current template validation, an immutable preview, an authorized routed loader workflow, and fresh approval before handoff. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ldg_candidates | LDG candidates | Yes | Every request | Lookup | Read-only LDG LOV candidate response | search_legislative_data_groups | Prevents guessing an LDG identity. | Provide LDG search text and select one returned Name only when the result is not unique. | SelectedLegislativeDataGroupName; SelectedLegislativeDataGroupId |
| confirmed_ldg | Confirmed LDG and costing context | Yes | Every request | Lookup | Read-only exact LDG LOV response | confirm_legislative_data_group | Supplies the exact LDG ID and the costing flex number used by later branch lookups. | Correct the selected candidate if exact confirmation fails. | LegislativeDataGroupName; LegislativeDataGroupId; LegislationCode; CostAllocationIdFlexNumber |
| location_source | Exact Location source | Yes | Every request | Lookup | Read-only LocationCostSearchVO response | resolve_location_source | Supplies LocationId, LocationCode, and Create presence evidence. | Provide an exact code or a uniquely matching name. | LocationId; LocationCode; LocationName; SourceId; CreatePresenceResult |
| location_set | Authoritative Location SetCode | Conditional | Create, Update, Correct, End Date, or Zap | Lookup | Read-only locationsLov response | resolve_location_set_code | SetCode is required by the loader identity; a display SetName is not a substitute. | Resolve one row matching both LocationId and LocationCode. | LocationSetCode |
| current_allocation | Effective current allocation | Conditional | Query, Update, or Correct | Lookup | Read-only Generic Costing response | query_location_costing | Supplies exact current parent and account state only to branches that require it. | Provide a precise effective date and stop on ambiguous state. | CurrentParent; CurrentAccounts; PhysicalAccountIdentity; SubTypeSequence |
| costing_kff | Runtime Costing KFF | Conditional | Create, Update, or a Correct account MERGE containing Segment values | Lookup | Read-only runtime KFF describe response | resolve_runtime_costing_kff | Confirms the current Segment layout for account input. | Correct unsupported Segment input before preview. | RuntimeSegmentDefinitions |
| effective_history | Complete effective history | Conditional | End Date or Zap | Lookup | Read-only terminal PayCostSearchVO page set | query_location_costing_history | End Date needs the latest split; Zap needs the complete historical parent scope. | Page contiguously from offset zero through explicit hasMore=false. | EffectiveHistory; HistoricalParentKeys |
| history_accounts | Historical account fan-out | Conditional | Zap | Lookup | One read-only Generic Costing item response per history key | query_location_costing_history_accounts | Supplies every physical child bound to its historical parent. | Stop when any parent has no exact detail response or any returned identity conflicts. | ZapHistoryParents; ZapHistoryAccounts |
| loader_template | Current Data Loader template and component capability validation | Yes | Create, Update, Correct, End Date, or Zap | Verify | Output of the active governed import workflow; target-environment CostAllocationV3 Component Details, Date Effectivity evidence for End Date only | | Confirms the intended member, keys, dates, action, and returned Zap Segment fields and applies the End Date DAT shape and HDL SET instructions checks from ora_input_validation.md to the final source bytes only for each check's stated operation scope. Before End Date rendering, require evidence that CostAllocationV3 in the target environment supports changing the last effective end date. ReplaceLastEffectiveEndDate is an Oracle special attribute that need not appear in the template or Attributes tab; permit its template-membership exception only for End Date on that component with confirmed capability. No other absent attribute is covered by this exception. | Missing or negative capability evidence blocks End Date. If the shared validator rejects the confirmed special attribute, report a validator limitation and stop; do not substitute a SET instruction, suppress validation, or report a pass. | TemplateValidation; FinalSourceValidation; ComponentCapabilityEvidence for End Date only |
| immutable_preview | Immutable preview and approval | Yes | Create, Update, Correct, End Date, or Zap | Verify | Exact artifact and approval produced by the active governed import workflow | | Prevents authoring guidance from authorizing or replaying a Fusion mutation. Any corrected DAT or rebuilt ZIP invalidates the earlier validation and approval. | The active governed import workflow must produce a new ZIP, repeat final source/schema and Task Hook validation, and request fresh approval bound to its SHA-256, target environment, operation, and business effect before handoff. | PreviewFingerprint; ApprovalFingerprint; AuthorizedWorkflow |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The exact dependency evidence is present and valid for the selected operation. | Yes |
| Lookup | A named read-only resolver must obtain the value. | Yes, lookup only |
| Verify | An authorized external workflow must supply template, preview, or approval evidence. | Verify only |
| Blocked | A required value is missing, ambiguous, inconsistent, stale, or belongs to another operation branch. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCP.CHECK_DEPENDENCIES | decision | 700 | resolve_dependency | ready->LCP.APPLY_DEFAULTS;blocked->LCP.HANDLE_ERROR;unsupported->LCP.HANDLE_ERROR | none | stop | Recheck only the dependencies applicable to the already selected mutation branch before defaults or design enforcement. |
