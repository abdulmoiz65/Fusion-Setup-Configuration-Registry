# Maintenance Cloud Service Mapping Design Enforcement

## Scope

This file owns mandatory design gates for Service Mapping source recommendations for Subscriptions to Maintenance Cloud. It enforces source authority, target-interface boundaries, coverage context, publication-state clarity, and handoff discipline.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 10 | Confirm preventive-maintenance scope | Restrict analysis to Subscription coverage products and covered levels participating in the preventive-maintenance flow |
| 20 | Confirm Service Mapping authority | Use current Service Mapping evidence or supported lookups for source entities and aliases |
| 22 | Confirm describe-first source discovery | If the local source XML lacks the requested source value, use the permitted read-only describe path for the relevant object before suggesting any new alias |
| 25 | Confirm direct alias handoff | Return source aliases as direct Groovy references for the Algorithms workflow; do not recommend blanket conversion helpers |
| 30 | Confirm target interface boundary | Validate target needs against MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT without using target columns as source aliases |
| 40 | Confirm source-to-target pairing | Pair each source with one target business meaning, data type, length, and prerequisite state |
| 50 | Confirm publication boundary | Separate local recommendations from published or deployed Service Mapping state |
| 60 | Confirm algorithm boundary | Return source decisions and prerequisites to Algorithms without drafting Groovy, merging `ActionExpression` content, or running downstream processes |
| 70 | Confirm handoff boundary | When Groovy application is discussed, defer to the primary rule to present Groovy for approval before XML generation, append to executable Groovy, and ignore or remove blank, sample, placeholder, or comment-only content |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Service Mapping source analysis is requested | Error | resolve_maintenance_service_mapping_contract | Current mapping artifact, read route, source entity list, or publication evidence is missing | Obtain current Service Mapping evidence before recommending aliases | Yes, by supplying the supported artifact or resolver contract |
| Proposal covers preventive maintenance for subscriptions | Error | verify_subscription_maintenance_context | Coverage product, covered level, maintenance program template, or active subscription context is not verified | Resolve the Subscription preventive-maintenance context before mapping source aliases | Yes, by supplying or resolving missing context |
| A target Maintenance field is named | Error | resolve_maintenance_target_interface_fields | Field is not documented in MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT, or accepted runtime values are unresolved | Keep target mapping inside documented interface fields and mark accepted-value gaps explicitly | Yes, by selecting a documented target or providing release-matched accepted values |
| Requested source value is absent from local Service Mapping source XML | Error | verify_maintenance_source_resolution | Alias is suggested without exact source object, exact source attribute, data type, and source evidence from an allowed describe result or explicit no-describe implementer assumption | Use product describe for `Products` values and covered-level describe for `CoveredAssets` values; return `needs_describe` or `needs_decision` if exact evidence is unavailable | Yes, by completing describe-backed source resolution or recording an explicit no-describe assumption |
| A source alias is recommended | Error | verify_maintenance_source_resolution | Source object, source attribute, alias, type, access, publication state, or evidence source is missing | Return candidate as needs_describe, needs_decision, or prerequisite_pending instead of analyzed success | Yes, by completing source-resolution evidence |
| Source handoff recommends generic value conversion | Error | verify_maintenance_mapping_handoff | Handoff tells Algorithms to wrap every source alias in `toString()` or a generic conversion helper | Return direct source aliases such as `CoveredAssets.<attributeName>` or `Products.<attributeName>` and preserve source type information | Yes, by correcting the handoff |
| A target table column is used as a source | Error | verify_maintenance_source_resolution | Result uses target column name as proof of subscription source availability | Require a Service Mapping source alias and type for the business value | Yes, by selecting a real source candidate |
| Publication readiness is claimed | Error | verify_maintenance_mapping_publication | Published state is not environment-matched or source aliases are only local recommendations | Report publication prerequisite separately from mapping analysis | Yes, by supplying publication evidence |
| Handoff to Algorithms is requested | Error | verify_maintenance_mapping_handoff | Handoff omits source-to-target pairs, type checks, publication prerequisites, or unresolved decisions | Return a structured handoff with explicit unresolved items | Yes, by completing the handoff fields |
| Algorithm Groovy merge or XML generation behavior is requested | Error | verify_maintenance_mapping_handoff | Companion tries to approve Groovy, generate XML, overwrite, append, or clean the algorithm `ActionExpression` itself | Return to the primary Algorithms workflow; only note that Groovy must be approved before XML generation and that comments, placeholders, sample text, and blank content are not executable source decisions | Yes, by handing off instead of editing algorithm content |
| Live update, publish, import, scheduled process, or transfer validation is requested | Error | resolve_maintenance_service_mapping_contract | Supported execution contract and approval are missing | Refuse live action and identify the missing workflow contract | No live action until a separate supported workflow exists |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_maintenance_service_mapping_contract | Every Service Mapping checkpoint | mapping_context_id, source_entities, source_aliases, service_access, publication_state | ora_reference_lookups.md |
| verify_subscription_maintenance_context | Analysis or handoff depends on preventive-maintenance context | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id | ora_reference_lookups.md |
| resolve_maintenance_target_interface_fields | A Maintenance target field is mapped or reviewed | target_table, target_column, target_type, target_length, target_meaning | ora_reference_lookups.md |
| verify_maintenance_source_resolution | A source candidate or alias is evaluated | source_object, source_attribute, source_alias, source_type, source_status | ora_reference_lookups.md |
| verify_maintenance_mapping_handoff | Handoff to Algorithms or project workflow is requested | handoff_status, selected_sources, source_target_pairs, prerequisites, unresolved_items | ora_reference_lookups.md |
| verify_maintenance_mapping_publication | Published state or transfer readiness is claimed | publication_status, deployed_aliases, deployment_evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTSM.ENFORCE_DESIGN | step | 40 | design_enforcement | passed->MNTSM.CHECK_EXECUTION_CONTRACT;blocked->MNTSM.REPORT_ISSUES | MNTSM.CHECK_DEPENDENCIES | stop | Enforce source authority, preventive-maintenance scope, target interface boundary, source-to-target pairing, publication boundary, and handoff boundary. |
