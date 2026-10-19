# Design Enforcement

## Import Controls

Route every import only through `core.data-loader`. Require its immutable
approval preview and Task Hook validation bound to the archive SHA-256. Do not
use direct FSM APIs, UCM uploads, REST utilities, browser actions, or a
reconstructed approval envelope.

Data-security exports can contain sensitive policy grants and conditions. Do not
claim safety until target, task identity, archive hash, Data Loader validation,
same-environment confirmation where needed, and separate immediate approval are
all present.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MDSP.DESIGN_GATE | decision | 3 | design_enforcement | pass->MDSP.EXECUTION_GATE; fail->MDSP.BLOCKED | MDSP.DEPENDENCY | stop | Before building the immutable Data Loader import preview. |
