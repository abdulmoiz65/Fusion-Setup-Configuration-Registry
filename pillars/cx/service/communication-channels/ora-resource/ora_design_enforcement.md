# Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | 10 | Confirm channel prerequisites | Validate ChannelTypeCd, StripeCd, and PurposeCd through their Common lookups; resolve BUOrgId through the Business Unit skill; then confirm email forwarding and outbound SPF readiness when applicable before preview |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | 10 | Confirm filter priority and pattern effect | Filter order and regular expression behavior must be reviewed because rejected messages cannot be reprocessed by the application |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | 10 | Protect email processing, identity, and thread settings | Review the requested value for attachment-size, acknowledgment-loop, From-address, and email-thread impact before approval |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | 10 | Confirm user experience policy | Redwood users must not be enabled for Digital Engagement Channels with Live Window unless an exception is approved |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | 10 | Protect support-only timing settings | Runtime dispatch retry and timing settings must not be changed unless Oracle Support instructed it |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | 10 | Confirm retention impact | Interaction retention must meet business retention policy before Purge Interactions relies on it |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Channel setup | Error | resolve_email_channel_by_code | ChannelShortName is not unique; required lookup codes or BUOrgId are unresolved; or email forwarding/SPF readiness is absent when applicable | Use the generated unique short name, validated lookup codes, resolved BUOrgId, and applicable readiness evidence before preview | Yes |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Lookup setup related to channel configuration | Error |  | New lookup type starts with ORA | Do not create lookup names that start with ORA because that prefix is reserved for seeded application lookups | Yes |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Inbound attachment size profile change | Warning | get_profile_option_definition | Requested total email size can exceed the documented recommended 15 MB envelope | Keep inbound attachment settings within the documented email-size constraints | Yes |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Inbound acknowledgment profile change | Warning | get_profile_option_definition | Acknowledgment limits or stop patterns are missing where inbound loops are possible | Set limit, interval, and stop-pattern values together | Yes |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Outbound From address profile change | Warning | get_profile_option_definition | Company From address is not verified or inbox access is not confirmed | Use a no-reply address that the company can verify, or keep an Oracle-supported address until verification is complete | Yes |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Email-thread conversation count change | Warning | get_profile_option_definition | Requested past-conversation count is outside the supported 0 to 10 range | Use a value from 0 to 10 for SVC_EMAIL_NO_OF_PAST_CONVERSATIONS | Yes |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Inbound message filter create or update | Error | find_inbound_message_filter_by_alt_key | Pattern, action, or priority can reject legitimate emails without review | Review examples and message priority before approval; rejected messages cannot be reprocessed by the application | Yes |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | ORA_SVC_ENABLE_DEC_WITH_LIVEWINDOW change | Error | get_profile_option_definition | Redwood agents would receive value Yes without an exception | Use No for Redwood agents; restrict Yes to explicitly approved Classic Fusion exceptions | Yes |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Runtime event dispatch timing profile changes | Error | get_profile_option_definition | Requested change lacks Oracle Support instruction | Keep timing defaults and stop for Support guidance | No |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Sales for Redwood MCA settings | Error | get_profile_option_definition | SVC_MCA_DISABLE_OUTBOUND_WRAP_UP is not enabled or SVC_MCA_RECORD_ACTIVITIES_YN is not disabled for Sales for Redwood | Apply the documented Sales for Redwood settings before approval | Yes |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | SVC_INTERACTION_RETENTION_DAYS change | Error | get_profile_option_definition | Retention days is blank or less than 1 | Provide a retention value of 1 or greater that matches the retention policy | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | resolve_email_channel_by_code | Email channel create or update preview | ChannelCode and duplicate status | ora_reference_lookups.md |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | resolve_channel_type_code | New or changed ChannelTypeCd | Validated ChannelTypeCd | ora_reference_lookups.md |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | resolve_stripe_code | New or changed StripeCd | Validated StripeCd | ora_reference_lookups.md |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | resolve_channel_purpose_code | New or changed PurposeCd | Validated PurposeCd | ora_reference_lookups.md |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | resolve_business_unit_org_id | New or changed BUOrgId | BUOrgId and BusinessUnitIdFK | ora_reference_lookups.md |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | find_inbound_message_filter_by_alt_key | Inbound message filter create or update preview | FilterId and duplicate status | ora_reference_lookups.md |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | resolve_inbound_filter_lookup_codes | Inbound message filter create or update preview | Enabled FilterTypeCd and ActionCd values | ora_reference_lookups.md |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | get_profile_option_definition | Profile option value preview | Definition, enabled levels, and updatable flags | ora_reference_lookups.md |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | get_profile_option_definition | Profile option value preview | Definition, enabled levels, and updatable flags | ora_reference_lookups.md |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | get_profile_option_definition | Profile option value preview | Definition, enabled levels, and updatable flags | ora_reference_lookups.md |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | get_profile_option_definition | Profile option value preview | Definition, enabled levels, and updatable flags | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | COMM.DESIGN | step | 30 | design_enforcement | read_ready->COMM.DONE;mutation_ready->COMM.APPROVAL_GATE;blocked->RETURN_ISSUES | COMM.LOOKUP | stop | Email channel design gates must be checked |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | EMAILPROFILE.DESIGN | step | 30 | design_enforcement | pass->EMAILPROFILE.APPROVAL_GATE;blocked->RETURN_ISSUES | EMAILPROFILE.LOOKUP | stop | Email profile option design gates must be checked |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.DESIGN | step | 40 | design_enforcement | pass->FILTER.APPROVAL_GATE;blocked->RETURN_ISSUES | FILTER.PREFLIGHT | stop | Inbound message filter design gates must be checked |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | OMNI.DESIGN | step | 30 | design_enforcement | pass->OMNI.APPROVAL_GATE;blocked->RETURN_ISSUES | OMNI.LOOKUP | stop | Omnichannel profile option design gates must be checked |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | MCA.DESIGN | step | 30 | design_enforcement | pass->MCA.APPROVAL_GATE;blocked->RETURN_ISSUES | MCA.LOOKUP | stop | MCA profile option design gates must be checked |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | INTERACT.DESIGN | step | 30 | design_enforcement | pass->INTERACT.APPROVAL_GATE;blocked->RETURN_ISSUES | INTERACT.LOOKUP | stop | Interaction profile option design gates must be checked |
