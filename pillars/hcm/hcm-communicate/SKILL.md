---
skill_id: "hcm.hcm-communicate"
name: "HCM Communicate"
description: "Coordinates HCM implementation guidance for the HCM Communicate offering."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM HCM Communicate pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_communicate_requirements"
outputs:
  - "offering_scope"
  - "functional_area_skill_plan"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "scope"
  - "skill_path"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# HCM Communicate

## Purpose

Coordinates implementation work for offering `HCM Communicate` (`ORA_IRC_HCM_COMMUNICATE`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_IRC_HCM_COMMUNICATE`
Functional area count: `1`
Setup task count: `11`

- `ORA_IRC_EMPLOYEE_CAMPAIGNS`: Employee Communications

## Public Documentation

These links are Oracle's current public HCM Communicate documentation for the
offering, its Employee Communications setup tasks, and closely related runtime
operations. Use them as documentation references; the effective FDOS catalog
and the generated child skills remain authoritative for task identity, skill
routing, export/import support, and execution boundaries.

### Offering, enablement, and security

- [What's HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/what-s-hcm-communicate.html)
- [Enable HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/enable-hcm-communicate.html)
- [HCM Communicate Roles](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/hcm-communicate-roles.html)
- [Oracle Communicate Setup and Maintenance Tasks](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/hcm-communicate-setup-and-maintenance-tasks.html)

### Employee Communications setup tasks

- [Create an Email Template](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-an-email-template.html) — Manage Email Templates
- [Create a Predefined Link](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-predefined-link.html) — Manage Predefined Links
- [Create an Email Sender Profile](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-an-email-sender-profile.html) — Manage Email Profiles
- [Create a Predefined Audience Using Eligibility Profiles](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-predefined-audience.html) — Manage Predefined Audience Criteria
- [Create a Predefined Audience Using Filtered Lists](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-predefined-audience-using-filtered-lists.html) — audience alternative using HCM Lists
- [Create a Communication Team](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-communication-team.html) — Manage Communication Teams
- [Add Alternative Contact Details](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-alternative-contact-details.html) — team contact-order preferences
- [Upload an Image to the Media Library](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/upload-an-image-to-the-media-library.html) — Manage Communicate Media
- [Configure SMS for Campaigns](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/configure-sms-for-campaigns.html) — Manage SMS Configuration

### Scheduled processes and related capabilities

- [Scheduled Processes for HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/scheduled-processes-for-hcm-communicate.html)
- [Schedule Communicate Campaigns Using Scheduled Process (26B)](https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/meex-26b/26B-employee-experience-wn-f43748.htm)
- [Set Up the Grow Banner Using HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/set-up-the-grow-banner-using-hcm-communicate.html)
- [Create a Grow Notification](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/create-a-grow-notification.html)
- [Employee Communications REST Endpoints](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-employee-communications.html)

## Scheduled Process Guidance

Oracle recommends the following HCM Communicate scheduled-process cadence. In
test environments, run the processes manually when validating that campaign
emails are sent and posts are published. Starting in 26B, use Schedule
Communicate Campaigns as the default campaign-email process.

| Scheduled process | When to run | Recommended cadence | What it achieves | Process owner |
|---|---|---|---|---|
| Import User and Role Application Security Data | After Campaign Administrator and Campaign Manager roles are created and assigned | Every 24 hours | Imports the latest user and role security assignments so Communicate access is current | Campaign Administrator |
| Refresh HCM Communicate Audience | When a campaign uses a predefined audience and its audience breakdown is needed | Every 24 hours | Refreshes the audience data used to display the campaign audience breakdown | Campaign Manager |
| Schedule Communicate Campaigns (26B and later) | After campaign activation and while campaign email processing is required | Every 5–10 minutes | Creates the underlying Prepares and Sends Communicate Campaign Message process instances that prepare and send campaign emails | Schedule through Scheduled Processes; access is governed by the campaign-administrator security policy |
| Track Campaign Email Delivery | After an email is sent | Every 30 minutes | Tracks campaign email delivery after dispatch | Campaign Manager |
| Publish Communicate Posts | When a post is submitted for publishing | Every 24 hours | Publishes submitted Communicate posts | Campaign Administrator |
| Process HCM Communicate Grow Notifications | When a Grow notification is created | Every 24 hours | Processes and sends Grow notification emails | Campaign Administrator |

Source: [Scheduled Processes for HCM Communicate](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/scheduled-processes-for-hcm-communicate.html).

### 26B campaign-email transition

Enable the `ORA_HCO_NODELAY_TRIGGER_ESS` profile option before scheduling
Schedule Communicate Campaigns. Configure the new process with a frequency of
5–10 minutes. Oracle states that Prepare Campaign Email and Send Campaign Email
are existing processes that will be removed in a future release; keep them only
as legacy guidance for pre-26B configurations, not as the default for 26B and
later.

The new process creates multiple instances of the underlying Prepares and Sends
Communicate Campaign Message scheduled process. To let a campaign administrator
view and manage those instances, configure the documented data-security policy
for the campaign administrator and select the following definitions in its SQL
predicate:

```sql
EXISTS
(select 1 from dual)
and DEFINITION in (
  'JobDefinition://oracle/apps/ess/hcm/recruiting/messaging/ProcessCommunicateCampaign',
  'JobDefinition://oracle/apps/ess/hcm/recruiting/messaging/CommunicateSchedulerESS',
  'JobDefinition://oracle/apps/ess/hcm/recruiting/messaging/EvaluateEligibilityJob',
  'JobDefinition://oracle/apps/ess/hcm/recruiting/messaging/ProcessDigest',
  'JobDefinition://oracle/apps/ess/hcm/recruiting/messaging/ProcessGrowNotifications'
)
```

The 26B readiness note is the source for this transition guidance: [Schedule
Communicate Campaigns Using Scheduled Process](https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/meex-26b/26B-employee-experience-wn-f43748.htm).
