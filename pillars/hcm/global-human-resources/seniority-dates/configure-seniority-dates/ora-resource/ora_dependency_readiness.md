# Configure Seniority Dates Dependency Readiness

## Purpose

Defines the conditional configuration, formula, worker-scope, and target
references used by Configure Seniority Dates. Each supplied value is resolved
independently through its own documented contract and no missing setup is created.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Create intake completeness | Identify supplied business inputs. If any required create input is missing, ask once for exactly those inputs and stop before deep validation. |
| 2 | Seniority rule | After complete intake, resolve the supplied rule name or code to SeniorityDateCode. |
| 3 | Environment and privileges | Determine the configured environment and validate required current-state and Data Loader privileges without asking the user for environment confirmation. |
| 4 | Seniority configuration identity | Read fresh current target data or confirm the proposed create identity using the resolved code. |
| 5 | Rule-usage evaluation | For update or delete, invoke evaluate_seniority_rule_usage using the fresh exact target primary key and map ruleUsed to RecordPresent. |
| 6 | Remaining configuration values | Resolve attribute, level, basis, flags, and every technical field required by the current operation-specific create template independently. |
| 7 | Formula references | Resolve each supplied formula independently. |
| 8 | Worker and scope references | Resolve supplied worker type, country, Legal Employer, Union, and Collective Agreement values, or apply the `No restriction` default. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| create_intake | Complete create business inputs | Mandatory | Create | Needs Input | Create intake |  | Require rule, attribute, and level. Default omitted Active to Y, Cumulative to N, Display in Guided Flows to N, Allow Edit to Y, and scope to `No restriction` before lookup resolution | Provide only the missing required values | Complete intake |
| seniority_rule | Seniority rule | Conditional | A complete create intake or a supplied non-create selector | Lookup | Common Lookup type ORA_PER_SENIORITY_ITEMS | resolve_seniority_rule | Resolves the code required by the configuration read | Provide one exact rule code or meaning | SeniorityDateCode and display Meaning |
| mutation_environment | Configured Fusion environment and privileges | Mandatory | Create, edit, or delete | Verify | Current environment configuration and authorized core services | validate_mutation_environment | Prevents a preview or mutation against an unknown or unauthorized target | Determine the configured environment without user confirmation | Safe environment alias and preflight result |
| seniority_configuration_identity | Existing configuration or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Seniority Date Configuration resource | find_configured_seniority_date_rules | Prevents an ambiguous target or duplicate create | Provide one exact rule selector | Resolved configuration identity and current values |
| record_present | Evaluated rule-usage value | Mandatory | Update or delete | Verify | employmentConfigurations/action/performEmploymentOperations | evaluate_seniority_rule_usage | Determines whether the target is used before a mutation is planned | No user input; invoke with the fresh resolved primary key | RecordPresent Y or N |
| seniority_attribute | Seniority attribute | Conditional | An attribute value is supplied | Lookup | Current describe-declared attribute values | resolve_seniority_attribute | Stores one supported attribute value | Provide one exact attribute code or meaning | Stored seniority attribute value |
| seniority_level | Seniority level | Conditional | A level value is supplied | Lookup | Current describe-declared level values | resolve_seniority_level | Stores one supported level value | Provide one exact level code or meaning | Stored seniority level value |
| seniority_object | Seniority object | Conditional | An object value is supplied | Lookup | Current describe-declared object values | resolve_seniority_object | Stores one supported object value | Provide one exact object code or meaning | Stored seniority object value |
| seniority_basis | Seniority basis | Conditional | A basis value is supplied | Lookup | Current describe-declared basis values | resolve_seniority_basis | Stores one supported basis value | Provide one exact basis code or meaning | Stored seniority basis value |
| active_flag | Active flag | Conditional | Active is supplied or defaulted | Lookup | Current describe-declared Active values | resolve_seniority_active | Prevents an unsupported stored flag | Provide one exact code or meaning when overriding | Stored Active value |
| cumulative_flag | Cumulative flag | Conditional | Cumulative is supplied or defaulted | Lookup | Current describe-declared Cumulative values | resolve_seniority_cumulative | Prevents an unsupported stored flag | Provide one exact code or meaning when overriding | Stored Cumulative value |
| allow_edit_flag | Allow Edit flag | Conditional | Allow Edit is supplied or defaulted | Lookup | Current describe-declared Allow Edit values | resolve_seniority_allow_edit | Prevents an unsupported stored flag | Provide one exact code or meaning when overriding | Stored Allow Edit value |
| display_in_ui_flag | Display in UI flag | Conditional | Display in UI is supplied or defaulted | Lookup | Current describe-declared Display in UI values | resolve_seniority_display_in_ui | Prevents an unsupported stored flag | Provide one exact code or meaning when overriding | Stored Display in UI value |
| union_member_flag | Union Member flag | Conditional | Union Member is supplied or defaulted | Lookup | Current describe-declared Union Member values | resolve_seniority_union_member | Prevents an unsupported stored flag | Provide one exact code or meaning when overriding | Stored Union Member value |
| technical_tuple | Template-driven technical fields | Conditional | Create template exposes required or optional technical fields, or edit evaluates existing tuple members | Lookup | Current operation-specific Data Loader create template, schema, LOV, defaults, and exact triggering-field evidence | derive_seniority_configuration_tuple | Validates only populated or template-required fields without inventing values | For create, do not provide tuple members independently; omit absent fields and preserve optional blanks. For edit, preserve the exact current tuple unless change is explicitly supported. | Required populated technical fields; omitted absent fields; supported optional values |
| adjustment_formula | Adjustment formula | Conditional | An adjustment formula is supplied | Lookup | Current formula configuration | resolve_seniority_adjustment_formula | Stores one exact compatible formula reference | Provide one exact formula selector | Stored adjustment formula reference |
| hour_conversion_formula | Hour-conversion formula | Conditional | An hour-conversion formula is supplied | Lookup | Current formula configuration | resolve_seniority_hour_conversion_formula | Stores one exact compatible formula reference | Provide one exact formula selector | Stored hour-conversion formula reference |
| worker_type | Worker type | Conditional | A worker type is supplied | Lookup | Current worker-type configuration | resolve_seniority_worker_type | Stores one exact supported worker type | Provide one exact code or meaning | Stored worker-type value |
| country | Country | Conditional | A country is supplied | Lookup | Current country configuration | resolve_seniority_country | Establishes one exact country scope | Provide one exact country code or name | Stored country or legislation value |
| legal_employer | Legal Employer | Conditional | A Legal Employer is supplied | Lookup | Current Legal Employer configuration | resolve_seniority_legal_employer | Keeps scope attached to one exact Legal Employer | Provide one exact Legal Employer selector | Stored Legal Employer reference |
| union | Union | Conditional | A Union is supplied | Lookup | Current Union configuration | resolve_seniority_union | Keeps scope attached to one exact Union | Provide one exact Union selector | Stored Union reference |
| collective_agreement | Collective Agreement | Conditional | A Collective Agreement is supplied | Lookup | Current Collective Agreement configuration | resolve_seniority_collective_agreement | Keeps scope attached to one exact Collective Agreement | Provide one exact Collective Agreement selector | Stored Collective Agreement reference |
| no_restriction_scope | Unrestricted scope choice | Conditional | Create explicitly supplies `No restriction` or omits every scope selector | Verify | Create intake | validate_scope_no_restriction | Leaves all scope dimensions blank as the explicit or defaulted scope | No input required when scope is omitted | Blank scope dimensions |
| current_business_state | Fresh target and package-state evidence | Mandatory | Create, edit, delete, preview, revalidation, or verification | Lookup | Current configuration resource and current Data Loader contract | read_current_seniority_rule | Prevents use of a prior export, saved identifier, or stale preview | No user input; read fresh state | Canonical business-state fingerprint and current values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Run the read-only resolver now; do not pause |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEN.DEPENDENCIES | decision | 2 | resolve_dependency | ready->SEN.READ;not_required->SEN.READ;needs_input->SEN.ERROR;unresolved->SEN.ERROR | SEN.VALIDATE | stop | After input validation and before task-local reference lookups |
