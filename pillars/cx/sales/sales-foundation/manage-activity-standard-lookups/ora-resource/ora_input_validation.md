# Activity Standard Lookup Input Validation

Validate the requested activity lookup-code operation before reading or changing
Fusion. This task maintains codes under an existing Activity standard lookup
type; it does not create a new lookup type.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Sales lookup configuration levels and the Manage Activity Standard Lookups task location |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Lookup-code shape, effective dates, enablement, translations, predefined data, deletion, and session refresh |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup and child lookup-code REST operations |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/considerations-when-setting-up-call-reports.html | Activity Objective and Activity Outcome lookup types and their no-tag rule |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/enable-default-task-status.html | ZMM_ACTIVITY_STATUS_CD display-sequence behavior |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/change-calendar-colors.html | ZMM_ACTIVITY_TYPE tag behavior |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | Activity Type function membership and documented function codes |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-activity-type-lookups.html | Function-specific Activity Type verification |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-configure-default-activity-search-in-accounts.html | ORA_ZMM_ACTIVITY_FILTER_TYPE values and display-sequence behavior |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Operation: Review, Create, Update, Deactivate, Delete, Translate, Export, Import, or Validate | Block the workflow | State the intended operation | Always |  |
| Parent lookup type | LookupType | Block lookup-code resolution and every mutation route | Provide the exact existing Activity standard lookup type | Always | resolve_activity_standard_lookup_type |
| Lookup-code identity | LookupCode | Block the workflow | Provide the exact code; do not infer it from the meaning | Review, Create, Update, Deactivate, Delete, Translate, or Validate | find_activity_standard_lookup_code |
| New lookup-code definition | LookupCode and Meaning; optional Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and Tag | Block preview | Provide the missing stable code or user-facing meaning | Operation is Create |  |
| New Activity Type definition | ActivityFunctionCodes, EnabledFlag, and StartDateActive in addition to LookupCode and Meaning | Block preview | Provide one or more exact functions from APPOINTMENT, TASK, and CALLREPORT, plus enablement and effective start | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | derive_activity_type_function_tag |
| Update fields | At least one of Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, or Tag | Block preview | State the exact field and new value | Operation is Update |  |
| Deactivation method | EnabledFlag=N, EndDateActive, or both | Block preview | State whether to disable, end-date, or do both | Operation is Deactivate |  |
| Translation | Language, TranslatedMeaning, and optional TranslatedDescription | Block translation guidance or package preparation | Provide one enabled language and translated meaning per translation | Operation is Translate |  |
| Execution context | TargetEnvironment and ExecutionIntent | Block a live write but allow a local plan | Identify the exact configured Fusion environment and whether execution or guidance is requested | Create, Update, Deactivate, or Delete |  |
| Mutation approval | Approval bound to the immutable method, endpoint, target, body or delete effect, environment, and current-state preview | Block the live-write handoff | Approve the exact preview after the read-before-write check | Create, Update, Deactivate, or Delete is requested for live execution |  |
| CSV package | Current template or completed task export ZIP for ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS | Block import handoff | Obtain the current package for this exact setup task and preserve its template-derived files and headers | Operation is Import |  |
| CSV package approval | Approval bound to the immutable ZIP SHA-256, task code, environment, row delta, and verification plan | Block import handoff | Approve the exact validated package preview | Operation is Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Existing parent only | Reject a request to create or rename LookupType; route new standard lookup-type design to the appropriate lookup task | LookupType creation or rename is requested |  |
| Activity Type creation contract | Permit Create only when the existing parent is ZMM_ACTIVITY_TYPE, the exact code is absent, the requested functions are valid, and Tag exactly equals the canonical function-derived tag | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | derive_activity_type_function_tag |
| Activity function shape | Reject a blank list, duplicates, or a value outside APPOINTMENT, TASK, and CALLREPORT; preserve the selected set while canonicalizing only its order | ActivityFunctionCodes is supplied | derive_activity_type_function_tag |
| Lookup-code shape | Reject a blank code, a code longer than 30 characters, or a code containing spaces; recommend underscores without silently rewriting the supplied value | LookupCode is supplied |  |
| Meaning shape | Reject a blank Meaning or TranslatedMeaning and a value longer than 80 characters | Create, Update of Meaning, or Translate |  |
| Description length | Reject Description or TranslatedDescription longer than 240 characters | A description is supplied |  |
| Enabled flag | Accept only Y or N after displaying any normalized boolean representation to the user | EnabledFlag is supplied |  |
| Date shape and order | Require ISO `YYYY-MM-DD`; reject EndDateActive earlier than StartDateActive | Either active date is supplied |  |
| Display sequence | Require an integer; do not infer a sequence | DisplaySequence is supplied |  |
| Tag length and scope | Reject a Tag longer than 150 characters; reject any Tag for an Activity lookup type other than ZMM_ACTIVITY_TYPE | Tag is supplied |  |
| Activity Type function tag | Derive a leading-and-trailing-colon Tag in APPOINTMENT, TASK, CALLREPORT order; reject a user-supplied Tag that differs from the derived value | Operation is Create and LookupType is ZMM_ACTIVITY_TYPE | derive_activity_type_function_tag |
| Calendar color tag | Require an explicit valid HTML color code and current-environment evidence that the change won't overwrite an Activity-function Tag; otherwise route the color change to guided UI | Operation is Update, LookupType is ZMM_ACTIVITY_TYPE, and the requested Tag purpose is calendar color |  |
| Known public task scope | Accept ORA_ZMM_ACTIVITY_OBJECTIVE, ZMM_ACTIVITY_OUTCOME, ZMM_ACTIVITY_STATUS_CD, ZMM_ACTIVITY_TYPE, or ORA_ZMM_ACTIVITY_FILTER_TYPE as publicly documented task-scope evidence; for any other type require current evidence that it appears in Manage Activity Standard Lookups | Always | resolve_activity_standard_lookup_type |
| Create identity | Require the exact code to be absent before POST; never convert a duplicate create into an update | Operation is Create | find_activity_standard_lookup_code |
| Fixed Activity-search list | Reject Create, Delete, or an EndDateActive change for ORA_ZMM_ACTIVITY_FILTER_TYPE | LookupType is ORA_ZMM_ACTIVITY_FILTER_TYPE |  |
| Existing identity | Require exactly one existing code before Update, Deactivate, Delete, Translate, or Review | Operation is Update, Deactivate, Delete, Translate, or Review | find_activity_standard_lookup_code |
| Lookup-code immutability | Reject an attempt to change LookupCode with PATCH; treat replacement as a separately reviewed create plus optional deactivation or deletion | Operation is Update |  |
| CSV schema | Require a current completed ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS export or template ZIP, exact metadata and filenames, unchanged template headers, an existing unchanged ZMM_ACTIVITY_TYPE parent row, blank system audit values on a new row, and the canonical function-derived Tag | Operation is Import | verify_activity_standard_lookup_csv_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.VALIDATE | step | 1 | validate_input | valid->ACTIVITY_STD.DEPENDENCIES;missing_or_invalid->ACTIVITY_STD.BLOCKED | none | stop | Always |
