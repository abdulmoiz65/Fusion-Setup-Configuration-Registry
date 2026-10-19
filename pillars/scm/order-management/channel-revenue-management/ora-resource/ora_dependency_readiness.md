# Channel Adjustment Types Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_CJM_MANAGE_ADJ_TYPES | Manage Channel Adjustment Types | 1 | Reference Data Set | When SetName is supplied, resolve one exact Reference Data Set before validating the adjustment-type archive. |
| ORA_CJM_MANAGE_ADJ_TYPES | Manage Channel Adjustment Types | 2 | Channel Adjustment Type | Use the resolved set identity as evidence for the adjustment-type validation; do not create or alter the set in this task. |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | 1 | DFF parent and context carriers | Derive the mandatory DFF parent and requested context parent carrier rows from the supplied DFF code, resolved application ID, source context codes, and current task template. When available, use the current task-level export only to reconcile existing carrier values. |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | 2 | DFF task-template contract | Obtain the selected setup-task template and validate the supplied global and context segment rows against its exact CSV member headers. |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | 3 | Value set | When a source gives a value-set name rather than a code, resolve the exact current code and validation contract before preparing the segment row. |
| ORA_CJM_MANAGE_CHANNEL_VALUE_SETS | Manage Channel Value Sets | 1 | Value-set parent carrier | Resolve the exact value-set code, then obtain the matching current FSM parent carrier when the value set already exists. |
| ORA_CJM_MANAGE_CHANNEL_VALUE_SETS | Manage Channel Value Sets | 2 | Child value rows | Validate each child row against the selected task template before assembling the immutable FSM package. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_CJM_MANAGE_ADJ_TYPES | Manage Channel Adjustment Types | CJMAT.REFERENCE_DATA_SET | Reference Data Set | Yes | SetName is supplied for an adjustment type | Lookup | Fusion setIdSetsLOV | resolve_reference_data_set | The adjustment type must reference one valid reference data set. | Supply an existing exact SetName; if the set does not exist, create it through the ERP reference-data-set task and retry after it is available. | SetCode; SetName |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | CJMDF.TASK_TEMPLATE | DFF task-template contract | Yes | A DFF segment import source is supplied | Lookup | Current task template; matching current task export carrier when available | validate_dff_segment_against_task_template | A segment CSV row must use the selected task's exact supported header contract and valid parent hierarchy. | Supply the target DFF and required segment identity values. The workflow derives the DFF parent and requested context parent carriers; it does not require a user-supplied FSM extract. | DescriptiveFlexfieldCode; ApplicationId; SegmentCode; SegmentIdentifier; ColumnName |
| ORA_CJM_MANAGE_CHANNEL_VALUE_SETS | Manage Channel Value Sets | CJMVS.VALUE_SET_PARENT | Value-set parent carrier | Yes | A value-set import source is supplied | Lookup | Exact value-set REST collection result; current task FSM export | resolve_value_set_by_exact_code | Child values require a matching template-supported parent carrier. A REST result confirms identity only and must not be converted into an FSM parent row. | Supply a Value Set Code and preserve the matching exported parent carrier. For a new value set, supply the template-supported technical parent values. | ValueSetCode; ModuleId; parent carrier state |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_CJM_MANAGE_ADJ_TYPES | Manage Channel Adjustment Types | DEPENDENCY_BLOCKER | The Reference Data Set is missing or ambiguous | Lookup: yes; Create: no |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | DEPENDENCY_BLOCKER | The supplied segment cannot satisfy the current task-template contract | Lookup: yes; Create: no |
| ORA_CJM_MANAGE_CHANNEL_VALUE_SETS | Manage Channel Value Sets | DEPENDENCY_BLOCKER | The exact value set cannot be resolved or an existing parent carrier is absent from the current task export | Lookup: yes; Create: no |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_CJM_MANAGE_ADJ_TYPES | Manage Channel Adjustment Types | CJMAT.RESOLVE_REFERENCE_DATA_SET | decision | 1 | resolve_dependency | resolved->CJMAT.FIND_REFERENCE_DATA_SET;not_applicable->CJMAT.FIND_ADJUSTMENT_TYPE_BY_CODE;blocked->RETURN_ISSUES | none | stop | A Channel Adjustment Types archive is prepared for validation |
| ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS | Manage Channel Descriptive Flexfields | CJMDF.RESOLVE_DFF_PARENT | decision | 2 | resolve_dependency | resolved->CJMDF.RESOLVE_VALUE_SET_CODE;not_found->CJMDF.RETURN_ISSUES;ambiguous->CJMDF.RETURN_ISSUES;blocked->CJMDF.RETURN_ISSUES | CJMDF.VALIDATE_DFF_INPUT | stop | A DFF segment import source identifies a target DFF code |
| ORA_CJM_MANAGE_CHANNEL_VALUE_SETS | Manage Channel Value Sets | CJMVS.RESOLVE_PARENT_CARRIER | decision | 2 | resolve_dependency | resolved->CJMVS.RESOLVE_VALUE_SET;blocked->RETURN_ISSUES | CJMVS.VALIDATE_FSM_INPUT | stop | A value-set source identifies its parent code and selected FSM template |
