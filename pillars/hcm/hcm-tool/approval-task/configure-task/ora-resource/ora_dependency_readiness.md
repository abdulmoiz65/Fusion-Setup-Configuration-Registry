# Dependency Readiness

## Source Material

- Developer-supplied exported Word document: HCM Config Task UI screenshots and REST calls for BPM based flows.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | HCM task configuration UI | When the Configure Task icon is not visible, enable HRC_TXN_TASK_CONFIGURATION_ENABLED at Site level before configuration. |
| 2 | Approval process | Resolve one exact processId before reading or changing task configuration. |
| 3 | Current task configuration | Read the configuration for that processId before preparing changes. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| HCM_TASK_CONFIGURATION_UI | HRC_TXN_TASK_CONFIGURATION_ENABLED profile option enabled and updatable at Site, with Site profile value true | Conditional | The Configure Task icon is not visible | Verify | Developer-supplied Word document and Setup and Maintenance UI | TBD | The document identifies this as the prerequisite that exposes the Configure Task icon. | In Manage Profile Options, create or enable the option for Global Human Resources / Transactions, then set its Site value to true in Manage Administrator Profile Values. | Profile option visibility |
| APPROVAL_PROCESS | One exact approval process | Yes | Every configuration request | Lookup | Approval-options finder result | find_approval_process_by_name | The documented read and write actions require processId. | Provide the exact approval_process name. | processId |
| CURRENT_TASK_CONFIGURATION | Current configuration result | Yes | Before previewing a change | Lookup | readTaskConfiguration result | read_task_configuration | Json must contain the complete reviewed task configuration. | Read configuration for the exact resolved processId before preparing Json. | Current task configuration result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verify | Configure Task icon is not visible. | No; the source supplies a UI remediation but no authorized lookup contract. |
| Lookup | Approval process and current configuration are resolved through documented read-only calls. | Yes |
