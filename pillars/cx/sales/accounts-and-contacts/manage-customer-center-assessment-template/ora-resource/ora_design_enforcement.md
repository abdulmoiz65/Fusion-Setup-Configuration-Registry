# Design Enforcement

Do not apply task-specific business-design gates to an unchanged Manage
Customer Center Assessment Template FSM package. Oracle documents assessment
design rules for interactive authoring; those rules are not extra pre-import
confirmations for an unchanged task package.

Official source:

- [How to create assessment templates](https://docs.oracle.com/en/cloud/saas/sales/oasal/how-to-create-assessment-templates.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve package intent | Validate and submit package as one immutable task artifact without interpreting rows as separate design request |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An unchanged FSM package is imported | None | | None beyond objective task and package validation | Do not request question, rating, scoring, weight, dependency, privilege, or downstream-impact acknowledgement | Not applicable |
| User separately asks to create or modify assessment-template design | Outside this import gate | | Do not infer separate request from package contents | Route explicit request to owning setup workflow and apply documented design rules there | Not applicable |
