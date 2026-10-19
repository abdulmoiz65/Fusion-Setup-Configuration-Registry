# Manage Sourcing Notifications Design Enforcement

Sources: user-provided screenshot **Screenshot 2026-09-24 at 7.57.00 PM.png**, reviewed on 2026-09-24.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Restrict notification updates | Allow updates only to the three Enable checkboxes shown for the selected notification: Auction, RFQ, and RFI. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Updating a Sourcing Notification Subscription | Blocker |  | The update includes InternalRecipientEnabledFlag, ExternalRecipientEnabledFlag, any recipient value, or a requested mutable field other than AuctionEnabledFlag, RequestForQoutationEnabledFlag, or RequestForInformationEnabledFlag. | Preserve the Internal and External recipient indicators and submit only the selected Auction, RFQ, and RFI enable-flag values. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SOURCING_NOTIFICATION.ENFORCE_EDITABLE_ENABLE_FLAGS | step | 15 | design_enforcement | compliant->SOURCING_NOTIFICATION.RETURN_VALIDATION_READY;noncompliant->RETURN_ISSUES | SOURCING_NOTIFICATION.VALIDATE_CAPABILITY_MATRIX | stop | A notification update request is limited to the screenshot-defined Auction, RFQ, and RFI Enable checkboxes. |
