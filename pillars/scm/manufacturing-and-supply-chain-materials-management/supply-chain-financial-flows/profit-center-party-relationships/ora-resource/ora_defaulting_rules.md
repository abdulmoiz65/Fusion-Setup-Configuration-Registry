# PCBU defaulting rules

Operation scope: historical parent-only restrictions below apply to parent-create/header-update. For buyer-create/buyer-edit/buyer-delete or seller-create/seller-edit/seller-delete, evaluate the respective profile sections and their transport gate instead; shared identity, environment and artifact rules still apply.


Evidence: source PayablesBuAssignmentEO.xml Attribute InterCompanyPurchaseFlag declares DefaultValue=N and BooleanYNPropertySet, with a Y/N list validator. This does not prove Data Loader wire encoding or all create paths. Do not infer Y from the Redwood buyer-profile title. EnterpriseId is not a developer-configurable tenant choice in this draft.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Optional header selections | No default selection; leave explicitly blank supplier, customer, trade organization and ship-to unset | Parent create with an explicitly blank optional input | No | |

For header update, omitted fields mean unchanged. Do not serialize blank optional columns, copy all existing values, clear fields, derive defaults, or replace identity. Clearing any header field is unsupported. If all selected values equal the existing values, return a no-change result and stop before upload; do not submit a no-op test.

## Child default evidence

The EO declares a storage default of N for InterCompanyPurchaseFlag and setter-derived receivables reference-set IDs. Do not serialize these as guessed defaults. Follow the buyer and seller rules below, verify target omission behavior and read back derived values. These fields are not defaults for parent header operations.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCBU.CHECK_DEFAULTS | step | 40 | apply_default | success->PCBU.CHECK_DESIGN;failure->PCBU.RETURN_ISSUES | PCBU.CHECK_DEPENDENCIES | stop | Operation-specific scope: preserve unspecified fields without changing the prepared artifact |

## Buyer defaults and preservation

For create, require both BU selections; do not default procurement or bill-to BU from the PCBU name. Omitted optional party-site and address rows remain omitted. Do not send InterCompanyPurchaseFlag: the EO declares N, while Redwood omits this field. Verify target transport behavior without forcing Y from the word Intercompany.

For edit, omitted fields and rows remain unchanged. Revalidate bill-to BU after procurement changes and bill-to location after address-set changes. A caller's request to delete one bill-to row does not delete the buyer profile. A request to delete the profile uses its child identity and includes cascade impact review. Do not copy Redwood's null fallback onto omitted input: the UI submits a complete form, while a conversational edit may specify one field only.

## Seller defaults and preservation

Do not default receivables BU, buyer procurement BU, buyer bill-to BU or supplier site from the parent name. Preserve omitted fields and rows on edit; revalidate dependent LOV selections after changes. Do not derive a site ID from a numeric-looking site code.

Redwood sends only IntercompanyReceivablesBUId for the assignment, not the selected set ID. REST row create looks up a set from the parent BU; the EO setter derives the intercompany customer address set from the selected receivables BU. Do not reproduce either by guessing setter order or writing ICReceivablesCustomerAddrSetid. Resolve the LOV context, then verify the resulting set after execution. A mismatch blocks completion.

Do not copy Redwood's null fallback for absent row fields into a partial conversational edit. Required row selections must remain populated. The unused ReceivablesBUId is not interchangeable with IntercompanyReceivablesBUId.
