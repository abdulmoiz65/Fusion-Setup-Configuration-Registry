# Defaulting Rules

Resolve supplied wording/intent (in any language) before applying defaults. A default never overrides an explicit valid choice unless a documented business transition requires it; conflicting requests require clarification. If a dynamic default's source is unavailable, disclose it has no data source, preserve supplied/omitted update values and defer the unknown default to Fusion; do not block solely for absent offline metadata or invent a value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted group or child collection | Preserve current values and rows | Update | No | find_project_type |
| EndDateActive | Blank | Create with no end date | No |  |
| Class-category assignments | No new assignment rows | Create with no requested class categories; preserve all existing assignments on update | No; do not select a category or apply a child MandatoryFlag default when no assignment is requested |  |
| EnableBillingFlag, EnableCapitalizationFlag, BurdenCostFlag, CostSchOverrideFlag, BurdenAccountFlag, InterfaceCompleteAssetFlag, CintSchOverrideFlag, SponsoredFlag, AutoAssetCreateFlag | N | Create when unspecified and no explicit transition requires otherwise; serialize required fields. BurdenAccountFlag remains N for an omitted component-item choice, including separate-item burdening | No | resolve_project_type_boolean_flags |
| BurdenCostJournalFlag, TotalBurdenedJournalFlag | Y when the resolved create has BurdenCostFlag Y; N otherwise | Create with omitted journal choices; task create policy mirrors the evidenced enable-burdening UI event and serializes the codes explicitly | No; preserve explicit Y/N choices and omitted update values | resolve_project_type_boolean_flags |
| Name2, ElementNumber, Name1 | Blank | Create without enabled same-item component expenditure items; separate-item burdening uses the raw-cost project/task | No; conflicting explicit routing intent needs clarification, not silent removal |  |
| SponsoredFlag burdening transition | Enable burdening | Sponsored newly enabled while burdening is not selected; event-time normalization, not a permanent sponsored invariant | Yes in working request; disclose original/resulting flags and still validate schedule and use-state | resolve_project_type_use |
| AssetAllocationMethod, CapitalEventProcessing | N | Create when omitted, following the nonnull entity defaults; preserve explicit eligible values when capitalization permits them | No |  |
| BurdenAmtDisplayMethod | S | Create with no explicit burden accounting choice | No | resolve_project_type_burden_method |
| VendorInvoiceGroupingCode | G | Initial default with no explicit treatment; not a correction for EI grouping | No; EI with G fails design and needs a resolved M/N choice | resolve_project_type_supplier_grouping |
| PJF_CLASS_CATEGORY.csv.MandatoryFlag | Y when resolved category AutoaccountingFlag is Y; otherwise category MandatoryFlag; N only where the evidenced creation context has no category | New assignment with omitted user choice and complete category default evidence | No; missing category flags defer defaulting to Fusion without blocking or guessing N; preserve any explicit Y/N choice | resolve_project_type_class_category |
| InterfaceAssetCostCode | F when EnableCapitalizationFlag is Y; null otherwise | Create or capitalization changes, following evidenced dependent setter behavior | Reject conflicting independently supplied transfer mode; import setter ordering has not been live-tested |  |
| AutoAssetLineAllocateMode | ALL_COSTS | Create when omitted, following the proven attribute default | No; preserve explicit DIRECT_COSTS or ALL_COSTS | resolve_project_type_auto_asset_mode |

## Create Page Observations

SRC-UI-CREATE captures the supplied blank Create Project Type screenshots on October 9, 2026, with burdening and capitalization disabled. These are displayed initial values, not proof of saved values, enabled-feature defaults, or FSM serialization. Use the Standard Defaults above for the evidenced internal codes.

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Name and Set | Blank; required markers displayed | Blank create page | No; collect both |  |
| From Date | 10/9/26 displayed; required marker present | Supplied blank create screenshots only | No; do not hardcode this date or default an import date from the screenshot |  |
| Description, To Date and Work Type | Blank; no required markers displayed | Supplied blank create screenshots | No |  |
| Enable burdening, billing, capitalization and sponsored projects | Unchecked | Initial create page | No; Standard Defaults serialize N when required |  |
| Default Cost Burden Schedule, Project Name and Task Name | Blank and disabled | Burdening disabled | No |  |
| Allow cost burden schedule change, create burden component items, and both burden journal checkboxes | Unchecked and disabled | Burdening disabled on blank create | No; enabling burdening is a separate UI event |  |
| Burden cost accounting method | Include burden cost on same expenditure item selected; separate-item radio unselected; both disabled | Burdening disabled on blank create | No; Standard Defaults use S |  |
| Cost Type, Asset Line Grouping Method and Default Capitalized Interest Rate Schedule | Blank and disabled | Capitalization disabled | No; do not invent Raw, Expenditure type or a schedule |  |
| Asset Cost Allocation Method and Event Processing Method | None displayed; disabled | Capitalization disabled | No; Standard Defaults use N, which is distinct from a blank |  |
| Use grouping method for supplier invoices | Checked and disabled; new/merged-addition radios unselected | Capitalization disabled on blank create | No; Standard Defaults use G, not Boolean Y |  |
| Require complete asset definition, Allow override, Create project assets automatically, and Allocate only associated costs | Unchecked and disabled | Capitalization disabled on blank create | No; automatic allocation's unchecked control maps to ALL_COSTS, not Boolean N |  |
| Classifications | No data to display | Blank create with no assignments requested | No; create no assignment rows and do not invoke Add Row for an omitted group |  |

