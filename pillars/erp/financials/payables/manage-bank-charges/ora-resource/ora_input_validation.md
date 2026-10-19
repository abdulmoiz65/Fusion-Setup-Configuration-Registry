# Manage Bank Charges — Input Validation

## Input validation policy

This step checks a create request for one new header and one or more charge
lines before reference lookups and defaulting. Reject malformed supplied values
and conflicting bank or branch option/name pairs without clearing, rounding,
truncating or replacing customer input.

For update and end-date requests, select the intended records from a fresh
export and validate the resulting values. Preserve requested changes, original
values and unspecified fields. Do not apply create defaults to updates.

A missing create value may continue as default pending only when
`ora_defaulting_rules.md` supplies it. Reference verification belongs to
`ora_reference_lookups.md` and `ora_dependency_readiness.md`; complete range,
parent assembly and fresh-state checks belong to `ora_design_enforcement.md`.

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: ORA_AP_BANK_CHARGE_LINE::BankChargeStandard, ORA_AP_BANK_CHARGE_LINE::BankChargeNegotiated, ORA_AP_BANK_CHARGE_LINE::StartDate, ORA_AP_BANK_CHARGE_LINE::EndDate, ORA_AP_BANK_CHARGE_LINE::TransAmountFrom, ORA_AP_BANK_CHARGE_LINE::TransAmountTo -->
<!-- fscr-create-fields: ORA_AP_BANK_CHARGE::Attribute1, ORA_AP_BANK_CHARGE::Attribute10, ORA_AP_BANK_CHARGE::Attribute11, ORA_AP_BANK_CHARGE::Attribute12, ORA_AP_BANK_CHARGE::Attribute13, ORA_AP_BANK_CHARGE::Attribute14, ORA_AP_BANK_CHARGE::Attribute15, ORA_AP_BANK_CHARGE::Attribute2, ORA_AP_BANK_CHARGE::Attribute3, ORA_AP_BANK_CHARGE::Attribute4, ORA_AP_BANK_CHARGE::Attribute5, ORA_AP_BANK_CHARGE::Attribute6, ORA_AP_BANK_CHARGE::Attribute7, ORA_AP_BANK_CHARGE::Attribute8, ORA_AP_BANK_CHARGE::Attribute9, ORA_AP_BANK_CHARGE::AttributeCategory, ORA_AP_BANK_CHARGE::AttributeDate1, ORA_AP_BANK_CHARGE::AttributeDate2, ORA_AP_BANK_CHARGE::AttributeDate3, ORA_AP_BANK_CHARGE::AttributeDate4, ORA_AP_BANK_CHARGE::AttributeDate5, ORA_AP_BANK_CHARGE::AttributeNumber1, ORA_AP_BANK_CHARGE::AttributeNumber2, ORA_AP_BANK_CHARGE::AttributeNumber3, ORA_AP_BANK_CHARGE::AttributeNumber4, ORA_AP_BANK_CHARGE::AttributeNumber5, ORA_AP_BANK_CHARGE::CurrencyCode, ORA_AP_BANK_CHARGE::LegalEntityIdentifier, ORA_AP_BANK_CHARGE::LegalEntityName, ORA_AP_BANK_CHARGE::ReceivingBankCountry, ORA_AP_BANK_CHARGE::ReceivingBankName, ORA_AP_BANK_CHARGE::ReceivingBankNumber, ORA_AP_BANK_CHARGE::ReceivingBankOption, ORA_AP_BANK_CHARGE::ReceivingBranchName, ORA_AP_BANK_CHARGE::ReceivingBranchNumber, ORA_AP_BANK_CHARGE::ReceivingBranchOption, ORA_AP_BANK_CHARGE::SettlementPriorityDisplay, ORA_AP_BANK_CHARGE::TransferringBankCountry, ORA_AP_BANK_CHARGE::TransferringBankName, ORA_AP_BANK_CHARGE::TransferringBankNumber, ORA_AP_BANK_CHARGE::TransferringBankOption, ORA_AP_BANK_CHARGE::TransferringBranchName, ORA_AP_BANK_CHARGE::TransferringBranchNumber, ORA_AP_BANK_CHARGE::TransferringBranchOption, ORA_AP_BANK_CHARGE_LINE::Attribute1, ORA_AP_BANK_CHARGE_LINE::Attribute10, ORA_AP_BANK_CHARGE_LINE::Attribute11, ORA_AP_BANK_CHARGE_LINE::Attribute12, ORA_AP_BANK_CHARGE_LINE::Attribute13, ORA_AP_BANK_CHARGE_LINE::Attribute14, ORA_AP_BANK_CHARGE_LINE::Attribute15, ORA_AP_BANK_CHARGE_LINE::Attribute2, ORA_AP_BANK_CHARGE_LINE::Attribute3, ORA_AP_BANK_CHARGE_LINE::Attribute4, ORA_AP_BANK_CHARGE_LINE::Attribute5, ORA_AP_BANK_CHARGE_LINE::Attribute6, ORA_AP_BANK_CHARGE_LINE::Attribute7, ORA_AP_BANK_CHARGE_LINE::Attribute8, ORA_AP_BANK_CHARGE_LINE::Attribute9, ORA_AP_BANK_CHARGE_LINE::AttributeCategory, ORA_AP_BANK_CHARGE_LINE::AttributeDate1, ORA_AP_BANK_CHARGE_LINE::AttributeDate2, ORA_AP_BANK_CHARGE_LINE::AttributeDate3, ORA_AP_BANK_CHARGE_LINE::AttributeDate4, ORA_AP_BANK_CHARGE_LINE::AttributeDate5, ORA_AP_BANK_CHARGE_LINE::AttributeNumber1, ORA_AP_BANK_CHARGE_LINE::AttributeNumber2, ORA_AP_BANK_CHARGE_LINE::AttributeNumber3, ORA_AP_BANK_CHARGE_LINE::AttributeNumber4, ORA_AP_BANK_CHARGE_LINE::AttributeNumber5, ORA_AP_BANK_CHARGE_LINE::BankChargeNegotiated, ORA_AP_BANK_CHARGE_LINE::BankChargeStandard, ORA_AP_BANK_CHARGE_LINE::EndDate, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.CurrencyCode, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.LegalEntityIdentifier, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.LegalEntityName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankCountry, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBankOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.ReceivingBranchOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.SettlementPriorityDisplay, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankCountry, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBankOption, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchName, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchNumber, ORA_AP_BANK_CHARGE_LINE::ORA_AP_BANK_CHARGE.TransferringBranchOption, ORA_AP_BANK_CHARGE_LINE::StartDate, ORA_AP_BANK_CHARGE_LINE::TransAmountFrom, ORA_AP_BANK_CHARGE_LINE::TransAmountTo -->

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BKC.INPUT | step | 10 | validate_input | pass->BKC.LOOKUPS;fail->BKC.ERROR | none | stop | true |

