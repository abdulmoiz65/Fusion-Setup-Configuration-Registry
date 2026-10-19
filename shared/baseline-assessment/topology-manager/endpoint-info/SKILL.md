---
skill_id: "shared.baseline-assessment.topology-manager.application-endpoint"
name: "Topology Manager Application Endpoint API"
description: "Plans and executes supported Topology Manager application endpoint, secure-attribute, security-policy, and module endpoint API operations."
layer: "shared"
pillar: "Common"
type: "advisory"
execution_mode: "assisted"
owner_team: "Topology Manager and shared enablement teams"
version: "0.1.0"
inputs:
  - "target_environment"
  - "operation"
  - "application_identifier"
  - "module_identifier"
  - "query_controls"
  - "mutation_payload"
  - "execution_options"
outputs:
  - "validated_application_endpoint_request_plan"
  - "response_summary"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
persists_project_state: false
workspace_outputs: []
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Target environment release supporting the Topology Manager API"
side_effects:
  - "Read operations retrieve Topology Manager application endpoint configuration."
  - "Approved create, patch, and delete operations change target-environment application endpoint configuration."
  - "FDOS OAuth may refresh its local gitignored token cache."
required_privileges:
  - "Authenticated access with the Topology Manager resource scope required by the selected route"
---

# Topology Manager Application Endpoint API

## Purpose

Resolve one supported application endpoint, module endpoint, secure-attribute,
or endpoint-security-policy request before forming a request. Fail closed on
ambiguous resource intent, conflicting identifiers, unsupported fields, or
invalid payloads.

## Help Intent

Treat requests for help, usage, capabilities, or example requests as
informational. Do not resolve an API operation or resource class. Do not
authenticate. Do not display a request preview. Do not call any API.

Treat `TM skill usage`, `topology-manager skill usage`, and `topologyManager
skill usage` as equivalent help intents. Return the same usage guidance for
each phrase.

Explain that this skill supports application endpoint list, get, create, update,
and delete operations; deployed-module endpoint retrieval; secure-attribute
get, create, and delete operations; and endpoint security-policy get, create,
update, and delete operations. Explain the applicable required identifiers and
that writes require explicit approval.

## Topology Manager Usage Response

For any Topology Manager usage help intent, return the following descriptive
guidance. Include environment information as a Topology Manager capability.
Do not authenticate, display a request preview, or call an API while returning
this guidance.

Topology Manager lets you inspect and manage application endpoints, deployed
module endpoints, secure attributes, endpoint security policies, and
environment information.

### Application Endpoints

- List application endpoints: “List application endpoints”.
- Get one endpoint: “Get endpoint for app FIN”.
- Create an endpoint: “Create an endpoint for app FIN with URL
  https://example.com”.
- Update an endpoint: “Update the endpoint for app FIN to
  https://example.com”.
- Delete an endpoint: “Delete the endpoint for app FIN”.

### Deployed Module Endpoints

Use the application short name and the module short name to look up a deployed
module endpoint. For example: “Get deployed module endpoint for app FIN and
module short name PAYMENTS”. This is read-only and returns the module's
internal and external endpoint values by default.

### Secure Attributes

- Get secure attributes: “Show secure attributes for app FIN”.
- Create secure attributes: “Secure attribute clientId for app FIN”.
- Delete secure attributes: “Delete secure attributes for app FIN”.

### Endpoint Security Policies

- Get a policy: “Show the security policy for app FIN”.
- Create a policy: “Create a security policy for app FIN”.
- Update a policy: “Update the security policy for app FIN”.
- Delete a policy: “Delete the security policy for app FIN”.

### Combined Endpoint Setup

For a combined setup request, create the application endpoint first. After it
succeeds, apply the requested security policy or secure attributes. Examples:

- “Create an endpoint for app APP_NAME with URL https://example.com and secure
  it with policy oracle/wss_saml_token_over_ssl_client_policy”.
