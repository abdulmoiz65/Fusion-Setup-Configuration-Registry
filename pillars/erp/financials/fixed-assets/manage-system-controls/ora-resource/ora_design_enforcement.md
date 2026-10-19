# Manage System Controls: Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before System Controls ZIP creation | Error | Current Key Flexfields export and current System Controls export metadata | Any requested structure is disabled, selected instance is disabled or ambiguous, newly deployed structure lacks parent-verified target context, any structure field is not populated from the selected enabled `StructureInstanceCode`, or Oldest Date Placed in Service is not serialized as `YYYY/MM/DD`. | Use the three selected enabled `StructureInstanceCode` values and serialize Oldest Date Placed in Service as `YYYY/MM/DD`. | Yes, before ZIP creation |


