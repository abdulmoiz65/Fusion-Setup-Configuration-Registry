# HCM Exclusion Rules Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A documented LOV returns no match | Block import and ask the user to provide a correct value |
| A documented LOV returns duplicates | Request the documented disambiguator and stop until it identifies one result |
| An attribute-based exclusion rule specifies an attribute that exclusionRuleAttributesLOV does not return for its selected exclusion type | Stop import and tell the user that the specified attribute cannot be used to define the exclusion |
| A set-backed attribute value has no exact setIdSets match, has multiple matches, supplied SetName and SetCode identify different rows, or the result lacks SetId or SetCode | Stop import and request one valid unambiguous reference-data SetName or SetCode; do not select a set by guesswork, place a name/code in AttributeValue, or omit the returned SetCode from AttributeSetCode |
| exclusionRules returns multiple same-name parents, a different ExclusionType, or no supported child collection for the selected ExclusionType | Stop package preparation and require one exact existing parent and supported child collection; do not create a duplicate parent or child row |
| A list child already exists | Omit that child detail row; do not create a duplicate child row |
| A matching attribute or hierarchy child exists without a usable ExclusionRuleDtlId | Stop package preparation; do not create another child row |
| The HCM exclusion-rule package omits a template-resolved CSV member, header, mapping, row relationship, metadata node order, or has an altered ASM_SETUP_CSV_METADATA.xml | Stop before package preparation. Export the task again and retain the fresh template and metadata unchanged |
| A generated row differs from the template-derived ViewInstanceName or GroupingKey pattern and applicable fallback, relationship, field mapping, or header order | Stop before package preparation. Correct the package only from the current resolver output and documented fallback; do not fabricate migration or linkage values |
| A generated detail row omits a required criterion field or places a value in a different field | Stop before package preparation. Correct the row using the documented task mapping: non-country list identifier to IdValue, country-list TerritoryCode to Value, attribute fields to FlexContext, ColumnName, TableName, Operator, and AttributeValue, Department Hierarchy or Department Tree to TreeCode and TopNodeValue, and Position Hierarchy or Supervisor Hierarchy to TopNodeValue |
| A package is requested before the required rule attributes and fresh validated task export are available | Stop before package generation; do not invent attributes, CSV rows, metadata, or parent-detail linkage |
| A CSV import is requested before the core Data Loader task-validation preview is built from the final archive | Classify as an approval blocker; build the task-validation preview before asking for approval |
| A separate package approval is requested in addition to task-validation approval | Classify as an approval blocker; request one approval only for the exact task-validation preview and archive |
| A Core Data Loader import fails or does not return a verifiable process log | Classify as process failed, preserve a sanitized diagnostic and process-log reference, and do not retry automatically |
| A direct REST create or update is requested | Stop as unsupported; do not send REST POST, PUT, or PATCH for HCM exclusion-rule configuration |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Blocked | A supplied rule fails input validation, lookup resolution, CSV layout validation, or design enforcement | Correct the configuration and restart validation |
| Approval blocker | The task-validation preview is missing, its single approval is missing, or its approved envelope does not match the exact archive | Stop before core.data-loader |
| Process failed | core.data-loader import fails or does not produce a verifiable process log | Persist a sanitized diagnostic and process-log reference; do not retry automatically |
| Ready | The rule passes validation, defaulting, design enforcement, and CSV readiness | Continue to the separately approved core.data-loader execution workflow |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any user-facing response | Show business display names, meanings, statuses, and next actions only. Do not expose internal IDs, lookup codes, column names, table names, flexfield context codes, GroupingKeys, or process identifiers. |
| A lookup fails | Show the affected display field and the required correction or disambiguator without exposing internal IDs or internal codes. |
| CSV import failure | Show the failure class, task name, sanitized status, diagnostic, and safe next action without exposing internal IDs or internal codes. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A resolver returns no match or ambiguous results | Do not choose a list, hierarchy, person, position, or organization value by guesswork |
| An attribute is not returned by exclusionRuleAttributesLOV for its selected exclusion type | Do not use that attribute to define the exclusion or substitute another attribute by guesswork |
| A set-backed attribute resolver returns no match or ambiguous results | Do not choose a reference-data set by guesswork, retain a SetName or SetCode in AttributeValue, substitute a different SetId, or omit/substitute the returned SetCode in AttributeSetCode |
| An existing parent or child cannot be reconciled through exclusionRules | Do not create a duplicate parent or child row, or replace a child identifier by guesswork |
| The verified CSV layout cannot establish a member, header, mapping, row relationship, or metadata contract | Do not create a CSV package or reuse an obsolete export. A missing ViewInstanceName or GroupingKey pattern alone uses the documented fallback. |
| A selected criterion cannot populate every required detail field or would use a different field | Do not create a CSV package. Resolve the missing value or correct the row through the documented task mapping; do not substitute IdValue, Value, TreeCode, TopNodeValue, or attribute fields. |
| The final task-validation preview is not available | Do not request package approval or invoke core.data-loader |
| A task-validation preview is available | Do not request a separate package approval; request one approval only for the exact task-validation preview and archive |
| An exclusion-rule create or update is requested | Do not use REST POST, PUT, or PATCH; prepare, approve, and submit the current export-backed CSV package through core.data-loader only |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMEX.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A task rule returns an issue |
| HCMEX.READY | terminal | 70 | terminal | none | HCMEX.CSV_READINESS | stop | HCM exclusion-rule validation, design enforcement, and CSV readiness are complete |
