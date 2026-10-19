# Maintenance Cloud Service Mapping Dependency Readiness

## Scope

This resource evaluates prerequisites for source analysis, source-to-target mapping handoff, and publication readiness checks. It does not create, update, publish, import, or execute Service Mapping configuration.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 10 | Service Mapping contract | Resolve the supported Service Mapping artifact, read route, source fields, access evidence, and publication evidence for this setup task |
| 20 | Subscription maintenance context | Verify coverage product, covered levels, and maintenance program template association for the Subscription preventive-maintenance feature |
| 30 | Target interface field context | Validate selected MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT fields and target shape |
| 40 | Source resolution | Choose or preserve source candidates with alias, type, access, and publication state |
| 50 | Mapping handoff | Return source-to-target pairs, type compatibility, prerequisites, and unresolved decisions to the companion Algorithms task |
| 60 | Publication or transfer evidence | If requested, verify published mapping state or report it as unresolved before transfer validation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| service_mapping_contract | Supported Service Mapping artifact or lookup route | Yes | Every checkpoint | Lookup | Pending implementation contract | resolve_maintenance_service_mapping_contract | The supplied docs do not describe the Service Mapping export, update, or publish contract; permitted describe paths are source-discovery only | Provide the current Service Mapping artifact or supported read route for this task | mapping_context_id, source_entities, source_aliases, service_access, publication_state |
| subscription_maintenance_context | Subscription coverage and maintenance template context | Yes | Analysis or handoff depends on preventive maintenance | Lookup | Subscription and coverage evidence | verify_subscription_maintenance_context | The readiness feature depends on a maintenance program template associated to a coverage product and covered levels | Provide subscription id or number, coverage product, covered levels, and maintenance template evidence | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id |
| target_interface_fields | Maintenance target interface field context | Yes | A target Maintenance field is mapped or reviewed | Lookup | Oracle target table documentation plus implementation release | resolve_maintenance_target_interface_fields | Service Mapping analysis must know the target field shape without treating target fields as source aliases | Provide target table, target column, and intended business meaning | target_table, target_column, target_type, target_length, target_meaning |
| source_resolution | Source candidate and alias decision | Yes | Source analysis or handoff is requested | Lookup | Current Service Mapping evidence, allowed describe output, and user decisions | verify_maintenance_source_resolution | Algorithms need confirmed aliases and types, not just target table names | Provide selected source object and attribute from source XML or allowed describe, or explicitly approve a no-describe assumption | source_object, source_attribute, source_alias, source_type, source_status, evidence_source |
| mapping_handoff | Structured Service Mapping handoff | Conditional | Handoff to Algorithms or project workflow is requested | Lookup | Source-resolution records and target field context | verify_maintenance_mapping_handoff | The companion Algorithms task needs a clear source-to-target handoff and unresolved prerequisite list | Provide source records, target fields, type checks, and continuation context | handoff_status, selected_sources, source_target_pairs, prerequisites, unresolved_items |
| publication_evidence | Published mapping state | Conditional | User asks whether mapping is deployed, published, or ready for transfer | Lookup | Environment publication evidence | verify_maintenance_mapping_publication | Local recommendation or file evidence does not prove deployed Service Mapping state | Provide environment-matched publication evidence or accept prerequisite_pending | publication_status, deployed_aliases, deployment_evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence is present, matches the resolver contract, and has no unresolved publication or source-selection blocker | Lookup only when the resolver contract is documented |
| Lookup | User supplied alternate keys or partial evidence that a documented read-only resolver can complete | Yes, read-only lookup only |
| Needs Decision | Multiple source candidates or target interpretations remain viable | No create or publish; request implementer decision |
| Needs Describe | Source XML lacks the requested value and exact attribute evidence is missing | Yes, only the permitted read-only Subscription Product describe path for the relevant source object |
| Prerequisite Pending | Source is selected but exposure, access, or publication remains unresolved | No live change; complete Service Mapping prerequisite through supported workflow |
| Blocked | Required artifact, endpoint, source decision, or publication evidence is missing or ambiguous | No live operation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTSM.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | satisfied->MNTSM.ENFORCE_DESIGN;needs_decision->MNTSM.REPORT_ISSUES;prerequisite_pending->MNTSM.REPORT_ISSUES;blocked->MNTSM.REPORT_ISSUES | MNTSM.RESOLVE_LOOKUPS | stop | Evaluate Service Mapping contract, subscription context, target field context, source decision, handoff readiness, and publication evidence for the current rule_phase. |
