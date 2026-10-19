# Performance Templates Design Enforcement

Sources: [REST resource and field guidance](../../performance-template-rest-source-contract.md) and existing setup guidance. Verify UI-only restrictions for the target release and environment.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce lifecycle state | Reject operations blocked by in-use, documents/periods, read-only, ESS, permission, or child-reference state. |
| 2 | Enforce root and child shape | Allow only writable fields through the documented owning accessor; reject technical, derived, stale, and display-only values. |
| 3 | Enforce parent and feature dependencies | Apply process-flow/role, ratings, participant, matrix-manager, section/item, questionnaire, dynamic-skills, date, and content/profile dependencies. |
| 4 | Enforce dependent-field invariants | Re-evaluate every applicable dependent relationship after normalization. A bypass request or residual contradiction blocks the run. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any mutation request | Error | inspect_template_rest_metadata | The request contains nonupdateable, derived, technical, display-only, generated-id, or unsupported child attributes | Remove disallowed attributes and use the owning accessor | Yes |
| A template, role, section, role action, period, or questionnaire is changed or deleted | Error | read_template_by_id | In-use, document, period, role-action, ESS, permission, or read-only state blocks the requested lifecycle operation | Stop or select an operation permitted by the current lifecycle state | Yes |
| A process flow is selected | Error | resolve_active_process_flow | The selected process flow does not contain the required task or is not active and effective | Resolve the process flow through its documented lookup, then select a compatible flow | Yes |
| Calculated-ratings-only is explicitly requested and the process-flow REST projection omits `IncludeTalentReviewCalibFlag` | Continue with server validation | resolve_active_process_flow | The flow is active and effective, live template Describe marks the payload field writable, and every calculated-only section and role-action reset is included | Preserve the explicit request; do not infer the hidden flag as `N`. Execute only after the normal preview and approval gate. Treat a definite Fusion validation rejection as authoritative and reconcile any ambiguous response before another effect. | No |
| A new template definition or FSM package is created | Error | resolve_performance_role | No template-role record is present | Add at least one valid template-role record before validation or import | Yes |
| Two or more section weights or overall-calculation memberships change together | Route to validated FSM archive | read_template_by_id | Independent REST PATCH requests expose an intermediate section-weight total that Fusion rejects, or can commit only part of the intended calculation graph | Read every affected section and preserved sibling, materialize the complete final section set with included weights totaling 100 and excluded sections explicitly outside the calculation, validate one FSM archive, import once under the normal approval gate, wait for terminal completion, and verify the full saved graph | Yes |
| A manager, worker, or participant role is selected | Error | resolve_performance_role | The role is not effective or is incompatible with the configured process flow and role set | Resolve the role through its documented lookup, then correct the incompatible combination | Yes |
| A role absent from an existing template must also participate in one or more sections | Route to validated FSM archive | resolve_template_role_action_context | The REST template-role and role-action child creates would split a required atomic graph, and the role action cannot bind until Fusion generates `TmplRoleId` | Obtain the exact section choice before any write. Materialize the role and role-action rows in one validated FSM graph, preserve required sibling rows, import once under the normal approval gate, and verify terminal saved state. Do not probe with an isolated role POST. | Yes |
| An existing template role and its last section action are removed | Route to guarded atomic REST batch | resolve_active_process_flow | Separate DELETE commits form a validation cycle; an FSM import that omits rows is merge-only; root settings or period questionnaires still reference the role; or the assigned process flow still requires participant selection or feedback | Read the template and inventory every section action, period questionnaire, root role reference, and current process-flow task. Require an explicit compatible replacement-flow choice when needed; never guess or clear a period-required flow. Apply and verify prerequisite changes, refresh both exact child ETags, execute only the two-part `atomic_role_delete`, and verify both absences plus preserved siblings. Never use wildcard concurrency or claim omission deleted a row. | Yes |
| A template section is configured | Error | resolve_template_section | The section doesn't resolve to an effective Section Definition, or supplied values attempt to replace inherited attributes outside documented overrides | Select an effective Section Definition and apply only valid dependent overrides | Yes |
| Calculated ratings or section calculations are configured | Error | read_template_by_id | Rating, rounding, mapping, section-rating, calculated-only, or manual-rating values are inconsistent with parent settings | Correct the dependent rating configuration and remove stale values | Yes |
| Any documented dependent-field rule applies | Error | | The normalized payload retains a contradictory dependent value, or a request asks to bypass the rule. | Apply the documented reset and re-evaluate all applicable relationships. If any invariant remains unsatisfied, stop before preview, approval, import, or mutation; no request or approval can waive it. | Yes, only by making the payload compliant |
| A section, item, or role action is configured | Error | resolve_template_role_action_context | A template section has no role action, a role action references a user role absent from template roles, or its FSM `UserRoleTypeCode` is not `WORKER`, `MANAGER`, or `PARTICIPANT`; REST linkage must use the owning template's `TmplRoleId` | Add a role action for every section and correct its template-role linkage and role type before validation; do not send FSM role headings in REST | Yes |
| A period or period child is configured | Error | read_template_by_id | Dates, duplicate document types/questionnaires, due dates, availability/calibration, or Anytime restrictions are violated | Correct period fields and child rows before retrying validation | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_template_rest_metadata | Any REST request | Writable fields, accessor path, and supported operation | ora_reference_lookups.md |
| read_template_by_id | Existing-template operation | Lifecycle flags, object version, and child state | ora_reference_lookups.md |
| resolve_active_document_type | A document type is supplied | Active document type identity and name | ora_reference_lookups.md |
| resolve_active_process_flow | A process flow or step is supplied | Effective process flow identity, task names, and step | ora_reference_lookups.md |
| resolve_performance_role | A role or role action is supplied | Effective role type, name, and dates | ora_reference_lookups.md |
| resolve_template_section | A section or role action section is supplied | Effective section identity, name, description, dates, and type | ora_reference_lookups.md |
| resolve_effective_rating_model | Rating model or revision model values are supplied | Effective rating model identity and code | ora_reference_lookups.md |
| resolve_review_period | A period is supplied | Review period identity, name, and dates | ora_reference_lookups.md |
| resolve_questionnaire | A period questionnaire is supplied | Active latest questionnaire code, name, and version | ora_reference_lookups.md |
| resolve_template_role_action_context | A template section or role action is supplied | Parent lifecycle state, section identity, and effective role identity | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.ENFORCE_DEPENDENT_FIELD_INVARIANTS | decision | 60 | design_enforcement | compliant->PT.ENFORCE_REST_DESIGN;blocked->RETURN_ISSUES | PT.APPLY_PAYLOAD_DEFAULTS | stop | Every applicable dependent-field rule is normalized and compliant |
| PT.ENFORCE_REST_DESIGN | decision | 70 | design_enforcement | compliant->PT.EXECUTION_APPROVAL_GATE;blocked->RETURN_ISSUES | PT.ENFORCE_DEPENDENT_FIELD_INVARIANTS | stop | Create, update, delete, or child operation; enforce only lifecycle locks applicable to the selected operation and fields |
