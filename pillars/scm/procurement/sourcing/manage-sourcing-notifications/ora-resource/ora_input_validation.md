# Manage Sourcing Notifications Input Validation

Sources: user-authorized inspection of the **Manage Sourcing Notifications** task page in a configured Fusion environment on 2026-09-22; live Data Loader sample and attribute-details workbooks for **Sourcing Notification Subscription** on 2026-09-23; user-provided screenshot **Screenshot 2026-09-24 at 7.57.00 PM.png**, reviewed on 2026-09-24.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| New notification subscription identity | NotificationId, NotificationType, NotificationTypeCode, and RestAction | Reject the source before preview | Supply every live-template field marked required for new records. Preserve the documented user-key alternatives: NotificationId / NotificationTypeCode and NotificationTypeCode / NotificationType. | Creating a Sourcing Notification Subscription through Data Loader |  |
| Notification enable update scope | Existing notification identity and one or more of AuctionEnabledFlag, RequestForQoutationEnabledFlag, or RequestForInformationEnabledFlag | Reject the source before preview | Supply only the requested Auction, RFQ, or RFI enable-flag values for the selected notification. Do not include recipient fields. | Updating a Sourcing Notification Subscription through Data Loader |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| NotificationId | Accept a string of no more than 18 characters. Use it with the live user-key alternative NotificationTypeCode. | Creating a Sourcing Notification Subscription through Data Loader |  |
| NotificationType | Accept a string of no more than 80 characters. The live metadata classifies it as a foreign key and identifies NotificationTypeCode as its user-key alternative. | Creating a Sourcing Notification Subscription through Data Loader |  |
| NotificationTypeCode | Accept a string of no more than 30 characters. The live metadata classifies it as a user key and foreign key. | Creating a Sourcing Notification Subscription through Data Loader |  |
| RestAction | Require a string of no more than 10 characters. The live create sample uses POST. | Creating a Sourcing Notification Subscription through Data Loader |  |
| Subscription enable flags | Validate AuctionEnabledFlag, RequestForQoutationEnabledFlag, and RequestForInformationEnabledFlag as optional strings of no more than one character. Preserve the live template's exact field names, including RequestForQoutationEnabledFlag. The screenshot labels these controls Auction, RFQ, and RFI. | Creating or updating a Sourcing Notification Subscription through Data Loader |  |
| Recipient fields on update | Reject InternalRecipientEnabledFlag, ExternalRecipientEnabledFlag, recipient values, and any requested mutable field outside the three documented enable flags. Internal and External are recipient indicators in the screenshot, not update controls. | Updating a Sourcing Notification Subscription through Data Loader |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SOURCING_NOTIFICATION.VALIDATE_CAPABILITY_MATRIX | step | 10 | validate_input | valid->SOURCING_NOTIFICATION.ENFORCE_EDITABLE_ENABLE_FLAGS;invalid->RETURN_ISSUES | none | stop | A Manage Sourcing Notifications Data Loader source is ready for validation. |
