# Manage Channel Claim Types Design Enforcement

Source: existing create policy, user-requested parity with Claim Reasons update support, and operation contracts cited in ora_input_validation.md. These are task-local design gates; live Fusion remains authoritative for existing records.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Parent-child and Business Unit review | Keep channelClaimTypes as the parent Data Loader discriminator and businessUnitLevelMappings as the optional child discriminator. Resolve every supplied Business Unit ID or name through the Financials Manage Business Unit resolver before final loader validation. |
| 2 | Applicability and dates review | Apply create-only side rules on create; update current-value/date checks run after existing-record resolution. |
| 3 | Execution route check | Permit only FSCR Run Book/core.data-loader create or update with Task Hook; direct REST POST and PATCH are prohibited. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new parent claim type with child mappings is prepared | Error | resolve_business_unit_identity | Create parentage, required BU identity/mapping code or resolved active BU is invalid | Correct create linkage and use resolved BusinessUnitId | Yes, before preview |
| A create is prepared | Error | | Side applicability or effective dates are invalid | Correct create flags/dates before rebuilding preview | Yes, before preview |
| An update is prepared | Error | | Unrequested fields or children would be overwritten, an existing child would be reparented, or a missing target would be inserted | Preserve sparse changes and validate current values after lookups; no upsert or collection replacement | Yes, before preview |
| AR-related optional values are supplied | Warning | | None | FSCR cannot validate transaction types, credit memo types, chargeback types, receivables activities, or other AR-related values because dependent Skills are unavailable | No FSCR validation available |
| Any create or update is requested | Error | | The route bypasses FSCR Run Book/core.data-loader Task Hook | Finish validation first, then build preview and obtain approval; do not use a direct REST write | Yes, before preview |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_business_unit_identity | Child create or a non-null requested BusinessUnit change on update | Resolved active BusinessUnitId; BusinessUnitName; ActiveFlag; supplied-ID comparison to proposed BU only on create | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCT.VALIDATE_DESIGN | step | 6 | design_enforcement | compliant->CJMCT.APPLY_DOCUMENTED_DEFAULTS;not_compliant->RETURN_ISSUES | CJMCT.FIND_REFERENCE_DATA_SET | stop | A reference-data-set-resolved channel claim type is prepared for core.data-loader preview |
