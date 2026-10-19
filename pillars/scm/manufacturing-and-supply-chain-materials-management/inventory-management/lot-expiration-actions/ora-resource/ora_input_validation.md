# Lot Expiration Actions Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood `lot-expiration-actions-page.js` | The Active checkbox output is converted to the backend `ActionDisabledCode` value. |
| Redwood `CreateLotExpirationActionsREST.js` and `EditInventoryExpiryActionREST.js` | The create and edit payloads apply the checkbox conversion before submission. |
| User approval | Apply this sourced Active-checkbox normalization before Data Loader handoff. |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Data Loader and Fusion own required fields, uniqueness, lengths, server-side domains, and final field enforcement. |
| Local validation ownership | Normalize only the approved Active-checkbox representation for `ActionDisabledCode`; reject unsupported or conflicting local representations. |
| Hidden UI fields | `AutomatedActionCode` and `ExpirationActionStatusId` are hidden by the active Redwood metadata rule. Do not accept them as user-facing local inputs or create lookup rules for them. |
| REST execution | Do not create direct REST write guidance; `core.data-loader` owns execution for `inventoryLotExpirationActions`. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Active checkbox representation | `ActionDisabledCode` as `N` or `Y`, selected checkbox token `active`, or an empty checkbox selection | Preserve a blank when the field is omitted; stop only when a supplied representation is unsupported | Supply `N` or `Y`, select `active`, or provide an empty checkbox selection | `ActionDisabledCode` is supplied for normalization |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| `ActionDisabledCode` is selected checkbox token `active` | Fill `ActionDisabledCode` with `N` | Pass the canonical code to Data Loader |  |
| `ActionDisabledCode` is an empty checkbox selection | Fill `ActionDisabledCode` with `Y` | Pass the canonical code to Data Loader |  |
| `ActionDisabledCode` is already canonical `N` or `Y` | Preserve the supplied code | Pass the canonical code to Data Loader |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Active checkbox normalization | Convert selected `active` to `N`; convert an empty checkbox selection to `Y`; preserve canonical `N` or `Y` | Before Data Loader handoff |  |
| Unsupported status representation | Reject a supplied value other than `active`, an empty checkbox selection, `N`, or `Y` | `ActionDisabledCode` is supplied |  |
| Conflicting status representation | Reject values that express more than one status for the same field | More than one `ActionDisabledCode` representation is supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOTEXPIRY.VALIDATE_INPUT | step | 10 | validate_input | valid->LOTEXPIRY.CHECK_DEPENDENCIES;invalid->LOTEXPIRY.HANDLE_ERROR | none | stop | Before Data Loader task validation or import preparation |
