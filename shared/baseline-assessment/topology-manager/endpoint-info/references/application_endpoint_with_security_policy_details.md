# Application Endpoint Security Policy API Reference

Source: supplied Topology Manager OpenAPI v3.0.1 contract and the internal supported-policy catalog.

| Operation | Method and path | Inputs | Contract behavior |
| --- | --- | --- | --- |
| Get policy | `GET /endpointSecurityPolicies/{endpointKey}` | `endpointKey`; optional `fields` defaulting to `endpointKey,policyName` | Read-only. |
| Create policy | `POST /endpointSecurityPolicies` | `endpointKey`, `policyName`; optional credential fields | Exact-preview approval; success is `201 Created`. |
| Update policy | `PATCH /endpointSecurityPolicies/{endpointKey}` | `endpointKey`; valid policy payload | Exact-preview approval; success is `201 Created`. |
| Delete policy | `DELETE /endpointSecurityPolicies/{endpointKey}` | `endpointKey` | Exact-preview approval; success is `204 No Content`. |

Supported policy fields are `endpointKey`, `policyName`, `clientId`, `clientSecret`, `username`, and `password`. `endpointKey` and `policyName` are required for create or update. `policy`, `security policy`, `securityPolicy`, `securityPolocy`, and `policy name` map to `policyName` when one policy interpretation is clear; `client id` maps to `clientId`; and `client secret` maps to `clientSecret`. Never infer credentials.

Accept only these policy names for create or update:

| Policy name | Username and password |
| --- | --- |
| `oracle/wss_http_token_over_ssl_client_policy` | Required together. |
| `oracle/wss_saml_token_over_ssl_client_policy` | Not used; do not send either field. |
| `oracle/wss_username_token_over_ssl_client_policy` | Required together. |
| `oracle/wss10_username_token_with_message_protection_client_policy` | Required together. |
| `oracle/wss11_username_token_with_message_protection_client_policy` | Required together. |

For username-token policies, fail input validation if either credential is absent. These fields are application-policy payload values, not FDOS authentication credentials. Never print or persist them; a preview states only whether each required field was supplied.

For a successful `200 OK` GET with null, missing, or blank `policyName`, return exactly:

`application <appname> is not configured with security policy`

For GET, pass every user-requested response field in the comma-separated
`fields` query parameter; the default is `endpointKey,policyName`. When the
user requests `username`, return it. When the user requests `password` or
`clientSecret`, pass the field to the API but redact its value from responses,
diagnostics, and artifacts. If no fields are requested, confirm successful
retrieval without disclosing response properties.

Do not automatically retry POST, PATCH, or DELETE. Redact all sensitive policy details from diagnostics.
