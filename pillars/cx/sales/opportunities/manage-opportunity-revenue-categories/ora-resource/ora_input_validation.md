# Manage Opportunity Revenue Categories Input Validation

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use these task-scoped rules for Manage Opportunity Revenue Categories under the
Opportunities functional area. The source basis is the Common Features
[Standard Lookup Code](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-standard-lookups-lookup-codes.html)
contract, the repository standard-lookup contract, and a fresh same-target task
export. This task manages codes only under standard lookup
`MOO_REVN_CATEGORY`; it does not manage set-enabled revenue types or reference
data set assignments.

Set `RequestMode` explicitly. Use `SingleLookup` for Read or one-code Create,
Update, or Disable. Use `Package` for full-task Export or Import. Direct REST
mutation is not a supported mode or route.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Request envelope | Operation and RequestMode | Block lookup, export, package review, or handoff | Select one supported operation and compatible SingleLookup or Package mode | Every opportunity revenue-category request |  |
| Target environment | EnvironmentUrl, EnvironmentIdentity, FusionRelease, and ProjectId | Block live reads, export, or handoff | Select and verify one target Fusion environment and durable project workspace | Every request |  |
| SingleLookup identity | LookupCode | Block lookup or package preparation | Provide the exact MOO_REVN_CATEGORY code | SingleLookup Read, Create, Update, or Disable | find_revenue_category_lookup_code |
| SingleLookup Create definition | Meaning; optional Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag | Block package preparation | Provide a display meaning for the new code; EnabledFlag defaults to Y only when omitted | SingleLookup Create |  |
| SingleLookup Update definition | At least one of Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag | Block package preparation | Provide at least one documented mutable standard-lookup field | SingleLookup Update |  |
| SingleLookup mutation state and impact | Exact current state or confirmed absence, live-read timestamp, owner, purpose, affected revenue field, historical-use assessment, downstream consumers, and intended minimal delta | Block package preparation | Complete the fresh read-before-write and business-impact review | SingleLookup Create, Update, or Disable | find_revenue_category_lookup_code |
| Export request | Exact target and release with TaskCode fixed to MOO_MANAGE_REVENUE_CATEGORIES | Block export | Run the complete automatic task export without a LookupCode selector | Package Export |  |
| FSM baseline, parent-child closure, final package, exact task identity, and persisted Data Loader task context | Fresh completed exact-target/release baseline; separate final PackagePath and PackageSha256; TaskCode MOO_MANAGE_REVENUE_CATEGORIES; TaskName Manage Opportunity Revenue Categories; one exact ASM task identity; metadata-derived members and headers; exactly one MOO_REVN_CATEGORY parent row when changed child rows exist; require persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area | Block Data Loader handoff | Export the exact task, preserve its contract, add the current parent carrier row, build and reopen the reviewed ZIP, validate SHA-256, and resolve persisted Data Loader task context before handoff | SingleLookup Create, Update, or Disable; Package Import | verify_revenue_category_fsm_package |
| FSM changed rows | For every changed row: RowOperation, LookupType MOO_REVN_CATEGORY, LookupCode, proposed fields, fresh current-state lock, impact evidence, and preservation evidence | Block package review or Data Loader handoff | Resolve and validate every changed row; SingleLookup requires exactly one matching row and Package Import validates all rows atomically | SingleLookup Create, Update, or Disable; Package Import | verify_revenue_category_fsm_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| Operation is outside Create, Update, Disable, Read, Export, or Import | Reject before lookup or package validation | Every revenue-category setup request |  |
| RequestMode is SingleLookup for Export or Import, or Package for Read, Create, Update, or Disable | Reject the incompatible mode; do not apply one-code rules to full-task Export or multi-row Import | Every request |  |
| ExecutionRoute requests direct REST, shared setup import, browser execution, or another write route | Reject the route; supported writes use only the exact FSM package through core.data-loader | Every mutation or Import |  |
| LookupCode is blank, or Meaning is blank on a Create row | Reject before lookup or package readiness | SingleLookup code work or any changed package row |  |
| A supplied or packaged LookupType is not MOO_REVN_CATEGORY, or SetId, SetCode, BUOrgId, or OrganizationCode is supplied | Reject the incompatible scope; this task is fixed to one standard lookup and accepts no reference-set context | Every SingleLookup request and every changed package row |  |
| LookupCode exceeds 30 characters, Meaning exceeds 80 characters, Description exceeds 240 characters, Tag exceeds 150 characters, or EnabledFlag is not Y or N | Reject the invalid field and show the documented constraint | A SingleLookup request or changed package row supplies the field |  |
| StartDateActive or EndDateActive is not an ISO 8601 date, or DisplaySequence is not an integer | Reject the invalid field before lookup or package readiness | A SingleLookup request or changed package row supplies the field |  |
| EndDateActive precedes StartDateActive | Reject the date range before lookup or preview | Both active dates are supplied |  |
| Update attempts to rename LookupCode | Reject the immutable-identity change | SingleLookup Update or a package Update row |  |
| Disable supplies a mutable field other than EnabledFlag=N, Read supplies any mutable field, or any row encodes Delete | Reject the unsupported delta; Disable changes only EnabledFlag and Delete is unsupported | SingleLookup Disable or Read; every changed package row |  |
| Package Export supplies LookupCode, row delta, current-state lock, impact, final package, or narrowed row scope | Reject the invented scope; export the complete exact task baseline | Package Export |  |
| The baseline is missing, stale, incomplete, failed, cross-target, cross-release, or for another task | Reject package readiness and obtain a fresh completed exact-task export | SingleLookup Create, Update, or Disable; Package Import | verify_revenue_category_fsm_package |
| ORA_FND_APP_STANDARD_LOOKUP_CODE.csv has a changed row but FND_APP_STANDARD_LOOKUP.csv is header-only, has no exact MOO_REVN_CATEGORY row, has duplicate parent rows, or has a parent row whose LookupType or current business metadata differs from verify_revenue_category_lookup_type | Reject before preview because Fusion skips orphan child rows; rebuild the package with exactly one current, unchanged MOO_REVN_CATEGORY parent carrier row and blank system-audit fields | SingleLookup Create, Update, or Disable; Package Import with changed child rows | verify_revenue_category_fsm_package |
| A child row's FND_APP_STANDARD_LOOKUP.LookupType does not exactly equal the sole parent row's LookupType | Reject the parent-child mismatch before preview; do not rely on successful Data Loader counters | SingleLookup Create, Update, or Disable; every changed Package Import row | verify_revenue_category_fsm_package |
| ASM task identity, metadata-derived members, exact headers/order, parent-child closure, preservation, reviewed row delta, fresh state lock, impact, exact task name/code, persisted Data Loader task context, reopened final PackageSha256, or immutable path binding is missing or inconsistent | Reject the complete package; do not synthesize task context for FSM mutation handoff, repair, partially submit, or request child-owned approval | SingleLookup Create, Update, or Disable; Package Import | verify_revenue_category_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.VALIDATE | step | 1 | validate_input | valid->OPP.REVENUE_CATEGORY.DEFAULT;missing->OPP.REVENUE_CATEGORY.RETURN_MISSING;invalid->OPP.REVENUE_CATEGORY.RETURN_FAILED | none | stop | Every opportunity revenue-category request |
