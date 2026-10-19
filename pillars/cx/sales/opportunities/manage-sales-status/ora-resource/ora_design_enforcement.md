# Manage Sales Status Design Enforcement

These rules preserve documented Sales behavior and prevent unrelated runtime
product-line concepts from being treated as setup metadata.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Validate status design | Preserve predefined categories and maintain at least one active Open status |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Creating or changing a sales status | Blocker |  | Status category is outside Lost, No Sale, Open, or Won | Associate the status with one predefined category; new categories cannot be added | Yes |
| Reviewing the complete status configuration | Blocker |  | No active status remains in the Open category | Retain or create at least one active Open-category status | Yes |
| Changing predefined status codes | Warning |  | A predefined code is deprecated or replaced | Retain predefined codes and add additional unique codes instead | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_STATUS.DESIGN | decision | 2 | design_enforcement | pass->OPP.SALES_STATUS.PACKAGE;blocked->OPP.SALES_STATUS.RETURN_MISSING | OPP.SALES_STATUS.VALIDATE | stop | Before building and validating the fresh-export-derived immutable package for a sales-status change |