- “Create an endpoint for app APP_NAME with URL https://example.com and add
  secure attributes clientId=<value> and clientSecret=<value>”.
- “Add secure attributes clientId=<value> and clientSecret=<value> for app
  APP_NAME”.

`<value>` represents user-supplied sensitive data. Never repeat the value in a
preview, response, diagnostic, or artifact.

### Natural-Language Variations

Recognize equivalent request phrasing case-insensitively across camelCase,
snake_case, kebab-case, spaces, and punctuation. The user can identify an
application as an app, application, endpoint, endpoint key, or app short name;
they can identify a module as a module, module key, or module short name.

Examples of supported variations:

- “Register app APP_NAME at https://example.com”.
- “Change APP_NAME URL to https://example.com”.
- “Get module endpoint for APP_NAME, module PAYMENTS”.
- “Protect clientId and clientSecret for APP_NAME”.
- “Apply SAML policy to APP_NAME”. Ask for the supported policy name when the
  request does not provide one.
- “Create APP_NAME, configure https://example.com, then add SAML policy”. Ask
  for the supported policy name before previewing the follow-on policy request.
- “Show pod release and upgrade status”.

### Environment Information

Use Topology Manager to retrieve read-only environment name, type, size,
release, break-glass, and derived upgrade-status information. For example:
“Show environment info”.

### Safety and Approval

Reads show a request preview and may proceed after it. Writes show an exact
request preview and require explicit approval. Secure-attribute values and
credentials are always redacted. Updating a provisioned application endpoint
shows the provisioned-configuration overwrite warning before it can proceed.

## Authentication

Use the shared FDOS OAuth authentication flow through
`core.auth.fusion-oauth-authentication` and execute the request with
`core.fusion-api.rest-api-client`. The FDOS OAuth flow owns login, token-cache
reuse, refresh, and the single safe-read retry after a cached-token `401` or
`403`. This skill must not ask for a Fusion password, construct Basic
authentication, or generate a Fusion Common-specific token.

Never print or persist OAuth tokens, Authorization headers, client secrets,
secure-attribute values, or endpoint-security-policy credentials.

## API Base Route

Use the configured Spectra host with this public base route:

```text
{restBaseUrl}/api/fusion-common/topologymanager/v1
```

All paths in this skill's references are relative to that base route. Compose
the final route with exactly one `/v1` segment; do not use an internal cluster
service URL.

## Resource References

Load only the reference for the resolved resource before forming a request:

| Resource | Reference |
| --- | --- |
| Application endpoint | `references/application_endpoint_details.md` |
| Application endpoint security policy | `references/application_endpoint_with_security_policy_details.md` |
| Application secure attributes | `references/application_secure_attributes.md` |
| Module endpoint | `references/module_endpoint_details.md` |

## Natural-Language Normalization and Routing

Normalize user-supplied labels case-insensitively across camelCase, PascalCase,
snake_case, kebab-case, spaces, and punctuation. Correct a synonym or minor
typo only when the selected API contract has one unambiguous meaning. Preserve
the supplied identifier value exactly when composing an API path because
application and module identifiers can be case-sensitive.

- For application endpoint, endpoint-security-policy, and secure-attribute
  requests, map `app`, `application`, `endpoint`, `endpointKey`,
  `appShortName`, `app short name`, `app_short_name`, and `app-short-name` to
  canonical `endpointKey` when the phrase identifies the target application.
  Different values supplied through aliases are conflicting identifiers: ask one
  concise clarification and make no API call.
- For deployed-module retrieval, map `module`, `moduleKey`, `moduleShortName`,
  `module short name`, `module_short_name`, and `module-short-name` to canonical
  `moduleKey`. Require both `endpointKey` and `moduleKey`; never infer either
  from an endpoint URL.
