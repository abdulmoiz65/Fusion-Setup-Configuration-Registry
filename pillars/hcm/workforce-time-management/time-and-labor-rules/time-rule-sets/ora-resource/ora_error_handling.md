# Time Rule Sets Error Handling

Source: Requested discriminator, matching, dependency, cycle, ordering, effective-date, approval, and import safeguards, observed failed-parent-key and missing-member reconciliation evidence, the developer-requested new-Time-Rule preview and approval gate, and developer-provided failed-import evidence for BOM-prefixed CSV headers and a short or overlong CSV row.

## Error Situations

| Situation | What Should Happen | Next Action |
|---|---|---|
| Parent or member required data is missing or invalid | Identify the row and stop before import | Correct the source row |
| A Time Rule Sets CSV starts with EF BB BF or the first parsed header is not RuleSetName or ProcessingOrder as applicable | Stop before import; classify the package as invalid | Rewrite both CSV files as UTF-8 without BOM, validate their first bytes and headers, and create a new ZIP |
| A Time Rule Sets CSV data row has more or fewer parsed fields than its header | Stop before preview or import; classify the package as invalid | Report the file, row number, header field count, and row field count; rebuild the CSV with exactly matching field counts and create a new ZIP |
| Fusion reports that the first required attribute is missing even though it is visibly present in the CSV | Treat CSV encoding as a primary diagnostic; do not assume the business value is missing | Inspect the raw first three bytes and parsed first header, reconcile whether any parent or member rows were created, then correct the package |
| Parent resolution is missing, ambiguous, uncommitted, or sourced only from an import diagnostic | Do not default or retain member RuleSetUnqId | Refresh the authoritative Time Rule Sets export and resolve exactly one committed parent row |
| Time Rule match is missing, ambiguous, compatible-only, or unverified | Do not retain an unresolved RuleName reference | Refresh lookup; obtain selection for ambiguous candidates, or prepare the missing complete requested rule through the supported Time Rules workflow |
| No verified existing Time Rule matches a complete requested condition | Do not block local rule preparation | Derive a compatible rule from an exact verified sibling or documented template, and prepare and validate the immutable Time Rules archive |
| New Time Rule requirement is incomplete | Do not prepare the rule archive | Request only the missing rule type, threshold, period, or intended result |
| Time Rules archive is unapproved or differs from the approved archive | Stop before the Fusion import and dependent Rule Set preparation | Obtain approval for the exact current immutable archive |
| Referenced RuleType is incompatible with RuleSetType | Block the Rule member | Correct the member or obtain an authorized compatibility mapping |
| Child Rule Set is missing, ambiguous, or unready | Block the nested member | Correct identity or prepare and verify the child first |
| Child reference creates a self, direct, or indirect cycle | Reject the reference | Remove the cyclic edge and rerun graph validation |
| Time Category is missing or ambiguous | Block the member and do not auto-create a category | Correct the code or name, or separately authorize category creation capability |
| ProcessingOrder is nonpositive, duplicate, or duplicates member identity at the same order | Reject the member collection | Assign unique positive values and remove duplicate identity |
| Parent, rule, child, or category effective dates are incompatible or unknown | Block the affected member | Supply authoritative date evidence or correct the effective interval |
| Missing Time Rule import fails or cannot be verified | Stop Rule Set preparation | Diagnose and verify the Time Rule before reference |
| Upstream Time Rules import is accepted but is not terminal | Start task-authorized status monitoring and preserve the approved Rule Set intent | Continue status requests until terminal success or failure; on success, refresh and verify the named rules before Rule Set preparation; never retry the import automatically |
| Validated immutable FSM CSV ZIP or explicit import approval is missing | Stop before live creation or update | Prepare and validate the package through core.data-loader, then obtain approval for its immutable preview |
| A package was prepared from a copied source Rule Set row, its metadata differs from the fresh export, or a literal blank, `0`, or `#null` changed during preparation | Stop before preview or import | Reprepare from normalized intent and the fresh staged package contract, then validate through core.data-loader |
| The exact validated stage ZIP is not linked before approval | Stop before requesting approval | Display the clickable link to the immutable parent-only or member-only ZIP, then request the stage-specific approval |
| Import result is uncertain | Never resubmit automatically | Reconcile and verify authoritative state first |
| Parent and member are submitted together before a committed RuleSetUnqId is available | Stop member preparation even when metadata orders the parent first | Import and verify the parent stage, refresh the authoritative export, then create a new member preview |
| Parent import fails in an approved multi-stage request | Stop the workflow before member preparation or upload | Report the parent failure and preserve the approved request for a corrected parent retry |
| Parent import succeeds but the workflow is about to stop without preparing approved members | Treat this as incomplete orchestration, not successful completion | Refresh Time Rule Sets, resolve committed RuleSetUnqId, and automatically present the member archive preview |
| Member archive has not received its own exact Data Loader approval | Stop before member upload even when the parent archive was approved | Present the immutable member preview and wait for its separate exact `approve` |
| Member import reports success but the refreshed export has no exact member row | Classify the run as verification failed; do not report the member as attached | Re-resolve the committed parent RuleSetUnqId, rebuild GroupingKey, obtain approval for the corrected member import, and verify again |
| Accepted asynchronous request fails, times out, has partial success, remains uncertain, or fails read-back verification | Do not report final success and do not retry upload, initiation, create, update, import, or load | Preserve the last known status and verification evidence; provide one safe investigation or resume action |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, unavailable, or its bounded polling slice ends without a result | Do not ask the user to retry exports, check again, or approve another export | Continue task-authorized status monitoring with the same accepted ProcessId until a terminal result is available |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, returns no result, has partial or uncertain status, or produces an unusable ZIP | Do not claim the export evidence is ready and do not submit a duplicate export automatically | Preserve the accepted ProcessId, last-known status, ProcessLog when available, and ZIP-validation evidence; provide one safe investigation or resume action |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Defaulting | A required parent or member default cannot be produced | Correct the affected row before validation |
| Input | A field, discriminator, order, identity, type, or date rule fails | Correct and revalidate the package |
| Package encoding | A CSV contains a BOM or a file-specific first header cannot be parsed exactly | Rebuild the complete package as UTF-8 without BOM and revalidate it before seeking retry authorization |
| Package shape | A CSV data row has a different parsed field count from its header | Rebuild the package with exact header-width rows and revalidate it before seeking approval |
| Package contract | The archive is not prepared from the fresh staged headers/metadata contract, or literal field states were not preserved | Reprepare from normalized intent and rerun Data Loader validation |
| Lookup | A rule, child Rule Set, parent, or category is missing or ambiguous | Refresh or correct the authorized source |
| Decision required | Rule candidates are multiple or compatible-only | Disclose differences and obtain user selection |
| Rule requirement incomplete | A missing Time Rule request lacks its type, threshold, period, or intended result | Request only the missing requirement; do not prepare an archive |
| Import approval required | A validated Time Rules or Time Rule Sets archive is unapproved or materially different from its approved preview | Present or refresh the exact immutable archive and stop only before Fusion import |
| Final completion monitoring | An approved asynchronous request is accepted but not yet terminal | Continue task-authorized status requests and preserve the continuation state; do not treat accepted initiation as verified success |
| Export monitoring | A task-authorized read-only export or authoritative refresh is accepted but not yet terminal, downloaded, or ZIP-validated | Continue status checks using the same accepted ProcessId; do not request a retry or submit a duplicate export for the same task and purpose |
| Export failure | A task-authorized read-only export or authoritative refresh fails, times out, has no usable result, or the result ZIP fails validation | Preserve status and process evidence; do not claim readiness or retry automatically |
| Dependency graph | A child is unready or cyclic | Prepare the child or remove the cycle |
| Import | A required FSM CSV package, approval, or verification is missing | Resolve the gap through core.data-loader; do not invent a direct REST create route |
| Reconciliation | Import status is uncertain | Verify state before retrying |
| Verification failed | The import completed but the authoritative export lacks the exact parent-member relationship | Re-resolve the committed parent identity and stop before a separately approved corrective import |

