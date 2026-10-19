# Consolidation Groups Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Search, Read One, Create, Update, Monitor Load, Delete, FSM Import, or FSM Export | Stop and request one operation | Classify the operation before choosing a mechanism | Always | |
| Legislative Data Group reference | Fusion LegislativeDataGroupId or exact Legislative Data Group name | Stop before LDG-scoped work | Resolve exactly one accessible LDG by ID or exact name; use its exact returned Name under LegislativeDataGroupName for HDL and retain its ID for read scope | Search, Read One, Create, Update, or Payroll Definition reference selection | |
| Documented HDL group fields | ConsolidationSetName and ConsolidationSetCode; Comments is optional | Stop and identify each missing required value | Supply Name and immutable Code for the documented MERGE shape | Create or Update | |
| Create duplicate preflight | Resolved LegislativeDataGroupId, ConsolidationSetName, and ConsolidationSetCode | Stop before create preview or submission | Complete the exact LDG-scoped duplicate query; require no exact Name or Code match and hasMore=false | Create | check_consolidation_group_duplicate_by_ldg |
| Update record key | View Business Objects-confirmed user key or Fusion surrogate ID | Stop before preparing Update | Export the target Payroll Consolidation Group metadata and use only a supported update key | Update | |
| Comments content | Comments filename and matching UTF-8 file under ClobFiles | Stop before packaging Comments | Put the description text in the named file and place only its filename in the data row | Create or Update when Comments are supplied | |
| Search scope | LegislativeDataGroupId; SearchTerm is optional | Stop and request an accessible LDG | Resolve the LDG before running the LDG-scoped collection lookup | Search | search_consolidation_groups_by_ldg |
| Read-one scope | LegislativeDataGroupId and ConsolidationSetId | Stop and request both identifiers | Search the complete LDG-scoped collection and require one exact ID match | Read One | find_consolidation_group_by_id_in_ldg |
| Loader monitoring scope | RequestId | Stop and request the loader request ID | Use the request ID returned by the separately authorized HDL submission workflow | Monitor Load | get_hdl_data_set_status |
| Payroll Definition group reference | LegislativeDataGroupId and an explicitly selected generic Code and Meaning pair | Stop and request the LDG or selection | List eligible groups for the LDG and require explicit selection | Payroll Definition reference selection | list_consolidation_group_payroll_references_by_ldg |
| Target HDL metadata | Exported Payroll Consolidation Group metadata from View Business Objects | Stop before relying on an unconfirmed update key, shape, or action | Export the target-environment metadata and confirm actions, keys, requiredness, lengths, and CLOB handling | Update, Delete, or any shape outside the documented create MERGE example | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Fusion LDG ID is supplied | Valid only when one accessible LDG with that exact ID resolves | Use the exact returned Name under LegislativeDataGroupName and retain the ID for search or verification | verify_legislative_data_group_by_id |
| An LDG name is supplied | Valid only when one accessible LDG has the exact name | Preserve the exact returned Name under LegislativeDataGroupName and retain the returned ID for search or verification | find_legislative_data_group_by_exact_name |
| Create is requested | Valid only when LegislativeDataGroupName, ConsolidationSetName, ConsolidationSetCode, any optional Comments file, and a passed exact duplicate preflight are ready | Prepare PayrollConsolidationGroup.dat without explicit integration-key columns and add an optional ClobFiles entry; require immutable preview and explicit approval before mutation | check_consolidation_group_duplicate_by_ldg |
| Update is requested | Valid only with a View Business Objects-confirmed user key or Fusion surrogate ID, unchanged Code, and metadata-confirmed action-specific requiredness | Prepare a MERGE record using the confirmed update key and supported changed attributes | |
| Monitor Load is requested | Valid only when the data-set status, PayrollConsolidationGroup business-object status, and messages can be reviewed | Require terminal transfer, import, and load results with zero relevant errors before reporting success | get_hdl_data_set_status |
| A group is selected for a Payroll Definition | Valid only after an explicit Code and Meaning selection | Map generic Code to the selected ConsolidationSetId; do not relabel it as ConsolidationSetCode | list_consolidation_group_payroll_references_by_ldg |
| Delete is requested | Unsupported until View Business Objects confirms a delete action and key contract | Stop without preparing or executing delete | |
| FSM Import or FSM Export is requested | Unsupported from the supplied task-specific evidence | Stop until a task-specific action, schema, keys, scope, status, and error contract is supplied | |
| Internal payrollGeneric Create, Update, or Delete is requested | Invalid mutation route | Use HCM Data Loader for supported Create or Update preparation; do not use internal Redwood mutation services | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is one of Search, Read One, Create, Update, Monitor Load, Delete, FSM Import, or FSM Export | Reject an unclassified operation | Always | |
| Business object is PayrollConsolidationGroup and data file is PayrollConsolidationGroup.dat | Reject a different component or filename for this task | Create or Update | |
| Record action is MERGE | Reject an undocumented action | Create or Update | |
| METADATA and MERGE rows have matching ordered fields and delimiter counts | Reject a malformed data-file shape before packaging | Create or Update | |
| Explicit integration-key owner and identifier columns are absent | Reject SourceSystemOwner, SourceSystemId, or other fabricated integration-key columns from resource-generated create records | Create | |
| LegislativeDataGroupName is the exact Name returned by one accessible LDG lookup | Reject an unresolved or ambiguous name, an ID placed under the name header, or a value that doesn't match the returned Name exactly | Create or Update | find_legislative_data_group_by_exact_name |
| Update key is supported by exported View Business Objects metadata | Reject an invented, default-generated, or otherwise unconfirmed update key | Update | |
| ConsolidationSetName is nonblank and no longer than 60 characters | Reject a blank or overlength value | Create or Update | |
| ConsolidationSetCode is nonblank and no longer than 60 characters | Reject a blank or overlength value | Create or Update | |
| Create duplicate preflight compares both identities exactly and hasMore is false | Reject a duplicate, incomplete page set, ambiguous result, authentication failure, or transport failure before preview | Create | check_consolidation_group_duplicate_by_ldg |
| ConsolidationSetCode remains unchanged for an existing group | Reject an attempted Code change | Update | |
| Comments contains only a filename whose UTF-8 file exists under ClobFiles | Reject direct CLOB text, a missing file, or a file outside ClobFiles | Create or Update when Comments are supplied | |
| Identifiers preserve exact values | Stop before a conversion that may lose precision or substitute one identifier type for another | Any identifier is parsed, compared, displayed, or written to a data file | |
| Audit fields and ObjectVersionNumber are not caller-maintained | Reject caller-supplied audit or version fields | Create or Update | |
| Effective dates, child resources, expansions, and invented HDL attributes are absent | Reject unsupported fields | Create or Update | |
| Loader completion includes terminal data-set and PayrollConsolidationGroup import and load results with zero relevant errors | Do not report success from upload, submission, or a nonterminal status | Monitor Load | get_hdl_data_set_status |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.VALIDATE_INPUT | decision | 1 | validate_input | valid->CG.RESOLVE_DEPENDENCIES;invalid->CG.HANDLE_ERROR | none | stop | Always |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle Fusion Cloud HCM, Example of Loading Payroll Consolidation Group: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-payroll-consolidation-group.html
- Oracle Fusion Cloud HCM, Supported Key Types: https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/supported-key-types.html
- Oracle Fusion Cloud HCM, PAY_CONSOLIDATION_SETS: https://docs.oracle.com/en/cloud/saas/human-resources/oedmh/payconsolidationsets-23509.html
