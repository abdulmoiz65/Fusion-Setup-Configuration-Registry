# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Priority type lookup contract | Verify the complete read-only Fusion endpoint and response mapping before resolving a friendly priority value |
| 2 | Sort lookup contract | Verify the complete read-only Fusion endpoint and response mapping before resolving a friendly sort value |
| 3 | sequenceDFF schema and context | Preserve blank FSM DFF/attribute columns when no DFF value is supplied; obtain a fresh task-specific template before supplying a DFF value |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| priority_type_lookup_contract | Pick sequence rule type lookup contract | Yes | A priority is supplied as a user-facing value rather than a backend code | Lookup | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` through `core.fusion-api.rest-api-client` using the selected environment | resolve_pick_sequence_rule_type | The approved core-routed standard lookup resolver maps a priority meaning to its code | Provide a priority meaning or backend code | Priority1Code through Priority5Code |
| sort_lookup_contract | Pick sequence rule sort lookup contract | Yes | A sort is supplied as a user-facing value rather than a backend code | Lookup | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` through `core.fusion-api.rest-api-client` using the selected environment | resolve_pick_sequence_rule_sort | The approved core-routed standard lookup resolver maps a sort meaning to its code | Provide a sort meaning or backend code | Sort1Code through Sort5Code |
| sequence_dff_schema | Release Sequence Rules additional-information DFF schema | Conditional | A REST sequenceDFF value or an FSM DFF/attribute value is supplied | Blocked | A successful FSM import contained the exported blank DFF/attribute columns; populated DFF context and segment metadata must come from a fresh task-specific template | | The validated FSM archive needs no DFF value when those columns are blank; a populated DFF remains schema-dependent | Obtain a fresh task-specific template before supplying DFF values | sequenceDFF context and segment attributes |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | A complete approved read-only resolver contract is available | Yes |
| Blocked | A DFF value is supplied without a verified task-specific template context and segment schema | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSR.CHECK_LOV_READINESS | decision | 20 | resolve_dependency | ready->RSR.APPLY_UI_DEFAULTS;blocked->RSR.HANDLE_ISSUE | RSR.VALIDATE_UI_INPUT | stop | A supplied priority or sort needs display-value resolution |
| RSR.CHECK_DFF_READINESS | decision | 60 | resolve_dependency | ready->RSR.DONE;not_applicable->RSR.DONE;blocked->RSR.HANDLE_ISSUE | RSR.RESOLVE_SORT_CODES | stop | A REST sequenceDFF value or an FSM DFF/attribute value is supplied |
