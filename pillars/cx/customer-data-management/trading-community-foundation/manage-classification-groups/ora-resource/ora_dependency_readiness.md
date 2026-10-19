# Dependency Readiness

Do not infer missing target dependencies from business values inside an
unchanged FSM task CSV package. Oracle's export can omit unmodified seeded
setup while retaining references to it, so absence from one CSV member is not
evidence that the target dependency is missing.

Official sources:

- [Add to the List of Available Industry Classification Categories](https://docs.oracle.com/en/cloud/saas/sales/fadsi/add-to-the-list-of-available-industry-classification-categories.html)
- [Export and import CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html)

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM package integrity | Preserve the complete package and its Oracle-defined business-object ordering; do not derive additional user confirmations from individual row values |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| fsm_package_dependencies | Business references contained in the exported task package | No separate preflight gate | An unchanged package passes task identity and archive validation | Not evaluated locally | Oracle-generated FSM package | | Package row values do not prove that a referenced seeded value is missing from the target | Do not request category-existence or privilege confirmation before preview; let the selected import workflow return an authorization or business-validation error if one exists | None |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Not evaluated locally | A complete unchanged task package contains business references | No; continue to immutable preview without requesting confirmation |
| Fusion rejection | The approved import later returns an authorization or business-validation error | No automatic retry; report the returned result and stop |