## Package contract

| Member | Required shape |
|---|---|
| `ASM_SETUP_CSV_METADATA.xml` | Exact same-task metadata and node paths |
| `ORA_AP_BANK_CHARGE.csv` | One header row using all 44 columns in template order |
| `ORA_AP_BANK_CHARGE_LINE.csv` | One or more child rows using all 50 columns in template order |

For a prepared one-group create package, reject missing, additional, renamed,
reordered or inconsistent members and columns. Preserve blank cells as blanks;
blank is distinct from numeric zero.

## Required create values

Check customer-supplied values now. An omitted value may remain default pending
only if the corresponding create default applies; check the effective value
after defaulting.

| Scope | Required effective value | Omission handling |
|---|---|---|
| Header | Legal entity, currency, settlement priority and transferring/receiving bank and branch options | Continue only when the corresponding standard default applies; otherwise reject |
| Each charge line | `StartDate`, `TransAmountFrom`, `BankChargeStandard` and `BankChargeNegotiated` | Reject |
| Optional range endpoints | `EndDate` and `TransAmountTo` | Blank is allowed, subject to cross-row design rules |
| Specific bank or branch | Corresponding nonblank name | Reject when missing or whitespace-only |

## Field validation

| Check | Required behavior |
|---|---|
| Free-text fields | Preserve the supplied value. Use trimming only to determine whether a required name is blank. Do not enforce an unverified maximum length. |
| Dates | Use `YYYY-MM-DD` for customer-supplied calendar dates. When `EndDate` is supplied, require `StartDate` ≤ `EndDate`. |
| Charge and payment amounts | Require finite, nonnegative decimal values for `BankChargeStandard`, `BankChargeNegotiated`, `TransAmountFrom` and `TransAmountTo`. Do not round or impose unverified precision or scale. |
| Amount endpoints | When `TransAmountTo` is supplied, require `TransAmountFrom` ≤ `TransAmountTo`. |
| Flexfields | Accept optional native string, date and decimal values with type checks only. Do not apply local DFF context, value-set, requiredness or default rules; Fusion may still validate supplied values. |

## Option and name consistency

Apply these rules to the resulting values for both create and update assessment,
independently for transferring and receiving banks and branches, before reference
lookup. Interpret `ALL` and `ONE` using the local choice mappings in
`ora_reference_lookups.md`.

| Effective option | Corresponding name | If the rule fails |
|---|---|---|
| Specific bank | Must be nonblank | Request the bank name |
| All banks | Must be blank | Request removal of the name or selection of Specific bank |
| Specific branch | Must be nonblank | Request the branch name |
| All branches | Must be blank | Request removal of the name or selection of Specific branch |

For create requests, when both an option and its corresponding name are omitted,
the applicable All default may be applied later. When a name is supplied without
an option, stop and ask for the option.

For update assessment, preserve verified current values for omitted fields and
combine them with the explicitly requested changes before checking the pair.
An omitted option does not require a new value when the existing option is known
and consistent with the resulting name. Changing an option to All while omitting
the name preserves the existing name; a retained nonblank name still conflicts.
If required current values are unknown
or ambiguous, return evidence_unresolved. Do not apply create defaults or treat
omission as clearing. An explicitly blank value requests clearing and must
satisfy the resulting field's requiredness and consistency rules. Never
silently clear a conflicting name.
