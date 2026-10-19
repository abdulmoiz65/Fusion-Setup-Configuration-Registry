# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Selected index profile | Validate exactly one complete Item or Catalog profile. |
| 2 | Active Run Book Product Management task | Resolve exactly one active `CUSTOM_EGP_MANAGE_PM_INDEXES` task named `Manage Product Management Indexes`. |
| 3 | Product Management Indexes invocation contract | Resolve the authoritative delegated invocation contract from that active task before preparing a handoff. |
| 4 | Current index metadata | Compare the selected profile with the authoritative current index metadata. |
| 5 | Named child attributes | Resolve every profile triplet to the child name-and-scope contract before either handoff branch. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SALES_INDEX.NAMED_PROFILE | Named child attribute inputs | Yes | Every request | Lookup | Product Management available-attribute metadata | resolve_sales_index_attribute_names | Code-only triplets are not accepted by the child delta guard. | Require one exact metadata match per requested identity; preserve the full profile and explicit removals. | Ordered named attributes_to_add |
| SALES_INDEX.PM_INDEXES_DELEGATION | Manage Product Management Indexes delegation | Yes | Every request | Verify | Active Run Book dashboard; exact task code `CUSTOM_EGP_MANAGE_PM_INDEXES`; exact task name `Manage Product Management Indexes`; child single-index input set | resolve_product_management_index_delegation | The resolved Product Management task owns canonical index resolution, attribute delta calculation, Data Loader import, readback, and ESS rebuild approval. | Use the active Run Book task only when exactly one matching Product Management task is present; then delegate one selected index at a time with its requested additions, removals, rebuild preference, and target environment. | resolved_product_management_index_task, canonical_index_name, single_index_request, attributes_to_add, attributes_to_remove, index_rebuild_requested, target environment |
| SALES_INDEX.CURRENT_INDEX_METADATA | Current selected-index metadata | Yes | Every request | Lookup | Product Management Indexes read-only canonical-index and existing-index metadata flow | verify_index_attribute_profile | The selected profile must be compared before choosing an attribute delta or rebuild-only path. | Resolve the canonical index and compare exact AttributeCode#GroupCode#ObjectCode identities in the current authenticated Fusion environment. | Current attributes and comparison result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| BLOCKED | The active Run Book has zero or multiple exact Product Management task matches, or the delegated invocation or current-index metadata contract is unresolved, missing, or ambiguous. | No |
| READY | The selected profile, one active resolved Product Management task, delegation contract, and metadata comparison are complete. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.CHECK-DELEGATION-CONTRACT | decision | 20 | resolve_dependency | ready->SALES_INDEX.VERIFY-INDEX-PROFILE;blocked->RETURN_ISSUES | SALES_INDEX.VALIDATE-REQUEST | stop | Every validated request; resolve PM_INDEXES_DELEGATION here, then evaluate CURRENT_INDEX_METADATA and NAMED_PROFILE in VERIFY-INDEX-PROFILE |
