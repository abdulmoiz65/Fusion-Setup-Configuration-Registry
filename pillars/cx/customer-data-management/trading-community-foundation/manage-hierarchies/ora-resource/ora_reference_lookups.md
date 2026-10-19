# Reference Lookups

Live hierarchy lookups use only GET requests and describe-discovered readable
projection fields. Supplied-file import routing is local validation owned by
`ora_input_validation.md`; it is not a Fusion lookup.

## Exact ADF Collection Filters

For an exact hierarchy collection lookup, send one `q` parameter with
semicolon-separated equality clauses. For example:

```text
q=TreeStructureCode='HZ_DNB_HIERARCHY';TreeCode='TREECODEFDOS'
```

Pass that value unchanged as one client query argument. Do not use a
SQL-style `and` between clauses: it can return zero rows even when the same
exact pair is present in the collection. Apply the same syntax whenever both
`TreeStructureCode` and `TreeCode` filter `fndTrees` or `fndTreeVersions`.
Use the same one-parameter semicolon form for an exact direct node fallback,
including the current-run `TreeVersionId`.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| describe_hierarchy_tree_resources | read_operation=describe or before a hierarchy collection read | Configured Fusion environment and fixed resource names | GET /fscmRestApi/resources/11.13.18.05/fndTrees/describe; GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions/describe; GET /fscmRestApi/resources/11.13.18.05/fndTreeNodes/describe | Resource names, readable attributes, query capabilities, child resources, and supported methods | Require a successful describe response for each requested resource; retain only GET-readable contract facts | Sanitized resource availability and readable schema summary | Report every unavailable or unauthorized resource; do not probe another namespace, version, or endpoint |
| read_ui_aligned_hierarchy_inventory | read_operation=list, including an unqualified list or show request | Optional exact TreeStructureCode, resolved as-of date, and current describe results | GET /fscmRestApi/resources/11.13.18.05/fndTrees and GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions, each with an exact TreeStructureCode query when supplied and pagination until hasMore=false | Describe-confirmed readable tree identity and display attributes; version TreeStructureCode, TreeCode, TreeVersionId, Status, EffectiveStartDate, EffectiveEndDate, and NodeCount; plus hasMore | Join versions to headers by the exact case-sensitive TreeStructureCode and TreeCode pair; retain only Status=ACTIVE, EffectiveStartDate less than or equal to the as-of date, EffectiveEndDate greater than or equal to the as-of date, and numeric NodeCount greater than zero; require at most one retained version for each exact hierarchy pair | One sanitized hierarchy-level row per eligible exact pair, selected version identity, NodeCount, applied criteria, as-of date, result count, and pagination completion for both collections | A completed zero-row result is valid; multiple eligible versions for one hierarchy are ambiguous; stop on an orphan version, missing required filter attribute, nonnumeric NodeCount, incomplete pagination, mismatched structure rows, authorization failure, or transport failure |
| read_hierarchy_tree_inventory | read_operation=inventory | Optional exact TreeStructureCode plus current describe result | GET /fscmRestApi/resources/11.13.18.05/fndTrees with an exact TreeStructureCode query when supplied and pagination until hasMore=false | Only attributes confirmed readable by current fndTrees describe, plus hasMore and links needed for this run | Without a supplied structure retain every accessible tree; with a structure require every returned row to match it exactly | Sanitized hierarchy inventory, result count, and pagination completion | An empty completed inventory is valid; stop on incomplete pagination, mismatched rows, authorization failure, or transport failure |
| read_hierarchy_tree_exact | read_operation=hierarchy_detail, versions, nodes, or full_read | Exact TreeStructureCode and TreeCode plus current describe result | GET /fscmRestApi/resources/11.13.18.05/fndTrees with exact TreeStructureCode and TreeCode filters and pagination until hasMore=false | Only attributes confirmed readable by current fndTrees describe, plus links needed for child traversal | Require exactly one row whose TreeStructureCode and TreeCode both match case-sensitively | Exact sanitized hierarchy detail and current-run child-link availability | No exact match is not found; more than one exact match is ambiguous; stop without selecting or fabricating an item key |
| read_hierarchy_versions | read_operation=versions, nodes, or full_read after one exact tree resolves | Exact hierarchy identity, optional TreeVersionId, and current describe result | GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions with exact TreeStructureCode and TreeCode filters and pagination until hasMore=false | Only attributes confirmed readable by current fndTreeVersions describe, plus links needed for node traversal | Return every exact-pair version; when TreeVersionId is supplied require exactly one exact match | Sanitized version candidates or exact version detail and current-run node-link availability | Empty results are not found; duplicate exact identifiers are ambiguous; stop on incomplete pagination |
| read_hierarchy_nodes | read_operation=nodes, or full_read with an exact TreeVersionId | Exact hierarchy and version resolved in the current run plus current describe result | Follow the FndTreeNode child link returned by the exact current-run version. When absent, GET `/fscmRestApi/resources/11.13.18.05/fndTreeNodes` with one exact `q` containing `TreeStructureCode`, `TreeCode`, and `TreeVersionId`; paginate until hasMore=false | Only attributes confirmed readable by current fndTreeNodes or returned-child describe, plus hasMore | Accept nodes only from the selected exact version and return every page | Sanitized node and relationship summary plus pagination completion | An empty completed collection is valid. The direct fallback requires all three exact current-run identifiers and a describe-confirmed readable contract; stop on identity mismatch, incomplete pagination, authorization failure, transport failure, or an unavailable fallback contract. |
| read_hierarchy_labels | read_operation=full_read after one exact tree resolves | Exact hierarchy response from the current run | Follow the FndTreeLabelVO child link returned by the exact current-run tree; paginate until hasMore=false | Only attributes exposed as readable by the returned child contract | Accept only rows reached from the exact current-run tree | Sanitized hierarchy-label summary and pagination completion | Report a missing child link or empty collection; do not probe another endpoint |
| read_hierarchy_data_source_parameters | read_operation=full_read after one exact tree resolves | Exact hierarchy response from the current run | Follow the FndTreeDataSourceParamsVO child link returned by the exact current-run tree; paginate until hasMore=false | Only attributes exposed as readable by the returned child contract | Accept only rows reached from the exact current-run tree | Sanitized data-source-parameter summary and pagination completion | Report a missing child link or empty collection; do not probe another endpoint |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Supplied hierarchy import | Resolve the fixed object, mode, volume, and activity order, then allow the selected shared/Core workflow and its declared dependencies to inspect and validate the CSV as required |
| Supplied hierarchy delete | Resolve Hierarchy or HierarchyNode with DELETE_RECORD. Do not run a row-identity or member-edge lookup before upload; the immutable supplied file is the approved scope and Fusion Import Management evaluates its rows. Run Trees lookups only when the user separately requests record-level verification and supplies the required identities outside the opaque CSV. |
| read_operation=describe | Run only the describe lookup and return the sanitized readable contract |
| read_operation=list | Describe first; paginate both header and version collections; apply ACTIVE, inclusive as-of-date effectiveness, and NodeCount greater than zero; then return one row per eligible hierarchy and disclose the criteria and as-of date |
| read_operation=inventory | Describe first, then return all completed matching header pages without applying version or node eligibility filters |
| read_operation=hierarchy_detail | Describe first, resolve one exact tree, and stop after its detail summary |
| read_operation=versions | Resolve one exact tree, then return every matching version |
| read_operation=nodes | Resolve one exact tree and its versions; require an exact TreeVersionId before following its returned node link or using the describe-confirmed exact node-triple fallback |
| read_operation=full_read | Resolve one exact tree, versions, labels, and data-source parameters; retrieve nodes only for an exact TreeVersionId |
| A GET response is uncertain, partial, or fails | Stop and report the classified failure; never replace it with a write, browser, alternate namespace, or guessed endpoint. A missing node child link may use only the declared exact `fndTreeNodes` fallback. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MH.READ_HIERARCHY | step | 4 | reference_lookup | resolved->MH.DONE_READ;unresolved->MH.ERROR | MH.DEFAULT_READ_OPERATION | stop | Execute only lookup branches applicable to a validated and defaulted read operation |
