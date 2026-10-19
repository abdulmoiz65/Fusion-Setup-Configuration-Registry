# Maintenance Cloud Service Mapping Reference Lookups

## Scope and authority

This file owns lookup mechanics and the source catalogue for `Manage Service Mappings for Subscriptions to Maintenance Cloud`. Public Oracle documentation is authoring evidence for Subscription coverage behavior and Maintenance target interface-table shape. It is not live environment evidence, not a Service Mapping export, and not proof that a customer environment has published aliases or access.

The supplied documentation does not identify the supported live Service Mapping read/export/publish route. Those unresolved contracts remain `TBD` in the lookup rows so the registry fails closed until the implementation owner provides the missing read path and response mapping. Missing source attributes have one limited exception: the two permitted read-only Subscription Product describe paths below may be used only to discover exact source attributes and data types before suggesting a Service Mapping variable.

## Source Catalogue

| Source | Documentation | Reviewed Scope and Status |
|---|---|---|
| S1 | https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf | General Subscription Management guide. Used for subscriptions, products, coverage products, covered levels, validation, activation, and approval context. |
| S2 | https://docs.oracle.com/en/cloud/saas/readiness/sales/24b/ssma-24b/24B-subscription-wn-f31902.htm | 24B readiness feature for preventive maintenance plans in subscriptions. Used for coverage-template association, active-subscription process order, and no-steps-to-enable statement. |
| T1 | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntprogramsint-28604.html | MNT_PROGRAMS_INT target interface table. Used for maintenance program header field names, type hints, length hints, key fields, and interface identity. |
| T2 | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntworkrequirementsint-16187.html | MNT_WORK_REQUIREMENTS_INT target interface table. Used for work requirement field names, type hints, length hints, key fields, and asset or item requirement concepts. |

## Target Interface Model

