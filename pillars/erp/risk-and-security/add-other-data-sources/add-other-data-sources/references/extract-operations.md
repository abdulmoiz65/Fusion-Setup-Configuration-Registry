# Extract Operations

## Purpose

Transform `openApiFileContent`, a stringified OpenAPI or Swagger JSON document,
into Data Integrator extraction objects and source endpoints. The extraction
stage first builds a `REST Operations` contract, then sends that contract to
`scripts/openapi_output_formatter.py` for consistent object and endpoint
formatting.

## Input

- `openApiFileContent`: validated OpenAPI 3 or Swagger 2 JSON returned by
  `generate-openapi-spec.md`

## Build the REST Operations Contract

1. Read every supported HTTP operation under the OpenAPI document's `paths`
   object: `get`, `post`, `put`, `patch`, `delete`, `head`, and `options`.
2. Resolve local `$ref` values used by parameters, request bodies, responses,
   schemas, and reusable components before deriving operation objects. Support
   OpenAPI 3 components and Swagger 2 definitions when present. For every
   schema node, first resolve a local `$ref` recursively when it is present;
   otherwise derive the structure directly from that inline schema node. An
   inline schema is not a fallback or an empty schema merely because it does
   not use `$ref`. Treat a schema with `properties` as an object even when it
   omits `type: object`, and recursively derive array items from `items`.
3. Set `resourcePath` to the exact matching key from `paths`, retaining its
   documented spelling, case, slashes, and path placeholders. Confirm it still
   exactly matches a source `paths` key before formatting.
4. Choose one display name per operation: description, then summary, then
   operation ID, then a readable method-and-path name. Use it consistently for
   the operation, request object, and endpoint names and descriptions.
5. Set `operationType` to the lower-case HTTP method.
6. Resolve request and response content types from operation-level
   `consumes`/`produces` values or document-level values for Swagger 2, and
   from `requestBody.content` and response `content` for OpenAPI 3. Prefer JSON
   when multiple documented media types apply.
7. Add every documented path, query, and form parameter to
   `requestParameters.Parameters`. Represent each parameter type as `string`
   or `number`.
8. Create exactly one `requestObject` for each operation. Merge its resolved or
   inline request-body schema (or Swagger 2 body parameter) with all path,
   query, and form parameters, without overwriting a request-body property when
   a parameter has the same name. An inline OpenAPI 3 request body such as
   `content.application/json.schema.type: object` with `properties` must be
   converted exactly as the equivalent schema reached through a local `$ref`.
   When there is no body, construct the request object from those parameters.
   Use an empty object only when the operation has neither a body nor
   parameters.
9. Create exactly one `responseObject` from the selected successful response:
   prefer `200`, then another `2xx`, then `default`, then the first response
   with a body.
10. Use the operation ID for a request-object code when available. Use a named
    response schema or definition key for a response-object code when available;
    otherwise derive a stable code from the operation. Name a named response
    from its documented schema title when present, otherwise use its schema or
    definition key unchanged; do not prettify the key by inserting spaces.
    Apply these response-object-code overrides after resolving the response
    schema:
    - `/interop/rest/security/v2/report/roleassignmentreport/user`:
      `responseObject.objectCode` must be `RoleAssignmentList`.
    - `/interop/rest/security/v2/role/getavailableroles`:
      `responseObject.objectCode` must be `RoleList`.
    Because the formatter derives `responseKey` from
    `responseObject.objectCode`, these overrides also require the endpoint
    `responseKey` to use the same value.
11. Represent scalar values in `objectStructure` as only `string` or `number`.
    Preserve object nesting and represent arrays using one item whose structure
    represents the array item type. Apply this conversion identically to every
    resolved `$ref` schema, inline schema property, and parameter merged into a
    request object.
12. For every nonempty `objectStructure`, build
    `objectTreeStructure.attributes` as its complete recursive mirror. Create
    exactly one tree node for every scalar, object, and array property. Set
    each node's `attributeId` to its full underscore-delimited property path.
    Add `children` only to an object or array node that has one or more child
    properties; its value must be the recursively complete child-node list.
    Omit `children` entirely for scalar nodes and for object or array nodes with
    no child properties. Never emit `children: []`. The `attributeId` is the
    canonical value used for the corresponding flattened item's `attributeCode`.
    When `objectStructure` is empty,
    `objectTreeStructure.attributes` and
    `dataExtractionObjectAttributes.items` must also be empty.
