# Time Allocations Design Enforcement

## Source Basis

- User-provided edit restriction: Allocation Name and Effective End Date cannot be changed after a Time Allocation is created, 5 October 2026.

- User-authorized Time Consumer Sets timeCategoriesLOV pattern with verified TcatCd mapping for Time Allocations, 5 October 2026.

- User-provided Generic FSM Baseline, received 5 October 2026.
- User-requested correction separating fresh-export discovery from import readiness, 5 October 2026.
- Developer-provided Time Allocation UI Skeleton.
- User-provided verified Time Attribute field lookup contract, received 5 October 2026.
- User-provided verified Time Attribute data-source and value validation contract, received 5 October 2026.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce immutable allocation fields | Reject requests to change Allocation Name or Effective End Date on an existing allocation. Retain the read-only effective end date of 12/31/4712. After fresh export, verify the prepared edit preserves the existing name and end date. |
| 2 | Enforce allocation-type branching | Enable and require Summation Level only when Allocation Type is Hours. |
| 3 | Enforce numeric row rules | Require positive Hours and positive Attribute Display Sequence values. |
| 4 | Enforce Output-table column branching | Show Hours only for Hours allocations, Percentage only for Percentage allocations, no numeric column for Equally allocations, and selected Time Attributes as additional Output-table columns. |
| 5 | Enforce resolved Time Attribute columns | Represent each resolved Time Attribute as an Output-table column. |
| 6 | Validate FSM prerequisites | For catalog-routed FSM CSV Create or Edit, validate task-specific inputs, dependencies, and operation rules before obtaining an export. |
| 7 | Obtain fresh same-task baseline | Obtain a fresh export for ORA_HWM_MANAGE_TIME_ALLOCATIONS through shared.setup-export.task-level-export; stop if it cannot be obtained or validated. |
| 8 | Populate scoped changes | Populate only the approved task-specific change; preserve unrelated exported values. This scope approval is not submission approval. |
| 9 | Validate FSM package | Validate the ZIP retains exact-case ASM_SETUP_CSV_METADATA.xml, the task-scoped object CSV, valid keys, relationships, and approved row scope using the documented task-specific contract. |
| 10 | Route to Data Loader | Route the validated FSM ZIP to core.data-loader only when FSM evidence proves the expected import route. |
| 11 | Wait for preview | Wait for core.data-loader to produce the immutable package preview. |
| 12 | Require current approval | Obtain explicit approval for that current preview through core.data-loader; do not reuse stale preview or approval evidence or add a duplicate approval gate. |
| 13 | Submit once | Import once through the declared FSM route owned by core.data-loader. |
| 14 | Reconcile | Reconcile the result through the task's documented read/export path using its documented selectors; preserve diagnostics and stop on failure, partial success, timeout, or uncertainty. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | | Effective End Date differs from the fixed read-only value 12/31/4712, or an Edit requests changing the existing Effective End Date | Reject the end-date change; preserve the existing end date during Edit. If the exported value conflicts with the fixed-date rule, stop and report the discrepancy rather than rewriting it | No |
| Editing an existing Time Allocation | Error | | The request renames the allocation, or the prepared package changes its Allocation Name from the fresh same-task export | Reject the rename and retain the existing Allocation Name as the selection key. Do not reinterpret a rename as a Create operation | No |
| Allocation Type is Hours | Error | | Summation Level is blank or is not Time Card or Day | Select a valid Summation Level | Yes |
| Allocation Type is Equally or Percentage | Error | | Summation Level remains enabled or populated | Disable and clear Summation Level | Yes |
| A hours row is present | Error | | Hours is not greater than 0 | Provide a positive Hours value | Yes |
| Allocation Type is Hours | Error | | The Output table does not show the Hours column | Show the Hours column and do not show the Percentage column | Yes |
| Allocation Type is Percentage | Error | | The Output table does not show the Percentage column | Show the Percentage column and do not show the Hours column | Yes |
| Allocation Type is Percentage | Error | | Percentage is blank | Provide a Percentage value | Yes |
| Allocation Type is Percentage | Error | | A Percentage value is not greater than 0 | Provide a decimal value greater than 0 | Yes |
| Allocation Type is Percentage | Error | | The total Percentage across all Output-table rows is not 100 | Correct the Percentage values so their total is 100 | Yes |
| Allocation Type is Equally | Error | | The Output table shows a Hours or Percentage column | Remove numeric Output-table columns | Yes |
| A source row supplies a Time Category | Error | resolve_time_category | The source row TcatCd differs from the resolved category code or contains TcatId in place of that code | Use the resolver-returned TcatCd for that source row and retain the verified name for display | Yes |
| A Time Attribute is selected | Error | resolve_time_attribute_field | The resolved Time Attribute is not represented as an Output-table column | Add the resolved Time Attribute as an Output-table column using its DisplayName | Yes |
| An FSM package is being prepared after fresh export | Error | | A proposed change modifies unrelated exported values or exceeds approved row scope | Restore the unrelated values and prepare only the approved task-specific change | Yes |
| Catalog-routed FSM CSV Create or Edit | Error | | The FSM package is converted to an HCM Data Loader archive or a direct Fusion REST mutation is proposed | Retain the FSM ZIP and use core.data-loader through the declared FSM route | Yes |
| An FSM package is being validated after fresh export | Error | | FSM evidence does not prove the expected import route | Stop and rebuild the package from a validated fresh same-task export | Yes |
| Before FSM package preparation | Error | | The fresh same-task export does not establish the CSV members, headers, field mappings, valid keys, or relationships needed for the requested change | Stop and identify only the specific unresolved mapping or operation rule; do not invent keys or borrow another task's CSV contract | No |
| Before Data Loader handoff | Error | | The exact-case ASM_SETUP_CSV_METADATA.xml, task-scoped CSV, valid keys, or approved row scope has not been validated | Complete package validation against the fresh same-task export before preview | Yes |
| Before Data Loader handoff | Error | | The documented read/export path and selectors cannot identify and compare the allocation and its changed rows after import | Stop before submission and resolve the specific reconciliation gap from task guidance and export evidence | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_time_category | A source row supplies a Time Category | Verified TcatCd and TcatName | ora_reference_lookups.md |
| resolve_time_attribute_field | A Time Attribute is added or searched | Verified DisplayName, Name, and TimeAttrributeFieldId | ora_reference_lookups.md |

