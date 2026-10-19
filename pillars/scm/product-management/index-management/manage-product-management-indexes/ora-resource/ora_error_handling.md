# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The request names multiple indexes or an attribute's index cannot be assigned unambiguously | Stop before index-specific lookup or payload preparation. Ask the user to select one index and its attributes for this invocation; do not split or queue the input. |
| Final immutable Data Loader ZIP contains a different IndexName or more than one indexed-attributes DAT | Stop before Task Hook and approval with `input_validation`. Rebuild and revalidate an artifact for only the active canonical index. |
| The selected index load, readback, or ESS result is pending, failed, or uncertain | Report its status and next user action. Do not resubmit or start a different index as a continuation of this invocation. |
| Business object is blank or differs from productManagementESIndexedAttributes | Stop and request the exact registered Data Loader business object. |
| Business-object registration lookup is unavailable, returns no exact match, or has an undocumented contract | Stop before sample generation or import planning; record the unresolved registration requirement. |
| User-provided index name is absent, has no exact LookupCode-or-Meaning match in ORA_EGP_PM_ES_INDEXES, or matches multiple unique LookupCodes | Stop before the action-specific lookup and payload preparation. Request a disambiguated index name; do not choose a LookupCode. |
| Index scope is absent, or scope resolution returns zero or multiple candidates | Stop before payload preparation. Request IndexName, GroupCode, and ObjectCode; do not infer a target from the attribute name. |
| Index scope resolution returns exactly one candidate | Stop and present the candidate IndexName, GroupCode, and ObjectCode for user confirmation. Do not continue to exact attribute validation until it is confirmed. |
| Seeded index metadata is unavailable, malformed, or includes an invalid SeededIndexedAttributes identity | Stop before addition-delta calculation. Correct the index name or obtain a valid metadata response; do not infer seeded attributes. |
| Existing indexed-attribute lookup is unavailable, malformed, or returns a row without a complete code identity | Stop before addition-delta calculation. Do not assume that an attribute is absent. |
| Addition delta is empty and no removals are requested | Do not prepare Data Loader rows. For a rebuild-only request, this means every seeded identity is already indexed. Record that the index already matches the calculated target state, then prepare the ESS rebuild request unless the user explicitly confirms that ESS submission is not required. |
| Data Loader change is pending or failed | Do not prepare or submit the ESS rebuild job. Report the Data Loader status and wait for completion or correction. |
| A nonempty delta reaches the Data Loader gate | Require the validated request and delta, final ZIP digest, exact target environment, and core Data Loader approval before import. If approval is absent, stop at REQUEST_DATA_LOADER_APPROVAL. After an accepted Request ID, stop at WAIT_DATA_LOADER_STATUS until the user requests a check. A pending check returns to that wait terminal. Only a user-requested terminal successful status for the same Request ID and canonical index permits VERIFY_LOADED_ATTRIBUTES; failed or uncertain status stops at HANDLE_ERROR. Resume this gate from the durable task record; do not recalculate the post-import delta, re-upload, or infer consent. |
| A terminal successful Data Loader status is returned | Preserve the complete core status report, then read back every requested change for the exact canonical IndexName. If all changes verify, prepare the ESS payload and request fresh approval in the same reply. |
| Post-load readback is missing a requested addition, retains a requested removal, or returns another index | Persist a `blocked` continuation state with the readback evidence. Do not prepare or submit ESS. |
| ESS rebuild approval is absent | Present the exact ESS payload, target environment, and index impact; stop until the user explicitly confirms submission. |
| The narrow DELETE lookup returns zero rows, returns multiple exact matches, or a supplied AttributeId differs from the exact target record | For zero rows, run the declared index-only fallback, follow every page, and match the exact index, attribute, group, and object names locally. Stop before payload preparation if that read is incomplete, no unique backend-issued AttributeId remains, or the supplied ID differs. Correct the identity or ID; do not synthesize or reuse an ID. |
| Available-attribute lookup returns zero or multiple matches, or its response does not include items | Stop before POST payload preparation or import planning; do not infer the attribute code or target context. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | The request names multiple indexes, has ambiguous attribute-to-index assignment, or its archive contains a different IndexName | Select one index and correct its request or artifact before any Fusion mutation; do not split, merge, or skip indexes automatically. |
| input_validation | The business object value is blank or does not exactly match the task contract | Correct the business object and restart validation. |
| catalog_or_metadata_mismatch | The supplied business object cannot be verified as the exact registered object | Obtain the documented read-only registration lookup contract and verify one exact match. |
| input_validation | User-provided index name is absent or does not resolve through an exact LookupCode-or-Meaning match to one unique LookupCode in ORA_EGP_PM_ES_INDEXES | Provide a disambiguated index name, then restart index validation. |
| input_validation | IndexName is absent, or the available-attributes lookup cannot resolve exactly one scope candidate | Provide IndexName, GroupCode, and ObjectCode, then restart scope validation. |
| input_validation | RestAction DELETE cannot resolve exactly one backend-issued AttributeId from IndexName, AttributeName, GroupName, and ObjectName, or a supplied AttributeId does not match it | Correct the exact indexed-attribute identity or AttributeId and restart removal validation. |
| approval_blocker | One available-attributes lookup result supplies one scope candidate but the user has not confirmed it | Present the candidate scope and wait for explicit confirmation before exact attribute validation. |
| catalog_or_metadata_mismatch | A POST indexed attribute cannot be uniquely validated from indexAvailableAttributes | Correct the indexName request body or requested attribute context, then verify one exact available attribute. |
| catalog_or_metadata_mismatch | Seeded metadata or existing indexed attributes cannot be represented as complete AttributeCode#GroupCode#ObjectCode identities | Correct the live metadata contract before calculating a delta. |
| approval_blocker | A required Data Loader change has succeeded, or Data Loader was intentionally skipped for an empty delta, but the exact ESS payload has not received fresh confirmation | Present the rebuild payload and wait for approval. |
| process_failed | A terminal successful Data Loader status cannot be verified by exact-index readback | Preserve the readback evidence and correct the index data before any ESS preparation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| When multiple indexes are supplied | State that this skill accepts one index per invocation and ask which index and attributes to process now; do not present a queued execution plan. |
| Before any Data Loader sample generation or REST import planning | The exact business object, registration-verification status, and any unresolved lookup fields. |
| Before the available-attributes lookup | The supplied index name, whether LookupCode or Meaning matched, the unique returned LookupCode, lookup type ORA_EGP_PM_ES_INDEXES, and lookup Meaning as display evidence. |
| Before payload preparation for an added indexed attribute | The target index, group, object, requested attribute name, and available-attribute validation result. |
| Before addition-delta payload preparation | The seeded identity count, requested-addition identity count, existing identity count, and resulting addition count; do not expose backend IDs. |
| Before payload preparation for an indexed attribute removal | The target index, requested attribute name, group name, object name, and backend-issued AttributeId resolved directly from Product Management Indexed Attributes. |
| After scope resolution returns one candidate | The candidate index, group, object, source attribute name, and a request for explicit scope confirmation. |
| After a successful terminal Data Loader status | The unchanged complete core status report, post-load readback result, target environment, affected index, rebuild impact, exact immutable ESS payload, and fresh approval question. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The request or approved archive contains multiple indexes | Do not pass it to Task Hook, Data Loader, or ESS; do not upload, initiate, submit a rebuild job, or silently select an index. |
| A different index is requested after this invocation | Treat it as a separate request with fresh input validation and approval gates; never carry approval or an external Request ID across indexes. |
| The business-object registration is unverified or the lookup contract remains `TBD` | Do not infer a REST path, build a payload, generate an import plan, or attempt a Fusion write. |
| Index-name lookup is unverified, missing, or ambiguous | Do not call indexAvailableAttributes, use a lookup Meaning as IndexName, build a payload, or initiate a Data Loader workflow. |
| Available-attribute validation is unverified for RestAction POST | Do not infer an attribute code, target context, or payload. |
| RestAction DELETE has no uniquely resolved AttributeId from the exact IndexName, AttributeName, GroupName, and ObjectName, or has a mismatched user-supplied AttributeId | Do not build a delete row, reuse an AttributeId from another record, or initiate a Data Loader workflow. |
| Scope resolution is unconfirmed, missing, or ambiguous | Do not populate GroupCode or ObjectCode, build a payload, or initiate a Data Loader workflow. |
| The addition delta is empty and no removals are requested | Do not initiate Data Loader. Do not skip ESS unless the user explicitly confirms it is not required. |
| A Data Loader change has not been verified successful | Do not submit the ESS job. |
| A successful Data Loader status has not yet completed exact-index readback | Do not end the index-management response at the status report or prepare an ESS approval prompt. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PMINDEX.REQUEST_SCOPE_CONFIRMATION | terminal | 60 | terminal | none | none | stop | One scope candidate is resolved and requires user confirmation |
| PMINDEX.REQUEST_SCOPE_INPUT | terminal | 70 | terminal | none | none | stop | Canonicalized index name or index scope is missing or cannot be resolved uniquely |
| PMINDEX.REQUEST_ATTRIBUTE_ID | terminal | 95 | terminal | none | none | stop | A removal request could not resolve the backend-issued AttributeId for the exact indexed-attribute record |
| PMINDEX.HANDLE_ERROR | terminal | 200 | terminal | none | none | stop | Validation or lookup fails or is blocked |
| PMINDEX.DATA_LOADER_GATE | decision | 110 | execution_gate | approval_required->PMINDEX.REQUEST_DATA_LOADER_APPROVAL;status_not_requested->PMINDEX.WAIT_DATA_LOADER_STATUS;status_pending->PMINDEX.WAIT_DATA_LOADER_STATUS;status_succeeded->PMINDEX.VERIFY_LOADED_ATTRIBUTES;status_failed->PMINDEX.HANDLE_ERROR;blocked->PMINDEX.HANDLE_ERROR | none | stop | Nonempty POST or DELETE delta; require immutable artifact approval and a successful user-requested status for the same accepted Request ID before readback |
| PMINDEX.REQUEST_DATA_LOADER_APPROVAL | terminal | 115 | terminal | none | PMINDEX.DATA_LOADER_GATE | stop | Exact Data Loader artifact and target environment require core.data-loader approval before any import |
| PMINDEX.WAIT_DATA_LOADER_STATUS | terminal | 116 | terminal | none | PMINDEX.DATA_LOADER_GATE | stop | Accepted Data Loader Request ID awaits an opt-in status check or remains pending; resume only from the recorded gate |
| PMINDEX.REQUEST_ESS_APPROVAL | terminal | 145 | terminal | none | PMINDEX.PREPARE_ESS_REBUILD | stop | Immutable ESS payload prepared; fresh approval is required |
| PMINDEX.REQUEST_ESS_APPROVAL_EMPTY | terminal | 146 | terminal | none | PMINDEX.PREPARE_ESS_REBUILD_EMPTY | stop | Empty delta skipped Data Loader; immutable ESS payload still requires fresh approval |
| PMINDEX.DONE_ESS_SKIP_AFTER_LOAD | terminal | 148 | terminal | none | PMINDEX.PREPARE_ESS_REBUILD | stop | After verified load, user explicitly confirmed ESS submission is not required; record the skip decision |
| PMINDEX.DONE_ESS_SKIP_EMPTY | terminal | 149 | terminal | none | PMINDEX.PREPARE_ESS_REBUILD_EMPTY | stop | With empty delta, user explicitly confirmed ESS submission is not required; record the skip decision |
