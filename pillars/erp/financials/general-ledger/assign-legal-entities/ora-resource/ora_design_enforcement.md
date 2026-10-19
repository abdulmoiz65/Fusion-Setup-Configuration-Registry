# Assign Legal Entities Design Enforcement

The supported outcome is a hybrid read plus controlled CSV-import handoff: ledger REST first proves an exact PRIMARY ledger of type L, the declared shared export route then acquires one Assign Legal Entities package scoped to that primary, legal-entity REST supplies each candidate's current identity and effectivity, and that one scoped package proves current assignment and ledger readiness. Only the reviewed direct-row delta is handed to `core.data-loader`; this resource does not execute an import.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `FDOS Decision!A1:C15`, `Validations!A1:H20`, `PL-SL Readiness!A1:F22`, `Export Files!A1:F21`, and `TBD Register!A1:F10`.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm assign-only scope | Require GL_ASSIGN_LEGAL_ENTITIES and a direct add-mapping request; route removal, reassignment, and balancing-segment assignment elsewhere |
| 2 | Confirm primary configuration before export | Require one REST-resolved PRIMARY ledger of type L; never submit an export for an unresolved or secondary ledger and never silently re-parent |
| 3 | Acquire and confirm scoped source authority | Create GL_ASSIGN_LEGAL_ENTITIES through core.fusion-api.rest-api-client with SetupTaskCSVExportCriteria and SetupTaskCSVExportProcess as sibling arrays at the request root, TaskCode GL_ASSIGN_LEGAL_ENTITIES in the root and both child rows, and the criterion BusinessObjectCode GL_PRIMARY_LEDGER, AttributeSet Set1, AttributeName PRIMARY_LEDGER_ID, AttributeValue resolved LedgerId. Never nest criteria inside the process row. Use the returned ProcessId for polling and download through shared.setup-export.fsm-csv-export; require exact task and scope metadata plus one parent whose Name matches the normalized REST Name in GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv |
| 4 | Confirm legal-entity identity, effectivity, and scoped unassignment | Require exact current legal-entity identity, supported effectivity, and complete duplicate evidence from every direct row in the scoped export |
| 5 | Confirm retained-earnings readiness | Require populated RetEarnCcidSegments for the current primary ledger and every associated secondary ledger, including disabled relationships |
| 6 | Enforce direct-row contract | Populate only the documented direct mapping fields, keep both nullable flags and service-owned audit fields blank, keep hidden fields out of user control, preserve all existing values, and create exactly one row per requested mapping |
| 7 | Enforce package boundary | Change only ORA_GL_JOURNAL_CONFIG_DETAIL.csv for a direct mapping; preserve every other observed Assign export file and every unrelated row; never add balancing-segment child rows |
| 8 | Preview and approval handoff | Show exact environment, task, identities, member-level diff, row values, preserved members, retained-earnings readiness, and immutable artifact fingerprint; obtain approval immediately before the declared Data Loader import step |
| 9 | Verify and report | After any separately approved import, immediately re-export, verify the direct mapping, report downstream balancing-segment state, and stop on uncertainty |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error |  | Action is removal, reassignment, ledger-child authoring, or balancing-segment assignment rather than direct add mapping | Use the separately owned task or resource for the requested operation | No |
| Ledger reference resolves | Error | resolve_primary_ledger | Ledger is not PRIMARY, LedgerTypeCode is not L, or current identity is ambiguous | Supply the exact owning primary ledger; never silently re-parent | Yes, user corrects input |
| Primary ledger REST gate passes | Error |  | Export was submitted before the gate; SetupTaskCSVExportCriteria is nested inside SetupTaskCSVExportProcess rather than being its sibling at the request root; TaskCode is missing from the root or either child row; task metadata is not GL_ASSIGN_LEGAL_ENTITIES; BusinessObjectCode is not GL_PRIMARY_LEDGER; AttributeSet is not Set1; AttributeName is not PRIMARY_LEDGER_ID; or AttributeValue differs from the resolved LedgerId | Discard the candidate and acquire one fresh exact-scoped export through the declared shared route | Yes, refresh evidence |
| Scoped package resolves | Error | resolve_primary_configuration_exact | GL_LEDGER.csv or ORA_GL_PRIMARY_LEDGER_CONFIG.csv has zero, multiple, or nonmatching Name rows, or downstream parent references escape the validated scope | Refresh or correct the scoped task export | Yes, refresh evidence |
| Legal entity resolves | Error | resolve_legal_entity_exact_identifier | Identifier or canonical Name is ambiguous, EffectiveTo precedes the run date, or a populated EffectiveFrom is after the run date | Preserve null EffectiveFrom; otherwise correct the identifier or wait until the legal entity is effective | Yes, outside this task |
| Duplicate assessment runs | Error | check_existing_direct_assignment | An exact populated identifier match exists, an exact canonical ObjectName match exists in a legacy blank-identifier row, or any legacy row has both identity fields blank so absence cannot be proven | Do not add a duplicate; refresh or correct an incomplete export before retry | No |
| Primary or associated secondary retained earnings is checked | Error | check_retained_earnings_readiness | RetEarnCcidSegments is blank, missing, or ambiguous for the current primary ledger or any associated secondary ledger, including a disabled relationship | Complete 'Specify Ledger Options' for PL and all its associated SLs and retry | Yes, outside this task |
| New direct mapping row is authored | Error |  | TimeZoneDefaultLeFlag or TaxDefaultLeFlag is populated instead of remaining blank or null | Leave both nullable flags blank | Yes, regenerate row |
| New or existing row is carried into the package | Error |  | A new-row audit field is populated or any existing audit, flag, identity, status, or unrelated value changes | Keep new-row audit fields blank and restore every existing exported value | Yes, regenerate row or package |
| Proposed delta is authored | Error | verify_assignment_delta | New direct-row count differs from requested mappings, an unrelated row changes, or any nonowning file is authored | Rebuild the smallest semantic delta | Yes, regenerate and re-preview |
| Direct mapping exposes incomplete balancing-segment setup | Warning | report_balancing_segment_state | Runtime tries to add ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv or other child rows in this task | Report and route downstream balancing-segment setup separately | No child-row fix here |
| Preview or approval is requested | Error | verify_assignment_delta | Any required lookup or dependency is blocked, package is not fresh, diff is not exact, target environment is missing, or approval is not bound to the immutable import artifact | Resolve blockers, regenerate preview, and obtain explicit step-local approval | Yes, after evidence is complete |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_primary_ledger | Every request | LedgerId, normalized Name, LedgerCategoryCode, and LedgerTypeCode | ora_reference_lookups.md |
| resolve_primary_configuration_exact | After scoped package selection | Exact Name in the one GL_LEDGER.csv row and the one ORA_GL_PRIMARY_LEDGER_CONFIG.csv row, plus downstream parent-scope agreement | ora_reference_lookups.md |
| resolve_legal_entity_exact_identifier | Every requested legal entity | LegalEntityId, identifier, canonical Name, EffectiveFrom, and EffectiveTo | ora_reference_lookups.md |
| check_existing_direct_assignment | Before proposing a row | Exact identifier matches, exact canonical-name matches in legacy blank-identifier rows, matching parents, unattributable legacy-row count, and proof status | ora_reference_lookups.md |
| check_retained_earnings_readiness | After all associated secondary relationships are enumerated | Primary result, complete associated-secondary list, per-ledger retained-earnings result, failing-ledger list, and overall readiness | ora_reference_lookups.md |
| report_balancing_segment_state | Proposed mapping and post-import re-export | Existing child evidence and downstream setup-needed indicator | ora_reference_lookups.md |
| verify_assignment_delta | Before preview and after import re-export | Mapping count, added rows, changed members, preserved members, and semantic diff | ora_reference_lookups.md |