SRC-UI-SEPARATE captures the October 12, 2026 screenshots supplied with this repair request. It is a configured, unsaved create page, not another blank-create default observation.

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Enable burdening and Enable billing | Checked | Supplied configured create page | No; reflects this request's selections, not a universal create default |  |
| Burden accounting method | Create separate expenditure item for burden cost selected | Supplied configured create page | No; resolve to D | resolve_project_type_burden_method |
| Component-item checkbox, Project Name and Task Name | Unchecked/blank and disabled | Separate-item burdening selected | No; do not request these disabled inputs. The create default N is independently supported by SRC-EO |  |
| Allow cost burden schedule change and both burden journal checkboxes | Checked | Supplied configured create page | No; override permission is explicit in the request; omitted create journal choices use Standard Defaults |  |
| Default Cost Burden Schedule | Blank with required marker | Burdening enabled on supplied page | No; collect or resolve the requested schedule | resolve_project_type_burden_schedule |
| Capitalization controls | Disabled; None for allocation/event and checked supplier grouping | Enable capitalization unchecked on supplied page | No; do not request inactive asset settings; use established disabled-state codes |  |
| Classifications | No data to display | No assignments requested | No; create no child rows |  |

The displayed From Date 10/12/26 is not an import default. Journal defaults above are an explicit task policy for new creates, not a claim that FSM imports execute UI listeners. Updates continue to preserve omitted groups; do not clear existing destinations or reset journals from a screenshot.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.APPLY_DEFAULTS | step | 4 | apply_default | applied->PTYPE.ROUTE_OPERATION;failure->PTYPE.RETURN_ISSUES | PTYPE.RESOLVE_REFERENCES | stop | Apply evidence-backed defaults after references resolve or are explicitly deferred; leave unknown dynamic defaults to Fusion |

## UI Behavior Boundaries

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| UI burden-cost and total-burden journal selections | Selected | Burdening changes to enabled, including enabling Sponsored while burdening was disabled | Yes at that UI event; preserve subsequent explicit choices and do not repeat on unrelated updates | |
| UI burden destination project/task and journal selections | Clear destination project/task and unselect both journals | Burdening changes to disabled | Yes in working UI state; the schedule and project-level-change option are not automatically cleared by this interaction | |
| UI capitalization options | Asset allocation and capital-event processing become None; capital-cost type, grouping method and schedule clear; complete-asset, schedule-override, automatic-asset-creation and automatic-allocation selections become false; supplier-invoice grouping is selected | Capitalization changes to disabled | Yes in working UI state; do not translate these UI selections into import codes without an established mapping | |

Enabling Sponsored while burdening is already enabled leaves the journal choices unchanged. Disabling a control alone does not prove a value reset. In-use restrictions and parent-option conditions continue to govern whether controls can be changed.

Keep the supported create omission policy and explicit update scope. Disclose original and resulting working values for applied normalization; do not infer import resets or permission to overwrite existing rows.

## Source Alignment

See [Source Evidence Index](ora_reference_lookups.md#source-evidence-index): SRC-EO proves the N/S/G and ALL_COSTS defaults and nonnull asset-allocation/event fields; SRC-EOIMPL proves the dependent F/null setter. SRC-UI supports the event-time sponsored/burdening and capitalization resets; SRC-UI-SEPARATE corroborates selected journals and disabled component/destination controls. SRC-UI-CREATE records the initial displayed states separately. The burden-enabled create journal policy explicitly serializes Y/Y rather than relying on import ordering. These observations do not authorize overwriting omitted update groups. Preservation is SRC-FSCR policy; category-dependent defaults still require current category evidence.
