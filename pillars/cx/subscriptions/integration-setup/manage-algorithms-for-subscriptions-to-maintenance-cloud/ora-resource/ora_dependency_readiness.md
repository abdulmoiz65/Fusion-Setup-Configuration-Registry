# Maintenance Cloud Algorithm Dependency Readiness

## Scope

This resource evaluates setup prerequisites before a Maintenance Cloud algorithm proposal, approved local artifact, or transfer validation is treated as ready. It does not run scheduled processes, import Maintenance data, or change Fusion configuration.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 10 | Algorithm contract | Resolve the supported Manage Algorithms artifact, mutation route, verification route, and approval boundary for this setup task |
| 20 | Service Mapping sources | Confirm source aliases, data types, access, and publication prerequisites before using them in algorithm logic |
| 30 | Subscription maintenance context | Verify the subscription coverage product, covered levels, and maintenance program template association |
| 40 | Target interface contract | Complete field-level mapping to MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT and resolve import-specific codes or keys |
| 50 | Approval | Bind approval to the exact algorithm proposal, current source fingerprints, and target environment before any artifact or live change |
| 60 | Downstream transfer evidence | For validation after activation, correlate the three documented scheduled processes and target Maintenance result evidence |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| algorithm_contract | Supported Manage Algorithms contract | Yes | Every checkpoint | Lookup | Pending implementation contract | resolve_maintenance_algorithm_contract | The supplied docs do not describe how this algorithm is exported, updated, imported, or verified | Provide the supported algorithm artifact and mutation/verification route for this task | algorithm_contract_status, algorithm_artifact_id, mutation_route, verification_route |
| service_mapping_handoff | Service Mapping source handoff | Yes | Proposal or approved change maps subscription data into Maintenance Cloud fields | Lookup | Service Mapping task result or supplied handoff | verify_maintenance_service_mapping_handoff | Algorithms require confirmed source aliases and data types; target table names do not identify subscription sources | Provide source aliases, source object names, types, and publication prerequisites | confirmed_sources, source_types, publication_prerequisites |
| subscription_coverage_context | Active subscription coverage and maintenance template association | Yes | Proposal or transfer validation depends on preventive maintenance | Lookup | Subscription and coverage evidence | verify_subscription_maintenance_context | The readiness feature depends on a maintenance program template associated to the coverage product and an active subscription before transfer | Provide subscription id or number, coverage product, standard coverage, covered levels, and template evidence | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id |
| target_interface_mapping | Maintenance target interface field mapping | Yes | Proposal maps output fields | Lookup | Oracle target table docs plus implementation mapping | resolve_maintenance_interface_import_contract | Program header and work requirement rows must map to documented interface fields and retain their relationship | Provide field-level source-to-target mapping and any import-specific action or program type code values | target_program_fields, target_requirement_fields, accepted_action_codes, program_type_code |
| explicit_approval | Exact proposal approval | Conditional | approved_change or artifact_result | Lookup | Approval record | verify_maintenance_approval_evidence | Local artifact preparation or live change must be approved for the exact current proposal | Approve the complete proposal after validation and design gates pass | approval_status, approval_reference, approved_scope |
| scheduled_process_results | Preventive maintenance transfer process evidence | Conditional | transfer_validation | Lookup | ESS request IDs, process logs, target result evidence | verify_maintenance_target_import_state | The feature requires three scheduled processes after activation before instantiated Maintenance program evidence exists | Provide request IDs or equivalent result artifacts for all three processes | process_statuses, interface_statuses, instantiated_program_id, validation_errors |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence is present, matches the resolver contract, and has no unresolved publication or approval blocker | Lookup only when the resolver contract is documented |
| Lookup | User supplied an alternate key or partial evidence that a documented read-only lookup can resolve | Yes, read-only lookup only |
| Blocked | Required value, supported endpoint, import contract, approval, or process evidence is missing or ambiguous | No create or live process; ask for the missing contract or evidence |
| Draft Only | Field mapping can be documented from the supplied sources but runtime mutation or import remains unsupported | No live execution |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTALG.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | satisfied->MNTALG.ENFORCE_DESIGN;blocked->MNTALG.REPORT_ISSUES;draft_only->MNTALG.REPORT_ISSUES | MNTALG.RESOLVE_LOOKUPS | stop | Evaluate algorithm contract, service mapping handoff, subscription coverage context, target interface mapping, approval, and downstream transfer evidence for the current rule_phase. |
