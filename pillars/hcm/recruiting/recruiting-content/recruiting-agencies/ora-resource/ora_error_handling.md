# Recruiting Agencies Error Handling

## Purpose

Defines customer-facing results, internal-only diagnostics, immutable approval gates, and stop-before-retry behavior.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation or agency field is missing | Return the named missing value and stop before lookup or package work |
| Referral Type, Contract Type, or Exclusivity Length is invalid or ambiguous | Return INVALID_LOOKUP_VALUE for the named field and request an enabled value |
| Person Specific lacks Exclusivity Length | Return EXCLUSIVITY_REQUIRED and request an enabled Exclusivity Length |
| Create finds an exact Agency Name | Return ALREADY_EXISTS; never convert Create to Update |
| Update finds no exact Agency Name | Return NOT_FOUND; never convert Update to Create |
| Update finds multiple exact Agency Names | Return AMBIGUOUS_AGENCY without exposing the match count |
| Allow Internal Candidate Search is requested | Return UNSUPPORTED_AGENCY_OPTION and direct the user to maintain it manually in Fusion |
| Agent, deletion, direct REST, or database work is requested | Return UNSUPPORTED and stop |
| Fresh export or package proof is missing, stale, or invalid | Return BLOCKED with one plain-language corrective action |
| A requested Retrieve field's CSV header is missing or duplicated | Return BLOCKED for that field; never shift columns or guess a replacement |
| Create StatusCode remains blank after defaulting | Return BLANK_STATUS_AFTER_DEFAULTING and do not submit |
| Project execution context is missing or inactive for Create, Update, or Import | Return to the initializer/core.runbook workflow described in dependency readiness before candidate preparation; distinguish missing local planning artifacts from a Run Book requiring creation. Do not report a package-validation failure or fabricate an envelope. For failed or unknown Run Book outcomes, reconcile instead of retrying. |
| Approval is absent or does not match the current ZIP fingerprint and target | Return BLOCKED and request approval for the current immutable preview |
| Export, lookup, import, or verification fails, conflicts, times out, is partial, or is uncertain | Return PROCESS_FAILED, preserve sanitized diagnostics, and stop without retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required operation, field, export, artifact, fingerprint, or approval is absent | Provide the named missing item and restart validation |
| INVALID_LOOKUP_VALUE | A supplied lookup code or meaning is disabled, unmatched, or ambiguous | Enter an enabled value for the named field |
| EXCLUSIVITY_REQUIRED | Person Specific has no valid Exclusivity Length | Enter an enabled Exclusivity Length |
| ALREADY_EXISTS | Create has an exact Agency Name match | Use a different name or submit a separate explicit Update |
| NOT_FOUND | Update has no exact Agency Name match | Enter an existing exact Agency Name |
| AMBIGUOUS_AGENCY | Update has more than one exact Agency Name match | Correct duplicate setup records before retrying |
| UNSUPPORTED_AGENCY_OPTION | Allow Internal Candidate Search is requested | Maintain the field manually in Fusion |
| UNSUPPORTED | Agents, deletion, direct APIs, database work, or unproven package content is requested | Remove the unsupported scope |
| BLOCKED | Fresh evidence, package proof, or matching approval is unavailable | Complete the stated prerequisite |
| PROCESS_FAILED | An operation fails or has an uncertain outcome | Review internal diagnostics and retry only through a new approved preview after resolution |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Retrieve success | Requested agency details under their exact customer-facing labels, using the named CSV-header mapping, without export narration or identifiers |
| Candidate preview | Target environment, Agency Name, Create or Update, effective values, and immutable ZIP SHA-256 |
| Approval request | Target environment, Agency Name, operation, and the exact fingerprint being approved |
| Successful import | Agency Name, completed operation, and successful business outcome |
| Validation or unsupported outcome | Short title, affected field or Agency Name when useful, stable result code, and one corrective action |
| Failed or uncertain operation | PROCESS_FAILED and one safe next action; technical evidence remains in internal diagnostics |

## Customer-Facing Response Contract

