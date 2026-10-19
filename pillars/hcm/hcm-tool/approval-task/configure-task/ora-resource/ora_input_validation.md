# Input Validation

## Source Material

- Developer-supplied exported Word document: HCM Config Task UI screenshots and REST calls for BPM based flows.
- Developer-supplied task-configuration JSON sample for writeTaskConfiguration.
- [How You Define Approvals for Human Capital Management](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-define-approvals-for-human-capital-management.html#Managing-Approval-Transactions)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Approval process selection | Exact approval_process name | Return APPROVAL_PROCESS_REQUIRED. | Provide the exact process name used by the approval-options finder. | Every read, preview, or write request |  |
| Requested configuration scope | Explicit requested changes for notifications, reminders, aggregation, participant actions, or another documented task setting | Return CONFIGURATION_SCOPE_REQUIRED. | State the settings and intended outcomes to configure. | Every preview or write request |  |
| Complete task configuration | Json containing the complete approved task configuration serialized as a string | Return TASK_CONFIGURATION_JSON_REQUIRED. | Read the current task configuration, retain every unchanged setting, and apply only the approved changes. The internal HCM Config Task export defines the required serialized-object shape; its sample values are not target defaults. | writeTaskConfiguration preview or write requested |  |
| Commit indicator | commitNeededFlag set to true or false | Default to true only when the requester has not supplied a value. | Supply true or false. | writeTaskConfiguration preview or write requested |  |

## JSON Structural Contract

Treat the supplied JSON as a structural example only. It is not a payload
template or a source of defaults for a different approval process. Build the
serialized `Json` value from the complete current configuration returned for
the resolved processId, then apply only the reviewed changes.

| JSON Section | Required Shape | Validation Guidance | Applies When |
|---|---|---|---|
| Root configuration | One complete JSON object serialized into the `Json` string field | Reject a JSON object sent in place of the serialized string, invalid JSON, or a partial patch. Preserve every current root member that is not part of the approved change. | writeTaskConfiguration preview or write requested |
| accessList | Object keyed by task action; each action value is an object keyed by actor category | Preserve all returned action and actor-category entries. For entries represented in the supplied sample, values are the uppercase policy literals PERMIT or RESTRICT; do not add, remove, or change an entry without explicit review. | The target current configuration includes accessList |
| notificationActions | Array of notification-action objects | Preserve ordering and every returned item unless a reviewed change identifies the item. Each supplied-example item contains excludeNotificationPrefix, header, recipient, and status; preserve their JSON types and literal values, including the string literal `null` when the current configuration uses it. | The target current configuration includes notificationActions |
| taskLevelConfigMap | Object containing task-level settings | Preserve every returned setting. Validate ISO-8601 duration strings where used, documented enum/literal values where used, nullable values where currently null, and the exact JSON type returned for each setting. Do not coerce string booleans such as `true` or `false` into JSON booleans unless the current configuration itself uses booleans. | The target current configuration includes taskLevelConfigMap |

## Sample-Derived Task-Level Fields

The sample demonstrates these task-level field families. This list is a
review aid, not a complete-schema assertion: a target response can include
additional fields that must remain in the complete serialized configuration.

| Field Family | Sample-Derived Fields | Validation Guidance | Applies When |
|---|---|---|---|
| Participant and outcome controls | allowInitiatorEditParticipants, allowParticipantsEditFutureParticipants, ApprovalPre-conditionsForMandateCommentsBeforeUpdatingOutcomes, allowAllParticipantsRouteTask | Retain the exact current field names and values unless the approved scope explicitly changes them. | Field exists in the current taskLevelConfigMap |
| Schedule, escalation, reminder, and renewal | dueDateDuration, escalationLevels, expirationDurationAtTask, expirationDurationType, isDueDateEnabled, isReminderEnabled, reminderDuration, reminderRecurrenceTimes, reminderRelativeDate, isExpirationEscalate, isExpirationMoveForward, isExpirationRenewal, renewalTimes | Validate durations as ISO-8601 strings and preserve null versus non-null state and related scheduling flags as returned. | Field exists in the current taskLevelConfigMap |
| Assignment and notification controls | isAssignToUsersManager, isAutoClaimEnabled, isExcludeSaturdayAndSunday, isGroupNotificationConfig, isHideEndUserURL, isMakeNotificationActionable, isNotificationSecured, isOneNotificationPerUserPerAction, isSendTaskAttachmentWithEmail, senderNameSource | Treat each value and type as process-specific. A request to enable one setting, such as auto claim, must not replace neighboring controls with the sample values. | Field exists in the current taskLevelConfigMap |
| Approval behavior and payload exclusions | isEscalateOrRenewOnlyAtLastAssignee, isSkipUserAsApproverDisabled, isTaskAggregate, UserNamesInPayloadAttributesToSkipForApproval | Preserve the exact current literals and blank-string values unless included in the approved scope. | Field exists in the current taskLevelConfigMap |

## Reference-Validated Deadline and Aggregation Literals

The user-supplied, environment-generated task configuration reference was
inspected locally without retaining its complete contents. For a target whose
corresponding fields are strings, it validates the following serialization:

| Requested behavior | Field | Reference-validated string value |
|---|---|---|
| Once per Task aggregation | `isTaskAggregate` | `TASK` |
| Enable a one-day due date | `isDueDateEnabled`; `dueDateDuration` | `true`; `P1DT0H0M0S` |
| Task-level two-day expiration | `expirationDurationType`; `expirationDurationAtTask` | `STATIC`; `P2DT0H0M0S` |
| Escalate once at expiration | `isExpirationEscalate`; `escalationLevels` | `true`; `1` |
| Exclude weekends | `isExcludeSaturdayAndSunday` | `true` |

Use these literals only after a fresh target read confirms the matching fields.
The target may have null `dueDateDuration`, `expirationDurationType`,
`expirationDurationAtTask`, and `escalationLevels` before the policy is first
enabled; the reference validates their explicit null-to-string transition.
Preserve every other returned field unchanged.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| approval_process is present and nonblank | Continue to the exact approval-process lookup. | Every request | find_approval_process_by_name |
| Json is present and represents the complete approved configuration, including notificationActions and taskLevelConfigMap and preserving accessList when returned for the target | Continue to the mutation design gate. | writeTaskConfiguration preview or write requested |  |
| Json is a JSON-encoded string and parses to exactly one root object | Continue to the mutation design gate. Do not accept an object-valued request field or a double-encoded JSON string. | writeTaskConfiguration preview or write requested |  |
| Json retains all root members and all returned accessList, notificationActions, and taskLevelConfigMap members outside the approved diff | Continue to the mutation design gate. Reject a configuration built from the supplied sample alone or a request that omits unchanged target values. | writeTaskConfiguration preview or write requested |  |
| Each changed notificationActions item retains its required current shape and JSON types | Continue to the mutation design gate. Reject a change that normalizes a current string literal `null`, drops an item property, or changes an unapproved item. | notificationActions change requested |  |
| Each changed taskLevelConfigMap value retains its current JSON type; duration values remain ISO-8601 durations | Continue to the mutation design gate. Reject type coercion, an invalid duration, or an unapproved neighboring setting change. | task-level setting change requested |  |
| commitNeededFlag is true or false | Continue to the mutation design gate. | writeTaskConfiguration preview or write requested |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TASK_CONFIG.VALIDATE_INPUT | decision | 1 | validate_input | valid->TASK_CONFIG.FIND_APPROVAL_PROCESS;missing->TASK_CONFIG.MISSING_INPUT | none | stop | Every request |
