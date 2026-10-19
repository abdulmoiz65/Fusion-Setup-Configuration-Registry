# Lot Grades Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood inventory-lot-serial setup lot-grades page | Grade Code and Description are required by the UI; GradeDisabledCode is rendered as the Active checkbox |
| Redwood CreateGradeDrawerTemplateSpPrimaryActionChain | The UI converts the selected active checkbox token to GradeDisabledCode N and an empty checkbox selection to Y before submission |
| User approval | Apply the observed Active checkbox normalization before Data Loader handoff |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Data Loader and Fusion own required fields, lengths, uniqueness, server-side domains, and final field enforcement |
| Local validation ownership | Normalize only the approved Active checkbox representation for GradeDisabledCode and reject unsupported or conflicting local representations |
| REST execution | Do not create direct REST write guidance; core.data-loader owns execution for Inventory Lot Grades |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Active checkbox representation | GradeDisabledCode as N or Y, selected checkbox token active, or empty checkbox selection | Stop when a supplied representation is neither a canonical code nor an observed UI checkbox representation | Supply N or Y, select active, or provide an empty checkbox selection | GradeDisabledCode is supplied for normalization |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| GradeDisabledCode is the selected UI checkbox token active | Continue after filling GradeDisabledCode with N | Pass the canonical code to Data Loader |  |
| GradeDisabledCode is an empty UI checkbox selection | Continue after filling GradeDisabledCode with Y | Pass the canonical code to Data Loader |  |
| GradeDisabledCode is already the canonical code N or Y | Continue without changing the supplied canonical code | Pass the canonical code to Data Loader |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Active checkbox normalization | Convert selected checkbox token active to N; convert an empty checkbox selection to Y; preserve canonical N or Y | Before Data Loader handoff |  |
| Unsupported status representation | Reject a value other than active, an empty checkbox selection, N, or Y | GradeDisabledCode is supplied |  |
| Conflicting status representation | Reject values that express more than one status for the same field | More than one GradeDisabledCode representation is supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOTGRADE.VALIDATE_INPUT | step | 10 | validate_input | valid->LOTGRADE.CHECK_DEPENDENCIES;invalid->LOTGRADE.HANDLE_ERROR | none | stop | Before Data Loader task validation or import preparation |
