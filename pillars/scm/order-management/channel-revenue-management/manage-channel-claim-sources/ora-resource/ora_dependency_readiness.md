# Manage Channel Claim Sources Dependency Readiness

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| REFERENCE_DATA_SET | Reference data set | Yes | Create or update needing set resolution; ID-only update inherits verified parent set | Lookup | Fusion set identity | resolve_reference_data_set | Scoped mapping and defaults | Supply consistent identifiers; updates cannot reassign the set | SetId; SetCode; SetName |
| EXISTING_PARENT | Existing source mapping | Conditional | Update or create_child | Verify | Fusion existing record | resolve_existing_claim_source | Exact existing parent | Missing target blocks, never creates | Current parent identity and values |
| NEW_CHILD_UNIQUENESS | No existing settlement method match | Conditional | create_child | Lookup | Complete existing child collection | find_settlement_method_duplicate | Prevent duplicate child creation | Existing parent is required, not a duplicate parent-create error | Exact method match count |
| EXISTING_CHILD | Existing settlement method | Conditional | Child update | Verify | Fusion child under parent | resolve_existing_settlement_method | Child ownership and current state | Supply existing SourceSettlementMethodId | Current child values and predefined status |
| CLAIM_CLASS | Claim class | Conditional | Create | Lookup | Fusion lookup | resolve_claim_class | Valid class code | Provide an exact code | ClaimClassCode; ClaimClass |
| CLAIM_SOURCE | Claim source | Conditional | Create | Lookup | Fusion lookup | resolve_claim_source | Valid source code | Provide an exact code | ClaimSourceCode; ClaimSource |
| DEFAULT_TYPE | Default claim type | Conditional | Non-null reference supplied on create or changed on update | Lookup | Fusion channel claim types eligible under the default-reference resolver | resolve_default_claim_type | Valid default | Resolve existing type using the resolver's set-sharing rule; do not auto-create dependencies | DefaultClaimTypeId; DefaultClaimType |
| DEFAULT_REASON | Default claim reason | Conditional | Non-null reference supplied on create or changed on update | Lookup | Fusion channel claim reasons eligible under the default-reference resolver | resolve_default_claim_reason | Valid default | Resolve existing reason using the resolver's set-sharing rule; do not auto-create dependencies | DefaultClaimReasonId; DefaultClaimReason |
| SETTLEMENT_METHOD | Settlement method | Conditional | Child create or changed name | Lookup | Fusion lookup | resolve_settlement_method | Valid method name | Update accepts name, not a code mutation | SettlementMethod |
| ACCOUNTING_FOR | Accounting application | Conditional | Child create or non-null changed AccountingFor | Lookup | Fusion lookup | resolve_accounting_for | Valid accounting application | Receivables or Payables; predefined restriction evaluated by design gate | AccountingFor |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCS.CONFIRM_DEPENDENCIES | decision | 3 | resolve_dependency | resolved->CJMCS.RESOLVE_REFERENCES;blocked->RETURN_ISSUES | CJMCS.RESOLVE_EXISTING | stop | Evaluate only dependencies applicable to operation and proposed changes; reuse fresh verified existing-target evidence |
