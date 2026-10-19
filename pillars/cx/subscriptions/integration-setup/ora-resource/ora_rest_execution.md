# Integration Setup REST and Data Loader Execution

## Allowed Routes

Use `core.fusion-api.rest-api-client` only for the declared read-only metadata,
rule-set, and published-status lookups. Do not use direct REST mutation. Use
`core.data-loader` for every Data Loader source, validation, upload, initiation,
monitoring, and diagnostic operation, including publishing through
`subscriptionGroupingRuleSets_publishGroupingRuleSets` and attribute-map
updates through `subscriptionGroupingRuleSets_updateOmOssAttrMap`.

The declared read-semantic Order Management-to-Subscription lookup is `POST
/crmRestApi/resources/11.13.18.05/subscriptionGroupingRuleSets/action/getOmOssAttrMap`
with `Content-Type: application/vnd.oracle.adf.action+json`,
`REST-Framework-Version: 9`, and an empty JSON object body. It returns the
attribute map in `result` and must never be used as a configuration write.

## Approval Gate

Before upload or initiation, confirm the selected Fusion environment, registered
business object, live schema, source mapping, immutable archive checksum, Task Hook
envelope, and current explicit approval. Revalidate the checksum and approval at
execution time.

## Recovery

Stop on lookup, validation, upload, initiation, or processing failures. Preserve
redacted diagnostics and do not retry a load without a new valid approval. Direct
REST mutation and CSV task import remain unsupported routes.
