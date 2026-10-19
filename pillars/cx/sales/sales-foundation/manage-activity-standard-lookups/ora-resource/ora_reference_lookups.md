# Activity Standard Lookup Reference Lookups

Use read-only Standard Lookups REST calls to resolve the exact parent type,
current lookup-code state, and order-sensitive sibling values. These resolvers
never create, update, deactivate, or delete a Fusion record.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup type and child lookup-code endpoint inventory |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-get.html | Lookup-code finder, fields, lengths, defaults, and list behavior |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Configuration levels and predefined-data identification |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | APPOINTMENT, TASK, and CALLREPORT Activity functions and tag requirement |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html | Function-specific Activity Type finder and verification fields |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| derive_activity_type_function_tag | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | ActivityFunctionCodes from the reviewed request; documented canonical function order APPOINTMENT, TASK, CALLREPORT | Require one or more unique values from APPOINTMENT, TASK, and CALLREPORT; retain the selected set, order it canonically, join with colons, and add leading and trailing colons | ActivityFunctionCodes; Tag; examples: APPOINTMENT becomes :APPOINTMENT: and all three become :APPOINTMENT:TASK:CALLREPORT: | A blank, duplicate, unsupported, or conflicting supplied Tag blocks preview; do not infer a function. |
| verify_activity_standard_lookup_csv_package | Operation is Import | SetupDataZipPath; LookupType; LookupCode; Meaning; EnabledFlag; StartDateActive; Tag | ZIP root contains ASM_SETUP_CSV_METADATA.xml, FND_APP_STANDARD_LOOKUP.csv, and ORA_FND_APP_STANDARD_LOOKUP_CODE.csv; metadata identifies ObjectShortName ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS, ObjectType TASK, ProcessType EXPORT, and ProcessStatus COMPLETED; scope includes ZMM_ACTIVITY_TYPE; parent CSV contains one unchanged ZMM_ACTIVITY_TYPE row; child headers match the package metadata; one reviewed new row has blank system audit fields and exact derived Tag | PackagePath; PackageTaskCode; PackageProcessStatus; ParentRow; ChildHeaders; CandidateRow; PackageSha256 | A loose CSV, wrong task, incomplete process, missing scope or parent, changed headers, nonblank new-row audit values, duplicate code, conflicting tag, or multiple candidate rows blocks preview and import. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_activity_standard_lookup_type | Always after input and task-scope validation | LookupType | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?fields=LookupType,Meaning,Description,CustomizationLevel,ModuleId,RestAccessSecured&links=self,canonical, with LookupType encoded as one path segment | LookupType, Meaning, Description, CustomizationLevel, ModuleId, RestAccessSecured and returned item links | The returned LookupType exactly equals the requested value | LookupType, LookupTypeMeaning: Meaning, LookupTypeDescription: Description, CustomizationLevel, ModuleId, RestAccessSecured, ParentItemLink | No match blocks because this task only maintains codes under an existing type. A mismatched or ambiguous item, 401, 403, or other REST failure stops the workflow. |
| find_activity_standard_lookup_code | LookupCode is supplied | LookupType, LookupCode | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes?finder=LookupCodeFinder;LookupCode={LookupCode}&fields=LookupCode,Meaning,Description,EnabledFlag,StartDateActive,EndDateActive,DisplaySequence,Tag,LastUpdatedBy&links=self,canonical, passing finder as one encoded query parameter | LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, LastUpdatedBy and returned item links | Return zero or one item whose LookupCode exactly equals the requested value | LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, LastUpdatedBy, CodeItemLink | No match permits Create only. It blocks Review, Update, Deactivate, Delete, and Translate. More than one exact match, 401, 403, or another REST failure stops the workflow. |
| list_activity_standard_lookup_codes | LookupType is ZMM_ACTIVITY_STATUS_CD or ORA_ZMM_ACTIVITY_FILTER_TYPE and DisplaySequence is created or changed | LookupType | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes?fields=LookupCode,Meaning,EnabledFlag,StartDateActive,EndDateActive,DisplaySequence&onlyData=true&limit=500 | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence | Use all returned siblings for the exact parent; determine the active lowest sequence and resulting order without selecting a value on the requester's behalf | CurrentLookupOrder, CurrentLowestSequence, CurrentDefaultCode, ProposedLookupOrder, ProposedDefaultCode | An incomplete, paginated beyond the requested limit, ambiguous, or failed list blocks an order-changing write. Do not infer impact from a partial result. |
| verify_activity_type_by_function | After an approved ZMM_ACTIVITY_TYPE create for each selected ActivityFunctionCode | LookupCode, ActivityFunctionCode, current date | GET /crmRestApi/resources/11.13.18.05/activityTypeLookupsLOV?finder=ByActivityFunctionFinder;Bind_ActivityFunctionCode={ActivityFunctionCode},Bind_CurrentDate={current_date}&fields=LookupCode,LookupType,Meaning,EnabledFlag,LookupEnabledFlag,StartDateActive,EndDateActive,Tag&onlyData=true | LookupCode, LookupType, Meaning, EnabledFlag, LookupEnabledFlag, StartDateActive, EndDateActive, Tag | Exactly one returned item has LookupType ZMM_ACTIVITY_TYPE, the requested LookupCode, enabled state, effective dates, and canonical Tag for that selected function | VerifiedActivityFunctionCodes; VerifiedLookupCode; VerifiedMeaning; VerifiedEnabledFlag; VerifiedStartDateActive; VerifiedTag | No exact item, an item returned for only some requested functions, an ambiguous result, or a REST failure makes verification fail; do not claim the Activity Type is complete. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact parent and exact code are returned | Use the canonical links and returned current state for editability, impact, preview, and verification. |
| Exact parent exists and exact code is not found for Create | Continue as a create candidate; do not use upsert. |
| ZMM_ACTIVITY_TYPE Create has a valid function list | Derive the canonical Tag from exactly those functions and carry it unchanged into the REST body or verified CSV row. |
| Exact code already exists for Create | Block the POST and show the current row; do not reinterpret the request as Update. |
| Exact code is absent for a non-Create operation | Block the operation and request a corrected identity or an explicit Create request. |
| A code CRUD request has no export package | Continue with exact Apps Common preflight; export membership is not a prerequisite for lookup-code POST, PATCH, or safe DELETE. |
| LastUpdatedBy is SEED_DATA_FROM_APPLICATION | Treat the row as predefined data when applying Extensible-level restrictions. This is positive evidence only; a different updater does not prove that a previously modified row was never predefined. |
| Parent or code resolver returns 401 or 403 | Classify as authorization or privilege failure and stop; do not try another lookup category. |
| Any read fails or is ambiguous | Stop and disclose the safe method, endpoint identity, status, and request ID or ECID when available; do not proceed to a write. |
| A write has an uncertain transport outcome | Run the exact code GET once to reconcile state before any retry decision; never replay the mutation automatically. |
| ZMM_ACTIVITY_TYPE exists after create but is missing from a selected function LOV | Report incomplete function visibility and stop; do not issue an automatic compensating write or claim success. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.LOOKUP_TYPE | step | 3 | reference_lookup | matched->ACTIVITY_STD.LOOKUP_CODE;not_found->ACTIVITY_STD.BLOCKED;ambiguous->ACTIVITY_STD.FAILED;failure->ACTIVITY_STD.FAILED | ACTIVITY_STD.DEPENDENCIES | stop | Always |
| ACTIVITY_STD.LOOKUP_CODE | step | 4 | reference_lookup | found->ACTIVITY_STD.LOOKUP_ORDER;not_found->ACTIVITY_STD.LOOKUP_ORDER;failure->ACTIVITY_STD.FAILED | ACTIVITY_STD.LOOKUP_TYPE | stop | LookupCode is supplied; otherwise record not_requested and continue |
| ACTIVITY_STD.LOOKUP_ORDER | step | 5 | reference_lookup | resolved->ACTIVITY_STD.DEFAULTS;not_requested->ACTIVITY_STD.DEFAULTS;failure->ACTIVITY_STD.FAILED | ACTIVITY_STD.LOOKUP_CODE | stop | DisplaySequence is created or changed for ZMM_ACTIVITY_STATUS_CD or ORA_ZMM_ACTIVITY_FILTER_TYPE; otherwise record not_requested |
