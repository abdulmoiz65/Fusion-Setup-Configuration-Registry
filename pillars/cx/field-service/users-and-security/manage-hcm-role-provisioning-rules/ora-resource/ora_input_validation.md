# Input Validation

## Delegation Requirements

The selected task must be Manage HCM Role Provisioning Rules with task code
PER_MANAGE_HCM_ROLE_PROVISIONING_RULES. The requested operation, source and
target environments, scope, and archive or input-file provenance must be passed
unchanged to common.security-console.manage-hcm-role-provisioning-rules. This
pillar task does not validate an archive, acquire authentication, or invoke a
Fusion client.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HRPRFS.VALIDATE_DELEGATION | step | 1 | validate_input | valid->HRPRFS.CHECK_SHARED_WORKFLOW;invalid->HRPRFS.BLOCKED | none | stop | Before routing an HCM Role Provisioning Rules request to the shared workflow. |
