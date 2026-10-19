# Manage Data Enrichment Integration Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation selection | operation=configure or operation=check_status | Stop before guidance or a REST call | Ask whether configuration guidance or a read-only status check is required | Always | |
| Target Fusion environment | fusion_environment_context with one exact nonproduction or production target identity | Stop before authentication or a REST call | Ask for the named Fusion environment without requesting credentials | operation=check_status | |
| Configuration scope | configuration_scope=enrichment, smart_data, or both | Continue with both and disclose the assumption | User may narrow the guidance to enrichment or Smart Data | operation=configure | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| operation=configure and configuration scope is known | Valid | Evaluate configuration prerequisites and design gates | |
| operation=check_status and one exact Fusion environment is known | Valid | Evaluate authenticated read readiness | |
| operation is unsupported or ambiguous | Invalid | Stop and request one supported operation | |
| A request includes a password, client secret, access token, refresh token, or Authorization header | Invalid | Do not echo or persist the value; tell the user to enter secrets only in the authorized product UI or local credential flow | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is exactly configure or check_status | Continue on the matching branch | Always | |
| Fusion environment resolves to one exact target | Continue to the read-readiness gate | operation=check_status | |
| Request attempts POST, PATCH, PUT, DELETE, Data Loader generation, import, or credential submission | Return unsupported; this task skill owns guidance and a read-only GET only | Always | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEI.SELECT_OPERATION | decision | 1 | validate_input | valid->DEI.READINESS;invalid->DEI.HANDLE_ERROR | none | stop | Normalize the request to configure or check_status and reject secrets or unsupported mutations. |
