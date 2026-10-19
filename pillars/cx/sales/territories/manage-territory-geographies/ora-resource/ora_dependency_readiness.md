# Dependency Readiness

Require an active project Run Book, explicit environment and selected OAuth
properties before native Data Loader preflight. Use approved external
connectivity from the first live command when networking is restricted.

Before Task Hook validation, core Data Loader must have persisted its final
immutable archive and preflight. Require `taskRouted=true`,
`mappingComplete=true`, `sourceType=ORA_CX_IMPORT`,
`cxImportObjectCode=GeoTerritoryInterface`, the target-verified UCM account,
and matching environment, Run Book and archive SHA-256. A source CSV checksum
cannot replace the final archive checksum.

The declared metadata lookup must agree with the account in core preflight.
The identity needs native Data Loader metadata/initiation privileges and
Documents upload access. Do not claim a successful metadata GET proves write
privileges. Let the approved core operation report authorization failures;
do not use a test upload or another transport as a privilege probe.

Treat compatible country structures and master geography paths as target
prerequisites; no documented exact `geoZones` equivalence check is available.

Existing uncertain upload or initiation evidence blocks resubmission. Preserve
legacy checkpoints and obtain a supported reconciliation route; a new CSV or
new preflight must not bypass the same unresolved operation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.DEPENDENCIES | step | 3 | resolve_dependency | ready->TG.UCM_METADATA;blocked->TG.ERROR | TG.CSV | stop | Before Task Hook preview; native core preflight must already exist. |
