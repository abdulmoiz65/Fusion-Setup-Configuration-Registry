# Design Enforcement

## Policy

There will be no more than one item master organization in an enterprise.

## Notes

More than one item master organization is permitted only for multi-enterprise customers with no true overlap in business flows (for example, General Electric). The lookup evaluates item master organizations that already exist; it does not query the item organization currently being created because that organization does not yet exist. The requested item-master designation is evaluated from the creation input.

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An item organization is being created | Blocking | find_existing_item_master_organizations | One or more existing item master organizations are found and the requested creation would make the new organization an item master organization | Do not create another item master organization. Use the existing item master organization, unless an approved multi-enterprise exception applies. | Yes |
| An item organization is being created | Blocking | find_existing_item_master_organizations | More than one existing item master organization is found, regardless of whether the new organization is intended to be an item master organization | Rationalize the existing item master organizations and retain one per enterprise, unless an approved multi-enterprise exception applies. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_existing_item_master_organizations | Before evaluating either item-master design rule during item organization creation | Existing item master organization IDs, codes, names, and count | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MIO.ENFORCE | decision | 6 | design_enforcement | compliant->MIO.DONE;blocked->MIO.HANDLE_ISSUE | MIO.FIND_EXISTING_ITEM_MASTERS | stop | Creation after existing item master organizations have been identified |
| MIO.DESIGN_GATE | step | 3 | design_enforcement | lookup_required->MIO.FIND_EXISTING_ITEM_MASTERS | MIO.VALIDATE | stop | Creation passed local input validation |
