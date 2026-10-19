# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Scope | All Business Units record, or one active requisitioning BU | Block preview | Select one supported scope | Every create or update | |
| Defaults | Values for the BPA attributes being changed | Block preview | Supply the intended defaults | Every create or update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Specific BU identity is exact | Reject blank or ambiguous BU identity; let `core.data-loader` and Fusion validate active status | Specific-BU setup | |
| Scope is unambiguous | Reject a mix of All Business Units and specific-BU values in one record | Every record | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPPAD.VALIDATE_INPUT | step | 1 | validate_input | valid->EPPPAD.CHECK_DEPENDENCIES;invalid->EPPPAD.HANDLE_ISSUES | none | stop | Every request |
