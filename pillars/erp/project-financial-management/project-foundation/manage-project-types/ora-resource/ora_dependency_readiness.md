# Dependency Readiness

Offline dynamic verification is optional when no source is authored or a supplemental eligibility check is unavailable. A resolver may return validated or deferred_to_fusion with blocking=false. The latter is a completed pre-upload disposition, not proof of membership. Missing package/baseline required for preservation or missing required CSV input is a separate issue.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Exact target and fresh Project Type export |
| 2 | Set/use state | Set code supplied/resolved; use-state checked when available or explicitly deferred |
| 3 | Conditional references | Known constraints checked; dynamic references validated or explicitly deferred |
| 4 | Package/approval | Exact package and immutable approved preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PTYPE.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_project_type_scope | Prevent cross-target write | Supply target | Scope |
| PTYPE.BASELINE | Current joined export | Yes | Update/import | Lookup | current_export | find_project_type | Preserve groups/children | Export fresh | Baseline |
| PTYPE.USE | Project/template use | Conditional | Protected mutation | Lookup | it has no data source; use provided current evidence when present | resolve_project_type_use | Prevent inherited semantic breakage | Apply known restrictions; unknown state is deferred_to_fusion | Known use state or deferred status |
| PTYPE.REFS | Conditional references | Conditional | Referenced group changes | Lookup | Individual validated or deferred_to_fusion resolver outputs | resolve_project_type_references | Ensure valid inherited defaults | Resolve named dependency | IDs/codes |
| PTYPE.WORK_TYPE | Work-type reference | Conditional | Work type change | Lookup | Current target active work types | resolve_project_type_work_type | Actual LOV proves active-date eligibility, not a billing/capitalization predicate | Resolve one eligible value | PJF_PROJECT_TYPE.csv.Name |
| PTYPE.SET | Set | Conditional | Set supplied or changed | Lookup | Completed current-target set REST collection from resolve_project_type_set | resolve_project_type_set | Canonical set code required | Resolve from the shared collection; unavailable retrieval still defers membership non-blockingly with supplied CSV-ready code | SetCode |
| PTYPE.BURDEN_SCHEDULE | Cost burden schedule | Conditional | Burden schedule supplied or required | Lookup | Current target schedule and eligibility evidence | resolve_project_type_burden_schedule | Prevent accepting task-specific or inactive schedules | Use the verified resolver predicates; unavailable complete UI coverage remains non-blocking | IndSchName |
| PTYPE.BURDEN_PROJECT | Burden destination project | Conditional | BurdenCostFlag Y, BurdenAmtDisplayMethod S and BurdenAccountFlag Y | Lookup | Current target eligible project evidence | resolve_project_type_burden_project | Establish component destination identity; separate-item D uses the raw-cost project/task | Resolve destination when possible; otherwise retain supplied name and defer membership | Name2 and internal ProjectId |
| PTYPE.BURDEN_TASK | Burden destination task | Conditional | Same-item component routing enabled and optional task supplied | Lookup | Resolved parent and current task candidates | resolve_project_type_burden_task | Task name input must produce task number and correct owning project | Resolve within selected project when possible; otherwise retain supplied task number and project names; do not require a task or run for D | ElementNumber, Name1 |
| PTYPE.CLASS_CATEGORY | Classification category | Conditional | Class assignments supplied | Lookup | it has no data source | resolve_project_type_class_category | Category names and defaults must be authoritative | Use supplied category name; defer unavailable membership/default checks | ClassCategory and default flags |
| PTYPE.LANGUAGES | Translation languages | Conditional | Translation language supplied | Lookup | it has no data source | resolve_project_type_languages | Canonical eligible language code required | Retain supplied codes; defer installation/activation eligibility | Language, SourceLang |
| PTYPE.DFF | Deployed flexfields | Conditional | Context or segments supplied | Lookup | it has no data source | resolve_project_type_flexfields | Context controls segment meaning and eligibility | Preserve supplied scoped values; defer deployed validation non-blockingly | Scoped context and segment values |
| PTYPE.AUTO_ASSET_MODE | Automatic asset allocation mode | Conditional | Mode supplied or changed | Lookup | Verified fixed control representation | resolve_project_type_auto_asset_mode | DIRECT_COSTS/ALL_COSTS are proven serialized values | Validate actual code or resolved control intent | AutoAssetLineAllocateMode |
| PTYPE.PACKAGE | FSM contract | Yes | Import | Verify | Template/generated package | verify_project_type_package | Loader contract | Preserve checksum | Contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Applicable checks passed or have explicit non-blocking deferred_to_fusion dispositions | Yes; normal approval and execution workflow applies |
| Deferred to Fusion | Dynamic offline source or supplemental eligibility unavailable | Yes; record it has no data source where applicable and defer validation to upload results |
| Missing artifact | Required package/baseline/template or required CSV input missing | No; collect the actual required artifact/value; missing offline dynamic source alone is not this category |
| Protected mutation | In-use semantics would change | No; preserve value |
| Unsupported | Delete/direct setup REST write | No; return refusal |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.RESOLVE_DEPENDENCIES | step | 6 | resolve_dependency | ready->PTYPE.ENFORCE_DESIGN;deferred->PTYPE.ENFORCE_DESIGN;missing->PTYPE.RETURN_ISSUES;conflict->PTYPE.RETURN_REFUSAL | PTYPE.ROUTE_OPERATION | stop | Before preview/validation completes |

## Refined Operational Readiness

- **BP-033 — Readiness recommendation:** Before downstream billing use, assess transaction controls, billability, contract linkage, revenue method and rate-schedule behavior. These are not additional project-type create inputs. Validate a supplied Work Type through its existing resolver, but do not demand separate billing-design evidence to set EnableBillingFlag Y. Missing downstream evidence is readiness_not_assessed and does not block the setup preview/load or prove billing readiness.
- **BP-035 — Operational control:** Produce a quarterly report of project type, active-project count, billing/capitalization/burden/sponsored flags, default schedule, override permission, and last-used date; retire unused types and flag near-duplicates.

## Evidence Ownership

Reference resolver authority and deferral boundaries come from [Source Evidence Index](ora_reference_lookups.md#source-evidence-index), especially SRC-FSCR and PT-POL-001. The prerequisite list is task-local readiness, not an implementation program. BP-033 is a non-blocking downstream readiness recommendation; BP-035 governs an operational-readiness claim. Missing evidence for either must not be reported as Oracle setup validation failure.
