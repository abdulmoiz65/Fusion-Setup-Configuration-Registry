# Core Data Loader Execution Boundary

## Purpose

Keep Item Import package preparation separate from Fusion execution. This task
skill prepares and validates one immutable FBDI ZIP from the current public
Oracle Item Import template, then hands that unchanged archive to
`core.data-loader`.

## Boundary

The registered FBDI Data Loader business object is `item`. The task skill must
not upload the ZIP, call an ESS job, initiate or monitor an import, query a
Fusion execution endpoint, or invoke a product-specific loader. It provides
only the ZIP and read-only validation evidence: template provenance, SHA-256
digest, member manifest, row counts, mapping preview, and Batch ID.

`core.data-loader` exclusively owns any subsequent authorization, upload,
import initiation, monitoring, and diagnostics under its own workflow.