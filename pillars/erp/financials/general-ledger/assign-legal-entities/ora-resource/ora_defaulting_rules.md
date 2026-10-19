# Assign Legal Entities Defaulting Rules

The direct row is deterministic from the two mandatory business identities. Nullable flags and service-owned audit fields remain blank on new rows; existing rows retain every exported value. Defaults never substitute for identity or retained-earnings readiness.

Authoring source: `assign-legal-entities-fdos-resource-analysis.xlsx`, especially `Import Fields!A1:H19`, `Defaults!A1:D20`, and `Observed Evidence!A1:C15`.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| GL_LEDGER.Name | Exact normalized primary ledger Name | Every new direct mapping row | No; derive from current REST identity and exact export parent | resolve_primary_configuration_exact |
| ObjectTypeCode | LEGAL_ENTITY | Every new direct mapping row | No |  |
| SetupStepCode | NONE | Every new direct mapping row | No |  |
| LedgerName | True blank | Every new direct mapping row | No; never copy a target or secondary ledger Name |  |
| LegalEntityIdentifier | Exact validated user identifier | Every new direct mapping row | No; user owns the identifier and the resolver validates it | resolve_legal_entity_exact_identifier |
| ObjectName | Canonical current legal-entity Name | Every new direct mapping row | No; derive from the exact identifier REST result and never copy an existing assignment-row name | resolve_legal_entity_exact_identifier |
| NextActionCode | NONE | Every new direct mapping row | No |  |
| StatusCode | CONFIRMED | Every new direct mapping row | No |  |
| CreatedBy | True blank | Every new direct mapping row | No; preserve the exact value on existing rows |  |
| LastUpdateLogin | True blank | Every new direct mapping row | No; preserve the exact value on existing rows |  |
| LastUpdateDate | True blank | Every new direct mapping row | No; preserve the exact value on existing rows |  |
| LastUpdatedBy | True blank | Every new direct mapping row | No; preserve the exact value on existing rows |  |
| CreationDate | True blank | Every new direct mapping row | No; preserve the exact value on existing rows |  |
| EffectiveFrom resolver evidence | Preserve the exact returned value, including null | After legal-entity identity resolution; this evidence is not defaulted into the direct assignment row | No | resolve_legal_entity_exact_identifier |
| TimeZoneDefaultLeFlag | True blank | Every new direct mapping row | No; do not infer or accept Y or N in this task and preserve existing-row values |  |
| TaxDefaultLeFlag | True blank | Every new direct mapping row | No; do not infer or accept Y or N in this task and preserve existing-row values |  |
| Hidden legal-entity key | Do not put in CSV | Every new direct mapping row | No; the import resolves it from LegalEntityIdentifier | resolve_legal_entity_exact_identifier |
| Hidden configuration key | Do not put in CSV | Every new direct mapping row | No; the import resolves the parent from GL_LEDGER.Name | resolve_primary_configuration_exact |
| Balancing-segment assignment state | Do not author in this task | Every direct legal-entity mapping | No; re-export and report downstream setup state instead | report_balancing_segment_state |
| Every field of an existing or unrelated row | Preserve exported value | Carrying the baseline package | No |  |

## Default Safety Rules

| Situation | What Happens |
|---|---|
| User omits a mandatory identity | Do not default it; return the missing ledger reference or legal-entity identifier |
| Current REST Name and export Name disagree | Do not choose one silently; stop and refresh or correct the source evidence |
| EffectiveFrom is null | Preserve null as authoritative lookup evidence; do not invent a start date |
| EffectiveFrom is populated | Preserve the value and block when it is after the run date; do not alter the date |
| TimeZoneDefaultLeFlag is processed | Keep a true blank in every proposed new row; reject a requested populated override and preserve every existing-row value |
| TaxDefaultLeFlag is processed | Keep a true blank in every proposed new row; reject a requested populated override and preserve every existing-row value |
| Audit columns are processed | Keep true blanks in every proposed new row and preserve the exact exported values of every existing row |
| Intentional blank is serialized | Emit a zero-character CSV field; reject whitespace and textual null sentinels |
| Balancing-segment setup is absent | Report the downstream gap after re-export; never add company or balancing-segment child rows in this task |
| Any default or derived value changes after preview | Invalidate approval, rebuild the exact semantic diff, and preview again |

## Observed Non-Constant Default Evidence

The 2026-08-13 sample contained 215 one-legal-entity configurations with one time-zone default, 41 with none, 113 multiple-entity configurations with exactly one default, seven multiple-entity configurations with none, and one legacy or test anomaly with multiple Y values. Across the 898 direct rows, TimeZoneDefaultLeFlag was Y on 330 and N on 568 with no blanks, TaxDefaultLeFlag was blank on all 898, and none of the five audit fields was blank on an existing row. The developer-authorized new-row contract nevertheless keeps both nullable flags and all five audit fields blank while preserving every existing exported value. Existing values, including the anomaly, are not normalized by this task, and the anomaly must never be copied into a new row. These counts are evidence, not production constants.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALE.APPLY_DEFAULTS | step | 60 | apply_default | prepared->ALE.ENFORCE_DESIGN;blocked->RETURN_ISSUES | ALE.CHECK_DEPENDENCIES | stop | Build the smallest proposed direct-row delta only from validated user values, authoritative resolver output, documented constants, intentional blanks, and preserved scoped-baseline values. |
