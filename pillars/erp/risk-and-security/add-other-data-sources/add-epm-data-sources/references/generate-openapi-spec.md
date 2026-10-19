# Generate OpenAPI Specification

Produce one accurate, connector-ready OpenAPI document from the supplied JSON input. Generate OpenAPI 3 by default; generate Swagger 2.0 only when the user or the target connector explicitly requires it. The input may provide documentation URLs directly, ask the skill to discover official documentation from a datasource and operation summaries, or request datasource-only discovery. The final response must contain only the complete OpenAPI JSON object—no Markdown fences, narrative, or omissions.

## Input

Accept either of these input shapes.

### Documentation-URL mode

```json
{
  "datasourceType": "<data source type>",
  "Rest API documentation": ["<REST API documentation URL>"],
  "Security Documentation": "<security documentation URL>"
}
```

### Discovery mode

```json
{
  "datasourceType": "<data source type>",
  "operations": [
    "<plain-language summary of one requested REST operation>"
  ],
  "securityType": "<requested authentication type>",
  "debug": true
}
```

`securityType` identifies the required authentication type to discover and use, for example `OAuth2 JWT Assertion`. In discovery modes, when `securityType` is omitted, apply the datasource-specific default below; otherwise default it to `OAuth2 Assertion`. It is a discovery constraint, not evidence for an OpenAPI field: the selected official Security Documentation must confirm it. `debug` is optional and defaults to `false`. It is useful in discovery mode and does not change the generated OpenAPI document.

For example:

```json
{
  "datasourceType": "Oracle EPM REST API",
  "operations": [
    "Get all available roles",
    "Get all user role assignments"
  ],
  "securityType": "OAuth2 JWT Assertion"
}
```

### Datasource-only discovery mode

```json
{
  "datasourceType": "<data source type>"
}
```

### Datasource-specific discovery constraints

Apply these constraints when the datasource type identifies the stated datasource, regardless of casing or harmless naming variations.

- For Oracle EPM, including EPM ARCS, EPM-ARCS, and EPM-FCCS, discover only these operations:
  - `Get all available roles`
  - `Get all user role assignments`
  Use `OAuth2 JWT Assertion` as the required security type when `securityType` is omitted. Do not select user-list, group-list, or any other EPM operation.
- Interpret `OCI` as OCI Identity Domains (formerly IDCS), not OCI service APIs generally. Use `OAuth2 with Client credential grant type` as the required security type when `securityType` is omitted. Select only Identity Domain REST API and security documentation that confirms the client credentials grant.

When the user explicitly supplies a conflicting `securityType` for one of these datasource types, ask for clarification rather than silently overriding it.

For Oracle EPM operation-summary discovery, if any requested operation is not one of the two allowed EPM operations, ask the user to limit the request to those operations before documentation discovery.

This mode has no `operations`, documentation URLs, or security-type input. It uses the fixed discovery targets and version-selection rules in Workflow step 1.2.

Treat supplied REST API documentation URLs, or the official REST API pages selected in discovery mode, as the source of truth for endpoints, parameters, request bodies, responses, and media types. Treat the supplied Security Documentation URL, or the official security page selected in discovery mode, as the sole source of truth for `securitySchemes`, including the authentication type, OAuth flow, token URL, scopes, and scheme name. Do not derive, supplement, or override `securitySchemes` from REST API documentation, including sample requests, cURL commands, Authorization headers, or response examples. If an input field is absent or empty, omit only the parts that cannot be established from the applicable supplied source.

## Interactive Input Completion

Before determining the input mode, validate the supplied input.

When `datasourceType` is absent, empty, or ambiguous, do not generate an OpenAPI document. Ask the user for the datasource type.

When the user intends operation-summary discovery but provides no non-empty `operations` array, ask for the requested operations. Do not ask this question when the user explicitly requests datasource-only discovery.

When `securityType` is absent, use the applicable datasource-specific default; otherwise use `OAuth2 Assertion`. Do not ask for it. When it is supplied but ambiguous, ask the user to clarify the authentication type.

When required information is missing, send one concise clarification message containing every missing field. Do not emit partial OpenAPI JSON, invent values, or begin documentation discovery until the user responds.

Use this format:

> I need the following information before generating the OpenAPI specification:
> - `datasourceType`: ...
> - `operations`: ...
>
> You can reply with:
> ```json
> {
>   "datasourceType": "...",
>   "operations": ["..."],
>   "securityType": "OAuth2 JWT Assertion"
> }
> ```

The final-response-only JSON rule applies after input completion. Clarification responses may be normal conversational text.

## Workflow

