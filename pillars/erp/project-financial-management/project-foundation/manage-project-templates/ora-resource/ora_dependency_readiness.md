# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Exact target, identity, and full current requested-surface baseline |
| 2 | Prepared request completeness | After documented defaults and reference resolution, verify one supported representation for each actual required value; request only values still unresolved. Server-derived omissions follow input-validation rules |
| 3 | Child operations | Each requested documented child family/action, schema, operation-specific runtime overlay, and local payload preflight resolves; returned URIs are required only for operations on an existing parent |
| 4 | Use/route/approval | Consumer impact, complete route, immutable preview, and approval pass |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PTMPL.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_template_scope | Prevent cross-target write | Supply target | Scope |
| PTMPL.BASELINE | Full requested REST-surface baseline | Yes | Update/end-date/child CUD | Lookup | Target REST GET | find_project_template | Safe preserve/diff | Read all requested core fields/children | Baseline/returned links |
| PTMPL.REFERENCES | Documented reference representations | Yes | Create/reference change | Validate | Target REST operation schema and prepared request values | resolve_template_references | Prevent malformed or conflicting request fields without demanding customer knowledge of internal IDs | Verify prepared representations after defaults/resolution; request only unresolved required references. Supported root names pass directly and Fusion validates eligibility on POST | Canonical values |
| PTMPL.REQUIRED_ID | Operation-required ID conversion | Conditional | Exact operation/runtime contract requires an ID and customer supplied only its documented name | Lookup | Target-proven standalone resource in the correct ID domain | resolve_required_reference_id | Satisfy an actual ID-only contract without using another template's context | Resolve exactly one mapping and show it in preview; zero/multiple/unproven resolver blocks | Name, ID, source, cardinality |
| PTMPL.PLAN_TYPE | Project plan type representation | Conditional | Project plan type supplied | Validate | Published Project Templates schema and supplied value | resolve_project_plan_type | Prevent an invalid attribute representation | Use `ProjectPlanType` or `ProjectPlanTypeId`, never `ProjectPlanTypeName` | Exact canonical field/value |
| PTMPL.WORK_TYPE | Template/task work type | Conditional | Supplied or explicitly required by fresh operation-specific create metadata | Validate | Published operation schema, supplied value and target create evidence | resolve_template_references | Preserve optionality and documented task inheritance | Supply one supported representation only when requested or truly operation-required | Exact work type representation |
| PTMPL.TEMPLATE_ROW | Template-row applicability | Yes | Create Template page | Verify | Template indicator | find_project_template | This page applies only to template rows | Keep the template indicator in scope | Template row |
| PTMPL.PRIORITY | Project priority code resolution | Conditional | A priority display name is supplied | Lookup | Complete standard lookup target evidence and selected target business date | resolve_project_priority | Prevent a display meaning being submitted as a code | Resolve exactly one enabled effective member; zero/multiple matches block | ProjectPriorityCode and redacted resolution evidence |
| PTMPL.SECTIONS | Child/setup operations | Conditional | Child/setup change | Validate | Published nested/direct operation schemas, documented defaults, fresh target inheritance context and returned links when the parent exists | resolve_template_sections | Prevent partial/inconsistent template | Apply documented defaults and evidenced task flag inheritance. Do not require or synthesize omitted nested task organization from a root display name; verify Fusion-derived values on task readback. Direct-create organization prerequisites remain applicable. Prepare omitted nested external IDs through the defaulting policy and bind them to approval; direct-create requiredness remains operation-specific | Body fields/URIs/keys/options/default evidence |
| PTMPL.CODE_VALUES | Documented code-only display values | Conditional | A registered display-name alias is supplied | Lookup | Named standard lookup type and complete target lookup evidence | resolve_template_code_values | Avoid guessed codes while preserving supported names | Resolve one enabled effective result, or block; API-supported name/hint fields pass directly | Canonical code and redacted supplied-name evidence |
| PTMPL.PAYLOAD_PREFLIGHT | Exact payload contract | Yes | Every write preview | Verify | Exact JSON bytes, fresh target operation metadata, and runtime overlays | verify_template_route | Prevent unknown fields, omitted runtime requirements, conflicts, and malformed values before approval | Run the task-local validator and preserve its report; describe the result as structurally ready, not guaranteed target acceptance | Matching payload/schema checksums and zero issues |
| PTMPL.USE | Existing consumers | Conditional | Semantic/end-date change | Lookup | Documented target REST use evidence | resolve_template_use | Prevent downstream project creation impact | Resolve consumers | Counts/impacts |
| PTMPL.ROUTE | Complete workflow route and authorization checkpoints | Yes | Every write | Verify | Active workflow classification, selected executor, published REST contract, authenticated target read, and required adapter/registration evidence | verify_template_route | Prevent partial write or import-routing bypass without requiring a probe | Imports enter core.data-loader; direct task operations require explicit non-import selection. Consuming workflow binds approval to the exact artifact and retains sanitized receipts | Classification/executor/methods/paths/coverage/checksum/registration |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All dependencies ready | Yes |
| Missing artifact | Baseline/section/use/route evidence absent | No |
| Conflict | Duplicate identity/child, hidden prerequisite, active-use impact | No |
| Unsupported | Root delete, duplicate/copy, FSM/CSV import, missing REST CUD method/schema, or incomplete requested write surface | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.RESOLVE_DEPENDENCIES | step | 6 | resolve_dependency | ready->PTMPL.ENFORCE_DESIGN;missing->PTMPL.RETURN_ISSUES;conflict->PTMPL.RETURN_REFUSAL | PTMPL.ROUTE_OPERATION | stop | Before preview/validation completes |