## Observed Non-Constant Export Evidence

The read-only 2026-08-13 evidence contained 577 Assign export ledger configurations, 898 direct assignment rows, 55 direct rows with blank LegalEntityIdentifier, 1,257 balancing-segment child rows, and 10 direct assignments under Vision Foods whose populated identifiers and names matched the prior REST cross-check. All 55 legacy blank-identifier rows had a nonblank, distinct ObjectName; one exact ObjectName also appeared on a populated-identifier row under another parent, so the export demonstrates a real legacy-name duplicate case. The remaining Assign files had observed counts of 577 parent configuration rows, 330 relationship rows, 809 rows in each primary and secondary ledger alias, 93 ledger segment-value assignments, 1,105 journal conversion rules, and zero primary balancing-segment-value conversion rules. These counts delimit the historical evidence sample and must never become expected production totals or override the current scoped-export contract.

The user-supplied 2026-08-18 export is the current shape evidence for scoped operation. ASM_SETUP_CSV_METADATA.xml declares task GL_ASSIGN_LEGAL_ENTITIES and PRIMARY_LEDGER_ID value Vision Operations (USA); the package contains exactly one parent configuration, its SECONDARY relationship to IAS Reporting Vision Ops, ledger-option evidence for both, and 56 already-assigned legal entities under the same parent. Runtime must derive these values from the validated ledger and new export rather than hard-code the sample.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.ENFORCE_DESIGN | decision | 70 | design_enforcement | passed->ALE.PREVIEW_GATE;blocked->RETURN_ISSUES | ALE.APPLY_DEFAULTS | stop | Before preview or import handoff, enforce REST-first ledger validation, exact primary-ledger export scope, source authority, retained-earnings readiness, nullable-field policy, smallest delta, and preservation boundaries. |
