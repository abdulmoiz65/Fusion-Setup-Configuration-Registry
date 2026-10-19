# Input Validation

## CSV Column Intent Resolution

Resolve the requested target column before applying field validation or invoking a reference lookup. Interpret user language broadly using the intent below and surrounding request context; continue only when it identifies one CSV column. If two columns remain plausible, ask the smallest clarifying question rather than applying a value lookup to both.

| CSV Column | User Intent | Data Source |
|---|---|---|
| PJF_INSTALLATION.csv.Name | Business Unit being configured for Project Accounting | Financials Business Units LOV through `resolve_active_project_accounting_entity` |
| PJF_INSTALLATION.csv.ExpCycleStartDayCode | Costing: Expenditure Cycle Start Day | Static seeded `PJF_EXP_START_DAY` lookup |
| PJF_INSTALLATION.csv.CcProcessIoCode | Cross-Charge Options: Processing Method Within Business Unit | Static `N`/`B` cross-charge lookup |
| PJF_INSTALLATION.csv.CcDefaultRateDateCode | Cross-Charge Options: Transfer Price Currency Conversion: Date Type | Static seeded `PJF_BU_RATE_DATE` lookup |
| PJF_INSTALLATION.csv.CcProcessIuCode | Cross-Charge Options: Processing Method Between Business Units | Static `N`/`B` cross-charge lookup |
| PJF_INSTALLATION.csv.SamePaGlPeriod | Project Accounting periods: maintain common accounting and project accounting periods | Static `Y`/`N` flag set |
| PJF_INSTALLATION.csv.BookTypeCode | Asset integration: Default Asset Book | `fixedAssetBooksLOV` REST list |
| PJF_INSTALLATION.csv.DefaultRateDateCode | Costing Currency Conversion: Rate Date | Static seeded `PJF_BU_RATE_DATE` lookup |
| PJF_INSTALLATION.csv.RetProcessFlag | Asset integration: Enable retirement processing | Static `Y`/`N` flag set |
| PJF_INSTALLATION.csv.ExpTreeCode | Expenditure Organization Hierarchy: hierarchy identity | fndTrees REST response TreeCode through resolve_expenditure_tree; never inferred from any name |
| PJF_INSTALLATION.csv.ExpTreeStructureCode | Expenditure Organization Hierarchy: hierarchy structure | fndTrees REST response TreeStructureCode through resolve_expenditure_tree; never inferred from any name |
| PJF_INSTALLATION.csv.ProjTreeCode | Project and Task Owning Organization Hierarchy: hierarchy identity | fndTrees REST response TreeCode through resolve_project_tree; never inferred from any name |
| PJF_INSTALLATION.csv.ProjTreeStructureCode | Project and Task Owning Organization Hierarchy: hierarchy structure | fndTrees REST response TreeStructureCode through resolve_project_tree; never inferred from any name |
| PJF_INSTALLATION.csv.ExpTreeVersionName | Expenditure Organization Hierarchy: hierarchy version | FndTreeVersionVO REST exact unique ACTIVE/effective version check under returned ExpTreeCode through validate_expenditure_tree_version; never a code source |
| PJF_INSTALLATION.csv.ProjTreeVersionName | Project and Task Owning Organization Hierarchy: hierarchy version | FndTreeVersionVO REST exact unique ACTIVE/effective version check under returned ProjTreeCode through validate_project_tree_version; never a code source |
| PJF_INSTALLATION.csv.ProjStartOrgName | Project and Task Owning Organization Hierarchy: Start Organization or Top Organization | Exact projectOrganizationsLOV REST result through resolve_project_start_organization |
| PJF_INSTALLATION.csv.ExpStartOrgName | Expenditure Organization Hierarchy: Start Organization or Top Organization | Exact projectOrganizationsLOV REST result through resolve_expenditure_start_organization |
| PJF_INSTALLATION.csv.UserPeriodSetName | Project Accounting Calendar | `accountingCalendarsLOV` REST list |
| PJF_INSTALLATION.csv.UserConversionType | Costing Currency Conversion: Rate Type | `currencyConversionTypesLOV` REST list |
| PJF_INSTALLATION.csv.UserConversionType1 | Cross-Charge Options: Transfer Price Currency Conversion: Rate Type | `currencyConversionTypesLOV` REST list |
| PJF_BU_PU_RELATIONSHIP.csv.PJF_INSTALLATION.Name | Parent Business Unit being configured for Project Accounting | Financials Business Units LOV through `resolve_active_project_accounting_entity` |
| PJF_BU_PU_RELATIONSHIP.csv.Name | Project Units: related Project Unit | Fresh Project Unit relationship evidence through `resolve_active_project_accounting_entity` |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create_options, update, validate, export, import | Block | Ask for supported intent; enterprise-BU create/enable is separate | Every request |  |
| Business unit | Business-unit name or clear business wording resolved to one active Financials business unit | Block | Provide the business unit to configure | Every request | resolve_active_project_accounting_entity |
| BU function status | One active BU with Project Accounting enabled | Block | Correct the BU identity or enable Project Accounting separately | Every write | find_project_accounting_business_unit |
| Option scope | hierarchies, costing, periods, project_units, cross_charge | Preserve omitted groups | Ask only if change intent is ambiguous | Update/import | find_current_bu_options |
| Hierarchy details | Display Tree Name, supplied Tree Version Name, start organization, and same-as-owning flag | Block affected group | Supply complete owning and conditional expenditure triples; resolve each display Tree Name before checking its version | Hierarchy change | resolve_project_org_hierarchies |
| Target | TargetEnvironment | Block | Supply exact Fusion target | Every request | verify_bu_function_scope |
| Artifacts | current_export, package_template, reference snapshots, and feature_status | Block affected preview | Obtain current target evidence | Update/import | verify_bu_function_package |
| Current configuration date | Current target configuration date from the active workflow, used consistently for both hierarchies | Block affected hierarchy before lookup validation or ZIP generation | Resolve current target date context; do not silently substitute host date | Hierarchy creation/change | resolve_project_org_hierarchies |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| One active Project Accounting entity resolves exactly in its required role and context | Satisfied | Write the returned exact name to the applicable CSV field, then obtain the fresh task-export baseline | resolve_active_project_accounting_entity |
| One active BU has Project Accounting enabled | Satisfied | Continue with option baseline and applicable financial context | find_project_accounting_business_unit |
| Task row is absent and create_options requested | Satisfied | Create only missing implementation row | find_current_bu_options |
| Hierarchy triple resolves and start organization has the required classification | Satisfied | Preserve technical codes from the matching fndTrees response and the validated version name | resolve_project_org_hierarchies |
| Project-unit removal is unused and removable | Satisfied | Show the removal explicitly | resolve_project_unit_relationships |
| Project-unit removal is used downstream | Refused | Preserve the association | resolve_project_unit_relationships |
| Cross-charge prerequisites are incomplete | Blocked | Complete legal-entity, rate, and schedule setup | resolve_cross_charge_references |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Active Project Accounting entity resolves exactly once | Resolve business-unit and Project Unit roles through resolve_active_project_accounting_entity. Start organizations use the dedicated projectOrganizationsLOV role resolvers after tree/version resolution; require exact names and unique active effective OrganizationId, not a unique row count | Applicable supplied entity fields | resolve_active_project_accounting_entity |
| Active BU resolves exactly once and Project Accounting is enabled | Accept only one active enabled match; otherwise block | Every write | find_project_accounting_business_unit |
| Ledger, legal entity, currency, and accounting calendar are consistent | Accept only a single consistent financial context; otherwise block | Implementation-row creation or calendar/period, costing/conversion, or cross-charge change; not a relationship-only addition | resolve_bu_financial_context |
| Owning/expenditure tree resolves exactly once, its supplied version exists uniquely under it, and the start organization is uniquely resolved, active and classified | Accept only complete tree/version REST receipts and organization identity/classification evidence; otherwise block. Version validation requires an exact unique match with Status = ACTIVE and EffectiveStartDate <= current configuration date <= EffectiveEndDate; missing status/date fields, incomplete pagination or failed REST results block ZIP generation. Versions never supply technical codes. Missing independent membership proof is excluded from this input gate only when the available PABF export does not expose hierarchy membership; proven membership mismatches still block. Apply the membership warning from ora_design_enforcement.md | Hierarchy change | resolve_project_org_hierarchies |
| Hierarchy technical codes have REST provenance | Resolve each supplied display Tree Name first. ProjTreeCode and ProjTreeStructureCode must equal TreeCode and TreeStructureCode from the matching project fndTrees record; ExpTreeCode and ExpTreeStructureCode must equal those fields from the matching expenditure fndTrees record. Never derive, normalize, uppercase, or construct codes from a tree name, and never obtain a code from a version name. Reject missing or mismatched response provenance; preserve omitted groups. Reuse a verified tree response only for identical supplied tree names in the same target; otherwise resolve independently. | Hierarchy creation or change | resolve_project_org_hierarchies |
| Project Tree Name resolves exactly once | Require count = 1 after exact TreeName matching; map only returned TreeCode and TreeStructureCode unchanged | Project hierarchy creation or change | resolve_project_tree |
| Project Tree Version Name exists under its resolved tree | Require count = 1 for the exact supplied TreeVersionName under returned ProjTreeCode, Status = ACTIVE and inclusive effective-date bounds covering the current configuration date; stop for zero/ambiguous matches, non-ACTIVE status, ineffective date range, missing fields or failed/incomplete REST results before ZIP generation; no technical-code mapping | Project hierarchy creation or change | validate_project_tree_version |
| Expenditure Tree Name resolves exactly once | Require count = 1 after exact TreeName matching; map only returned TreeCode and TreeStructureCode unchanged | Expenditure hierarchy creation or change | resolve_expenditure_tree |
| Expenditure Tree Version Name exists under its resolved tree | Require count = 1 for the exact supplied TreeVersionName under returned ExpTreeCode, Status = ACTIVE and inclusive effective-date bounds covering the current configuration date; stop for zero/ambiguous matches, non-ACTIVE status, ineffective date range, missing fields or failed/incomplete REST results before ZIP generation; no technical-code mapping | Expenditure hierarchy creation or change | validate_expenditure_tree_version |
| Project calendar, copied-period state, and common-period choice are compatible with the ledger | Accept only when a different project calendar is enabled with the required period state, or `SamePaGlPeriod=Y` uses ledger-compatible common periods; otherwise block | Calendar or period change | resolve_project_calendar |
| Expenditure cycle start day resolves to one current enabled PJF_EXP_START_DAY value | Interpret the user's business wording against the complete valid lookup set and write only the resolved LookupCode to ExpCycleStartDayCode; block no valid result, multiple plausible results, or a disabled or ineffective result | An expenditure cycle start day is supplied or changed | resolve_expenditure_cycle_start_day |
| Cross-charge processing method within business unit resolves to one valid value | Resolve the supplied code, UI label, meaning, translation, description, or business wording to N (None) or B (Borrowed and lent). Processing Method Within Business Unit, within business unit, within BU, and internal business-unit cross-charge aid column selection; they do not restrict accepted value wording. | CcProcessIoCode is supplied | resolve_cross_charge_within_bu_process_code |
| Cross-charge default rate date resolves to one current enabled PJF_BU_RATE_DATE value | Interpret the user's business wording against the complete valid lookup set and write only the resolved LookupCode to CcDefaultRateDateCode; block no valid result, multiple plausible results, or a disabled or ineffective result | CcDefaultRateDateCode is supplied | resolve_rate_date_code |
| Cross-charge processing method between business units resolves to one valid value | Resolve the supplied code, UI label, meaning, translation, description, or business wording to N (None) or B (Borrowed and lent). Processing Method Between Business Units, between business units, between BUs, and cross-business-unit cross-charge aid column selection; they do not restrict accepted value wording. | CcProcessIuCode is supplied | resolve_cross_charge_between_bu_process_code |
| SamePaGlPeriod resolves to Y or N | Interpret affirmative or negative user wording and write only Y or N; reject blank, contradictory, indeterminate, or ambiguous intent | Every PJF_INSTALLATION row | resolve_yes_no_flag |
| Asset book resolves to one effective corporate asset book returned by the documented lookup endpoint | Interpret the supplied business value against the complete returned book set and write only the resolved BookTypeCode; reject a tax book, ineffective book, no valid result, or multiple plausible results | BookTypeCode is supplied | resolve_default_asset_book |
| Default rate date resolves to one current enabled PJF_BU_RATE_DATE value | Interpret the user's business wording against the complete valid lookup set and write only the resolved LookupCode to DefaultRateDateCode; block blank, no valid result, multiple plausible results, or a disabled or ineffective result | Every PJF_INSTALLATION row | resolve_rate_date_code |
| RetProcessFlag resolves to Y or N | Interpret affirmative or negative user wording and write only Y or N; reject blank, contradictory, indeterminate, or ambiguous intent | Every PJF_INSTALLATION row | resolve_yes_no_flag |
| Accounting-calendar input resolves to one accounting calendar returned by the documented lookup endpoint | Accept either the user-defined calendar name (`UserPeriodSetName`) or the internal calendar code (`PeriodSetName`) as input. Query the corresponding exact queryable REST attribute, require one de-duplicated `CalendarId` across either query, write the returned `UserPeriodSetName` to the CSV, and retain the name, code, and IDs in the receipt; reject no valid result or multiple plausible results. | UserPeriodSetName is supplied or changed | resolve_accounting_calendar |
| Costing Currency Conversion rate-type input resolves to one currency conversion type returned by the documented lookup endpoint | Interpret the supplied business value against the complete returned rate-type set, write the target UserConversionType, and retain its stable ID; reject no valid result or multiple plausible results | UserConversionType is supplied or changed | resolve_currency_conversion_type |
| Cross-Charge Options Transfer Price Currency Conversion rate-type input resolves to one currency conversion type returned by the documented lookup endpoint | Interpret the supplied business value against the complete returned rate-type set, write the target value to UserConversionType1, and retain its stable ID; reject no valid result or multiple plausible results | UserConversionType1 is supplied or changed | resolve_currency_conversion_type |
| Every project-unit addition or removal resolves and every removal is unused | Accept only when each named change has sufficient relationship and usage evidence; otherwise block the named item | Relationship change | resolve_project_unit_relationships |
| Cross-charge method and receiver overrides satisfy prerequisites | Accept only when legal-entity, rate, and schedule prerequisites are complete; otherwise block | Cross-charge change | resolve_cross_charge_references |
| Fields map to exact target-validated package contract | Accept; else reject | Import preview | verify_bu_function_package |
| PA period type and expenditure-cycle start day are populated and valid | Accept; else reject | Period/costing change | resolve_costing_references |
| ProjStartOrgName has one active effective identity with PROJECTS | Require complete exact-name REST results, exactly one eligible OrganizationId after de-duplication, and an active effective PROJECTS row. Reject missing role, zero/multiple identities, inactive/ineffective rows, malformed fields, incomplete pagination or REST failure before ZIP generation | Supplied ProjStartOrgName for hierarchy creation/change | resolve_project_start_organization |
| ExpStartOrgName has one active effective identity with EXPENDITURES | Require complete exact-name REST results, exactly one eligible OrganizationId after de-duplication, and an active effective EXPENDITURES row. Reject missing role, zero/multiple identities, inactive/ineffective rows, malformed fields, incomplete pagination or REST failure before ZIP generation | Supplied ExpStartOrgName for hierarchy creation/change | resolve_expenditure_start_organization |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUFUNC.RESOLVE_COLUMN_INTENT | step | 1 | validate_input | resolved->BUFUNC.VALIDATE_INPUT;invalid->BUFUNC.RETURN_ISSUES | none | stop | Before input validation or any reference lookup for a supplied CSV value |
| BUFUNC.VALIDATE_INPUT | step | 2 | validate_input | valid->BUFUNC.APPLY_DEFAULTS;invalid->BUFUNC.RETURN_ISSUES | BUFUNC.RESOLVE_COLUMN_INTENT | stop | Every Configure Project Accounting Business Function request |
| BUFUNC.FIND_BUSINESS_UNIT | step | 4 | validate_input | valid->BUFUNC.FIND_BASELINE;invalid->BUFUNC.RETURN_ISSUES | BUFUNC.APPLY_DEFAULTS | stop | Require one active BU with Project Accounting enabled and match its Name in the fresh task export |
| BUFUNC.FIND_BASELINE | step | 5 | validate_input | valid->BUFUNC.RESOLVE_OPTIONS;invalid->BUFUNC.RETURN_ISSUES | BUFUNC.FIND_BUSINESS_UNIT | stop | Resolve the current implementation row from the fresh task export |
| BUFUNC.ROUTE_OPERATION | decision | 13 | evaluate_result | supported->BUFUNC.RESOLVE_DEPENDENCIES;unsupported->BUFUNC.RETURN_REFUSAL;invalid->BUFUNC.RETURN_ISSUES | BUFUNC.RESOLVE_EXPENDITURE_START_ORGANIZATION | stop | After business-unit, option, and applicable hierarchy REST resolution |

## Refined Required Evidence

- **BP-002 — Required evidence:** For every business unit using different periods, capture the justification; complete calendar and period definitions; active open/close ownership; reconciliation from project periods to GL months; and transaction, costing, billing, revenue, and accounting cutoffs.
