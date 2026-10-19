# Configure Subinventories Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| LOV Analysis for Name to ID Resolution: Configure Subinventories, 14-Aug-2026 | UI/BO flow scope, implementation fields, display-to-code resolution, exclusions, and context-sensitive LOV behavior |
| Redwood Configure Subinventories flow and dynamic layouts in inventory-setup-ui | Documents checkbox controls and the canonical values supplied to the subinventories, subinventoryItems, and locatorItems payloads |
| User decision | Resolve every LOV marked Yes through task-local standard lookup guidance |
| User-approved normalization rule | Defines friendly-value normalization before Data Loader handoff |
| User routing requirement | Defines REST-default and FSM-only import routing for the requested object scope |
| User-approved FSM template policy | Requires locator packages to use a verified reusable empty template-only export and forbids current-data exports as package sources |
| User-approved locator structure resolver contract | Resolves a Locator Structure code or name to both canonical structure fields, then maps the name to REST and the code to FSM |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Leave required fields, lengths, uniqueness, server-side domains, and final record validation to Data Loader and Fusion. |
| Local validation ownership | Normalize only the documented checkbox/friendly values and validate sourced display-value resolution conditions, exact-match behavior, exclusions, and documented parent context needed before a selected resolver. |
| REST execution | Use standardLookupsLOV only for read-only resolution; core.data-loader owns all execution. |
| Object-level import routing | Classify requested rows as subinventories, subinventoryItems, locatorItems, or locators before artifact preparation. Locators are FSM-only; the other three objects allow FSM and REST with REST as the default. |
| FSM locator template provenance | Use only a verified empty template-only export for the same task, environment, and compatible release. Reuse a valid project-local template; refresh it only when required by provenance, integrity, compatibility, or structure checks. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Subinventory Header LOV display value | Subinventory Type, Cancel Backorders, Locator Control Type, Replenishment Count Method, Default Replenishment Count Type, or Sourcing Type display value | Not applicable when none of these values is supplied | Supply a display value only when the corresponding header setting is in scope | A subinventory header LOV setting is supplied by display value |  |
| Locator LOV display value | Locator Type or LPN Enabled display value | Not applicable when neither value is supplied | Supply a display value only when the corresponding locator setting or search facet is in scope | A locator LOV setting is supplied by display value |  |
| Subinventory Item Association LOV display value | Inventory Planning Method, Default Replenishment Count Type, Sourcing Type, or Min-Max Enabled display value | Not applicable when none of these values is supplied | Supply a display value only when the corresponding item-association setting or search facet is in scope | A subinventory item association LOV setting is supplied by display value |  |
| Locator Item LOV display value | Default Replenishment Count Type display value | Not applicable when it is not supplied | Supply a display value only when the corresponding locator-item setting is in scope | A locator-item LOV setting is supplied by display value |  |
| Subinventory checkbox or friendly value | Quantity Tracked, Asset Subinventory, Depreciable, PAR Location, Offline Counting, Oracle Health Location, Auto Create Delivery, WMS flags, LPN Controlled Subinventory, or Full LPN value | Not applicable when none is supplied | Supply one documented friendly value for the corresponding field | A normalized subinventory attribute is supplied |  |
| Subinventory or locator item Full LPN value | Full LPN value | Not applicable when it is not supplied | Supply one documented Boolean-friendly value | A normalized Full LPN attribute is supplied |  |
| Locator item Count Required value | Count Required value | Not applicable when it is not supplied | Supply one documented friendly value | A normalized locator-item Count Required attribute is supplied |  |
| Object-level import route | Requested object scope and selected route: REST or FSM | Stop before artifact preparation | Identify each requested object and select its supported route | Any import source is prepared |  |
| FSM locator template | Project-local template-only ZIP, task code, source environment, compatible release evidence, stored fingerprint, member inventory, CSV headers, and empty-row verification | Stop before FSM package preparation | Reuse a verified local empty template or export a replacement with `--template-only` | Locator rows are requested |  |
| Locator structure resolution | Locator Structure, `LocatorStructureMeaning`, or Structure Instance Code | Not applicable when no Locator Structure value is supplied | Supply one logical locator-structure value and resolve it to the canonical code/name pair through the enabled locator structure instances | A Locator Structure value is supplied for REST or FSM Subinventories, or for an FSM locator row | resolve_locator_structure_instance |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Subinventory Type display value is supplied | Continue only after one eligible INV_SUB_TYPE value resolves | Fill SubinventoryType with LookupCode | resolve_subinventory_type |
| A Cancel Backorders display value is supplied | Continue only after one eligible ORA_INV_TO_FILLKILL_OPTIONS value resolves | Fill FillKillToLookup with LookupCode | resolve_cancel_backorders |
| A Locator Control Type display value is supplied | Continue only after one eligible INV_SUB_LOCATOR_CONTROL value resolves | Fill LocatorControl with LookupCode | resolve_locator_control_type |
| A header Replenishment Count Method display value is supplied | Continue only after one ORA_REPLENISHMENT_COUNT_METHOD value resolves | Fill CountMethod with LookupCode | resolve_header_count_method |
| A header Default Replenishment Count Type display value is supplied | Continue only after one eligible INV_DEFAULT_REPLEN_COUNT_TYPE value resolves | Fill DefaultCountTypeCode with LookupCode | resolve_header_default_count_type |
| A header Sourcing Type display value is supplied | Continue only after one INV_SOURCE_TYPES value resolves | Fill SourcingType with LookupCode | resolve_header_sourcing_type |
| A Locator Type display value is supplied | Continue only after one INV_LOCATOR_TYPES value resolves | Fill the documented locator type field with LookupCode | resolve_locator_type |
| A Locator Structure value is supplied for a supported REST or FSM route | Continue only after exactly one distinct enabled locator structure row matches the supplied value by code or name | Retain the matched row's `StructureInstanceCode` and `StructureInstanceName` as the canonical pair | resolve_locator_structure_instance |
| REST Subinventories is selected after locator-structure resolution | Continue only with the canonical pair | Fill `LocatorStructureMeaning` with the returned `StructureInstanceName` | resolve_locator_structure_instance |
| FSM Subinventories or locators is selected after locator-structure resolution | Continue only with the canonical pair | Fill `StructureInstanceCode` with the returned `StructureInstanceCode` | resolve_locator_structure_instance |
| An LPN Enabled display value is supplied | Continue only after one YES_NO value resolves | Fill the LPN enabled flag with LookupCode | resolve_lpn_enabled |
| An Inventory Planning Method display value is supplied | Continue only after one eligible INV_MATERIAL_PLANNING value resolves | Fill MinimumMaximumPlanningCode with LookupCode | resolve_inventory_planning_method |
| An item-association Default Replenishment Count Type display value is supplied | Continue only after one eligible INV_DEFAULT_REPLEN_COUNT_TYPE value resolves | Fill DefaultCountTypeCode with LookupCode | resolve_item_default_count_type |
| An item-association Sourcing Type display value is supplied | Continue only after one INV_SOURCE_TYPES value resolves | Fill SourceType with LookupCode | resolve_item_sourcing_type |
| A Min-Max Enabled display value is supplied | Continue only after one YES_NO value resolves | Fill the Min-max enabled flag with LookupCode | resolve_minmax_enabled |
| A locator-item Default Replenishment Count Type display value is supplied | Continue only after CountMethod is available as context and one INV_DEFAULT_REPLEN_COUNT_TYPE value resolves | Fill DefaultCountTypeCode with LookupCode | resolve_locator_item_default_count_type |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact display-value resolution | Trim outer whitespace and match Meaning case-insensitively exactly; do not fuzzy-match, contains-match, or select the first candidate | Any selected standard lookup resolver runs |  |
| Excluded Cancel Backorders code | Reject an exact match whose LookupCode is ORG_LEVEL | resolve_cancel_backorders runs | resolve_cancel_backorders |
| Excluded Locator Control code | Reject an exact match whose LookupCode is 1 | resolve_locator_control_type runs | resolve_locator_control_type |
| Excluded Default Replenishment Count Type code | Reject an exact match whose LookupCode is 3 for the documented header and subinventory-item flows | resolve_header_default_count_type or resolve_item_default_count_type runs |  |
| Excluded Inventory Planning Method code | Reject an exact match whose LookupCode is 1 | resolve_inventory_planning_method runs | resolve_inventory_planning_method |
| Locator-item count-type context | Retain CountMethod as context evidence; do not infer an undocumented narrower REST filter | resolve_locator_item_default_count_type runs | resolve_locator_item_default_count_type |
| Object-level route selection | Allow REST or FSM for subinventories, subinventoryItems, and locatorItems; default an unspecified route to REST for only those registered objects. Allow locators only in an FSM package and reject any locator row in a REST, REST-BO, DAT, or XLSX business-object source. | Any import source is prepared |  |
| Canonical locator structure | Run `resolve_locator_structure_instance` for every supplied Locator Structure value in supported REST or FSM Subinventories and FSM locator rows. Write the canonical name to REST `LocatorStructureMeaning` and the canonical code to FSM `StructureInstanceCode`. | A Locator Structure value is supplied | resolve_locator_structure_instance |
| Locator structure input consistency | If separate locator-structure name and code inputs are supplied, require both to resolve to the same enabled row; otherwise block as conflicting input. | More than one locator-structure input field is supplied | resolve_locator_structure_instance |
| FSM locator template provenance | Require a template produced through `setupTaskCSVTemplateExports` for `ORA_INV_CONFIGURE_SUBINVENTORIES`; reject a current-data `setupTaskCSVExports` artifact even if its existing rows were later removed. | An FSM locator package is prepared |  |
| Reusable template validation | Require matching task and environment identity, compatible target release, matching stored fingerprint, exactly one `ASM_SETUP_CSV_METADATA.xml`, expected CSV members and headers, and no current setup-data rows before requested locator rows are added. | A project-local template is reused |  |
| Template refresh | Export a replacement with `--template-only` only when no reusable template exists, a validation check fails, environment/release compatibility changes, expected structure changes, or the user explicitly requests refresh. | Template acquisition is required |  |
| Baseline separation | Keep an explicitly requested current-configuration export separate from the template and never use it as the locator FSM package source. | A baseline export also exists |  |

