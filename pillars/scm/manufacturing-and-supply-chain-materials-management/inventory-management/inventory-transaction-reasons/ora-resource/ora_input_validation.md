# Inventory Transaction Reasons Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood inventory-transactions-setup-ui CreateTransactionReasonsVO metadata rules | ReasonName, Description, EnableDate, DisableDate, ReasonType, and ReasonContextCode are visible but not locally required |
| Redwood inventoryTransactionReasonsV2 layout | Reason Context is enabled only when ReasonType equals 1 |
| Implementation owner confirmation | Registered Data Loader business object is inventoryTransactionReasonsV2 |
| Implementation owner approved rule | EnableDate and DisableDate use YYYY-MM-DD, are not before the current date, and DisableDate is not before EnableDate |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Leave required fields, lengths, uniqueness, dates, and business-object domains to Data Loader and Fusion |
| Local validation ownership | Validate only the sourced UI-only condition for a supplied Reason Context and the selected display-value resolvers |
| REST execution | Do not create direct REST write guidance; Data Loader owns execution for inventoryTransactionReasonsV2 |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Reason Context UI condition | ReasonType equals 1, or ReasonContext and ReasonContextCode are blank | Stop before Data Loader handoff when a Reason Context is supplied for another ReasonType | Set ReasonType to 1 or remove the Reason Context value | ReasonContext or ReasonContextCode is supplied |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Reason Type display value is supplied instead of ReasonType | Continue only after exactly one Type LOV entry resolves | Fill ReasonType and ReasonTypeMeaning from the Type resolver | resolve_inventory_reason_type |
| Reason Context display value is supplied instead of ReasonContextCode | Continue only after ReasonType is resolved and exactly one Context LOV entry resolves | Fill ReasonContextCode and ReasonContext from the Context resolver | resolve_inventory_reason_context |
| ReasonType and ReasonTypeMeaning are both supplied | Continue only when the code and display value identify the same Type LOV entry | Return a conflicting-input issue when the supplied pair differs | resolve_inventory_reason_type |
| ReasonContextCode and ReasonContext are both supplied | Continue only when the code and display value identify the same Context LOV entry | Return a conflicting-input issue when the supplied pair differs | resolve_inventory_reason_context |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Reason Context enablement | Reject a supplied ReasonContext or ReasonContextCode unless ReasonType equals 1 | Before Context lookup or Data Loader handoff |  |
| Type pair consistency | Reject conflicting ReasonType and ReasonTypeMeaning values | Both values are supplied | resolve_inventory_reason_type |
| Context pair consistency | Reject conflicting ReasonContextCode and ReasonContext values | Both values are supplied | resolve_inventory_reason_context |
| Enable Date format | Reject an EnableDate that is not in YYYY-MM-DD format | EnableDate is supplied |  |
| Disable Date format | Reject a DisableDate that is not in YYYY-MM-DD format | DisableDate is supplied |  |
| Enable Date not in the past | Reject an EnableDate before the current date | EnableDate is supplied |  |
| Disable Date not in the past | Reject a DisableDate before the current date | DisableDate is supplied |  |
| Date order | Reject a DisableDate before EnableDate | Both EnableDate and DisableDate are supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITR.VALIDATE_INPUT | step | 10 | validate_input | valid->ITR.RESOLVE_REASON_TYPE;invalid->ITR.HANDLE_ERROR | none | stop | Before Data Loader task validation or import preparation |
