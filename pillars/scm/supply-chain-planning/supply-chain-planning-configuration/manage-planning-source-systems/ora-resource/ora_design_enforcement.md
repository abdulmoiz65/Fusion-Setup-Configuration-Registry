# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Compare instance-organization data | Determine whether ORA_MSC_INSTANCE_ORG.csv changed from the supplied FSM export baseline |
| 2 | Compare flex-field mappings | Determine whether ORA_MSC_FLEX_FIELD_MAPPING.csv changed from the supplied FSM export baseline |
| 3 | Enforce application-instance inclusion | Block when either changed file is present without ORA_MSC_APPS_INSTANCE.csv |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| ORA_MSC_INSTANCE_ORG.csv changed compared with the supplied FSM export baseline | Blocker |  | ORA_MSC_APPS_INSTANCE.csv is not in the import package | Add ORA_MSC_APPS_INSTANCE.csv and revalidate the package | Yes |
| ORA_MSC_FLEX_FIELD_MAPPING.csv changed compared with the supplied FSM export baseline | Blocker |  | ORA_MSC_APPS_INSTANCE.csv is not in the import package | Add ORA_MSC_APPS_INSTANCE.csv and revalidate the package | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSCPS.PACKAGE_GATE | decision | 3 | design_enforcement | passed->MSCPS.COMPLETE;blocked->MSCPS.BLOCKED;failure->MSCPS.FAILED | MSCPS.DEPENDENCIES | stop | Before FSM import when either tracked CSV changed compared with the supplied FSM export baseline |
