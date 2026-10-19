# Design Enforcement

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate input shape | Confirm the analysis group and every supplied child analysis code satisfy the input contract. |
| 2 | Resolve current state | For an update or delete, resolve the exact existing record, all required live-template key fields, and any child or dependency state needed for the requested change. |
| 3 | Enforce analysis-code design | Confirm the submitted create, update, or delete design preserves record identity, supported Data Loader behavior, and exactly one default analysis code whenever child records remain. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new master and one or more child analysis-code records are supplied | Blocking | | The live create template does not support one parent row and child rows linked by the same unique `AnalysisGroupCode`, or the source does not use that linkage | Use one parent row first and the same `AnalysisGroupCode` in every child row. If the live template rejects this shape, stop before import and use the master-first fallback | Yes |
| Child analysis-code records are added to an existing master | Blocking | get_analysis_group | The parent `analysisGroupId` cannot be resolved, is not copied to every proposed child row, or the Data Loader source lacks that matching parent row | Resolve exactly one parent ID, include one parent row, and link every child row before preview | Yes |
| One or more child analysis-code records are supplied | Blocking | | A child row sets `RestAction` to CREATE | Keep child RestAction blank; Data Loader uses its supported MERGE behavior when a matching parent row is present | Yes |
| One or more child analysis-code records are supplied | Blocking | | Two child records in the same analysis group use the same AnalysisCode | Keep each analysis code unique within its analysis group | Yes |
| One or more child analysis-code records are supplied in the same master-and-children source | Blocking | | The proposed child records do not contain exactly one record with DefaultAnalysisCodeFlag set to Y | Add or correct child records so exactly one is the default for the AnalysisGroupCode | Yes |
| Child analysis-code records are added later | Blocking | get_cost_analysis_group_codes | The combined existing and proposed child records do not contain exactly one record with DefaultAnalysisCodeFlag set to Y | Retrieve all existing Cost Analysis Codes first, then add or correct Cost Analysis Code records so exactly one is the default for the AnalysisGroupCode | Yes |
| An existing master or child record is updated | Blocking | get_analysis_group | The exact existing record, required live-template key fields, or confirmed updateable fields are unavailable | Generate the live update sample, resolve the record, retain all required key fields, and populate only fields the live template permits | Yes |
| An update changes AnalysisGroupId, AnalysisGroupCode, or AnalysisCode identity | Blocking | get_analysis_group | The request treats an identity change as an update | Redesign the change as a reviewed delete-and-create operation; do not overwrite an existing record's identity | Yes |
| A child analysis-code record is deleted | Blocking | get_cost_analysis_group_codes | The exact parent and Cost Analysis Code identities are unresolved, the live delete template rejects the operation, or the resulting Cost Analysis Code set does not contain exactly one default | Use the live delete template, resolve the exact Cost Analysis Code, retrieve the complete current Cost Analysis Code set, and correct the resulting set before preview | Yes |
| An analysis-group master is deleted | Blocking | get_cost_analysis_group_codes | Any Cost Analysis Code record or dependent reference remains, dependency lookup is incomplete, or delete behavior is not confirmed by live metadata | Remove or rehome supported dependencies and confirm the master is empty before preparing a delete preview; never assume cascade deletion | Yes |
| An analysis code is reused in another analysis group | Informational | | None | Reuse is allowed when it supports a different analysis-group view of costs | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| get_analysis_group | Child rows are added to an existing master, or the live create template rejects create-together code linkage and the master-first fallback is selected | One resolved parent `analysisGroupId` for the supplied AnalysisGroupCode | ora_reference_lookups.md |
| get_cost_analysis_group_codes | A Cost Analysis Code record is added or deleted, or a master delete needs readiness confirmation | Every existing Cost Analysis Code and defaultAnalysisCodeIndicator; complete Cost Analysis Code-set result for the resolved group | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAG.ENFORCE_DESIGN | decision | 3 | design_enforcement | compliant->CAG.DONE_REVIEW;blocked->CAG.HANDLE_ISSUE | CAG.VALIDATE_INPUT; CAG.RESOLVE_PARENT for an existing parent or master-first fallback | stop | Create, update, or delete analysis-group master or child records through a live-template-supported Data Loader workflow; resulting child sets must retain exactly one default when children remain. |
