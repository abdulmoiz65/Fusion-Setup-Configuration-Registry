# Balance Groups FSM Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| FSM_CONFIGURATION_PACKAGE_UNSUPPORTED | Explain that this is a limitation of the current FSCR task CSV adapter, not lack of Oracle XML configuration-package support. Obtain a task CSV export/template through shared.setup-export.task-level-export; Oracle's documented Manage Configuration Packages procedure is a separate workflow and must not be silently substituted |
| FSM_CSV_ARCHIVE_REQUIRED | Stop before authentication, upload, or import when local format validation fails; identify the required archive format |
| FSM_FIELD_MAPPING_REQUIRED or FSM_SCOPE_UNVERIFIED | First resolve the declared references and apply every matching successful profile/default, including new supporting definition/link and numeric-dimension child rows. Prepare all resolvable requested rows as a reviewable draft before reporting genuine remaining gaps. Do not repeat trial waivers for the now-successful pattern, invent IDs, or submit a partial package |
| Existing group has no linked attribute definition | A complete empty lookup is a preparation branch, not an unsupported-child error. Include the supported definition/group link and all requested children in one FSM CSV ZIP; continue through validation and the normal Data Loader approval/upload lifecycle |
| Parent-only Employee create uses the documented preparation defaults | Do not classify the supported mapping or blank defaults as missing, require another populated sample, or ask for a trial-mapping waiver. Proceed through ordinary validation and upload approval; a real template mismatch or lookup failure still blocks |
| Task context still contains a business object after switching to FSM | Refresh the local task plan and context from the generated task manifest before approval; preserve the selected task and existing Run Book binding |
| Template export times out | Preserve TaskCode, ProcessId, environment, last status and elapsed wait; follow the export skill's next-check policy and do not submit a duplicate export |
| Archive changes after preview or approval | Stop and repeat preparation and the Data Loader approval workflow for the changed bytes |
| Fusion import fails or partially succeeds | Use core.data-loader status diagnostics and applicable FSM ProcessLog; distinguish failed and successful data and reconcile before retry |
| PAY_BALDF_CHILD_BAL_CAT on BalanceAttributeDefault | Classify the import as process failed and the preparation gap as FSM_FIELD_MAPPING_REQUIRED. A category LOV match does not prove that the CSV category key resolves. Compare the failed row with the category key contract, including effective dates; report unresolved fields without claiming the category is absent from Fusion or that one speculative change is sufficient. Stop before another preview until the mapping passes input validation |
| Category resolution fails for multiple verified categories with dates populated | Report a repeated category-resolution failure in the FSM path. Adding dates and changing the category did not resolve the observed failures. Compare the supplied named-reference/null-sentinel profile before another trial; do not claim an exact root cause, ignored IDs, unsupported categories or a proven separator fix from the error message alone |
| Named-reference trial also returns PAY_BALDF_CHILD_BAL_CAT | Record that the named-reference profile did not resolve the observed failure; do not recommend repeating that same change as a proven fix. A category failure does not establish that later dimension or attribute references passed. Apply the developer-confirmed FSM helper and foreign-key expression in ora_reference_lookups.md when preparing a correction. Retain remaining unverified field mappings as such and obtain exact-archive approval for a revised trial |
| XML mapping sample contains null IDs and literal #null LDG IDs | Identify differences from the prepared CSV using the reference evidence. Do not replace the requested category or dimension with the sample values, derive a base name from an ID, treat all null forms as equivalent, or submit again until missing target mappings are resolved or explicitly waived for a separately approved trial |
| Service-V3 helper evidence differs from the FSM CSV column names | Accept the developer's confirmation that FSM uses the supplied helper and apply its COALESCE foreign-key expression. Do not block solely on the absence of a separate caller file, add service attributes as CSV columns, or switch import routes. If resolution still fails, inspect the actual CSV field assignments and runtime name/context/date binds; numeric-input precedence and successful import remain separate questions |
| BalanceAttribute succeeds while BalanceAttributeDefault fails | Preserve the successful balance assignment. Prepare any corrected retry with only failed default-inclusion rows and template-required companion files; do not replay successful child rows. Changed bytes require fresh validation and exact-artifact approval |
| Developer confirms the corrected default-inclusion import succeeded | Record developer-confirmed runtime success of the named-reference-plus-category-FK profile in ora_reference_lookups.md. Supersede earlier blanket no-success or unsupported-mapping findings for that profile. Do not invent server counts or claim a fresh status query; for a later status request use the Data Loader status workflow. Preserve target-specific reference checks for subsequent loads |
| Attribute-definition identity or dimension resolution remains ambiguous | Identify the unresolved field and its actual helper from BalanceAttributeDefinitionVO. BalanceCategoryUserKeyHelper resolves only the category. BalanceDimensionUserKeyHelper and BalanceDimensionIdKHPVO are now supplied: apply their code/display-name precedence and LDG context from ora_reference_lookups.md; do not request them again. Ask for the still-missing attribute-definition helper or CSV-to-helper binding only when that specific new mapping needs it. Do not block supported assignments/default inclusions solely because another helper or mapping is unsupplied |
| An upload or initiation result is uncertain | Do not replay automatically; use the declared reconciliation/status route before any separately approved retry |
| Successful UI HAR supplied while FSM preparation is blocked | Report the captured success only for that UI example. Identify the remaining CSV schema/artifact gap; do not report the user's requested group as created or replay the UI mutations |
| LOOKUP_ENVIRONMENT_MISMATCH or LOOKUP_CONTRACT_UNAVAILABLE | Stop the lookup; report the selected environment and failing sanitized route. Do not change the supplied versioned path or combine reference IDs from different environments |
| LOOKUP_PARENT_CONTEXT_REQUIRED | The defined-balance search requires verified parent context. Identify the missing lookup prerequisite; do not reuse example IDs, invent a placeholder ID or create a partial parent |
| LOOKUP_RESULT_INCOMPLETE | Report the returned page count and paging inconsistency. Use the documented pBalanceName-filtered request for balance selections; do not declare the balance absent from an unfiltered or capped response |
| Reference lookup has no exact match or multiple matches | Report the unresolved requested reference and match count. Preserve the complete dimension wording; ask for clarification of a similar-name candidate instead of silently selecting it |
| Parent lookup finds an existing group during create | Report that the parent already exists and block duplicate creation. Parent existence does not prove requested child setup exists; do not switch to update without a revised operation |
| Organization-level dimension restriction or default inclusion is requested | Return LOOKUP_CONTRACT_UNAVAILABLE before GET; the supplied findEmployeeLevelDimensions criterion covers Employee only. Obtain the corresponding lookup contract; do not change GroupLevelFlag or silently skip the requested dimension |
| Category source points to a dimension endpoint | Use only the separate category contract documented from the supplied HAR; never fill BalanceCategoryId from BalanceDimensionId |
| Restriction reference resolution succeeds but the CSV restriction mapping is incomplete | Retain the resolved category FK or dimension ID with its restriction role and identify the missing CSV fields or relationship as FSM_FIELD_MAPPING_REQUIRED. Do not discard the valid reference result, copy a default-inclusion row as a restriction, or infer parent restriction flags or clearing behavior from an omitted input |
| Parent restriction flag update is rejected, followed by an attribute-definition category rejection | Report the parent rejection first and the dependent definition error separately. A saved UI export or supplied category/dimension helper does not establish the permitted parent transition. Compare the target's current flags and children with the exported state; obtain the parent BalanceGroup VO/entity validation or import implementation for the rejected flag before claiming a root cause or correction. Do not diagnose unresolved category/dimension references when their exact lookups passed, or automatically delete/recreate existing setup |
| Employee restriction XML export contains no assignments/default inclusions | Use its definition/link and named-reference evidence from ora_reference_lookups.md without claiming successful FSM execution. It does not prove a safe conversion of a populated unrestricted group, an automatic parent flag change from child rows, or preservation of existing children |
| Developer confirms the empty-group restriction FSM load passed | Apply Supported Empty-Group Restriction Preparation from ora_reference_lookups.md for matching targets without another experimental-mapping waiver. Keep developer-confirmed success separate from independently retrieved process results. The earlier populated-group rejection remains unresolved and does not make all FSM parent flag updates unsupported |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preparation | Produce the full FSM ZIP and show requested scope, supporting rows, archive link and only genuine unresolved mappings. Preparation is not import completion |
| Approval | Use the core.data-loader preview and Task Hook for the exact archive/environment. Ask once after preparation unless the same identified load explicitly includes auto-approval. This skill-authoring request is not permanent upload approval. After valid approval, verify and upload the same bytes without another confirmation or returning only a preparation result |
| Accepted initiation | The Data Loader initiation result; do not claim the group or child setup was created yet |
| Requested status | Returned data-set status, loaded/failed counts and applicable FSM process-log diagnostics; no successful-creation claim without completed results |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BG.EXECUTION_GATE | decision | 11 | execution_gate | fsm_preparation_ready->BG.DONE_FSM_PREPARATION;blocked->BG.HANDLE_ERROR | BG.ENFORCE_DESIGN | stop | The final FSM archive has passed task validation and is ready for the Data Loader preview lifecycle |
| BG.HANDLE_ERROR | step | 12 | error_handler | disclosed->RETURN_ISSUES | none | continue | A prior node reports a missing contract, invalid artifact, inconsistent task context, failed reference lookup, or failed preparation |
| BG.DONE_FSM_PREPARATION | terminal | 13 | terminal | none | BG.EXECUTION_GATE | continue | Return evaluated rule results to Task Hook; submission still requires its normal preview, approval and archive verification |
| RETURN_ISSUES | terminal | 14 | terminal | none | none | continue | Return classified blockers without any Fusion mutation |

