# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment | Confirm the configured Fusion environment is the intended BOSS read target. |
| 2 | BOSS OAuth | Prepare the shared BOSS OAuth client without exposing credentials. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DOMAINS.DEP.ENVIRONMENT | Target Fusion environment | Yes | Any BOSS read or mutation | Satisfied | fusion_environment_context and core/auth/fusionEnv.properties | | Domain results must come from the intended environment. | Confirm the configured environment before the BOSS call. | Target environment identity |
| DOMAINS.DEP.BOSS_OAUTH | BOSS OAuth configuration | Yes | Any BOSS read or mutation | Satisfied | core.auth.fusion-oauth-authentication and core.fusion-api.rest-api-client | | BOSS calls require boss_scope and the separate gitignored token cache. | Use the shared OAuth flow; never paste, execute, or persist a credential-bearing token command. | Authenticated BOSS client readiness |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Target environment and BOSS OAuth are ready. | Lookup only |
| Blocked | Environment is ambiguous or BOSS OAuth configuration is incomplete. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOMAINS.ACCESS | step | 2 | resolve_dependency | ready->DOMAINS.LIST_SELECT;blocked->RETURN_ISSUES | DOMAINS.VALIDATE | stop | Input validation passed |
