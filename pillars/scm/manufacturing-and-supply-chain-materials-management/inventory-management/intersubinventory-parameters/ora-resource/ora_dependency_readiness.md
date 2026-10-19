# Intersubinventory Parameters Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| User confirmation | Provenance that external BO registration is complete for `interSubinventoryParameters`; it does not establish runtime readiness |
| Live configured-target Data Loader metadata check | BO visibility, sample support, mandatory attributes, and key attributes for that selected environment and run |
| Per-run Data Loader metadata preflight | Revalidation before every Data Loader preparation; prior successful results are not reusable |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader business-object metadata | Complete a read-only current-run preflight for exact BO discriminator `interSubinventoryParameters` in the selected environment; confirm visibility, sample support, mandatory attributes, and key attributes |
| 2 | BO-owned organization and subinventory references | Leave organization and subinventory resolution to the registered BO and Data Loader; do not invoke a task-local REST resolver |
| 3 | Approved standard lookups | Resolve only Destination Type, Transfer Type, and Receipt Routing when their documented code or meaning field is supplied |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| intersubinventory_parameters_bo | Data Loader business-object metadata | Yes | Before `core.data-loader` prepares Intersubinventory Parameters data | Required for current run only | Read-only metadata preflight in selected environment |  | Registration, visibility, sample support, mandatory attributes, and keys can vary by environment or release | Record selected environment, exact discriminator `interSubinventoryParameters`, run/timestamp identity, visibility result, sample-support result, mandatory attributes, key attributes, and sanitized diagnostic; never reuse prior-run success | `interSubinventoryParameters` |
| bo_owned_references | Organization and subinventory references | Yes | Organization, source subinventory, or destination subinventory is supplied | BO-owned | Registered BO and Data Loader |  | The user confirmed these reference mappings are handled by the BO | Supply BO-supported values; do not add local REST lookups | `OrganizationCode`, `OrganizationId`, `FromSubinventory`, `ToSubinventory` |

## Runtime Evidence Contract

- External BO-registration confirmation is user-provided provenance only, not runtime readiness evidence.
- A successful metadata preflight from another environment or earlier run must not be reused.
- The current run succeeds only when the selected environment exposes exact discriminator `interSubinventoryParameters` and metadata confirms sample support, mandatory attributes, and key attributes.
- Persist only sanitized metadata evidence; never record tokens, credentials, session material, or full sensitive payloads.
- A missing, failed, ambiguous, or incomplete preflight blocks Data Loader handoff. Do not fall back to direct REST mutation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.CHECK_READINESS | decision | 20 | resolve_dependency | ready->ISP.RESOLVE_DESTINATION_TYPE;blocked->ISP.HANDLE_ERROR | ISP.VALIDATE_INPUT | stop | After initial validation; run the current selected environment's read-only metadata preflight for exact BO `interSubinventoryParameters` and retain complete sanitized runtime evidence before lookup or handoff |
