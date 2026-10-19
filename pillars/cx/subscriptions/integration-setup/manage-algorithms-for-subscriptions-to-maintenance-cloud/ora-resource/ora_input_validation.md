# Maintenance Cloud Algorithm Input Validation

## Scope

This resource validates the authoring and checkpoint inputs for `Manage Algorithms for Subscriptions to Maintenance Cloud`. The supplied Oracle documentation establishes the Subscription coverage context, the activation and scheduled-process handoff, and the Maintenance Cloud target interface-table shape. It does not provide a complete supported algorithm mutation/import contract, so execution remains blocked wherever that contract is required.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Checkpoint context | rule_phase, implementation objective, project context, requested algorithm outcome, source documents reviewed | Stop this checkpoint; do not infer an execution phase | Caller supplies the current phase and objective for this task | Every checkpoint | |
| Algorithm authoring artifact | Supported current algorithm export, source XML, payload, or configuration artifact for this setup task | Stop before proposal, approval, artifact creation, or live execution | Implementation owner must provide the supported Manage Algorithms artifact contract for Subscriptions to Maintenance Cloud | Every checkpoint | resolve_maintenance_algorithm_contract |
| Service mapping handoff | Confirmed source aliases, source data types, service access, and publication prerequisites for subscription coverage, covered levels, and maintenance program template values | Return to source-resolution before drafting algorithm logic | Use the companion Service Mappings task or a supplied configuration handoff; do not invent aliases from target table names | proposal, approved_change, artifact_result, transfer_validation | verify_maintenance_service_mapping_handoff |
| Subscription maintenance eligibility | Subscription identifier, subscription status evidence, coverage product, maintenance program template association, covered level identifiers | Stop before claiming Maintenance Cloud integration readiness | Verify the active subscription and coverage-maintenance context through a documented lookup or supplied evidence | proposal, transfer_validation | verify_subscription_maintenance_context |
| Target interface mapping scope | Selected MNT_PROGRAMS_INT header fields; selected MNT_WORK_REQUIREMENTS_INT work requirement fields; per-field source, type, length, and derivation rule | Block proposal and preview; target shape is ambiguous | Complete a field-level mapping matrix against the documented target interface tables | proposal, approved_change, artifact_result | resolve_maintenance_interface_import_contract |
| Approval evidence | Complete proposal, exact target environment, current source fingerprints, selected algorithm artifact, and explicit approval bound to that version | Block artifact creation or any live change | Obtain approval for the exact current proposal and target; source-selection approval is not enough | approved_change or artifact_result | verify_maintenance_approval_evidence |
| Transfer validation evidence | Request IDs or batch identifiers for Send Maintenance Program and Covered Assets to Oracle Maintenance, Import Maintenance Programs, and Retrieve Instantiated Maintenance Program | Report validation incomplete; do not assert downstream instantiation | Supply scheduled-process evidence and result artifacts for the active subscription | transfer_validation | verify_maintenance_target_import_state |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported algorithm contract | Treat the algorithm source, write method, import route, verification query, and rollback or correction procedure as unresolved until documented | Every checkpoint that would prepare or execute an algorithm change | resolve_maintenance_algorithm_contract |
| Source versus target ownership | Reject proposals that use Maintenance interface table columns as proof that a Subscription source alias exists | A source alias is missing or only a target column is named | verify_maintenance_service_mapping_handoff |
| Coverage product context | Require evidence that the subscription product is a coverage product with covered levels and a maintenance program template association | Proposal or transfer validation uses preventive-maintenance behavior | verify_subscription_maintenance_context |
| Active subscription gate | Do not treat scheduled-process transfer as ready unless the subscription is active | transfer_validation | verify_subscription_maintenance_context |
| Target table boundary | Allow mapping only to documented MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT interface fields; reject direct base Maintenance table updates | Proposal names a target field or table | resolve_maintenance_interface_import_contract |
| Header and child linking | Require a stable header-to-work-requirement relationship using documented header, program, or batch identifiers; do not create orphan work requirement mappings | Proposal maps work requirement rows | resolve_maintenance_interface_import_contract |
| Program header field shape | Validate program code, name, type, subtype, organization, dates, forecast and work-order windows, timezone, suppress-merge, review, reference, DFF, and load request fields against documented data types and lengths | Proposal maps MNT_PROGRAMS_INT | resolve_maintenance_interface_import_contract |
| Work requirement field shape | Validate requirement name, type, item or asset identifier, schedule, meter, condition, status, dates, forecast and work-order window, work-order status, priority, and firm planned fields against documented data types and lengths | Proposal maps MNT_WORK_REQUIREMENTS_INT | resolve_maintenance_interface_import_contract |
| Enumerated target meanings | Require explicit value decisions for requirement type Asset or Item, status Draft or Active, and any undocumented program type or action codes | Proposal supplies enumerated values | resolve_maintenance_interface_import_contract |
| System and audit columns | Do not ask the implementer to supply who columns, ESS request columns, or other system-managed audit values as business inputs | Input collection includes system-managed columns | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Algorithm contract is TBD | Blocked | Capture the missing Manage Algorithms artifact and execution route; do not create a local mutation artifact | resolve_maintenance_algorithm_contract |
| Required subscription or coverage context is not verified | Blocked | Resolve active subscription, coverage product, covered levels, and template association before algorithm proposal | verify_subscription_maintenance_context |
| Service mapping source decisions are incomplete | Blocked | Complete mapping source decisions before translating them into Maintenance interface fields | verify_maintenance_service_mapping_handoff |
| Target interface mapping is complete but live import route is not documented | Draft only | Return the field mapping and execution gap; no live write, process submission, or success claim | resolve_maintenance_interface_import_contract |
| All phase-applicable validation, dependency, lookup, design, and approval gates pass | Checkpoint passed | Return findings, evidence references, unresolved live gaps, and the safe next action | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTALG.VALIDATE_INPUT | step | 10 | validate_input | valid->MNTALG.RESOLVE_LOOKUPS;invalid->MNTALG.REPORT_ISSUES | none | stop | Validate phase, source evidence, mapping scope, target interface field shape, and approval evidence required for the requested checkpoint. |
