# Input Validation

## CSV Column Intent Resolution

Resolve the requested business field using this table before validating its value. Accept wording in any language when context identifies one field; ask for clarification when more than one field remains plausible. Unknown offline dynamic membership is recorded as deferred_to_fusion, non-blocking, per the explicit user policy in reference lookups. Retain the supplied CSV-ready representation; clarify only missing or ambiguous required inputs.

| CSV Column | User Intent |
|---|---|
| PJF_PROJECT_TYPE.csv.ProjectType | Name |
| PJF_PROJECT_TYPE.csv.EndDateActive | To Date |
| PJF_PROJECT_TYPE.csv.StartDateActive | From Date |
| PJF_PROJECT_TYPE.csv.EnableBillingFlag | Enable billing |
| PJF_PROJECT_TYPE.csv.EnableCapitalizationFlag | Enable capitalization |
| PJF_PROJECT_TYPE.csv.Description | Description |
| PJF_PROJECT_TYPE.csv.BurdenCostFlag | Enable burdening |
| PJF_PROJECT_TYPE.csv.CostSchOverrideFlag | Allow cost burden schedule change for projects and tasks |
| PJF_PROJECT_TYPE.csv.BurdenAccountFlag | Create expenditure items for burden cost components |
| PJF_PROJECT_TYPE.csv.BurdenAmtDisplayMethod | Burden cost accounting: same or separate expenditure item |
| PJF_PROJECT_TYPE.csv.CapitalCostTypeCode | Cost Type |
| PJF_PROJECT_TYPE.csv.InterfaceCompleteAssetFlag | Require complete asset definition |
| PJF_PROJECT_TYPE.csv.CapitalEventProcessing | Event Processing Method |
| PJF_PROJECT_TYPE.csv.AssetAllocationMethod | Asset Cost Allocation Method |
| PJF_PROJECT_TYPE.csv.VendorInvoiceGroupingCode | Supplier invoice grouping: use grouping method and grouping option |
| PJF_PROJECT_TYPE.csv.CipGroupingMethodCode | Asset Line Grouping Method |
| PJF_PROJECT_TYPE.csv.InterfaceAssetCostCode | Asset-interface state derived from Enable capitalization |
| PJF_PROJECT_TYPE.csv.BurdenCostJournalFlag | Create burden cost accounting journal entries |
| PJF_PROJECT_TYPE.csv.TotalBurdenedJournalFlag | Create burdened cost accounting journal entries |
| PJF_PROJECT_TYPE.csv.CintSchOverrideFlag | Allow override (capitalized interest schedule) |
| PJF_PROJECT_TYPE.csv.SetCode | Set |
| PJF_PROJECT_TYPE.csv.Name | Work Type |
| PJF_PROJECT_TYPE.csv.IndSchName | Default Cost Burden Schedule |
| PJF_PROJECT_TYPE.csv.ElementNumber | Task Name: resolve chosen task to its task number |
| PJF_PROJECT_TYPE.csv.Name1 | Project name owning the selected burden-cost task |
| PJF_PROJECT_TYPE.csv.Name2 | Project Name (burden destination) |
| PJF_PROJECT_TYPE.csv.SponsoredFlag | Enable sponsored projects |
| PJF_PROJECT_TYPE.csv.AutoAssetCreateFlag | Create project assets automatically |
| PJF_PROJECT_TYPE.csv.AutoAssetLineAllocateMode | Allocate only associated costs for automatically created assets |
| PJF_CLASS_CATEGORY.csv.PJF_PROJECT_TYPE.ProjectType | Parent project type Name |
| PJF_CLASS_CATEGORY.csv.ClassCategory | Class Category |
| PJF_CLASS_CATEGORY.csv.MandatoryFlag | Assign to all projects |
| PJF_PROJECT_TYPE_TRANSLATION.csv.PJF_PROJECT_TYPE.ProjectType | Parent project type Name |
| PJF_PROJECT_TYPE_TRANSLATION.csv.Description | Translated Description |
| PJF_PROJECT_TYPE_TRANSLATION.csv.ProjectType | Translated project type Name |
| PJF_PROJECT_TYPE_TRANSLATION.csv.SourceLang | Source language for project type translation |
| PJF_PROJECT_TYPE_TRANSLATION.csv.Language | Translation language |

**Flexfields**

The following DFF columns are grouped here by CSV, following the requested reference format. Resolve deployed context and segment business labels when metadata is available; these ordinal names are not business-intent labels. Preserve untouched values. Grouping preserves known input-shape checks. When target metadata is unavailable, state it has no data source and defer deployed-context/value-set validation non-blockingly to the FSM service.

