# Manage Bank Charges — Defaulting Rules

## Create defaulting policy

For a create request, FSCR applies the header defaults below when the customer
does not supply the corresponding field. An explicit customer value always
wins. Defaults are applied before required-field and option/name
validation, recorded in the normalized design, and copied exactly into the
line's parent-qualified header references.

Use the display values in the table below. Do not infer a default when a
customer supplies a bank or branch name but omits its option, because silently
selecting All would conflict with the supplied specific name. Never invent a
country code, bank number, branch number or legal-entity identifier.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ORA_AP_BANK_CHARGE.CurrencyCode | USD | New create header and field omitted | No | resolve_currency |
| ORA_AP_BANK_CHARGE.SettlementPriorityDisplay | Express | New create header and field omitted | No | resolve_settlement_priority |
| ORA_AP_BANK_CHARGE.TransferringBankOption | All banks | New create header, option omitted, and TransferringBankName omitted or blank | No | resolve_bank_option |
| ORA_AP_BANK_CHARGE.TransferringBranchOption | All branches | New create header, option omitted, and TransferringBranchName omitted or blank | No | resolve_branch_option |
| ORA_AP_BANK_CHARGE.ReceivingBankOption | All banks | New create header, option omitted, and ReceivingBankName omitted or blank | No | resolve_bank_option |
| ORA_AP_BANK_CHARGE.ReceivingBranchOption | All branches | New create header, option omitted, and ReceivingBranchName omitted or blank | No | resolve_branch_option |
| ORA_AP_BANK_CHARGE.LegalEntityName | All | New create header and both LegalEntityName and LegalEntityIdentifier omitted or blank | No | resolve_legal_entity |

The seven rows above are executable FSCR create defaults. LegalEntityIdentifier
remains blank when LegalEntityName defaults to All. Other header references,
all line scalar fields, and all header and line flexfields have no FSCR default.

## Task Nodes

This table is required compiler metadata for the executable rule registry.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BKC.DEFAULTS | step | 40 | apply_default | pass->BKC.DESIGN;fail->BKC.ERROR | BKC.DEPENDENCIES | stop | true |
