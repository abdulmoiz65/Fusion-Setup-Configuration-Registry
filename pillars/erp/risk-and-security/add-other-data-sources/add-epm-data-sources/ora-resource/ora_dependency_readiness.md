# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Connector selection | Resolve one supported connector type and one connector name from the prompt. |
| 2 | Seeded source type | Derive EPM-ARCS or EPM-FCCS from the parsed connector type for the seeded-connector filter. |
| 3 | BOSS OAuth client | Select core.fusion-api.rest-api-client with boss_scope. |
| 4 | Seeded connector query | Run the read-only BOSS query filtered by source type before every downstream workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| epm_seeded_connector_definition | Connector definition collection for the selected source type | Yes | Every request | Verify | Read-only BOSS connectorDefinitions query response | query_seeded_epm_connector_definition | Determines whether to proceed to OpenAPI or UI credential setup | Direct the user to UI setup when the returned connector is not ready | Seeded connector collection; connector ID; seeded-connector readiness |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Seeded connector not set up | The query returns an empty collection | No; ask the user to complete seeded connector setup through the Fusion UI |
| Connector UI setup required | Exactly one connector is returned but is not both active and completed | Only after the user completes UI credential setup |
| Registered connector validation timeout | The specific registered connector does not become completed and active within 5 minutes | No; report last sanitized status and do not replay the registration POST |
| Authentication or authorization | BOSS client cannot acquire or use boss_scope | No |
| Transport or environment | The BOSS endpoint cannot be reached | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPMDS.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->EPMDS.QUERY_SEEDED_CONNECTOR;blocked->EPMDS.HANDLE_ISSUE | EPMDS.VALIDATE_INPUT | stop | After input validation |
