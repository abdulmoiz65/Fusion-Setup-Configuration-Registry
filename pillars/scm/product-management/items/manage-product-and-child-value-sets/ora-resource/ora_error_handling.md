# Manage Product and Child Value Sets Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input, parent lookup, dependency, or design validation fails | Stop before setup execution, return the failed condition, and request the corrected value-set definition or parent evidence |
| The documented metadata lookup cannot establish one qualifying parent | Stop; do not infer a parent or issue a setup change |
| Post-import value-set verification returns zero or many matches, or does not match the requested definition or values | Report functional verification as failed with the mismatched business field. Do not retry the import or modify the value set automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation refusal | The failing validation, the supplied value-set identity, and the one safe corrective action; exclude credentials and raw sensitive payloads |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A Subset parent is missing, ambiguous, or non-independent | Do not create the child subset or silently substitute a different parent |
| The request has not passed all validation nodes | Do not treat validation readiness as authorization to write setup data |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VSET.HANDLE_ERROR | step | 50 | error_handler | handled->VSET.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, or design failure |
| VSET.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| VSET.READY_FOR_EXECUTION | terminal | 70 | terminal | none | VSET.ENFORCE_DESIGN | stop | All documented validations passed; no setup write has been executed |
