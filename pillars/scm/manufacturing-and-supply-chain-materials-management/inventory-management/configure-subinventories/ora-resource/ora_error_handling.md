# Configure Subinventories Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Standard lookup returns no exact display-value match | Stop before Data Loader handoff and request a valid display value for the affected field and lookup type. |
| Standard lookup returns more than one exact display-value match | Stop before Data Loader handoff and request an unambiguous display value; never select the first result. |
| Standard lookup returns an excluded code | Stop before Data Loader handoff and explain that the value is unavailable in the current UI flow. |
| Checkbox or friendly value is unsupported or conflicting | Stop before Data Loader handoff and request one documented friendly value for the affected normalized attribute. |
| Standard lookup request returns authentication or authorization failure | Stop and report auth/authz failure; refresh authentication only through the selected core authentication workflow. |
| Standard lookup request has a transport or Fusion API failure | Stop and record the failure class; do not infer a value, retry a mutation, or use stale lookup data. |
| Locator row is supplied to a REST, REST-BO, DAT, or XLSX business-object source | Stop before artifact preview or submission. Remove locator rows from the REST source and prepare a separate immutable task-scoped FSM ZIP that retains the parent subinventory identity. |
| Locator FSM package is derived from a current-data export | Stop before package preparation, preview, or submission. Do not strip rows from that export and reuse it as a template; select a verified project-local template-only artifact or obtain a replacement with `--template-only`. |
| Project-local locator template cannot be verified | Stop before package preparation. Report the failed task, environment, release compatibility, fingerprint, manifest, member/header, or empty-row check and obtain a replacement empty template with `--template-only`. |
| Valid project-local empty template already exists | Reuse it. Do not create another Fusion template-export process unless the user explicitly requests refresh. |
| Locator Structure value matches no enabled locator structure row | Stop before REST source or FSM package preparation and request a valid enabled Locator Structure name or Structure Instance Code. |
| Locator Structure value matches multiple distinct enabled rows across code or name | Stop as ambiguous. Report the supplied value and matching codes/names without selecting the first row. |
| Separately supplied Locator Structure name and code resolve to different enabled rows | Stop as conflicting input and request one consistent value or pair before REST source or FSM package preparation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| lookup_no_match | A supplied display value has no eligible exact Meaning match | Request a valid display value. |
| lookup_ambiguous | A supplied display value has more than one eligible exact Meaning match | Request a more precise display value or an approved system value. |
| lookup_excluded | The exact match is a source-excluded LookupCode | Request a value allowed by the documented UI flow. |
| normalization_invalid | A supplied checkbox or friendly value cannot be normalized to its documented canonical value | Request one documented friendly value; do not infer or coerce a value. |
| auth_authz | The read-only lookup is unauthorized | Restore the approved authentication context and rerun the read-only lookup. |
| transport_environment | The read-only lookup cannot reach Fusion | Resolve the environment or transport problem before rerunning the lookup. |
| fusion_api | Fusion returns a non-authentication API failure | Preserve sanitized failure evidence and correct the reported Fusion-side issue. |
| import_route_mismatch | A locator child row is assigned to a REST or registered-business-object source | Repackage the locator row in the FSM ZIP; do not substitute locatorItems or another REST business object. |
| fsm_template_source_mismatch | A locator FSM package uses a current-data export or lacks template-only provenance | Discard the candidate package and use a verified project-local empty template-only export. |
| fsm_template_validation | A cached empty template fails identity, compatibility, integrity, manifest, member/header, or empty-row validation | Export a replacement with `shared.setup-export.task-level-export --template-only`, then restart package preparation and approval. |
| locator_structure_not_found | A Locator Structure value for a supported route matches neither `StructureInstanceCode` nor `StructureInstanceName` on an enabled row | Request a valid enabled structure name or code and rerun the read-only resolver. |
| locator_structure_ambiguous | A Locator Structure value for a supported route matches more than one distinct enabled row across code or name | Request an unambiguous value; do not select the first row or continue to REST source or FSM package preparation. |
| locator_structure_conflict | Separately supplied locator-structure name and code values resolve to different enabled rows | Request one consistent value or pair and rerun the read-only resolver. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSUBINV.DATA_LOADER_HANDOFF | decision | 180 | execution_gate | ready->CSUBINV.DONE;blocked->CSUBINV.HANDLE_LOOKUP_ERROR;failure->CSUBINV.HANDLE_LOOKUP_ERROR | CSUBINV.CHECK_DEPENDENCIES | stop | Before handing the selected REST source or FSM ZIP to core.data-loader. Locators may proceed only through the FSM route. |
| CSUBINV.HANDLE_LOOKUP_ERROR | step | 900 | error_handler | issues->RETURN_ISSUES | none | stop | A Configure Subinventories normalization, standard-lookup, route, or FSM template-validation node returns blocked or failure. |
| RETURN_ISSUES | terminal | 910 | terminal | none | none | continue | A normalization, route, lookup, or FSM template-provenance issue prevents import handoff. |
| CSUBINV.DONE | terminal | 190 | terminal | none | CSUBINV.DATA_LOADER_HANDOFF | continue | Local task rules passed and core.data-loader owns final validation and execution for the selected REST or FSM route. |
