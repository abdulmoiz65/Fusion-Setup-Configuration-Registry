# Payroll Costing Value Sets Reference Lookups

These are task-local evidence resolvers. They inspect the submitted package and consume the validated output of the declared shared reference-data workflow. They do not define a direct Fusion REST route, Value Set CRUD operation, or alternate import mechanism.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| inspect_task_csv_package_metadata | A package is exported, authored, validated, or imported | Sanitized package identity; ASM_SETUP_CSV_METADATA.xml; file manifest; headers; package release | Require exactly one task metadata record with ORA_PAY_PAYROLL_COSTING_VALUE_SETS, TASK, TASK_CSV_SERVICE, FND_APP_FLEX_VALUE_SET, LBA, and HcmPayCostTop; require the six exact file names and headers | Validated task identity; root business object; module scope; service metadata; release; file list | Block the package; do not repurpose a package from another task or release |
| verify_target_module_evidence | A root Value Set is created or modified | Target environment; package release; proposed ModuleId; sanitized result from shared reference-data validation | Require one passed target-evidence result whose target environment and applicable release match the operation record and whose ModuleId matches the proposed root row | Validated ModuleId; target-evidence reference; validation status | Block authoring; the observed 61ECAF4AAAEAE990E040449821C61C97 value is not portable evidence |
| resolve_parent_value_set_reference | A value row, Dependent model, or Subset model refers to a parent Value Set | Parent ValueSetCode; IndependentValueSetCode when supplied; submitted root and child rows; shared reference-data validation result | Match the exact code to one incoming root row or one passed target-reference result; reject a cyclic parent chain | Resolved parent ValueSetCode; Independent parent evidence; child-parent readiness | Block the affected row and request a valid Independent parent or target-reference result |
| verify_table_validation_source_evidence | A validation-table row or Table model is requested | Parent ValueSetCode; FromClause; value and optional ID, description, enabled, active-date, WHERE, ORDER BY, and alias fields; shared reference-data validation result | Require a passed validation result for the exact proposed source and target environment; preserve the task CSV fields without generating SQL | Validated table-source evidence; parent association; readiness | Block authoring; do not guess source SQL, aliases, or table semantics |
| resolve_related_value_pair | A related Value Set or mapping row is requested | ValueSetCode; ValueSetCode1; Value1; Value2; relationship state; submitted rows; shared reference-data validation result | Require exactly two resolved Independent Value Sets; require each mapping value in its validated member and a confirmed task-contract orientation | Resolved pair; mapping readiness; relationship-enable readiness | Block the relationship or mapping; do not swap the values or enable a new incomplete relationship |
| verify_value_set_security_evidence | SecurityEnabledFlag, DataSecurityObjectName, or a protected Value Set is involved | Root ValueSetCode; security fields; requested behavior; shared reference-data validation result | Require one passed result that confirms the security reference when applicable and confirms the Value Set is not protected for the requested mutation | Security readiness; protection status; permitted behavior | Block the mutation; protected Value Sets and their managed values are not editable |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The request has a target-environment reference result from the declared shared workflow | Consume its sanitized pass or fail result; do not perform a replacement direct lookup |
| A submitted package has no metadata, a different task identity, an incompatible scope, a missing CSV node, or a changed header | Stop package processing before generic export or import handling |
| A package evidence result is ambiguous | Stop and require a single validated result; do not choose a candidate automatically |
| A request requires a live Value Set lookup contract not declared here | Stop with the task boundary; route only through the declared shared reference-data workflow when it supplies an authorized contract |

## Contract Boundaries

| Contract Item | Status | Treatment |
|---|---|---|
| Target Payroll Costing module discovery API or query | TBD | This resource consumes the shared validator's sanitized target-evidence result; it does not invent a live query |
| Target Value Set and value discovery API or query | TBD | This resource consumes validated evidence only; it does not create a direct Value Set read or write route |
| Validation View Object authoring lookup | TBD | Block authoring until authoritative task metadata or successful target evidence supplies the contract |
| Direct generic Value Sets REST operation | Out of scope | Never use it as a task execution route; REST attribute documentation is supporting semantics only |

## Evidence Register

