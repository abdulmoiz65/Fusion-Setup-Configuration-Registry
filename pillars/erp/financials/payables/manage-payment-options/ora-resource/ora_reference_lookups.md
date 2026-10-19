# Reference Lookups

`Manage Payment Options` creates the same `AP_SYSTEM_PARAMETER` row as its sibling `Manage Invoice Options`. Before live normalization, run `scripts/resolve_lookup_prerequisites.py`; it delegates only the shared-row prerequisite checks to the sibling's task-local read-only preflight contract. Invoice Options-owned default payment-term lookups remain with Manage Invoice Options. The Payment Options adapter remains offline, and neither component calls CRM, BICC, or SQL.

| Resolver | When used | Lookup result | Safety rule |
|---|---|---|---|
| `resolve_business_unit_by_name_and_enterprise` | A create targets `BuName` | `finBusinessUnitsLOV` confirms one active exact BU. `EnterpriseId` is taken from an explicit row value, otherwise only from one distinct nonblank value in the fresh FSM baseline. | Block a missing/inactive/ambiguous BU or Enterprise ID. Never create a BU. |
| `resolve_business_unit_primary_ledger` | A new row is created | `ledgersLOV/{PrimaryLedgerId}` returns the ledger name and currency; these become the derived `SOBName` and `BaseCurrencyCode`. | Block a missing, malformed, or conflicting receipt. |
| `resolve_bank_charge_deduction_type` | Bank Charge Deduction Type is supplied | Map **Standard** to `S`, **Negotiated** to `N`, and **None** to `X` in `BankChargeDeductionTypeDes`. | Block every other value. Do not confuse this control with Bank Charge Bearer. |

Payment Options and Invoice Options use the same `AP_SYSTEM_PARAMETER` row and CSV package contract. Validate the resulting shared row through the sibling Invoice Options contract before preview; do not bypass that dependency with a payment-only package.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A supporting lookup returns one or more readable records | Proceed without local exact, case, uniqueness, or ID selection. Preserve the submitted CSV value for FSM Import. |
| A supporting lookup returns a readable zero-result | Record a warning and preserve the submitted CSV value for authoritative FSM Import validation. |
| A supported read-only lookup is later evidenced | Add one task-scoped resolver with source values, request path, match rule, output mapping, and no-match/many-match behavior before it is used |
| A delegated supporting GET returns HTTP 400 | Preserve the submitted value and record both `validation_skipped` and `resolver_contract_issue`; FSM Import remains authoritative. The create-time BU/ledger derivation remains blocking only when it cannot derive required CSV values. |
