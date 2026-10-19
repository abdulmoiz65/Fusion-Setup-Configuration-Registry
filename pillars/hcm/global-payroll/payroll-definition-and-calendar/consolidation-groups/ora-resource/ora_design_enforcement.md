# Consolidation Groups Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify operation and mechanism | Route supported Create and Update preparation to HCM Data Loader; keep Search, Read One, reference resolution, and monitoring read-only; stop unsupported Delete and FSM requests. |
| 2 | Resolve LDG scope and key representation | Establish one accessible LDG, use its exact returned Name under LegislativeDataGroupName for HDL, and retain its Fusion ID for read scope. |
| 3 | Complete Create duplicate preflight | Compare the proposed Name and Code exactly against every row in the resolved LDG using the literal current App UI query and complete paging. |
| 4 | Preserve record and business identity | Keep ConsolidationSetId, Name, business Code, generic Code, Meaning, and any metadata-confirmed update key distinct. |
| 5 | Validate HDL shape | Require the documented PayrollConsolidationGroup MERGE fields, matching metadata and data rows, optional CLOB-file packaging, and target metadata for deviations. |
| 6 | Protect loader execution | Require authorized access, exact preview, explicit approval, one submission, terminal status validation, and correction through a new archive after failure. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create or Update is prepared | Error | | A mutation mechanism other than HCM Data Loader is selected | Prepare the documented PayrollConsolidationGroup MERGE archive and hand it to a separately authorized HDL workflow | Yes |
| A group is needed by a dependent Payroll Definition or payroll process | Error | | No Consolidation Group exists in the required LDG | Create at least one group through the documented HDL mechanism before dependent setup | Yes |
| An LDG reference is used in an HDL record | Error | find_legislative_data_group_by_exact_name | The name doesn't resolve to exactly one accessible LDG, differs from the exact returned Name, or a Fusion ID is placed under LegislativeDataGroupName | Preserve the exact returned Name under LegislativeDataGroupName and retain the ID separately for read scope | Yes |
| A group is created | Error | | Explicit integration-key columns are included, Name or Code is missing or over 60 characters, LegislativeDataGroupName is missing, or an invented attribute is included | Omit explicit integration keys and use the verified ConsolidationSetName, LegislativeDataGroupName, ConsolidationSetCode, and optional Comments shape | Yes |
| A group is created | Error | check_consolidation_group_duplicate_by_ldg | The LDG is unresolved, paging is incomplete, the query is ambiguous or fails, or an exact Name or Code duplicate exists | Stop before preview or mutation; return the existing ID, Name, Code, LDG, and audit fields for a duplicate. A passed preflight permits preview only and never replaces explicit approval. | Yes |
| An existing group is updated | Error | find_consolidation_group_by_id_in_ldg | A View Business Objects-confirmed update key is unavailable, Code changes, LDG changes, or action-specific requiredness is unconfirmed | Preserve the existing Code and LDG; confirm the update key, action, and required attributes from target metadata | Yes |
| Comments are supplied | Error | | The data row contains CLOB text, the referenced UTF-8 file is absent, or the file is outside ClobFiles | Put the text in the referenced file under ClobFiles and place only the filename in Comments | Yes |
| A documented create load is prepared without the target View Business Objects export | Warning | | Optional attributes, extra actions, and target-release differences are presented as confirmed | Keep the create record within the verified working MERGE shape and identify the unavailable metadata; export it before relying on additional behavior | Yes |
| Update, Delete, or a nonexample HDL shape is prepared | Error | | The target Payroll Consolidation Group View Business Objects metadata has not been reviewed | Export and review supported actions, keys, fields, lengths, and CLOB rules before preparation | Yes |
| Search or Read One is prepared | Error | search_consolidation_groups_by_ldg | LDG scope is absent, paging is ignored, a retained keyword can hide the target, or a dedicated item route is invented | Resolve the LDG, use the documented read-only collection, follow paging, and exact-match IDs client-side | Yes |
| A group identity is stored, compared, mapped, or displayed | Error | | Fusion ID, metadata-confirmed update key, Name, business Code, generic Code, or Meaning are substituted for one another | Preserve each value and use the operation-specific key | Yes |
| A Payroll Definition selector is used | Error | list_consolidation_group_payroll_references_by_ldg | No explicit Code and Meaning pair is selected or generic Code is called ConsolidationSetCode | Require explicit selection and map generic Code to the selected ID only | Yes |
| Loader completion is evaluated | Error | get_hdl_data_set_status | Success is inferred from upload, submission, a nonterminal status, or the data-set status alone | Review terminal data-set status, PayrollConsolidationGroup status, counts, and relevant messages | Yes |
| A loader phase fails | Error | list_hdl_data_set_messages | The failed archive is retried automatically or messages are ignored | Correct the source, build a new archive, submit as a new load only with approval, and preserve sanitized failure evidence | Yes |
| Internal payrollGeneric Create, Update, or Delete is prepared | Error | | An internal Redwood mutation service is treated as the supported data-changing route | Stop and use HCM Data Loader for supported Create or Update | No |
| Delete is requested | Error | | View Business Objects metadata does not confirm a supported delete action and keys | Stop until the target contract is supplied | No |
| FSM Import or FSM Export is requested | Error | | General FSM guidance or catalog flags are treated as a task-specific schema and action contract | Stop until action, schema, keys, scope, status, and errors are verified | No |
| Country-specific behavior is presented | Error | | A distinct field, label, type, or validation is invented | Use the confirmed core Name, LDG, and optional Description pattern | Yes |
| Protected data or operations are handled | Error | | Authentication, privilege, LDG data security, approval, or redaction is bypassed | Require authorized access and redact credentials, tenant values, audit identities, trace data, and routing data | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_legislative_data_group_by_id | A Fusion LDG ID establishes task scope or must resolve to an HDL LDG name | LegislativeDataGroupName, LegislativeDataGroupId, LegislationCode | ora_reference_lookups.md |
| find_legislative_data_group_by_exact_name | An LDG name establishes task scope or an HDL reference | LegislativeDataGroupName, LegislativeDataGroupId, LegislationCode | ora_reference_lookups.md |
| check_consolidation_group_duplicate_by_ldg | Create is prepared or submitted | DuplicatePreflight or existing ConsolidationSetId, Name, Code, LDG, and audit fields | ora_reference_lookups.md |
| search_consolidation_groups_by_ldg | A list or keyword search is required | Group rows and paging state | ora_reference_lookups.md |
| find_consolidation_group_by_id_in_ldg | Read One or Update precheck is required | ID, Name, Code, Comments, audit values, LDG ID | ora_reference_lookups.md |
| list_consolidation_group_payroll_references_by_ldg | Payroll Definition choices are required | Generic Code and Meaning pairs | ora_reference_lookups.md |
| get_hdl_data_set_status | Loader progress or completion is evaluated | Request ID and terminal data-set status values | ora_reference_lookups.md |
| list_hdl_business_object_statuses | Loader progress or completion is evaluated | PayrollConsolidationGroup import and load status and counts | ora_reference_lookups.md |
| list_hdl_data_set_messages | Loader progress is reviewed or a phase fails | Sanitized confirmed business-object and record messages | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.ENFORCE_DESIGN | decision | 5 | design_enforcement | pass->CG.EXECUTE_OR_RETURN;blocked->CG.HANDLE_ERROR | CG.APPLY_DEFAULTS | stop | Any Consolidation Groups request |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle Fusion Cloud HCM, Example of Loading Payroll Consolidation Group: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-payroll-consolidation-group.html
- Oracle Fusion Cloud HCM, Examples of Using Consolidation Groups: https://docs.oracle.com/en/cloud/saas/human-resources/fapus/examples-of-using-consolidation-groups.html
- Oracle Fusion Cloud HCM, Using the HCM Data Loader REST API: https://docs.oracle.com/en/cloud/saas/human-resources/tutorial-hdl-rest/index.html
