---
task_code: "DOO_MANAGE_ORCHESTRATION_PROCESS_ASSIGNMENT_RULES"
task_name: "Manage Orchestration Process Assignment Rules"
parent_skill_id: "scm.order-management.orders"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Orchestration Process Assignment Rules

**Task code:** `DOO_MANAGE_ORCHESTRATION_PROCESS_ASSIGNMENT_RULES`

**Purpose:** Define the rules that assign an orchestration process to a fulfillment line or an eligible group of fulfillment lines.

**Manual-only execution rule:** The user completes the approved change manually in the Fusion Setup and Maintenance user interface, using the **Manage Process Assignment Rules for Sales Orders** task; no API, import, automated configuration, or browser automation.

Use the standard manual workflow in [shared.common.manual-tasks](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual steps

1. Confirm the approved change identifies the business scenario, intended population, deployed target orchestration process, rule priority, test cases, and rollback owner. Do not proceed if the target process is not deployed or if you cannot access the named task.
2. In **Setup and Maintenance**, first select the **Order Management** offering. Then search for and open **Manage Process Assignment Rules for Sales Orders**. Review the active rules, their priorities, and any custom or predefined rule that could match the same population. Use **View Predefined Rules** or set **View** to **AssignProcess** when needed to determine the evaluation order.
3. For a new rule, select **Create New Rule**, enter a unique meaningful name and a description that states the approved business purpose and scope. For a change, deactivation, or retirement, first capture the current conditions, action, priority, active status, and description so the approved rollback baseline is available.
4. Add or revise the approved IF conditions: select **New Condition**, choose the required header, fulfillment-line, item-definition, or item-category attribute, select the operator, enter or select the approved value, and confirm the resulting condition. For category selection, use **Item Category (Order Fulfill Line)**, not **Category (Order Fulfill Line)**.
5. Add or revise the approved THEN action: select **Then**, **Do**, and **New Action**; select **Process Name (Order Fulfill Line)**; then search for and select the deployed target process. Add further approved conditions or an **Otherwise** branch only when it is the intended default for the orchestration group.
6. Set the approved priority and review the complete rule. Higher-priority rules run first, while the lowest priority runs last and can override earlier assignments; review the predefined **AssignProcess** rule at Medium priority when determining the intended order. Ensure lines in a shipment set, configured item, or kit will resolve to one compatible process.
7. For a temporary suspension, deactivate the rule rather than delete it when restoration may be required. For permanent retirement, confirm no active population relies on it. Activate and publish the approved rule only after peer review and test evidence are complete; record the release time and rule details in the approved change record.

## Manual validation guidance

1. Submit a new sales order that matches every intended condition and confirm the eligible fulfillment line receives the target process. Capture the order number, fulfillment-line details, process name, and evidence.
2. Submit a new sales order that fails one intended condition and confirm it resolves to the approved alternate or default process. When ranges or quantities are used, test values immediately below, at, and above each boundary.
3. When applicable, validate a shipment set, configured item, or kit and confirm all lines resolve to one compatible process. Also test a representative scenario outside the rule scope and confirm its process selection is unchanged.
4. Use new orders for assignment testing. Do not use a revision of an existing line to prove reassignment, because a sales-order revision does not reassign an existing order line to a different orchestration process.
5. Confirm the deployed target process is selectable, the rule name, purpose, conditions, action, and priority match the approved design, overlapping custom and predefined rules have been reviewed, and any default behavior is intentional. Record the release details, validation results, and rollback baseline in the approved change record.