Normal output must never expose process or request identifiers, export identifiers, filenames, paths, package members, task codes, rule IDs, exact-match counts, stack traces, SQL/JBO details, or backend evidence. The target identity and ZIP fingerprint may be shown only at the explicit preview and approval gate. If technical diagnostics are explicitly requested, present sanitized details separately from the customer-facing result.

| Result | Customer-Facing Message Pattern |
|---|---|
| Retrieve success | Agency details retrieved. Return each requested field under its exact label; Main Contact comes from `AgencyContact` and Agency Email comes from `AgencyEmail` |
| Create success | Agency created. The recruiting agency “{Agency Name}” was created successfully |
| Update success | Agency updated. The recruiting agency “{Agency Name}” was updated successfully |
| MISSING | Required information is missing. Provide {Field Name} and try again. Error code: MISSING_REQUIRED_AGENCY |
| INVALID_LOOKUP_VALUE | {Field Name} isn’t valid. Enter an enabled {Field Name} value and try again. Error code: INVALID_LOOKUP_VALUE |
| INVALID_AGENCY_EMAIL | Agency Email isn’t valid. Enter a valid email address and try again. Error code: INVALID_AGENCY_EMAIL |
| INVALID_CREATE_JA_FLAG | Create job application on behalf of candidate isn’t valid. Enter Y or leave it blank. Error code: INVALID_CREATE_JA_FLAG |
| INVALID_STATUS | Status isn’t valid. Enter a target-valid Status value and try again. Error code: INVALID_STATUS |
| EXCLUSIVITY_REQUIRED | Exclusivity Length is required. Enter an enabled Exclusivity Length for a Person Specific agency. Error code: EXCLUSIVITY_REQUIRED |
| ALREADY_EXISTS | Agency already exists. A recruiting agency named “{Agency Name}” already exists. Use a different name or request an Update. Error code: ALREADY_EXISTS |
| NOT_FOUND | Agency not found. We couldn’t find “{Agency Name}” to update. Verify the name exactly and try again. Error code: NOT_FOUND |
| AMBIGUOUS_AGENCY | Agency name isn’t unique. Correct the duplicate agency records before trying again. Error code: AMBIGUOUS_AGENCY |
| UNSUPPORTED_AGENCY_OPTION | Manual action is required. Maintain Allow Internal Candidate Search in Fusion. Error code: UNSUPPORTED_AGENCY_OPTION |
| UNSUPPORTED | Request isn’t supported. This skill manages agency rows through the guarded FSM workflow and does not manage agents or deletion. Error code: UNSUPPORTED |
| BLOCKED | Action is required before we can continue. {Plain-language prerequisite}. Error code: BLOCKED |
| PROCESS_FAILED | The agency operation didn’t complete. Review the diagnostic record or contact your administrator before preparing a new preview. Error code: PROCESS_FAILED |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Agent-related request | Do not create, update, retrieve, export, import, provision, or relate agents, accounts, coverage, or roles |
| Unknown package contract | Do not invent files, columns, keys, child rows, relationships, serialization, or lifecycle values |
| Approval does not match the frozen preview | Do not invoke core.data-loader |
| Direct API, database, deletion, or manual-only field request | Do not create an alternate execution path |
| Failure, timeout, conflict, partial result, or uncertainty | Do not retry, resubmit, use REST fallback, or claim rollback or success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.PREVIEW_IMPORT | decision | 70 | execution_gate | approved->RA.IMPORT_READY;blocked->RA.HANDLE_ISSUES;changed->RA.HANDLE_ISSUES | RA.CHECK_DESIGN | stop | Before any import handoff |
| RA.HANDLE_ISSUES | step | 80 | error_handler | disclosed->RA.RETURN_ISSUES | none | stop | Any validation, lookup, identity, dependency, design, approval, process, or unsupported outcome |
| RA.DONE_RETRIEVE | terminal | 90 | terminal | none | RA.VERIFY_EXPORT_ROUTE | stop | Fresh agency export was verified and requested details were returned |
| RA.IMPORT_READY | terminal | 95 | terminal | none | RA.PREVIEW_IMPORT | stop | The unchanged candidate ZIP and exact approval are ready for core.data-loader |
| RA.RETURN_ISSUES | terminal | 100 | terminal | none | RA.HANDLE_ISSUES | stop | A customer-friendly outcome and safe next action were returned |
