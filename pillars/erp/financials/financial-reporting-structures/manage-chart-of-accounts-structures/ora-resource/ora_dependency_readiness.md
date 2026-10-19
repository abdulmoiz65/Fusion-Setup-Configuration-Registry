# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Referenced value-set metadata | For every requested segment, resolve an explicit ValueSetCode or SegmentCode_VS lookup candidate and verify compatible format and MaximumLength before structure package work |
| 2 | Chart of Accounts LOV | Confirm existence and obtain StructureInstanceId before FSM export |
| 3 | Qualified segment-label metadata | Resolve every assigned label and confirm it is nonglobal and permitted for COA segments |
| 4 | Segment tree metadata | When a default hierarchy is requested, verify the GL_ACCT_FLEX tree against the verified segment value set |
| 5 | Complete same-task FSM export | Export populated CSV data and ASM_SETUP_CSV_METADATA.xml after the absence decision; derive internal codes, CSV columns, XML values, and defaults |
| 6 | Template-only FSM export | Use only as a supplement when the complete export needs file-shape clarification |
| 7 | Data Loader import path | Submit the immutable FSM package only through core.data-loader after task validation, preview, and explicit approval |
| 8 | Oracle functional and EDM documentation | Resolve only documented defaults |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_object | Existing chart of accounts structure | Yes | Before FSM export, create, or import package | Verify | GET chartOfAccountsLOV then GET by StructureInstanceId | find_chart_of_accounts, get_chart_of_accounts | Idempotency | Provide precise COA Name if lookup is ambiguous | Existing COA identity and comparable detail |
| referenced_value_sets | Referenced segment value sets | Yes | Before FSM export, defaulting DefaultValueSetCode, or creating structure rows | Verify | GET valueSets using explicit ValueSetCode or SegmentCode_VS lookup candidate for every requested segment | find_value_set | A structure package must contain only verified compatible value-set references | An absent candidate is creation readiness, not a user-clarification or separate creation-approval request. A differing or ambiguous candidate still stops for an update-or-new decision. | Existing ValueSetId, ValueSetCode, ValidationType, ValueDataType, ValueSubtype, MaximumLength, and flags |
| qualified_segment_labels | COA-qualified segment labels | Conditional | One or more SegmentLabelCode values are assigned | Verify | Complete same-task segment-label export and qualified KFF label metadata | resolve_segment_label_code | Only nonglobal labels other than GL_GLOBAL can be assigned to COA segments | Provide the business classification or internal SegmentLabelCode for every assignment | SegmentLabelCode, GlobalFlag, allowed-domain result |
| segment_tree_context | Segment default hierarchy | Conditional | TreeCode or TreeStructureCode is supplied | Verify | FND_TREE_VL and value-set-filtered tree metadata | verify_segment_tree | The default hierarchy must use GL_ACCT_FLEX and belong to the segment value set | Provide TreeCode, TreeStructureCode, and DefaultValueSetCode | TreeCode, TreeStructureCode, DefaultValueSetCode, tree match |
| data_loader_import_path | Data Loader authorization | Yes | Before any live import | Ready | Approved immutable FSM ZIP and core.data-loader task-validation result |  | The FSM ZIP is package evidence only; it must not be submitted through a direct FSM import endpoint | Approve the exact package fingerprint and target environment | Approved source path, checksum, preview, and Data Loader handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COASTR.READY | step | 3 | resolve_dependency | ready->COASTR.LOOKUP | COASTR.VALIDATE | stop | Always |
