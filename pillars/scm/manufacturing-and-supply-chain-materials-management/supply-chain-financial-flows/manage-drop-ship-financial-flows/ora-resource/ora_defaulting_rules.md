# Defaulting Rules

Source: developer-provided create-record contract.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AgreementType | DROP_SHIP | Every create request | No; this is a fixed value | |
| Status | DRAFT | Every create request | No; this is a fixed header value | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.DSF.APPLY-CREATE-DEFAULTS | step | 3 | apply_default | applied->FOS.DSF.CONFIRM-LOADER-READINESS;invalid_override->RETURN-ISSUES | FOS.DSF.CHECK-NAME-AVAILABLE | stop | Every agreement header create request |
