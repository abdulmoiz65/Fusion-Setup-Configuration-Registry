# Configure Legislations for Human Resources Design

Search retains its read-only contract. The developer-tested Delete action is
prepared by the task workflow and submitted only by core.data-loader.
Verify Delete is a separately requested read-only continuation. Create currently
prepares Legislation Rules inputs; its Business Object integration is explicitly
deferred. Update/Edit remains unsupported. A rule terminal never submits a load.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select the operation | Keep Search, Create, Delete, and Verify Delete on their own declared graph branches |
| 2 | Protect the target | Delete requires a unique exact Fusion record; Verify Delete uses the original code and successful-load context |
| 3 | Preserve the selected route | All lookups use the governed REST client; all deletion uploads and initiation use Data Loader |
| 4 | Prepare the validated DAT | After DELETE_READY for phase=prepare, the owning workflow constructs the DAT from the input contract and fixed defaults, persists it in the active project, and follows execution_intent |
| 5 | Hand off an explicit load | core.data-loader validates live metadata and creates the immutable ZIP/preflight, then invokes Task Hook data-load with phase=validate_artifact before its single approval lifecycle and submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An operation is requested | Error | | The operation is not Search, Create, Delete, or Verify Delete | Return UNSUPPORTED; author the separate operation before executing it | No |
| A task-owned HCM REST resource call is selected | Error | | The call uses a path outside the standard resource route declared in ora_reference_lookups.md or treats a browser-captured path as a fallback | Use the fixed skill-owned lookup endpoint with the configured restBaseUrl; do not require a user-supplied resource path or version | No |
| Search is selected | Error | | A POST, PATCH, PUT, DELETE, ADF_REST Business Object mutation, FSM export/import, or loader submission is proposed | Execute only the lookup contract in ora_reference_lookups.md | No |
| Search is selected | Error | | A write preview, immutable ZIP, Task Hook import approval, or standalone approve message is demanded as a prerequisite | Remove the inapplicable mutation prerequisite; authentication and task readiness still apply | Yes |
| Search returns no matches | Error | | The caller would create or configure a legislation automatically | Return the Search outcome only; absence is not mutation authorization | No |
| Search returns multiple matches | Error | | The caller would choose one record for a later mutation without a separate selection and workflow | Present the candidates; no write follows from Search | No |
| Delete lookup is starting | Error | | The proposed call is a write, an unfiltered target discovery, a guessed endpoint, or a substitute browser/FSM route | Perform only the declared read-only target resolver | No |
| Delete target has been resolved | Error | resolve_installed_legislation_for_delete | No unique exact target exists, name and code conflict, pagination is incomplete, or target evidence belongs to another environment | Resolve or clarify the target before preparing any deletion; never choose the first partial match | No |
| Delete values are prepared | Error | | RestAction is treated as the business operation; a generic sample is invoked with --operation delete; or a direct HTTP POST/DELETE is proposed | Construct the DAT from the ordered contract in ora_input_validation.md and the fixed values in ora_defaulting_rules.md after DELETE_READY; preserve MERGE/POST custom-action semantics and route any explicit load through core.data-loader | No |
| Delete with execution_intent=prepare_only | Error | | The workflow would upload the DAT or initiate a load after preparing the requested file | Persist only the validated DAT and return its link with the selected legislation; preparation has no Fusion write side effect | No |
| Delete with execution_intent=load and phase=prepare completed | Error | | The workflow bypasses core.data-loader, selects another task/object, or treats catalog CSV support as an FSM route or permission for Create/Update | Delegate the prepared source to core.data-loader with PAY_CONFIGURE_LEGISLATIONS_FOR_HUMAN_RESOURCES, dataloader_import_mode=REST, and businessObject=deleteInstalledLegislation; Data Loader owns metadata validation, ZIP preparation, upload, initiation, and diagnostics | No |
| Delete Task Hook data-load is invoked | Error | | Live metadata/source validation or final immutable ZIP/preflight is incomplete, or task data lacks phase=validate_artifact and the original selection context | Let Data Loader invoke Task Hook for the exact final bytes, evaluate this graph, and retain its preview only after all rules pass; never invoke Task Validator directly or forge an envelope | No |
| Delete is handed to Data Loader | Error | | Approval is sought before live schema and Task Hook validation; approval is reused for changed bytes/environment/target; or an extra task approval duplicates Data Loader's own gate | Complete Data Loader's exact-artifact lifecycle once; after approval verify its retained envelopes without rerunning this graph | No |
| Delete Data Loader approval or submission is reached | Error | | The workflow interprets the initial delete request as approval without Data Loader's required approval context, changes the approved artifact, reruns lookups, or rebuilds the DAT after approval | Follow only Data Loader's approval lifecycle, including its explicit same-request auto-approval rules when applicable; bind approval to environment, legislation, operation, and immutable ZIP, then reuse the verified retained bytes and envelopes | No |
| Delete with phase=validate_artifact | Error | | A rule would add defaults, rename a member, rewrite data, or regenerate the immutable ZIP | Return the validation issue to Data Loader for a fresh preparation cycle | No |
| Verify Delete is selected | Error | | A write is proposed, the load is still in progress/failed, or the original code/environment/access context is unavailable | Use the declared verification resolver only after the prerequisite status check | No |
| A later explicit status or deletion-verification request is received | Error | | Accepted initiation is treated as load success, status/errors are skipped, or absence is queried without the original selection | Invoke core.data-loader status handling first; select Verify Delete only after successful load with zero failures and retained original code/environment, then evaluate the declared absence lookup | No |
| A source suggests another execution route | Error | | Capture content or obsolete copied Payroll guidance would override the selected operation | Treat captures as evidence only and retain this developer-defined boundary | No |
| Create is selected | Error | | A rule-specific lookup or collection of dependent required inputs precedes successful available-legislation selection | Execute the Create eligibility resolver first; preserve provided inputs without prematurely requiring missing rule values | No |
| Create target is unavailable | Error | | Absence in the available list is claimed to prove an installed record or an invalid country | Use installed classification before explaining already exists versus unavailable; suggest Edit only as a separately requested operation | No |
| Shared selection changes | Error | | Rule values, currency or row mappings from a previous legislation/environment would be reused | Discard dependent resolved context and re-run eligibility and relevant lookups; preserve original user input separately | No |
| Create preparation completes | Error | | Some required business value is unresolved, an explicit option is invalid, row pairs disagree or readonly Process in Payroll is treated as writable | Return the exact missing/invalid input; prepare logical values only after their owning validation passes | No |
| Current Create delivery | Error | | A DAT/ZIP is generated or a Create submission/approval is offered without the future Business Object integration | Return CREATE_DATA_PREPARED with CREATE_BO_CONTRACT_PENDING; use Prepared Create Mapping Contract in ora_reference_lookups.md; no serialization or upload is authorized in this stage | No |
| Existing manifest import route | Error | | businessObject=deleteInstalledLegislation is selected for Create because the manifest contains that import line | That tested route applies only to Delete; keep Create on this preparation branch | No |
| Additional Create sections | Error | | Element Classifications, Payment Types, Component Groups or Balance Dimensions are auto-filled or submitted using the Legislation Rules contract | Retain shared legislation selection and report the requested section needs its own authored rules | No |
| Final prepared summary | Error | | Omitted defaults cause an extra approval prompt, or prepared values are represented as already created | Show selected legislation, tax date, currency, rule meanings and ordered mapping rows with Process in Payroll; label defaulted values and explicitly state pending BO integration | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_installed_legislation_for_delete | Delete design check after target resolution | Unique exact target, original name/code comparison, complete lookup evidence, and environment binding | ora_reference_lookups.md |

