# Assign Legal Entities Reference Lookups

Ledger validation must complete through the read-only ledger REST resolver before an Assign Legal Entities export is submitted. The resulting primary-ledger-scoped export is authoritative for the current parent configuration, its secondary-ledger relationships, already assigned legal entities, retained-earnings readiness, and the package delta. Live legal-entity REST resolution supplies the candidate identifier, current canonical Name, and effectivity that are not present when the candidate is not yet assigned.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `REST Evidence!A1:G9`, `Export Files!A1:F21`, `Oracle Sources!A1:D19`, and `Observed Evidence!A1:C15`; and the user-supplied scoped export `Assign Legal Entities_20260818_072052_893.zip`.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_primary_configuration_exact | After the scoped Assign package is selected | Normalized REST Name plus complete GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv from that package | Require exactly one GL_LEDGER.csv data row whose Name equals the normalized REST Name and exactly one ORA_GL_PRIMARY_LEDGER_CONFIG.csv data row whose Name equals the same value; require every exported parent reference used by downstream checks to equal that Name | Exact primary Name, one-row configuration evidence, and scope-agreement result | Zero or many rows, a Name disagreement, or any extra parent configuration blocks; never free-type or silently substitute another parent |
| check_existing_direct_assignment | After the complete scoped Assign package is selected and the current canonical legal-entity Name resolves | Validated primary Name, exact LegalEntityIdentifier, canonical current ObjectName, and all ORA_GL_JOURNAL_CONFIG_DETAIL.csv rows in the scoped export | First require every direct row to belong to the validated primary; filter rows whose ObjectTypeCode is LEGAL_ENTITY and SetupStepCode is NONE; compare populated LegalEntityIdentifier exactly and compare ObjectName exactly on legacy blank-identifier rows; any match is an existing assignment in this scoped configuration; no match proves no scoped duplicate only when every legacy blank-identifier row has a nonblank ObjectName | Populated-identifier match count, legacy canonical-name match count, matching primary Name, legacy blank-identifier row count, unattributable legacy-row count, and scoped duplicate-proof status | Any exact identifier or canonical-name match blocks as a duplicate; a row outside the validated primary, a legacy row with both identity fields blank, missing columns, incomplete scoped export, or ambiguous package selection blocks proof; otherwise zero matches proves no duplicate in the validated primary configuration |
| check_retained_earnings_readiness | After the exact primary export parent and all associated SECONDARY relationships are enumerated | Exact primary Name, ORA_GL_LEDGER_RELATIONSHIP.csv rows where GL_LEDGER.Name equals the primary and TargetLedgerCategoryCode is SECONDARY, GL_PRIMARY_LEDGER.csv, GL_SECONDARY_LEDGER.csv, and RetEarnCcidSegments | Parse each CSV with an RFC 4180-compatible CSV parser so quoted multiline segment values remain one field and one row. Require exactly one primary ledger row by exact Name in GL_PRIMARY_LEDGER.csv; take every associated secondary from TargetLedgerName, including rows whose RelationshipEnabledFlag is N, require exactly one exact Name row for each in GL_SECONDARY_LEDGER.csv, and require trimmed RetEarnCcidSegments to be nonblank for the primary and every associated secondary | Primary Name and retained-earnings result, complete associated-secondary list, per-secondary Name and retained-earnings result, relationship enabled evidence, failing-ledger list, and overall readiness | A missing or ambiguous ledger row or any truly blank RetEarnCcidSegments blocks; a quoted multiline value is populated and must not be classified from a physical line fragment; list every failing PL or SL and ask the user to complete 'Specify Ledger Options' for PL and all its associated SLs and retry |
| report_balancing_segment_state | After the proposed legal-entity mapping delta is formed and again after import re-export | Resolved ledger, resolved legal entities, and ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv | Report existing company or balancing-segment child rows for the selected mapping; this task never authors them | Existing balancing-segment evidence and downstream setup-needed indicator | Missing child rows are reported as downstream setup state, not filled by this task |
| verify_assignment_delta | Before preview and after any import re-export | Requested mapping count, scoped baseline package, and proposed or re-exported package | Require one new direct LEGAL_ENTITY and NONE row per requested mapping in ORA_GL_JOURNAL_CONFIG_DETAIL.csv; require no authored change in the other nine exported CSV files or ASM_SETUP_CSV_METADATA.xml and no extra direct row | Added-row count, affected identifiers, affected parent Name, changed-member list, preserved-member list, scope-metadata preservation, and semantic diff | A missing or extra row, changed nonowning file, changed metadata or scope, changed unrelated row, or ambiguous diff blocks |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_primary_ledger | After local ledger-reference shape validation | Exact ledger Name or numeric LedgerId | /fscmRestApi/resources/11.13.18.05/ledgersLOV with encoded exact q by Name plus onlyData=true and limit=10, or /fscmRestApi/resources/11.13.18.05/ledgersLOV/{LedgerId} for an item GET. Do not send a fields query parameter | Response fields to extract: LedgerId, Name, LedgerCategoryCode, LedgerTypeCode, CurrencyCode, ChartOfAccountsId, CalendarName | Require exactly one exact ledger with LedgerCategoryCode PRIMARY and LedgerTypeCode L; a SECONDARY match is disclosed and rejected for this direct-assignment parent | LedgerId for the PRIMARY_LEDGER_ID export scope, normalized Name for parent validation, LedgerCategoryCode, LedgerTypeCode, currency, chart, and calendar evidence | Zero or many exact matches block; a SECONDARY or non-L row blocks and requires the owning primary; HTTP or authorization failure is not a no-match result |
| resolve_legal_entity_exact_identifier | After local identifier shape validation | Exact LegalEntityIdentifier | /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV with encoded exact q for LegalEntityIdentifier plus onlyData=true and limit=10. Do not send a fields query parameter | Response fields to extract: LegalEntityId, Name, LegalEntityIdentifier, EffectiveFrom, EffectiveTo | Require exactly one exact identifier; derive the canonical current Name and effectivity without copying a stale assignment-row name; preserve null EffectiveFrom exactly as returned | LegalEntityId, LegalEntityIdentifier, ObjectName from Name, EffectiveFrom including intentional null, and EffectiveTo | Zero or many exact matches, an end date before the run date, malformed populated effectivity, or an HTTP or authorization failure blocks; null EffectiveFrom does not block |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact ledger Name request | Query ledgersLOV by the exact supplied Name with onlyData=true and limit=10, omit the fields query parameter, require one PRIMARY ledger of type L, and retain its returned LedgerId for the scoped export |
| Exact legal-entity identifier request | Query legalEntitiesLOV with onlyData=true and limit=10, omit the fields query parameter, encode or bind the exact value without changing case, punctuation, or internal whitespace, and count the full returned set before classifying cardinality |
| Requested Fields table values | Treat them only as response fields to extract and validate after a successful response; never translate this column into a fields URL parameter for these LOV endpoints |
| Export CSV parsing | Use an RFC 4180-compatible parser for all exported CSV members; never split or classify rows from physical lines because quoted values such as RetEarnCcidSegments can contain embedded newlines |
| Numeric LedgerId request | Use the item resource and still require PRIMARY and L; an HTTP 200 does not waive category or task-parent rules |
| Zero, one, or many matches | Follow the resolver-specific cardinality; never fuzzy-match, select the first result, or turn ambiguity into success |
| REST and export disagreement | Stop and disclose both non-sensitive identities; do not prefer stale export data or silently rewrite current REST identity |
| Read-only REST success | Treat the response only as the fields it actually returns; after PRIMARY and L are proven, use the returned LedgerId—not the ledger Name—as the PRIMARY_LEDGER_ID export scope value; legal-entity REST success supplies candidate identity and effectivity but does not prove scoped assignment absence, retained earnings, or final package delta |
| Local package disagreement | Stop with environment, release, task, member, header, row, and identity evidence; never splice packages |
| Sensitive response data | Retain only sanitized resolver evidence and exact non-sensitive values required by this task; never persist credentials or tokens |

