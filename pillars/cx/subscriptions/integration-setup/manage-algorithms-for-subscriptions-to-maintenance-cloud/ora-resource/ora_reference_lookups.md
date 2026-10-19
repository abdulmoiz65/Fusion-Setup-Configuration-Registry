# Maintenance Cloud Algorithm Reference Lookups

## Scope and authority

This file owns lookup mechanics and the source catalogue for the Maintenance Cloud algorithm task. Public Oracle documentation is used as authoring evidence for business flow and target interface field meanings. It is not a live environment lookup and does not prove that a customer environment has the same deployed configuration, service mapping aliases, privileges, or process results.

Because the supplied documentation does not identify supported Fusion REST lookup endpoints for this setup task, every live lookup contract below remains unresolved until the implementation owner provides the supported read path and response mapping.

## Source Catalogue

| Source | Documentation | Reviewed Scope and Status |
|---|---|---|
| S1 | https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf | General Subscription Management guide. Used for coverage products, covered level context, subscription validation, activation, and approval context. |
| S2 | https://docs.oracle.com/en/cloud/saas/readiness/sales/24b/ssma-24b/24B-subscription-wn-f31902.htm | 24B readiness feature for preventive maintenance plans in subscriptions. Used for coverage-template association, active-subscription process order, and no-steps-to-enable statement. |
| T1 | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntprogramsint-28604.html | MNT_PROGRAMS_INT target interface table. Used for program header field names, types, lengths, primary key, and interface indexes. |
| T2 | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntworkrequirementsint-16187.html | MNT_WORK_REQUIREMENTS_INT target interface table. Used for work requirement field names, types, lengths, primary key, and interface indexes. |

## Target Interface Model

| Target Area | Documented Object | Key Documentation Facts | Authoring Boundary |
|---|---|---|---|
| Maintenance program header | MNT_PROGRAMS_INT | Interface entity for maintenance program header information; primary key is INTERFACE_ROW_ID; HEADER_NUMBER links child interface entities; PROGRAM_CODE and PROGRAM_NAME are user-facing identifiers | Use as target field evidence only; do not infer source aliases or direct table writes |
| Maintenance work requirement | MNT_WORK_REQUIREMENTS_INT | Interface entity for maintenance program work requirement information; primary key is INTERFACE_ROW_ID; HEADER_NUMBER links to related interface entities; PROGRAM_ID links to the program; REQUIREMENT_TYPE_CODE values include Asset and Item; STATUS_CODE values include Draft and Active | Use as target field evidence only; do not infer source aliases or direct table writes |
| Preventive maintenance subscription flow | Subscription Management readiness feature | A maintenance program template associated to a coverage product creates a maintenance program for covered levels; after activation, scheduled processes interface and retrieve the instantiated program | Treat process submission and polling as separate workflow contracts, not algorithm authoring proof |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_maintenance_algorithm_contract | Every checkpoint that needs current algorithm identity, mutation route, artifact preparation, or verification | Target environment, setup task name, current algorithm artifact identifier, rule_phase | TBD | Supported algorithm artifact, algorithm version, active flag, supported import or save route, verification path, correction route | Match exactly one current Maintenance Cloud algorithm contract for this setup task and target environment | algorithm_contract_status, algorithm_artifact_id, algorithm_version, mutation_route, verification_route | Stop; ask implementation owner for the supported Manage Algorithms artifact and execution contract |
| verify_maintenance_service_mapping_handoff | Proposal or approved change references subscription source aliases or custom fields | Service mapping handoff identifier, source alias, source object, source type, publication evidence | TBD | Source alias, source object, data type, service access, publication state, prerequisite status | Match each proposed source exactly once and require publication or explicit prerequisite status | confirmed_sources, source_types, publication_prerequisites | Stop; return unresolved source questions to Service Mapping |
| verify_subscription_maintenance_context | Proposal or transfer validation depends on preventive-maintenance subscription behavior | Subscription number or id, coverage product, standard coverage, covered level identifiers, maintenance program template identifier | TBD | Subscription status, product type, coverage product, covered level type and value, maintenance program template, activation status | Match one active subscription context and one applicable coverage-maintenance template association | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id | Stop; ask for the exact subscription, coverage product, template, or covered level evidence |
| resolve_maintenance_interface_import_contract | Proposal maps to Maintenance Cloud target interface fields or transfer validation is requested | Environment release, target interface table, column list, process names, batch code or header number | TBD | Supported import method, accepted action codes, program type code for subscription preventive plan, batch/header semantics, validation status source | Match the target import contract for MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT in the current release | supported_import_method, accepted_action_codes, program_type_code, batch_keys, result_status_fields | Stop; preserve target data model mapping but mark execution contract incomplete |
| verify_maintenance_approval_evidence | approved_change or artifact_result | Proposal id, current source fingerprints, target environment, approved target fields, approver or approval reference | TBD | Approval timestamp, approved proposal version, approved target environment, approved change scope | Approval must match current source fingerprints, exact target environment, and exact field-level change scope | approval_status, approved_scope, approval_reference | Stop for missing, stale, broader, or ambiguous approval |
| verify_maintenance_target_import_state | transfer_validation | Scheduled process names, request ids, subscription id, batch code, header number, program code, requirement name | TBD | Process status, interface row status, instantiated maintenance program identifier, errors, warnings, retrieval status | Correlate the three documented scheduled processes to the same subscription and maintenance program context | process_statuses, interface_statuses, instantiated_program_id, validation_errors | Stop; report incomplete or ambiguous transfer evidence without retrying a process |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Lookup endpoint is TBD | Keep the lookup node incomplete and block readiness; do not substitute a browser, direct SQL, table docs, or another REST resource |
| Oracle public documentation describes a table column | Use it only as target field evidence; require service mapping or environment lookup evidence for source alias and deployed configuration |
| Subscription is not active | Treat downstream transfer readiness as blocked because the readiness feature requires activation before running the three scheduled processes |
| Service Mapping source evidence is missing | Return the missing source object, alias, type, or publication prerequisite to the caller; do not draft Groovy from target table names |
| Transfer process evidence is supplied | Correlate the three scheduled processes and target row identifiers before claiming instantiated preventive maintenance program evidence |

## Unsupported Live Contracts

| Future Capability | Missing Contract | Required Completion Evidence |
|---|---|---|
| Algorithm mutation or import | TBD: supported Manage Algorithms export/import artifact, mutation route, save path, verification path, rollback or correction path, and privilege model | Oracle-documented or team-approved execution contract for this setup task and exact target environment |
| Subscription maintenance-context lookup | TBD: REST read path and response mapping for subscription, coverage product, covered levels, and maintenance program template association | Read-only lookup contract with match rules and returned identifiers |
| Maintenance interface import contract | TBD: action codes, program type code value, import method, batch semantics, and supported status source for MNT_PROGRAMS_INT and MNT_WORK_REQUIREMENTS_INT | Release-matched import documentation or validated implementation contract |
| Scheduled process submission and polling | TBD: ESS submission route, parameters, polling route, timeout, retry, and diagnostic log retrieval | Separate approved workflow for Send Maintenance Program and Covered Assets to Oracle Maintenance, Import Maintenance Programs, and Retrieve Instantiated Maintenance Program |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTALG.RESOLVE_LOOKUPS | step | 20 | reference_lookup | resolved->MNTALG.CHECK_DEPENDENCIES;unresolved->MNTALG.REPORT_ISSUES;incomplete_contract->MNTALG.REPORT_ISSUES | MNTALG.VALIDATE_INPUT | stop | Resolve only documented lookup contracts for algorithm, mapping, subscription context, interface import contract, approval, and transfer validation. |
