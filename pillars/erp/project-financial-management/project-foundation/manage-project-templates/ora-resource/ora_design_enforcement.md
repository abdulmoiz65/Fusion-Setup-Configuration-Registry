# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity/dates | One exact template and valid availability |
| 2 | Validate core context | BU, project unit/type, organization, status agree |
| 3 | Validate child operations | Requested setup options and child rows have complete REST contracts |
| 4 | Protect consumers/route | Downstream impact and full route coverage are safe |
| 5 | Protect approval | Customer approves the exact business change; the runtime binds that approval to the exact payload checksum internally |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create/update/duplicate | Blocker | find_project_template | Duplicate/ambiguous identity or bad dates | Correct identity/dates | Yes |
| Core context | Blocker | resolve_template_references | A required context field is missing, uses conflicting alternatives, or is absent from the target operation schema | Supply one documented representation. Fusion validates activity and compatibility on POST. | Yes |
| Project plan type | Blocker | resolve_project_plan_type | Payload contains ProjectPlanTypeName, conflicting alternatives or a plan-type field absent from the operation schema | Normalize the name to ProjectPlanType or use one supplied ProjectPlanTypeId | Yes |
| Project priority | Blocker | resolve_project_priority | Display-name lookup has zero/multiple enabled effective matches, incomplete evidence or malformed eligibility dates | Resolve exactly one target code and retain redacted evidence before preview; never guess or silently select one | Yes |
| Setup option/child operation | Blocker | resolve_template_sections | Missing prerequisite, duplicate key, unknown child field, unsupported verb, or incomplete operation schema | Correct/preserve section; do not require future item/child links for an atomic root create | Yes |
| Task create | Blocker | resolve_template_sections | Missing TaskName or required booleans after evidenced inheritance; missing direct-create organization or fresh operation-required nested organization; an ID-only contract with no proven mapping; missing work type only when fresh operation-specific metadata requires it; invalid, duplicate or conflicting generated external IDs; invalid supplied hierarchy/date/value or response-only field | Preserve omitted nested task organization for Fusion derivation and verify readback; apply other defaults/inheritance, require actual unresolved inputs, and validate target operation requirements | Yes |
| Existing semantic/end-date change | Blocker | resolve_template_use | Unknown or unsafe project/integration impact | Preserve or phase change | Yes |
| REST route | Blocker | verify_template_route | Any requested surface is absent from the published operation schema, an exact operation-required ID cannot be resolved safely, or repository-required CUD registration is absent at submission | Correct the exact gap; do not pre-resolve a supported root name or treat a zero-row GET's missing write/child links as evidence of unsupported create | Yes |
| Payload preflight | Blocker | verify_template_route | Validator status is not passed, current metadata is missing, or the consuming workflow's current payload/target/method/URI/route differs from the approval record | Validate and preserve the immutable artifact; verify approval-bound integrity immediately before dispatch. Any change needs a new preview and approval. The shared REST client need not implement task-specific approval or diagnostic flags | Yes |
| Execution routing | Blocker | verify_template_route | Workflow classification/executor is absent or ambiguous, or an import/load bypasses core.data-loader or lacks its selected adapter/registration and approved artifact | Record the active workflow route; complete Data Loader checks for imports. A direct task operation must be explicitly selected outside import scope, never relabeled to evade import gates | Yes |
| Task number or external ID change | Blocker | resolve_template_sections | Preview promises independent TaskNumber and ExternalTaskId preservation despite evidenced coupled behavior | Show both resulting values and verify both on task readback; stop remaining writes on an unexpected coupled change | Yes |
| Customer approval surface | Blocker | verify_template_route | Approval request asks the customer to reconcile internal hashes or omits the target business change | Present the target, template, references, dates, child tasks, method, and endpoint in business terms and ask one approve/decline question; retain hashes only in the machine record | Yes |
| Existing-template contextual LOV | Blocker | resolve_template_references | A new-template create attempts to call another template's ProjectTypes, ProjectUnits, or OwningOrganizations LOV | Remove the lookup. Preserve supported customer-supplied names and let the approved POST validate their compatibility. | Yes |
| Delete/duplicate/copy/FSM/CSV import | Blocker |  | Unsupported REST contract | End-date only when documented/authorized | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_project_template | Every request | Stable identity/baseline | ora_reference_lookups.md |
| resolve_project_priority | Priority display name supplied | Exactly one enabled effective lookup code, target business date and redacted resolution evidence | ora_reference_lookups.md |
| resolve_template_code_values | A registered code-only display-name alias is supplied | One enabled effective member of the documented target lookup type, canonical code and supplied-name evidence | ora_reference_lookups.md |
| resolve_template_references | Create/reference change | Canonical documented name/ID/code representation and local field shape | ora_reference_lookups.md |
| resolve_project_plan_type | Project plan type supplied | Canonical attribute and exact customer-supplied name or ID | ora_reference_lookups.md |
| resolve_required_reference_id | Exact operation requires an ID not supplied by the customer | Proven standalone resolver, exact name, correct ID domain, cardinality-one mapping | ora_reference_lookups.md |
| resolve_template_sections | Section/child/copy change | Keys/options/prerequisites/copy map | ora_reference_lookups.md |
| resolve_template_use | Semantic/end-date change | Consumer counts/impact | ora_reference_lookups.md |
| verify_template_route | Every write | Methods/field-child REST coverage and CUD authorization | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.ENFORCE_DESIGN | decision | 7 | design_enforcement | pass->PTMPL.EXECUTION_GATE;blocked->PTMPL.RETURN_REFUSAL;failure->PTMPL.RETURN_ISSUES | PTMPL.RESOLVE_DEPENDENCIES | stop | Before write approval |
