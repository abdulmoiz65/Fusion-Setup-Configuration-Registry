# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Duplicate/ambiguous type | Stop with name/set/cardinality |
| Conditional burden/capital option invalid | Stop and name parent/child dependency |
| Fusion returns JBO-27020 for BurdenAccountFlag | Stop before retry; explicitly populate BurdenAccountFlag using the documented default or supplied valid value |
| Separate-item create omits component choice or destination | Apply BurdenAccountFlag N and blank destinations; do not return needs_input for controls disabled in this mode. Nonnull serialization does not require a user decision |
| Downstream burden mapping or billing-design evidence absent | Record BP-031/BP-033 readiness_not_assessed as non-blocking recommendations; do not confuse them with missing CSV inputs or Oracle validation failures |
| Fusion returns PJF_PROJ_TYP_CAP_INV_GROUP | Stop before retry; reject EI combined with G; resolve and preserve the user's valid M or N choice rather than forcing N |
| Missing dynamic catalog, eligibility proof or mode meanings | State it has no data source where no offline source exists; record deferred_to_fusion with blocking=false, preserve supplied CSV-ready values, and continue normal preview/upload. Validate proven control representations without invented lookup meanings |
| Default capitalized-interest schedule supplied through CSV | Report missing exported destination; do not populate cost burden IndSchName |
| Work-type or task name confused with project names | Show exact CSV intent mapping and resolve canonical identities before serialization |
| In-use protected mutation | Preserve current value and explain inherited impact |
| Translation/category child collision | Reject exact child row; preserve others |
| User reports Classifications Add Row error | For a request with no class categories, keep the optional group omitted and use the declared FSM route. If assignments are requested, retain that scope and diagnose through the supported workflow; do not silently drop requested rows or claim that the UI error was reproduced or fixed |
| Package/import fails | Report target, checksum, member/row, Oracle message; no auto-retry |
| Initiation accepted | Return in_progress with the executor's initiation result; pillar project services persist the returned receipt. Stop without automatic status, log or export calls |
| Submission or receipt persistence is indeterminate | Preserve available identifiers and redacted diagnostics; stop without replay. Supported read/status or target-state recovery requires a later explicit recovery request |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity/date/field/group failure | Correct input |
| Authoring evidence gap | Missing offline dynamic lookup or supplemental eligibility | Non-blocking service validation deferral under PT-POL-001; do not claim the value was independently verified |
| Dependency readiness | Required CSV input or package/baseline missing, or a known dependency conflict | Complete actual inputs/artifacts or correct the proven conflict; missing offline dynamic sources are deferred |
| Protected mutation | In-use semantic restriction | Preserve current value |
| Unsupported | Delete/direct setup REST | Stop/use supported route |
| Approval blocker | Preview absent/changed/declined | Stop without import |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Resolver outcomes, non-blocking deferred fields labelled it has no data source where applicable, source types, canonical mappings, target, operation, type/set, use-state, groups, references, warnings |
| Preview | Before/after base fields, translation/category diffs, counts, checksum |
| Journal defaults | Identify any applied create Y/Y journal defaults and preserve explicit choices. Disclose SRC-DOC's caution that accounting raw cost and total burdened cost separately can account raw cost twice; downstream accounting review remains distinct from setup validation |
| Initiation result | Data Load In Progress using the selected loader's response format; returned receipt retained by pillar project services with target and approved artifact/checksum. Deferred fields remain unverified; do not equate accepted initiation with import completion |
| Explicitly requested status or results | Use the selected loader's status workflow and disclose observed counts/errors and deferred-field validation results when available; active or incomplete results remain pending. Status alone is not fresh-export verification |
| Explicitly requested setup verification | After successful load completion, compare a fresh same-task data export with the approved changes and preserved groups/children; retain target/checksum, export evidence, row counts and discrepancies before claiming verified completion |
| Sponsored without burdening | Disclose the UI warning rather than claiming unconditional rejection or permanently forcing burdening. For an unused type in the applicable UI, the first save warns about disabling burdening for Sponsored; Yes commits, No only hides the popup, and later saves can bypass that warning because its flag is already set. Cancel resets the warning flag and rolls back. FSCR approval remains separate. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous identity/reference | Do not choose first/partial match |
| In-use protection fails | Do not force semantic mutation |
| Direct REST/delete requested | Do not infer unsupported operation |
| Template/approval absent | Do not import |
| Deferred offline validation | Do not claim membership verified, invent lookup results, or block solely because no offline source exists |
| Failure | Do not retry automatically or claim target-state success |
| Accepted initiation without an explicit follow-up request | Do not poll, retrieve logs, query data sets/errors, export target state, or report verified completion |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.EXECUTION_GATE | decision | 8 | execution_gate | ready->PTYPE.RETURN_SUCCESS;not_ready->PTYPE.RETURN_ISSUES;declined->PTYPE.RETURN_REFUSAL | PTYPE.ENFORCE_DESIGN | stop | Return validation or require approved preview |
| PTYPE.RETURN_SUCCESS | terminal | 9 | terminal | none | PTYPE.EXECUTION_GATE | continue | Pre-upload checks complete with deferred fields disclosed; package approval is not proof of service validation or import success |
| PTYPE.RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Correctable issue |
| PTYPE.RETURN_REFUSAL | terminal | 11 | terminal | none | none | continue | Unsupported/protected/declined action |

## Evidence and Authorization Boundaries

See [Source Evidence Index](ora_reference_lookups.md#source-evidence-index): SRC-EO establishes BurdenAccountFlag as nonnull, SRC-EOIMPL establishes EI/G rejection and transferred-asset restrictions, and SRC-UI establishes the save-warning boundary. Historical error/lookup descriptions without retained receipts are authoring context, not newly executed tests. No previous user’s authorization is carried into another run. Disclose PT-POL-001 deferrals in the exact preview and apply the selected executor’s approval gates. Initiation and later requested status/verification are separate stages under core.data-loader's successful-initiation and Inspect data-load status or information contracts (SRC-FSCR). The task-rule graph ends at its pre-upload terminal; it does not authorize an automatic post-initiation operation.
