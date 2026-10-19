# Dependency Readiness

## Readiness Checks

| Dependency | Ready When | Applies When | If Not Ready |
|---|---|---|---|
| Target environment | Canonical identity, REST host, selected project, and declared Apps Common route agree | Always | Stop before external calls and report the sanitized mismatch |
| Current task export attempt | Automatic export was attempted and its outcome recorded | Inventory or Review | Attempt export before offline evidence; continue exact live reads if export fails |
| Documented identity | Exact code or one exact documented display name resolves against the task-local baseline plus refreshed guidance | Documented Inventory, Review, Set, or Remove | Never fuzzy-match; an exact exported or explicitly reviewed environment-only code may continue |
| Apps Common read route | Exact profile definition, level, and child collections can be read through the declared shared client | Always | Return the actual auth, authorization, transport, environment, or response-shape failure |
| Profile definition | Exact live parent definition exists | Review, Set, Remove, or BulkSet | Return not_found and stop mutation |
| Scope capability | Selected Site, Product, or User level is enabled and updatable in live profileOptionLevels | Set, Remove, or BulkSet | Select an eligible scope or stop |
| Scope identity | Site uses SITE; Product uses one exact application short name; User uses one exact UserName and UserGuid | Set, Remove, or BulkSet | Correct the key; never guess or reuse another scope key |
| Current child state | Exact selected item is present once or its absence is established by the exact collection | Set, Remove, or BulkSet | Resolve ambiguity or privileges before preview |
| Stored-value dependency | Proposed value resolves to the exact active code, ID, rule, map, template, user, or role required by SqlValidation | Create, Update, Set, or BulkSet | Resolve the intended stored value before preview |
| Qualification template | Exact template resolves to one active/deployed Lead AssessTemplateId | Template profile mutation | Complete or deploy the template first |
| Assignment rule | Exact selected rule group is published for the required Lead candidate object | Assignment-rule mutation | Publish or correct the rule first |
| Copy Map | Exact selected map exists for the intended conversion route | Mapping-profile mutation | Create or correct the Copy Map first |
| Approval participant | Exact administrator or approver identifier is valid | Approval-profile mutation | Resolve the intended user or role first |
| Mutation privilege | FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV is available | Before Create, Update, or Delete | Stop and report the required privilege |
| Immutable approval | Approval is bound to the complete canonical environment, method, endpoint, identity, expected state, body/delete effect, and preview digest | Immediately before a write | Stop and obtain a new exact preview approval |

## Sequencing Rules

- Qualification-template creation and deployment remain owned by
  `MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`; this task consumes exact
  deployed identity evidence only.
- Cross-task sequencing stays outside this graph.
- Inventory and Review attempt the task export before live reconciliation.
  Mutations do not require export and never use FSM or Data Loader.
- Complete every read-only lookup and dependency before building the Apps
  Common CRUD preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPO.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->SPO.LOOKUP_PROFILE;missing->SPO.RETURN_ISSUES | SPO.VALIDATE | stop | Require canonical environment, Apps Common read readiness, exact identity, conditional dependencies, scope key and capability, current-state evidence, mutation privilege, and approval readiness when execution is requested |
