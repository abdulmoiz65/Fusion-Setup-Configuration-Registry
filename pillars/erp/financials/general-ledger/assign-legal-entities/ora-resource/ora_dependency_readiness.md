# Assign Legal Entities Dependency Readiness

The task first proves the requested ledger exists and is a primary normal ledger through read-only REST. Only then may it submit an Assign Legal Entities export scoped to that validated primary. The returned scoped package becomes the baseline for current parent, secondary-ledger, assignment, retained-earnings, and delta checks; candidate legal-entity identity and effectivity come from the exact read-only legal-entity resolver.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `FDOS Decision!A1:C15`, `PL-SL Readiness!A1:F22`, `Export Files!A1:F21`, and `TBD Register!A1:F10`; and the user-supplied scoped export `Assign Legal Entities_20260818_072052_893.zip`.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Primary-ledger REST gate | Resolve the supplied exact Name or LedgerId and stop unless exactly one ledger exists with LedgerCategoryCode PRIMARY and LedgerTypeCode L |
| 2 | Scoped Assign export acquisition | After the REST gate passes, use core.fusion-api.rest-api-client to create one GL_ASSIGN_LEGAL_ENTITIES export process. In the request root, SetupTaskCSVExportCriteria and SetupTaskCSVExportProcess must be sibling arrays, never nested inside one another. Put TaskCode GL_ASSIGN_LEGAL_ENTITIES in the root and in both child rows; the criterion must use BusinessObjectCode GL_PRIMARY_LEDGER, AttributeSet Set1, AttributeName PRIMARY_LEDGER_ID, and AttributeValue equal to the resolved LedgerId. Then pass only the returned ProcessId to shared.setup-export.fsm-csv-export for polling and download; do not use the task-level-export CLI, the ledger Name as AttributeValue, or an unscoped export |
| 3 | Scoped package and parent proof | Require one fresh returned package whose metadata declares the exact task and PRIMARY_LEDGER_ID scope for the resolved LedgerId and whose single GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv parent equals the normalized REST Name |
| 4 | Legal-entity identity and effectivity | Resolve each exact identifier after scoped export acquisition, derive its current canonical Name, preserve null EffectiveFrom, and validate populated effectivity |
| 5 | Existing scoped assignment state | Use every direct row from the complete scoped export to detect exact identifier or legacy canonical-name duplicates under the validated primary |
| 6 | Retained-earnings readiness | From the same scoped export require nonblank RetEarnCcidSegments for the current primary ledger and every associated secondary ledger, including disabled relationships |
| 7 | Smallest-delta package readiness | Add exactly one direct row per mapping in ORA_GL_JOURNAL_CONFIG_DETAIL.csv, keep nullable flags and new-row audit fields blank, preserve every existing value, every other file, metadata, scope, and unrelated row, and produce a reviewed semantic diff |

The create request body must have this exact nesting, substituting only the validated numeric LedgerId:

