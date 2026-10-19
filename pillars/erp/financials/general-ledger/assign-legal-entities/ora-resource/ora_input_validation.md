# Assign Legal Entities Input Validation

The runbook supplies two mandatory business inputs: a ledger reference and one or more exact legal-entity identifiers. The nullable default flags remain blank on new rows, and service-owned audit values remain blank on new rows while all existing-row values are preserved. This contract is assign-only; removal, reassignment, and balancing-segment assignment are outside this task.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `User Inputs!A1:F13`, `Import Fields!A1:H19`, and `Validations!A1:H20`.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Primary ledger identity | Ledger reference as exact Name or numeric LedgerId | Stop and request the ledger reference | Resolve one exact ledger, retain its LedgerId for export scope, and normalize its current Name for parent validation; require LedgerCategoryCode PRIMARY and LedgerTypeCode L | Always | resolve_primary_ledger |
| Legal entity identity | LegalEntityIdentifier | Stop and request each missing exact identifier | Resolve each identifier exactly once and derive its current canonical Name | One row per requested legal-entity mapping | resolve_legal_entity_exact_identifier |
| Nullable direct-row flags | TimeZoneDefaultLeFlag and TaxDefaultLeFlag as blank or null only | Leave both proposed fields blank | Do not infer or populate Y or N; preserve the exported values of every existing row | Every new direct mapping row |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Ledger reference passes local shape validation | Continue only when one exact primary normal-ledger identity resolves | Derive the exact current Name and LedgerId; if the supplied ledger is SECONDARY, disclose the category and require its owning primary instead of silently re-parenting | resolve_primary_ledger |
| Resolved PRIMARY ledger of type L is available | Submit or reuse a fresh Assign Legal Entities export only through the declared shared export route with BusinessObjectCode GL_PRIMARY_LEDGER, AttributeSet Set1, AttributeName PRIMARY_LEDGER_ID, and AttributeValue equal to the resolved LedgerId | Do not use the ledger Name as AttributeValue; do not acquire the task export before this gate; after completion validate its metadata and one-parent contents |  |
| Scoped Assign export is available | Continue only when its metadata declares GL_ASSIGN_LEGAL_ENTITIES and PRIMARY_LEDGER_ID scope for the resolved LedgerId and its single GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv Name equal the normalized REST Name | Bind every downstream validation and proposed row to that exact scoped parent | resolve_primary_configuration_exact |
| LegalEntityIdentifier passes local shape validation | Continue only when one current exact legalEntitiesLOV row resolves | Derive LegalEntityId, canonical Name, EffectiveFrom, and EffectiveTo | resolve_legal_entity_exact_identifier |
| Live legal-entity identity resolves after scoped export acquisition | Preserve null EffectiveFrom; when populated, require a valid date on or before the run date and reject a not-yet-effective entity | Use the exact identifier and derived canonical Name against the scoped export for duplicate validation | resolve_legal_entity_exact_identifier |
| Complete direct-assignment rows are available | Continue only when no direct LEGAL_ENTITY and NONE row matches either the exact populated identifier or, for a legacy blank-identifier row, the exact current canonical ObjectName | Show every matching parent Name and block the duplicate; a complete export with no exact identifier or canonical-name match proves no duplicate | check_existing_direct_assignment |
| Primary and associated-secondary ledger rows are available | Continue only when RetEarnCcidSegments is populated for the current primary ledger and every associated secondary ledger, regardless of RelationshipEnabledFlag | Block and ask the user to complete 'Specify Ledger Options' for PL and all its associated SLs and retry | check_retained_earnings_readiness |
| Proposed package delta is ready for review | Continue only when the number of new direct rows equals the requested mapping count and no nonowning member changes | Regenerate the smallest delta and re-preview | verify_assignment_delta |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Missing-value normalization | Treat null, blank, and whitespace-only mandatory values as missing; do not guess or copy a value from an existing assignment row | Every supplied business input |  |
| Ledger exactness | Accept only an exact Name or numeric LedgerId; require one PRIMARY row of type L | Ledger reference is supplied | resolve_primary_ledger |
| Secondary-ledger input | Report the resolved SECONDARY category and require the owning primary ledger; do not silently substitute or re-parent | Supplied ledger resolves as SECONDARY | resolve_primary_ledger |
| Legal-entity identifier shape | Require a nonblank exact identifier no longer than 30 characters | Each requested mapping | resolve_legal_entity_exact_identifier |
| Legal-entity name derivation | Use the current canonical Name returned for the exact identifier and require no more than 240 characters; do not copy a name from an existing assignment row | Each requested mapping | resolve_legal_entity_exact_identifier |
| Legal-entity effective-from handling | Preserve a null EffectiveFrom exactly as null; when populated, require a valid date on or before the run date | Each requested mapping | resolve_legal_entity_exact_identifier |
| Direct row object type | Require ObjectTypeCode LEGAL_ENTITY | Every generated mapping row |  |
| Direct row setup step | Require SetupStepCode NONE | Every generated mapping row |  |
| Direct row ledger child | Require LedgerName to be a true blank field | Every generated mapping row |  |
| Direct row next action | Require NextActionCode NONE | Every generated mapping row |  |
| Direct row status | Require StatusCode CONFIRMED | Every generated mapping row |  |
| Time-zone default domain | Require blank or null on a new row; reject attempts to populate Y, N, whitespace, or a textual null sentinel in this task | Every generated mapping row |  |
| Tax default domain | Require blank or null on a new row; reject attempts to populate Y, N, whitespace, or a textual null sentinel in this task | Every generated mapping row |  |
| Audit-field ownership | CreatedBy, LastUpdateLogin, LastUpdateDate, LastUpdatedBy, and CreationDate remain blank on a new row and retain their exact exported values on every existing row | Every generated mapping row and every carried baseline row |  |
| One row per mapping | Require generated direct-row count to equal requested mapping count; two requested legal entities produce exactly two new rows | Single or multi-entity request | verify_assignment_delta |
| Unsupported action | Reject removal, reassignment, ledger-child authoring, or balancing-segment assignment in this task | Requested action is not direct add mapping |  |
| Unknown fields | Reject attempts to populate hidden keys, service-owned fields, company or balancing-segment child rows, or undocumented columns | User supplies technical fields outside the documented contract |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.VALIDATE_INPUT | step | 10 | validate_input | valid->ALE.RESOLVE_PRIMARY_LEDGER;invalid->RETURN_ISSUES | none | stop | Before any read-only lookup, scoped-export submission or selection, package inspection, delta authoring, preview, approval, or import handoff. |
