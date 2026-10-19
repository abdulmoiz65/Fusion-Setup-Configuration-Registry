# Manage Organization Hierarchies and Classifications Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Authorized target access | Confirm the operator can review, maintain, export, import, and verify the selected route |
| 2 | Approved enterprise hierarchy design | Confirm the hierarchy type, selected classifications, impact, deployment window, and rollback expectation |
| 3 | Current target baseline | Reconcile hierarchy type, selected classifications, and applicable default hierarchy |
| 4 | Static valid values | Resolve hierarchy-type and classification inputs to valid values |
| 5 | Conditional default hierarchy | Resolve tree, active tree version, and starting organization for organization or department hierarchy |
| 6 | Business-unit impact | Identify whether a hierarchy change affects existing business-unit implementation rows and requires follow-up |
| 7 | Exact FSM package contract | Obtain and validate the target-pod template, metadata, headers, translations, and process behavior before import |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| authorized_target_access | Authorized target-task access | Yes | Every request | Verify | Customer authorization | | Target review and verification are required | Confirm environment and operator privileges | Target environment, operator, allowed route |
| approved_hierarchy_design | Owner-approved hierarchy outcome | Yes | Every request | Verify | Accountable owner | | The task controls enterprise-wide project-organization behavior | Approve hierarchy type, classifications, impact, window, and rollback | Approved design and owner |
| current_target_baseline | Reconciled current hierarchy state | Yes | Update, removal, replacement, or import | Verify | Authorized target task and fresh current-data export | resolve_current_org_hierarchy_setup | Prevents stale or cross-environment changes | Capture the exact current state | Current hierarchy, classifications, default hierarchy |
| target_allowed_values | Static hierarchy type values | Yes | Every change | Verify | Organization Hierarchy Types static table | resolve_allowed_hierarchy_type | Prevents invalid hierarchy selection | Provide the desired hierarchy outcome | Hierarchy type |
| target_classification_values | Static organization classification values | Yes | Every change | Verify | Organization Classifications static table | resolve_available_org_classifications | Prevents invalid or empty classification selection | Provide at least one desired classification | Classifications, additions, removals, preserved values |
| default_hierarchy_combination | Valid default hierarchy | Conditional | Organization or department hierarchy | Verify | Authorized target task choices | resolve_default_org_hierarchy | Non-None hierarchy requires a compatible tree, version, and start organization | Select one complete target combination | Tree, active version, starting organization |
| business_unit_impact | Existing business-unit impact | Conditional | Hierarchy type changes | Verify | Current target task warning and current state | resolve_current_org_hierarchy_setup | Hierarchy change can affect all configured project and expenditure business-unit hierarchy settings | Review impact and plan the separate maintenance-process handoff | Impact confirmation and follow-up requirement |
| target_template_contract | Exact target-pod FSM package contract | Yes | FSM import | Verify | Customer-provided or freshly exported target evidence | verify_org_hierarchy_fsm_package | Catalog support does not define exact mappings or permitted mutations | Acquire the exact template and current export before preview | Metadata, members, headers, translations, operation, checksum, process behavior |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every route-specific dependency is satisfied | No; continue to defaulting and design enforcement |
| Missing | Access, approval, current state, target values, default hierarchy, impact, or package evidence is absent | No; return issues |
| Unsupported | Requested import would replace a hierarchy type, remove classifications, use direct REST, or invoke an internal service | No; refuse only the unsupported operation and continue independent supported work |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.CHECK_DEPENDENCIES | step | 6 | resolve_dependency | ready->OHCL.APPLY_DEFAULTS;missing->OHCL.HANDLE_ERROR;unsupported->OHCL.REFUSED | OHCL.RESOLVE_DEFAULT_HIERARCHY | stop | After current state and target values resolve |

## Refined Operational Readiness

- **BP-016 — Blocking control:** Before activating a new hierarchy or tree version, prove that all organizations referenced by active and historical projects and transactions are retained or safely mapped.
- **BP-017 — Operational control:** After organization additions, classification changes, or hierarchy type/version changes, hand off to `PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY` and verify completion independently.
- **BP-018 — Operational control:** Produce a hierarchy control report with organization, hierarchy/version, business unit, active dates, classifications, owning eligibility, expenditure eligibility, active-project count, and transaction volume.
