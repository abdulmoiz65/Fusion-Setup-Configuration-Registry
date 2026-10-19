# Recruiting Messaging Configuration Defaulting Rules

Only the two defaults below are executable. A valid supplied value always takes precedence.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| MESSAGE_LIMIT_ADMIN_ALERT_EMAIL_ID | admin_alerts@invalidemail.com | No administrator alert email value is supplied | No; preserve any supplied value that passes validation |  |
| ORA_IRC_ALL_EMAIL_MARKETING_CATEGORIES | ORA_PROSPECT_EMAIL_TEMPLATE,ORA_POOL_EMAIL_TEMPLATE,ORA_PROFILE_EMAIL_TEMPLATE,ORA_EVENT_POOL_NOTIFICATION,ORA_SEND_EVENTINVITE_EXT,ORA_IRC_CAND_POOL,ORA_SEND_INVITE,ORA_IRC_OUTREACH_MESSAGE,BULK_ADHOC_MESSAGE_FROM_LIST_VIEWS | No all-marketing-category value is supplied | No; preserve a supplied value only when it exactly matches the complete ordered list |  |

## Product Values That Are Not Import Defaults

| Field | Documented Product or UI Value | Required Omission Behavior |
|---|---|---|
| ORA_IRC_EMAIL_MAX_SIZE | 20 MB | Do not synthesize 20; omit the setting and preserve destination behavior when no change is requested |
| ORA_IRC_INBOX_CONVERSATION_DURATION | 180 days; maximum 365 days | Do not synthesize 180; omit the setting and preserve destination behavior when no change is requested |
| ORA_IRC_INBOUND_EMAIL_NOTIFY_RECRUITER_OR_POOL_OWNER | Selected in the email-reply UI | Do not synthesize a native selected value; the exact native token remains artifact-gated |
| ORA_IRC_INBOUND_EMAIL_NOTIFY_HM | Selected in the email-reply UI | Do not synthesize a native selected value; the exact native token remains artifact-gated |
| ORA_IRC_OUTBOUND_VANITY_EMAIL_CATEGORIES | No selections is the functional default | Do not synthesize a native value; native codes and omission behavior remain artifact-gated |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| IRCMSG.DEFAULT.ADMIN_ALERT_EMAIL | decision | 15 | apply_default | supplied->IRCMSG.DEFAULT.ALL_EMAIL_MARKETING_CATEGORIES;defaulted->IRCMSG.DEFAULT.ALL_EMAIL_MARKETING_CATEGORIES;failed->IRCMSG.ERROR.INPUT | IRCMSG.LOOKUP.COUNTRY | stop | Every proposal; apply the administrator alert email default only when its value is omitted | all |
| IRCMSG.DEFAULT.ALL_EMAIL_MARKETING_CATEGORIES | decision | 16 | apply_default | supplied->IRCMSG.ENFORCE.DESIGN;defaulted->IRCMSG.ENFORCE.DESIGN;failed->IRCMSG.ERROR.INPUT | IRCMSG.DEFAULT.ADMIN_ALERT_EMAIL | stop | Every proposal; apply the complete ordered marketing-category list only when its value is omitted | all |