```json
{
  "TaskCode": "GL_ASSIGN_LEGAL_ENTITIES",
  "SetupTaskCSVExportCriteria": [{"TaskCode": "GL_ASSIGN_LEGAL_ENTITIES", "BusinessObjectCode": "GL_PRIMARY_LEDGER", "AttributeSet": "Set1", "AttributeName": "PRIMARY_LEDGER_ID", "AttributeValue": "<resolved LedgerId>"}],
  "SetupTaskCSVExportProcess": [{"TaskCode": "GL_ASSIGN_LEGAL_ENTITIES"}]
}
```

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ale_primary_ledger | Primary normal-ledger identity | Yes | Always | Lookup | Exact user ledger reference through ledgersLOV | resolve_primary_ledger | Direct legal-entity assignment belongs to the primary configuration and is inherited by secondaries | Provide an exact primary ledger Name or LedgerId | LedgerId, normalized Name, category, type, currency, chart, and calendar evidence |
| ale_scoped_assign_package | Fresh validated-primary-scoped Assign Legal Entities task package | Yes | Only after ale_primary_ledger is satisfied | Acquire and verify | core.fusion-api.rest-api-client for the one criteria-bearing GL_ASSIGN_LEGAL_ENTITIES create request, followed by shared.setup-export.fsm-csv-export with the returned ProcessId for polling and download, or one already completed fresh export with that exact receipt |  | Current assignment, parent, secondary, retained-earnings, balancing-segment, metadata, and preservation evidence must come from one exact scoped package | Use the exact root-sibling request body above with GL_PRIMARY_LEDGER, Set1, PRIMARY_LEDGER_ID, and the resolved LedgerId; never nest criteria inside the process row or substitute an unscoped task-level export | Package path, environment, release, task identity, exact scope tuple, members, headers, row counts, source receipt, and fingerprint |
| ale_export_parent | Exact scoped export parent configuration | Yes | After the scoped package is selected | Verify | GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv in that package | resolve_primary_configuration_exact | Metadata scope must identify the resolved LedgerId, while both one-row parent files must equal the current REST Name exactly | Refresh the scoped task export when the current primary is absent, duplicated, or mismatched | Exact LedgerId scope, exact Name, one-row parent evidence, and scope-agreement result |
| ale_legal_entity | Exact legal-entity identity and effectivity | Yes | For each requested mapping after scoped export acquisition | Lookup | Exact LegalEntityIdentifier through legalEntitiesLOV | resolve_legal_entity_exact_identifier | The identifier is the import resolver and the current Name must be derived, not copied from assignment data; effectivity is not available for an unassigned candidate in the scoped export | Provide one exact identifier per mapping | LegalEntityId, LegalEntityIdentifier, ObjectName, EffectiveFrom including null, and EffectiveTo |
| ale_duplicate_assignment | Scoped direct-assignment check | Yes | Before proposing a row | Verify | Complete scoped ORA_GL_JOURNAL_CONFIG_DETAIL.csv plus the canonical current legal-entity Name | check_existing_direct_assignment | Re-adding an exact populated identifier is a duplicate; for a legacy row with a blank identifier, an exact canonical ObjectName match proves the same legal entity is already assigned in this primary configuration | Do not import when either the exact identifier or canonical current Name already exists in a scoped direct row | Identifier match count, legacy canonical-name match count, primary Name, unattributable legacy-row count, and scoped proof status |
| ale_retained_earnings | Primary and secondary retained-earnings readiness | Yes | After primary and secondary rows are available | Verify | ORA_GL_LEDGER_RELATIONSHIP.csv, GL_PRIMARY_LEDGER.csv, and GL_SECONDARY_LEDGER.csv RetEarnCcidSegments | check_retained_earnings_readiness | Assign Legal Entities must not proceed until the current primary ledger and every associated secondary ledger have retained earnings populated, regardless of enabled status | Complete 'Specify Ledger Options' for PL and all its associated SLs and retry | Primary result, complete associated-secondary list, per-ledger retained-earnings result, failing-ledger list, and overall readiness |
| ale_balancing_segment_state | Downstream balancing-segment state | No | Proposed mapping exists and after any import re-export | Verify | ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv | report_balancing_segment_state | Adding a legal entity can expose incomplete downstream balancing-segment setup, but this task must not author child rows | Review and route downstream balancing-segment setup separately | Existing company-value evidence and downstream setup-needed indicator |
| ale_delta | Reviewed smallest package delta | Yes | Before approval handoff | Verify | Baseline and proposed Assign task packages plus requested mapping count | verify_assignment_delta | Only the direct mapping rows belong to this task; all other members and unrelated rows are preserved | Review one new direct row per requested identifier and no other logical change | Added rows, identifiers, parent Name, changed members, preserved members, and semantic diff |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact required values and current evidence already agree | Continue without changing dependency setup |
| Lookup | A documented read-only Fusion REST resolver can obtain current identity or scoped association evidence | Yes, read-only lookup only |
| Acquire and verify | The primary-ledger REST gate passed and the declared scoped-export route can return one current exact-scoped package | Yes, create the process through core.fusion-api.rest-api-client using root-sibling criteria and process arrays with GL_PRIMARY_LEDGER / Set1 / PRIMARY_LEDGER_ID / resolved LedgerId, then give the returned ProcessId to shared.setup-export.fsm-csv-export for polling and download |
| Verify | A current local task export or proposed package must be inspected or compared | Yes, local verification only |
| Blocked | Required identity, package, retained-earnings readiness, evidence, or exact delta proof is missing, failed, or ambiguous | No; request correction or fresh evidence |
| Not required | A conditional dependency does not apply | Continue while preserving the intentional blank and other existing values |

## Observed Non-Constant Readiness Evidence

For Vision Foods - USA Ledger, the 2026-08-13 export contained nine SECONDARY rows. `VisionFoods` and `Vision Foods - USA IFRS SecLed` were enabled and had populated retained-earnings evidence. `CX_SL_TEST_BALANCE_BLANK`, `CX_FDOS_SL_BAL_260724`, `CX_SL_TEST_JOURNAL_BLANK`, `CX_SL_TEST_JRN_DIFF_COA_CAL`, `CX_SL_TEST_JRN_DIFF_CAL_CUR`, `CX_FDOS_SL_JRN_260724`, and `FDOS_DOC_SL_JRN_20260803_0855` were disabled and had blank retained-earnings evidence. This current sample is blocked because disabled secondaries are still associated secondaries and must have RetEarnCcidSegments populated.

The user-supplied 2026-08-18 package demonstrates the scoped shape: metadata task GL_ASSIGN_LEGAL_ENTITIES with PRIMARY_LEDGER_ID Vision Operations (USA), one exact parent row in each parent file, one SECONDARY relationship to IAS Reporting Vision Ops, and populated RetEarnCcidSegments for both the primary and associated secondary. The 56 direct assignment rows all belong to the scoped primary. These names and counts are evidence only.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.ACQUIRE_SCOPED_EXPORT | step | 30 | resolve_dependency | ready->ALE.RESOLVE_SCOPED_EVIDENCE;blocked->RETURN_ISSUES | ALE.RESOLVE_PRIMARY_LEDGER | stop | After the primary-ledger gate passes, use core.fusion-api.rest-api-client for exactly one GL_ASSIGN_LEGAL_ENTITIES create request in the current explicitly requested run. A prior no-ProcessId failure is audit history only and must not replace or block this fresh attempt after the FDoS contract was corrected. Keep SetupTaskCSVExportCriteria and SetupTaskCSVExportProcess as sibling arrays at the request root, put TaskCode GL_ASSIGN_LEGAL_ENTITIES in the root and each child row, and set the criterion to BusinessObjectCode GL_PRIMARY_LEDGER, AttributeSet Set1, AttributeName PRIMARY_LEDGER_ID, and AttributeValue equal to the resolved LedgerId. Use only its returned ProcessId with shared.setup-export.fsm-csv-export for polling and download; never submit a second POST in the same run, nest the criteria inside the process row, call the unscoped task-level-export CLI, or use the ledger Name as AttributeValue. |
| ALE.CHECK_DEPENDENCIES | decision | 50 | resolve_dependency | ready->ALE.APPLY_DEFAULTS;blocked->RETURN_ISSUES | ALE.RESOLVE_SCOPED_EVIDENCE | stop | After the scoped package, exact parent, legal-entity identities, scoped duplicate proof, and retained-earnings evidence resolve and before any proposed package delta is populated. |