| Target Area | Documented Object | Key Documentation Facts | Service Mapping Boundary |
|---|---|---|---|
| Maintenance program header | MNT_PROGRAMS_INT | Holds maintenance program header information; primary key is INTERFACE_ROW_ID; HEADER_NUMBER links child interface entities; PROGRAM_CODE, PROGRAM_NAME, PROGRAM_TYPE_CODE, organization, dates, forecast and work-order windows, suppress merge, review, reference, and DFF fields are available | Use as target field evidence only; source aliases must come from Service Mapping evidence |
| Maintenance work requirement | MNT_WORK_REQUIREMENTS_INT | Holds maintenance program work requirement information; primary key is INTERFACE_ROW_ID; HEADER_NUMBER links related interface entities; REQUIREMENT_TYPE_CODE values include Asset and Item; STATUS_CODE values include Draft and Active; item, asset, schedule, meter, condition, date, forecast, work-order, route, and reference fields are available | Use as target field evidence only; source aliases must come from Service Mapping evidence |
| Subscription preventive-maintenance flow | Subscription readiness feature | A maintenance program template associated to a coverage product creates a maintenance program for covered levels; after activation, three scheduled processes interface and retrieve instantiated maintenance program details | Service Mapping guidance may prepare source exposure; scheduled processes and target import verification are separate workflow contracts |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_maintenance_service_mapping_contract | Every checkpoint that needs current Service Mapping source entities, aliases, access, publication state, or supported update route | Target environment, setup task name, mapping context, current artifact identifier, rule_phase | TBD | Mapping context name, source entities, source attributes, aliases, data types, access flags, publication state, supported update or publish route | Match exactly one current Service Mapping context for Subscriptions to Maintenance Cloud | mapping_context_id, source_entities, source_aliases, source_types, service_access, publication_state, update_route | Stop; ask implementation owner for the supported Service Mapping export or read contract |
| verify_subscription_maintenance_context | Analysis or handoff depends on preventive-maintenance subscription behavior | Subscription id or number, coverage product, standard coverage, covered level identifiers, maintenance program template identifier | TBD | Subscription status, product type, coverage product, covered level type and value, maintenance program template, activation status | Match one subscription coverage context and one applicable maintenance template association | active_subscription_id, coverage_product_id, covered_level_keys, maintenance_program_template_id | Stop; ask for exact subscription, coverage product, covered level, or template evidence |
| resolve_maintenance_target_interface_fields | Target interface field validation or source-to-target pairing is requested | Target table name, target field name, environment release, proposed business meaning | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntprogramsint-28604.html and https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/oedsc/mntworkrequirementsint-16187.html | Column name, data type, length, precision, documented comments, primary key status | Match target field exactly in MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT; unresolved accepted values remain a decision gap | target_table, target_column, target_type, target_length, target_meaning, target_gap | Stop for unknown field; return accepted-value gaps for action codes, program types, statuses, or other undocumented runtime values |
| verify_maintenance_source_resolution | Analysis or handoff evaluates a source candidate | Business meaning, source object, source attribute, target field, mapping context | Current source XML first; if absent, `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` for `Products` or `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` for `CoveredAssets` | Source object, exact source attribute, alias, data type, queryability, service access, publication status, candidate confidence, evidence source | Match one candidate to one business meaning and target field; keep alternatives separate | source_object, source_attribute, source_alias, source_type, source_status, alternatives, evidence_source | Return needs_describe, needs_decision, or prerequisite_pending; do not choose by target column name alone |
| verify_maintenance_mapping_handoff | Handoff is requested by the companion Algorithms task or project workflow | Source-resolution records, target interface fields, publication prerequisites, unresolved questions, caller continuation | TBD | Handoff identity, selected source records, target fields, type compatibility, prerequisites, unresolved decisions, next owner | Handoff must match current request identity and include unresolved items explicitly | handoff_status, selected_sources, source_target_pairs, prerequisites, unresolved_items | Stop; ask for missing source record, target field, or continuation details |
| verify_maintenance_mapping_publication | User asks whether Service Mapping is deployed or ready for transfer | Mapping context, source aliases, publication or deployment evidence, target environment | TBD | Publication status, last publish time, source aliases, access flags, environment identity | Match published state for the exact target environment and mapping context | publication_status, deployed_aliases, deployment_evidence | Stop; local artifact evidence is not publication evidence |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Lookup endpoint is TBD | Keep the lookup node incomplete and block readiness; do not substitute browser navigation, direct SQL, table documentation, or another REST resource |
| Source XML lacks a requested `Products` value | Use `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` to find exact product-level attribute names and data types before recommending a Service Mapping variable |
| Source XML lacks a requested `CoveredAssets` or covered-level value | Use `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` to find exact covered-level attribute names and data types before recommending a Service Mapping variable |
| Describe cannot be run, fails, or returns ambiguous candidates | Return `needs_describe` or `needs_decision` with the missing evidence or alternatives; do not invent a `_Custom` alias |
| Oracle public documentation describes target fields | Use it only to validate target field names and shape; require Service Mapping evidence for source aliases, data types, access, and publication |
| Coverage product and maintenance template association is unverified | Return the exact missing coverage, covered level, or template fact; do not produce source-to-target readiness |
| Multiple source candidates fit one target field | Return needs_decision with alternatives and evidence; do not select a default without documented owner or user decision |
| Published state is unknown | Mark publication as prerequisite_pending, not analyzed success |

## Unsupported Live Contracts

| Future Capability | Missing Contract | Required Completion Evidence |
|---|---|---|
| Service Mapping export, create, update, or publish | TBD: supported route, request path, privilege model, payload format, response fields, and mapping context identity | Separate approved workflow; the two permitted describe paths only support read-only source discovery |
| Service Mapping create, update, or publish | TBD: supported executor, payload format, approval gate, idempotency, verification, and recovery | Separate approved mutation workflow; this authoring package does not supply it |
| Subscription coverage-context live lookup | TBD: REST read path and response mapping for subscription coverage product, covered levels, and maintenance program template | Read-only lookup contract with exact match rules and returned identifiers |
| Published mapping verification | TBD: environment-matched source alias and publication status acquisition | Supported verification contract with sanitized evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTSM.RESOLVE_LOOKUPS | step | 20 | reference_lookup | resolved->MNTSM.CHECK_DEPENDENCIES;unresolved->MNTSM.REPORT_ISSUES;incomplete_contract->MNTSM.REPORT_ISSUES | MNTSM.VALIDATE_INPUT | stop | Resolve documented lookup contracts for service mapping source evidence, subscription maintenance context, target interface fields, source decisions, handoff, and publication state. |
