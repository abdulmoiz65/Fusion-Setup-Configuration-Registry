# Input Validation

Source basis: Oracle Fusion Cloud Sales, Sales Lead Lookups, and Oracle
Applications Common Standard Lookups REST endpoints.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Inventory, Review, AddCode, UpdateCode, DisableCode, RemoveCode, or BulkSet | Block validation | Provide or normalize one supported operation | Always | |
| Target environment | EnvironmentUrl, canonical EnvironmentIdentity, and ProjectId | Block before external calls | Resolve selected Fusion environment/project | Always | |
| Export attempt evidence | Status and, when successful, ProcessId, archive hash, environment, release, timestamp, member list, and counts | Disclose and continue live reads | Run automatic task export | Inventory or Review | find_standard_lookup_candidates |
| Exact lookup identity | LookupType; LookupCode for code-specific operations | Block lookup | Provide exact case-sensitive values | Review or mutation | find_standard_lookup_candidates |
| Proposed code values | Meaning plus optional Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and Tag | Block preview | Supply only intended supported fields | AddCode, UpdateCode, DisableCode, or BulkSet | |
| Expected current state | Exact current item fingerprint or explicit absent state | Block preview | Re-read exact code | Mutation | find_standard_lookup_candidates |
| Duplicate evidence | Exact code result and timestamp | Block AddCode preview | Require zero exact matches | AddCode | find_standard_lookup_candidates |
| Conditional impact evidence | Availability, translation, historical-reference, reporting, integration, and UI effect appropriate to the requested change | Block impact-sensitive preview | Review current use and disclose effect | DisableCode, RemoveCode, Meaning change, or availability change | |
| Immutable preview | Environment, type/code, operation, method, endpoint, expected state, delta/body/delete effect, verification plan, and PreviewSha256 | Block approval | Build after complete live preflight | Before mutation approval | |
| Execution approval | Standalone approval bound to complete PreviewSha256 and fields | Block write | Present immutable preview and wait | Immediately before POST, PATCH, or DELETE | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Unsupported operation | Reject | Always | |
| LookupType or LookupCode has separators, control characters, surrounding whitespace, or case drift | Reject before URL construction | Exact lookup | |
| LookupType is a documented Set ID type | Return unsupported and route to Manage Set Enabled Lookups | Always | find_standard_lookup_candidates |
| LookupType is neither documented nor exported | Require exact live standard resolution and explicit environment-only review | Review or mutation | find_standard_lookup_candidates |
| Inventory union omits a candidate or candidate status | Mark incomplete | Inventory | find_standard_lookup_candidates |
| Type is omitted from FSM export but resolves live | Continue Inventory/Review or mutation; export omission is not a blocker | Always | find_standard_lookup_candidates |
| AddCode finds exact code | Block duplicate | AddCode | find_standard_lookup_candidates |
| UpdateCode, DisableCode, or RemoveCode does not resolve exactly one code | Block | Existing-code mutation | find_standard_lookup_candidates |
| EnabledFlag is not Y or N | Reject | AddCode, UpdateCode, DisableCode, or BulkSet | |
| DisplaySequence is supplied and is not a positive integer | Reject | AddCode, UpdateCode, or BulkSet | |
| StartDateActive is later than EndDateActive | Reject | AddCode, UpdateCode, DisableCode, or BulkSet | |
| AddCode lacks LookupCode or Meaning | Block preview | AddCode or BulkSet create row | |
| Update/Disable has no actual mutable-field delta | Return no change; do not PATCH | UpdateCode or DisableCode | |
| Proposed body contains immutable key on PATCH, audit/module/ownership/BOSS/translation field, or unknown field | Reject and minimize body | Mutation | |
| RemoveCode lacks positive customer-created evidence | Refuse DELETE and offer DisableCode | RemoveCode | find_standard_lookup_candidates |
| Meaning change lacks translation inventory/impact disclosure | Block preview | UpdateCode or BulkSet | find_standard_lookup_candidates |
| Bulk rows duplicate LookupType/LookupCode | Reject and identify duplicates | BulkSet | |
| Approval does not match complete preview digest, method, endpoint, state, and body/effect | Block write and require new approval | Execution | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLL.VALIDATE | step | 1 | validate_input | valid->SLL.DEPENDENCIES;invalid->SLL.RETURN_ISSUES | none | stop | Validate operation, canonical environment, conditional export evidence, exact identities, supported mutable fields, current/duplicate state, conditional impact/delete safety, immutable preview, and approval inputs |
