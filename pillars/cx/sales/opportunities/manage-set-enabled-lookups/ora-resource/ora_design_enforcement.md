# Manage Set Enabled Lookups Design Enforcement

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Apply these mandatory gates after every affected lookup parent, returned
reference group, set, current state, and route-specific dependency has been
resolved.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task and lookup scope | Keep task identity fixed to FND_MANAGE_SET_ENABLED_LOOKUPS and lookup scope limited to the two directly owned types |
| 2 | Bind explicit set choice, parent, and set | Ask the Common-vs-different-set question when needed, then use each parent's returned nonblank ReferenceGroupName to resolve the confirmed exact set and any requested business-unit assignment |
| 3 | Compare operation with current state | Permit Create only for an absent code and Read, Update, Disable, or Delete only for one exact existing code in the resolved set |
| 4 | Protect identity and fields | Preserve type, code, set, reference group, module, audit, seed, and returned item identity; permit only validated mutable fields |
| 5 | Validate route evidence | For FSM, validate fresh export, exact package contract, every row delta, impact, state lock, and immutable hash; for REST, validate one exact method, link, body, impact, preview, and approval |
| 6 | Enforce execution boundary | Default Create, Update, and Disable to FSM; allow requester-selected REST or verified final REST_FALLBACK with all route gates passed; use Delete only through explicitly selected direct REST; never treat accepted Data Loader initiation as permission to poll |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | resolve_set_enabled_lookup_parent | Affected parent is missing or ambiguous, returns blank ReferenceGroupName, lacks canonical metadata, falls outside this adapter's exact catalog mapping, or the workflow assumes ReferenceGroupName from LookupType | Re-run the parent GET, prove catalog ownership, and use only its returned nonblank ReferenceGroupName and metadata | Yes |
| Every request except Package Export without row scope | Blocker | resolve_lookup_reference_set | SetSelectionDecision is missing; Common Set was inferred or resolves to a non-Common set; SetId/SetCode is malformed, unknown, cross-environment, ambiguous, or conflicts with another selector, package row, or requested BU assignment; or the assignment doesn't match the parent-returned ReferenceGroupName | Ask whether Common Set should be used or a different exact Set ID/Set Code should be selected; resolve or preserve one exact confirmed set per row and complete the record-set prerequisite outside this skill when an assignment is absent | Yes |
| Create | Blocker | resolve_set_enabled_lookup_state | The exact LookupCode already exists in the resolved set or absence evidence is stale | Refresh exact state and use Update only when that is the requester's intent | Yes |
| Read, Update, Disable, or Delete | Blocker | resolve_set_enabled_lookup_state | No exact LookupCode exists in the resolved set | Supply an existing code; never silently convert the operation to Create | Yes |
| Update, Disable, or Delete | Blocker | resolve_set_enabled_lookup_state | Current-state lock or returned child item identifier/link is missing, stale, or doesn't match the intended row | Re-read the exact child and rebuild route evidence | Yes |
| Any mutation | Blocker | resolve_set_enabled_lookup_state | LookupType, LookupCode, SetId, SetCode, ReferenceGroupName, ModuleId, audit, seed, or returned item identity changes, or an unsupported field is present | Preserve immutable identity and restrict the delta to validated mutable fields | Yes |
| Package Export | Blocker | resolve_set_enabled_lookup_parent | A single set selector or LookupCode is incorrectly required, or export scope is narrowed without explicit supported evidence | Export the complete exact task; allow both owned types and multiple rows | Yes |
| Package Import or FSM Create, Update, or Disable | Blocker | verify_set_lookup_package_readiness | Same-target freshness, task identity and persisted Data Loader task context, ASM identity, member inventory, headers, row counts, per-row set, row delta, impact, state lock, final SHA-256, or immutable handoff evidence is absent or inconsistent | Refresh the task export, rebuild the smallest exact package delta, and validate every changed row | Yes |
| Native FSM package with several rows or both owned types | Blocker | verify_set_lookup_package_readiness | Any changed row is invalid, targets another lookup type, lacks an exact set or state lock, encodes Delete, or wasn't included in the reviewed impact and hash | Correct the complete package; never submit a partial subset under the approved fingerprint | Yes |
| Direct REST Create | Blocker | resolve_set_enabled_lookup_state | Route is neither explicitly selected nor verified REST_FALLBACK, parent editability/REST-security evidence is missing, exact absence isn't proven, method isn't collection POST, body includes unsupported or immutable fields, Upsert-Mode isn't false, or preview/approval is incomplete | Build a fresh create-only POST preview from current parent metadata with Upsert-Mode=false and obtain separate approval | Yes |
| Direct REST Update or Disable | Blocker | resolve_set_enabled_lookup_state | Parent editability/REST-security evidence is missing, method isn't PATCH to the returned item link, body includes more than the intended mutable delta, current state or impact is stale, or preview/approval is incomplete | Rebuild one exact PATCH preview from current parent metadata and the returned item, then obtain separate approval | Yes |
| Delete | Blocker | resolve_set_enabled_lookup_state | Route is FSM or wasn't explicitly selected as REST; parent metadata doesn't support the operation; method isn't bodyless DELETE to the returned item link; historical/downstream impact, preview, or approval is incomplete | Prefer Disable, or complete the exact destructive REST preview from current parent metadata and obtain separate approval | Yes |
| LookupType is MOO_SETID_REVN_CATEGORY | Blocker |  | The request actually targets standard lookup MOO_REVN_CATEGORY | Route standard revenue-category maintenance to its dedicated task | Yes |
| Inventory or Read | Blocker | resolve_set_enabled_lookup_state | Read-only evidence is treated as mutation authorization | Return sanitized current state only | Yes |
| Accepted Data Loader initiation | Blocker |  | The same request attempts to poll status, retrieve ProcessLog, or run live verification after Fusion accepted initiation | Return the accepted initiation result and wait for a later explicit status or verification request | Yes |

