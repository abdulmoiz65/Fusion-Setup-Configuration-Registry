---
task_code: "DOO_MANAGE_EXTERNAL_INTERFACE_ROUTING_RULES"
task_name: "Manage External Interface Routing Rules"
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

# Manage External Interface Routing Rules

- **Task code:** `DOO_MANAGE_EXTERNAL_INTERFACE_ROUTING_RULES`
- **Purpose:** Create and update rules that route fulfillment requests to the appropriate external connectors.
- **Manual-only execution rule:** The user completes the approved change manually in the **Manage External Interface Routing Rules** page in Oracle Fusion, with no API, import, automated configuration, or browser automation.

Use the [standard shared manual workflow](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual steps

1. Confirm the approved routing condition, task type, target connector, interface type, service name when applicable, priority, expected payload, controlled test order, and rollback owner. Work in a nonproduction environment first. Confirm that the task type is used by the applicable orchestration-process step, the connector is active and tested, and none of the referenced objects has `_Obsolete` in its name.
2. Open **Navigator** > **My Enterprise** > **Setup and Maintenance**. Select the **Order Management** offering before searching for tasks. In **Tasks**, search for **Manage External Integration Routing Rules for Sales Orders** and open it. The **Manage External Interface Routing Rules** page opens. Review the predefined rules and active custom rules that could match the same request. To inspect a rule, right-click it, select **Actions** > **Edit**, and select **IF** or **DO** to review its logic.
3. For a new rule, select **Create New Rule**, then enter the approved name and description. For an update, open the approved rule and retain all unapproved logic unchanged. Use **Visual Information Builder** consistently; do not mix it with Oracle Business Rules.
4. Define the **IF** condition: select **New Condition**, select the approved attribute, operator, and value, and select **OK**. Add **AND** criteria only where approved. Use the task type used by the orchestration-process step when the rule is intended to route that task type.
5. Define the **THEN** action: select **Then** > **Do** > **New Action** > **Perform an Action**, select **Set Connector Name**, search for and select the approved deployed connector, and select **OK**. Add a secondary action, such as interface type, maximum cancellation wait, service name, aggregation limit, or customer cross-reference resolution, only when it is specified in the approved integration design.
6. Review the priority against every existing rule that can match the same request. Select the rule, set the approved **Priority**, select **Activate Rule**, then select **Save and Close** and **Publish**. A saved routing change is not released until active rules are published.
7. If a controlled test shows incorrect routing, stop further controlled test submissions. Restore the captured prior condition, connector action, priority, or active state; select **Save and Close** and **Publish**; then use a new controlled order to confirm the prior connector and expected payload are restored.

## Manual validation guidance

1. Submit a new controlled sales order that meets the routing condition and confirm the fulfillment line follows the expected orchestration-process step and status.
2. Confirm the expected connector and service endpoint are selected for the outgoing request. Where available, inspect **Flow Trace** for the `EILMainProcess` instance and the **InvokeFulfillmentService** audit entry to verify the approved fulfillment service and connector target in the payload.
3. Submit a negative test order that fails one condition and confirm it follows the expected alternate route. For a threshold rule, test values below, at, and above the approved boundary.
4. Record the order number, fulfillment line, matched condition values, task type, connector, payload evidence, tester, validation result, and any rollback evidence in the approved change record.
