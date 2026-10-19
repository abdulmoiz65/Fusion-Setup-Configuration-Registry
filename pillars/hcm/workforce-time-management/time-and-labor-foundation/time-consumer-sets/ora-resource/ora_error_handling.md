# Time Consumer Sets Error Handling

## Source Basis

- Time Consumer Sets authoring pack: 03-authoring-guardrails.md, 05-crud-lifecycle-behavior.md, and 06-rest-describe-evidence.md.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The target release is before 27A | Inform the user: Time Consumer Sets is not available through this skill for environments before release 27A. Stop before validation, lookup, REST sample generation, provider approval, or execution. |
| Release details are unavailable and the live REST capability cannot be confirmed, or a 27A-or-later environment lacks one exact usable current timeConsumerSets registration and metadata set | State that this skill cannot be used in the target environment because its required REST capability is unavailable. Stop; do not select FSM, reuse historical metadata, or use a direct REST route. |
| A required parent field, routing selection, consumer, or selected-consumer Time Category is missing | Identify the missing business value and stop before preview. |
| A new configuration has a blank, nonnumeric, or different TimeConsumerSetId from its parent | Block preview and upload. Generate one unique numeric local parent ID and repeat it exactly in every new configuration row. |
| Time Category lookup is zero, many, or unavailable | Mark the selection unresolved and stop; do not use a sample identifier or select a partial TcatName match. |
| A criteria search or update has multiple matches | Show every Consumer Set meeting all supplied conditions and ask the user to select one. |
| A criteria search or update has no match | State that no Consumer Set met all supplied conditions. |
| A create duplicate check finds an exact-name, partial-name, or equivalent-parameter candidate | Present the matching Consumer Set's business values and wait for the user's choice to use it or create a new Consumer Set; do not prepare, submit, or create anything without that choice. |
| An update criteria search has no selected complete record, a page is incomplete, or the complete record cannot be read | Stop before preview; do not create a new Consumer Set, infer an identity, or alter current approval settings. |
| A detail lookup returns 401 or 403 | Classify as authentication or authorization failure; do not treat the parent or configuration as absent. |
| An existing child identity is missing or ambiguous | Stop before child update or delete; select one verified current configuration. |
| A final Data Loader DAT contains a Python-style Boolean literal | Classify as input validation; stop before upload, correct the XLSX-to-DAT serialization to lowercase true or false, validate the final archive contents, and obtain fresh approval. |
| A write result is uncertain | Do not replay POST, PATCH, DELETE, or upsert automatically; reconcile only through an approved read-only verification path. |
| A direct REST request would expose an opaque key or internal code in user-facing output | Replace it with a descriptive placeholder or verified business label. |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not enter the provider-owned approval process and do not place a warning, diagnostic, or technical note in the summary. |
| A Complete Summary includes Worker approval or ApprovalWorkflowForWorkersFlag | Remove the internal attribute from the summary and Defaults Applied; retain false only for loader execution. |
| Complete Summary and Defaults Applied were not displayed before an approval request | Return to the approval gate, display the required business-only summary, and then request approval; do not upload or initiate a load first. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Unsupported release | The target environment release is before 27A | Inform the user that Time Consumer Sets is not available through this skill for environments before release 27A; stop without an alternate route. |
| Capability unavailable | The release is 27A or later, or unavailable, and usable current timeConsumerSets REST metadata cannot be confirmed | Explain that the skill cannot be used in the target environment and stop; do not select FSM or direct REST. |
| Input validation | Required or conditional field validation fails | Correct the affected business value and restart validation. |
| Input validation | Complete Summary source is blank, unverified, unresolved, or metadata-only | Correct the source values before generating the summary. |
| Input validation | A Boolean value in the final upload archive is not lowercase true or false | Correct the source conversion, verify the final DAT archive contents, and restart validation and approval. |
| Lookup resolution | The documented Time Category collection returns no exact TcatName match or more than one exact match | Correct the supplied Time Category business value or resolve the ambiguity before preview. |
| Lookup resolution | The paginated Consumer Set collection cannot be completed or its required name comparison cannot be evaluated | Preserve sanitized evidence and stop; do not treat a partial collection as no match. |
| Authentication or authorization | A read-only Fusion call returns 401 or 403 | Refresh authentication once only where the shared client permits, then stop if rejected again. |
| Existing-record key resolution | A current configuration cannot be selected exactly | Re-read the parent with configurations and select one current child. |
| Fusion API | A documented service response reports an error | Preserve redacted diagnostics and stop before retry. |
| Approval blocker | A proposed mutation lacks the owning workflow's exact preview and approval | Present the approved workflow's target and effect, then wait for approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Unsupported release | State that Time Consumer Sets is not available through this skill for environments before release 27A. |
| Capability unavailable | State that the required REST capability is unavailable in the target environment and the skill cannot be used there. |
| Validation or lookup failure | Affected business field, safe failure class, and one safe next action. |
| Authentication failure | Target environment, read-only operation, and access failure without credentials or tokens. |
| Mutation gate | Exact business target and the missing preview or approval condition. |
| Complete Summary is blocked | Missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The target release is before 27A | Do not validate task fields, perform lookups, generate REST samples, seek approval, or execute a route. |
| Required REST capability is unavailable | Do not select an FSM fallback, reuse historical metadata, or execute a direct REST request. |
| A lookup contract is incomplete | Do not present the task as preview-ready or execute a substitute lookup. |
| A write failed or has an uncertain result | Do not automatically retry a non-idempotent operation. |
| Nested parent payload behavior is not verified | Do not claim child create, update, or deletion semantics from UI payload shape alone. |
| A direct REST mutation is considered | Do not author or execute it from this ora-resource set. |
| A Complete Summary is presented | Do not expose identifiers, codes, keys, internal values, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw boolean values, diagnostics, warnings, Worker approval, or ApprovalWorkflowForWorkersFlag. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.HANDLE_ERROR | step | 90 | error_handler | handled->TCS.RETURN_ISSUES | none | stop | A validation, release-support, dependency, lookup, design, authorization, service, or approval gate is blocked |
| TCS.RETURN_UNSUPPORTED_RELEASE | terminal | 95 | terminal | none | TCS.CHECK_RELEASE_SUPPORT | stop | The target environment is before release 27A; inform the user that Time Consumer Sets is not available through this skill |
| TCS.RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | A blocking issue has been disclosed with one safe next action |
| TCS.PROVIDER_APPROVAL | step | 60 | execution_gate | ready->TCS.READY;blocked->TCS.HANDLE_ERROR;unsupported->TCS.HANDLE_ERROR | TCS.ENFORCE_DESIGN | stop | A valid business-only Complete Summary is present; provider execution and approval ownership remain unchanged |
| TCS.READY | terminal | 110 | terminal | none | TCS.PROVIDER_APPROVAL | stop | Input, dependencies, defaults, design gates, and Complete Summary passed for handoff to the provider-owned approval process |
| TCS.SEARCH_SINGLE_RESULT | terminal | 91 | terminal | none | TCS.SEARCH_TIME_CONSUMER_SETS | stop | One name-search match was loaded completely and presented to the user |
| TCS.SEARCH_MULTIPLE_RESULTS | terminal | 92 | terminal | none | TCS.SEARCH_TIME_CONSUMER_SETS | stop | Multiple case-insensitive name-search matches were presented to the user for selection |
| TCS.SEARCH_NO_RESULTS | terminal | 93 | terminal | none | TCS.SEARCH_TIME_CONSUMER_SETS | stop | No exact or case-insensitive contains name-search match was found |
| TCS.AWAIT_DUPLICATE_CHOICE | terminal | 94 | terminal | none | TCS.SEARCH_TIME_CONSUMER_SETS | stop | A create request has a similar Consumer Set with all supplied criteria matching and awaits the user's use-existing or create-new choice |