## Sources

- Developer request: use FSM setup import with no Data Loader business-object selection, 2026-10-08.
- Developer-supplied FSM configuration-package ZIP, inspected 2026-10-08. Only component and field names are retained here; exported setup values are not repository fixtures.
- The enclosing task SKILL.md owns the FSM CSV import contract and core.data-loader handoff.
- Oracle's configuration-package import procedure and HAR evidence are cited in ora_reference_lookups.md.
- Developer-supplied attribute validation endpoints and active-environment host confirmation, 2026-10-09; no live mutation is authorized by the lookup contracts.
- Developer-confirmed successful minimal parent import and request to standardize its defaults, 2026-10-09; this removes only the former unsupported-mapping blocker for that known case.
- Developer restriction category/dimension lookup request, 2026-10-09; shared lookup mechanics and HAR evidence are owned by ora_reference_lookups.md.
- Default-inclusion FSM ProcessLog diagnosis and requested correction, 2026-10-09; retain partial success and stop before retrying an unresolved CSV key.
- Repeated category-resolution failures with populated dates and developer-supplied BalanceAttributeDefaultVORow mapping, 2026-10-09; compare the actual reference profile without attributing the error to an unproven single field.
- Developer-supplied service-V3 VO, helper Java and BalanceCategoryIdKHDPVO XML, 2026-10-09; the foreign-key calculation is source-confirmed.
- Developer confirmation, 2026-10-09, that FSM uses this helper: removes the missing-applicability blocker, while preserving unresolved field mappings and runtime outcome checks.
- Subsequent developer confirmation, 2026-10-09, that the corrected default-inclusion import worked: supersedes the earlier no-success state for that prepared profile.
- Developer-supplied BalanceAttributeDefinitionVO, repeated category key-helper VO and Java, 2026-10-09: attribute, category and dimension helpers have distinct responsibilities.
- Developer restriction resolver extension, 2026-10-09: reuse confirmed reference resolution without treating it as proof of an unverified restriction import layout.

- Developer-requested automatic combined child preparation, 2026-10-09, backed by the approved FSM CSV archive and retrieved successful component ProcessLog: one BalanceAttributeDefinition, one BalanceAttribute and one BalanceAttributeDefault processed with zero failures/warnings; the archive also contained their BalanceGroupInclusion link. No customer identifiers are retained here.
