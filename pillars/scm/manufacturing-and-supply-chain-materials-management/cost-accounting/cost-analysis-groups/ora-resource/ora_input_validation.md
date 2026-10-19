# Input Validation

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Developer-provided REST payload example for `costAccountingCostAnalysisGroups`

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, update, or delete; target level (master or detail) | Stop | Identify the requested operation and target level; allow update/delete only if the live Data Loader template and validation accept it | Always | |
| Analysis group identity | AnalysisGroupCode | Stop | Provide an analysis group code before preparing the Data Loader source | Always | |
| Existing-record identity | Resolved analysisGroupId and every live key field from the update/delete template | Stop | Resolve the exact existing master and use the live Data Loader key-fields workbook; do not infer keys | Update or delete | get_analysis_group |
| Analysis-code identity | costAccountingCostAnalysisCodes[].AnalysisCode | Stop | Provide an analysis code for every supplied child code record | One or more child analysis-code records are supplied | |
| Analysis-code parent link | For a create-together load, the same unique `AnalysisGroupCode` in one parent row and every child row, as accepted by the live Data Loader template; for an existing parent, resolved `analysisGroupId` copied to one parent row and every child row | Stop | Generate the live create template before source preparation. Use code linkage for a new master only when that template accepts it; otherwise use the master-first fallback. Do not prepare an orphan child-only source | One or more child analysis-code records are supplied | get_analysis_group (existing parent only) |
| Default analysis-code selection | Exactly one child record with DefaultAnalysisCodeFlag set to `Y` after combining existing, created, updated, and deleted child records; every serialized flag is the string literal `Y` or `N` | Stop | Normalize functional `Yes`/`True` to `Y` and `No`/`False` to `N`, then correct the resulting child-code set if needed | One or more child analysis-code records are supplied, changed, or deleted | get_cost_analysis_group_codes |
| Master deletion readiness | No child records or dependent references, as confirmed by complete read-only lookups and live metadata | Stop | Remove or rehome supported dependencies, then revalidate; never assume cascade delete | Master delete | get_cost_analysis_group_codes |

## Functional User Prompts

| Business Question | Information Captured | Applies When |
|---|---|---|
| Do you want to create, update, or delete a master or detail record? | Operation and target level | Always |
| What is the analysis group code you want to create, update, or delete? | AnalysisGroupCode | Always |
| What description should appear for this analysis group? | AnalysisGroupDescription | Always |
| Are you creating the group only, creating it with analysis codes, or adding analysis codes to an existing group? | Request mode and whether existing children must be retrieved | Always |
| For each analysis code, what code and description should be used? | costAccountingCostAnalysisCodes[].AnalysisCode and description | One or more child analysis codes are created or updated |
| Which one analysis code should be the default after the change? | DefaultAnalysisCodeFlag selection | One or more child analysis codes are created, updated, or deleted while children remain |
| For a delete, confirm the exact record identity and later approve the immutable deletion preview. | Existing key fields and explicit approval | Update or delete |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|
| AnalysisGroupDescription is supplied or omitted | Defer mandatory and optional behavior to live Data Loader metadata; the provided source does not define that field contract | Always | |
| costAccountingCostAnalysisCodes is omitted | Continue; the user may create only the analysis group and add analysis codes later | The child collection is blank or absent | |
| DefaultAnalysisCodeFlag is supplied | Confirm the live Data Loader metadata, then require the serialized source value to be the string literal `Y` or `N`. Normalize `Yes`/`True` to `Y` and `No`/`False` to `N`; reject values outside these supported representations | A child analysis-code record supplies DefaultAnalysisCodeFlag | |
| Generated child source is ready for preview | Inspect every populated DefaultAnalysisCodeFlag value in the generated workbook/DAT source; allow preview only when all are exactly `Y` or `N` | One or more child analysis-code records are supplied | |
| Group and child records are created together | Validate the proposed child records for the AnalysisGroupCode; exactly one record must have DefaultAnalysisCodeFlag set to Y | The master and one or more children are in the same source | |
| New parent and child rows are created together | Require one parent row followed by child rows with the same unique `AnalysisGroupCode`, and verify this code-based linkage against the live create template | A new master and one or more child analysis-code records are supplied | |
| Existing parent and child rows include AnalysisGroupId | Require one resolved, nonblank `AnalysisGroupId`, one matching parent row, and require every proposed child row to use that same value | Child analysis-code records are added to an existing master | get_analysis_group |
| Child RestAction is blank | Use the supported Data Loader MERGE behavior; do not set child RestAction to CREATE | One or more child analysis-code records are supplied | |
| Live create template rejects code-based linkage | Stop before import and use the master-first fallback: create the master, resolve it by exact `AnalysisGroupCode`, then prepare a separate parent-plus-children source | The master and children are requested together | get_analysis_group |
| Child records are added to an existing AnalysisGroupCode | Retrieve the existing parent and Cost Analysis Codes, combine them with the proposed Cost Analysis Codes, and require exactly one record with DefaultAnalysisCodeFlag set to Y | The source adds Cost Analysis Codes without creating the master | get_cost_analysis_group_codes |
| An existing master or child is updated | Generate the live update sample, resolve the existing record, retain all live key fields, and populate only confirmed updateable fields; retain the child RestAction required by the live template | Update | get_analysis_group |
| A child identity is changed | Treat the request as delete-and-create; do not overwrite the existing AnalysisCode or parent identity | Update request changes AnalysisCode or AnalysisGroupId | get_analysis_group |
| A detail record is deleted | Generate the live delete sample, stop if live validation rejects the action, resolve its exact parent and Cost Analysis Code identities, and validate the complete resulting Cost Analysis Code set has exactly one default | Detail delete | get_cost_analysis_group_codes |
| A master record is deleted | Generate the live delete sample, stop if live validation rejects the action, and block unless complete read-only checks confirm no Cost Analysis Code rows or dependent references; never infer cascade behavior | Master delete | get_cost_analysis_group_codes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAG.VALIDATE_INPUT | decision | 1 | validate_input | create_together->CAG.ENFORCE_DESIGN;existing_parent_or_fallback->CAG.RESOLVE_PARENT;invalid->CAG.HANDLE_ISSUE | none | stop | Create an analysis-group master and its child analysis codes together, or validate a live-template-supported update or delete request |