13. Populate `dataExtractionObjectAttributes.items` depth-first from that tree.
    Include every container and scalar node. Use slash-delimited property paths
    without a leading slash for `attributePath`; use the corresponding tree
    node's `attributeId` for `attributeCode`; use the documented property title
    or property name for `name`.
14. Validate that each operation path, parameter, object code, attribute path,
    and attribute code is traceable to the input OpenAPI document. For every
    nonempty object structure, require a nonempty
    `dataExtractionObjectAttributes.items` list and an exact flattened entry for
    every tree node. Each flattened item's `attributeCode` must exactly equal
    its corresponding `objectTreeStructure` node's `attributeId`. No
    `objectTreeStructure` node may contain an empty `children` array. An empty
    request `objectStructure` is valid only when the operation has neither a
    request body nor path, query, or form parameters. An empty response
    `objectStructure` is valid only when the selected successful response has
    no documented content or schema. A schema with inline `properties`, or an
    array whose `items` schema is derivable, is documented content and must not
    produce an empty structure. Do not treat an unresolved `$ref`, an
    unsupported schema construct, or an extraction failure as an empty
    structure; fail validation instead. Do not format a partial operation
    model.

15. Verify inline-schema parity: an operation using an inline object schema and
    an otherwise equivalent operation using a local `$ref` must produce the
    same `objectStructure`, `objectTreeStructure.attributes`, and flattened
    `dataExtractionObjectAttributes.items`. Include this parity case in
    regression validation for the extraction implementation.

## REST Operations Syntax

The empty structures in this example are initialization placeholders only. They
are valid in final output only when the corresponding request or response has
no derivable schema and no eligible request parameters.

```json
{
  "REST Operations": [
    {
      "resourcePath": "<exact OpenAPI paths key>",
      "name": "<resolved operation display name>",
      "operationType": "<lower-case HTTP method>",
      "requestContentType": "<documented request media type>",
      "responseContentType": "<documented response media type>",
      "requestParameters": {
        "Parameters": [
          {
            "In": "<path, query, or formData>",
            "Name": "<documented parameter name>",
            "Type": "<string or number>"
          }
        ]
      },
      "requestObject": {
        "objectCode": "<operation ID or stable derived code>",
        "name": "<resolved operation display name>",
        "objectType": "TARGET",
        "objectStructure": {},
        "objectTreeStructure": {
          "attributes": []
        },
        "dataExtractionObjectAttributes": {
          "items": []
        },
        "selectedFlag": true
      },
      "responseObject": {
        "objectCode": "<response schema key or stable derived code>",
        "name": "<resolved response object name>",
        "objectType": "SOURCE",
        "objectStructure": {},
        "objectTreeStructure": {
          "attributes": []
        },
        "dataExtractionObjectAttributes": {
          "items": []
        },
        "selectedFlag": true
      }
    }
  ]
}
```

## Format the Connector Objects

Pass the complete `REST Operations` JSON to the task-local formatter through
standard input and retain its complete standard output in memory for the next
handoff. Do not create `rest-operations.json`, `operation-model.json`, a
generated-artifacts directory, or a project artifact for this runtime-only
stage.

The formatter returns:

```json
{
  "dataExtractionObjects": {
    "items": []
  },
  "sourceEndPoints": {
    "items": []
  }
}
```

For each operation, the formatter preserves `selectedFlag: true`, assigns
sequential object and endpoint reference codes, then writes these endpoint
associations:

- `requestObjectCode` from the formatted request object's reference code;
- `requestKey` from the formatted request object's `objectCode`;
- `responseObjectCode` from the formatted response object's reference code;
- `responseKey` from the formatted response object's `objectCode`.

It preserves nested object structures, flattened attribute metadata, and
request parameters as JSON values. It rejects a malformed REST Operations
contract or an object structure that lacks its flattened attributes. The
formatter reads standard input and writes standard output only; it does not
invoke an external API or create a generated-artifacts directory.

## Final Connector-Model Handoff

Insert the formatter output unchanged into `extractedData` as
`dataExtractionObjects` and `sourceEndPoints`. The remaining connector fields
are filled from task context and the resolved Data Integrator template metadata.
Pass the completed operation output to the next enabled workflow stage.
