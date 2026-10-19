# Performance Templates Dependency Readiness

Sources: Performance Templates lookup matrix and [REST resource and field guidance](../../performance-template-rest-source-contract.md). Verify UI-specific prerequisites for the target release and environment.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | REST describe metadata | Confirm the requested root or child accessor, operation, and writable shape. |
| 2 | Existing template state | For changes, read the template to determine in-use, document, period, role, section, and ESS lifecycle guards. |
| 3 | Referenced setup objects | Resolve every supplied document type, process flow, role, section, questionnaire, profile/content, rating model, rating level, review period, qualifier, and lookup code through its documented resolver. |
| 4 | Parent-child graph | Create, update, or delete children only through their owning REST accessor and parent context. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PT_REST_METADATA | Generated REST metadata | Yes | Always | Lookup | Fusion REST describe endpoint | inspect_template_rest_metadata | It defines the root/child accessors and writable versus read-only attributes | Inspect the contract before request validation | Writable fields and accessor path |
| PT_EXISTING_TEMPLATE | Existing template lifecycle state | Conditional | Update, delete, or child operation | Lookup | Fusion REST singleton endpoint | read_template_by_id | Lifecycle guards depend on in-use, document, period, role, section, and ESS state | Read the template by TemplateDefnId | Template state and child graph |
| PT_REFERENCE_OBJECTS | Referenced setup objects | Conditional | A request supplies a documented Performance Templates reference field | Lookup | Field-specific Fusion LOV and REST endpoints in ora_reference_lookups.md | resolve_template_references | Each supplied reference must match one valid value using the resolver that owns its field. An exported FSM CSV is contextual evidence only and cannot resolve a process flow. | Provide a valid, unambiguous value for every supplied reference field | Validated lookup code, name, dates, and resolved identity required by the target record |
| PT_PARENT_CONTEXT | Owning parent accessor | Yes | Any child operation | Verify | Parent REST view-link context | read_template_by_id | Child identifiers and context are supplied by their parent accessor, not by arbitrary payload fields | Use the documented child accessor below its resolved parent | Parent identity and allowed child operation |

## FSM CSV Record Graph and Omission Rules

Use this table when preparing an `HRA_MANAGE_PERFORMANCE_TEMPLATES` FSM
archive. A CSV member is included only when its row has a valid parent and its
business purpose applies. Never include an empty, orphaned, placeholder, or
speculative child CSV row merely because the exported archive contained that
member.

| CSV | Parent CSV | Business purpose | Include when | Must not exist when |
|---|---|---|---|---|
| `HRA_TEMPLATE` | none | Stores the template-level data, including its process flow and document type. | Every new or changed template archive; exactly one parent row is required for the template being configured. | Never omit it from an archive containing any template child row. |
| `HRA_PROCESS_STEP_ALERTS` | `HRA_TEMPLATE` | Stores notification lead days for process-flow tasks. | Alert days are explicitly configured for a task from the selected process flow. | No alert day is requested for that task, or the task is not in the selected process flow. |
| `HRA_TEMPLATE_ROLE` | `HRA_TEMPLATE` | Stores the roles used by the template. | Every template; include at least one selected template role. | A role is not selected for the template, or the row would duplicate an existing selected role. |
| `HRA_TEMPLATE_TRANSLATION` | `HRA_TEMPLATE` | Stores translated template values such as name and comments. | A translated template value is created or changed. | No translated template value is supplied for the locale. |
| `HRA_TEMPLATE_SECTION` | `HRA_TEMPLATE` | Stores the template sections, initially inheriting values from the selected section definition. | A section is selected for the template; include at least one section whenever the template has a template period. | No section is selected and no template period exists; never omit all section rows when a template period exists. |
| `ORA_HRA_TEMPLATE_ROLE_ACTION` | `HRA_TEMPLATE_SECTION` | Stores how a role can rate, comment on, and share a section. | Every included template section; include at least one valid role-action row for that section. | Its parent template section is absent; never omit all role actions for an included section. |
| `HRA_TEMPL_SEC_ITEMS` | `HRA_TEMPLATE_SECTION` | Stores defaulted content details for a section. | Content details are explicitly defaulted for the section. | The section has no defaulted content details. |
| `HRA_TMPL_PERIODS` | `HRA_TEMPLATE` | Stores individual template periods available for the template. | A distinct template period is requested. | No template period is requested. |
| `HRA_TMPL_PERIOD_DATES` | `HRA_TMPL_PERIODS` | Stores task due dates based on the selected process flow. | A due date is configured for a process-flow task in the parent period. | No due date is configured for that task, including an `ORA_ANYTIME` period. |
| `HRA_TMPL_PERIODS_TRANSLATION` | `HRA_TMPL_PERIODS` | Stores translated template-period values such as name. | A translated template-period value is created or changed. | No translated template-period value is supplied for the locale. |
| `ORA_HRA_TMPL_PERIOD_DOCUMENT_TYPE` | `HRA_TMPL_PERIODS` | Stores an interim document type associated with the template period. Its bare `Name`, `DateFrom`, and `DateTo` identify the referenced document type; the `HRA_TEMPLATE.*` and `HRA_TMPL_PERIODS.TmplDefn*` columns identify only the parent template. | The parent period is associated with an interim feedback template period and an interim document type is selected. | The parent period is not associated with an interim feedback template period, or the bare document-type dates do not exactly match the resolved document type. |
| `ORA_HRA_TMPL_PERIOD_QSTNR` | `HRA_TMPL_PERIODS` | Stores the questionnaire assigned to each template-period role. | The template includes a questionnaire section and a questionnaire is assigned to that role. | No questionnaire section exists, or no questionnaire is assigned to that role. |
| `ORA_TMPL_PERIOD_ELIGIBILITY_PROFILE` | `HRA_TMPL_PERIODS` | Stores the eligibility profile applicable to the template period. | An eligibility profile applies to the parent period. | No eligibility profile applies to the parent period. |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Metadata, required parent state, and referenced values are resolved | Yes |
| Lifecycle blocked | An in-use, document-locked, read-only, or ESS-pending state prevents the operation | No |
| Reference not found or ambiguous | A documented lookup returns zero or more than one matching value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.RESOLVE_REST_DEPENDENCIES | decision | 40 | resolve_dependency | ready->PT.APPLY_PAYLOAD_DEFAULTS;blocked->RETURN_ISSUES | PT.READ_EXISTING_TEMPLATE | stop | Create, update, delete, or child operation; require parent state only for an existing parent |
