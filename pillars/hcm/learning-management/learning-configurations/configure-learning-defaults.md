---
task_code: "CUSTOM_CONFIGURE_LEARNING_DEFAULTS"
task_name: "Configure Learning Defaults"
parent_skill_id: "hcm.learning-management.learning-configurations"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Configurations"
functional_area_code: "ORA_LEARNING_CONFIGURATIONS"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Configure Learning Defaults

## Purpose and route

Set reusable non-provider Learning behavior; creating a course, offering,
community, audience or resource is a separate owning task. This single catalog
task covers the first four PM C7 business topics, not four invented FSM tasks.
Use the [common workflow](references/workflow.md) for intake, full inventory,
proposal and approval. Release/build is not a mandatory business input.

## Contract Not Resolved

Catalog identity and support flags are preserved in frontmatter. CSV export/import
is not supported. The generated REST mode with an empty businessObject does not
authorize Data Loader sampling or submission. BC REST is TBD ETA 27B in the
approved taxonomy; read/write fields, privileges and operation mapping remain
TBD. Do not invent a payload, switch to direct REST or automate the UI.
An authorized implementer may use the documented product pages; agent execution
must wait for the declared provider contract. Resolve technical gaps with the
implementation owner, not by asking the customer to guess an API.

## Business intake and complete inventory

List every topic below on a broad review, including not-applicable or unverified
topics. Ask only unanswered questions; existing choices need not be repeated.
Codes below are documentation source keys, not endpoint or lookup codes.

| Topic | Business question | Evidence and scope |
| --- | --- | --- |
| Evaluations (D1) | Which offering types need an evaluation, which questionnaire, and must completion require it? | Questionnaire dependency; per-type saved choice and learner completion scenario. |
| Access and enrollment (D2) | Who should discover content, who may enroll, through which flow, and how should prior completion be treated? | Separate view mode from enrollment; courses, offerings, specializations and access-group defaults. Do not create groups here. |
| Manager-created assignments (D3) | Should prior completion exempt a team member or require a retake? | Manager assignment scenario distinct from learner-created assignments. |
| Completion certificates (D4) | Should courses/specializations offer certificates, and which approved template? | Template preview and learner/manager print behavior. |
| Learner/community assignments (D5) | What assignment type, due-date rule, note, community reassignment behavior, hierarchy selection and summary metrics are needed? | Assignment defaults and metric definitions; preserve intentional exceptions. |
| Virtual attendance (D6) | Is virtual instructor-led learning in scope; what threshold and administrator override policy are wanted? | Provider and sync dependencies; attendance boundary cases. No provider credentials collected here. |
| Conversation defaults (FDD C7) | Which conversation behavior, audience and default should change? | Actual field/value mapping TBD; not AI-agent deployment. |
| Calendar event templates (FDD C7) | Which learner/instructor templates, languages and event content need customization? | Approved template revision and sample event/ICS. Calendar profile enablement is separate Common work. |
| Alerts (FDD C7) | Which alert, recipients, trigger, timing and channel should apply? | Before/after rule plus delivery and non-delivery tests; avoid duplicate notifications with calendar integration. |

The FDD supplies topic scope, not detailed conversation/template/alert wire
contracts. Preserve those rows as unverified or input-required until supported
fields are known. Missing optional decisions are Deferred, not invented defaults.

## Product guidance

Sources D1–D6 are linked in [source register](references/sources-and-dependencies.md).

- **D1:** My Client Groups > Learning and Development > Configure Evaluations.
  Prepare questionnaires first; select Learner Evaluation questionnaires,
  preview them, and set defaults independently for blended, instructor-led and
  self-paced offerings. See the design rules for mandatory-completion impact.
- **D2–D4, D6:** Configure Catalog Defaults. These choices govern defaults, not
  retroactive mass updates. Certificate choices include No Certificate or
  Certificate with an available template; preview the selected template.
- **D5:** Configure Learner Defaults. Assignment type, due-date and note defaults,
  community reassignment, workforce-hierarchy learner selection, and metrics
  are distinct decisions. Completed excludes Bypass Completed; request the
  separate Bypass Complete metric when that population is wanted.
- **D6:** Documented virtual providers include Adobe Connect, Microsoft Teams,
  WebEx and Zoom. Attendance requires report processing by Sync Instructor-Led
  Training for Learning. This is a conditional provider/job handoff, not
  permission to configure a provider or submit an ESS job.

## Acceptance evidence

After a supported provider is implemented and approved, re-read each attempted
setting and test the selected personas using separately authorized test data.
Check discoverability independently of enrollment, prior-completion handling
for manager and community paths, evaluation completion gating, certificate
printing, threshold attendance and template/alert outputs. Saved defaults alone
do not prove notification delivery or downstream behavior. Never create live
test courses or assignments implicitly. Keep unresolved tests Pending and return
their owner and next action.
