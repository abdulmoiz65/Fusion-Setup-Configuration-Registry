# Learning Paths Reference Lookups

All calls in this file are read-only and target-scoped.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_learning_path_identity | Duplicate checking, non-create planning, or readback | Exact learningItemNumber preferred; learningItemId when available | GET hcmRestApi/resources/{version}/learningPaths using findByLearningItemNumber, PrimaryKey, or RowFinder with pLearningItemId; follow the returned item link | learningItemId, learningItemNumber, learningItemTitle, learningItemType, learningItemFormat, learningItemStatus, learningItemVisibility, learningItemLastModifiedDate, publication, validity, renewal, due, reassignment, and assignment status fields; links | Require exactly one number or ID match for an existing path; create stops on an exact-number duplicate; title is collision evidence only | Exact identity, parent state, item link, and normalized fingerprint | Stop the affected row on zero or multiple required matches; report duplicate create evidence |
| resolve_learning_path_existing_graph | Existing path validation, update, activation, deletion, or reconciliation | Returned item link from resolve_learning_path_identity | Follow the returned item link and request activitySections, nested activities, metrics, userActionHints, and whereUsed | Section IDs, numbers, statuses, order, completion rules, predecessor fields and activities-required; nested activity IDs, numbers, order, predecessor fields, elearn identity/status/type/format and activity status; metrics; hints; whereUsed | Require one complete snapshot; every predecessor must resolve inside the grouped path; fingerprint normalized order, membership, edges, usage, metrics, and last-modified evidence | Current manifest, graph, statuses, usage, learner-impact evidence, and fingerprint | Stop on missing children, duplicates, dangling edges, self-reference, cycles, or changed evidence |
| resolve_learning_path_change_request | A returned asynchronous change request is reconciled | Returned item link and exact changeRequestId | Follow the returned learningPaths item link to changeRequests | changeRequestId, status, processingStatus, processingStatusMeaning, reconcileLastRunProcessId, reconcileLastRunProcessDate, reconcileStartDate, reconcileEndDate, reasonCode, and reasonCodeMeaning | Require one exact change request; poll only while its documented processing status is nonterminal | Processing status, sanitized process identifier, dates, and reconciliation outcome | Stop on zero or multiple matches, undocumented status, failure, or timeout |
| resolve_learning_path_lifecycle_values | Activate or retire | Current and requested learningItemStatus | GET hcmRestApi/resources/{version}/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_WLF_ELEARNING_STATUS | LookupCode, Meaning, enabled status, validity, and lookup type | Require one exact current enabled target value and an FDD-allowed transition | Validated current status, target status, and transition evidence | Stop on a missing, disabled, expired, ambiguous, or transition-ineligible value |
| resolve_learning_path_loader_registration | Any create or update mutation is proposed | Exact business object learningPaths, target environment, and selected create or update operation | Resolve current business-object registration and paginated template, component, attribute, and supported-operation metadata through core.data-loader | Registration discriminator, exact business object, template, components, writable attributes, supported operation, and metadata fingerprint | Require exactly one current learningPaths registration and a template/component/attribute contract that supports the selected operation | Registration discriminator, template, components, writable attributes, operation, and fingerprint | Block the mutation on no or multiple registrations, missing metadata, or unsupported operation; Direct REST is allowed only for a separately named exception whose loader operation is proven unsupported |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A create or update mutation is requested | Run resolve_learning_path_loader_registration before preview and execute the supported mutation through core.data-loader; do not substitute Direct REST automatically |
| Read-only validation or an explicitly empty Draft is requested | Use the confirmed target contract without requiring an unrelated new-activity provider |
| A row adds or replaces an activity | Stop only that row while authoritative eligibility and relationship evidence is unavailable |
| A grouped graph is supplied | Resolve the current graph when applicable, then reject duplicate, dangling, self-referential, direct-cycle, and indirect-cycle edges |
| A change request is returned | Poll only the documented changeRequests child and do not generalize it to unrelated writes |
| A collection returns an item | Follow its returned item link; never construct the opaque item hash |
| Lookup evidence changes after preview | Invalidate the manifest and approval and rebuild both |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.RESOLVE_REFERENCE | decision | 3 | reference_lookup | resolved->LPT.APPLY_DEFAULTS;not_required->LPT.APPLY_DEFAULTS;blocked->LPT.HANDLE_ERROR | LPT.CHECK_DEPENDENCIES | stop | An applicable documented identity, graph, lifecycle, usage, or change-request lookup is required |
