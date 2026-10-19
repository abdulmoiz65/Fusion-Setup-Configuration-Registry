---
task_code: "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
task_name: "Manage Administrator Profile Values"
parent_skill_id: "hcm.learning-management.learning-management-common"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Management Common"
functional_area_code: "ORA_LEARNING_MANAGEMENT_COMMON"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Administrator Profile Values

## Setup Task Metadata

- Task name: `Manage Administrator Profile Values`
- Task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Validate enabled/updatable level, exact allowed values and consumer impact; recommendations are not defaults; keep the seven Redwood flags separate from Grow and the release-dependent Communities row.

Readiness here is rule-contract readiness only; environment, privileges, current
state, exact values and approval still require the selected provider's gates.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Learning Management`
- Functional area / Setup Object: `Learning Management Common`
- Setup task name: `Manage Administrator Profile Values`
- Setup task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Administrator Profile Values` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Profile Options: Decide the Learning Experience

Customer navigation: **Setup and Maintenance > Tasks > Search > Manage
Administrator Profile Values**. Configure existing values; do not recreate
Oracle-delivered profile definitions. Before proposing a write, confirm the
definition, editability, allowed values, enabled levels, and any applicable
overrides through the profile provider. Do not assume all options are Boolean
or that every change belongs at Site level.

### Entry paths and baseline-aware questions

Apply the FDD's three entry paths without changing the execution contract:

| Input available | Next step |
| --- | --- |
| No usable business decisions | Read the selected, authorized baseline where supported, then group only applicable unanswered business questions. Show recommendations with their business reasons; do not select answers for the implementer. |
| Partial decisions or draft values | Acknowledge accepted choices and valid exceptions. Validate supplied values, retain their source, and ask only for the gaps. |
| Complete intended-value input | Validate the entire selected scope and compare with current settings. Return the delta and exceptions without repeating answered questions. Complete input is not execution approval. |

Before asking BQ-03 or BQ-09 solely to fill a prerequisite, check the actual
configured value. A valid populated Site language or governed BI folder needs
no replacement question. Check a supplied change or conflicting value even if
the prerequisite is populated; "only if blank" does not hide invalid input.
A failed read is `Not validated`, not blank. Keep planning useful, but do not
call its recommendations a tenant-validated delta.

Suppress Teams-specific enablement questions when the provider decision is
already known to be non-Teams or none; do not infer an N write. Ask join timing
only when virtual sessions are relevant or the implementer explicitly requests
it. Ask about template customization independently of Outlook. Retain the
scheduled-process language prerequisite described below when applicable.

### Review categories

Use the [Learning Setup Skill FDD](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21511838840)
categories to keep the conversation focused:

Apply the attachment-specific rules in [PM review guidance](#profile-attachment-interpretation).
In particular, never use its prefilled "Current tenant setting" column as a
live baseline, submit a placeholder, or copy its summary counts into a proposal.

| Category | Customer guidance |
| --- | --- |
| Required when applicable | Explain the prerequisite and propose a value only when the relevant condition is true and the verified setting is missing. A populated value still needs validity checks; a failed read is not a missing value. |
| Review recommended | Show the relevant recommendation, verified current setting, and business impact. Customer choices remain explicit. |
| Review on demand / already optimal | Summarize settings that need no action. Inspect individual settings when the customer requests them or a symptom makes them relevant. |
| Ignored by this guided scope | Exclude from the proposed execution delta; explain the exclusion. This classification does not mean Oracle has removed the option. |

### Questions and proposed decisions

The following starting points come from the FDD; they are recommendations,
not unconditional Oracle defaults. Validate the actual value representation
before mapping a business answer to a provider request.

| Customer decision | Exact profile option code | Guideline |
| --- | --- | --- |
| BQ-01: Who needs calendar views: learners, administrators, both, or neither? | `ORA_WLF_ENABLE_SELF_SERVICE_LEARNING_CALENDAR`; `ORA_WLF_ENABLE_ADMIN_LEARNING_CATALOG_CALENDAR` | Propose Y for each selected audience, N for an explicit exclusion; defer an unresolved choice. |
| BQ-02: Will you use Teams, Zoom, Adobe Connect, or no virtual provider? | `ORA_WLF_ENABLE_ADVANCED_MEETING_OPTIONS` | Recommend Y for the FDD's Teams enhancements. Do not enable solely because another virtual provider is used; retain unrelated current settings. Provider integration is separate. |
| BQ-03: Will Outlook calendar synchronization be used, and what should the default language be? | `FND_LANGUAGE` | If applicable and blank, require a supported Site-level language chosen by the customer. Preserve a valid populated setting. This is application-wide, so assess other consumers before changing it. |
| BQ-04: Should learners receive observer-checklist completion notices? | `ORA_WLF_OBS_CHCKLST_LRNR_COMPL_NOTIFY` | Recommend Y; respect an explicit No. Defer when undecided. |
| BQ-05: Should learner and instructor invitations be customized? | `ORA_WLF_CUSTOMIZE_CALENDAR_TEMPLATES` | Recommend Y when customization is wanted; propose N only for an explicit decision. Configure the templates separately. Do not derive this decision solely from whether Outlook is used. |
| BQ-06: Which attendance confirmation experience is required? | `ORA_WLF_MARK_ATTENDANCE_REDWOOD_PAGES_ENABLED` | Inspect the supported choices first; explain them and validate the selected value. The FDD suggests Both, but its Boolean and Administrator examples are inconsistent. Do not send Y or infer an administrator/learner role mapping. |
| BQ-07: How early should the Join action become available for virtual sessions? | `ORA_WLF_LEARN_ILT_ALLOW_JOIN_CONFERENCE_MINUTES_PRIOR` | Offer 15 minutes as an FDD starting point. Require a non-negative number and validate the supported representation and range with current metadata. If unset, Join always appears; blank is not equivalent to zero. |
| BQ-08: Will Grow recommendations be used with Learning? | `ORA_WLF_ENABLE_GROW_RECOMMENDATIONS` | Propose Y or N from that decision; keep it separate from Redwood enablement. |
| BQ-09: Will analysis reports select learners for assignments? | `WLF_RBA_BI_FOLDER` | If needed and blank, agree a governed custom BI folder. Validate the existing path rather than replacing it with an example. |

The BQ IDs retain FDD traceability, not a mandatory interview order. A skipped,
blank or "don't know" optional answer is Deferred, not No, zero or approval of
the recommendation. An explicit value of zero remains an actual value. If the
business condition makes a prerequisite required, ask for the missing value
and explain the affected feature; do not silently defer the dependency away.

For `FND_LANGUAGE`, the current
[scheduled-process guidance](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/scheduled-background-processes-for-oracle-learning.html)
also requires a Site-level value before Sync Instructor-Led Training for
Learning runs. Check that dependency when the process is in scope even if
Outlook is not used; otherwise omit the irrelevant language question.

The current [Microsoft integration guidance](https://docs.oracle.com/en/cloud/saas/talent-management/favcl/integrate-microsoft-outlook-calendar-and-teams-with-oracle-learning.html)
supports calendar-template customization for both Outlook events and ICS
files. This takes precedence over FDD sample dialogues that equate no Outlook
with no template customization. For attendance, the
[attendance feature reference](https://docs.oracle.com/en/cloud/saas/readiness/hcm/24d/lear-24d/24D-learning-wn-f34744.htm)
describes enrollment-details and attendance-form choices; use the current
tenant definition to verify their availability and exact stored values.

### Redwood recommendation

Discuss the FDD's seven-option bundle as one experience decision and recommend
Y where supported and editable:

| Experience | Exact profile option code |
| --- | --- |
| Single catalog listing | `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` |
| Assignment management | `ORA_WLF_ASSIGNMENTS_REDWOOD_ENABLED` |
| Courses | `ORA_WLF_ENABLE_REDWOOD_COURSES` |
| Learning paths | `ORA_WLF_ENABLE_REDWOOD_LEARNING_PATHS` |
| Self-paced learning management | `ORA_WLF_ENABLE_DL_API` |
| Learning resources | `ORA_WLF_LEARN_ADMIN_RESOURCES_VBCS_ENABLED` |
| Categories and topics | `ORA_WLF_CATG_TOP_REDWOOD_ENABLED` |

If all seven are already enabled, give one summary. Otherwise present only
affected rows and any valid explicit exceptions. Explain the experience
affected by an exception without silently replacing it. Some delivered flags
can become noneditable; this is not a reason to recreate or force them.

The FDD additionally lists `ORA_WLF_COMMUNITIES_REDWOOD_ENABLED`, although its
bundle narrative says seven and the supplied current profile reference does
not list that code. Treat it as a separate, release-dependent review item.
Require current documentation and provider confirmation before including it
in a change; do not silently add an eighth bundle member.

### On-demand settings and operational cautions

Use the current [profile reference](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/profile-options-for-oracle-learning.html)
and FDD when search, retakes, incident reporting, sync scheduling, analysis
timeouts, or content troubleshooting are explicitly in scope. Preserve
unrelated settings rather than presenting every Learning flag for review.
The [on-demand code map](#on-demand-profile-options)
distinguishes business-policy choices from Support-directed tuning.

- For `WLF_RBA_BI_FOLDER`, validate BI Consumer Role Open permission and the
  analysis Worker/Person ID requirements. Changing a populated folder path
  can break existing reports; require an impact review.
- Keep `ORA_WLF_ROLLUP_ON_COMPLETION` enabled; investigate content status
  reporting when completion fails.
- Player, HACP/CORS, JWPlayer, and SCORM commit tuning require Oracle Support
  direction. Do not use them as routine implementation optimization.
- The external AICC/HACP player option excludes LinkedIn Learning imports
  through external-provider support.
- `ORA_WLF_UPLOAD_PLAYER_LOGS` is learner-scoped troubleshooting. Confirm the
  diagnostic scope and when to restore the prior setting; avoid broad logging.
  Y logs all launched SCORM/HACP content, N (default) disables logging, and a
  content number targets one item. Retrieve diagnostics through the BI report.
- The FDD excludes `ORA_WLF_AUTO_LAUNCH_PDF_ACTIVITY` and
  `ORA_WLF_AUTO_LAUNCH_WEBLINK_ACTIVITY` from this guided setup. Current Oracle
  documentation still describes them for offering activities, not self-paced
  learning content; label them excluded from scope, not obsolete. A specific
  request needs a separate validated review.

## Profile attachment interpretation

`oracle_learning_profile_options_triage.xlsx` (attachment 21940378693),
`Profile options` sheet, contains these groups:

| Source rows | Review treatment |
| --- | --- |
| 6–16, 21–24 | Review recommended; use this task's business questions and seven-option Redwood bundle. |
| 18–20, 27–36, 38 | On-demand review; use the code map below. |
| 37, 39 | Conditional prerequisites: `WLF_RBA_BI_FOLDER` and `FND_LANGUAGE`. |
| 25–26 | Excluded from guided changes: PDF and web-link auto-launch. |
| 17 | `REDWOOD COMMUNITY PLACEHOLDER` is not a profile code. Never resolve or submit it as one. |

The workbook's prefilled `Current tenant setting` cells are examples, not
evidence from the selected environment. The `Triage` sheet's "already optimal"
label expressly does not verify tenant state. Do not reinterpret the `Oracle
Recommended Value` column as a customer decision. Most display-name cells are
empty; obtain actual names from the provider, keeping the exact code visible.

For this attachment, column B identifies the option, H is the sample current
setting, I is the recommendation, and J is the implementer's final decision.
Only treat J as intended input when it actually contains an explicit decision
or value; a status such as "reviewed" does not specify a value. A blank J does
not inherit H or I as user input. Apply the guided question and review-category
rules above: one Redwood bundle recommendation, only applicable unanswered
questions, and no proactive on-demand or ignored-row interview.

For another workbook, identify its actual intended-value column (for example,
`Profile Value` in FDD scenario 1.3); do not impose this attachment's column
positions on it. Keep raw input and mapping separate. A blank cell means no
supplied value, not an instruction to clear the configured value. A clear or
reset request needs an explicit decision and a supported provider operation.
Unknown codes need correction; valid but out-of-guided-scope codes need a scope
decision, not an invented obsolete classification or silent execution.

Trim surrounding whitespace from identifier cells only after recording the
raw source and normalization (for example, `FND_LANGUAGE ` in row 39). Do not
silently normalize a proposed value or path: row 37's illustrative BI path
contains a trailing period/space and must not be copied into a request. Ask
for the actual governed folder when required. Unknown codes and conflicts
need correction, not a fuzzy match or a new profile definition.

### On-demand profile options

Read current product guidance and provider metadata only for the selected
topic. Keep unaffected values. An on-demand bucket does not mean every
option requires Oracle Support, and a documented default is not a readback.

| Review trigger | Exact code(s) | Decision rule |
| --- | --- | --- |
| Search results too broad or narrow | `ORA_WLF_SS_CATALOG_SEARCH_MODE` | Aggressive matches any term; Neutral requires all terms, in any order; Relaxed matches terms as entered or exactly. Verify stored choices; the workbook's sample N is not a Boolean contract. |
| Retraining or repeat access policy | `ORA_WLF_ALLOW_RETAKE_REDWOOD_PAGES_ENABLED` | Applies to completed self-paced offerings; confirm the repeat-training policy before proposing a change. |
| Incident reporting policy | `ORA_WLF_DISABLE_INCIDENT_REPORTING` | Explain the inverse meaning of the flag and confirm the support process. |
| Support-directed content-player change | `ORA_WLF_ELEARNING_AICC_ENABLE_EXTERNAL_PLAYER`, `ORA_WLF_ELEARNING_PLAYER_VERSION`, `ORA_WLF_HACP_ENABLE_429`, `ORA_WLF_HACP_SET_CORS_HEADER`, `ORA_WLF_JWPLAYER_VERSION` | Require a specific Support direction and target-valid values; never use the workbook's sample Y for a version field. |
| Targeted playback diagnosis | `ORA_WLF_UPLOAD_PLAYER_LOGS` | Confirm user/content scope, duration and restoration. Do not enable broad logging as a setup default. |
| Support-directed SCORM tuning | `WLF_SCORM_AUTO_COMMIT`, `WLF_SCORM_COMMIT_INTERVAL_CNT`, `WLF_SCORM_COMMIT_INTERVAL_SEC` | Review documented Y/50/60 defaults, current settings and the Support instruction; no blanket reset. |
| Analysis timeouts | `ORA_WLF_ANALYSIS_FETCH_TIMEOUT_MINS` | Investigate the symptom and workload before changing the documented 16-minute starting point. |
| Instructor-led synchronization schedule | `ORA_WLF_DISABLE_AUTO_SYNC_ILT` | Explain that disabling automatic submission requires an agreed scheduled-process plan. Do not change or submit a job just because the FDD lists N. |

This task's `ORA_WLF_ROLLUP_ON_COMPLETION` caution comes from product
documentation, not an extra workbook review row. Communities is a separate
release-dependent FDD row; do not substitute it silently for the placeholder.

## Source conflicts that affect decisions

| Evidence | Maintained handling |
| --- | --- |
| FDD attendance recommendation varies between Y, Both and Administrator; workbook row 22 also uses Y. | No literal mapping until the current definition confirms supported values and behavior. An undecided answer is Deferred. |
| FDD has seven Redwood bundle members plus a separate communities entry; workbook has a placeholder. | Keep the seven-option bundle stable; communities requires separate release/definition evidence. |
| FDD example treats no Outlook as no calendar customization; workbook row 23 focuses on Outlook. | Ask about template customization independently; current product guidance includes ICS. |
| FDD BQ-05 says keep Y, but the general rule retains current values for "not sure". | Retain current and mark Deferred for uncertainty; a recommendation is not consent. |
| FDD BQ-02 maps other providers to N but says hide the Teams-specific option when not relevant. | Do not clear a configured value solely because another provider is mentioned. Explain any explicit requested disable and validate its impact. |
| FDD scenario 1.1 says three changes but its table also changes join timing from 0 to 15. | Compute deltas and counts from validated current/proposed values, never sample narrative counts. |
| Scenario 1.2 says attendance is undecided but its table places Both in Proposed and Administrator in Action. | Retain the verified current value and action Deferred; do not copy the malformed row. |
| Scenario 1.3 says Outlook requires customized templates and accepts a workbook language as satisfying the dependency. | Confirm customization separately and validate the actual configured Site value. File input alone cannot establish a satisfied tenant dependency. |
| Guided-input prose says retain a recommendation when supplied input fails validation. | Keep the recommendation visible as advice; preserve the invalid supplied value and correction needed. Never silently promote the recommendation into an executable replacement. |
| Profile Triage summary says all already-optimal changes require Support, while detailed rows include business-policy choices. | Use the per-option on-demand rules; Support restrictions apply only to the documented tuning options. |
| Workbook source values, blank names and overall category totals are incomplete as a live proposal. | Resolve names, levels, applicability and current state; report excluded/invalid rows independently. |

Validate current provider metadata and applicable feature prerequisites before
converting a recommendation into an executable value. Release/build remains
optional context under the Common workflow, not a required user-supplied input.
Unresolved product conflicts affect only their dependent rows.

## Completion evidence

Confirm configured code, level, target and value against the approved proposal,
and validate the intended Learning experience. Preserve current valid exceptions;
a changed value alone does not prove that integrations or dependent templates work.
