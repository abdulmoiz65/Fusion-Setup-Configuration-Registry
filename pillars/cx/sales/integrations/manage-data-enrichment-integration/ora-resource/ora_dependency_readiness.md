# Manage Data Enrichment Integration Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | DaaS subscription and service instance | For configuration guidance, confirm that an Account or Contact Enrichment subscription and activated service instance exist. |
| 2 | DaaS integration user role | For configuration guidance, confirm the integration user has DATASERVICE_CLIENT_API_APPID. |
| 3 | Fusion environment and authenticated read access | For check_status, resolve one exact environment and allow the shared REST client to obtain or refresh its local OAuth token without exposing it. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| daas_subscription | Active enrichment subscription and service instance | Yes | operation=configure | Satisfied or Blocked | Customer subscription and activation records | | The integration page needs an activated data-service endpoint. | Confirm activation before entering integration details. | subscription_readiness |
| daas_integration_role | DATASERVICE_CLIENT_API_APPID role | Yes | operation=configure | Satisfied or Blocked | Identity administrator confirmation | | Oracle requires the role for the integration user. | Ask the identity administrator to confirm the role assignment; do not request user credentials. | integration_role_readiness |
| fusion_read_context | Exact Fusion environment and authenticated CRM REST access | Yes | operation=check_status | Satisfied or Blocked | Selected environment context and core OAuth flow | | The status lookup must not run against an ambiguous environment or without authorized read access. | Select one environment; complete the local OAuth flow if prompted. | target_environment, authenticated_read_ready |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every dependency applicable to the selected operation is satisfied | Run the read-only lookup only for check_status; no create is supported |
| Missing | A required subscription, role, environment, or authenticated read context is absent | No |
| Unsupported | The request asks this skill to create subscriptions, assign roles, enter credentials, or mutate Fusion through REST or Data Loader | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEI.READINESS | decision | 2 | resolve_dependency | ready->DEI.DESIGN_GATE;missing->DEI.HANDLE_ERROR;unsupported->DEI.HANDLE_ERROR | DEI.SELECT_OPERATION | stop | Evaluate only the dependencies applicable to the selected configure or check_status operation. |
