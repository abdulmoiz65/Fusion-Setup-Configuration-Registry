# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted base field or section | Preserve current value/rows | Update/end-date | Yes | find_project_template |
| Omitted child collection | Preserve all current child rows | Update | Yes | resolve_template_sections |
| Root create value | Apply only listed documented defaults or a validated literal default proven by fresh operation-specific target create metadata. Generic response/describe default annotations cannot override the create contract. Do not invent status, identity, work type or dates | Create | No | |
| Root project schedule for dated tasks | Do not invent project dates or replace them with template availability. Validate supplied ordered bounds; dated tasks alone do not make an omitted project end date required | Supplied task dates | No | resolve_template_sections |
| Project plan type | No implicit association. If supplied, preserve the exact approved name/ID choice; if omitted, omit both plan-type attributes. Fusion validates a supported supplied name on POST. | Create/update | No | resolve_project_plan_type |
| ExternalTaskId | Nested template create: preserve supplied valid IDs. When omitted, use the supplied TaskNumber as ExternalTaskId to preserve the requested task number; otherwise generate FSCR- plus one UUID request namespace and the task sequence padded to at least three digits. Check uniqueness against all supplied/generated IDs and the 100-character limit; collisions block rather than renaming requested numbers. Save values once in the prepared payload and never regenerate during approval revalidation. Direct task creation retains its existing supplied/operation-required contract | Task create | No | resolve_template_sections |
| WorkType/WorkTypeId | Omit root work type when absent unless fresh operation-specific create metadata requires it. Task work type derives from project/parent task; preserve that derivation by omission | Create | No | |
| ProjectCurrencyCode | Preserve a supplied currency; otherwise omission is allowed by the POST required array unless fresh operation-specific target create evidence requires it. The docs do not identify a default source; do not promise a specific currency or derive one locally | Root create | No | verify_template_route |
| TaskOrganizationName or TaskOrganizationId | Nested template create: leave omitted fields absent for Fusion derivation; verify actual organization from task readback. Preserve explicit overrides and never send both alternatives. Direct task create retains explicit/evidenced parent-organization preparation or a proven operation-specific default | Nested and direct task create; never PATCH | No | |
| CrossChargeLaborFlag, CrossChargeNonLaborFlag, AllowCrossChargeFlag, AutoAssetCreateFlag | JSON false when omitted at root create; preserve supplied booleans | Root create only; never PATCH | No | |
| Task CrossChargeLaborFlag and CrossChargeNonLaborFlag | Summary task inherits the project; subtask inherits its identified parent task. Materialize the required JSON booleans from evidenced parent values; missing/ambiguous inheritance blocks unless explicit task booleans are supplied | Nested/direct task create only; never PATCH | No | |
| Task interest, cross-charge enablement, capitalization, schedule and work-type defaults | Preserve project/parent-task derivation by omission; never copy root fields into differently named task fields or flatten capitalization to false | Task create | No | |
| QuickEntries.MandatoryFlag | JSON false when omitted; preserve an explicit boolean | Nested/direct quick-entry create | No | |
| Other documented server defaults | Leave unrequested optional values omitted: PlanningProjectFlag and KPI notification/note flags default true; capital-event processing defaults N; team allocation defaults 100 and TrackTimeFlag false. Do not apply the four root false defaults to every boolean | Create | No | |
| AllowCapitalizedInterestFlag | Omit when not supplied so the project type derives it; do not default it to false | Root create | No | |
| AutoAssetLineAllocateMode | ALL_COSTS when omitted | Root create | No | |
| AssetAllocationMethodCode | Omit when not supplied so the project type derives it; validate supplied codes in input validation | Root create | No | |
| Copy scope | No implicit source sections; copy/duplicate/create-from is unsupported | Every request | No | resolve_template_sections |
| ProjectTemplateEndDate | Blank | Create | No |  |
| Setup-option display flag | No implicit enable/disable choice | Create/update | No | resolve_template_sections |
| Route | REST only after complete published and target-authorized coverage; otherwise stop | Every write | No | verify_template_route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTMPL.APPLY_DEFAULTS | step | 2 | apply_default | applied->PTMPL.FIND_TEMPLATE;failure->PTMPL.RETURN_ISSUES | PTMPL.VALIDATE_INPUT | stop | Valid input |

UI candidate selection and outline-display behavior do not establish REST defaults
or writable-field mappings. Use the reviewed operation contract; unproven mappings block.