## Value Normalization

| BO / UI Area | Backend Attribute | Friendly Values for Enabled | Friendly Values for Disabled | Canonical Output | Applies When | Source-backed UI Mapping |
|---|---|---|---|---|---|---|
| subinventories | QuantityTracked | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | Quantity Tracked checkbox maps checked to 1 and unchecked to 2. |
| subinventories | AssetSubinventory | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | Asset Subinventory checkbox maps checked to 1 and unchecked to 2. |
| subinventories | Depreciable | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | Depreciable checkbox maps checked to 1 and unchecked to 2. |
| subinventories | ParLocation | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | PAR Location checkbox maps checked to 1 and unchecked to 2. |
| subinventories | OfflineCounting | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | Offline Counting checkbox maps checked to 1 and unchecked to 2. |
| subinventories | OracleHealthLocation | Yes, Y, true, 1 | No, N, false, 2 | Y or N | Value is supplied | Oracle Health Location checkbox maps checked to Y and unchecked to N. |
| subinventories | AutoCreateDelivery | Yes, Y, true, 1 | No, N, false, 2 | Y or N | Value is supplied | Auto Create Delivery checkbox maps checked to Y and unchecked to N. |
| subinventories | UseSubinventoryForManufacturingAndMaintenanceInWmsCode | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied and the WMS option is applicable | WMS subinventory checkbox maps checked to 1 and unchecked to 2. |
| subinventories | UsePackingUnitForProductCompletionAndReturnCode | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied and the WMS option is applicable | WMS packing-unit checkbox maps checked to 1 and unchecked to 2. |
| subinventories | LPNControl | Yes, Y, true, 1 | No, N, false, 0 | 1 or 0 | Value is supplied | LPN Controlled Subinventory checkbox maps checked to 1 and unchecked to 0. |
| subinventories | FullLPNFlag | Yes, Y, true, 1 | No, N, false, 0 | true or false | Value is supplied and LPN Control is enabled | Full LPN checkbox is passed as a Boolean. |
| subinventoryItems | FullLPNFlag | Yes, Y, true, 1 | No, N, false, 0 | true or false | Value is supplied | Subinventory Item Full LPN checkbox is passed as a Boolean. |
| locatorItems | CountRequired | Yes, Y, true, 1 | No, N, false, 2 | 1 or 2 | Value is supplied | Count Required checkbox maps checked to 1 and unchecked to 2. |
| locatorItems | FullLPNFlag | Yes, Y, true, 1 | No, N, false, 0 | true or false | Value is supplied | Locator Item Full LPN checkbox is passed as a Boolean. |

