# Configure Subinventories Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Implementation owner confirmation | External BO registration is complete for subinventories, subinventoryItems, and locatorItems in that order |
| Live Data Loader metadata checks | The configured target exposes subinventories, subinventoryItems, and locatorItems |
| User routing requirement | Locators are child setup data under subinventories and use FSM only; subinventories, subinventoryItems, and locatorItems support REST by default or explicitly selected FSM |
| User-approved FSM template policy | Reuse a verified project-local empty template-only export and refresh it only on a defined validation failure or explicit user request |
| User-approved locator structure resolver contract | Resolve an enabled locator structure code or name to the canonical `StructureInstanceCode` and `StructureInstanceName` for REST and FSM route mapping |
| LOV Analysis for Name to ID Resolution: Configure Subinventories, 14-Aug-2026 | Parent context dependencies and conditional standard-lookup resolution scope |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Object-level route selection | Classify every requested row before artifact preparation. Locators require FSM; the three registered business objects default to REST and may use explicitly selected FSM. |
| 2 | Registered business objects | Preserve the approved REST execution order: subinventories, subinventoryItems, locatorItems. |
| 3 | Data Loader metadata visibility | Confirm live metadata visibility only for each registered business object selected for the REST route. |
| 4 | FSM locator template | For locator rows, reuse a verified project-local empty template-only export or obtain a replacement with `--template-only` only when required. Never use a current-data export as the package source. |
| 5 | FSM locator package | Add only the requested locator rows to the verified empty template, retain the parent subinventory identity, and do not create a REST business-object source. |
| 6 | Subinventory Header values | Resolve any supplied header display values before their values are handed to the selected import route. |
| 7 | Locator structure normalization | When a Locator Structure value is supplied, resolve it to one enabled canonical code/name pair. Use `StructureInstanceName` for REST Subinventories and `StructureInstanceCode` for FSM Subinventories and locators. |
| 8 | Locator values | Resolve any supplied locator display values in the selected subinventory context. |
| 9 | Subinventory Item Association values | Resolve any supplied item-association display values in the selected organization and item context. |
| 10 | Locator Item values | Resolve any supplied locator-item display values after the applicable subinventory and CountMethod context is available. |
| 11 | Import handoff | Hand off only when all applicable route, template, artifact, and lookup dependencies are satisfied. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| subinventories_bo | Registered Data Loader business object: subinventories | Yes | Before Data Loader execution | Satisfied | Implementation owner confirmation and live metadata check |  | It owns the subinventory header flow | Use subinventories first in the approved execution order | businessObject |
| subinventory_items_bo | Registered Data Loader business object: subinventoryItems | Yes | Before Data Loader execution | Satisfied | Implementation owner confirmation and live metadata check |  | It owns the subinventory item association flow | Use subinventoryItems after subinventories | businessObject |
| locator_items_bo | Registered Data Loader business object: locatorItems | Yes | Before Data Loader execution | Satisfied | Implementation owner confirmation and live metadata check |  | It owns the locator item flow | Use locatorItems after subinventoryItems | businessObject |
| configured_subinventories_loader_visibility | Data Loader metadata visibility | Yes | Before Data Loader execution | Satisfied | Live metadata checks for subinventories, subinventoryItems, and locatorItems |  | The configured environment exposes every registered BO | Recheck visibility if the target environment changes | Registered BO metadata |
| locator_fsm_route | Locator child-object route | Yes | Locator rows are requested | Verify | User routing requirement and immutable task-scoped FSM ZIP |  | Locators are not a registered REST business object for this task | Keep locator rows in the FSM ZIP with their parent subinventory identity; do not prepare a REST, REST-BO, DAT, or XLSX source | FSM ZIP and parent subinventory identity |
| locator_fsm_template | Verified empty Configure Subinventories template | Yes | Locator rows are requested | Verify | Project-local `setupTaskCSVTemplateExports` artifact or a replacement produced with `--template-only` |  | Prevents existing setup data from being copied into a locator import package | Reuse the local template only when task, environment, compatible release, fingerprint, manifest, member/header, and empty-row checks pass; otherwise export a replacement empty template | Template ZIP path, task code, environment identity, release evidence, fingerprint, member inventory, headers, and empty-row result |
| locator_fsm_template_refresh | Replacement empty template export | Conditional | The local template is missing, unverifiable, incompatible, changed, structurally invalid, or the user explicitly requests refresh | Verify | `shared.setup-export.task-level-export --template-only` |  | Avoids unnecessary Fusion export jobs while failing closed on unsafe cached templates | Do not refresh a template that passes every reuse check | Replacement template path and provenance receipt |
| locator_structure_instance | Enabled locator structure canonical pair | Conditional | A Locator Structure value is supplied for REST or FSM Subinventories, or for an FSM locator row | Lookup | `locatorStructureInstances` filtered by `StructureInstanceEnabled = 'Y'` | resolve_locator_structure_instance | REST accepts the canonical `StructureInstanceName` as `LocatorStructureMeaning`; FSM accepts the canonical `StructureInstanceCode` | Supply one Locator Structure value as a code or name; if both are supplied separately, they must identify the same row | `StructureInstanceCode`, `StructureInstanceName`, then route-specific target field |
| selected_rest_object_visibility | Selected REST business-object visibility | Conditional | A REST source is requested for subinventories, subinventoryItems, or locatorItems | Verify | Live Data Loader metadata check for each selected registered business object |  | REST metadata is relevant only for objects using the REST route | Verify only the selected REST business objects; locator rows never satisfy this dependency | Registered BO metadata |
| header_subinventory_type | Subinventory Header: Subinventory Type | Conditional | A Subinventory Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_SUB_TYPE | resolve_subinventory_type | The UI displays Meaning and stores LookupCode | Provide a valid Subinventory Type display value | SubinventoryType |
| header_cancel_backorders | Subinventory Header: Cancel Backorders | Conditional | A Cancel Backorders display value is supplied | Lookup | standardLookupsLOV LookupType ORA_INV_TO_FILLKILL_OPTIONS excluding ORG_LEVEL | resolve_cancel_backorders | The UI displays Meaning and stores LookupCode | Provide a valid eligible Cancel Backorders display value | FillKillToLookup |
| header_locator_control | Subinventory Header: Locator Control Type | Conditional | A Locator Control Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_SUB_LOCATOR_CONTROL excluding code 1 | resolve_locator_control_type | The UI displays Meaning and stores LookupCode | Provide a valid eligible Locator Control Type display value | LocatorControl |
| header_count_method | Subinventory Header: Replenishment Count Method | Conditional | A Replenishment Count Method display value is supplied | Lookup | standardLookupsLOV LookupType ORA_REPLENISHMENT_COUNT_METHOD | resolve_header_count_method | The UI displays Meaning and stores LookupCode | Provide a valid Replenishment Count Method display value | CountMethod |
| header_default_count_type | Subinventory Header: Default Replenishment Count Type | Conditional | A header Default Replenishment Count Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_DEFAULT_REPLEN_COUNT_TYPE excluding code 3 | resolve_header_default_count_type | The UI displays Meaning and stores LookupCode | Provide a valid eligible header Default Replenishment Count Type display value | DefaultCountTypeCode |
| header_sourcing_type | Subinventory Header: Sourcing Type | Conditional | A header Sourcing Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_SOURCE_TYPES | resolve_header_sourcing_type | The UI displays Meaning and stores LookupCode | Provide a valid header Sourcing Type display value | SourcingType |
| locator_type | Locator: Locator Type | Conditional | A Locator Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_LOCATOR_TYPES | resolve_locator_type | The UI displays Meaning and stores LookupCode | Provide a valid Locator Type display value | Locator type field |
| locator_lpn_enabled | Locator: LPN Enabled | Conditional | An LPN Enabled display value is supplied | Lookup | standardLookupsLOV LookupType YES_NO | resolve_lpn_enabled | The UI displays Meaning and stores LookupCode | Provide a valid Yes or No display value | LPN enabled flag |
| item_planning_method | Subinventory Item Association: Inventory Planning Method | Conditional | An Inventory Planning Method display value is supplied | Lookup | standardLookupsLOV LookupType INV_MATERIAL_PLANNING excluding code 1 | resolve_inventory_planning_method | The UI displays Meaning and stores LookupCode | Provide a valid eligible Inventory Planning Method display value | MinimumMaximumPlanningCode |
| item_default_count_type | Subinventory Item Association: Default Replenishment Count Type | Conditional | An item-association Default Replenishment Count Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_DEFAULT_REPLEN_COUNT_TYPE excluding code 3 | resolve_item_default_count_type | The UI displays Meaning and stores LookupCode | Provide a valid eligible item-association Default Replenishment Count Type display value | DefaultCountTypeCode |
| item_sourcing_type | Subinventory Item Association: Sourcing Type | Conditional | An item-association Sourcing Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_SOURCE_TYPES | resolve_item_sourcing_type | The UI displays Meaning and stores LookupCode | Provide a valid item-association Sourcing Type display value | SourceType |
| item_minmax_enabled | Subinventory Item Association: Min-Max Enabled | Conditional | A Min-Max Enabled display value is supplied | Lookup | standardLookupsLOV LookupType YES_NO | resolve_minmax_enabled | The UI displays Meaning and stores LookupCode | Provide a valid Yes or No display value | Min-max enabled flag |
| locator_item_default_count_type | Locator Item: Default Replenishment Count Type | Conditional | A locator-item Default Replenishment Count Type display value is supplied | Lookup | standardLookupsLOV LookupType INV_DEFAULT_REPLEN_COUNT_TYPE with CountMethod context | resolve_locator_item_default_count_type | The UI documents a CountMethod-dependent flow and stores LookupCode | Provide CountMethod context and a valid locator-item Default Replenishment Count Type display value | DefaultCountTypeCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable display-value resolver returns exactly one eligible LookupCode, every locator package derives from a verified empty template, every locator row has an FSM package, and every selected REST object remains visible | Continue to the import handoff gate |
| Lookup | A supplied display value requires standardLookupsLOV resolution | Read-only lookup only |
| Blocked | A locator row is prepared for REST, a locator package derives from a current-data export, the cached template cannot be verified, a locator structure has no unique enabled code-or-name match or conflicting inputs resolve to different rows, a required parent context is unavailable, a value is excluded, or another resolver has no exact unique result | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSUBINV.CHECK_DEPENDENCIES | decision | 170 | resolve_dependency | ready->CSUBINV.DATA_LOADER_HANDOFF;blocked->CSUBINV.HANDLE_LOOKUP_ERROR | CSUBINV.RESOLVE_LOCATOR_ITEM_DEFAULT_COUNT_TYPE | stop | All applicable route, empty-template provenance, artifact, and Configure Subinventories standard-lookup dependencies have completed. |
