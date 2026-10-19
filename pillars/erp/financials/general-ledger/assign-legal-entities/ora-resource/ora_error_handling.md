# Assign Legal Entities Error Handling

The source analysis performed read-only exports and five read-only HTTP 200 checks. No import was executed. A failed live request stops that run before retry, documentation fallback, package reuse, approval, or import handoff. A prior run that returned no ProcessId remains audit history only and is not current runtime evidence.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `FDOS Decision!A1:C15`, `User Inputs!A1:F13`, `Validations!A1:H20`, and `TBD Register!A1:F10`.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Ledger reference is missing | Ask only for exact ledger Name or numeric LedgerId |
| Ledger lookup returns zero or many | Show sanitized cardinality and stop; never fuzzy-match or select the first row |
| Supplied ledger is SECONDARY | Report its category and require the owning primary ledger; never silently re-parent |
| Assign Legal Entities export is requested before ledger existence, PRIMARY category, and L type are proven | Stop before export submission; complete resolve_primary_ledger first |
| Export task or scope metadata is missing or disagrees with the validated ledger | Reject the package and reacquire GL_ASSIGN_LEGAL_ENTITIES with PRIMARY_LEDGER_ID equal to the resolved LedgerId |
| LegalEntityIdentifier is missing, over 30 characters, zero-match, or many-match | Identify the affected mapping and stop before package authoring |
| Legal entity is end-dated | Disclose EffectiveTo and reject the mapping |
| Legal entity has null EffectiveFrom | Preserve null and continue when all other eligibility checks pass; do not invent a start date |
| Legal entity has populated EffectiveFrom after the run date | Disclose EffectiveFrom and reject the not-yet-effective mapping until that date |
| Exact populated identifier or legacy canonical ObjectName is already assigned | Show the match type and every current parent Name, then reject the duplicate mapping |
| Legacy row has both LegalEntityIdentifier and ObjectName blank | Show the unattributable-row count and reject duplicate proof until a complete attributable export is available |
| RetEarnCcidSegments is blank, missing, or ambiguous for the primary or any associated secondary | List every failing PL or SL, block, and ask the user to complete 'Specify Ledger Options' for PL and all its associated SLs and retry |
| TimeZoneDefaultLeFlag or TaxDefaultLeFlag is populated on a new row | Reject the populated override and regenerate the row with a true blank |
| Audit fields are populated on a new row or any existing value changes | Reject the delta; leave new-row audit fields blank and restore the exact exported values of every existing row |
| Package is stale, wrong-environment, wrong-release, incomplete, unsafe, unscoped, wrong-primary-scoped, or ambiguous | Stop with package source, task, environment, release, scope, member, and header diagnostics; never splice packages |
| Proposed row count differs from requested mapping count | Show requested and generated counts and rebuild the delta |
| Any nonowning file or unrelated row changes | Show the semantic diff and reject the package until only direct assignment rows remain |
| A balancing-segment child row is proposed | Reject it and route the downstream setup separately |
| Read-only REST call fails | Classify the actual authentication, authorization, transport, client, or Fusion API failure; do not report value not found |
| A prior scoped-export POST failed without a ProcessId under an older or corrected request contract | Preserve its diagnostic as audit history, but do not use it to block or replace current evidence. After the user explicitly requests a new test run and the FDoS contract has been corrected and validated, that new run may submit exactly one fresh request using the current contract |
| The current run's scoped-export POST fails | Preserve the sanitized response and stop the current run; do not infer another payload or submit a second POST in that run |
| Preview has unresolved validation, lookup, dependency, or design blockers | Stop and list every blocker with its exact corrective action; do not request import approval |
| User changes inputs, source package, target environment, defaults, or rows after preview | Invalidate preview and approval and regenerate the immutable artifact |
| Import fails after a separately approved future execution | Stop before retry, preserve sanitized failure evidence, and require operator review; never replay an uncertain mutation automatically |
| Post-import re-export cannot prove the mapping | Report an uncertain outcome and stop before another import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required business input, domain, length, cardinality, or fixed direct-row contract is invalid | Correct the affected input or proposed row and rerun from validation |
| Catalog mismatch | Task identity, expected export member, header, or hierarchy context does not match current catalog or package evidence | Refresh the catalog or task export and re-resolve the exact task |
| Authentication or authorization | Read-only REST identity cannot be obtained with the approved session or privilege | Restore approved access and rerun the read-only resolver; do not infer a value |
| Transport or environment | Target identity, network, timeout, package path, or environment binding fails | Correct the environment or transport condition and restart from fresh evidence |
| Fusion API | Fusion returns a non-success response or malformed business result | Preserve sanitized response evidence and stop; do not reinterpret as no match |
| Approval blocker | Exact environment, immutable artifact, semantic diff, explicit approval, or complete readiness is missing | Resolve the gate and regenerate preview before any import |
| Process failed or uncertain | A separately approved import fails or cannot be verified | Stop before retry and reconcile through read-only export evidence |
| Artifact persistence | Package, diff, evidence, or diagnostic cannot be safely preserved | Stop without importing; correct the safe destination and repeat preview |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Identity resolution | Exact task code and name, target environment, sanitized ledger reference, resolved category and type, legal-entity identifier, canonical Name, effectivity, and match counts |
| Package readiness | Environment, release, task, package source receipt, PRIMARY_LEDGER_ID scope attribute and exact value, member inventory, headers, observed row counts, fingerprint, and freshness decision |
| Primary and secondary retained-earnings readiness | Primary Name and every associated secondary Name, relationship type, RelationshipEnabledFlag, per-ledger retained-earnings result, failing-ledger list, and overall readiness |
| Legal-entity eligibility | Exact identifier and canonical Name match count, preserved EffectiveFrom including null, EffectiveTo, and effective-date result |
| Duplicate assessment | Validated primary Name, populated exact-identifier match count, legacy exact-canonical-name match count, legacy blank-ID count, unattributable-row count, and scoped proof completeness |
| Delta preview | Requested mapping count, exact added direct rows, field-by-field values, changed member list, preserved member list, unrelated-row diff, and artifact fingerprint |
| Readiness | Every failed or ambiguous requirement, owning rule, failing identities, safe interim behavior, and exact corrective action |
| Approval | Exact environment, operation, immutable import artifact, semantic business effect, preview fingerprint, and the fact that approval applies only to the declared Data Loader step |
| Verification | Re-export receipt, exact new mapping evidence, downstream balancing-segment report, preserved existing values, and any uncertain outcome |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| REST returned a ledger or legal entity | Do not treat HTTP 200 or one identity match as proof of scoped assignment absence, relationship readiness, retained earnings, or package correctness |
| Ledger is secondary | Do not silently substitute the owning primary |
| Ledger REST validation has not passed | Do not submit, select, or inspect an Assign Legal Entities export as runtime evidence |
| Scoped export is acquired | Do not accept task metadata other than GL_ASSIGN_LEGAL_ENTITIES, a scope attribute other than PRIMARY_LEDGER_ID, a scope value other than the resolved LedgerId, or more than one parent configuration |
| Legal-entity Name exists in an old row | Do not copy it instead of deriving the current canonical Name from the exact identifier; use that derived Name only for the exact legacy duplicate comparison |
| Blank legacy identifiers exist | Do not ignore them; compare each nonblank ObjectName exactly to the derived current canonical Name and block when it matches |
| RetEarnCcidSegments is blank for any associated ledger | Do not waive the blocker because the relationship is disabled or CONFIRMED |
| Nullable flag is blank | Do not infer Y or N from sample frequencies or existing rows |
| Nullable flag is explicitly supplied | Do not populate it in a new row; this task keeps both flags null |
| Direct mapping is requested | Do not author GL_LEDGER_SEG_VAL_ASSIGNMENT.csv, ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv, conversion-rule rows, or any other nonowning file |
| Resource graph reaches preview gate | Do not execute a Fusion write from this resource; hand the reviewed artifact to the declared Data Loader workflow only after complete readiness and explicit step-local approval |
| Import outcome is failed or uncertain | Do not retry automatically, reuse stale approval, or create another package before read-only reconciliation |
| An older scoped-export run has a no-ProcessId failure diagnostic | Do not treat that diagnostic as the result of a new explicitly requested run after the request contract changed; the new run owns one current create attempt |

