# Manage Inventory Organizations Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required organization identity, ownership, item-master, or location data is missing | Stop and request only the missing approved value |
| Exact organization lookup finds no source or more than one source | Stop and ask for an unambiguous OrganizationId, OrganizationCode, or OrganizationName |
| A duplicate OrganizationCode or OrganizationName is found | Stop and require a distinct identity; do not convert the request into an update |
| Oracle returns a validation, authorization, transport, or process error | Preserve the redacted response and external identifier when available; stop before retry or a different execution route |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields, lengths, or conditional information are missing or invalid | Correct the request and revalidate |
| Lookup | The read-only source or duplicate lookup is unavailable, ambiguous, or has no required match | Supply an unambiguous value or restore lookup access |
| Approval blocker | A mutation, copy, or parameter update lacks the required immediate approval | Present the exact target, operation, and immutable payload or artifact for approval |
| Fusion API or transport | Oracle rejects the operation or the environment is unavailable | Preserve diagnostics and stop before retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any mutating operation | Exact target environment, operation, and immutable request payload or import artifact, followed by explicit approval |
| On a lookup failure | Resolver name, supplied identifiers, no-match or ambiguity result, and corrective action without secrets |
| On an Oracle failure | Environment, operation, external ID when available, redacted message, and next safe action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is ambiguous or unavailable | Do not select a result, fuzzy-match, or proceed with create, copy, update, or parameter maintenance |
| Required validation input is missing | Do not bypass the missing input using a browser, direct REST write, loader, or another integration |
| A mutating operation lacks immediate explicit approval | Do not submit it or retry it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INVORG.HANDLE_ERROR | terminal | 30 | terminal | none | none | stop | Any invalid input or lookup failure |
| INVORG.READY | terminal | 40 | terminal | none | INVORG.RESOLVE_EXISTING | stop | All documented input and optional lookup checks pass; the request is ready for its separately approved execution workflow |
