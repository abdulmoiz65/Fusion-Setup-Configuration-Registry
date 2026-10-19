---
task_code: "ORA_FOM_MANAGE_ORDER_APPROVAL_RULES"
task_name: "Manage Order Approval Rules"
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

# Manage Order Approval Rules

- **Task code:** `ORA_FOM_MANAGE_ORDER_APPROVAL_RULES`
- **Purpose:** Create, modify, activate, publish, and test sales-order approval rules that route submitted sales orders to the approved approvers before fulfillment.
- **Execution rule:** The user completes the approved change manually in the Fusion Setup and Maintenance user interface; no API, import, automated configuration, or browser automation.

Use the standard manual workflow in [SKILL.md](SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual steps

1. In the target nonproduction Fusion environment, ensure the user has Order Management administration access and the `FOM_MANAGE_ORDER_APPROVAL_RULES_PRIV` privilege. Before changing a rule, record the approved policy, scope, condition values, approver or approval group, expected order status, test orders, and rollback owner; confirm the selected individual, group, job-level hierarchy, or supervisor chain is current.
2. Enable approval for the intended source system: open **Navigator** > **My Enterprise** > **Setup and Maintenance**, select the **Order Management** offering, then search for **Manage Order Management Parameters**. Set **Start Approval Process for Sales Orders** to **Yes** for the applicable source system. Set **All** to **Yes** only when every configured source system requires approval, then save.
3. In **Setup and Maintenance**, select the **Order Management** offering before searching for **Manage Order Approval Rules**, then open the task. Review the active rules, their conditions, actions, and policy coverage. Capture the existing configuration before modifying a rule.
4. Create a rule by selecting **Create New Rule**, entering the approved rule name, and using **Enter Description** in the **IF** area to describe the approved condition. Select **New Condition**, choose the approved attribute, operator, and comparison value, then save the condition. Select attributes from **Order Header** when using the attribute tree; do not select attributes under **HierarchyPrincipal** or **Task**. Use **AND** to add further approved criteria.
5. Use the condition that matches the approved policy: order totals for high-value orders, an order-header attribute for customer exceptions, price adjustment or price validation for pricing exceptions, an order-line attribute for line-specific exceptions, or a trade-compliance attribute for trade-compliance exceptions. When using **Order Total Amount**, also add **Primary is equal to Yes**. For a manually entered attribute, first test that it is not blank and then test its approved value.
6. Define the **THEN** action: select **Then** > **Do**, use **Enter Description** to state the approved routing outcome, then select **New Action** > **Perform an Action** and enter the approved assignment values. Use **Assign to Individual** for a named recipient, **Assign to Group** for an approval group, **Assign to Supervisors** for a hierarchy chain, or **Assign to Job Level** to route to the approved job level. Set recipients who need visibility but not approval to **Information Only**. Save and close the rule.
7. Open the new or updated rule, select **Activate Rule**, save and close it, confirm that it is active, then select **Publish**. Record the published rule, timestamp, approver routing, and approved change record. A saved rule is not effective until it is published.
8. If a published rule routes orders incorrectly, stop further test submissions, restore the captured prior condition, action, or active state, save and publish the restoration, and use a new controlled test order to confirm the prior behavior.

## Manual validation guidance

1. Submit a new sales order that meets every rule condition and verify that its status becomes **Approval Pending**. In **View Approval Information**, verify the displayed rule and approver routing.
2. In the approver’s session, open **Pending Notifications** or the worklist, approve the request, refresh the order-entry session, and verify that the sales order status becomes **Processing**.
3. Submit a new order that does not meet the condition and verify that this rule does not start approval. Test the condition boundary values where applicable.
4. Reject a qualifying approval request and verify that the sales order returns to **Draft**, is unlocked, and displays the rejection details on **Approval Notes**.
5. Record the order number, source system, condition values, approval request, approver, decision, final status, and validation evidence in the approved change record.
