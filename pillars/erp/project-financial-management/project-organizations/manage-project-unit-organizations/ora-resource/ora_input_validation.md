# Input Validation

Source: developer-provided FSCR input specification, sections 1–7 and 9.
Tenant findings are supplied evidence, not independently retested here.

A later explicit request for status, progress, results, counts or errors uses
the registered project acceptance binding: accepted Request ID, same target/task,
approved archive hash and approval reference. Load it from the selected project;
chat history or a supplied request ID alone is insufficient.
Validate that binding and take `status_requested` directly to
PUORG.STATUS_REQUEST_GATE. Missing or conflicting context blocks. New-load name/code, lookup,
defaulting, package-generation and approval checks below apply to preparation
requests; do not repeat them or submit another load on this resume route.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested organization identity | ProjectUnitName or ExistingOrganizationName as one requested organization name | Block | Supply one nonblank name up to 240 characters; the organization search derives the action | Every request | find_active_organization |
| Project Unit code | User-supplied or explicitly accepted ProjectUnitCode | Block | Offer a name-derived suggested code or manual entry; for bulk input, show every missing row and suggestion together and collect all choices in one request | Every row | |
| New identity | ProjectUnitName normalized from the requested name | Block | Bind the searched name after DerivedAction is CREATE_NEW | DerivedAction = CREATE_NEW | find_active_organization |
| Existing identity | ExistingOrganizationName and OrganizationId selected during lookup | Block | Preserve the exact returned name and select the exact organization and parent classification record | DerivedAction = USE_EXISTING_ORGANIZATION | find_active_organization |
| Existing classification label | Selected ClassificationCode and exact organizationClassificationsLOV display label | Block | Resolve the selected returned code to exactly one LOV row before generation | DerivedAction = USE_EXISTING_ORGANIZATION | resolve_organization_classification |
| Target and evidence | TargetEnvironment; fresh target-bound lookup evidence | Block | Resolve project environment and evidence | Every request | verify_project_unit_setup_scope |
| Durable project handoff | project_id, safe unused receipt location, artifact registration, run-record and token-log paths; registered acceptance binding for resume | Block submission or resume | Use declared core project services and ora_dependency_readiness.md#execution-persistence-and-resume-contract; reconcile missing local evidence without submitting again | Every request | verify_project_unit_setup_scope |
| Package | One Organization.dat in a ZIP | Block import | Generate after all lookup gates pass | Import | verify_project_unit_package_contract |
| Bulk rows | Ordered rows with one requested name per row and complete target-bound resolver evidence per row | Block all archives | Report every row number and issue together; resolve all rows before packaging | Bulk request | find_active_organization |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Organization routing evidence is complete | Valid only when find_active_organization returns a derived action or a documented terminal outcome | Continue through PUORG.ROUTE_OPERATION; do not accept an input action | find_active_organization |
| Existing-organization selection is required | Valid only when the resolver binds the exact returned organization and parent classification record | Continue only with the resolver-selected identity | find_active_organization |
| Existing-organization classification is selected | Valid only when organizationClassificationsLOV returns exactly one row for the selected returned ClassificationCode and its label agrees with any returned organization label | Bind ResolvedOrganizationClassification before defaults or generation | resolve_organization_classification |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Action is a derived workflow output, not a normal user input | Do not request or trust a user-selected action; remove it from normalized user input and derive it only from organization-search evidence | Every request | find_active_organization |
| ProjectUnitCode is required as a nonblank string up to 150 characters | Preserve the chosen code exactly; a name-derived suggestion may be shown but must not be used without explicit acceptance; do not impose an unverified regex; use configured value-set validation when available | Both actions | |
| ProjectUnitName and ExistingOrganizationName are strings up to 240 characters | Use the one supplied requested name for the initial exact search; after routing preserve returned intentional whitespace for an existing organization | Every request | find_active_organization |
| ExistingClassification is an optional code or label; ExistingLocation is an optional name | Resolve exact selected classification record and LocationId; resolve the selected returned code's display label through organizationClassificationsLOV | Existing action | resolve_organization_classification |
| Supplied dates use valid calendar YYYY/MM/DD, including year 0001 | Reject other formats, impossible dates and end before start | Both actions | |
| HDL names, classifications and codes contain no raw pipe, newline, backslash or control characters | Block serialization until a supported escaping contract is available; do not silently sanitize supplied values | Both actions | |
| Exact action-specific headers, order, row count, lengths, constants, parent references and dates | Run scripts/validate_project_unit_organization_hdl.py with expected action | Generated ZIP | verify_project_unit_package_contract |
| Bulk organization names and supplied Project Unit codes are unique within the request | Flag every conflicting row; generate no archive until corrected | Bulk request | |
| Bulk rows use one metadata layout per component and one MERGE per organization | Group by derived action; produce separate ZIPs for new and existing rows because their headers/order differ; never discard invalid rows or import a valid subset | Bulk request | verify_project_unit_package_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.VALIDATE_INPUT | step | 1 | validate_input | valid->PUORG.FIND_ORGANIZATION;status_requested->PUORG.STATUS_REQUEST_GATE;invalid->PUORG.RETURN_ISSUES | none | stop | For preparation validate every row and the whole batch; for a later explicit status request validate the retained same-target task/request and approved archive binding, then resume without discovery, generation or submission |
