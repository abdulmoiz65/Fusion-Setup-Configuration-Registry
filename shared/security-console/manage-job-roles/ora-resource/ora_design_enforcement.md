# Design Enforcement

## Import Controls

Route every import only through `core.data-loader`. Require its immutable
approval preview and its Task Hook validation envelope bound to the archive
SHA-256. Do not use a direct FSM API, UCM upload, REST utility, browser action,
or reconstructed approval envelope.

The export can contain role hierarchy and privilege-membership data. Do not
claim that import is safe until the target environment, exact task identity,
archive hash, Data Loader validation, same-environment confirmation when
applicable, and separate immediate upload approval are all present.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MJR.DESIGN_GATE | decision | 3 | design_enforcement | pass->MJR.EXECUTION_GATE; fail->MJR.BLOCKED | MJR.DEPENDENCY | stop | Before building the immutable Data Loader import preview. |
