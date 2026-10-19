# Usage Rating Setup REST Execution

## Route Selection

Use REST only when the request explicitly selects REST for the resolved setup
task. Use `core.fusion-api.rest-api-client` for every Fusion REST lookup and
write. Use `core.data-loader` for Data Loader workbook generation, validation,
upload, import initiation, status monitoring, and diagnostics; do not substitute
a direct REST route for a Data Loader request.

## Preflight and Preview

Before a write, confirm the target environment, caller privileges, exact object
identity, task-specific dependency lookups, catalog support, and complete payload.
Show the immutable endpoint, method, headers, payload, and target environment, then
obtain explicit approval immediately before submitting one write.

## Execution and Verification

Submit a live POST, PATCH, activation action, upload, or import once only. Verify
completed REST writes through the task's declared read-only lookup. For Data Loader
operations, let `core.data-loader` own upload, polling, status collection, and
process diagnostics.

## Failure Handling

Do not retry an uncertain or failed live write automatically. Stop on input,
catalog, authorization, transport, or Fusion API failures and persist redacted
diagnostics in the project workspace. A cached-token HTTP 401 or 403 may receive
the one refresh retry owned by the core REST client.
