# Design Enforcement

Do not apply task-specific business-design gates to an unchanged Manage
Customer Center Task Template FSM package.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve package intent | Validate and submit the package as one immutable task artifact without interpreting rows as a separate design request |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An unchanged FSM package is imported | None | | None beyond objective task and package validation | Do not request owner, template dependency, privilege, or downstream-impact acknowledgement | Not applicable |
| User separately asks to change task-template business design | Outside this import gate | | Do not infer that separate request from package contents | Route the explicit request to its owning setup workflow | Not applicable |
