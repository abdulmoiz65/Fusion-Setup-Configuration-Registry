# Configure Item Transaction Defaults Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Oracle Fusion Cloud SCM REST API, Create One Item Transaction Default, 26c, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/op-itemtransactiondefaults-post.html | Confirms `DefaultType` is the code and `DefaultTypeMeaning` is the meaning of that code |
| Oracle Fusion Cloud Applications REST API, Get All Standard Lookups, 25d, https://docs.oracle.com/en/cloud/saas/applications-common/25d/farca/op-servername-fscmrestapi-resources-11.13.18.05-standardlookupslov-get.html | Confirms the standard-lookup response exposes `LookupCode`, `LookupType`, and `Meaning` |
| Redwood UI source, `inventory-transactions-setup-ui` commit `ffeef64afea9fa606bba1b3fb1a1eed3f83e6abf`, `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/layout.json` and `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/create-page.js` | Confirms the UI sends the selected standard-lookup Meaning as `DefaultTypeMeaning` before its staged REST workflow |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Resolve a supplied DefaultType code or DefaultTypeMeaning display value to one `INV_ITEM_TXN_DEFAULTS_TYPE` standard-lookup row; send its canonical Meaning in DefaultTypeMeaning |
| Backend-owned validation | Data Loader and Fusion own required fields, keys, uniqueness, lengths, server-side domains, and all unsupported input checks |
| REST execution | Do not create direct REST write guidance; core.data-loader owns execution for Item Transaction Defaults |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Default Type identity | DefaultType, or DefaultTypeMeaning | Let Data Loader report its required-field validation | Supply a LookupCode in DefaultType or a Meaning in DefaultTypeMeaning | Before Data Loader preparation | resolve_default_type_meaning |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| DefaultTypeMeaning is supplied without DefaultType | Continue only after one standard lookup row resolves by exact Meaning | Replace with the returned canonical Meaning; record LookupCode as resolver output only | resolve_default_type_meaning |
| DefaultType is supplied without DefaultTypeMeaning | Continue only after one standard lookup row resolves by exact LookupCode | Preserve DefaultType and fill DefaultTypeMeaning with the returned Meaning | resolve_default_type_meaning |
| Both DefaultTypeMeaning and DefaultType are supplied | Continue only when both inputs resolve to the same standard lookup row | Set DefaultTypeMeaning to its returned Meaning; stop on a conflict | resolve_default_type_meaning |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Default Type lookup normalization | Treat DefaultType as a LookupCode and DefaultTypeMeaning as a friendly display value; trim outer whitespace and resolve either through the documented standard lookup only | Either value is supplied | resolve_default_type_meaning |
| Conflicting Default Type inputs | Reject when supplied DefaultType and DefaultTypeMeaning resolve to different LookupCode/Meaning rows | Both DefaultType and DefaultTypeMeaning are supplied | resolve_default_type_meaning |
| Blank values | Preserve blanks; Data Loader and Fusion own any defaulting and validation | A field is omitted |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITD.VALIDATE_INPUT | step | 10 | validate_input | valid->ITD.RESOLVE_DEFAULT_TYPE_MEANING;invalid->ITD.HANDLE_ERROR | none | stop | Before Data Loader preparation |
