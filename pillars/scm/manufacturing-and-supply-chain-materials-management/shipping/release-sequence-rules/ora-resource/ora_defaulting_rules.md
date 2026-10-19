# Client-Side Defaulting Rules

Apply these sourced Redwood UI derivations before downstream Data Loader preparation. They do not inspect Fusion state, invoke a REST endpoint, or replace the Data Loader business-object contract.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Sort1Code through Sort5Code | A | The corresponding Priority1Code through Priority5Code changes to a nonblank value | Yes | |
| Sort1Code through Sort5Code | Clear the corresponding sort value | The corresponding Priority1Code through Priority5Code is cleared | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSR.APPLY_UI_DEFAULTS | decision | 30 | apply_default | applied->RSR.RESOLVE_PRIORITY_CODES;not_applicable->RSR.RESOLVE_PRIORITY_CODES;failed->RSR.HANDLE_ISSUE | RSR.CHECK_LOV_READINESS | stop | A Release Sequence Rules record passes UI-input readiness |
