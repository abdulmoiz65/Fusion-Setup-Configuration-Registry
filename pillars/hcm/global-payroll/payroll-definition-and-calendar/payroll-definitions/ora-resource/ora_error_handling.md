# Payroll Definitions Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, object, calendar field, effective date, or key is missing | Classify as input validation, return each affected field, and stop before DAT preparation. |
| Target View Business Objects metadata is missing or conflicts with a proposed header | Classify as catalog mismatch, identify the object and conflicting field or action, and require a new target export. |
| A VBCS/Redwood create is requested but the exact mutation endpoint or payload is not source-evidenced | Classify as unsupported VBCS create contract, identify the missing method, PayRestName, payload, required-field, or date-serialization evidence, and stop. Do not ask for an HDL template when the requested field is present in the supplied PayrollDVO. |
| A lookup returns no match | Return the field, supplied value, LDG and effective-date scope, and a not-found result. |
| A lookup returns multiple matches | Return an ambiguity error and request a more precise value; never choose automatically. |
| An Allow Negative Payments lookup value has zero or more than one exact Code or Meaning match | Return not-found or ambiguity as applicable; do not normalize, alter, fuzzy-match, or substitute the supplied value. |
| PlannedSubmissionFixedDate is not a valid date or the supplied time is not exactly HH24:MI:SS | Return this validation message: You must enter the date for the PlannedSubmissionFixedDate attribute in YYYY/MM/DD HH24:MI:SS format. |
| A Consolidation Group / Consolidation Set lookup has more pages than were retrieved | Return incomplete-paging and stop before using any candidate. |
| ConsolidationSetCode is absent but ConsolidationSetName, Name, Consolidation Group, or Consolidation Group Name is supplied | Derive ConsolidationSetCode from that same exact supplied value and continue; do not classify the code as missing, stop, or prompt the user. |
| OrganizationPaymentMethodCode is absent but Organization Payment Method Name, OrgPaymentMethodName, or BaseOrgPayMethodName is supplied | Derive OrganizationPaymentMethodCode from that same exact supplied value and continue; do not classify the code as missing, stop, or prompt the user. |
| A Payroll Definition lookup finds a row outside the requested LDG or effective date | Return a field-level effective-date-range or not-found error; never use that PayrollId. |
| An Organization Payment Method lookup finds a row outside the exact LDG or EffectiveDate | Return a field-level effective-date-range or not-found error; never use that OrgPaymentMethodId. |
| A lookup route, filter, field projection, paging rule, or eligible-OPM contract is unresolved | Stop before runtime lookup or production-readiness claims and request target-pod evidence. |
| Authentication or LDG data access is denied | Classify as auth or authz; do not reinterpret denial as absence or expose credentials. |
| A read-only lookup fails in transport or the target environment | Classify as transport or environment, preserve sanitized request scope, and stop without inventing a match. |
| Fusion or HDL rejects the DAT | Classify as Fusion API or process failed as applicable, return the object, redacted row identity, phase, and confirmed message, and require a corrected new archive. |
| A loader operation times out | Classify as process timeout and report environment, operation, business object or TaskCode, ProcessId or requestId when available, last status, elapsed wait, and safe next-check path. |
| A diagnostic or project artifact cannot be persisted | Classify as artifact persistence, preserve the in-memory result, and report the intended destination without exposing sensitive data. |
| Preview or explicit approval is missing for a live HDL handoff | Classify as approval blocker and stop before upload, import, or load. |
| A live upload, import, or load outcome is uncertain | Verify through safe status reads in the authorized loader workflow; do not retry automatically or claim success. |
| Delete, end-date, correction, retroactive adjustment, or an unconfirmed localization is requested | Return Unsupported and identify the missing target action, key, field, or localized contract. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Required values, formats, keys, dates, or coherent schedule fields are missing or invalid | Correct the reported fields and validate again. |
| CATALOG_MISMATCH | Target HDL metadata is absent, stale, or inconsistent with the proposed HDL action or header | Re-export the affected business-object attributes and reconcile the contract. |
| AUTH_AUTHZ | Authentication, functional privilege, Data Exchange access, or LDG data security fails | Correct access through the authorized environment owner; do not expose or persist credentials. |
| TRANSPORT_ENVIRONMENT | A read-only lookup or loader handoff cannot reach the target safely | Preserve sanitized diagnostics and retry only after the environment issue is resolved. |
| FUSION_API | Fusion rejects a read or returns an unrecognized contract | Preserve the redacted response evidence and confirm the target release contract. |
| PROCESS_TIMEOUT | A separately authorized loader workflow does not reach a terminal status in the allowed wait | Report the last confirmed state and use the safe next-check path. |
| PROCESS_FAILED | Import, load, or record processing reaches a confirmed failure | Retrieve available status or process messages, correct the source, and prepare a new archive. |
| ARTIFACT_PERSISTENCE | Required diagnostics cannot be written to the approved project path | Report the path and retain a sanitized result for manual persistence. |
| APPROVAL_BLOCKER | Exact preview or explicit approval is missing or stale | Regenerate the preview and obtain approval bound to it. |
| AMBIGUOUS | More than one reference match exists | Request a more precise code, source key, or context. |
| INCOMPLETE_PAGING | A required lookup response has more pages or a page cannot be retrieved | Stop and retrieve all pages before resolving a value. |
| EFFECTIVE_DATE_RANGE | A matched object does not contain the requested effective date or range | Correct the effective date or select an object effective for that date or range. |
| UNSUPPORTED | Supplied evidence does not establish the requested action, field, or localization behavior; this includes a VBCS mutation payload not evidenced by PayrollDVO | Stop and obtain target-pod evidence. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation | Business object, operation, affected field, supplied sanitized value, and required correction. |
| Reference resolution | Resolver, source field, LDG and effective-date scope, match count, and no-match or ambiguity result. |
| Metadata readiness | Target environment, business object, export date or release when known, missing action or attribute facts, and affected DAT header. |
| Live HDL handoff | Target environment, object sequence, archive identity, operation, key strategy, LDG, effective dates, calendar design, business effect, unresolved risks, and exact approval status. |
| Loader timeout or failure | Environment, operation, business object or TaskCode, ProcessId or requestId when available, phase, last status, elapsed wait, sanitized messages, and safe next action. |
| Sensitive evidence | Confirm that credentials, tokens, cookies, private keys, customer data, protected identifiers, and sensitive payloads were redacted and not persisted. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Target HDL metadata is absent or stale | Do not present a production DAT or HDL field contract as ready; continue VBCS/Redwood field validation when PayrollDVO source evidence exists. |
| A name, code, ID, or source-system reference is unresolved or ambiguous | Do not place it in an HDL field or choose a match automatically. |
| The eligible-OPM lookup contract is unresolved | Do not claim a ValidPaymentMethod row is production-ready. |
| A mutation route other than HDL is proposed | Do not use the internal UI lookup resources to create, update, delete, migrate, extend, or adjust payroll data. |
| Preview or approval is absent or changed | Do not upload or submit the archive. |
| A live POST, import, loader, or other mutation fails or has an uncertain outcome | Do not retry without idempotency or fresh explicit approval after safe verification. |
| A loader archive fails | Do not resubmit the same failed archive automatically; correct it and use a new approved load. |
| Backend behavior is undocumented | Do not fabricate required flags, types, lengths, code lists, localized attributes, error payloads, retry behavior, or supported actions. |
| Sensitive data is present | Do not disclose or persist credentials, tokens, private keys, customer data, production-only sensitive values, or unredacted payloads. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PD.EXECUTION_GATE | decision | 6 | execution_gate | hdl_preparation_ready->PD.DONE_HDL_PREPARATION;validation_ready->PD.DONE_VALIDATION;guidance_ready->PD.DONE_GUIDANCE;blocked->PD.HANDLE_ERROR | PD.ENFORCE_DESIGN | stop | Validation, dependency, lookup, defaulting, and design checks completed |
| PD.HANDLE_ERROR | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | continue | A prior node reports invalid, blocked, unsupported, unauthorized, ambiguous, not-found, failed, or uncertain |
| PD.DONE_HDL_PREPARATION | terminal | 8 | terminal | none | PD.EXECUTION_GATE | continue | The HDL contract is validated for handoff to a separately authorized loader workflow; no Fusion write is authorized by this terminal |
| PD.DONE_VALIDATION | terminal | 9 | terminal | none | PD.EXECUTION_GATE | continue | The requested validation result is ready for return; no Fusion write occurred |
| PD.DONE_GUIDANCE | terminal | 10 | terminal | none | PD.EXECUTION_GATE | continue | Source-backed Payroll Definitions guidance is ready for return; no Fusion write occurred |
| RETURN_ISSUES | terminal | 11 | terminal | none | none | continue | Blocking, unsupported, or failure details are safely classified and disclosed |

## Sources

- Developer-provided PayrollDefinition-HDL.md, accessed 2026-08-13.
- Developer-provided PayrollDVO source, accessed 2026-08-14.
- Repository AGENTS.md error-handling and credential-safety directives, supplied with the authoring request.
- Oracle Fusion Cloud HCM, HCM Data Loader: https://docs.oracle.com/en/cloud/saas/human-resources/faihm/hcm-data-loader.html
