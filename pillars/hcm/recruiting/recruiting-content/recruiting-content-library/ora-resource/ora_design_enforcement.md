# Recruiting Content Library Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Restrict the channel | Keep the initial version within the Recruiting Content Library CSV task flow. |
| 2 | Establish export baseline | Use a full task-native export and locate the requested DescriptionCode with its related version and translation rows. |
| 3 | Evaluate lifecycle-sensitive data | Apply the documented inactive-description and inactive-version handling. |
| 4 | Verify Recruiting Booster | Before importing a Booster-only description type create or update, require Recruiting Booster to be enabled. Do not apply this step to export. |
| 5 | Resolve optional references | When supplied, validate MessageDesignCode and WabaTemplateName through their documented active-value resolvers before completion. |
| 6 | Protect notification content | Do not disable predefined notifications and keep notification content at or below 15 MB. |
| 7 | Restrict category-dependent data | Include Availability Context only for its supported description types and attachments only for file-based description types. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every initial-version request. | Error | | The request uses a non-CSV mechanism, direct migration service, or direct API route. | Use only the supported Recruiting Content Library CSV task flow. | No |
| Reading current content before a targeted update. | Error | | A scoped export is requested, or the requested DescriptionCode and related version and translation rows cannot be located in the full export baseline. | Use a full task-native export for v1 and locate the requested rows. | Yes |
| Preparing an import with a reduced package. | Error | | The reduced package alters archive structure or non-data files, or omits requested DescriptionCode records with related version and translation records. | A reviewed full task-native export may be re-imported. When a reduced package is used, preserve archive structure and all non-data files unchanged and retain the requested DescriptionCode records with related version and translation records. | Yes |
| Importing a record whose target description is inactive. | Error | | The request assumes the target description will be modified. | The migration implementation removes the inactive description from import; use a separately approved process for lifecycle changes. | No |
| Importing a version that exists but is no longer active in the target. | Error | | The request assumes the target version will be updated. | The migration implementation removes that version from import; use a separately approved process for lifecycle changes. | No |
| Importing a version with MessageDesignCode. | Error | resolve_active_recruiting_message_design | DesignTypeCode is not ORA_HTML_TEMPLATE_USER, or MessageDesignCode has no exact active match. | Correct the reference before an approved import; do not claim automatic repair. | Yes |
| Importing a version with WabaTemplateName. | Error | resolve_active_whatsapp_template | WabaTemplateName has no exact active match for HCM_RECRUITING and ORA_PROFILE_EMAIL_TEMPLATE. | Correct the reference before an approved import; do not claim automatic repair. | Yes |
| Creating or updating by CSV import with ORA_IS_LOOP_CANC_NOTIFY, ORA_IS_LOOP_INV_NOTIFY, ORA_IS_LOOP_REMIND_NOTIFY, ORA_IS_LOOP_SCHED_NOTIFY, ORA_IS_LOOP_UPDATE_NOTIFY, or ORA_IS_LOOP_RESCHED_NOTIFY. | Error | resolve_recruiting_booster_enabled | The REST API version is unresolved, or EnabledFlag does not indicate Recruiting Booster is enabled. | Stop the create or update. Export remains allowed and unaffected. | No |
| Editing a predefined notification. | Error | | The intended change disables the notification. | Keep the predefined notification enabled; its content may be changed through the approved flow. | Yes |
| Maintaining notification content. | Error | | Notification content exceeds 15 MB. | Reduce the content size and optimize images or logos before another approved attempt. | Yes |
| Importing Availability Context data. | Error | | DescriptionTypeCode is not ORA_HIRING_TEAM_NOTIFICATION, ORA_JA_EMAIL_TEMPLATE, ORA_POSTING_DESCRIPTION, or ORA_PROSPECT_EMAIL_TEMPLATE. | Reject or omit Availability Context data for every other description type. | Yes |
| Importing an attachment. | Error | | DescriptionTypeCode is not ORA_OFFER_LETTER_TEMPLATE or ORA_PROV_OFFER_LETTER_TEMPLATE. | Reject or omit attachments for every other description type. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_active_recruiting_message_design | MessageDesignCode is supplied. | Exact active MessageDesignCode for DesignTypeCode ORA_HTML_TEMPLATE_USER and the applicable lookup code. | ora_reference_lookups.md |
| resolve_active_whatsapp_template | WabaTemplateName is supplied. | Exact active WabaTemplateName for HCM_RECRUITING and ORA_PROFILE_EMAIL_TEMPLATE. | ora_reference_lookups.md |
| resolve_recruiting_booster_enabled | A Booster-only description type is created or updated by CSV import. | RecruitingBoosterEnabled from the documented feature EnabledFlag. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCL.DESIGN | decision | 50 | design_enforcement | pass->RCL.DONE;blocked->RCL.BLOCKED | RCL.DEFAULT | stop | A CSV request contains scoped, lifecycle-sensitive, optional-reference, or notification content. |