## Read-Only Evidence Snapshot

The following 2026-08-13 observations support the contracts but are not runtime constants:

- `ledgersLOV` exact Name returned HTTP 200 and one row for LedgerId 1225, Vision Foods - USA Ledger, PRIMARY, type L.
- `ledgersLOV/1225` returned HTTP 200 for the same primary identity.
- `legalEntitiesLOV` exact identifier US103 returned HTTP 200 and one row for LegalEntityId 100010823925051, Vision Foods USA Ltd.
- A secondary-ledger query returned HTTP 200 and one row for LedgerId 1227 with category SECONDARY; it did not expose its owning primary, relationship status, enabled flag, or retained earnings.
- The actual ORA_GL_JOURNAL_CONFIG_DETAIL.csv export contained 898 direct rows: 843 with populated LegalEntityIdentifier and 55 legacy rows with blank identifiers. All 55 legacy rows had nonblank, distinct ObjectName values; none had both identity fields blank. One legacy ObjectName, ZHRX-KW-Regression-Legal Entity, exactly matched a populated-identifier row under another parent, demonstrating why the canonical-name legacy check must block an existing assignment.
- The user-supplied 2026-08-18 scoped export declared ObjectShortName GL_ASSIGN_LEGAL_ENTITIES and PRIMARY_LEDGER_ID scope value Vision Operations (USA) in ASM_SETUP_CSV_METADATA.xml. It contained one GL_LEDGER.csv row and one ORA_GL_PRIMARY_LEDGER_CONFIG.csv row for that primary, two relationship rows of which one was SECONDARY, ledger-option rows for the primary and that secondary, and 56 direct legal-entity assignment rows all under the scoped primary. Both the primary and associated secondary had populated RetEarnCcidSegments. These identities and counts are sample evidence, never runtime constants.