1. Determine the input mode.
   - When REST API documentation URLs are supplied, fetch every supplied URL.
   - When URLs are absent and `operations` is supplied, use operation-summary discovery:
     - If `securityType` is omitted, set the discovery constraint to the applicable datasource-specific default; otherwise set it to `OAuth2 Assertion`.
     - Search for each operation using the datasource type, the operation summary, and `REST API`.
     - If the REST API is based on the System for Cross-domain Identity Management (SCIM) protocol, also try to discover REST APIs or operations that return the requested related data as attached or nested response content for these operation summaries:
       - `Get all App Roles with app info for each AppRole object`
       - `Get all users with role assignments for each user object`
       Select such an operation only when the official documentation explicitly shows that the response contains the corresponding application information for each AppRole object or role assignments for each user object. Do not infer nested fields or synthesize joined responses from separate APIs.
     - Select only a page published on the datasource vendor's official documentation site that explicitly documents the requested operation. Do not use search-result snippets, community pages, blogs, forums, code repositories, cached copies, third-party API catalogs, or pages merely quoting the vendor documentation.
     - When multiple official pages document the same operation for different REST API versions, select the latest version explicitly identified by the official documentation.
     - Confirm the selected page states an HTTP method and REST resource path before using it. A search-result title or snippet is not sufficient evidence.
     - Search separately for the datasource's official authentication or security documentation. When `securityType` is supplied, use it as a search and selection constraint. Treat the selected page as the Security Documentation source only after confirming that it documents the requested authentication type and its applicable mechanism.
     - If multiple official pages remain equally plausible after applying the latest-version rule, a candidate does not document the requested operation, the latest version cannot be established, the requested `securityType` cannot be confirmed, or no official source is found, stop and ask the user for the documentation URL or a more specific operation summary. Do not guess.
   - When the input contains only `datasourceType`, use datasource-only discovery:
     1. Set the security discovery constraint to the applicable datasource-specific default; otherwise set it to `OAuth2 Assertion`.
     2. For Oracle EPM, including EPM ARCS, EPM-ARCS, and EPM-FCCS, search only for the two fixed operations `Get all available roles` and `Get all user role assignments`. For all other datasources, search official vendor documentation for at most one REST API in each target category: user-list information, role-list information, and user-role-assignment information.
     3. For each candidate, confirm that an official page explicitly documents the HTTP method and REST resource path.
     4. For each target category, when multiple official pages document the same API at different versions, select that API's highest explicitly identified version. Include every verified target-category API at its own latest version.
     5. If an API exposes no explicit version, use the verified unversioned API documentation for that API.
     6. API versions are selected independently. It is acceptable for the resulting specification to contain endpoints at different API versions when each endpoint comes from the latest verified version of its own API.
     7. Search separately for the datasource's official authentication or security documentation and use it only if it confirms the applicable default or an explicitly requested `securityType`. Do not infer a security scheme when no official security source is found.
2. Follow relevant links or reference pages only when they are part of the selected documentation and necessary to resolve endpoint, schema, or security details. Build an endpoint inventory containing only the operation pages supplied or selected for the user's requested operations, or the fixed target categories in datasource-only discovery mode. Do not infer version variants, CRUD operations, undocumented companion endpoints, or additional operations merely because they are related to the datasource.
3. For each endpoint, extract its exact HTTP method, documented resource path, summary/description, query/path/header parameters, request body, responses, and media types. Generate a unique, meaningful camelCase `operationId` from the documented action and resource (for example, `getAvailableRoles`); do not use generic or sequential IDs. Preserve the documented spelling, casing, primitive types, required flags, enum values, formats, and response shape.
4. Derive server information only from the documentation. In OpenAPI 3, use `servers`; in Swagger 2.0, use `host` and `basePath`. If the documentation uses the `<BASE-URL>` placeholder instead of a concrete server, preserve it in OpenAPI 3 as `"servers": [{"url": "https://<BASE-URL>"}]` rather than guessing a concrete host. Normalize full endpoint URLs into the version-appropriate server and path components when possible.
5. Extract reusable request and response object schemas into version-appropriate reusable components when their structure is documented and reusable: `components/schemas` in OpenAPI 3 or `definitions` in Swagger 2.0. Use `$ref` for those schemas. For every property of every object schema, include a concise, factual `description` alongside its documented `type`, based on the source documentation or its documented example. Define inline schemas when reuse would obscure the documented model. Do not add fields that are merely typical or implied.
6. Read only the Security Documentation source—either the Security Documentation URL from the input or the security page selected during discovery—when generating `securitySchemes`; do not use REST API documentation, including sample requests, cURL commands, or Authorization headers, for this purpose. Add security definitions and operation-level `security` only when the Security Documentation documents the authentication mechanism and its application. Use `components/securitySchemes` in OpenAPI 3 or `securityDefinitions` in Swagger 2.0. Do not define a top-level `security` section. Use ONLY an OAuth2 security scheme for documented OAuth authentication; do not model an OAuth access token as an `http` `bearer` scheme. Include only the flow, token URL, scopes, and scheme name documented in the Security Documentation or its directly linked, relevant reference pages. For Oracle EPM, including EPM ARCS, EPM-ARCS, and EPM-FCCS, when the Security Documentation identifies the Assertion Grant type, define the scheme as `"OAuth2": {"type": "oauth2", "flows": {"jwtAssertion": {...}}}`; use the exact lower-camel-case flow key `jwtAssertion` required by the target connector. For OCI Identity Domains, use the standard OpenAPI `clientCredentials` flow only when its official Security Documentation confirms the client credentials grant. Do not add Basic Auth or any other security definition or requirement.
7. Validate the finished document as JSON and against its selected OpenAPI version. If the target connector requires the non-standard `jwtAssertion` OAuth2 flow, validate all standard portions and preserve that connector-specific flow key. Correct structural errors while retaining only documentation-backed content.
8. When `debug` is `true`, emit non-final diagnostic progress messages while discovering and generating the specification. The messages must identify:
   - each requested operation, or each fixed datasource-only target category searched;
   - every official documentation URL selected for that operation, with its page title and identified API version;
   - the official Security Documentation URL selected and the documented authentication mechanism;
   - the requested or defaulted `securityType` and whether the selected Security Documentation confirms it;
   - whether the latest-version rule was applied and why the selected version is the latest official version found; and
   - any directly linked reference page used to establish an endpoint, schema, token URL, or scope.
   Never present a search result, a third-party page, or an unverified candidate as a source used. Emit diagnostics before the final answer; the final answer must still be only the complete OpenAPI JSON object.

