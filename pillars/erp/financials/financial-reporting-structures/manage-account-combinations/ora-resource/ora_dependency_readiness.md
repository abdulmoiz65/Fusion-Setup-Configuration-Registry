# Manage Account Combinations Dependency Readiness

Dependencies establish package and import readiness. They do not authorize a Fusion mutation.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Candidate source | Normalize one supported source into rows that satisfy the 62-position contract. |
| 2 | Chart of accounts | Derive the COA identity from the candidate, resolve code first and natural-language name only as fallback, then retain the returned structure-instance number for the import handoff. |
| 3 | Package closure | Produce or accept only a verified GlBulkComboInterface.zip package with one GlBulkComboInterface.csv root member, preserving the delivered template column order. |
| 4 | Import handoff | Supply the verified package, structure-instance number, and import group to the approved FBDI execution workflow, which loads the interface file and runs Import Account Combinations. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| coa_identity | Exact enabled chart of accounts | Yes | Candidate needs COA metadata | Lookup | Fusion chartOfAccountsLOV | resolve_chart_of_accounts_from_candidate | The COA code and StructureInstanceNumber must correspond to the same enabled COA | Supply a candidate containing a CSV or ZIP position 1 value, or a natural-language COA identifier; do not select identity type separately | Chart of Accounts Code, StructureInstanceNumber, StructureInstanceId |
| package_contract | Verified FBDI package | Yes | Always | Verify | Candidate CSV or ZIP supplied in local task context |  | Oracle requires generated CSV data in a ZIP and requires the delivered template column order to remain unchanged | Supply a CSV or ZIP that meets the exact package, file, and row rules | Verified GlBulkComboInterface.zip and CSV hash |
| import_execution_contract | Approved FBDI execution route | Yes | Before any import | Blocked | Oracle account-combination import processing guidance, core.data-loader workflow, and current approval |  | Oracle loads the ZIP into the interface table before Import Account Combinations processes the selected chart of accounts and group | Route the verified package through the approved FBDI workflow and obtain approval immediately before the exact import | Target environment, package fingerprint, approval fingerprint, load request ID, chart of accounts, import group |
| import_registration_guidance | Oracle account-combination import registration guidance | Conditional | Before task readiness is asserted | Satisfied | Oracle Fusion Cloud Financials 26c, Import Account Combinations |  | The supplied Oracle guidance identifies the FBDI template, UCM account, scheduled process, and interface table | Reassess this dependency when the selected Fusion documentation release changes | Source reconciliation evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact required evidence is present and internally consistent | Read-only lookup only |
| Lookup | One documented read-only resolver can supply the value | Read-only lookup only |
| Blocked | Evidence, authority, approval, or a documented resolver contract is missing or ambiguous | No |

## Oracle Import Registration Source

Oracle Fusion Cloud Financials 26c, Import Account Combinations: https://docs.oracle.com/en/cloud/saas/financials/26c/oefbf/importaccountcombinations-3087.html

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-030-RESOLVE-DEPENDENCIES | decision | 30 | resolve_dependency | ready->MAC-040-APPLY-DEFAULTS;blocked->MAC-070-HANDLE-ERROR | MAC-020-RESOLVE-COA | stop | Always |
