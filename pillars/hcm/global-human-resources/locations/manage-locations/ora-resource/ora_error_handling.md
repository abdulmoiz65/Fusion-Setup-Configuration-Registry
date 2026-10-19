# Manage Locations Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| LOC-01 | The locationsV2 REST response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| LOC-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| LOC-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| LOC-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| LOC-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| LOC-03 | Create finds an exact existing LocationCode | Input validation | Stop the duplicate create; an existing LocationName is permitted |
| LOC-04 | Country does not resolve exactly or a mandatory MAIN-address value is missing | Input validation | Stop before preview and request only the corrected Country or missing labelled values |
| LOC-04A | The country layout is missing, incomplete, or cannot map a mandatory field | Catalog mismatch | Stop before preview and restore the current address contract; do not guess a field |
| LOC-05 | LocationOtherAddress is used for MAIN or an unmodified child or EFF row is populated | Input validation | Keep only the base MAIN address and explicitly modified additional sections |
| LOC-06 | The reference-data set is absent, unresolved, or ambiguous | Input validation | Stop before workbook authoring and request one exact set |
| LOC-07 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| LOC-09 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| LOC-09A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| LOC-10 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| LOC-10A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected locations |
| LOC-10B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| LOC-10C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| LOC-11 | An EFF FLEX value is a placeholder, `Global Data Elements` without that resolved context, or differs from its row category | Input validation | Stop before preview; resolve the exact current context, make the FLEX and category values equal, and regenerate |
| LOC-12 | A generated or supplied DAT line exceeds 4000 characters | File validation | Stop before upload; omit only columns blank in every data row, rebuild, and require every line to pass the limit |
| LOC-13 | Loader TimezoneName contains a time-zone code, long/short display, REST display value, or any value other than the enabled LOV `Name` | Input validation | Stop before preview; match the MAIN-address TimezoneCode to one enabled LOV row and write only its exact Name |
| LOC-14 | ShipToSiteFlag and ship-to reference fields violate their conditional contract | Input validation | Stop before preview; omit all references for Y, or provide exactly one resolved ID or complete code-and-set pair for N |
| LOC-15 | An edit or delete row lacks the live surrogate ID for its edited object | Input validation | Stop before preview; follow child links, resolve the exact `LocationId`, `LocAddressUsageId`, `LocationExtraInfoId`, or `LocationLegId`, and rebuild |
| LOC-16 | A supplied base, child, or dynamically resolved EFF value violates current live type, maximum length, precision/scale, allowed value/domain, or reference metadata | Input validation | Stop before preview; re-read the current attribute/context metadata, correct the value, and rebuild without hardcoding an EFF segment contract |
| LOC-17 | A date-effective edit copies/defaults an ActionReasonCode without explicit user input, or a supplied reason is expired or incompatible with the update | Input validation | Stop before preview; omit the optional field, or resolve the exact user-supplied update reason independently and rebuild |
| LOC-18 | A Location delete uses ZAP/root DELETE, targets the first history row, lacks complete LocationHistoryDef evidence, or has a MERGE range not derived from the predecessor start and selected end | Input validation | Stop before preview; refresh every history page, derive the bounded MERGE range, and rebuild with exactly one purge-future-changes directive |
| LOC-19 | A date-effective Location delete omits `LocationCode`, `SetCode`, or `LocationId`, including a surrogate-only root MERGE that the runtime Location translation entity rejects | Input validation | Stop before preview; re-read the current root Location, resolve its complete `LocationId` + `SetCode` + `LocationCode` tuple, rebuild the single root MERGE, and revalidate the immutable archive |
| LOC-20 | A request uses ZAP or asks to physically delete the logical Location | Unsupported | Return `UNSUPPORTED`; explain that Location supports only date-effective deletion of an eligible non-first split, and stop before lookup, source generation, preview, approval, upload, or initiation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, MAIN address, section scope, set, loader key, EFF context, time-zone value, or ship-to reference is invalid | Correct the input or source scope and restart resolution |
| File validation | The generated DAT shape is malformed or any line exceeds Fusion's limit | Rebuild through Core Data Loader and repeat validation before preview |
| Catalog mismatch | A required REST response is missing or Core Data Loader reports unavailable or stale metadata | Correct the reported contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | Core Data Loader reports that the reviewed source cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile Location state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Address or section failure | Country and missing MAIN-address labels, or the incorrectly populated child or EFF section, without exposing internal IDs |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Location or address rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key, set, address field, object surrogate ID, or target is unresolved | Do not infer or invent a value |
| A MAIN address is being edited | Do not use LocationOtherAddress; keep the change on the root Location row and retain LocAddressUsageId only in resolution evidence |
| A time-zone value fails | Do not cycle through code, long name, short name, or REST display guesses; repeat the exact enabled-LOV-Name resolution and obtain new approval for a rebuilt artifact |
| An EFF context fails | Do not substitute `Global Data Elements`; use it only if it is the exact resolved row context |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOC.ROUTE | decision | 8 | execution_gate | read->LOC.DONE;create_or_edit_or_delete_ready->LOC.LOADER_READY;mutation_blocked->LOC.ERROR | LOC.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| LOC.ERROR | step | 9 | error_handler | stopped->LOC.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| LOC.DONE | terminal | 10 | terminal | none | LOC.ROUTE | continue | Read completed |
| LOC.LOADER_READY | terminal | 11 | terminal | none | LOC.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| LOC.BLOCKED | terminal | 12 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