## FSM Handoff Boundary

Apply each enforcement-order step only at its stated stage. Before export,
validate business inputs, applicable dependencies, defaults, and documented
LOV behavior. Do not fail that stage merely because the fresh export and
package evidence do not yet exist.

The contract gate returns an export-workflow handoff when business validation
has passed and the catalog selects FSM CSV import. The invoking workflow must
then obtain a fresh same-task export through shared.setup-export.task-level-export,
inspect its CSV members, headers, mappings, keys, and relationships, verify
that every edited allocation retains its exported Allocation Name and Effective
End Date (including corresponding child references and date fields), and apply
the package-stage rules above. Preserve the task-specific supported operations,
fields, defaults, and LOV rules already documented here.

If export evidence cannot establish a required mapping, operation semantic,
or reconciliation selector, report that specific gap before import. The
baseline does not authorize guessing those details. Only a validated package
may proceed to core.data-loader for its immutable preview, current explicit
approval, one import, and documented reconciliation. Task-node completion
alone does not execute any of those external operations.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAL.ENFORCE_DESIGN | decision | 30 | design_enforcement | compliant->TAL.CHECK_EXECUTION_CONTRACT;blocked->TAL.HANDLE_DESIGN_ISSUE | TAL.APPLY_DEFAULTS | stop | A Time Allocations request has passed input validation and defaulting |