| Source ID | Title or Artifact | Exact URL or Supplied Identifier | Release or Date Used | Source Type | Used For |
|---|---|---|---|---|---|
| OHC-PAY-SETUP | Payroll Cost Allocation Key Flexfield Setup | https://docs.oracle.com/en/cloud/saas/human-resources/faipc/payroll-cost-allocation-key-flexfield-setup.html | Accessed 2026-08-19 | Oracle Help Center | Payroll Costing Value Set sequencing and Cost Allocation KFF use |
| OHC-PAY-REL | Payroll Cost Allocation Key Flexfield Structure | https://docs.oracle.com/en/cloud/saas/human-resources/fapus/payroll-cost-allocation-key-flexfield-structure.html | Accessed 2026-08-19 | Oracle Help Center | Existing or new sets, related-set rules, complete-combination validation, and redeployment |
| OHC-VS-OVERVIEW | Overview of Value Sets | https://docs.oracle.com/en/cloud/saas/applications-common/25c/oaext/overview-of-value-sets.html | 25c; accessed 2026-08-19 | Oracle Help Center | Validation models, protected Value Set restrictions, and deployment effects |
| OHC-VS-TYPES | Validation Type Options for Value Sets | https://docs.oracle.com/en/cloud/saas/applications-common/25c/oaext/validation-type-options-for-value-sets.html | 25c; accessed 2026-08-19 | Oracle Help Center | Format, Independent, Dependent, Subset, Table, range, security, and maintenance semantics |
| OHC-VS-PLAN | Considerations for Planning Value Sets | https://docs.oracle.com/en/cloud/saas/applications-common/25c/facia/considerations-for-planning-value-sets.html | 25c; accessed 2026-08-19 | Oracle Help Center | Data type, subtype, precision, scale, formatting, and security design semantics |
| OHC-VS-PROTECTED | Why can't I edit my flexfield or value set configuration? | https://docs.oracle.com/en/cloud/saas/human-resources/faucf/why-can-t-i-edit-my-flexfield-or-value-set-configuration.html | Accessed 2026-08-19 | Oracle Help Center | Protection explanation |
| OHC-FSM-BO | Business Objects for Moving Common Reference Objects | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/faicf/business-objects-for-moving-common-reference-objects.html | 25d; accessed 2026-08-19 | Oracle Help Center | Application Flexfield Value Set movement scope and redeployment consequence |
| OHC-FSM-CSV | Export and Import CSV File Packages | https://docs.oracle.com/en/cloud/saas/applications-common/25c/oafsm/export-and-import-csv-file-packages.html | 25c; accessed 2026-08-19 | Oracle Help Center | Template exports, package preservation, formatting, and result review |
| OHC-FSM-PROCESS | Key Information About Setup Data Export and Import Processes | https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/key-information-about-setup-data-export-and-import-processes.html | 26a; accessed 2026-08-19 | Oracle Help Center | Configuration package semantics, no-delete-by-omission, update behavior, import order, and process-result review |
| OHC-FSM-EXPORT | Setup Task CSV Exports REST Endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | 26c; accessed 2026-08-19 | Oracle Help Center | Supporting evidence that shared infrastructure supports task-level CSV export |
| OHC-FSM-IMPORT | Setup Task CSV Imports REST Endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | 26b; accessed 2026-08-19 | Oracle Help Center | Supporting evidence that shared infrastructure supports task-level CSV import |
| OHC-FSM-TEMPLATE | Setup Task CSV Template Exports REST Endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html | 26b; accessed 2026-08-19 | Oracle Help Center | Supporting evidence that shared infrastructure supports template export |
| OHC-RELATED-SUPP | Import Related Value Sets | https://docs.oracle.com/en/cloud/saas/financials/26a/fafcf/import-related-value-sets.html | 26a; accessed 2026-08-19 | Oracle Help Center | Supplemental relationship and mapping semantics only; not an execution route |
| SUP-TEMPLATE | Payroll Costing Value Sets_Template_20260819_051604_219.zip | User-supplied request excerpt | 11.13.26.10.0 | Task CSV evidence | Six file names and headers |
| SUP-EMPTY-EXPORT | Payroll Costing Value Sets_20260819_051301_313.zip | User-supplied request excerpt | 11.13.26.10.0 | Task CSV evidence | Empty normal export observation |
| SUP-TEST-EXPORT | Payroll Costing Value Sets_20260819_055604_135.zip | User-supplied request excerpt | 11.13.26.10.0 | Task CSV evidence | Observed ModuleId and Independent Character/Text test record |
| TARGET-EXPORT-300103767070301 | payroll-costing-value-sets_300103767070301.zip | project/draft-impl-project-20260819/exports/payroll/payroll-costing/payroll-costing-value-sets/payroll-costing-value-sets_300103767070301.zip | Observed 2026-08-19 | Target-environment task CSV evidence | Exact metadata flow TASK_CSV_SERVICE, task identity, scope, root object, service metadata, six files, headers, and FDOS test record |
| SUP-REQ | Generate resource files request | C:\\Users\\Joseph\\.codex\\attachments\\ca6d5e78-88bb-48ca-829e-661283505eba\\pasted-text.txt | 2026-08-19 | Developer-provided source | Task contract, metadata, schema excerpt, limits, and authoring gates |

The three ZIP files are referenced in the supplied request but are not present in the attachment directory available during authoring. Their stated contents are therefore retained as request-provided, release-specific evidence rather than independently re-inspected archive contents.