## Resolved Authoring Decisions

| Decision | Runtime Contract |
|---|---|
| EffectiveFrom | Preserve null; when populated, require a valid value on or before the run date |
| Retained earnings | Require populated RetEarnCcidSegments for the current PL and every associated SL, including disabled relationships; otherwise block with the Specify Ledger Options guidance |
| Nullable default flags | Keep TimeZoneDefaultLeFlag and TaxDefaultLeFlag blank on new rows; do not infer or accept populated overrides |
| Audit ownership | Keep audit fields blank on new rows and preserve exact existing-row values |
| Legacy duplicate proof | In the complete exported direct-row file, compare exact populated identifiers and compare the derived current canonical Name to ObjectName on blank-identifier rows; any match blocks, and zero matches proves absence when no row has both identity fields blank |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.PREVIEW_GATE | decision | 80 | execution_gate | approved->ALE.READY_FOR_IMPORT;blocked->RETURN_ISSUES | ALE.ENFORCE_DESIGN | stop | Confirm exact target environment, validated REST primary, fresh exact-scoped Assign package, complete dependency and retained-earnings readiness, smallest semantic delta, immutable artifact fingerprint, and explicit approval bound to the declared Data Loader import handoff; do not execute the import here. |
| ALE.READY_FOR_IMPORT | terminal | 90 | terminal | none | ALE.PREVIEW_GATE | stop | The task is fully ready for the separately declared core.data-loader import step and all normal live-operation gates still apply. |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Any validation, lookup, scoped-export, dependency, defaulting, design, preview, approval, import, or verification blocker requires a safe stop. |
