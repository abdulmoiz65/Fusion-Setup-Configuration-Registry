# Input Validation

## Import Requirements

Require all of the following before an import approval preview:

- A non-empty, readable, unencrypted FSM ZIP with exactly one
  `ASM_SETUP_CSV_METADATA.xml` member.
- Exact task identity `Manage Job Roles` (`ASXS_MANAGE_JOB_ROLES`) and current
  Fusion confirmation that CSV export/import is supported.
- The archive SHA-256, target environment identity, and completed Core Data
  Loader source and metadata validation.
- An unchanged archive from validation through upload.

Reject an archive with a missing, duplicate, unreadable, encrypted, or
ambiguous metadata member. Do not infer an alternative task, data object,
endpoint, or import adapter.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MJR.VALIDATE | step | 1 | validate_input | valid->MJR.DEPENDENCY; invalid->MJR.BLOCKED | none | stop | Before a Manage Job Roles import preview. |
