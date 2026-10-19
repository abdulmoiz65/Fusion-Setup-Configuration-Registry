# Balance Groups FSM Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select FSM task CSV route | Use core.data-loader with a valid task CSV archive; leave the Data Loader business-object selection empty |
| 2 | Preserve complete scope | Validate all requested sections against the task template before submitting any part of a combined request |
| 3 | Preserve archive semantics | Retain the template's member layout, identifiers, null values, and child relationships; never rewrite the reference XML package into an invented CSV contract |
| 4 | Bind approval | Hand the exact final archive and scope evidence to Task Hook and the core.data-loader approval workflow |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every FSM import | Error | | A business-object selection, HDL conversion, or DAT-template validation is requested | Keep businessObject empty and use the FSM task CSV route | Yes; correct preparation before approval |
| A configuration-package ZIP is supplied | Error | | The archive has the configuration-package structure instead of the task CSV contract | Return FSM_CONFIGURATION_PACKAGE_UNSUPPORTED and obtain a task CSV export/template; do not inject ASM_SETUP_CSV_METADATA.xml | No automatic conversion |
| Definitions or default inclusions are requested | Error | | Their required records or relationships are absent or unmapped in the CSV artifact | Use the corresponding CSV template sections; do not reject solely because there is no pre-existing AttributeCode | Yes; with verified CSV specification |
| Restrictions or usages are requested | Error | | Their representation is not established by the selected task's template | Obtain the correct task contract; route a separately catalogued usage task through its own workflow when required | No guessed component or cross-task execution |
| A combined create request is prepared | Error | | Only the parent is represented, or any requested child section would be silently dropped | Complete the full request before import | No partial submission without a revised user request |
| Reference HAR is used during preparation | Error | | Captured POST/PATCH calls, returned IDs, UI naming conventions, or extra child selections are substituted for the requested FSM contract or scope | Use the HAR only as structural evidence; preserve the FSM route, verified CSV mappings and explicitly requested child selections | Yes; correct preparation before approval |
| Create is requested | Error | find_balance_group_by_name_and_ldg | The template's create/update semantics or intended target identity are unverified | Resolve those semantics before approval; never promise create-only behavior from an import archive alone | No guessed operation |
| Existing balance selections are requested | Error | resolve_defined_balance_by_name_and_dimension | The requested association has not been verified by its documented lookup | Resolve all requested selections before approving their CSV representation | No guessed reference or partial-parent creation |
| Category restrictions or default-inclusion categories are explicitly requested | Error | resolve_default_inclusion_balance_category | The requested category has not been verified | Resolve each requested category independently from its dimension | No substitution of a dimension for a category |
| Dimension restrictions or default-inclusion dimensions are explicitly requested | Error | resolve_default_inclusion_employee_dimension | The requested dimension has not been verified or its group level lacks a supplied lookup contract | Resolve each complete Employee-level dimension; obtain a separate contract for Organization-level dimension resolution | No implicit punctuation or similar-name match |
| Supported parent-only Employee create | Error | | A populated example or mapping waiver is demanded solely for fields already covered by ora_defaulting_rules.md, or unspecified child setup is added | Use the supplied values and documented preparation defaults, then retain normal duplicate checks, Data Loader preflight and exact-artifact approval | Yes; prepare the supported minimal archive before approval |
| Default-inclusion preparation or retry | Error | | A successful LOV query, matching CSV structure, compiled rule plan or approved trial is presented as proof that the FSM reference mapping works | Keep structural validation, reference existence, mapping evidence and import outcome separate. Preserve unresolved checks; a separately approved trial override is not a validation pass. Require terminal component and row results before reporting import success | Yes; correct evidence classification before approval |
| Reusing the documented successful child patterns | Error | | The task is blocked solely because all child mappings are treated as unsupported, a pre-existing HDL AttributeCode is demanded, or the source XML's empty category ID is enforced against the successful corrected default-inclusion variant | Apply the supported profiles in ora_reference_lookups.md with target-specific lookups and normal immutable-archive approval. Keep balance-definition selection and default inclusion as separately requested child scopes | Yes; use the documented successful structure |
| Adding an existing defined balance to a group | Error | | BalanceAttributeDefinitionVO metadata is used to add unrequested definition, category-restriction or default-inclusion rows, or to require a category lookup solely because the definition VO has a category field | Preserve the requested balance/dimension assignment and existing attribute linkage. When the verified link lookup is empty, include the supported new definition/group link needed by the requested children. Preserve existing appropriate linkage otherwise. Restriction changes still require an explicit request and their own mapping | Yes; restore requested child scope |
| Supported combined child update | Error | find_balance_group_attribute_links | Preparation stops solely because the group has no linked definition, or only one of the requested child sections is prepared | Resolve the parent and all requested references, prepare the complete immutable FSM ZIP with required supporting records, and continue through core.data-loader Task Hook. Use one exact-package approval; same-load explicit auto-approval follows core.data-loader without another confirmation | Yes; prepare the supported combined archive |
| Supported empty-group restriction update | Error | find_balance_group_attribute_links | The matching confirmed profile is rejected as universally unsupported, or an existing definition is modified without the profile's complete-empty-link precondition | Apply the supported parent/definition/link preparation after exact reference and state checks. A populated-group conversion or different flag transition needs separate evidence; do not delete or replace existing setup automatically | Yes; use the matching supported profile and normal archive approval |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_balance_group_by_name_and_ldg | Before approving a named group creation | Exact LDG-scoped parent cardinality; zero matches for create | ora_reference_lookups.md |
| resolve_defined_balance_by_name_and_dimension | Before approving requested balance selections | Verified defined-balance evidence for every requested pair | ora_reference_lookups.md |
| resolve_default_inclusion_balance_category | Before approving requested category restrictions or default-inclusion categories | Verified category evidence for each requested role | ora_reference_lookups.md |
| resolve_default_inclusion_employee_dimension | Before approving requested dimension restrictions or default-inclusion dimensions | Verified Employee dimension evidence for each requested role; other levels require their own contract | ora_reference_lookups.md |
| find_balance_group_attribute_links | Before preparing existing-group child additions | Complete parent-scoped linkage result and reuse versus supporting-record decision | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BG.ENFORCE_DESIGN | decision | 10 | design_enforcement | pass->BG.EXECUTION_GATE;blocked->BG.HANDLE_ERROR | BG.RESOLVE_DEPENDENCIES | stop | Input and preparation dependencies passed |