| REST_FALLBACK | Blocker | verify_set_lookup_rest_fallback | Dedicated verifier did not return eligible, receipt is missing/stale/cross-target, CSV is repairable, jobs are pending/uncertain, diagnostics incomplete, or rows partially applied | Exhaust applicable CSV recovery and reconcile all prior submissions; then fresh parent/set/state and a separate immutable REST preview. All-applied returns without a write | Yes |
| Every changed FSM child | Blocker | verify_set_lookup_package_readiness | Matching unchanged in-package parent linkage or exact resolved SetCode is missing/conflicting | Add or retain one unchanged support parent per affected owned type; preserve unrelated baseline rows and never hand off a child-only package | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_set_enabled_lookup_parent | Every request | Exact catalog-owned parent identity, returned nonblank ReferenceGroupName, ModuleId, CustomizationLevel, RestAccessSecured, and self/canonical links for every affected type | ora_reference_lookups.md |
| resolve_lookup_reference_set | Every request except Package Export with no row scope | Per-row ReferenceGroupName, SetId, SetCode, optional BUOrgId, and assignment status | ora_reference_lookups.md |
| resolve_set_enabled_lookup_state | Inventory, Read, direct REST, and every changed package row | Current or absent state lock, lookup timestamp, and returned child item identifier/link when present | ora_reference_lookups.md |
| verify_set_lookup_package_readiness | Package Import or FSM Create, Update, or Disable | Fresh baseline, task identity and persisted Data Loader task context, metadata/member/header receipt, parent linkage, row delta, impact, state locks, final hash, and Data Loader handoff evidence | ora_reference_lookups.md |

| verify_set_lookup_rest_fallback | Before final fallback preview | Same-target classified exhaustion receipt, applicable recovery outcomes, fully reconciled prior submissions, fresh exact row reads and RestFallbackEligible=true | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SET_LOOKUP.DESIGN | decision | 7 | design_enforcement | pass->OPP.SET_LOOKUP.GATE;blocked->OPP.SET_LOOKUP.RETURN_MISSING;failed->OPP.SET_LOOKUP.RETURN_FAILED | OPP.SET_LOOKUP.DEPENDENCY | stop | Before returning read-only results, routing Export, handing an immutable FSM package to Data Loader, or submitting an approved REST mutation; reject automatic Common Set assignment |
