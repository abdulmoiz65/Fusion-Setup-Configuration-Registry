# Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 1 | Service offering opt-in | Service must be implemented and Service Entitlements must be available in Setup and Maintenance |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 2 | Matrix class result columns | The milestone code and threshold code must correspond to result columns already configured in the matrix class |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 3 | Default BU association | In a newly provisioned multiple-BU environment, the default BU must be associated to the ready-to-use milestones before BU-specific milestones are configured |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 4 | Coverage setup | Standard, default, or subscription coverages must be planned so milestones can be applied to service requests |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | milestone_existing_state | Existing milestone configuration | Conditional | Operation is update, delete, or duplicate create check | Lookup | MilestoneConfigId or alternate key | find_milestone_by_alt_key | Prevents accidental duplicate create and confirms the correct record for update or delete | Provide MilestoneConfigId when the alternate key is not unique | MilestoneConfigId: MilestoneConfigId |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | matrix_result_columns | Matrix class result columns | Yes | MilestoneCode or ThresholdCode is supplied | Verify | Matrix class setup owned by Service Entitlements implementation |  | Milestone and threshold codes are selected from result columns defined in matrix classes | Confirm the configured milestone and threshold result column names before preview | MilestoneCode: MilestoneCode; ThresholdCode: ThresholdCode |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | default_business_unit | Default business unit association | Conditional | Business Units feature is enabled and this is the first milestone configuration in a newly provisioned environment | Verify | Setup and Maintenance selected default BU |  | The default BU association is a one-time prerequisite for multi-BU milestone setup | Select and apply the default business unit in Setup and Maintenance before BU-specific configuration | BUOrgId: BUOrgId; BusinessUnitName: BusinessUnitName |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | business_unit_scope | Business unit milestone scope | Conditional | Request configures milestones for a specific BU | Satisfied | BUOrgId or BusinessUnitName supplied by the implementation owner |  | Milestones must be defined for each BU that intends to track them | Provide the BU for each milestone configuration row | BUOrgId: BUOrgId; BusinessUnitName: BusinessUnitName |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | coverage_plan | Coverage setup plan | Conditional | Milestones are expected to apply automatically to service requests | Verify | Standard, customer default, global default, or subscription coverage setup |  | Milestones are applied to service requests through coverage definitions | Confirm which coverage level will apply the configured milestone | CoverageType: CoverageType |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Satisfied | Required value is supplied and does not need a live lookup | No |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Lookup | MilestoneConfigId is missing and the documented milestone alternate key is supplied | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Verify | A prerequisite is documented but no approved read-only resolver was provided in this authoring scope | No |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Blocked | Required milestone identity, matrix result column, or BU scope is missing | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.DEPENDENCIES | step | 4 | resolve_dependency | ok->SVCMILESTONE.DESIGN;blocked->SVCMILESTONE.FAILED;failure->SVCMILESTONE.FAILED | SVCMILESTONE.LOOKUP | stop | Before milestone configuration preview |
