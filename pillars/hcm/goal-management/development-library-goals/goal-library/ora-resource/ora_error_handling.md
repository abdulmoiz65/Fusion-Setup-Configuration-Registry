# Development Library Goal Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Current variant fields or operation unavailable | Stop before payload mapping and return public-vs-current metadata mismatch evidence |
| Canonical create payload omits or nulls GoalName, TypeCode, StatusCode, or Visible | Return `MISSING_KEY_CREATE_FIELD`; do not preview or POST. A displayed default absent from JSON is not applied. |
| Create returns HTTP 201 but fresh exact read has null or mismatched lifecycle, audience, variant, name, or approved scope | Return `INVALID_CREATED_STATE`, retain the created identity, block Run Book completion, and do not retry or create a replacement name automatically. |
| Exact duplicate row has null StatusCode or Visible | Return `INVALID_EXISTING_LIBRARY_GOAL_STATE`; require an explicit repair or replacement decision instead of inventing a suffix. |
| Identity or code is ambiguous | Stop and request exact disambiguation |
| Child collection read is incomplete | Stop update; never reconstruct missing children from chat context |
| Parent or child validation fails | Confirm no parent, measurement, task, target outcome, or DFF change persisted; re-read complete state before reporting the error |
| Concurrency conflict | Re-read the complete parent and affected children, disclose the winning state, and require a new preview rather than retrying the stale mutation |
| Translation runtime root or composite identity is unavailable | Return `CONTRACT_TBD` identifying the required current OpenAPI resource (`libGoalTranslations` or `libGoalTaskTranslations`); do not fall back to a VBCS alias, infer a path, or synthesize a translation key |
| Translation update is rejected or has a stale concurrency value | Re-read the exact returned translation item, disclose the winning state, and require a new preview; never retry or overwrite automatically |
| Decimal-weight policy provider is unavailable | Return `PROVIDER_SKILL_UNAVAILABLE` for `core.fusion-api.apps-common.profile-options` and block a fractional-weight mutation; do not call a profile endpoint or modify the profile option |
| Timeout or ambiguous mutation | Return UNKNOWN_AFTER_SUBMISSION and reconcile by safe read |
| HDL is selected without a DAT/ZIP source | Select `hdl_generate`; resolve and validate the Development Library Goal rows, then have Core Data Loader generate the current-metadata source and immutable ZIP |
| DAT/ZIP is corrupt, unsafe, malformed, missing mandatory data, or has an unsupported component | Preserve and reject it. If business intent is complete and unambiguous, rebuild a separate generated source through Core; otherwise return file, component, line when available, validation code, and corrective action. No issue is waivable. |
| Measurement has no relationship to a supplied library goal | Return `MISSING_MEASUREMENT_RELATIONSHIP`; do not load orphan measurement content |
| Translation parent is missing, language is disabled/duplicated, or language equals the base language | Return `MISSING_TRANSLATION_PARENT`, `LANGUAGE_NOT_ENABLED`, `DUPLICATE_TRANSLATION_LANGUAGE`, or `BASE_LANGUAGE_TRANSLATION`; do not load the translation |
| A target-required business value remains unresolved after safe enrichment | Return `MISSING_MANDATORY_DATA`; do not invent the value or load the original source |
| Performance or mixed discriminator is present | Return `VARIANT_MISMATCH`; require a separate Performance archive |
| One approval is requested for multiple updates but batch is not explicitly supported | Keep the single approval group and build ordered item PATCH requests from each current operation contract. If PATCH is also unavailable, return a contract blocker; do not probe or invent a batch root. |
| Parent execution control is missing, stale, or identifies another Run Book task | Return `RUNBOOK_SEQUENCE_BLOCKED`; do not perform reads intended to prepare a later mutation or submit a write. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing variant, identity, or explicit child intent | Correct intake |
| Contract blocker | Current metadata does not support requested variant/operation | Obtain authoritative evidence |
| Fusion API | Supported request is rejected | Capture sanitized diagnostics and revalidate |
| Unknown after submission | Outcome cannot be proven | Read and reconcile; never replay automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Environment, operation, variant, target, full child diff, usage, mapping report, and fingerprint |
| Failure | Stage, class, safe object identity, message, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Current metadata does not verify requested development fields/operation | No payload or live write |
| Omitted child state is unreadable | No update |
| References are not proven absent | No delete |
| Ambiguous submission | No automatic retry |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.CSV_READY | terminal | 250 | terminal | none | GOAL_LIBRARY.VALIDATE | stop | CSV route is ready |
| GOAL_LIBRARY.HDL_READY | terminal | 255 | terminal | none | GOAL_LIBRARY.HDL_VALIDATE | stop | Error-free Development HDL task preflight is ready for `core.data-loader` preview |
| GOAL_LIBRARY.NO_CHANGE | terminal | 260 | terminal | none | GOAL_LIBRARY.WRITE_ROUTE | stop | Fresh values already match |
| GOAL_LIBRARY.DONE_READ | terminal | 270 | terminal | none | GOAL_LIBRARY.READ | stop | Read completed |
| GOAL_LIBRARY.DONE_SEARCH | terminal | 271 | terminal | none | GOAL_LIBRARY.SEARCH | stop | Bounded variant search completed, including an empty result |
| GOAL_LIBRARY.DONE_CREATED | terminal | 280 | terminal | none | GOAL_LIBRARY.CREATE_VERIFY | stop | Inactive create and key-field audience state verified |
| GOAL_LIBRARY.DONE_UPDATED | terminal | 290 | terminal | none | GOAL_LIBRARY.UPDATE | stop | Update verified without forced activation |
| GOAL_LIBRARY.DONE_ACTIVATED | terminal | 300 | terminal | none | GOAL_LIBRARY.ACTIVATE | stop | Activation verified |
| GOAL_LIBRARY.DONE_INACTIVATED | terminal | 310 | terminal | none | GOAL_LIBRARY.INACTIVATE | stop | Inactivation verified |
| GOAL_LIBRARY.DONE_DELETED | terminal | 320 | terminal | none | GOAL_LIBRARY.DELETE | stop | Guarded delete verified |
| GOAL_LIBRARY.DONE_TRANSLATION_READ | terminal | 321 | terminal | none | GOAL_LIBRARY.TRANSLATION_SEARCH | stop | Translation read completed |
| GOAL_LIBRARY.DONE_DECIMAL_POLICY_READ | terminal | 322 | terminal | none | GOAL_LIBRARY.DECIMAL_POLICY_READ | stop | Decimal-weight policy read completed |
| GOAL_LIBRARY.DONE_TRANSLATION_UPDATED | terminal | 323 | terminal | none | GOAL_LIBRARY.TRANSLATION_UPDATE | stop | Translation update verified |
| GOAL_LIBRARY.UNKNOWN | terminal | 330 | terminal | none | none | stop | A submitted mutation has an ambiguous outcome |
| GOAL_LIBRARY.BLOCKED | terminal | 340 | terminal | none | none | stop | A variant, dependency, approval, or safety gate blocks the request |
