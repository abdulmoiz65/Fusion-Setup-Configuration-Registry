# Error Handling

## Source

- Oracle Fusion Cloud SCM, [Create a Cost Organization](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-organization.html)


## Error Situations

| Situation | What Should Happen |
|---|---|
| No creation option is selected | Stop and request Create New or Use an existing organization. |
| Required attributes for the selected creation option are missing | Stop and request the missing attributes for that option. |
| Status is neither blank, `A`, `I`, `Active`, nor `Inactive` | Stop and request one of the supported values; do not create a Data Loader payload. |
| LegalEntityName does not name a previously defined legal entity | Stop; define or correct the legal entity before creating the cost organization. |
| CopyOrganizationName does not match the selected existing organization | Stop and correct the existing organization selection. |
| Existing-organization lookup returns zero, multiple, or truncated results | Stop; provide an exact CopyOrganizationName that resolves to one complete result. |
| User-supplied EffectiveStartDate differs from the resolved existing organization EffectiveStartDate | State both dates, state that the user-supplied date will not be used, and request approval to use the resolved date before continuing. |
| Data Loader source or Business Object validation fails | Stop before preview, correct the source data, and revalidate it through core.data-loader. |
| Upload or initiation is requested without an immutable Data Loader approval preview and a later standalone approve | Stop before the first POST. |
| Data Loader REST submission is requested | Route the operation through core.data-loader for upload and initiation; do not construct a direct REST request. |
| Existing Cost Organization update includes a field other than CostOrganizationName or Status | Stop before building an archive or preview; remove every nonpermitted update field. |
| Existing Cost Organization update has no CostOrganizationName or Status | Stop and request at least one permitted update field. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Creation option or its required attributes are missing or inconsistent; or Status cannot be normalized to `A` or `I` | Correct the supplied creation data. |
| Dependency readiness | The legal entity is not defined before cost organization creation | Define the legal entity, then revalidate. |
| Reference lookup | The existing organization cannot be resolved exactly or its required fields are unavailable | Correct CopyOrganizationName or resolve the Fusion lookup issue, then revalidate. |
| Approval blocker | A user-supplied EffectiveStartDate differs from the resolved existing organization date and approval was not granted | Obtain explicit approval to use the resolved EffectiveStartDate, or stop the setup. |
| Data Loader validation | The source or costOrganizations Business Object does not pass Data Loader validation | Correct the source data and generate a new immutable approval preview. |
| Approval blocker | Upload or initiation is requested without a current immutable approval preview and later standalone approve | Stop before upload; obtain a new preview and then send approve in a separate message. |
| Input validation | An existing Cost Organization update includes a field other than CostOrganizationName or Status, or neither permitted field is supplied | Correct the requested update so it contains CostOrganizationCode plus one or both permitted fields only. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or dependency failure | The selected creation option, affected field, and corrective action. |
| Data Loader validation failure | The affected source data, validation result, and corrective action. |
| Data Loader approval gate | The immutable preview and the required standalone approve action. |
| Existing organization effective-date override | The supplied EffectiveStartDate, the resolved EffectiveStartDate, the statement that the supplied date will not be used, and the required approval action. |
| Existing Cost Organization update policy | The exact CostOrganizationCode, the requested CostOrganizationName and/or Status, and confirmation that no other field is being updated. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or invalid input | Do not infer a creation option, legal entity, organization name, or classification code. Apply only the documented Status default and normalization rule; reject every other Status value. |
| Data Loader validation or approval gate is incomplete | Do not upload, initiate, retry, or construct a direct REST request. |
| Existing organization effective-date override is not approved | Do not continue to dependency readiness, create a Data Loader archive, or submit setup data. |
| Existing Cost Organization update violates the permitted-field policy | Do not build a Data Loader archive, preview, upload, initiate, retry, or construct a direct REST request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.CONFIRM_EFFECTIVE_START_DATE_OVERRIDE | decision | 4 | execution_gate | not_applicable->CCO.DEPENDENCIES;approved->CCO.DEPENDENCIES;declined->CCO.HANDLE_ISSUE | CCO.RESOLVE_EXISTING_ORGANIZATION | stop | CopyExistingOrgFlag is true; require approval only when a user-supplied EffectiveStartDate differs from the resolved date |
| CCO.DONE_DEFAULTED | terminal | 8 | terminal | none | CCO.DEFAULT_EFFECTIVE_DATE | stop | Effective Start Date defaulted |
| CCO.DONE_SUPPLIED | terminal | 9 | terminal | none | CCO.DEFAULT_EFFECTIVE_DATE | stop | Effective Start Date supplied |
| CCO.UPDATE_APPROVAL_GATE | decision | 14 | execution_gate | ready->CCO.DONE_UPDATE;blocked->CCO.HANDLE_ISSUE | CCO.UPDATE_ALLOWED_FIELDS | stop | Existing Cost Organization update has only permitted fields and an immutable core.data-loader approval preview |
| CCO.DONE_UPDATE | terminal | 15 | terminal | none | CCO.UPDATE_APPROVAL_GATE | stop | Existing Cost Organization update is validated and ready for the separate core.data-loader approval |
| CCO.HANDLE_ISSUE | step | 16 | error_handler | disclosed->RETURN_ISSUES | none | stop | Prior node reports invalid, blocked, or failed |
| RETURN_ISSUES | terminal | 17 | terminal | none | none | stop | Error disclosure complete |
