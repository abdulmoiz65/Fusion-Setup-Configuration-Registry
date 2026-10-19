# Organization Payment Methods Defaulting Rules

OPM.APPLY_DEFAULTS must retain the original supplied values for the mandatory checks owned by OPM.ENFORCE_HDL_DESIGN in ora_design_enforcement.md. Defaults and name-to-code derivation must never erase evidence of a prohibited change or an inherited-field conflict. Apply the existing payment-information precedence defaults only within the scope permitted by those design rules.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Default payment source | The first payment source may become the default payment source | The first payment source is created in the OPM user flow | Yes | |
| Payment-source level payment information | Payment-source-level value takes priority over the OPM-level value | Both levels contain payment information | No | |
| Default payment method rule | No default rule is required | OPM is submitted without a default rule or with no payment source | Yes | |
| Category | Derive from the selected Payment Type LOV | Payment Type is selected or changed | No | resolve_payment_type_by_legislation |
| Payment-source CurrencyCode | Copy the parent OPM CurrencyCode | A payment source is included in an explicitly requested REST payload | No | |
| Payment-source PaymentTypeId | Copy the parent OPM PaymentTypeId | A payment source is included in an explicitly requested REST payload | No | |
| Context-free default payment method rule | Set PMR DefaultValue to Y and omit TaxUnitId | The user explicitly directs that no legal organization, payroll, or TRU context is required | No | |

## FSCR Project DAT Defaults

These project-supplied defaults apply only during DAT preparation. They supplement the existing defaults and do not replace any existing instruction.

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| OrganizationPaymentMethodCode | Copy OrganizationPaymentMethodName exactly | The source provides OrganizationPaymentMethodName and no explicit OrganizationPaymentMethodCode | Yes | |
| PaymentSourceCode | Copy PaymentSourceName exactly | The source provides PaymentSourceName and no explicit PaymentSourceCode | Yes | |
| SourceSystemOwner | Omit | Every DAT preparation | No | |
| SourceSystemId | Omit | Every DAT preparation | No | |

## Mandatory Name-to-Code Derivation

These supplemental rules are mandatory and preserve the existing FSCR Project DAT Defaults above.

| Field | Required Derivation | Interaction Rule | Stop or Confirmation Rule |
|---|---|---|---|
| OrganizationPaymentMethodCode | Copy the value from `OrganizationPaymentMethodName` exactly when `OrganizationPaymentMethodCode` is not supplied. | Treat the derived value as available for continued processing. | Never prompt for, stop for, or request confirmation of an omitted Organization Payment Method Code. |
| PaymentSourceCode | Copy the value from `PaymentSourceName` exactly when `PaymentSourceCode` is not supplied. | Treat the derived value as available for continued processing. | Never prompt for, stop for, or request confirmation of an omitted Payment Source Code. |

## Observed Payment-Source Rule Defaulting

These developer-supplied observations describe the Fusion OPM user flow. They supplement the existing defaults and do not replace the HDL preparation or approval rules.

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Default payment method rule for the first payment source | Fusion creates a default rule for the first payment source | The first payment source is created in the OPM user flow | Yes; the user can delete the generated rule and submit the OPM without a rule | |
| Default payment method rule for an additional payment source | Do not create another default rule automatically | A second or later payment source is created | Yes; the user can explicitly define a valid rule subject to the payment-rule constraints | |
| Rule requirement for a payment source | No rule is created or required automatically after the generated first-source default rule is deleted | A payment source remains in the OPM without a payment method rule | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPM.APPLY_DEFAULTS | step | 7 | apply_default | applied->OPM.VALIDATE_PRENOTIFICATION | OPM.VALIDATE_PRENOTIFICATION_SELECTION | stop | The supplied operation needs documented defaults |
