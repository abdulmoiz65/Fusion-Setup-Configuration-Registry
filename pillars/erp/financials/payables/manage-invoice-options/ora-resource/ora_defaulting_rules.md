# Defaulting Rules

## Defaults

| Field(s) | Default value | Applies when | Explicit request | Handling |
|---|---|---|---|---|
| TermsDateBasis | `Invoice` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| GlDateFromReceiptFlag | `INVOICE` (Invoice date) | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| PayDateBasisLookupCode | `DISCOUNT` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| BudgetDateBasis | `ACC` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| DiscountDistributionMethod | `SYSTEM` (Single distribution) | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| AutoCalculateInterestFlag; ProrateIntInvAcrossDists | `N`; `N` (Single distribution) | Fusion initializes a new record; setting AutoCalculateInterestFlag to `Y` also defaults proration to `N` | Preserved; never replaced | Fusion default behavior |
| ApprovalWorkflowFlag; AllowForceApprovalFlag; ValidateBeforeApprovalFlag | `N`; `N`; `N` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| AlwaysTakeDiscFlag; DiscIsInvLessTaxFlag; ExcludeFreightFromDiscount | `N`; `N`; `N` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| AllowFinalMatchFlag; AllowFlexOverrideFlag; AllowPaidInvoiceAdjust; InvDocCategoryOverride; TransferDescFlexFlag | `N`; `N`; `N`; `N`; `N` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| BuildPrepaymentAccountsFlag; PrepaymentAvailableMesgFlag; RecalcPayScheduleFlag | `N`; `N`; `N` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |
| AllowInvThirdPartyOvrd; RoutingFlag; AttachmentMandatorySsFlag; DisallowAttachmentDelFlag | `N`; `N`; `N`; `N` | Fusion initializes a new record | Preserved; never replaced | Fusion default behavior |

## Defaulting Boundary

These are Fusion initialization defaults. For a create candidate, apply the
required Terms Date Basis, Accounting Date Basis, Pay Date Basis, and Budget
Date Basis values when omitted. For an existing business-unit record, preserve
the exported current value. Never replace a blank or omitted update value with
a default.
