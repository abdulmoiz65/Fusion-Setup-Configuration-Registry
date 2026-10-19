# Reference Lookups

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_chart_of_accounts | Before any FSM export, package, or create | COA Name | GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV?q=Name='{COA Name}' | Name, StructureInstanceId, StructureInstanceCode, StructureInstanceNumber, Description, EnabledFlag | Exactly one Name match | Existing instance identity for detail lookup | Stop on no result or ambiguity; compare a match before continuing |
| get_chart_of_accounts | A unique StructureInstanceId was found | StructureInstanceId | GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV/{StructureInstanceId} | Name, StructureInstanceCode, StructureInstanceNumber, Description, EnabledFlag | Exact ID | Existing instance detail | Stop if the detail response is unavailable |
| resolve_segment_label_code | A segment business classification or SegmentLabelCode is supplied | Business classification, SegmentLabelCode, and complete same-task export | Read ORA_FND_APP_KEY_FLEXFIELD_STRUCTURE_SEGMENT_LABEL.csv from the complete export; use qualified KFF label metadata only when no matching export row exists | SegmentLabelCode, GlobalFlag | Exact internal code with GlobalFlag N and SegmentLabelCode not equal to GL_GLOBAL | SegmentLabelCode, GlobalFlag, allowed-domain result | Stop if the label is absent, ambiguous, global, GL_GLOBAL, or a custom label has no exported internal code |
| verify_segment_tree | TreeCode or TreeStructureCode is supplied | TreeCode, TreeStructureCode, DefaultValueSetCode | Read FND_TREE_VL and the value-set-filtered tree metadata from an approved Fusion metadata source or complete same-task export | TreeCode, TreeStructureCode, ValueSetCode | Exactly one tree with TreeStructureCode GL_ACCT_FLEX associated with DefaultValueSetCode | Verified TreeCode, TreeStructureCode, and value-set association | Stop when the tree is absent, ambiguous, uses another tree structure, or is not associated with the segment value set |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COASTR.LOOKUP | decision | 4 | reference_lookup | absent->COASTR.DEFAULT;match->COASTR.DONE_MATCH | COASTR.READY | stop | Always |
