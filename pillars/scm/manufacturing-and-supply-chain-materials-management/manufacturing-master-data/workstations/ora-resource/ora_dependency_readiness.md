# Workstations FSM Dependency Readiness

## Source Evidence

| Source | Verified Fact | Source Anchor |
|---|---|---|
| Authoring skills for resources using FSM import/export | An import ZIP must be prepared only from a newly fetched live template. A static or previously downloaded template must not substitute for the target-environment template. Validate ZIP contents, filenames, directory structure, and manifest requirements before import. Import requires explicit approval after package validation. | [Authoring skills for resources using FSM import/export](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21459835549), Step 2 — Author Task Resources |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Validated Workstations input | Validate available Workstations fields before any package preparation. |
| 2 | Fresh live Workstations template | Fetch a new `ORA_WIS_WORKSTATIONS` template from the target Fusion environment. |
| 3 | Prepared FSM ZIP | Change only the newly fetched template's documented data files and preserve its required layout. |
| 4 | Package validation | Validate ZIP contents, filenames, directory structure, and manifest requirements. |
| 5 | Explicit approval | Obtain explicit approval for the exact validated package before a Fusion import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| WORKSTATIONS.FRESH_TEMPLATE | Fresh target-environment Workstations template | Yes | Before any FSM ZIP is prepared | Verify | Read-only Fusion setup-task CSV template export |  | Prevents an import package from using stale or static layout metadata. | Fetch a new template for the target environment and task code `ORA_WIS_WORKSTATIONS`. | Fresh export archive and fetch time |
| WORKSTATIONS.PACKAGE_FROM_TEMPLATE | ZIP prepared from the fresh template | Yes | Before package validation | Verify | Fresh template plus validated Workstations input |  | Keeps CSV names, ZIP layout, and manifest aligned with the target environment. | Use the fresh template as the only package base; do not substitute a prior or sample ZIP. | Prepared ZIP path and changed-file list |
| WORKSTATIONS.PACKAGE_LAYOUT | ZIP layout validation | Yes | Before approval or import | Verify | Prepared ZIP |  | Detects altered filenames, folders, or manifest requirements before import. | Validate ZIP contents, filenames, directory structure, and manifest requirements. | Validation result |
| WORKSTATIONS.IMPORT_APPROVAL | Explicit approval for the exact validated ZIP | Yes | Immediately before a Fusion import | Verify | Authorized approver |  | A validated package is still not authorized to change Fusion without approval. | Obtain approval that identifies the exact validated package. | Approval record and package identity |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WORKSTATIONS.FSM_PREPARE | step | 15 | resolve_dependency | ready->WORKSTATIONS.DESIGN_CREATE_CONTRACT;missing->WORKSTATIONS.RETURN_ISSUES | WORKSTATIONS.VALIDATE_DOCUMENTED_HEADERS | stop | Before an FSM Workstations package is prepared or imported. |
