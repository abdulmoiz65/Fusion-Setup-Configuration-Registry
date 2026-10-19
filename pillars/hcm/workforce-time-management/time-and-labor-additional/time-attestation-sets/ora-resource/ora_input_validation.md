# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Task identity | Exact task code ORA_HWM_MANAGE_ATTESTATION_SETS and task name Time Attestation Sets | Stop | Correct the task selection before export | Always | |
| Basic information | Name | Stop | Provide a nonblank Time Attestation Set name | Before create or edit | |
| Fresh same-task export | Current target-environment FSM ZIP and its export evidence | Stop | Obtain and validate a new export for this exact task | Before create or edit | |
| Approved change scope | Approved create or edit rows and operation intent | Stop | Obtain task-specific change scope | Before package preparation | |
| Update row scope | For an update, include the selected parent record and the complete desired child collection for that parent. Preserve every existing child row exactly as exported and add only the approved new or changed child rows | Stop | Rebuild the FSM ZIP without unrelated sets or child rows omitted from the selected parent collection | Before package preparation | |
| Complete Business Summary source | Verified structured business values after input validation, applicable lookup resolution, and defaulting | Stop before Core Data Loader handoff | Complete validation, lookup resolution, and defaulting; do not infer, format, or disclose unverified values | Before Core Data Loader handoff | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Export/import or CSV support remains UNKNOWN, or the export does not prove FSM routing | Blocked | Stop and record the catalog or route-evidence gap | |
| The ZIP contains exact-case ASM_SETUP_CSV_METADATA.xml, a task-scoped object CSV, valid export-confirmed keys, and approved rows only | Satisfied | Route the ZIP to core.data-loader for immutable preview | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| FSM CSV member layout and field names | Require ORA_HWM_ATTESTATION_SET.csv with ItrSetName, ItrSetId, ViewInstanceName, GroupingKey, ItrSetDescription, and ModuleId; and ORA_HWM_ATTESTATION_SET_LNS.csv with ORA_HWM_ATTESTATION_SET.ItrSetName, ItrSetName, ProcessingOrder, ItrSetLnId, ViewInstanceName, GroupingKey, QstnrVersionNum, QuestionnaireCode, TriggerEventCs, DisplayLevel, QuestionnaireName, TcatName, ItrSetId, QuestionnaireId, and TimeCategoryId | Before package preparation | |
| Name | Require a nonblank ItrSetName text value | Before package preparation | |
| Description | Accept an optional ItrSetDescription text value | Before package preparation | |
| Attestation section | Accept no attestation rows because the section is optional; require ProcessingOrder for every supplied row | Before package preparation | |
| Processing Sequence | Require a numeric ProcessingOrder for every supplied attestation row | Before package preparation | |
| Questionnaire | Accept a LOV value only after the Questionnaires endpoint returns exactly one QuestionnaireName that equals the supplied value after trimming only leading and trailing Unicode whitespace; map the provider-returned QuestionnaireCode, QuestionnaireName, QuestionnaireId, and VersionNumber to the CSV fields, with VersionNumber mapped to QstnrVersionNum | When an attestation row supplies a questionnaire | resolve_questionnaire_lov |
| Initiating Events | Accept a multiple-selection set containing only IN, OUT, Save, Submit, and Resubmit; group IN and OUT under Time Device Events, and Save, Submit, and Resubmit under Time Card Actions | When an attestation row is supplied | |
| Time Category | Accept a LOV value only after the documented timeCategoriesLOV lookup returns one exact TcatName match | When an attestation row supplies a time category | resolve_time_category_lov |
| Display Level | Require one nonblank value: Day, Detail, or Time Card | For every populated attestation row, before package preview | |
| Unrelated exported values remain unchanged | Reject the package and rebuild from a fresh export | Before preview | |
| Update package scope | Require exactly one parent CSV row and the complete desired child collection for the selected Time Attestation Set. Every existing child row from the fresh export must be retained exactly unless the approved change modifies or removes it; every added child row must be new or changed | Before preview | |
| Package type remains FSM ZIP | Reject an HCM Data Loader archive or another package type | Before preview | |
| Complete Business Summary coverage | Include every verified business value supplied by the user and every user-facing default actually applied; omit blank, null, unused, and metadata-only values | Before Core Data Loader handoff | |
| Complete Business Summary child records | Show a populated child section only when it has business values, using business labels only | Before Core Data Loader handoff | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAS_VALIDATE_FIELDS | step | 10 | validate_input | valid->TAS_DEFAULT_EVENTS;missing_or_invalid->RETURN_ISSUES | none | stop | A Time Attestation Set create or edit is prepared |
