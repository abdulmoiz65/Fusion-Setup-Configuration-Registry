# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| No FSM import package is supplied | Stop and request the package to validate before import |
| No retained FSM export baseline is supplied in setup_data_artifacts | Permit the import without baseline comparison |
| ORA_MSC_INSTANCE_ORG.csv changed from the baseline and ORA_MSC_APPS_INSTANCE.csv is absent | Block the import and clearly state that ORA_MSC_APPS_INSTANCE.csv must be included because ORA_MSC_INSTANCE_ORG.csv changed |
| ORA_MSC_FLEX_FIELD_MAPPING.csv changed from the baseline and ORA_MSC_APPS_INSTANCE.csv is absent | Block the import and clearly state that ORA_MSC_APPS_INSTANCE.csv must be included because ORA_MSC_FLEX_FIELD_MAPPING.csv changed |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | No import package is available | Provide the FSM import package |
| package_dependency_blocker | A required ORA_MSC_APPS_INSTANCE.csv file is absent after a tracked CSV changed | Add ORA_MSC_APPS_INSTANCE.csv and revalidate the package |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Package dependency blocker | The changed CSV file and the requirement to include ORA_MSC_APPS_INSTANCE.csv |
| Baseline absent | That no retained FSM export baseline was supplied and that import proceeds without comparison |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A tracked CSV changed and ORA_MSC_APPS_INSTANCE.csv is absent | Do not import the package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSCPS.COMPLETE | terminal | 4 | terminal | none | MSCPS.PACKAGE_GATE | continue | The package satisfies the documented source-system composition rules |
| MSCPS.COMPLETE_WITHOUT_BASELINE | terminal | 5 | terminal | none | MSCPS.DEPENDENCIES | continue | No retained FSM export baseline is supplied and import is permitted without comparison |
| MSCPS.BLOCKED | terminal | 6 | terminal | none | none | continue | A required input or package-composition dependency blocks import |
| MSCPS.FAILED | terminal | 7 | terminal | none | none | continue | Validation, dependency evaluation, or design enforcement fails unexpectedly |