The scope gates run before their lookups and check only the selected operation
and client route. CLHR.ENFORCE_DELETE_DESIGN consumes the completed target
lookup; it does not run a second resolver or require a future approval.

## Deferred Create Integration

| Item | Current status | Boundary |
|---|---|---|
| Registered BO names and DAT metadata | Pending next authoring stage | No guessed discriminator, filename, key or METADATA header |
| Object and array serialization | Pending next authoring stage | No invented escaping, delimiters, array encoding or row flattening |
| Action ordering and atomicity | Pending next authoring stage | No inferred write sequence, rollback or retry behavior |
| Empty mappings at submission | Pending BO contract | Preserve explicit empty prepared arrays; do not invent minimum row count or assert Fusion accepts them |
| Executor and validation | Future integration through core.data-loader | Live metadata, final immutable ZIP, Task Hook and its sole approval remain prerequisites |
| Readiness meaning | Current graph covers selection, validation and logical preparation | planned/ready is not Create submission readiness or confirmed creation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.ENFORCE_SEARCH_SCOPE | step | 5 | design_enforcement | allowed->CLHR.SEARCH;unsupported->CLHR.ERROR | CLHR.SEARCH_DEFAULTS | stop | Search only; preserve its read-only scope without applying Delete prerequisites |
| CLHR.ENFORCE_DELETE_SCOPE | step | 10 | design_enforcement | allowed->CLHR.RESOLVE_DELETE_TARGET;unsupported->CLHR.ERROR | CLHR.SELECT_OPERATION | stop | Delete only; pre-lookup scope and route gate, not the post-lookup target check |
| CLHR.ENFORCE_DELETE_DESIGN | step | 14 | design_enforcement | allowed->CLHR.DELETE_READY;blocked->CLHR.ERROR | CLHR.VALIDATE_DELETE_CONTRACT | stop | Delete only; consume resolved target evidence and the validated draft or final archive; return readiness without granting upload approval |
| CLHR.ENFORCE_VERIFY_SCOPE | step | 20 | design_enforcement | allowed->CLHR.VERIFY_DELETED;unsupported->CLHR.ERROR | CLHR.SELECT_OPERATION | stop | Verify Delete only; read-only continuation after successful-load and original-target prerequisites |
| CLHR.ENFORCE_CREATE_SCOPE | step | 50 | design_enforcement | allowed->CLHR.RESOLVE_CREATE_LEGISLATION;unsupported->CLHR.ERROR | CLHR.SELECT_OPERATION | stop | Create selection and Legislation Rules preparation only; declared GETs, no Delete BO reuse or direct mutations |
| CLHR.ENFORCE_CREATE_DESIGN | step | 65 | design_enforcement | prepared->CLHR.CREATE_DATA_PREPARED;blocked->CLHR.ERROR | CLHR.VALIDATE_CREATE_RULE_INPUTS | stop | Enforce shared identity, validated logical mapping and default disclosure; stop at prepared data because Create BO integration is deferred |