- **PJF_PROJECT_TYPE.csv**: Attribute1-Attribute10, AttributeCategory.
- **PJF_CLASS_CATEGORY.csv**: AttributeCategory, Attribute1-Attribute15.

Main project-type context uses PJF_PROJECT_TYPES_DESC_FLEX; the class-category assignment uses the separate PJF_PROJ_TYPE_CLASS_CAT_DESC_FLEX. The main embedded context LOV resolves a display name to AttributeCategory's ContextCode. Use each flexfield's deployed metadata when available; otherwise retain supplied context codes and segment values and record non-blocking deferred_to_fusion.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create, update, validate, export, import | Block | Clarify supported intent; delete is unproven | Every request |  |
| Identity | ProjectType and SetCode, or evidenced identifiers/natural-language equivalents | Block | Resolve canonical project-type name and set without requiring exact English wording | Every write | find_project_type |
| Dates | StartDateActive; optional EndDateActive | Block create | From Date maps to StartDateActive; To Date maps to EndDateActive; preserve omitted update values | Create/update |  |
| Option groups | basic, burdening, capitalization, class_categories, translations | Preserve omitted update groups | Use CSV intent mapping; clarify ambiguous schedule or grouping intent | Update | find_project_type |
| Target/artifacts | TargetEnvironment, current_export, package_template | Block | Obtain current target evidence through the declared workflow | Every write/import | verify_project_type_package |

## Minimal Create and Multiple Rows

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Minimum row data | Name, Set, From Date | Block incomplete row | Map Name to ProjectType, resolve Set to SetCode, and map From Date to StartDateActive; the screenshot's prepopulated date is UI evidence only, not a CSV default | Basic create with burdening, capitalization and sponsored behavior disabled |  |
| Optional basic data | Description, To Date, Work Type | Leave unspecified on create | Do not require these fields solely because legacy reference data includes them; apply target package requirements separately | Basic create |  |
| Separate-item burdening | Enable burdening Yes, burden accounting separate (D), default cost burden schedule; optional override and journal choices | Require the schedule; default omitted create options through Standard Defaults | Separate burden items use the raw-cost project/task. Do not require BurdenAccountFlag, Project Name or Task Name as user inputs for this branch; serialize BurdenAccountFlag N on create, not a null | Create with BurdenCostFlag Y and BurdenAmtDisplayMethod D |  |
| Same-item component expenditure items | Burden accounting same (S), Create expenditure items for burden cost components Yes, destination Project Name; optional Task Name | Require the destination project only when component items are explicitly enabled | Omitted create BurdenAccountFlag defaults N. Resolve the project and any supplied task only for enabled component-item routing; a task is optional | BurdenCostFlag Y, BurdenAmtDisplayMethod S and BurdenAccountFlag Y |  |
| Multiple row input | One business-labelled table row per requested project type | Block ambiguous or duplicate name/set identities | Normalize and validate every row independently; report row-specific issues before the immutable batch preview and existing loader approval gate | Multi-row create | find_project_type |
| Legacy setup examples | Existing records and blank optional fields supplied as reference | Do not treat reference records as requested creates | Use fresh identities for new rows; omit unused optional values instead of copying every empty field. The supplied NOVAL marker is not a literal To Date or a valid CSV date | Reference-only setup data accompanying a request |  |

