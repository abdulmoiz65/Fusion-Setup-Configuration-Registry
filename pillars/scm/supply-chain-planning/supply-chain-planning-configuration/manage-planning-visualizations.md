---
task_code: "CUSTOM_PLANNING_VISUALIZATIONS"
task_name: "Manage Planning Visualizations"
parent_skill_id: "scm.supply-chain-planning.supply-chain-planning-configuration"
pillar: "SCM"
offering: "Supply Chain Planning"
functional_area: "Supply Chain Planning Configuration"
functional_area_code: "ORA_MSC_VC_PLANNING_CONFIGURAT"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Planning Visualizations

- **Task code:** CUSTOM_PLANNING_VISUALIZATIONS
- **Purpose:** Create or update a Visualization with the requested measures, dimensions, filters, layout, and access setting.
- **Execution rule:** The user completes the approved change manually in Oracle Supply Chain Planning's Visualizations and Analysis Sets page; no API, import, automated configuration, or browser automation.

Use the standard manual workflow in [shared.common.manual-tasks](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual steps

1. Identify the target plan and whether to create a Visualization or edit an existing one. Establish the name, business question, measures, dimensions and hierarchy levels, filters, Table or Graph choice, layout, and Public or Private access. For a graph, identify its type and the intended axes, slices, groups, or series. Resolve any missing choice that changes the result before entering it. Check the active plan and leave unrelated plan setup unchanged.
2. In Oracle Supply Chain Planning, open **Navigator** > **Supply Chain Planning** > **Supply Planning**. Open the target plan, then choose **More** (...) > **View More** in its header. Under **Actions** > **Pages and Visualizations**, open **Visualizations and Analysis Sets**. Choose **Create Visualization**, or find the existing Visualization and open its edit action.
3. In **Properties**, enter the name and a useful description. Choose the group, **Enable in Plan Type**, Visualization Type, and Public or Private access as requested. Use **Table** for a pivot grid or **Graph** for a chart. On an existing Visualization, the Table or Graph choice is locked; use the graph-type control in Layout when editing a graph. Use **Comparison** when the requested result needs one and the selected type offers it.
4. In **Data**, select the requested measure or measures, then only the dimensions, hierarchies, and levels needed for the result. Check the selected counts. A Data selection does not set its final position in the Layout.
5. Set requested **Measure Criteria** in **Data** after selecting the measure and dimensions. Choose **Add**, a selected measure, the available **Condition**, and **Basis**. Enter a value or comparison measure where required; **Between** needs a second value, while empty and not-empty conditions need neither a basis nor value. Set decimal places only if needed. For combined criteria, set **And or Or** and the calculation **Levels**, hierarchy, and level. Review the criterion in the measure list. If the tab is unavailable or a criterion is incompatible, revisit the measure and dimension choices.
6. Set requested member filters in **Data** > **Members**. Use **Manual** for named members in the hierarchy tree. For an attribute rule, use **Member criteria** and choose its hierarchy, level, attribute, condition, and value when required. Check matched-member counts, returned names, and the filter summary. Choose the filter type before entering a rule because switching can discard unsaved selections; available types and attributes depend on the selected dimension.
7. Set a requested time window in **Data** > **Time Members** when a selected measure has a related Time dimension. Choose the hierarchy and level. Use **Automatic**, a relative range from plan start or today with Before or After and nonnegative period counts, a **Range** with From and To dates inside the plan limits, or explicit periods from the selected-level tree. Check the displayed period range or **Show Selected**. Correct any date or relative-range warning before continuing.
8. In **Layout**, place Table fields by their handles into **Columns**, **Rows**, **Filter bar**, or **Hidden layers**, in the requested order. For a Graph, choose the offered **Graph Type** in **Visualization Properties**. For bar, line, area, or combination graphs, assign hierarchies or **Measures** to X and Y; use Y2 only for individual measures when offered and needed. Set titles, labels, scales, and combination shapes where requested. For pie, set the slice hierarchy and label and hover formats; for bubble, a hierarchy and distinct X, Y, and size measures; for treemap or sunburst, the structure, levels or hierarchy, sizing and color measures, depth or rings, and hover format; for radar, **Group**, **Series**, and 3 to 10 selected measures. Put requested graph filter **Levels** under Layout **Filters** and resolve any conflict with axis hierarchies. These controls are separate from Data member and time filters. In **Visualization Details**, set available legend and data-label options.
9. If **Comparison** is requested and enabled, complete its available controls. Waterfall needs a selected bucket and plan archive; Trend needs a plan archive. A requested MAPE calculation needs a MAPE archive. Resolve any Comparison banner.
10. Review Properties, Data, filters, and Layout together. Preview the Visualization, correct any field or layout warning, and select **Save and Close**.

## Manual validation

- Confirm a unique name, at least one enabled plan type, the intended Table or Graph type and access, at least one measure, and the requested dimensions, hierarchy levels, and filters. Recheck Layout if Data selections changed.
- Check each Measure Criterion's selected measure, condition, required values, combination logic, and calculation levels. Check Manual member names or Member Criteria match counts; correct an unintended zero match or incompatible-filter message. Check time ranges and explicit periods against the plan limits.
- For a Table, verify the fields and their order in each pivot-grid zone. For a Graph with X and Y controls, verify both axes, **Measures** on one axis, no more than three selections across them, no duplicate selection, and compatible Layout filter levels. Check manual scale bounds and increments on each available axis and complete the required fields for the selected graph type.
- Preview the actual table or graph and confirm its values, labels, series, filter controls, and any requested Comparison. Correct any tab or validation message and preview again. After saving, confirm the success message or find the Visualization in the list, accounting for list filters. Record its saved name and plan, type, access, key data selections, filters, and layout, along with any verification limit.