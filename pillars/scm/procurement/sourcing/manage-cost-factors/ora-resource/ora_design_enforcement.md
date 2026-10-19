# Manage Cost Factors Design Enforcement

Sources: User-provided Manage Cost Factors business-rule content from Confluence page 14988929751; user-authorized inspection of the Redwood Manage Cost Factors page on 2026-09-01.

## Scope

This resource applies only to the interactive Redwood Cost Factors table. It
does not apply to a `core.data-loader` workbook or Data Loader Task Hook
validation cycle.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce Redwood Cost Factors table interaction rules | Apply the observed Create, row-specific Edit, inline Apply/Cancel, saved-code, and result-table behavior when the interactive table is used. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A user creates a cost factor | Error | | The Create action does not open an inline row with Apply and Cancel actions. | Use Create to begin an inline row; validate and apply or cancel that row before starting another create action. | Yes |
| A user edits a saved cost factor | Error | | The saved row lacks its row-specific Edit action. | Use the row-specific Edit action rather than a selection-based Actions menu. | Yes |
| A cost factor has already been saved | Error | | The Code field is editable. | Render Code as display-only after save. | Yes |
| A Duplicate action is proposed for the Redwood page | Error | | A Duplicate action is exposed or required without a documented Redwood UI behavior. | Do not expose or require Duplicate until a current source documents its behavior. | Yes |
| The Cost Factors search-results table is displayed | Error | | The table is constrained to the legacy 25-row maximum. | Allow the table to display more than 25 rows; do not enforce the legacy row cap. | Yes |
