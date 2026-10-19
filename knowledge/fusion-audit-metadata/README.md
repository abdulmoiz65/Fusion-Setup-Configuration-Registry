# Fusion Audit Metadata

This folder contains high-level Fusion Audit Setup application/product names discovered from `FND_AUDIT_WEBAPP_AM`.

The metadata exists because the Audit Setup REST APIs can get or update setup only after the caller already knows the functional application/product name, such as `Receivables`, `customer`, `sales`, or `ORA_SERVICE`. The REST API documentation points to `FND_AUDIT_WEBAPP_AM` for valid product values, but does not expose a REST discovery endpoint for that table.

## Files

| File | Purpose |
| --- | --- |
| `fnd-audit-webapp-applications.json` | The 55 valid high-level `WEBAPP` application/product names discovered from `FND_AUDIT_WEBAPP_AM`. |

## Discovery Notes

- Discovery used a local BI Publisher SOAP report over `FND_AUDIT_WEBAPP_AM`.
- The BI Publisher SOAP helper used to create and run that report is intentionally not part of the FSCR handoff package.
- Object and field-level audit details are intentionally not stored here because they can be fetched on demand through the Audit Setup REST APIs once a valid application/product name is known.
- During earlier REST extraction testing, `Payables` had a server-side connection closure, even after extended timeout, payload-only retry, and token refresh. Treat that as an environment/service behavior to re-test later.
