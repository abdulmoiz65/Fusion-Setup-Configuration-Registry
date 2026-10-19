# Manage Sourcing Notifications Error Handling

Sources: user-authorized inspection of the **Manage Sourcing Notifications** task page in a configured Fusion environment on 2026-09-22; live Data Loader sample for **Sourcing Notification Subscription** on 2026-09-23; user-provided screenshot **Screenshot 2026-09-24 at 7.57.00 PM.png**, reviewed on 2026-09-24.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A notification name, control, recipient value, or field-to-control mapping cannot be validated from the documented source | Reject the source before preview. Obtain the current Data Loader sample and the exact REST field mapping before retrying validation. |
| A notification update includes a recipient indicator or an unsupported field | Reject the source before preview. Preserve the Internal and External recipient indicators and submit only Auction, RFQ, and RFI enable-flag values. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Notification update governance failure | The requested update is outside the three screenshot-defined Enable checkboxes. | Remove recipient and unsupported fields, then revalidate the source. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Notification update governance failure | The disallowed recipient or unsupported field and the allowed Auction, RFQ, and RFI enable-flag fields. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| An update contains a recipient indicator or unsupported field | Do not preview, approve, or submit it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SOURCING_NOTIFICATION.RETURN_VALIDATION_READY | terminal | 20 | terminal | none | SOURCING_NOTIFICATION.ENFORCE_EDITABLE_ENABLE_FLAGS | stop | The source passes validation and the notification-update design gate. |
| RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | The source is missing or fails a documented validation requirement. |
