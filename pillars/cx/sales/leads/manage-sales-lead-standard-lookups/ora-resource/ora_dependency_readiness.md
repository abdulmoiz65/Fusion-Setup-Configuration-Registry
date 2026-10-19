# Dependency Readiness

## Dependency Rules

| Dependency | Required Evidence | Applies When | If Missing | Status |
|---|---|---|---|---|
| Target environment | Canonical environment, REST host, project, and Apps Common route agree | Always | Stop before external calls | Required |
| Automatic task export | Attempt result with environment and timestamp | Inventory or Review | Run shared setup export, then continue live reads even if it fails | Required for reconciliation |
| Documented candidate baseline | Current Oracle Sales Lead Lookups page or task-local baseline with refresh-unavailable disclosure | Inventory | Stop candidate-union completion when neither exists | Required |
| Apps Common read access | Exact standard parent, code collection, code item, and requested translation reads | Always | Stop on systemic auth, authorization, transport, pagination, or shape failure | Required |
| Existing standard parent | Exactly one live standard lookup type at standardLookups semantics | AddCode, UpdateCode, DisableCode, RemoveCode, or BulkSet | Stop; never create the type in this task | Required |
| Exact code state | AddCode proves absence; existing-code operations prove one exact current item and expected-state fingerprint | Mutation | Stop before preview | Required |
| Mutation privilege | Oracle Applications Common privilege to manage standard lookup codes | Before POST, PATCH, or DELETE | Stop and report required access | Required |
| Availability impact | Current references and availability effect are disclosed | DisableCode, RemoveCode, Meaning change, or other availability change | Stop until impact is reviewed | Conditional |
| Customer-created deletion evidence | Positive exact evidence that the selected code is customer-created and not delivered/seeded | RemoveCode | Refuse DELETE and offer DisableCode | Required for delete |
| Immutable approval | Approval matches canonical environment, type/code, method, endpoint, expected state, body/delete effect, and preview digest | Immediately before mutation | Stop and obtain exact approval | Required |

## Readiness Decisions

| Situation | Result | Next Action | Resolver |
|---|---|---|---|
| Export omits a documented live type | Ready for Inventory/Review and Apps Common code CRUD | Continue exact live state checks; do not synthesize FSM rows | find_standard_lookup_candidates |
| Export fails but live reads work | Inventory/Review may continue with disclosure | Complete the live candidate union | find_standard_lookup_candidates |
| Set ID type is requested | Not ready for this task | Route to Manage Set Enabled Lookups | find_standard_lookup_candidates |
| AddCode exact item is absent | Ready for POST preview when parent, fields, privilege, and approval gates pass | Build minimal immutable preview | find_standard_lookup_candidates |
| UpdateCode or DisableCode exact item exists once | Ready for PATCH preview when expected state and impact gates pass | Build changed-fields-only preview | find_standard_lookup_candidates |
| RemoveCode lacks positive customer-created evidence | Not ready for DELETE | Offer DisableCode | find_standard_lookup_candidates |
| Any candidate read has systemic failure | Not ready | Return classified issue; never silently omit it | find_standard_lookup_candidates |

## Sequencing Rules

- Use export only for Inventory/Review candidate reconciliation.
- Complete exact live parent/code/dependency reads before a mutation preview.
- Do not require business-owner or historical-use fields for routine AddCode or
  non-impactful UpdateCode.
- Never route lookup-code mutation through FSM, Data Loader, setup import, or a
  browser.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLL.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->SLL.LOOKUP;satisfied_with_export_warning->SLL.LOOKUP;missing->SLL.RETURN_ISSUES | SLL.VALIDATE | stop | Require canonical environment, conditional export-attempt evidence, documented scope, Apps Common access, exact parent/code state, mutation privilege, conditional impact/custom-delete evidence, and approval readiness |
