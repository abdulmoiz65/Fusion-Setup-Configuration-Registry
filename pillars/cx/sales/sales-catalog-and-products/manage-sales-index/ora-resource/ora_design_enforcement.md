# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve Product Management ownership | Send the selected profile or rebuild-only result to Manage Product Management Indexes. |
| 2 | Prevent direct execution | Do not call Data Loader or ESS directly from Manage Sales Index. |
| 3 | Preserve one-index scope | Do not combine Item and Catalog in one delegated invocation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A metadata comparison reports a selected-index delta | Error |  | The request attempts direct Data Loader or ESS execution, combines Item and Catalog in one Product Management invocation, or bypasses Manage Product Management Indexes. | Prepare one delegated Product Management request for each selected index. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.ENFORCE-DELEGATED-INDEXING | decision | 50 | design_enforcement | delegated_request_prepared->SALES_INDEX.DONE-DELTA-HANDOFF;blocked->RETURN_ISSUES | SALES_INDEX.VERIFY-INDEX-PROFILE | stop | The selected index has missing requested identities or explicit removals; preserve the full named profile and removals for child-owned delta calculation |
