# Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Channel lookup returns an error or resolves multiple channels for the requested ChannelCode | Stop, preserve sanitized diagnostics, and correct the lookup input before any preview |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Forwarding, access-point registration, or SPF readiness is missing | Stop before preview and ask for the missing readiness evidence |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Profile definition is missing, not updatable at the requested level, value validation fails, or From-address verification is rejected | Stop, show the profile option code and requested level, and do not retry a value write or switch addresses without a new preview |
| ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS | Manage Inbound E-Mail Profile Options | Inbound profile option definition, supported level, or value is unresolved | Stop and route to Manage Email Profile Options; do not create or change a profile option definition |
| ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS | Manage Outbound E-Mail Profile Options | Outbound profile option definition, supported level, or value is unresolved | Stop and route to Manage Email Profile Options; do not create or change a profile option definition |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Inbound filter lookup, lookup-code validation, duplicate preflight, FSM package validation, or import fails | Stop, preserve sanitized diagnostics, do not retry an FSM import, and do not reorder filters implicitly |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | Profile value update or Omnichannel event retention setup is rejected | Stop, show sanitized diagnostics, and do not run Purge Omnichannel Events as a workaround |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Requested MCA timing or Sales for Redwood setting conflicts with documented design rules | Stop before preview and request corrected values or Oracle Support evidence |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS | Manage Service Assignment Objects | Assignment object contract is TBD | Stop and request a documented operation contract |
| ORA_SVC_MANAGE_SERVICE_ZONES | Manage Service Regions | Service region contract is TBD | Stop and request a documented operation contract |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES | Manage Service Assignment Rules | Assignment rule contract is TBD | Stop and request a documented operation contract |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | Retention value is missing, less than 1, or profile value update is rejected | Stop, show sanitized diagnostics, and do not run Purge Interactions as a workaround |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | FSM package validation or import failure | A create or update package is rejected during validation or import | Preserve sanitized diagnostics, do not retry the import, and correct the approved FSM package before a new approval |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Duplicate filter | Alternate-key preflight finds an existing filter during create | Use update flow or change the pattern, action, or filter type |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Invalid lookup code | FilterTypeCd or ActionCd is not enabled in its standard lookup | Select an enabled documented lookup code |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Fusion lookup or FSM package failure | A read-only lookup, package validation, or import returns an error | Preserve request identity and sanitized diagnostics; stop before retry |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Profile value blocked | Definition is not updatable at requested level, value validation fails, or From-address verification is unresolved | Correct the level, value, or verification readiness and preview again |
| ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS | Manage Inbound E-Mail Profile Options | Routed profile value blocked | Resolve the approved existing profile option, supported level, and requested value through Manage Email Profile Options | Do not infer a profile definition or create it through the inbound task |
| ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS | Manage Outbound E-Mail Profile Options | Routed profile value blocked | Resolve the approved existing profile option, supported level, and requested value through Manage Email Profile Options | Do not infer a profile definition or create it through the outbound task |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | Profile value blocked | Definition is not updatable at requested level or design rule blocks the value | Correct the level or value and preview again |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Profile value blocked | Definition is not updatable or Oracle Support-only values are requested without evidence | Correct the value or attach Support instruction |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | Retention blocked | SVC_INTERACTION_RETENTION_DAYS is blank, less than 1, or update is rejected | Provide a valid retention policy value and preview again |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Preview | ChannelTypeCd, StripeCd, PurposeCd, AccountName, ChannelShortName, EnabledFlag, BusinessUnitName, forwarding readiness, SPF readiness, and lookup result |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Preview | FilterTypeCd, FieldName, Pattern, ActionCd, CustomFilterFlag, DeletedFlag, OrderNumber, defaults applied, duplicate preflight result, and priority warning |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Preview | ProfileOptionName, level, current value, requested value, enabled/updatable flags, applicable loop or size warnings, From-address verification readiness, and email-thread impact |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | Preview | ProfileOptionName, level, current value, requested value, Redwood exception status, and retention implications |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Preview | ProfileOptionName, level, current value, requested value, Sales for Redwood applicability, and Oracle Support-only settings |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | Preview | ProfileOptionName, level, current value, requested value, retention policy, and purge impact |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | Exact FSM import artifact approval is missing, channel identity is unresolved, or deletion is requested | Do not import a communication-channel package; channel deletion remains outside the supported FSM workflow |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | Request changes a profile option definition or uses an unverified From address as ready | Do not change profile definitions or claim outbound email readiness without verification |
| ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS | Manage Inbound E-Mail Profile Options | Request creates, changes, or deletes a profile option definition | Do not create, update, or delete a profile option definition; route supported value work to Manage Email Profile Options |
| ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS | Manage Outbound E-Mail Profile Options | Request creates, changes, or deletes a profile option definition | Do not create, update, or delete a profile option definition; route supported value work to Manage Email Profile Options |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | Exact FSM import artifact approval is missing or duplicate preflight is unclear | Do not import an inbound message filter package |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | Request changes a profile option definition or bypasses Redwood Live Window rule | Do not change profile definitions or set blocked values |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | Oracle Support-only values are requested without evidence | Do not change runtime dispatch timing profile values |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS | Manage Service Assignment Objects | Operation contract is TBD | Do not create or update assignment objects |
| ORA_SVC_MANAGE_SERVICE_ZONES | Manage Service Regions | Operation contract is TBD | Do not create or update service regions |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES | Manage Service Assignment Rules | Operation contract is TBD | Do not create or update assignment rules |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | Retention value is blank or less than 1 | Do not update retention profile options or run purge as a workaround |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | COMM.APPROVAL_GATE | decision | 40 | execution_gate | approved->COMM.READY;denied->COMM.REFUSED | COMM.DESIGN | stop | The exact Communication Channels FSM import artifact is ready for approval |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | COMM.READY | terminal | 41 | terminal | none | COMM.APPROVAL_GATE | stop | Explicit approval permits one validated communication-channel FSM package import through core.data-loader |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | COMM.REFUSED | terminal | 42 | terminal | none | COMM.APPROVAL_GATE | stop | The communication-channel FSM import artifact was denied or approval was not granted |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | COMM.DONE | terminal | 90 | terminal | none | COMM.DESIGN | stop | Read-only Communication Channels guidance is ready for handoff |
| ORA_SVC_MANAGE_COMM_CHANNELS | Manage Communication Channels | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Communication Channels gate produces issues |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | EMAILPROFILE.APPROVAL_GATE | decision | 40 | execution_gate | approved->EMAILPROFILE.READY;denied->EMAILPROFILE.REFUSED | EMAILPROFILE.DESIGN | stop | The exact email profile-value FSM import artifact is ready for approval |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | EMAILPROFILE.READY | terminal | 41 | terminal | none | EMAILPROFILE.APPROVAL_GATE | stop | Explicit approval permits one validated email profile-value FSM package import through core.data-loader |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | EMAILPROFILE.REFUSED | terminal | 42 | terminal | none | EMAILPROFILE.APPROVAL_GATE | stop | The email profile-value FSM import artifact was denied or approval was not granted |
| ORA_MANAGE_EMAIL_PROFILE_OPTIONS | Manage Email Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any email profile option gate produces issues |
| ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS | Manage Inbound E-Mail Profile Options | INBOUNDPROFILE.DONE | terminal | 90 | terminal | none | INBOUNDPROFILE.VALIDATE | stop | Inbound email profile option guidance is routed to Manage Email Profile Options |
| ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS | Manage Inbound E-Mail Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any inbound email profile option gate produces issues |
| ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS | Manage Outbound E-Mail Profile Options | OUTBOUNDPROFILE.DONE | terminal | 90 | terminal | none | OUTBOUNDPROFILE.VALIDATE | stop | Outbound email profile option guidance is routed to Manage Email Profile Options |
| ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS | Manage Outbound E-Mail Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any outbound email profile option gate produces issues |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.APPROVAL_GATE | decision | 50 | execution_gate | approved->FILTER.READY;denied->FILTER.REFUSED | FILTER.DESIGN | stop | The exact inbound message filter payload is ready for approval |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.READY | terminal | 51 | terminal | none | FILTER.APPROVAL_GATE | stop | Explicit approval permits one validated FSM package import through core.data-loader |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.DUPLICATE | terminal | 52 | terminal | none | FILTER.PREFLIGHT | stop | A duplicate inbound message filter blocks creation |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.REFUSED | terminal | 53 | terminal | none | FILTER.APPROVAL_GATE | stop | The inbound message filter preview was denied or approval was not granted |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | FILTER.DONE | terminal | 90 | terminal | none | FILTER.LIST | stop | Inbound message filter collection guidance is ready for preview handoff |
| ORA_SVC_MANAGE_EMAIL_FILTERS | Manage E-Mail Filters | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any inbound message filter gate produces issues |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | OMNI.APPROVAL_GATE | decision | 40 | execution_gate | approved->OMNI.READY;denied->OMNI.REFUSED | OMNI.DESIGN | stop | The exact Omnichannel profile-value FSM import artifact is ready for approval |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | OMNI.READY | terminal | 41 | terminal | none | OMNI.APPROVAL_GATE | stop | Explicit approval permits one validated Omnichannel profile-value FSM package import through core.data-loader |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | OMNI.REFUSED | terminal | 42 | terminal | none | OMNI.APPROVAL_GATE | stop | The Omnichannel profile-value FSM import artifact was denied or approval was not granted |
| ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS | Manage Omnichannel Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Omnichannel profile option gate produces issues |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | MCA.APPROVAL_GATE | decision | 40 | execution_gate | approved->MCA.READY;denied->MCA.REFUSED | MCA.DESIGN | stop | The exact MCA profile-value FSM import artifact is ready for approval |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | MCA.READY | terminal | 41 | terminal | none | MCA.APPROVAL_GATE | stop | Explicit approval permits one validated MCA profile-value FSM package import through core.data-loader |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | MCA.REFUSED | terminal | 42 | terminal | none | MCA.APPROVAL_GATE | stop | The MCA profile-value FSM import artifact was denied or approval was not granted |
| ORA_MANAGE_MCA_PROFILE_OPTIONS | Manage MCA Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any MCA profile option gate produces issues |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS | Manage Service Assignment Objects | ASSIGNOBJ.DONE | terminal | 90 | terminal | none | ASSIGNOBJ.VALIDATE | stop | Assignment object guidance remains blocked until source contract is provided |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS | Manage Service Assignment Objects | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any assignment object gate produces issues |
| ORA_SVC_MANAGE_SERVICE_ZONES | Manage Service Regions | ZONE.DONE | terminal | 90 | terminal | none | ZONE.VALIDATE | stop | Service region guidance remains blocked until source contract is provided |
| ORA_SVC_MANAGE_SERVICE_ZONES | Manage Service Regions | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any service region gate produces issues |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES | Manage Service Assignment Rules | ASSIGNRULE.DONE | terminal | 90 | terminal | none | ASSIGNRULE.VALIDATE | stop | Assignment rule guidance remains blocked until source contract is provided |
| ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES | Manage Service Assignment Rules | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any assignment rule gate produces issues |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | INTERACT.APPROVAL_GATE | decision | 40 | execution_gate | approved->INTERACT.READY;denied->INTERACT.REFUSED | INTERACT.DESIGN | stop | The exact Interaction profile-value FSM import artifact is ready for approval |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | INTERACT.READY | terminal | 41 | terminal | none | INTERACT.APPROVAL_GATE | stop | Explicit approval permits one validated Interaction profile-value FSM package import through core.data-loader |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | INTERACT.REFUSED | terminal | 42 | terminal | none | INTERACT.APPROVAL_GATE | stop | The Interaction profile-value FSM import artifact was denied or approval was not granted |
| ORA_SVC_INTERACTION_PROFILE_OPTIONS | Manage Interaction Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Interaction profile option gate produces issues |