The minimum row data is separate from request-level project/environment selection and the current export/template gates. Requested financial settings supply inherited-behavior evidence; they do not establish downstream production readiness or authorization to load. Do not require billing-design documents or burden-code mappings for task-scoped creation.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Create has verified absence of canonical name and set | Satisfied | Create candidate | find_project_type |
| Update resolves exactly once | Satisfied | Diff against baseline | find_project_type |
| Type is used or supplier treatment changes | Conditional | Apply known use/transfer evidence; if it has no data source, record non-blocking service-layer deferral | resolve_project_type_use |
| Referenced group changes | Conditional | Run each field resolver; validated or explicitly deferred_to_fusion outcomes permit continuation | resolve_project_type_references |
| Default capitalized-interest schedule is requested | Blocked | No CSV destination exists; obtain a supported task contract before proceeding |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Dynamic reference without offline source | Record it has no data source and deferred_to_fusion, blocking=false; preserve supplied CSV-ready values and continue normal upload workflow | Offline source or supplemental eligibility unavailable | resolve_project_type_references |
| Resolve column intent before value | Accept unambiguous business wording in any language; clarify multiple plausible columns | Every request |  |
| ProjectType and translated ProjectType shape | Require nonblank string of at most 240 characters; preserve authored language | Create or supplied translation |  |
| Description shape | Optional string of at most 2000 characters; preserve authored language | Main or translation description supplied |  |
| Date contract | Use StartDateActive and EndDateActive, not FromDate/ToDate as CSV headers; require start on create and non-reversed range; retain target package date representation | Dates supplied |  |
| Yes or No fields | Resolve each scoped option to its canonical Boolean code using the shared table | Scoped Boolean option supplied or required | resolve_project_type_boolean_flags |
| Burden accounting choice | Resolve both radio intents to one shared CSV field | BurdenAmtDisplayMethod supplied or required | resolve_project_type_burden_method |
| Cost Type | Resolve to the canonical code | CapitalCostTypeCode supplied or required | resolve_project_type_capital_cost |
| Asset grouping | Resolve to an eligible canonical code | CipGroupingMethodCode supplied or required | resolve_project_type_asset_grouping |
| Asset allocation | Resolve to an eligible canonical code | AssetAllocationMethod supplied or required | resolve_project_type_asset_allocation |
| Event processing | Resolve to the canonical code; explicit None is not a blank | CapitalEventProcessing supplied or required | resolve_project_type_capital_event |
| Supplier invoice treatment | Resolve coherent checkbox/radio intent without overwriting an explicit choice | VendorInvoiceGroupingCode supplied or required | resolve_project_type_supplier_grouping |
| Set representation | Resolve to canonical SetCode | Set supplied or changed | resolve_project_type_set |
| Work type representation | Resolve to canonical work-type name in Name | Work type supplied or changed | resolve_project_type_work_type |
| Cost burden schedule representation | Resolve to canonical schedule name in IndSchName | Cost burden schedule supplied or required | resolve_project_type_burden_schedule |
| Burden project representation | Resolve destination project name in Name2 | Burden destination project supplied or required | resolve_project_type_burden_project |
| Burden task representation | Resolve task number in ElementNumber and its owning project name in Name1 | Burden task supplied or required | resolve_project_type_burden_task |
| Class-category representation | Resolve canonical category name; do not serialize ClassCategoryId | Class children supplied | resolve_project_type_class_category |
| Parent references | Resolve each child PJF_PROJECT_TYPE.ProjectType to one parent row; translation ProjectType is separately authored translated text | Child members supplied | find_project_type |
| Translation language shape | Require Language and SourceLang, each at most four characters after canonical resolution; do not assume they are equal | Translation rows supplied | resolve_project_type_languages |
| Flexfield shape | AttributeCategory at most 30 characters; each Attribute segment at most 150; apply deployed-context/value-set checks when a source exists, otherwise defer those checks non-blockingly | Main or child DFF supplied | resolve_project_type_flexfields |
| Automatic asset allocation mode | Use the proven DIRECT_COSTS/ALL_COSTS control mapping; reject actual invalid codes or ambiguity, not the absence of seeded meanings | AutoAssetLineAllocateMode supplied or changed | resolve_project_type_auto_asset_mode |
| Hidden asset-interface state | No independent user-selectable transfer mode is established; apply evidenced dependent defaulting, then compare supplied value with that derived state | InterfaceAssetCostCode supplied or capitalization changes |  |
| Package shape | Require exact target base, class-category and translation members, headers and parent relationships | Import preview | verify_project_type_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.VALIDATE_INPUT | step | 1 | validate_input | valid->PTYPE.FIND_TYPE;invalid->PTYPE.RETURN_ISSUES | none | stop | Validate input shape and column intent; value resolution follows |
| PTYPE.ROUTE_OPERATION | decision | 5 | evaluate_result | supported->PTYPE.RESOLVE_DEPENDENCIES;unsupported->PTYPE.RETURN_REFUSAL;invalid->PTYPE.RETURN_ISSUES | PTYPE.APPLY_DEFAULTS | stop | After identity/reference resolution and evidence-backed defaults |

Existing business-design evidence requirements BP-029 and BP-032 are owned by design enforcement.

## Source Alignment

Name/description limits and fixed attribute domains are supported by SRC-EO in [Source Evidence Index](ora_reference_lookups.md#source-evidence-index). CSV headers, child relationships, translation/DFF shape and deployed eligibility must still match the selected current target template/export; source inspection is not a replacement for that runtime gate. Synthetic review fixtures are never accepted as current target evidence.