## Disclosure Rules

| Situation | What Must Be Shown |
|---|---|
| Defaulting failure | Affected row, field, and expected default |
| Package encoding failure | Affected file, observed first-byte signature, expected first header, parsed first header, whether Fusion created any parent or member rows, and the corrected package identity |
| Package shape failure | Affected file, data-row number, expected header field count, observed row field count, whether Fusion created any parent or member rows, and the corrected package identity |
| Rule selection required | Candidate RuleNames, types, normalized behavioral differences, and verification state |
| New Time Rule archive approval | Rule Type, rule name and description, template or formula, condition and threshold, Time Category, summation and reporting levels, message text and severity, effective dates, immutable archive identity, and confirmation that Fusion import does not occur before explicit approval |
| Child resolution or cycle failure | Parent, child, and complete discovered dependency path |
| Category resolution failure | Supplied code or name and missing or ambiguous result |
| Compatibility or date failure | Compared values, authorized rule if known, and unresolved evidence |
| Import block | Missing package, approval, or verification fields and confirmation that no Fusion change was attempted |
| Final completion monitoring | Accepted request identity, last known status, verified or pending configuration, defaulted values labeled Default, and the task-authorized monitoring stage |
| Export monitoring | Accepted export ProcessId, export purpose, last known status, polling stage, persisted ZIP reference when available, ZIP validation result, and confirmation that no duplicate export was submitted |
| Uncertain result | Submission identity, known status, and required verification step |
| Member verification failure | RuleSetName, committed exported RuleSetUnqId, ProcessingOrder, referenced RuleName or RuleSetName1, whether an exact member row exists, and the source of every identifier considered |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Rule or child reference is unresolved or ambiguous | Do not retain or import the reference |
| Either Time Rule Sets CSV starts with EF BB BF or has the wrong parsed first header | Do not submit the package |
| Any Time Rule Sets CSV data row does not have exactly the header's field count | Do not preview, approve, or submit the package |
| A package is derived by copying an existing Rule Set row or its exact validated ZIP is not linked before approval | Do not request approval or submit the package |
| An import fails because of package encoding | Do not resubmit automatically; require a corrected package, authoritative-state reconciliation, and explicit retry authorization |
| A compatible-only rule is found | Do not select it automatically |
| A validated Time Rules archive has not received explicit approval for its exact current preview | Do not import the Time Rule or continue dependent Rule Set creation |
| Any prepared Time Rule detail changes after archive approval | Do not reuse the prior approval; rebuild the archive and request approval for the revised immutable archive |
| An approved asynchronous request is In progress or not available | Do not ask for separate status authorization or retry the submission; continue only the task-authorized status monitoring and read-back verification flow |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, or unavailable | Do not ask the user to retry exports, check again, or approve another export; continue monitoring only the same accepted ProcessId |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, has no result, or produces an invalid ZIP | Do not report export evidence as ready or submit a duplicate export automatically |
| A category is missing | Do not create it without separately authorized capability |
| A cycle is detected | Do not prepare the parent |
| Type or effective dates are incompatible | Do not prepare the member |
| No direct REST create endpoint is documented | Do not block the FSM CSV import route or invent a direct REST create action |
| Import status is uncertain | Do not automatically resubmit |
| A RuleSetUnqId appears only in an import response, process log, exception key, failed transaction, or local prediction | Do not use it for a member row |
| A member import reports success but the authoritative export lacks the relationship | Do not report success and do not retry without a corrected preview and approval |
| Parent approval exists but member approval does not | Do not infer or reuse approval; do not upload the member archive |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RULESET.DEFAULT_ERROR | terminal | 17 | terminal | none | none | stop | Runtime defaulting failed |
| RULESET.INPUT_ERROR | terminal | 8 | terminal | none | none | stop | Parent, member, lookup, compatibility, date, or cycle validation failed |
| RULESET.DEPENDENCY_ERROR | terminal | 9 | terminal | none | RULESET.DEPENDENCY | stop | Dependency readiness failed |
| RULESET.IMPORT_HANDOFF_READY | terminal | 10 | terminal | none | RULESET.COMPLETE_SUMMARY | stop | The Complete Summary is displayed and the validated immutable FSM CSV ZIP is ready for the provider-owned Data Loader approval preview and import |
| RULESET.FINAL_COMPLETION_ERROR | terminal | 12 | terminal | none | none | stop | Task-authorized status monitoring reached failure, timeout, partial success, uncertainty, or read-back mismatch |
| RULESET.FINAL_COMPLETION_SUCCESS | terminal | 13 | terminal | none | RULESET.FINAL_COMPLETION | stop | Terminal success status and authoritative read-back verification both passed |
| RULESET.EXPORT_READY | terminal | 15 | terminal | none | RULESET.EXPORT_MONITOR | stop | Terminal export success, persisted result ZIP, and ZIP validation all passed |
| RULESET.EXPORT_ERROR | terminal | 16 | terminal | none | none | stop | Export monitoring reached failure, timeout, missing result, unusable ZIP, partial status, or uncertainty |
