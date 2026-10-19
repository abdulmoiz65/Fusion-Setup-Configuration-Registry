---
skill_id: "shared.common.manual-tasks"
name: "Manual Tasks"
description: "Guides an implementer through Oracle Fusion Setup and Maintenance tasks that must be completed manually. Use it to give manual guidance from supplied task documentation, repository product guidance, supported task metadata, or a safe Oracle-documentation fallback; it never automates the change."
layer: "shared"
type: "advisory"
execution_mode: "advisory"
owner_team: "FSCR Shared Framework"
version: "0.1.4"
inputs:
  - "manual_task_name"
  - "approved_configuration_change"
  - "target_environment"
  - "provided_task_documentation"
  - "runbook_task_metadata"
outputs:
  - "manual_execution_guidance"
  - "manual_validation_checklist"
  - "manual_task_status"
depends_on:
  - "knowledge/product-guidance/"
  - "knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json"
uses_core: []
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
persists_project_state: false
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges:
  - "Privilege to access the named Setup and Maintenance task"
---

# Manual Tasks

Guide the user to complete the requested setup in Fusion. Do not open Fusion, call an API, create an import, or make configuration changes on the user's behalf.

## Purpose

Provide a reusable, manual-only method for guiding approved Oracle Fusion Setup and Maintenance changes across pillars. Use task-specific documentation supplied with the request first, then relevant information in `knowledge/product-guidance/`, then supported task metadata, and otherwise direct the implementer to current-version Oracle documentation or their administrator.

## Workflow

1. Confirm `manual_task_name`, the target environment, and the approved business change. Do not recommend changing seeded configuration when the desired outcome is unclear.
2. Identify whether the task exactly matches an entry in the **Manual task catalog** and whether the request supplies task-specific instructions or a documentation link.
3. Select the guidance source in this order:
   1. If task-specific instructions or documentation were supplied to the skill, use that material first, whether or not the task is in the manual task catalog. Use catalog metadata only to confirm task identity and purpose.
   2. Otherwise, search `knowledge/product-guidance/` for information applicable to the exact task and approved change. If relevant guidance is available, use it as the manual guidance source, whether or not the task is in the manual task catalog. After reviewing it, use the latest available official Oracle Fusion documentation to fill gaps and verify release-dependent details; explicitly identify any older release used when the topic is unavailable in the latest release. Distinguish repository guidance, Oracle-documented behavior, and implementation recommendations.
   3. If neither supplied task-specific material nor relevant product guidance is available and the task is in the manual task catalog, use its linked task metadata and **Standard manual navigation**.
   4. If none of these sources is available, give the **Default fallback response**.
4. State clearly that the user must perform the task manually in Fusion. Do not open Fusion, call an API, create an import, or make a configuration change on the user's behalf.
5. Do not invent field values or user-interface controls that are absent from the selected guidance source. If the selected guidance conflicts with the approved change, task identity, or current application version, stop and ask the user to clarify or contact an administrator.
6. Ask the user to report completion, changed identifiers, and any validation outcome. When a project workspace is in scope, record token usage in the configured project token-usage log.

## Default fallback response

Use this response when the task is not in the manual task catalog, no task-specific instructions or documentation were supplied, and no relevant information is available in `knowledge/product-guidance/`:

> This is a manual Oracle Fusion task. Perform it manually using the Oracle documentation for your application's current version. For task-specific guidance, required access, or questions, contact your Fusion administrator.

## How to invoke

Use `shared.common.manual-tasks` whenever someone asks how to manually implement, configure, or validate a Fusion Setup and Maintenance task.

### Run Book fallback routing

`core.runbook` may invoke this skill automatically for a catalog-backed Run Book task that has no FSCR task skill or flat Markdown guidance. Treat the supplied task code, name, description, offering, functional area, sequence, pillar, skill-selection evidence, business objects, and match reason as task identity and context. Use the task description to explain the task's purpose; do not treat it as task-specific implementation instructions.

Example request with a catalog task and supplied documentation:

```text
Use shared.common.manual-tasks to guide the manual implementation of Manage Currencies in TEST. The approved change is to update the configured currency display. Follow this documentation first: <documentation link or attached instructions>.
```

Example request with an unlisted task:

```text
Use shared.common.manual-tasks to guide the manual implementation of <exact task name> in TEST. No task-specific documentation is available.
```

## Standard manual navigation

Use these steps for every catalog entry.

1. Sign in to the target Fusion environment with a role that can access Setup and Maintenance and the named task.
2. Open **Navigator** > **Setup and Maintenance**.
3. In the Tasks panel, search for the exact task name and select **Go to Task**.
4. Review the existing configuration and apply only the approved change.
5. Save the change, then validate the intended business behavior with safe test data where applicable.
6. Record the target environment, changed identifier or description, approved change reference, implementer, and validation result in the implementation evidence.

If the task is not visible or cannot be opened, stop and ask the Fusion security or setup administrator to confirm task access, offering enablement, and the required privilege. Do not substitute another task or attempt an alternate execution route.

## Manual task catalog

Each file contains verified task identity and purpose. The standard manual workflow above applies unchanged to every task.

| Task name | Task metadata |
| --- | --- |
| Manage Trading Community Messages | [manage-trading-community-messages.md](manage-trading-community-messages.md) |
| Manage Territories | [manage-territories.md](manage-territories.md) |
| Manage Currencies | [manage-currencies.md](manage-currencies.md) |
| Manage Messages | [manage-messages.md](manage-messages.md) |
| Manage Applications Core Messages | [manage-applications-core-messages.md](manage-applications-core-messages.md) |
| Manage Applications Core Profile Categories | [manage-applications-core-profile-categories.md](manage-applications-core-profile-categories.md) |
| Manage Languages | [manage-languages.md](manage-languages.md) |
| Manage Time Zones | [manage-time-zones.md](manage-time-zones.md) |
| Assign Help Text Administration Duty | [assign-help-text-administration-duty.md](assign-help-text-administration-duty.md) |
| Manage Help Security Groups | [manage-help-security-groups.md](manage-help-security-groups.md) |
| Manage Industries | [manage-industries.md](manage-industries.md) |
| Manage ISO Languages | [manage-iso-languages.md](manage-iso-languages.md) |
| Manage Natural Languages | [manage-natural-languages.md](manage-natural-languages.md) |
| Set Help Options | [set-help-options.md](set-help-options.md) |
| Manage Taxonomy Hierarchy | [manage-taxonomy-hierarchy.md](manage-taxonomy-hierarchy.md) |
| Manage Help Content | [manage-help-content.md](manage-help-content.md) |
| Manage Attachment File Formats | [attachment-file-formats.md](attachment-file-formats.md) |

## Sources

- `knowledge/product-guidance/` — relevant product and setup guidance when task-specific documentation was not supplied.
- `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json` — task identity, code, purpose, and supported import/export flags.
- Oracle Fusion Help, **Setup and Maintenance** — verify the current-release navigation and task UI before changing configuration.
