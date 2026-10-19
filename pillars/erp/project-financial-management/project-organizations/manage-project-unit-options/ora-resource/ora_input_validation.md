# Input Validation

## CSV Column Intent Resolution

| CSV Column | User Intent |
|---|---|
| PJF_PROJECT_UNIT.csv.Name | Project Unit Name |
| PJF_PROJECT_UNIT.csv.UserDefinedProjectNumCode | Project Numbering Method |
| PJF_PROJECT_UNIT.csv.ManualProjectNumType | Manual Project Numbering Method Type |
| PJF_PROJECT_UNIT.csv.DefaultProjCurrCode | Default Project Currency |
| PJF_PROJECT_UNIT.csv.SetCode | Default Set |
| ORA_PJF_PU_BU_RELATIONSHIP.csv.PJF_PROJECT_UNIT.Name | Parent Project Unit Name |
| ORA_PJF_PU_BU_RELATIONSHIP.csv.Name | Related Business Units |
| ORA_PROJECT_AUTOMATIC_NUMBER.csv.NextUniqueIdentifier | Next Unique Identifier |
| ORA_PROJECT_AUTOMATIC_NUMBER.csv.TableName | Automatic Project Numbering Table Name (no visible UI field) |
| PJF_REPORTING_SETUP.csv.Name | Project Unit Name |
| PJF_REPORTING_SETUP.csv.CommitmentStatusExtr | Other Commitments Status |
| PJF_REPORTING_SETUP.csv.CommitmentStatusPo | Status: Purchase Orders |
| PJF_REPORTING_SETUP.csv.CommitmentStatusReq | Status: Requisitions |
| PJF_REPORTING_SETUP.csv.CommitmentStatusSupinv | Status: Supplier Invoices |
| PJF_REPORTING_SETUP.csv.PlanamtAllocMethod | Allocation Basis Method |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation as create, update, validate, export, or import | Block preview | Ask for the intended operation; refuse project-unit delete and set-assignment mutation through this task | Every request |  |
| Project unit identity | ProjectUnitId, Organization, or exact project-unit name/code | Block preview | Ask for one stable project-unit identifier | Create option row, update, validate, or import | find_project_unit_options |
| General properties | Default set name, explicitly labeled SetCode, UserDefinedProjectNumCode, ManualProjectNumType, DefaultProjCurrCode, FteDay, FteWeek | Block when a required or conditional field is missing | Treat an unlabeled Default Set value as a set name; use SetCode only when explicitly labeled; project-number entry is required; ManualProjectNumType is validated only when entry code is MANUAL; supplied currency must exist; FTE values retain two decimals by round-down | General-property change | resolve_reference_set |
| Related business units | Exact BusinessUnitName list | Preserve current associations when omitted | Validate only nonblank, unique supplied names for additions; never convert omission into an empty list or request independent eligibility evidence | Related-business-unit change | resolve_project_business_units |
| Reporting setup | ExternalCommitments, PurchaseOrders, Requisitions, SupplierInvoices, per-type StatusValue, Basis | Preserve omitted fields on an existing complete row; use ora_defaulting_rules.md for omitted fields on a missing row | Resolve explicit intent first; clarify ambiguity; allow genuine omission to proceed to baseline resolution and defaulting | Reporting change, new project unit, missing `PJF_REPORTING_SETUP` row, or downstream plan-type/template use | find_project_unit_options |
| Target environment | TargetEnvironment | Block preview | Ask for the target Fusion environment | Every request | verify_project_unit_options_scope |
| Runtime artifacts | current_export, package_template, numbering_feature_status | Block affected preview | Obtain fresh target-pod artifacts; set membership is handled separately by resolve_reference_set | Create, update, validate, or import | verify_project_unit_options_package |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Project unit resolves exactly once and is already classified | Satisfied | Continue with its current option baseline | find_project_unit_options |
| Project unit has no implementation-option row and operation is create | Satisfied | Create only the missing option row | find_project_unit_options |
| Update has no single project-unit match | Blocked | Correct the project-unit identity | find_project_unit_options |
| Default set name, or explicitly labeled SetCode, resolves to exactly one distinct set through the current-target resolver | Satisfied | Preserve the returned SetCode, SetName, and resolution basis | resolve_reference_set |
| Every requested related-business-unit addition has a distinct nonblank name | Satisfied | Include it unchanged for Fusion import validation | resolve_project_business_units |
| A requested relationship removal is marked nondeletable or has project/template use | Refused | Keep the relationship and report the usage gate | resolve_project_business_units |
| Set assignment mutation is requested | Refused | Route to Manage Project Unit Set Assignments as a separate task |  |
| Current export has no `PJF_REPORTING_SETUP` row for the project unit | Correction required before completion | Resolve explicit choices and apply UI defaults only to omitted fields per ora_defaulting_rules.md, generate the missing same-task row from the fresh target template, import it, and independently export/read back the row before downstream use | find_project_unit_options |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Project unit resolves exactly once | Accept; otherwise block | Every write or import | find_project_unit_options |
| Project unit is currently effective and classified PRJ_PROJECT_UNIT | Accept; otherwise block | Every write or import | find_project_unit_options |
| UserDefinedProjectNumCode resolves to AUTOMATIC or MANUAL | Resolve a code, meaning, translation, or unambiguous natural-language equivalent to the canonical code; otherwise reject | General properties |  |
| ManualProjectNumType resolves to ALPHANUMERIC or NUMERIC when UserDefinedProjectNumCode is MANUAL | Resolve a code, meaning, translation, or unambiguous natural-language equivalent to the canonical code; otherwise reject | Manual project-number entry |  |
| DefaultProjCurrCode resolves to one enabled, effective target currency | Resolve code, name, description, translation, or unambiguous business wording through the documented live resolver and retain the canonical CurrencyCode; otherwise reject | DefaultProjCurrCode is supplied for creation or change | resolve_project_currency |
| FteDay and FteWeek are persisted at scale two by round-down | Accept the normalized two-decimal value | General properties |  |
| An ordinary Default Set value resolves by exact SetName, or an explicitly labeled set code resolves by exact SetCode | Accept; otherwise follow the resolver's failure outcome | General properties are created or Default Set changes | resolve_reference_set |
| NumberingMethod resolves to MANUAL or AUTOMATIC | Accept; otherwise reject | Numbering is supplied |  |
| NumberType is Numeric or Alphanumeric | Require for Manual; reject unsupported values | NumberingMethod is Manual |  |
| NextNumber is a positive whole number | Require for Automatic; otherwise reject | NumberingMethod is Automatic |  |
| NextNumber does not conflict with another active determinant | Accept; otherwise block before preview | NumberingMethod is Automatic | find_project_unit_options |
| Every requested related-business-unit addition has a distinct nonblank name | Accept and defer Project Accounting eligibility to Fusion import | Related business units are supplied | resolve_project_business_units |
| CommitmentStatusExtr, CommitmentStatusReq, CommitmentStatusPo, and CommitmentStatusSupinv resolve to A, N, or R | Resolve a code, meaning, translation, or unambiguous natural-language equivalent to the canonical code; write A or R for an included type and N for an excluded type; otherwise reject | Reporting setup is supplied |  |
| StatusValue resolves to N for an unselected commitment type | Accept; otherwise reject contradictory input | Commitment is excluded from summarization |  |
| PlanamtAllocMethod resolves to D, E, or S | Resolve a code, meaning, translation, or unambiguous natural-language equivalent to the canonical code; otherwise reject | Allocation basis is supplied |  |
| A complete `PJF_REPORTING_SETUP` row exists for the project unit | Accept only when the fresh export has exactly one row with all required commitment statuses and allocation basis; otherwise block task completion and downstream plan-type/template use | New project unit, missing reporting row, or downstream plan-type/template use | find_project_unit_options |
| Supplied fields map to a proven member and runtime-validated column | Accept; otherwise reject the unsupported field | Import preview | verify_project_unit_options_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.VALIDATE_INPUT | step | 1 | validate_input | valid->PUOPT.FIND_PROJECT_UNIT;invalid->PUOPT.RETURN_ISSUES | none | stop | Every Manage Project Unit Options request |
| PUOPT.RESOLVE_BUSINESS_UNITS | step | 5 | validate_input | resolved->PUOPT.ROUTE_OPERATION;not_required->PUOPT.ROUTE_OPERATION;failure->PUOPT.RETURN_ISSUES | PUOPT.RESOLVE_SET | stop | Validate distinct nonblank business-unit names; additions defer eligibility to Fusion FSM import and removals retain usage/deletability gates |
| PUOPT.ROUTE_OPERATION | decision | 6 | evaluate_result | supported->PUOPT.RESOLVE_DEPENDENCIES;unsupported->PUOPT.RETURN_REFUSAL;invalid->PUOPT.RETURN_ISSUES | PUOPT.RESOLVE_BUSINESS_UNITS | stop | After project-unit, set, and business-unit resolution |
## Related Business Unit Validation

Fusion FSM import validates the business-unit relationship. Include additions unchanged in the immutable preview and retain any Fusion rejection as the task diagnostic.
