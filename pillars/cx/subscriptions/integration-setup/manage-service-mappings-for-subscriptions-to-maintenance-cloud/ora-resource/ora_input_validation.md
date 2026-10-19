# Maintenance Cloud Service Mapping Input Validation

## Scope

This resource validates inputs and returned result shapes for `Manage Service Mappings for Subscriptions to Maintenance Cloud`. It focuses on source exposure, source alias selection, service access, publication prerequisites, and the handoff needed by the companion Algorithms task. The supplied Oracle documentation establishes Subscription coverage context, preventive-maintenance process flow, and target Maintenance interface-table shape. It does not document the live Service Mapping export, save, or publish contract, so those contracts remain blocking `TBD` lookup fields. For missing source attributes, only the two permitted read-only Subscription Product describe paths may be used to identify exact source attributes and data types before suggesting a Service Mapping variable.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Checkpoint scope | rule_phase equals intake, analysis, handoff, approved_change, or transfer_validation; exact task identity; requested mapping outcome | Return the missing or invalid checkpoint scope | Caller supplies the current phase and distinguishes source analysis from unsupported live mutation | Every checkpoint | |
| Service Mapping artifact or evidence | Current Service Mapping export, current mapping source XML, source entity list, or supported service mapping configuration evidence for this task | Stop before source analysis, source recommendation, or handoff | Provide the supported Service Mapping artifact or documented read-only lookup route for Subscriptions to Maintenance Cloud | Every checkpoint | resolve_maintenance_service_mapping_contract |
| Business requirement and source question | Business meaning, requested source object or target Maintenance field, known source candidates, project context, and continuation identity when applicable | Ask for the specific source question and target business meaning | Capture one source-resolution question per request; do not infer from target table names alone | intake or analysis | |
| Subscription maintenance context | Subscription coverage product, covered levels, maintenance program template association, active subscription evidence when transfer readiness is claimed | Stop before claiming preventive-maintenance mapping readiness | Verify the subscription coverage context through supplied evidence or documented lookup | analysis, handoff, transfer_validation | verify_subscription_maintenance_context |
| Target interface field context | Selected MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT fields, target data type, target length, and business role | Block source-to-target recommendation for undocumented target fields | Use the supplied Oracle target table documentation and require release-matched confirmation for unsupported fields | analysis or handoff | resolve_maintenance_target_interface_fields |
| Source resolution record | Source object, source attribute, source alias, data type, cardinality, service access, publication state, prerequisite state, and confidence | Return unresolved source fields; do not label result analyzed | Complete source-resolution analysis and preserve unresolved or assumed items explicitly | analysis or handoff | verify_maintenance_source_resolution |
| Configuration handoff | Structured result with source aliases, target interface fields, type and length compatibility, publication prerequisites, unresolved questions, and companion Algorithms next action | Return missing handoff fields | Produce a source-to-target handoff without claiming deployed Service Mapping or algorithm mutation | handoff | verify_maintenance_mapping_handoff |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Service Mapping evidence shape | Require a current artifact or documented read-only lookup output with source entity, alias, type, access, and publication fields | Every checkpoint | resolve_maintenance_service_mapping_contract |
| Describe-first source discovery | When source XML lacks the requested source value, require an allowed describe result with exact source object, exact source attribute, data type, and evidence source before suggesting a new alias | A missing source value is being mapped | verify_maintenance_source_resolution |
| Source and target separation | Reject results that treat MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT columns as Subscription source aliases | A source is missing or only a target column is named | resolve_maintenance_target_interface_fields |
| Coverage source fit | Require a source decision for coverage product, covered level, and maintenance program template values before recommending a mapping | Preventive-maintenance source mapping is requested | verify_subscription_maintenance_context |
| Target header field shape | Validate selected program header target fields against documented data types and lengths | Proposal or handoff maps MNT_PROGRAMS_INT | resolve_maintenance_target_interface_fields |
| Target work requirement field shape | Validate selected work requirement target fields against documented data types and lengths | Proposal or handoff maps MNT_WORK_REQUIREMENTS_INT | resolve_maintenance_target_interface_fields |
| Source data type compatibility | Preserve source type evidence and report incompatible character, number, date, timestamp, or flag shapes without silent coercion | Source and target are paired | verify_maintenance_source_resolution |
| Enumerated target values | Require documented or implementation-approved source and value rules for requirement type Asset or Item, work requirement status Draft or Active, and any action or program type codes | Enumerated target fields are used | resolve_maintenance_target_interface_fields |
| Publication state | Distinguish local source recommendation from published Service Mapping configuration | Handoff or transfer validation is requested | verify_maintenance_mapping_handoff |
| System and audit columns | Do not ask the implementer to map who columns, ESS request columns, load request identifiers, or system-generated primary keys as ordinary business sources | Source collection includes system-managed target columns | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Service Mapping artifact or read-only lookup route is missing | Blocked | Request current mapping evidence or supported read-only lookup route | resolve_maintenance_service_mapping_contract |
| Source question lacks business meaning or target context | Missing | Ask for the business meaning, source object, or target Maintenance field | |
| Coverage product or maintenance program template context is not verified | Blocked | Resolve subscription coverage context before recommending source aliases | verify_subscription_maintenance_context |
| Target field exists in the Oracle table docs but accepted runtime value rules are not documented | Needs decision | Return the specific accepted-value gap and continue only as draft guidance | resolve_maintenance_target_interface_fields |
| Requested source value is absent from source XML and describe evidence is unavailable | needs_describe | Request the allowed describe output or explicit implementer approval to proceed without describe evidence | verify_maintenance_source_resolution |
| Source candidate exists but publication or access is unresolved | prerequisite_pending | Return the source candidate with its publication or access prerequisite | verify_maintenance_source_resolution |
| Handoff accurately reports unresolved, blocked, or prerequisite-pending work | Valid structured outcome | Return findings to the caller without claiming deployed mapping | verify_maintenance_mapping_handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTSM.VALIDATE_INPUT | step | 10 | validate_input | valid->MNTSM.RESOLVE_LOOKUPS;invalid->MNTSM.REPORT_ISSUES | none | stop | Validate phase, current mapping evidence, source question, subscription coverage context, target interface context, and handoff shape. |
| MNTSM.EVALUATE_HANDOFF | step | 60 | evaluate_result | valid->MNTSM.RETURN_RULE_RESULTS;invalid->MNTSM.REPORT_ISSUES | MNTSM.CHECK_EXECUTION_CONTRACT | stop | Evaluate completed source-resolution and handoff checks; valid means checkpoint completion only, not deployed Service Mapping or Maintenance Cloud transfer success. |
