---
task_code: "ORA_FOM_MANAGE_ORDER_MANAGEMENT_EXTENSIONS"
task_name: "Manage Order Management Extensions"
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

# Manage Order Management Extensions

- **Task code:** `ORA_FOM_MANAGE_ORDER_MANAGEMENT_EXTENSIONS`
- **Purpose:** Extend Order Management through approved code extensions that run at predefined events in order creation and submission.
- **Manual-only execution rule:** The user completes the approved change manually in the **Manage Order Management Extensions** task in the Oracle Fusion Setup and Maintenance user interface, with no API, import, automated configuration, or browser automation.

Use the [standard shared manual workflow](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual steps

1. Work in a nonproduction environment first. Before writing or modifying code, consult the latest Oracle Order Management documentation set, beginning with the [26c Implementing Order Management guide](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/toc.htm) at **Extend** > **Extensions** > **Examples**. Confirm access to **Manage Order Management Extensions**, the approved business requirement, extension point, allowed data changes, validation or message behavior, test cases, performance expectation, rollback plan, and a durable unique extension name. Use an extension only when standard Order Management setup, flexfields, rules, and Page Composer cannot meet the approved requirement. Confirm that every referenced order attribute, extensible flexfield, public view object, message, connector, and web service is available and approved. Register a connector and web service before using an external service; use only synchronous interactions.
2. Open **Navigator** > **My Enterprise** > **Setup and Maintenance**. Select the **Order Management** offering before searching for tasks. In **Tasks**, search for **Manage Order Management Extensions** and open the task. Review the configured extensions on the three extension-point tabs. Before modifying an existing extension, record its sequence, active state, description, code, and observed runtime behavior.
3. Select the approved extension point. Use **On Save** for save-time or imported-source-order defaulting and validation; use **On Start of Submission Request** for supported writable header, line, flexfield, and attachment changes before submit validation and constraints; use **On End of Submission Request** only for final header and line flexfield updates before fulfillment. Do not update other attributes at On End. A failure at On Start returns the sales order to Draft with errors; a warning allows submission to continue.
4. Select **Create Extension** on the approved tab. Enter the approved unique name and a description that states the business purpose and scope, then enter the approved Groovy code in **Definition**. Use the `header` object to access the current sales order and its child rows, and use only supported entities, attributes, and methods. Read values with `getAttribute`, write only approved writable values with `setAttribute`, check optional attributes and flexfield values for null or blank values before evaluating them, and use an early condition so test logic runs only for the approved scenario. Use a controlled error to stop an invalid save or submit, or a warning only when the business flow may continue.
5. For an approved hold requirement, use **On Save** or **On Start of Submission Request**. Apply a hold only to a new sales order or an order in Draft status; do not apply it to a submitted order or change order. Before applying a header or line hold, verify that it is eligible and not already present. Do not apply a line hold to a child line of a model or kit. Use the approved hold code and comment, and handle a failed hold result as an error. For a hold on a shipment set, review every line in the set so the approved hold behavior is applied consistently.
6. Select **Validate** and correct every design-time error before saving. Validation checks code format and references; it does not replace runtime testing. Save the extension and set the approved **Sequence**. Active extensions at the same point run in ascending sequence order; use gaps such as 10, 20, and 30, review any extension that updates the same attribute, and account for the fact that an error or warning prevents later extensions at that point from running.
7. For an update, retain all unapproved code and configuration unchanged. Activate the extension only after peer review and nonproduction evidence are complete, then verify the approved sequence and active state on the selected extension-point tab. Do not delete an extension merely to replace it: a deleted extension name cannot be reused.
8. If the approved change causes errors, unexpected defaults, slow submissions, or incorrect downstream behavior, stop further controlled test submissions. Deactivate the affected extension or restore the recorded approved code and sequence, save the rollback configuration, and use a new controlled order to verify the prior behavior.

## Manual validation guidance

1. In the extension editor, select **Validate** and confirm that all design-time issues are resolved.
2. Create a positive test sales order that invokes the selected extension point, then save or submit it as applicable. Verify the expected defaulted value, validation result, message, data update, or synchronous web-service outcome. For a hold, confirm the approved hold code and comment appear at the approved header or eligible line scope.
3. Create a negative test that violates the intended rule and confirm that an error stops the applicable save or submit action and the sales-order status behaves as designed. Test null, blank, boundary, multiple-line, revision where applicable, and out-of-scope control scenarios. For a hold, also test an already submitted order, a change order, a line that is already on hold, and a child line of a model or kit where applicable; confirm that no unsupported hold is applied.
4. If the extension calls a web service, verify the request payload, response parsing, timeout behavior, and failure handling. Before production release, remove test-only conditional logic and replace ad hoc debugging behavior with appropriate logging.
5. Verify the active state and sequence after release. Use the **Runtime Threshold** tab to identify extensions that exceed the configured threshold; optimize, retest, and reassess slow code before increasing business volume. Record the extension name, extension point, sequence, test orders, results, rollback evidence, and final status in the approved change record.
