# Design Enforcement

The source describes new territory geography rows. Reject requested update,
upsert, replace or delete intent. This is source intent, not proof of a
server-enforced create-only operation. If the user requires that guarantee,
report the native contract gap before approval.

Require native core CX preflight and an unchanged final archive. Block a
competing SOAP upload, direct Import Activities creation/repair, transport
callback injection, custom `cxUploadContract`, or manually constructed Task
Hook envelope. Do not add unsupported initiation fields to emulate the old
Import Activities payload.

The approved artifact must retain its native CSV headers, identifiers, parent
ordering and paths. Require the final archive SHA-256, selected environment,
Run Book, object and live account to match preflight. Build preview only after
successful Task Hook rule evaluation. Approval is a subsequent core-owned
step; it is not a prerequisite for validating or building the preview.

After approval, core verifies retained integrity/context and uploads the exact
artifact without reopening sources or repeating validation. Accepted initiation
ends this request; query status/errors only for an explicit user request.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.DESIGN | decision | 6 | design_enforcement | pass->TG.PREFLIGHT;fail->TG.ERROR | TG.DEFAULTS | stop | Before preview; enforce new-record intent and native Data Loader execution ownership. |
