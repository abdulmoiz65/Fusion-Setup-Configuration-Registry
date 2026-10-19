# Manage Sales Status Category Mappings Design Enforcement

These rules preserve documented Sales behavior and prevent unrelated runtime
product-line concepts from being treated as setup metadata.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Verify the current matrix | Resolve exactly one current row for the selected opportunity category from a fresh same-target task export |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Changing allowed revenue statuses for an opportunity category | Blocker |  | The fresh same-target baseline does not contain exactly one row for the selected opportunity category | Export the exact task again and resolve one existing row before package preparation | Yes |
| Changing allowed revenue statuses for an opportunity category | Blocker |  | The package changes identifiers, version fields, metadata, another category, or anything other than the four proposed revenue flags | Rebuild the package from the fresh baseline and retain only the intended flag changes | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.STATUS_MAPPING.DESIGN | decision | 2 | design_enforcement | pass->OPP.STATUS_MAPPING.PACKAGE;blocked->OPP.STATUS_MAPPING.RETURN_MISSING | OPP.STATUS_MAPPING.VALIDATE | stop | Before building and validating the fresh-export-derived immutable package for a status-category mapping change |
