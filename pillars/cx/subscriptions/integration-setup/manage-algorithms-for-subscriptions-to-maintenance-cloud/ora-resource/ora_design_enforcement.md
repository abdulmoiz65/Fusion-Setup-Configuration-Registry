# Maintenance Cloud Algorithm Design Enforcement

## Scope

This file owns mandatory design gates for algorithm proposals that populate or validate Maintenance Cloud preventive-maintenance integration data. It uses the supplied Oracle sources for business flow and target interface-table boundaries, and it leaves missing execution contracts as blockers.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 10 | Confirm preventive-maintenance scope | Restrict this task to subscription coverage products and covered levels that participate in the preventive-maintenance feature |
| 20 | Confirm source authority | Use confirmed Service Mapping source aliases and types; never derive source aliases from Maintenance interface table names |
| 25 | Confirm direct source value usage | Use Service Mapping aliases directly in Groovy unless the requirement or a documented runtime contract requires explicit formatting, concatenation, or conversion |
| 30 | Confirm target boundary | Use MNT_PROGRAMS_INT for program header data and MNT_WORK_REQUIREMENTS_INT for work requirement data |
| 40 | Confirm parent-child consistency | Preserve the relationship between program header and work requirement rows through documented identifiers |
| 45 | Confirm Groovy-first approval gate | Present the exact Groovy draft for approval before generating or updating any `Algorithm_BO.xml` artifact |
| 50 | Confirm existing Groovy handling | Append to existing executable `ActionExpression` Groovy; remove or ignore blank, placeholder, sample, or comment-only content |
| 60 | Confirm process boundary | Treat scheduled process submission and result polling as downstream validation, not as algorithm authoring |
| 70 | Confirm approval boundary | Require exact approval before artifact creation or any live mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Proposal covers preventive maintenance for subscriptions | Error | verify_subscription_maintenance_context | Subscription is not active, coverage product is absent, covered levels are absent, or maintenance program template association is not verified | Resolve subscription coverage context before algorithm proposal | Yes, by supplying or resolving the missing context |
| Proposal maps source data into Maintenance Cloud | Error | verify_maintenance_service_mapping_handoff | Source alias, type, service access, or publication prerequisite is missing | Complete the Service Mapping handoff before drafting algorithm logic | Yes, by completing source-resolution |
| Proposal wraps all source values in generic conversion logic | Error | verify_maintenance_service_mapping_handoff | Draft uses blanket `toString()` conversion or a generic conversion helper for source aliases that should be passed directly | Use direct aliases such as `CoveredAssets.<attributeName>` or `Products.<attributeName>`; convert only where the requirement or documented runtime contract requires it | Yes, by removing unnecessary conversion wrappers |
| Proposal uses target table columns as source facts | Error | resolve_maintenance_interface_import_contract | Target field names are used to infer subscription source aliases or business meanings | Separate source alias decisions from target interface field choices | Yes, by providing field-level source-to-target mapping |
| Proposal targets Maintenance data | Error | resolve_maintenance_interface_import_contract | Target table is not MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT, or proposal implies direct base-table update | Stay inside documented interface-table boundary and supported import contract | No direct table update; fix by selecting documented interface fields |
| Work requirements are mapped | Error | resolve_maintenance_interface_import_contract | Work requirement rows cannot be linked to the program header or subscription covered level | Include documented header, program, batch, or covered-level linkage in the mapping | Yes, by adding linkage fields or source decisions |
| Algorithm XML artifact is generated before Groovy approval | Error | verify_maintenance_approval_evidence | Updated `Algorithm_BO.xml` is created in the same step as first-time Groovy drafting, or approval is not tied to the exact Groovy body/proposal artifact | Return the draft Groovy for approval first; generate XML only after a later explicit approval of that exact draft | Yes, by separating proposal and artifact creation steps |
| Approved Groovy is applied to an existing action | Error | resolve_maintenance_algorithm_contract | Existing executable Groovy would be overwritten, or comment-only/sample text would be preserved as runtime logic | Append approved Groovy after executable existing logic; ignore or remove comments, placeholders, sample text, and blank content | Yes, by merging the `ActionExpression` correctly before artifact creation |
| Enumerated target fields are populated | Error | resolve_maintenance_interface_import_contract | Requirement type, work requirement status, action code, program type, suppress merge, or work order option value is not documented or approved | Resolve exact accepted values for the target release before proposal | Yes, by providing release-matched accepted values |
| Process validation is requested | Error | verify_maintenance_target_import_state | Any of Send Maintenance Program and Covered Assets to Oracle Maintenance, Import Maintenance Programs, or Retrieve Instantiated Maintenance Program evidence is missing | Validate all three scheduled processes for the same subscription and target context | Yes, by supplying correlated request IDs or result artifacts |
| Live mutation, import, process submission, or verification is requested | Error | resolve_maintenance_algorithm_contract | Supported execution contract or exact approval is missing | Keep the result as draft guidance and report missing contract | No live action until contract and approval are supplied |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_subscription_maintenance_context | Proposal or transfer validation depends on preventive-maintenance subscription behavior | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id | ora_reference_lookups.md |
| verify_maintenance_service_mapping_handoff | Proposal maps any subscription source value | confirmed_sources, source_types, publication_prerequisites | ora_reference_lookups.md |
| resolve_maintenance_interface_import_contract | Proposal names Maintenance Cloud targets or import behavior | target_program_fields, target_requirement_fields, accepted_action_codes, program_type_code | ora_reference_lookups.md |
| verify_maintenance_target_import_state | Transfer validation after active subscription | process_statuses, interface_statuses, instantiated_program_id, validation_errors | ora_reference_lookups.md |
| resolve_maintenance_algorithm_contract | Any artifact creation, live change, import, or verification request | algorithm_contract_status, algorithm_artifact_id, mutation_route, verification_route | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTALG.ENFORCE_DESIGN | step | 40 | design_enforcement | passed->MNTALG.CHECK_EXECUTION_CONTRACT;blocked->MNTALG.REPORT_ISSUES | MNTALG.CHECK_DEPENDENCIES | stop | Enforce preventive-maintenance scope, source authority, target interface boundary, row linkage, process boundary, and approval boundary. |
