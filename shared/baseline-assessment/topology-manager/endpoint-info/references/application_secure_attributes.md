# Application Secure Attributes API Reference

Source: supplied Topology Manager OpenAPI v3.0.1 contract.

| Operation | Method and path | Inputs | Contract behavior |
| --- | --- | --- | --- |
| Get secure attributes | `GET /endpointSecureAttributes/{endpointKey}` | `endpointKey`; optional `fields` defaulting to `endpointKey,attributes` | Read-only; redact all returned attribute values. |
| Create secure attributes | `POST /endpointSecureAttributes` | `endpointKey`; optional string-to-string `attributes` object | Exact-preview approval; success is `201 Created`. |
| Delete secure attributes | `DELETE /endpointSecureAttributes/{endpointKey}` | `endpointKey` | Exact-preview approval; success is `204 No Content`. |

“Secure this property,” “secure these properties,” “protect these values,” and
equivalent requests with an application identifier and named attribute pairs,
but no policy name, route to `POST /endpointSecureAttributes`. Normalize the
pairs into a string-to-string `attributes` object. Ask one concise clarification
and make no API call when values are absent, attributes are not a string-to-
string map, or policy intent conflicts.

For a successful `200 OK` GET with missing, null, or empty `attributes`, return
exactly:

`application <appname> does not have any secured attributes/properties`

If no response fields are requested for a non-empty successful GET, confirm
successful retrieval without disclosing response properties.

Never print, persist, or include secure-attribute values, credentials, tokens,
or Authorization headers in previews, summaries, diagnostics, or artifacts.
