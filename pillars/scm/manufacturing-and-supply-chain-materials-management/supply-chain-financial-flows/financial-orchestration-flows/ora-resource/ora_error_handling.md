# Financial Orchestration Flows diagnostics

## Error Situations

| Situation | What Should Happen |
|---|---|
| Invalid or missing input | Return exact field, expected value and safe next action; no lookups for unsupported operations |
| Fusion rejects an Agreement create for a name or Priority conflict | Report the exact Fusion/Data Loader error and affected Agreement row; do not substitute another name or Priority or automatically retry. No separate pre-create uniqueness lookup is required. |
| LOV zero or multiple matches | Return candidates or missing selection; do not choose a fuzzy match |
| Fusion rejects a requested Agreement Status transition | Report the exact Data Loader/Fusion diagnostic and selected Agreement version; do not substitute another LOV value or retry the same correction automatically |
| Current-date query finds no version | Do not interpret it as permission to recreate or change effective dates |
| FOS_FOSTP_AGR_PTR_REQ during parent correction | Inspect whether the prepared correction included the resolved Priority and CORRECTION context; the Priority REST accessor sets AgreementSource=REST. Do not infer that a primary route must be added or that Status should change. Change Status only when explicitly requested and resolved through the status LOV; do not bypass the loader. If Priority was omitted, prepare a newly validated correction with the current Priority and obtain the applicable approval; if already included, investigate request/backend differences rather than blindly retrying |
| Unsupported RestAction Insert | The loader action is PATCH for dated Insert. Do not copy the UI JSON business value Insert into the DAT RestAction column; prepare and validate a new artifact under the documented Insert contract |
| There are no changes to save during Insert | Compare requested business values with the selected version. Ask for an intentional changed Description; never invent a change or retry unchanged bytes |
| Missing packaged contract or outside-source fallback | Report the missing lookup or mapping and stop the affected operation; do not reconstruct runtime behavior from a developer checkout or previous conversation |
| Schema or adapter mismatch | Stop before upload with missing contract evidence; do not edit registration automatically |
| Authentication or transport failure | Use shared client policy; redact credentials, cache contents and headers |
| Import timeout or uncertain result | Preserve requestId, last status and submitted artifact reference; check status/readback before another mutation |
| Partial or failed load | Report loaded/failed counts and sanitized row errors; preserve successful rows; no whole-file replay |
| ParentEffectiveStartDate or ParentEffectiveEndDate rejects an ISO date as nonnumeric | Stop; preserve the failed request ID, content ID and row diagnostic. Refresh the selected environment's FTR registration and inspect the parent-date foreign-key derivations. When both derive from AgreementId and the nested FTR URL uses them, rebuild without adding helper columns: leave any helper column already in the fresh template blank. Revalidate and obtain the applicable approval. Do not try another date format, substitute a number, change the registration datatype or replay the failed archive |
| ZIP rejects an FTR correction because no top-level business object is recognized | Stop before upload and inspect DAT section names. For a standalone existing-FTR correction, rebuild the artifact with only its FinancialTradeRelation METADATA section and selected MERGE row; remove PTR and Agreement sections. Preserve the resolved parent values in the FTR row only where the fresh FTR template requires them. Do not add an empty Agreement row or submit a multi-section child-only archive |
| Successful job but readback mismatch | Report verification failure; do not claim requested change succeeded |
| PTR deletion rejected | Do not delete children first, change the Agreement or blindly retry. Preserve diagnostics and check the same parent collections before any new mutation |
| PTR deletion completion | Require target PTR absent, Agreement header unchanged and sibling PTRs retained. Compare descendant behavior with preview; an FTR collection 404 alone does not prove physical deletion |
| Agreement correction completion | Verify selected composite identity, requested changes, requested Status when changed, and preserved Status and Priority when not requested to change |
| Procurement Agreement create completion | Read back the exact created Agreement. If an ownership event was supplied, verify DropshipForwardOwnershipChangeEventId equals the resolved EventDefinitionId; if it was omitted, report the saved value without claiming that Fusion kept it blank |
| Insert completion | Use resolve_flow_agreement_version at old/new starts: old end must be new start minus one day with original Description; new interval has changed Description, preserved end/Priority/status and same AgreementId. Do not replay stale identity dates |
| Child create/correction completion | Read selected Agreement/PTR/FTR collections and verify requested values and ordered linkage. Schema success alone does not prove nested creation |
| Shipment Primary Route reports an invalid Selling Trade Organization | Confirm the source has no Selling Trade Organization, FromTradeOrganizationId or ToTradeOrganizationId on PrimaryTradeRelation, then validate a new archive. Do not add, default or resolve a Primary Route trade organization as a workaround; assess FTR trade organizations under their separate explicit, buying-default and later-selling inheritance rules. |
| Charge Account is missing or invalid | Resolve the supplied ChargeAccount display combination in the FTR buying ledger and require one eligible ChargeAccountCodeCombinationId. A matching account in the selling ledger can have a different ID. Rebuild the source with the buying ledger's ID only; do not send ChargeAccount as fallback or retry a display value. |
| Internal Transfer Financial Routes are invalid | Check that the first FTR selling organization and last FTR buying organization are blank. For a multi-FTR PTR, verify every later selling organization and every earlier buying organization against its side-BU default. A single-FTR PTR has both fields blank. Confirm the failed load left no route before rebuilding and seeking new approval; do not replay the same archive. |
| Procurement Financial Routes are invalid | Check that every FTR has a selling organization eligible in its own selling BU. Leave the last FTR buying organization blank, including for a single-FTR PTR; populate the buying organization on each earlier FTR in a multi-FTR PTR. Confirm the failed load left no route before rebuilding and seeking new approval; do not replay the same archive. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| PTR deletion | Selected Agreement/PTR and complete FTR inventory; verified or uncertain descendant handling |
| LOV resolution | Selected labels and identifiers in correct side/date context; unresolved or ambiguous supplied values |
| Rule handoff | Validated rule results or blockers, not a claim of completed Fusion mutation |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Execution | No direct Fusion REST or UI mutation; use core.data-loader |
| Uncertain or partial result | No automatic replay or deletion of children to bypass a rejection |
| Missing lookup contract | No guessed mapping, silent field omission or dependency on prior conversation/developer checkout |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOF.CHECK_HANDOFF | step | 390 | execution_gate | success->FOF.RETURN_RULE_RESULTS;failure->FOF.RETURN_ISSUES | FOF.CHECK_DESIGN | stop | Return applicable validation results to core.data-loader; do not perform submission from this node |
| FOF.RETURN_ISSUES | terminal | 400 | terminal | none | none | stop | Return blockers using Error Situations; no mutation |
| FOF.RETURN_RULE_RESULTS | terminal | 410 | terminal | none | FOF.CHECK_HANDOFF | stop | Return validated rule results; live result verification uses the documented readback contracts |
