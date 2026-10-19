---
task_code: "ORA_POZ_CONFIGURE_SUPPLIER_OUTBOUND_SYNCHRONIZATION_SERVICE"
task_name: "Configure Supplier Outbound Synchronization Service"
parent_skill_id: "scm.procurement.suppliers"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
# Generator default only; this manual task has no configured Data Loader execution route.
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Configure Supplier Outbound Synchronization Service

**Manual task — guidance only.** State this up front. The user makes approved
changes in Fusion; no automated export/import, API calls, or browser actions.
Catalog flags and generated loader metadata do not authorize automation.

- Task code: `ORA_POZ_CONFIGURE_SUPPLIER_OUTBOUND_SYNCHRONIZATION_SERVICE`
- Purpose: Configure the service that systematically synchronizes updates to supplier records from Oracle Fusion Applications to the customer's applications.

Use the standard manual navigation in
[shared.common.manual-tasks](../../../../shared/common/manual-tasks/SKILL.md).

Give navigation, task-specific steps, and validation directly. Reuse supplied
context; clarify only an ambiguous task or scope. Do not request configuration
values, credentials, or completion confirmation in chat. The implementer obtains
missing approved values from the administrator and enters them in Fusion.
Do not invent defaults or create separate guides to repeat these steps.

## Manual steps

1. Sign in to the target Fusion environment with a role that can access Setup and Maintenance and the named task. Open **Navigator** > **Setup and Maintenance**.
2. Select **Procurement** in **Setup**, select **Suppliers**, and set **Show** to **All Tasks**. Open **Configure Supplier Outbound Synchronization Service**. Alternatively, use **Search Tasks** or the **Tasks** panel search to find that exact task name and select **Go to Task**.
3. Review the existing configuration. In **URL**, enter the receiving-service endpoint supplied by the integration administrator; this field is required. In **User Name**, enter the receiving-service account; this field is also required. Preserve settings outside the intended change.
4. Confirm the displayed **Security Policy** is `oracle/wss_username_token_over_ssl_client_policy`. It is shown as policy text, not a selection field; do not ask for a replacement policy or invent a policy control. Resolve any mismatch with the integration administrator before proceeding.
5. In **Password**, enter the receiving-service account password if setting or updating credentials.
6. If the task is unavailable or endpoint/account details are unknown, obtain access or configuration details from the setup or integration administrator before making changes.
7. Save the approved changes.

## Manual validation

Reopen the task and confirm the approved URL, User Name, and displayed security policy. Do not reveal or read back the password. Where an authorized test is available, verify that a safe supplier update reaches the intended receiving application and record the outcome. Otherwise record that end-to-end synchronization validation is deferred. Record the target environment, change description, implementer, and validation result; do not include passwords or other secrets.
