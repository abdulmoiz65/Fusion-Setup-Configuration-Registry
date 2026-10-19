# Dependency Readiness

Do not infer missing target dependencies from business values inside an
unchanged FSM task CSV package. Absence from one CSV member is not evidence
that referenced setup is missing from the target.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM package integrity | Preserve the complete package and Oracle-defined object ordering; do not derive extra confirmations from individual row values |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| fsm_package_dependencies | Business references contained in the exported task package | No separate preflight gate | An unchanged package passes task identity and archive validation | Not evaluated locally | Oracle-generated FSM package | | Package rows do not prove that referenced setup is missing | Do not request task owner, template dependency, privilege, or impact confirmation before preview; let Fusion return any authorization or business-validation error | None |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Not evaluated locally | A complete unchanged task package contains business references | No; continue to immutable preview without requesting confirmation |
| Fusion rejection | Approved import returns an authorization or business-validation error | No automatic retry; report returned result and stop |
