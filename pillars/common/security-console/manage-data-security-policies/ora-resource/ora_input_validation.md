# Input Validation

## Import Requirements

Before an approval preview require a non-empty, readable, unencrypted FSM ZIP
with exactly one `ASM_SETUP_CSV_METADATA.xml` member; exact task identity
`Manage Data Security Policies` (`ASXS_MANAGE_DATA_SECURITY_POLICIES`); current
confirmation of CSV export/import support; archive SHA-256; target environment
identity; and completed Core Data Loader source and metadata validation. The ZIP
must remain unchanged through upload. A modified export has a new hash and must
be revalidated.

Reject missing, duplicate, unreadable, encrypted, or ambiguous metadata. Do not
infer an alternative task, endpoint, or import adapter.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MDSP.VALIDATE | step | 1 | validate_input | valid->MDSP.DEPENDENCY; invalid->MDSP.BLOCKED | none | stop | Before a Manage Data Security Policies import preview. |
