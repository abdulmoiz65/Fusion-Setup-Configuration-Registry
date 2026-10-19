# Picking Rules Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Developer-provided Data Loader registration and visibility record | inventoryPickingRules is registered and visible as the Picking Rules business object |
| Redwood Picking Rules page and priority LOV chains | Priority display values use the INV_PICK_RULE_ALLOC_PRIORITY lookup type |
| User approval | Supplied boolean values, including `Y` or `N`, are normalized locally without an Advanced Inventory REST verification dependency for AllocateLPNFlag and LPNLocationOnlyFlag |

## FSM Readiness

| Dependency | What Must Happen |
|---|---|
| FSM template source | Discover a project-local template in `project/{project_id}/exports/manufacturing-and-supply-chain-materials-management/inventory-management/picking-rules/`, or obtain a replacement through `shared.setup-export.task-level-export` in template/spec mode. Do not use a populated export, manufacture metadata XML, or package loose CSV files. |
| Template provenance and integrity | Require a task-local receipt with task code, environment identity, compatible Fusion release, ZIP fingerprint, member/header inventory, and zero-data-row result. Verify the receipt against the ZIP before reuse; do not record an environment URL. |
| Native package contract | Preserve `ASM_SETUP_CSV_METADATA.xml`, `ORA_INV_RULE.csv`, `INV_RULE_SELECTION_CRITERION.csv`, and `ORA_INV_RULE_TRANSLATION.csv`. Add only the approved rule row; preserve the exported headers, encoding, member names, and empty child CSVs. |
| Core handoff | Hand the resulting immutable FSM ZIP to `core.data-loader` for final validation, Task Hook review, approval, and submission. |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Data Loader business object | Confirm inventoryPickingRules remains the governed execution route |
| 2 | Supplied boolean flags | Normalize supplied checkbox representations and trimmed case-insensitive `Y` or `N` literals locally without REST verification |
| 3 | Priority lookup | For REST only, resolve any supplied priority display Meaning to LookupCode. FSM preserves supplied priority values unchanged. |
| 4 | Data Loader metadata visibility | Confirm the configured environment exposes inventoryPickingRules before execution planning |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| inventory_picking_rules_bo | Registered Data Loader business object | Yes | Before Data Loader execution | Satisfied | Developer-provided registration record for inventoryPickingRules | | The registered BO is the governed execution route | Use inventoryPickingRules as the Data Loader business object | businessObject |
| inventory_picking_rules_loader_visibility | Data Loader metadata visibility | Yes | Before Data Loader execution | Satisfied | Developer-provided Data Loader visibility record | | The visibility record identifies inventoryPickingRules as Inventory Picking Rules | Recheck registration and environment access if a future metadata request fails | Data Loader metadata visibility |
| picking_rule_boolean_flags | Supplied boolean flags | Conditional | One or more supported boolean fields are supplied | Satisfied | User-provided field value | | The approved local normalization owns selected or empty checkbox representation conversion and `Y`/`N` conversion on the REST route; LPN fields have no REST verification dependency | Supply one supported boolean representation for each field | EnabledFlag, PartialAllowedFlag, SingleLotFlag, AllocateLPNFlag, LPNLocationOnlyFlag: true, false, `Y`, or `N` |
| picking_rule_priority_lookup | Priority sort display-value lookup | Conditional | REST request has one or more priority fields supplied as Meaning instead of LookupCode | Lookup | Developer-provided CRM REST response and Redwood priority LOV chains | resolve_picking_rule_priority | REST Data Loader receives LookupCode while Redwood displays Meaning; FSM values are passed through unchanged. | REST: supply an exact priority Meaning or canonical LookupCode. FSM: preserve the supplied native value. | Priority1Sort, Priority2Sort, Priority3Sort, Priority4Sort: REST LookupCode when resolution applies; FSM supplied value unchanged |
| picking_rules_fsm_template | Verified FSM template | Yes | Before FSM package authoring | Ready when one discoverable template and task-local receipt satisfy task, environment, release, fingerprint, metadata, member/header, and empty-row checks | Project-local template export and receipt, or approved task-level template export | | FSM package structure is Oracle-exported evidence, not inferred from REST fields | Provide a verified template and receipt or approve the routed template/spec export | Immutable Picking Rules FSM template |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The registered BO and its Data Loader visibility record are available for REST, or the classified FSM package passes template readiness | Continue |
| Lookup | A REST priority display value requires conversion to LookupCode | Run the documented read-only lookup |
| Blocked | BO registration or metadata visibility is unavailable, or a REST priority lookup cannot resolve a supplied display Meaning exactly once | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PICKRULES.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->PICKRULES.RESOLVE_PRIORITY;blocked->PICKRULES.RETURN_ISSUES | PICKRULES.NORMALIZE_BOOLEAN_FLAGS | stop | Classified REST requests proceed to the priority node after registered-BO and metadata-visibility readiness checks. |
| PICKRULES.CHECK_FSM_READINESS | step | 41 | resolve_dependency | ready->PICKRULES.FSM_DATALOADER_HANDOFF;blocked->PICKRULES.RETURN_ISSUES | PICKRULES.VALIDATE_FSM_ARCHIVE | stop | Classified FSM package passed native archive validation and its template/receipt checks. |
