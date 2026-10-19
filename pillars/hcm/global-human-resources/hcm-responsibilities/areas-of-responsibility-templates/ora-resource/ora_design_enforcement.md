# Areas of Responsibility Templates Design Enforcement

## Purpose

Defines the mandatory template, criteria, scope, and representative design
gates that Codex applies while authoring source from the current live Data
Loader template. It does not perform lookups, apply defaults, or create
missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm template | Require a supported object shape and one exact template or create-availability result |
| 2 | Resolve criteria and scope | Resolve each supplied attribute and its value exactly, including all object-backed scope values and hierarchy fields |
| 3 | Resolve direct assignment | Require one eligible worker-assignment pair and ResponsibilityName |
| 4 | Confirm mutation control | Require current source, preview, approval, and the declared Data Loader route |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| REGISTERED_OBJECT | Every request | Blocking |  | AORTemplate does not support the requested operation, source shape, field, or child row | Use only the registered supported operation and shape | No |
| TEMPLATE | Read, edit, delete, or create uniqueness check | Blocking | find_areas_of_responsibility_templates | A create TemplateCode exists, or a read/update/delete name has multiple exact matches without a TemplateCode or TemplateId | For create, supply an available TemplateCode. For an ambiguous name, supply a code or ID | Lookup fix |
| CRITERIA_SCOPE | A lookup-backed criterion or populated scope value is supplied | Blocking | resolve_aor_scope_value | Its attribute, value, target source field, type, cardinality, or multi-value encoding is guessed, unresolved, or unsupported | Resolve one compatible stored value, map it to its exact source field, and declare the encoding | Lookup fix |
| JOB_CRITERIA | Job criteria is supplied | Blocking | resolve_aor_job | The Job is missing, inactive, ineffective, or ambiguous | Resolve one active effective Job | Lookup fix |
| LOCATION_CRITERIA | Location criteria is supplied | Blocking | resolve_aor_location | The Location is missing, inactive, ineffective, or ambiguous | Resolve one active effective Location | Lookup fix |
| SCOPE_VALUE | A populated object-backed scope is supplied | Blocking | resolve_aor_scope_value | The scope value lacks an exact effective resolver result or cannot be mapped to its registered source columns | Resolve one compatible value through the AOR scope-value resolver matrix | Lookup fix |
| STATIC_BLANK_SCOPE | A blank static scope is supplied | Blocking |  | DynamicValueFlag is not Y and no resolved static business value is supplied | Stop before source generation: static blank scope serialization is temporarily unsupported pending an attribute-specific loader-proven contract | Source rebuild |
| HIERARCHY_EXCLUSIVITY | Any hierarchy scope is supplied | Blocking |  | More than one hierarchy type is present for one template | Keep only one hierarchy type in the source workbook | Source rebuild |
| HIERARCHY_PATH | A Department, Organization, Position, or Supervisor hierarchy scope is supplied | Blocking | Resolver specific to that hierarchy type | The hierarchy has no complete active loader-proven resolver contract | Stop before source generation; do not infer tree, node, or descendant mappings | No |
| DIRECT_ASSIGNMENT | A directly assigned representative is supplied | Blocking | resolve_aor_worker_assignment | The worker-assignment pair or ResponsibilityName is missing, ineligible, or ambiguous | Resolve one eligible worker-assignment pair and supply ResponsibilityName | Lookup fix |
| SOURCE | A mutation is prepared | Blocking |  | XLSX source, key provenance, validation result, or immutable preview is missing or stale | Rebuild and validate the smallest current XLSX source | Source rebuild |
| PREVIEW_CONTENT | A mutation preview is prepared | Blocking |  | The preview omits the environment alias, operation, exact target, explicit changes, preserved rows, per-row Scope and Criteria Mapping, XLSX source fingerprint, immutable Data Loader preview, or post-load reconciliation plan | Rebuild the complete immutable preview | Re-preview |
| SENSITIVE_OUTPUT | A preview or user-facing result is produced | Blocking |  | Credentials, runtime links, raw payloads, or transient IDs are exposed | Regenerate the output with sensitive and transient values removed | Re-preview |
| APPROVAL | A mutation is ready for submission | Blocking |  | Approval is absent, stale, bound to different target, source, metadata, preview, or reconciliation evidence, or any displayed or source value changed after approval | Obtain approval for the exact immutable preview | Re-preview |
| ROUTE | Create, edit, or delete | Blocking |  | Fusion REST, FSM CSV, a direct API batch, or an unapproved retry is proposed | Use only the declared Core Data Loader route | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_areas_of_responsibility_templates | Target, full read, or create-uniqueness evaluation | Exact identity, effective context, current parent and child values, and cardinality | ora_reference_lookups.md |
| resolve_aor_common_lookup | A lookup-backed criterion, scope, Assignment Category, or System Person Type is supplied | One exact enabled/effective stored lookup value; Lookup Tag does not constrain sibling AOR attributes unless the Data Loader contract explicitly says so | ora_reference_lookups.md |
| resolve_aor_system_person_type | A System Person Type criterion is supplied | One exact enabled/effective `SYSTEM_PERSON_TYPE` LookupCode mapped to `SystemPersonType` | ora_reference_lookups.md |
| resolve_aor_job_function | A Job Function criterion is supplied | One enabled exact LookupCode mapped to `JobFunctionCode` | ora_reference_lookups.md |
| resolve_aor_country | A Country scope or criterion is supplied | One nonobsolete exact TerritoryCode mapped to `Country` | ora_reference_lookups.md |
| resolve_aor_job | Job criteria is supplied | One active Job effective on the template StartDate | ora_reference_lookups.md |
| resolve_aor_location | Location criteria is supplied | One active Location effective on the template StartDate | ora_reference_lookups.md |
| resolve_aor_scope_value | An object-backed TemplateScope value is supplied | Exact stored keys and registered target columns for the selected AttributeName | ora_reference_lookups.md |
| resolve_aor_department_hierarchy | A Department Hierarchy scope is supplied | Active version, exact top-node membership, and descendant traversal evidence | ora_reference_lookups.md |
| resolve_aor_worker_assignment | A directly assigned representative is supplied | One eligible PersonId and AssignmentId pair | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AORT.ENFORCE | decision | 6 | design_enforcement | passed->AORT.ROUTE;not_required->AORT.ROUTE;blocked->AORT.ERROR | AORT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
