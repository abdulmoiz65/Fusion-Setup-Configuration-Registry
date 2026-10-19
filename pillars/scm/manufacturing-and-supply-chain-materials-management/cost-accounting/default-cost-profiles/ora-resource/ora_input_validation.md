# Default Cost Profiles Input Validation

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Default Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-default-cost-profile.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Default-profile association | One assignment scope: Cost Organization, Cost Book, or Category Name | Block before preview | Supply the intended assignment scope | Always | |
| Type-specific default cost profile | At least one of Asset Cost Profile Code, Expense Cost Profile Code, or Consigned Cost Profile Code | Block before reference lookup | Supply at least one type-specific default cost profile | Always | |
| Cost organization and cost-book resolution | Specified Cost Organization Name and Specified Cost Book Code | Block before cost-book resolution | Supply one exact cost organization name and one exact cost book code | Cost-book assignment is selected | resolve_cost_organization_by_exact_name |
| Item-category resolution | Supplied Item Category Code or Supplied Item Category Name | Block before category resolution | Supply exactly one item-category code or name | Category assignment is selected | |
| New-item profile behavior | Specified New Profile Creation | Block before preview | Supply an exact value accepted by the standard lookup; the current developer-selected value is Auto | Always | resolve_profile_creation_code_by_exact_meaning |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| New Item Profile Creation | Require exactly one standard-lookup result whose Meaning equals the supplied value | A value is supplied | resolve_profile_creation_code_by_exact_meaning |
| Type-specific default cost profiles | Require one or more of Asset Cost Profile Code, Expense Cost Profile Code, or Consigned Cost Profile Code | Always | |
| Cost Organization assignment | Associate the selected cost profile to apply it to all items in the specified cost organization | Cost Organization is the selected assignment scope | |
| Category Name assignment | Associate the selected cost profile to apply it to all items in the specified category | Category Name is the selected assignment scope | |
| Item category selector | Accept either Item Category Code or Item Category Name, but not both | Category assignment is selected | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.VALIDATE_INPUT | step | 10 | validate_input | valid->DCP.RESOLVE_COST_ORGANIZATION;invalid->DCP.HANDLE_ERROR | none | stop | Before preview |
