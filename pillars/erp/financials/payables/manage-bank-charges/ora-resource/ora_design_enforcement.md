# Manage Bank Charges — Design Enforcement

## Design enforcement policy

This step checks the complete create or snapshot-bound update design after
dependency checks and applicable defaults, before the separate execution gate.
It does not submit data to Fusion.

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: ORA_AP_BANK_CHARGE_LINE::BankChargeStandard, ORA_AP_BANK_CHARGE_LINE::BankChargeNegotiated, ORA_AP_BANK_CHARGE_LINE::StartDate, ORA_AP_BANK_CHARGE_LINE::EndDate, ORA_AP_BANK_CHARGE_LINE::TransAmountFrom, ORA_AP_BANK_CHARGE_LINE::TransAmountTo -->
<!-- fscr-create-fields: ORA_AP_BANK_CHARGE::Attribute1, ORA_AP_BANK_CHARGE::Attribute10, ORA_AP_BANK_CHARGE::Attribute11, ORA_AP_BANK_CHARGE::Attribute12, ORA_AP_BANK_CHARGE::Attribute13, ORA_AP_BANK_CHARGE::Attribute14, ORA_AP_BANK_CHARGE::Attribute15, ORA_AP_BANK_CHARGE::Attribute2, ORA_AP_BANK_CHARGE::Attribute3, ORA_AP_BANK_CHARGE::Attribute4, ORA_AP_BANK_CHARGE::Attribute5, ORA_AP_BANK_CHARGE::Attribute6, ORA_AP_BANK_CHARGE::Attribute7, ORA_AP_BANK_CHARGE::Attribute8, ORA_AP_BANK_CHARGE::Attribute9, ORA_AP_BANK_CHARGE::AttributeCategory, ORA_AP_BANK_CHARGE::AttributeDate1, ORA_AP_BANK_CHARGE::AttributeDate2, ORA_AP_BANK_CHARGE::AttributeDate3, ORA_AP_BANK_CHARGE::AttributeDate4, ORA_AP_BANK_CHARGE::AttributeDate5, ORA_AP_BANK_CHARGE::AttributeNumber1, ORA_AP_BANK_CHARGE::AttributeNumber2, ORA_AP_BANK_CHARGE::AttributeNumber3, ORA_AP_BANK_CHARGE::AttributeNumber4, ORA_AP_BANK_CHARGE::AttributeNumber5, ORA_AP_BANK_CHARGE::CurrencyCode, ORA_AP_BANK_CHARGE::LegalEntityIdentifier, ORA_AP_BANK_CHARGE::LegalEntityName, ORA_AP_BANK_CHARGE::ReceivingBankCountry, ORA_AP_BANK_CHARGE::ReceivingBankName, ORA_AP_BANK_CHARGE::ReceivingBankNumber, ORA_AP_BANK_CHARGE::ReceivingBankOption, ORA_AP_BANK_CHARGE::ReceivingBranchName, ORA_AP_BANK_CHARGE::ReceivingBranchNumber, ORA_AP_BANK_CHARGE::ReceivingBranchOption, ORA_AP_BANK_CHARGE::SettlementPriorityDisplay, ORA_AP_BANK_CHARGE::TransferringBankCountry, ORA_AP_BANK_CHARGE::TransferringBankName, ORA_AP_BANK_CHARGE::TransferringBankNumber, ORA_AP_BANK_CHARGE::TransferringBankOption, ORA_AP_BANK_CHARGE::TransferringBranchName, ORA_AP_BANK_CHARGE::TransferringBranchNumber, ORA_AP_BANK_CHARGE::TransferringBranchOption, ORA_AP_BANK_CHARGE_LINE::Attribute1, ORA_AP_BANK_CHARGE_LINE::Attribute10, ORA_AP_BANK_CHARGE_LINE::Attribute11, ORA_AP_BANK_CHARGE_LINE::Attribute12, ORA_AP_BANK_CHARGE_LINE::Attribute13, ORA_AP_BANK_CHARGE_LINE::Attribute14, ORA_AP_BANK_CHARGE_LINE::Attribute15, ORA_AP_BANK_CHARGE_LINE::Attribute2, ORA_AP_BANK_CHARGE_LINE::Attribute3, ORA_AP_BANK_CHARGE_LINE::Attribute4, ORA_AP_BANK_CHARGE_LINE::Attribute5, ORA_AP_BANK_CHARGE_LINE::Attribute6, ORA_AP_BANK_CHARGE_LINE::Attribute7, ORA_AP_BANK_CHARGE_LINE::Attribute8, ORA_AP_BANK_CHARGE_LINE::Attribute9, ORA_AP_BANK_CHARGE_LINE::AttributeCategory, ORA_AP_BANK_CHARGE_LINE::AttributeDate1, ORA_AP_BANK_CHARGE_LINE::AttributeDate2, ORA_AP_BANK_CHARGE_LINE::AttributeDate3, ORA_AP_BANK_CHARGE_LINE::AttributeDate4, ORA_AP_BANK_CHARGE_LINE::AttributeDate5, ORA_AP_BANK_CHARGE_LINE::AttributeNumber1, ORA_AP_BANK_CHARGE_LINE::AttributeNumber2, ORA_AP_BANK_CHARGE_LINE::AttributeNumber3, ORA_AP_BANK_CHARGE_LINE::AttributeNumber4, ORA_AP_BANK_CHARGE_LINE::AttributeNumber5, ORA_AP_BANK_CHARGE_LINE::BankChargeNegotiated, ORA_AP_BANK_CHARGE_LINE::BankChargeStandard, ORA_AP_BANK_CHARGE_LINE::EndDate, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.CurrencyCode, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.LegalEntityIdentifier, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.LegalEntityName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankCountry, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.SettlementPriorityDisplay, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankCountry, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchOption, ORA_AP_BANK_CHARGE_LINE::StartDate, ORA_AP_BANK_CHARGE_LINE::TransAmountFrom, ORA_AP_BANK_CHARGE_LINE::TransAmountTo -->

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BKC.DESIGN | step | 50 | design_enforcement | pass->BKC.EXECUTION_GATE;fail->BKC.ERROR | BKC.DEFAULTS | stop | true |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Update or end-date | Error |  | The intended header or line cannot be selected unambiguously from a fresh export, or the proposed change alters unspecified values or rows | Resolve the local target selection and preserve original and unspecified values; do not switch to create or apply create defaults | No |
| Replacement, deletion, replay or rollback | Error |  | The requested operation lacks an established identity and lifecycle contract | Stop preparation and report the exact unresolved contract | No |
| Create preparation | Error |  | Fresh exact-task snapshot is missing, stale, from another environment/release, or the requested group is not absent | Refresh the authorized export and repeat the exact group check | No |
| Header and child collection | Error |  | Design does not contain exactly one header and at least one complete child row | Reject the incomplete group | No |
| Parent assembly | Error |  | Any of the 18 parent-qualified child values differs from the header, or a duplicate/colliding staging signature exists | Reject; copy all parent values exactly and do not invent a persisted child key | No |
| Bank and branch scope | Error |  | An All option has a populated name, or a Specific option has no name | Correct the option/name pair before package preparation | No |
| Charge-line scalar values | Error |  | A required line value is missing, nonnumeric, nonfinite, negative, or has From greater than To or StartDate after EndDate | Correct the line values and revalidate | Yes |
| Multi-line range design | Error |  | Lines in the supported group use different effective periods, the first From is not zero, finite ranges are not adjacent, ranges overlap, or the final To is not open | Supply one same-period contiguous range set beginning at zero with one final open upper amount | Yes |

## Charge range rules

For each new bank-charge group, check the complete set of charge lines:

- Include at least one line. All lines in the supported create design use the
  same effective start and end dates.
- Start the payment amount ranges at zero. Each later range must begin exactly
  where the preceding range ends; do not add a currency increment or round the
  boundary.
- Reject overlapping date-and-amount coverage. For ordinary positive-width
  periods and ranges, touching at one endpoint alone is allowed.
- Leave the final range's upper amount blank so the group covers all higher
  payment amounts. A blank end date likewise means no specified end date; do
  not substitute an artificial limit for either blank.
- If a range check cannot be confirmed, stop and report that limitation. A
  completed import process alone does not prove every range check succeeded.

For example, `0–10,000` followed by `10,000–open` is contiguous for range
validation. These rules do not establish which charge is selected for a
payment of exactly `10,000`.
