# Financial Orchestration Flows defaults

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveEndDate | 4712-12-31 | Create when omitted; show in preview | No |  |
| Status | Let Fusion default DRAFT or preserve explicit DRAFT; do not send an activation request | Parent-only create | No |  |
| AutoActiveFlag | Omit when unspecified; disclose REST VO default Y and verify saved value | Create | No |  |
| MultiFinancialtradeRelationFlag | Omit; entity expression derives system option or N | Create | No |  |
| Priority | Preserve the current resolved Priority when no new value is requested; always include it in correction input. This is readback preservation, not a numeric default | Correction only | No | resolve_flow_agreement |
| Insert preservation | Preserve selected version Priority, Status=DRAFT and end date; require explicit new start and changed Description | Insert | No | resolve_flow_agreement_version |
| Description and QualifierRuleSetId | No invented defaults; omit if unspecified | Create or correction | No |  |
| Drop Ship Supplier Ownership Change Event | No default; leave DropshipForwardOwnershipChangeEventId unpopulated | PROCUREMENT Agreement create when the user omits the event | No; preserve any explicitly selected supported event |  |
| Procurement FTR selling trade organization | Select the first enabled organization in each FTR's selling-BU-scoped LOV order when omitted; do not use the BU relationship's DefaultTradeOrganizationId | Every FTR in a new PROCUREMENT PTR chain | No | resolve_flow_trade_org |
| First Shipment FTR selling trade organization | Leave FromTradeOrganization unpopulated when omitted | First FTR in a new SHIPMENT PTR chain | No |  |
| First Internal Transfer FTR selling trade organization | Leave FromTradeOrganization unpopulated | First FTR in a new INTERNAL_TRANSFER PTR chain | No |  |
| Later Internal Transfer FTR selling trade organization | Use that FTR selling BU relationship's DefaultTradeOrganizationId, verified in that BU | Every INTERNAL_TRANSFER FTR after the first when selling organization is omitted | No | resolve_flow_trade_org |
| Later FTR selling trade organization | Use the preceding FTR's resolved ToTradeOrganization, verified in this FTR's selling BU | Each FTR after the first in a new PTR chain except Internal Transfer, Procurement and Nonshippable Sales when selling organization is omitted | No | resolve_flow_trade_org |
| FTR buying trade organization | Use the buying BU relationship's DefaultTradeOrganizationId, verified in that BU | Each INTERNAL_TRANSFER or PROCUREMENT FTR except the last; or every FTR of other applicable flow types outside Nonshippable Sales, when buying organization is omitted | No | resolve_flow_trade_org |
| Last Procurement FTR buying trade organization | Leave ToTradeOrganization unpopulated | Last FTR of every PROCUREMENT PTR, including a single-FTR PTR | No |  |
| Last Internal Transfer FTR buying trade organization | Leave ToTradeOrganization unpopulated | Last FTR of every INTERNAL_TRANSFER PTR, including a single-FTR PTR | No |  |
| FTR derived parent-date helpers | If the fresh FTR template exposes ParentEffectiveStartDate or ParentEffectiveEndDate, retain each exposed column with a blank row value; do not add a missing column. Data Loader derives both URL values from AgreementId before forming the nested FTR URL | Existing FTR correction only when fresh deployed metadata verifies both foreign-key derivations and URL placeholders | No | resolve_flow_child_registration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOF.CHECK_DEFAULTS | step | 360 | apply_default | success->FOF.LOOKUP_PROCUREMENT_OWNERSHIP_EVENT;failure->FOF.RETURN_ISSUES | FOF.CHECK_DEPENDENCIES | stop | Apply applicable Agreement and new-FTR trade-organization defaults/preservation; never default creation fields for PTR deletion |
