# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Exact target and full current work-type export |
| 2 | Sets/children | Complete supported set/language checks; carry missing DFF or eligibility authority as nonblocking warnings without claiming full validation |
| 3 | Profile/use | Required consumer-impact handoff satisfies resolve_work_type_use before affected existing-identity changes proceed; absent source route or evidence stops the workflow |
| 4 | Package/approval | Exact final immutable archive and verified Data Loader preflight; Task Hook validation completes before the loader's preview/approval gate; approval is required only for submission |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| WTYPE.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_work_type_scope | Prevent cross-target write | Supply target | Scope |
| WTYPE.BASELINE | Full current work type | Yes | Update/import | Lookup | current_export | find_work_type | Safe diff | Export all members | Baseline |
| WTYPE.SETS | Reference set membership | Conditional | Set supplied or explicitly changed | Lookup | Complete target set collection; original name/code input type; current assignment baseline for proposed changes | resolve_work_type_sets | Resolve the intended set in its supplied field without cross-field fallback or invented eligibility filters | Do not ask for a set when omitted on create; preserve omitted assignments on update. For supplied assignments, supply the set name; identify a code explicitly only when intended. A unique name derives its code without another question | Canonical SetCode, original input type, matched field and reference display evidence |
| WTYPE.CHILDREN | Languages/DFF | Conditional | Child/DFF change or create | Lookup | Current translation catalog, DFF evidence result and retained translation-name collision evidence declared by the child resolver | resolve_work_type_children | Prevent invented or lost fields and conflicting translated names | Resolve supported fields; preserve omitted groups; require the completed name-collision check when translation rows are supplied. Only optional DFF/eligibility authority remains a nonblocking warning | Child results, required name-collision result and optional skipped-check warnings |
| WTYPE.LANGUAGE_SOURCE | Language catalog | Conditional | Translation rows supplied | Lookup | Declared languagesLOV REST read | acquire_work_type_languages | Separate identity from installation state | Use the configured target and shared REST client | Complete scoped language catalog |
| WTYPE.DFF_SOURCE | Flexfield validation evidence | Conditional | Create or DFF change | Verify | Declared metadata evidence boundary | resolve_work_type_dff_context | Deployed requiredness and segment mappings cannot currently be acquired | Return REFERENCE_UNRESOLVED, Warning, blocking=false; continue supported checks/preview without waiver, preserving proven supplied representation | Warning with skipped checks; no invented segment validation |
| WTYPE.USE | Profile/consumer state | Conditional; mandatory for applicable existing-identity impact diffs | Actual billable/utilizable/transfer, availability-date or set-assignment change on an existing identity | Verify | work_type_use_evidence captured by the active caller | resolve_work_type_use | Prevent billing/cross-charge/reporting disruption | Stop affected imports when the required handoff or supported source route is missing; resolve the workflow gap before a fresh run | Validated impact facts, or blocking missing/failure result |
| WTYPE.PACKAGE | FSM contract | Yes | Import | Verify | Current template/export, final immutable archive and retained preparation context | verify_work_type_package | Loader safety | Validate the exact prepared package before preview; Data Loader owns its later approval-bound archive verification; keep integrity values internal | Contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All dependencies ready | Yes |
| Missing artifact | Required baseline, package/template, consumer-impact handoff/source route or translation-name collision evidence absent, invalid, stale or incomplete | No; required impact evidence uses missing to RETURN_ISSUES; required child-check gaps use RESOLVE_CHILDREN failure to RETURN_ISSUES. Neither becomes a reference warning |
| REFERENCE_UNRESOLVED | Missing DFF/reference membership authority or unverified eligibility parity; no proven invalidity; excludes required consumer-impact evidence | Yes; Warning, blocking=false; complete remaining supported checks and preview with disclosure |
| Conflict | Duplicate assignment or unsafe set removal, invalid transfer/DFF/translation, active-use impact | No |
| Unsupported | Delete/direct setup REST mutation | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.RESOLVE_DEPENDENCIES | step | 6 | resolve_dependency | ready->WTYPE.ENFORCE_DESIGN;warning->WTYPE.ENFORCE_DESIGN;missing->WTYPE.RETURN_ISSUES;conflict->WTYPE.RETURN_REFUSAL | WTYPE.ROUTE_OPERATION | stop | Before preview/validation completes; required consumer-impact gaps use missing; only optional reference-authority warnings remain nonblocking |
