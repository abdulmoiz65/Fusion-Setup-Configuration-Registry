# Legal Entity HCM Information Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation
routing for Manage Legal Entity HCM Information. Loader templates and DAT
construction remain owned by the task skill and Core Data Loader.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Legal Entity identity | Legal Entity Name or LegalEntityIdentifier | MISSING | Request one business identifier | Every request | find_legal_entity_exact |
| Operation | Get, Edit, correction, dated update, end date, multirow child removal, date-effective delete, CSV Export, or CSV Import | MISSING | Request one supported intent | Every request |  |
| Mutation target | Legal Employer, Payroll Statutory Unit, or both; business category; context; segment changes | MISSING | Present only applicable business-facing branches and context labels after reads | Every EFF mutation | resolve_legal_entity_eff_metadata |
| Effective boundary | Unambiguous EffectiveStartDate or applicable end date | MISSING | Show current Basic details and effective range, then request the intended date | Every date-effective mutation | resolve_legal_entity_hcm_roots |
| Multirow selection | Exact selected child row | MISSING | Present sanitized row choices and require one exact selection | Multirow child removal | resolve_legal_entity_eff_context |
| Delete scope | Latest eligible current HCM Information change | MISSING | Explain that the Legal Entity remains and show only the eligible range | Date-effective delete | resolve_legal_entity_hcm_history |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Advanced search returns one exact record | Valid | Continue to synchronization readiness using only the fresh result | find_legal_entity_exact |
| Search returns zero or multiple exact records | Blocked | Request a unique Name or LegalEntityIdentifier | find_legal_entity_exact |
| LegalEmployerFlag is Y | Legal Employer branch applies | Resolve legalEmployers and its EFF envelope | resolve_legal_entity_hcm_roots |
| PsuFlag is Y | Payroll Statutory Unit branch applies | Resolve payrollStatutoryUnits and its EFF envelope | resolve_legal_entity_hcm_roots |
| Both flags are Y | Both branches apply | Resolve independently and preserve legalEmployersEFF, payrollStatutoryUnitsEFF order for mutation handoff | resolve_legal_entity_hcm_roots |
| A supported mutation is requested | Loader contract required | Validate every selected object and current UCM template before handoff | resolve_legal_entity_loader_contract |
| CSV Export is requested | Export route | Use the shared task-level export workflow |  |
| CSV Import is requested | Loader route | Validate source and route through Core Data Loader | resolve_legal_entity_loader_contract |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Identity | Trim whitespace and require one exact normalized Name or identifier match | Every request | find_legal_entity_exact |
| Read effective date | Use today's system date when omitted. When supplied, require an unambiguous YYYY-MM-DD value and retain only the `q=LegalEntityId` root row whose returned effective range covers it | Get | resolve_legal_entity_hcm_roots |
| Classification flags | Treat LegalEmployerFlag and PsuFlag as read-only routing facts | Every request | find_legal_entity_exact |
| Parent fields | Reject Name, Status, classification, and every other parent change | Every mutation |  |
| EFF attribute | Accept only a selected-context attribute identified as writable by current exact metadata | Edit or update | resolve_legal_entity_eff_metadata |
| Effective boundary | Reject a mutation date earlier than any affected top-level organization's current EffectiveStartDate | Every date-effective mutation | resolve_legal_entity_hcm_roots |
| Correction | When the requested operation EffectiveStartDate equals the affected top-level organization's current EffectiveStartDate, use `effectiveOf=RangeMode=CORRECTION;RangeStartDate=YYYY-MM-DD` and include ModifyOrganizationUnitForChildCorrect with the affected EFF branch, including when the EFF child row is new | Edit | resolve_legal_entity_hcm_roots |
| Date-effective update | When the requested operation EffectiveStartDate is later than the affected top-level organization's current EffectiveStartDate, existing rows require `effectiveOf=RangeMode=UPDATE;RangeStartDate=YYYY-MM-DD`; a new POST child requires `effectiveOf=RangeStartDate=YYYY-MM-DD` without RangeMode. Include SplitOrganizationUnitForEFFUpdate with every affected EFF branch, including a member whose EFF child row is new | Edit | resolve_legal_entity_hcm_roots |
| LE DAT date normalization | Normalize every populated date-only DAT value to ISO `YYYY-MM-DD` during task payload preparation, including action dates and `effectiveOf` RangeStartDate. Reject a source containing a date-only `YYYY/MM/DD` value; do not transform timestamps or datetimes | Every Data Loader upload | resolve_legal_entity_loader_contract |
| Changed values | Retain only explicitly requested segments whose normalized requested value differs from the fresh current value | Edit or update | resolve_legal_entity_eff_context |
| Multirow removal | Require a describe-confirmed multirow context and one exact selected child | Child removal | resolve_legal_entity_eff_context |
| Date-effective delete | Allow only the latest eligible current change; reject historical, future, first/only, complete, or user-selected older deletion | Date-effective delete | resolve_legal_entity_hcm_history |
| Value set | Resolve one exact enabled stored/display value | A changed segment declares a value set | resolve_legal_entity_eff_value_set |
| Loader object | Select legalEmployersEFF, payrollStatutoryUnitsEFF, or both strictly from affected applicable branches for EFF work; pair them with ModifyOrganizationUnitForChildCorrect for a correction or SplitOrganizationUnitForEFFUpdate for a dated update; select only DeleteOrganizationUnitForDTDelete for a date-effective parent-row delete | Every mutation | resolve_legal_entity_loader_contract |
| EFF root controls and locators | Require FLEX:PER_ORGANIZATION_INFORMATION_EFF, EFF_CATEGORY_CODE, OrganizationId, OrgUnitClassificationId, OrganizationEffectiveStartDate, OrgUnitClassEffectiveStartDate, and OrgUnitClassEffectiveEndDate in every selected EFF root header when required by the current live template. For every context row, set the `FLEX:PER_ORGANIZATION_INFORMATION_EFF` value to that row's resolved context code, not the literal flexfield identifier | Every EFF mutation | resolve_legal_entity_loader_contract |
| Existing and new EFF children | An existing child uses its current OrgInformationId, EffectiveStartDate, and EffectiveEndDate exactly as returned by the fresh selected context row, with `RestAction=PATCH`. A new child must omit child OrgInformationId, EffectiveStartDate, and EffectiveEndDate and use `RestAction=POST`; in a dated-update branch it must include `effectiveOf=RangeStartDate=YYYY-MM-DD` without RangeMode. Keep blank action OrgInformationId, and do not let child state change the selected correction/update mode | Every EFF row | resolve_legal_entity_loader_contract |
| Embedded action controls | For ModifyOrganizationUnitForChildCorrect, require blank dummyId, blank OrgInformationId, `RestAction=invoke`, ISO StartDate, and the resolved OrganizationId in the current template order. For SplitOrganizationUnitForEFFUpdate, validate the current template and populate every required action field, including ISO effectiveStartDate and resolved organizationId when required | Every correction or dated update | resolve_legal_entity_loader_contract |
| Loader operation | Require the requested root/action structure in the current selected-object template; do not copy another object's action contract | Every mutation | resolve_legal_entity_loader_contract |
| Technical delete contract | Use only `DeleteOrganizationUnitForDTDelete` with `RestAction=POST`, the current `Content-Type` application/vnd.oracle.adf.action+json, and current `REST-Framework-Version` metadata | Date-effective delete | resolve_legal_entity_loader_contract |
| Source evidence | Treat a source document as request evidence only; it never supplies mutation approval | Document-derived request |  |
| Multi-record conflicts | Reject duplicate targets, conflicting effective dates, ambiguous multirow selections, and inconsistent branch scope before loader handoff | Change table or multi-record input |  |
| Multi-record isolation | Resolve identity, OrganizationId, branch facts, CategoryCode, context rows, value sets, and effective boundaries independently for every Legal Entity | Change table or multi-record input |  |
| Export preservation | Preserve unrelated setup objects and values in an explicit task export package | CSV Export |  |
| Output | Show Basic details once, then business categories, contexts, segment labels, and display values. Preserve describe-backed zero-row contexts with segment values Not configured | Every successful read or verification | resolve_legal_entity_eff_metadata |
| End of Time | Render any terminal 4712 end date as End of Time | Every user-facing result |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.VALIDATE | decision | 1 | validate_input | valid->LE.SEARCH;csv_export->LE.EXPORT_DONE;missing->LE.ERROR;invalid->LE.ERROR;unsupported->LE.BLOCKED | none | stop | Every Manage Legal Entity HCM Information request |
