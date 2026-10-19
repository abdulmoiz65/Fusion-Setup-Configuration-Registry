# Learning Paths Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target contract | Use the matching raw Describe for methods, finders, writable fields, child resources, lookup routes, and DFF contexts |
| 2 | Current path state | Resolve exact identity, structure, graph, validity, renewal, usage, metrics, and applicable change-request state |
| 3 | New activity eligibility | For only rows that add or replace activities, require authoritative eligibility and relationship evidence |
| 4 | Lifecycle or deletion safety | Resolve live status transitions for lifecycle changes and current usage for parent deletion |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| LPT-DEP-READ-CONTRACT | learningPaths target read schema | Yes | Identity, validation, preview, or reconciliation | Satisfied | Supplied raw target Describe: 16 nodes, 292 attributes, 41 LOV-decorated attributes, 239 queryable attributes | | Collection/item reads, exact finders, children, links, lookup routes, and contexts are confirmed for the described target | Refresh the contract after a target or release change | Target identity, fields, child resources, lookup routes, and contexts |
| LPT-DEP-WRITE-CONTRACT | learningPaths write contract | Yes | Supported parent, section, or nested-activity mutation | Satisfied | Supplied raw target Describe declares parent POST/PATCH/DELETE and child CRUD | | Supported methods and field schemas are known; copy is absent and upsert is not exposed | Select an explicit supported operation and follow returned links | Method, writable fields, required inputs, and returned links |
| LPT-DEP-IDENTITY | Existing path identity and duplicate evidence | Conditional | Create collision check or non-create operation | Lookup | Exact target finders and returned item links | resolve_learning_path_identity | Identity must not rely on title or a manufactured opaque hash | Supply an exact number or technical ID | Exact identity, item link, last-modified evidence, and fingerprint |
| LPT-DEP-EXISTING-GRAPH | Existing sections, activities, predecessor graph, and usage | Conditional | Existing path validation, update, activation, deletion, or reconciliation | Lookup | Confirmed activitySections, nested activities, metrics, userActionHints, and whereUsed | resolve_learning_path_existing_graph | Graph and safety decisions require one complete current snapshot | Resolve the current path before preview | Membership, order, edges, status, usage, metrics, and fingerprint |
| LPT-DEP-ACTIVITY | New or replaced activity eligibility and relationship evidence | Conditional | A row adds or replaces an activity | Blocked | No authoritative catalog-item resolver is available in the approved source set | | Current membership proves neither new-item eligibility nor relationship exclusivity | Defer that row or supply an approved resolver contract; unaffected rows may continue | Exact activity identity, status, type, format, eligibility, and relationship evidence |
| LPT-DEP-LIFECYCLE | Lifecycle value and transition | Conditional | Activate or retire | Lookup | commonLookupsLOV for ORA_WLF_ELEARNING_STATUS plus FDD transition rules | resolve_learning_path_lifecycle_values | The raw payload does not enumerate current enabled values | Resolve the live value and allowed transition before preview | Current status, target status, enabled evidence, and transition eligibility |
| LPT-DEP-CHANGE-REQUEST | Documented asynchronous change request | Conditional | A returned change request must be reconciled | Lookup | Confirmed learningPaths changeRequests child | resolve_learning_path_change_request | Only documented change-request processing may be polled | Use the returned change request identity | Processing status, process identifier, dates, and result |
| LPT-DEP-SECURITY | HCM security profile | Conditional | Visibility requires restricted access | Verify | hcm.hcm-security.hcm-security-profile | | Visibility cannot exceed established security | Resolve the applicable profile before preview | Exact security profile identity |
| LPT-DEP-EXTENSIBILITY | Target DFF contexts and segments | Conditional | Extensible attributes are supplied | Verify | Raw Describe confirms WLF_LEARNING_ITEM and WLF_LI_SPECIALIZATION; live target metadata supplies segments | | Environment-specific segments are not portable | Resolve exact current segments and values | Context, segment identifier, and validated value |
| LPT-DEP-DATALOADER | Data Loader BC REST registration and operation | Yes | Any create or update mutation | Lookup | Current core.data-loader business-object registration, template, component, attribute, and operation metadata | resolve_learning_path_loader_registration | Taxonomy mapping and REST availability do not prove a current loader registration or operation | Correct the learningPaths registration or use only an explicitly documented Direct REST exception whose loader operation is proven unsupported | Registration discriminator, exact business object, template, components, attributes, selected operation, and metadata fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All dependencies applicable to the selected rows and operation are exact | Read-only lookups may run; mutation still requires approval |
| Row Blocked | A dependency applies to only some rows | No for those rows; unaffected valid rows may continue |
| Operation Blocked | A required contract, lifecycle, usage, or approval condition is unresolved | No for that operation |
| Not Required | A conditional dependency does not apply | No lookup needed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->LPT.RESOLVE_REFERENCE;not_required->LPT.RESOLVE_REFERENCE;blocked->LPT.HANDLE_ERROR | LPT.VALIDATE_INPUT | stop | Applicable dependencies are evaluated per grouped path and selected row |