## Sources

- Developer request: use FSM setup import with no Data Loader business-object selection, 2026-10-08.
- Developer-supplied FSM configuration-package ZIP, inspected 2026-10-08. Only component and field names are retained here; exported setup values are not repository fixtures.
- The enclosing task SKILL.md owns the FSM CSV import contract and core.data-loader handoff.
- HAR evidence and Oracle public documentation are recorded in ora_reference_lookups.md; the capture establishes UI relationships, not an FSM adapter contract.
- Developer-supplied attribute validation endpoints and HAR category lookup, 2026-10-09; lookups validate references without changing the FSM CSV import route.
- Developer request to reuse the successfully imported minimal parent behavior, 2026-10-09; ordinary exact-artifact upload approval remains required.
- Developer restriction category/dimension lookup request, 2026-10-09; shared lookup mechanics and HAR evidence are owned by ora_reference_lookups.md.
- Developer-supplied VO/helper and repeated failed default-inclusion trials, 2026-10-09; successful local validation did not establish successful FSM reference resolution.
- Subsequent developer-confirmed corrected default-inclusion success and saved successful balance-assignment evidence, 2026-10-09; supported child patterns do not require repeat experimental-mapping waivers when the target contract is evidenced.
- Developer-supplied BalanceAttributeDefinitionVO and category helper, 2026-10-09; definition metadata does not expand an existing balance-assignment request.

- Developer-requested automatic combined child preparation, 2026-10-09, backed by the approved FSM CSV archive and retrieved successful component ProcessLog: one BalanceAttributeDefinition, one BalanceAttribute and one BalanceAttributeDefault processed with zero failures/warnings; the archive also contained their BalanceGroupInclusion link. No customer identifiers are retained here.
