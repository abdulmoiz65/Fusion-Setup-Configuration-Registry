# Module Endpoint API Reference

Source: supplied Topology Manager OpenAPI v3.0.1 contract.

| Operation | Method and path | Inputs | Contract behavior |
| --- | --- | --- | --- |
| Get deployed module endpoint | `GET /endpoints/{endpointKey}/deployedModules/{moduleKey}` | `appShortName`, `moduleShortName`; optional `fields` | Read-only deployed-module endpoint lookup. |

Normalize `appShortName` to path parameter `endpointKey` and `module`,
`moduleKey`, `moduleShortName`, `module short name`, `module_short_name`, and
`module-short-name` to `moduleKey`. Both must be present, are not interchangeable
with an endpoint URL, and preserve their supplied case when composing the path.
Forward an optional `fields` query parameter unchanged.

When the module is absent, Fusion returns `404 Not Found` with
`Module not found: {endpointKey}/{moduleKey}`. Report that absence without
retrying or substituting another module. By default, return `internalEndpoint`
and `externalEndpoint` only.