## Normalization Rules

| Rule | What Happens |
|---|---|
| Match behavior | Trim outer whitespace and match the documented friendly values case-insensitively and exactly. |
| Blank value | Preserve a blank value; do not locally apply a default. |
| Recognized value | Replace a supplied friendly value with the field's documented canonical output before Data Loader handoff. |
| Unsupported or conflicting value | Stop and request one supported value; do not fuzzy-match, infer, or coerce an undocumented value. |
| UI side effects | Do not locally apply checkbox-driven clearing or defaulting; Data Loader and Fusion own backend validation and the user has not approved UI-parity defaulting rules. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSUBINV.VALIDATE_LOOKUP_INPUTS | step | 10 | validate_input | valid->CSUBINV.VALIDATE_IMPORT_ROUTE;invalid->CSUBINV.HANDLE_LOOKUP_ERROR | CSUBINV.APPLY_SUBINVENTORY_IDENTITY_DEFAULT | stop | After Subinventory Code and Translatable Subinventory Name defaulting; before checkbox normalization, LOV resolution, and import-route selection. |
| CSUBINV.VALIDATE_IMPORT_ROUTE | step | 15 | validate_input | valid->CSUBINV.RESOLVE_HEADER_SUBINVENTORY_TYPE;invalid->CSUBINV.HANDLE_LOOKUP_ERROR | CSUBINV.VALIDATE_LOOKUP_INPUTS | stop | Before artifact preparation. Classify locators as FSM-only, validate empty-template provenance when locators are requested, and route the three registered business objects to REST by default unless FSM is explicitly selected. |