## OpenAPI Requirements

- Use OpenAPI 3 by default (`"openapi": "3.x.x"`). Use `"swagger": "2.0"` only when Swagger 2.0 is explicitly required.
- Return JSON, never YAML.
- Include one unique, meaningful camelCase `operationId` on every operation, derived from its documented action and resource.
- Include version-appropriate OpenAPI components only when applicable and established by the documentation; `info` and `paths` are normally required for a usable specification. Do not define top-level `security`.
- Define request and response media types at every operation: use `requestBody.content` and `responses[*].content` in OpenAPI 3; use operation-level `consumes` and `produces` in Swagger 2.0. Do not define root-level `consumes` or `produces`.
- In OpenAPI 3, include request bodies with `requestBody` and documented content schemas. In Swagger 2.0, include request bodies as a single `in: "body"` parameter with a documented schema. Use `in: "formData"` only when the documentation explicitly specifies form fields.
- Model every documented response status code. If only a successful response is documented, include only that documented status. Add a response `description` from the source; use a minimal factual description when the source supplies a status but no prose.
- Use `type`, `format`, `items`, `properties`, `required`, `additionalProperties`, `enum`, and `default` only when documentation supports them. Represent unknown object schemas minimally rather than inventing their fields.
- In `components.schemas` (or Swagger 2.0 `definitions`), give every object property both a `type` and a concise, factual `description`.
- Use global `parameters` and `responses` only for truly reusable, documented components. Use operation-level definitions otherwise.
- Add tags only when the documentation exposes resource groups or categories; preserve their names.

## Evidence Rules

- Never invent endpoints, request fields, response fields, parameter names, authentication schemes, token URLs, scopes, defaults, status codes, or schemas.
- In discovery mode, operation summaries are search terms and selection criteria only; they are never evidence for an OpenAPI field. Every generated field must be supported by the selected official documentation page or an allowed directly linked reference page.
- In discovery mode, `securityType` is a search and selection constraint only; it is never evidence for a security scheme. Generate the requested scheme only when the selected official Security Documentation confirms its authentication type, flow, and applicable details.
- In discovery mode, use only vendor-published official documentation. For a requested operation with multiple official API versions, use the latest version that the official documentation explicitly identifies and keep every generated element aligned to that version.
- In datasource-only discovery mode, Oracle EPM (including EPM ARCS, EPM-ARCS, and EPM-FCCS) searches only for `Get all available roles` and `Get all user role assignments`. Other datasources search only for user-list, role-list, and user-role-assignment APIs. For each API, use its highest verified explicitly identified version; include each verified API independently.
- Never use REST API documentation, including sample requests, cURL commands, Authorization headers, or response examples, as evidence for a `securitySchemes` entry. Do not infer OAuth scopes such as `openid` or `profile`. Add a token URL or scope only when it is stated in the Security Documentation or in a directly linked, relevant reference page. When the target connector requires the non-standard `jwtAssertion` OAuth2 flow, preserve it even though it is not a standard OpenAPI OAuth flow.
- Do not silently merge similarly named models when the documentation distinguishes them.
- If sources conflict, prefer the more specific endpoint documentation; otherwise preserve the conflict conservatively by omitting the unsupported assertion.
- If documentation is incomplete, represent only what is supported. Favor a valid partial specification over plausible detail.
- Do not include a `security` requirement merely because a security scheme exists; apply it only where the documentation says it applies.

## Final Check

Before returning, confirm that the output is one parseable JSON object; it declares the selected OpenAPI version; each path begins with `/`; its parameters, request bodies, responses, and security components are valid for that version except an explicitly required connector-specific `jwtAssertion` flow; every `$ref` resolves; no content lacks source support; and every generated REST path uses the latest verified version of its own API when that API has an explicit version.