# Reference Lookups

Use the registered `collaborationParameters` business object only to read
existing settings. The remaining routes are read-only LOV resources and are
not Data Loader business objects.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_collaboration_parameter_by_code | A setting update is prepared | Code | /fscmRestApi/resources/11.13.18.05/collaborationParameters/{Code} | Code, Description, Value, DataType, LastUpdatedBy, LastUpdateDate | Code exactly matches the immutable parameter key | Existing parameter metadata and current Value | No match: stop because the setting cannot be created through this task. Many matches: stop because Code must be unique. |
| resolve_external_catalog_by_name | Code is ORA_VCS_DEFAULT_CATALOG_EXTERNAL | Value as CategorySetName | /fscmRestApi/resources/11.13.18.05/collaborationItemCategorySetsLOV?onlyData=true | CategorySetName, CategorySetId, CategorySetDescription | CategorySetName exactly matches Value | Validated CategorySetName for the Data Loader Value; the service resolves its stored identifier internally | No match or many matches: stop and require one exact catalog name. |
| resolve_user_account_by_username | Code is VMI_DEFAULT_REQUISITION_REQUESTER | Value as Username | /hcmRestApi/resources/11.13.18.05/userAccountsLOV?onlyData=true&finder=findByWord;StartsWithFlag=true,Category=2,FilterAttributes=UserName | Username, UserId | Username exactly matches Value after the UI finder returns candidates | Validated Username for the Data Loader Value; the service resolves its stored person identifier internally | No match or many exact matches: stop and require one exact username. |
| resolve_vcs_lookup_code | A lookup-governed setting is validated | LookupType and Value | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?onlyData=true&finder=LookupTypeFinder;ApplicationCode=FND,LookupType={LookupType} | LookupCode, Meaning | LookupCode exactly matches each submitted Value token | Validated LookupCode for the Data Loader Value; Meaning is display-only | No match: reject the value. Many matches: stop on ambiguous lookup data. |

The generic lookup resolver is used with these UI lookup types: ORA_VCS_YES_NO,
ORA_VCS_COLLAB_ORDER_TYPES, ORA_VCS_COLLAB_MEASURES_TYPES,
ORA_VCS_COLLAB_BOUNDARY_TYPE, ORA_VCS_CP_DL_LAYOUT, ORA_VCS_CP_DL_HORIZON,
ORA_VCS_PLAN_EDIT_OPTIONS, ORA_VCS_CP_DL_AGGR_LEVEL, ORA_VCS_NUM_FORMAT, and
ORA_VCS_FILE_DELIMITER. The UI excludes ORA_VCS_INPUT_VAL from
ORA_VCS_PLAN_EDIT_OPTIONS and ORA_VCS_CP_AGGR_PERIOD from
ORA_VCS_CP_DL_AGGR_LEVEL; those exclusions are design constraints, not
additional Data Loader business objects.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A route is a LOV resource | Use it read-only for validation or value conversion; never send it to Data Loader. |
| A catalog or requester name resolves to an identifier | Keep the validated name in the Data Loader Value. The service performs the identifier conversion; never replace the submitted name with the resolved identifier. |
| A generic lookup or Yes/No setting is updated | Keep each validated LookupCode unchanged in the Data Loader Value. Do not submit Meaning or a lookup identifier. |
| A setting code is not lookup-governed | Let the documented server validator evaluate it; do not invent an LOV endpoint. |
| A requested lookup is unavailable | Stop before a setting update and report the resolver, resource, and sanitized match result. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.REFERENCE_PARAMETERS | step | 10 | reference_lookup | found->CCS.VALIDATE_INPUT;missing->CCS.HANDLE_ERROR | none | stop | A setting update is prepared. |
