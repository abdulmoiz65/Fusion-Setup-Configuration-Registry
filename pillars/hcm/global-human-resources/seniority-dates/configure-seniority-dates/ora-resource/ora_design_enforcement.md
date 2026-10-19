# Configure Seniority Dates Design Enforcement

## Purpose

Defines the mandatory Seniority Date rule, compatibility, tuple, selector,
source-scope, and mutation-control design gates. It does not perform lookups,
apply defaults, or infer technical configuration.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm object and identity | Require a supported operation and one exact target or create-availability result |
| 2 | Confirm reference validity | Resolve every supplied lookup-backed value exactly after complete intake; do not treat display text as a cross-field schema |
| 3 | Confirm technical contract | Require current LOV mappings, one proven tuple, and exact operation-template fields |
| 4 | Validate source scope | Keep only the explicit delta and supported selector mappings and encodings |
| 5 | Confirm mutation control | Require current source, preview, approval, and the declared Data Loader route |
| 6 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| REGISTERED_OBJECT | Every request | Blocking |  | employmentSeniorityDateConfigurations does not support the requested operation, source shape, field, or row | Use only the registered supported operation and shape | No |
| RULE_IDENTITY | Read, edit, delete, or create uniqueness check | Blocking | find_configured_seniority_date_rules | The target or seniority-date code result is missing, ambiguous, or duplicated for create | Supply one exact target or unique code | Lookup fix |
| REFERENCE_CARDINALITY | A rule, attribute, level, flag, formula, worker, or scope reference is supplied | Blocking |  | Any supplied resolver-backed value has zero or multiple compatible results | Resolve every supplied value independently to exactly one compatible stored value | Lookup fix |
| LOOKUP_REFERENCE | A complete create intake supplies a rule, attribute, level, flag, formula, worker, or scope reference | Blocking |  | A supplied value has zero or multiple current exact matches | Correct the independently supplied reference | Lookup fix |
| DESCRIBE_CONTRACT | A LOV-backed field is supplied | Blocking |  | The value lacks the current describe-declared resource, filter, mapping, display field, or delimiter evidence | Re-resolve the field through its declared lookup contract | Lookup fix |
| TECHNICAL_TUPLE | Create derives technical configuration | Blocking | derive_seniority_configuration_tuple | A field required by the current operation-specific create template lacks one supported value, or a populated field conflicts with the current schema, LOV, or default evidence | Derive only the template-required fields; omit absent fields and preserve optional blanks | Lookup fix |
| TUPLE_PROVENANCE | A technical tuple is used | Blocking | derive_seniority_configuration_tuple | A tuple value is not in the approved triggering-field default map, comes from an unreviewed payload, another triggering field, semantic inference, or unvalidated same-release evidence | Rebuild the tuple from the approved map and current template/schema evidence | Lookup fix |
| SELECTOR_MAPPING | A display selector is supplied | Blocking |  | A REST display field is written to XLSX when unsupported, or its resolved ID or code target is missing | Write only the registered Data Loader ID or code target | Source rebuild |
| OPERATION_CONTRACT | A mutation source is prepared | Blocking |  | RestAction, keys, or source columns differ from the current operation-specific template | Regenerate the operation-specific source | Source rebuild |
| SCOPE | A mutation source is prepared | Blocking |  | XLSX includes unchanged or unrelated rows, unsupported fields, or an unsupported multi-value encoding | Retain only the explicit delta and declared comma encoding | Source rebuild |
| EDIT_PRESERVATION | Edit | Blocking | find_configured_seniority_date_rules | A field outside the explicit delta changes, or a populated or immutable rule requires versioning or disablement instead | Preserve the current row and use the supported lifecycle operation | Input fix |
| SOURCE | A mutation is prepared | Blocking |  | XLSX source, key provenance, validation result, or immutable preview is missing or stale | Rebuild and validate the smallest current XLSX source | Source rebuild |
| PREVIEW_CONTENT | A mutation preview is prepared | Blocking |  | The preview omits the environment alias, operation, exact rule, requested delta, preserved values, resolved reference labels, XLSX source fingerprint, immutable Data Loader preview, or post-load reconciliation plan | Rebuild the complete immutable preview | Re-preview |
| SENSITIVE_OUTPUT | A preview or user-facing result is produced | Blocking |  | Credentials, runtime links, raw payloads, or transient IDs are exposed | Regenerate the output with sensitive and transient values removed | Re-preview |
| APPROVAL | A mutation is ready for submission | Blocking |  | Approval is absent, stale, bound to different target, source, metadata, preview, or reconciliation evidence, or any displayed or source value changed after approval | Obtain approval for the exact immutable preview | Re-preview |
| ROUTE | Create, edit, or delete | Blocking |  | Fusion REST, FSM import, CSV omission, or an unapproved retry is proposed | Use only the declared Core Data Loader route | No |
| FRESH_STATE | Create, edit, delete, preview, approval revalidation, or verification | Blocking | read_current_seniority_rule | Any target, duplicate count, reference, package state, or current row is not freshly read for the current stage | Re-read current state through the declared route | Lookup fix |
| CREATE_INTAKE | Create | Blocking |  | Rule, attribute, or level is missing | Collect the complete create intake once; default omitted Active to Y, Cumulative to N, Display in Guided Flows to N, Allow Edit to Y, and scope to `No restriction` | Input fix |
| AUTHORITATIVE_COMPATIBILITY | Complete create intake with a current metadata contract that explicitly binds the combination | Blocking only on proven conflict | validate_authoritative_seniority_compatibility | The authoritative source explicitly rejects the exact independently resolved Attribute, Level, Cumulative, or override/time-basis value | Identify the source and correct the conflicting input; do not seek approval to override a proven conflict | Input fix |
| SCOPE_CHOICE | Create | Blocking | validate_scope_no_restriction | Supplied scope values are incompatible | Resolve each supplied scope value; when scope is omitted, apply `No restriction` | Lookup fix |
| UPDATE_DELTA | Update | Blocking | read_current_seniority_rule | The target is not exact, no delta is supplied, or a field outside the requested delta changes | Copy the fresh row, preserve omitted values, and rebuild the smallest update | Source rebuild |
| RECORD_PRESENT | Update or delete | Blocking | evaluate_seniority_rule_usage | The custom evaluation result is missing; or existing seniority records use the rule and an update changes anything other than Active, Allow Edit, or Display in UI; or deletion is requested | Invoke `performEmploymentOperations` with `configureSeniorityDatesOperation` and `evaluateRuleUsage`; map `ruleUsed` to the internal RecordPresent control only. For deletion, proceed to a delete preview only when no existing seniority records use the rule; otherwise return the blocked-delete error. | Input fix |
| DELETE_CAPABILITY | Delete | Blocking | confirm_seniority_deletion_capability | The current delete template lacks mandatory `RestAction=DELETE`, accepted primary key `SeniorityDateSetupId`, or one current eligible target | Rebuild the delete source from the current registered template with `RestAction=DELETE` and the fresh resolved `SeniorityDateSetupId`. | Source rebuild |
| FINGERPRINT | Preview, approval, execution, or verification | Blocking | fingerprint_seniority_business_state | The fingerprint is missing, stale, or differs from the approved preview | Generate a new preview and approval | Re-preview |
| REVALIDATION | Immediately before execution | Blocking |  | Target, references, duplicate cardinality, source, package, or fingerprint changed | Invalidate approval and regenerate the preview | Re-preview |
| VERIFICATION | After execution | Blocking | read_current_seniority_rule | Fresh read cannot prove approved create/update values and preserved update fields, or delete absence across required reads | Return failed or uncertain; reconcile without replaying the mutation | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_configured_seniority_date_rules | Target, create-uniqueness, tuple-state, or edit-preservation evaluation | Exact code result, current rule state, technical values, and cardinality | ora_reference_lookups.md |
| resolve_seniority_rule | Complete create intake or a non-create selector is supplied | One current exact rule code; Meaning is display-only | ora_reference_lookups.md |
| resolve_seniority_attribute | Complete create intake or a non-create attribute is supplied | One exact attribute code; Meaning is display-only | ora_reference_lookups.md |
| resolve_seniority_level | Complete create intake or a non-create level is supplied | One exact level code; Meaning is display-only | ora_reference_lookups.md |
| validate_authoritative_seniority_compatibility | Complete create intake and documented current metadata explicitly exposes a combination constraint | Identified authoritative source and its result; no display-text inference | ora_reference_lookups.md |
| derive_seniority_configuration_tuple | Create derives technical configuration or tuple provenance is checked | Minimal template-supported required fields, optional-field handling, and exact triggering-field provenance | ora_reference_lookups.md |
| validate_mutation_environment | A create, edit, or delete preflight runs | Safe environment alias and required current-state and Data Loader privilege result | ora_reference_lookups.md |
| validate_scope_no_restriction | Create supplies `No restriction` or omits all scope selectors | Defaulted or explicit choice and blank supported scope fields | ora_reference_lookups.md |
| read_current_seniority_rule | A mutation, preview, approval revalidation, or verification is required | Fresh current target state and canonical business-state fingerprint | ora_reference_lookups.md |
| evaluate_seniority_rule_usage | Update or delete target resolution, preview, revalidation, or verification | Fresh action result mapping ruleUsed to RecordPresent | ora_reference_lookups.md |
| confirm_seniority_deletion_capability | Delete planning is requested | Proven item-level deletion capability through the registered route | ora_reference_lookups.md |
| fingerprint_seniority_business_state | A preview, approval revalidation, or verification is required | Current canonical business-state fingerprint | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEN.ENFORCE | decision | 6 | design_enforcement | passed->SEN.ROUTE;not_required->SEN.ROUTE;blocked->SEN.ERROR | SEN.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