- An allowed policy name or an explicit policy-name field selects the
  security-policy API. “Secure this property,” “secure these properties,” or
  equivalent named-attribute intent without a policy name selects secure
  attributes. Host, port, protocol, URL, or endpoint-registration data selects
  the application endpoint API. A request such as “secure this app” without a
  policy name or attribute pairs is ambiguous; ask whether the user means a
  security policy or secure attributes and make no API call.
- Map read, show, get, and list to GET; create, register, and add to POST;
  change, update, and patch to PATCH; and delete and remove to DELETE. Fail
  input validation instead of substituting an unsupported operation.

## Request Preview Presentation

Render every read and mutation preview as concise plain text under a `Request
preview` heading. Use labeled lines in this order when applicable:

- `Method:`
- `Route:`
- `Resource:`
- `Target environment:`
- Endpoint key (`endpointKey`):
- `Query controls:`
- canonical non-secret payload fields and values
- `(inferred)` for each inferred value
- `(supplied, redacted)` for credentials and secure attributes
- `Warning:` for a provisioned application endpoint update
- `Expected response:` for reads or `Side effect:` for mutations

Do not render request previews as JSON or JSON-like object syntax, and do not
use JSON code fences.

### Provisioned Application Endpoint Update Preflight

Before rendering a `PATCH /endpoints/{endpointKey}` preview, issue this safe
preflight request:

```text
GET /enterpriseApplications/{endpointKey}?fields=domainName
```

Use the returned `domainName` to determine provisioned status:

- A non-empty `domainName` means the application is provisioned. Include these
  lines in the PATCH preview after the endpoint value and before the side
  effect:

```text
Side effect: Updates this provisioned app's endpoint configuration.
Warning: This is a provisioned app. Updating its endpoint will overwrite the provisioned configuration. Are you sure you want to update the endpoint of this provisioned app?

Reply with explicit approval of this exact preview and warning (for example, "Approve this PATCH") and I'll execute it.
```

- An empty or null `domainName` means the application is not provisioned. Show
  the standard PATCH preview and approval guidance without the provisioned-app
  warning.
- For a preflight failure, missing response field, or unexpected status, fail
  closed and do not render or execute the PATCH.

Only explicit approval that acknowledges the unchanged preview and warning may
apply a provisioned-app PATCH. A changed route, target environment, endpoint
key, or endpoint value requires a new preflight, preview, and approval.

## Combined Requests

For a combined request, create the application endpoint first. Only after
endpoint creation succeeds can the skill associate a security policy or add
secure attributes. Apply the existing plain-text preview, approval, and
redaction rules to each resolved mutation. Only after endpoint creation
succeeds may the follow-on call be previewed or executed.

## Assisted Execution

1. Infer exactly one supported resource and operation from the user request.
   Normalize `app`, `application`, `endpoint`, and app-short-name variants to
   `endpointKey`; preserve its supplied case in the path. For a module lookup,
   normalize `module` and module-short-name variants to `moduleKey` and require
   both identifiers.
2. Preflight the target environment, required identifiers, query controls,
   payload shape, resource scope, timeout, and destination artifact path. Fail
   closed on ambiguity, overwrite conflicts, or invalid payloads.
3. Show every request as a plain-text `Request preview`. Reads may proceed after
   the preview. POST, PATCH, and DELETE require explicit approval of the exact
   route, target, canonical non-secret fields, inferred defaults, redacted
   credential presence indicators, and side effect.
4. Do not automatically retry a mutation. For a cached-token `401` or `403`,
   let the shared FDOS OAuth path refresh once and retry only the original safe
   read. A mutation requires new approval before any retry.
5. Return only requested non-sensitive response fields. Do not emit raw JSON
   unless the user expressly requests it.

## Diagnostics and Persistence

Classify failures as input validation, auth/authz, transport/environment,
Fusion API, process timeout, process failed, artifact persistence, or approval
blocker. Do not create project artifacts for successful calls. If the user
explicitly requests a diagnostic, save only a redacted summary under
`project/{project_id}/artifacts/shared/baseline-assessment/topology-manager/`.
