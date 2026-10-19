# Time Categories Error Handling

## Source Basis

- Developer-provided Time Categories UI structure, screenshot, task behavior, and FSM baseline, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Name is blank or not unique | Identify the Name validation failure and stop before preview. |
| Current Name is missing, absent from the fresh export, or matches multiple exported rows | Stop before preview and require one exact existing Time Category Name. |
| The requirement cannot establish the included entries, attributes, values, unit of measure, logic, or business purpose | Ask only for the missing business clarification and stop before adding conditions. |
| Multiple plausible Time Categories match the requirement | Present exact and close matches and require the user's selection; do not select one automatically. |
| A suitable existing Time Category is selected | Reuse it and stop; do not prepare a duplicate create package. |
| A delivered Time Category is targeted for edit | Stop and require reuse of the delivered definition or selection of a non-delivered category. |
| An existing Time Category is targeted without explicit update intent | Stop and explain that updating it can affect downstream rules, consumer sets, layouts, balances, and attestations. |
| A request includes downstream objects | Stop those actions; Time Consumer Sets, layouts, balance definitions, attestations, and profiles are outside this task. |
| Track Usage is changed during edit | Reject the change and preserve the existing value. |
| An added condition row omits Time Attribute or Value Type | Identify the incomplete row and stop before preview. |
| Condition grouping is unbalanced or an Operator is invalid | Identify the affected expression and stop before preview. |
| A Time Attribute search returns no results | Ask for another Time Attribute search term; do not select or populate expression-result fields. |
| A Time Attribute search returns multiple results | Show every Name and require the user's selection; do not select automatically. |
| A Time Attribute data source is missing, has a mismatched identity, or has blank ImplementationType | Stop before preview; do not populate expression-result fields or resolve Value. |
| A FORMAT_VALUE_SET supplied value violates its returned type or non-null constraint | Show the supplied value, AttributeType, every violated constraint, and the returned-metadata format requirement; ask for a corrected value. |
| A selectable ValuesList search has no results or several results | Ask for another search term or require the user to select one Code; do not select automatically or merge duplicate display values. |
| A Specific Value uses an undocumented ImplementationType | Stop before preview and request documented value-resolution rules. |
| A required resolved display or selection field is blank or does not contain its corresponding resolved value | Stop before preview; correct the export-shaped package from the fresh export without changing unrelated records. |
| Value Type is not Specific Value | Do not enable, request, resolve, validate, or search Value. |
| Fresh FSM export cannot be obtained or validated | Stop; do not use a cached, substituted, or converted archive. |
| Export-shaped FSM package validation fails | Stop before approval or import; correct the reported changed record, display or selection mapping, CSV business object, row, or cross-file reference and rerun validation. |
| The current export does not support the required Time Categories row contract or presents ambiguous structural invariants | Stop before approval or import; refresh the export or obtain task-contract guidance. Do not select a category record merely to copy its technical fields. |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not enter the provider-owned approval process and do not place a warning, diagnostic, or technical note in the summary. |
| A validated FSM ZIP link is absent or does not identify the exact validated package | Stop before approval; display a clickable link to the immutable validated package outside the Complete Summary. |
| Preview or approval is missing or stale | Stop before import and obtain current preview and approval evidence. |
| FSM import fails, partially succeeds, times out, or is uncertain | Preserve sanitized diagnostics, reconcile current state, and stop before retry. |
| An approved Time Categories submission is pending, running, In progress, or unavailable | Continue task-authorized status monitoring with the accepted request identity. Do not report completion or submit another load. |
| An approved Time Categories submission succeeds but authoritative read-back differs from the approved configuration | Classify the result as a verification mismatch. Preserve the request identity and read-back evidence; do not claim completion or retry automatically. |
| Delete is requested | Return unsupported without preparing an FSM package or invoking Fusion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field or condition-expression rule fails | Correct the affected business value and restart validation. |
| Input validation | Complete Summary source is blank, unverified, unresolved, or metadata-only | Correct the source values before generating the summary. |
| Approval blocker | The approval request omits a clickable link to the exact validated FSM ZIP | Display the immutable validated-package link outside the Complete Summary, then request approval. |
| Catalog mismatch | Time Attribute search returns no result, multiple unselected results, or a data source whose identity does not match the selected TimeAttrributeFieldId | Refine the search or select TimeAttrributeFieldId; do not populate expression-result fields. |
| Input validation | A FORMAT_VALUE_SET value violates AttributeType, Precision, Scale, or a non-null minimum or maximum | Show the violated constraints and request a corrected value. |
| Catalog mismatch | A Specific Value implementation type has no documented value-resolution contract | Request the required value-resolution rules before continuing. |
| Input validation | A required resolved display or selection field is blank or mismatched | Correct the package from the fresh export before preview. |
| Catalog mismatch | FSM export evidence does not prove the expected task package | Rebuild from a fresh same-task export. |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval. |
| Process failed | FSM import fails, completes with errors, partially succeeds, or is uncertain | Preserve diagnostics, reconcile current state, and stop before retry. |
| Process timeout | FSM import does not reach a terminal status in the allowed wait | Stop polling and retain the process for a later check. |
| Verification mismatch | A terminal-success request does not reproduce the approved category parent, group-expression, or ordered conditions in an authoritative export | Preserve the request identity and comparison evidence; investigate before any separately authorized correction. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Affected field or condition row, safe failure category, and one corrective action. |
| Time Attribute or Specific Value resolution is blocked | The selected or supplied input, safe failure category, all matching results or violated constraints as applicable, and one corrective action. |
| Complete Summary is blocked | Missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values. |
| Time Attribute resolution is blocked | Search term, retrieved match count after all pages, selected identity when present, data-source identity and ImplementationType when returned, and one safe corrective action. |
| Package or import failure | Task identity, stage, sanitized message, and one safe next action. |
| Timeout or uncertain result | Process identifier when available, last status, elapsed wait when relevant, and reconciliation path. |
| Verification mismatch | Accepted request identity, verified parent/group/condition differences, and one safe investigation path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Time Attribute search has zero or multiple unselected results, or the selected data source is absent, mismatched, or has blank ImplementationType | Do not populate TimeAtrbFldName or RefrencedTimeAtrbName, select a first result, or continue to preview. |
| Value Type is not Specific Value | Do not use valueSearchTermOrValue, call ValuesList, or perform FORMAT_VALUE_SET validation. |
| A Specific Value uses an unsupported ImplementationType | Do not infer a lookup, accept the supplied value, or construct an undocumented request. |
| A required resolved display or selection field is blank or mismatched | Do not preview, approve, or import the package. |
| A Complete Summary is presented | Do not expose identifiers, codes, keys, internal values, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw boolean values, diagnostics, or warnings. |
| FSM package evidence is missing | Do not use a cached package, change package type, or hand-build a substitute archive. |
| Preview or approval evidence changed | Do not reuse earlier approval. |
| Import failed, partially succeeded, timed out, or is uncertain | Do not automatically retry. |
| Authoritative category read-back differs from the approved normalized configuration | Do not report success or retry automatically. |
| Delete is requested | Do not prepare source data or invoke Fusion. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.ROUTE | step | 60 | execution_gate | ready->TC.LOADER_READY;blocked->TC.ERROR;unsupported->TC.ERROR | TC.ENFORCE | stop | A valid business-only Complete Summary is present and create or edit has passed the task-local gates; provider approval ownership remains unchanged |
| TC.ERROR | step | 70 | error_handler | handled->TC.RETURN_ISSUES | none | stop | A validation, dependency, lookup, package, approval, or import gate is blocked |
| TC.RETURN_NOT_REQUIRED | terminal | 76 | terminal | none | TC.INTAKE | stop | The requirement does not require a Time Category |
| TC.RETURN_CLARIFICATION | terminal | 77 | terminal | none | TC.INTAKE | stop | The requirement needs business clarification before a Time Category decision |
| TC.RETURN_SELECTION | terminal | 78 | terminal | none | TC.SELECT_EXISTING | stop | The user must choose between plausible existing Time Categories |
| TC.REUSE_EXISTING | terminal | 79 | terminal | none | TC.SEARCH_EXISTING | stop | A suitable existing Time Category is selected or exactly matched |
| TC.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue has been disclosed with one safe next action |
| TC.LOADER_READY | terminal | 90 | terminal | none | TC.ROUTE | stop | Time Categories is ready for the selected Core Data Loader FSM preview workflow |
| TC.FINAL_COMPLETION_ERROR | terminal | 96 | terminal | none | none | stop | Task-authorized monitoring reached failure, timeout, partial success, uncertainty, or category read-back mismatch. |
| TC.FINAL_COMPLETION_SUCCESS | terminal | 97 | terminal | none | TC.FINAL_COMPLETION | stop | Terminal success status and authoritative category read-back verification passed. |