## Public and Captured Source Index

- Legal entities LOV: https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-legalentitieslov-get.html
- Ledgers LOV: https://docs.oracle.com/en/cloud/saas/financials/26b/farfa/api-list-values-ledgers-list-values.html
- Ledger item: https://docs.oracle.com/en/cloud/saas/financials/26b/farfa/op-ledgerslov-ledgerid-get.html
- Assignment concepts: https://docs.oracle.com/en/cloud/saas/financials/26b/faigl/assign-legal-entities-and-balancing-segments.html
- Primary and secondary inheritance: https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/legal-entities-and-primary-and-secondary-ledgers.html
- Ledger relationships table: https://docs.oracle.com/en/cloud/saas/financials/26a/oedmf/glledgerrelationships-6344.html
- Ledgers table: https://docs.oracle.com/en/cloud/saas/financials/26a/oedmf/glledgers-27770.html
- Ledger configuration details table: https://docs.oracle.com/en/cloud/saas/financials/25d/oedmf/glledgerconfigdetails-26396.html
- Assign task export provenance: `discovery/cptcpmqqy_assign_legal_entities_300104903036127.zip`.
- Current scoped-export contract evidence: user-supplied `Assign Legal Entities_20260818_072052_893.zip`.
- Captured responses: `outputs/assign-legal-entities-analysis-20260813/rest-confirm-ledger-query.json`, `rest-confirm-ledger-item.json`, `rest-confirm-legal-entity-query.json`, and `rest-confirm-secondary-ledger.json`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.RESOLVE_PRIMARY_LEDGER | step | 20 | reference_lookup | resolved->ALE.ACQUIRE_SCOPED_EXPORT;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | ALE.VALIDATE_INPUT | stop | Run resolve_primary_ledger first; do not submit or select any Assign Legal Entities export until exactly one PRIMARY ledger of type L is proven. |
| ALE.RESOLVE_SCOPED_EVIDENCE | step | 40 | reference_lookup | resolved->ALE.CHECK_DEPENDENCIES;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | ALE.ACQUIRE_SCOPED_EXPORT | stop | Select and validate the returned primary-ledger-scoped Assign export, match its one parent to REST identity, resolve each requested legal entity, and derive all remaining assignment and ledger-readiness evidence from that scoped package. |
