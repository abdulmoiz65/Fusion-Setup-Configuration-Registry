# Sources and dependencies

## Authoritative scope

Reviewed 2026-09-23. The [approved Learning taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-taxonomy/)
shows Learning Configurations, Step 06 / Stage 2 / P1, under Learning Management.
Its two tasks are Configure Learning Defaults and Configure Background
Processing; both show BC REST, TBD ETA 27B. Functional-area dependencies: None.
“Cleared” foundation roadmap status is not live implementation readiness.

Generated identity comes from the effective local catalogs:
ORA_LEARNING_MANAGEMENT / ORA_LEARNING_CONFIGURATIONS;
CUSTOM_CONFIGURE_LEARNING_DEFAULTS and CUSTOM_CONFIGURE_BACKGROUND_PROCESSING.
Both CSV and export/import flags are N. Keep generated task metadata unchanged
unless the catalog/generator route updates it.

[PM FDD OLC-115246](https://confluence.oraclecorp.com/confluence/display/VS/OLC-115246+FDD%3A+Learning+Setup+Skill),
page 21511838840, version 7, updated 2026-09-14, supplies C7 scope and GB-01–16.
Map conversation defaults, calendar event templates, assignment/catalog defaults
and alerts to Configure Learning Defaults; map background processing to its
own task. This is a business-topic mapping, not proof of writable attributes.
The FDD identifies API dependency OLC-100310; detailed C7 execution fields are
not supplied. Do not revive the retired CUSTOM_LEARNING_SETUP grouping or
invent one FSM task per PM topic. External-provider setup is excluded.

## Oracle documentation register

Use current unversioned Oracle pages below, reviewed 2026-09-23. They explain
product behavior, not the missing Fusion REST/loader contract. Recheck current
documentation when changing these rules; do not infer target release from an
API path.

| Key | Oracle documentation | Owning guidance |
| --- | --- | --- |
| D1 | [Offering evaluation defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/set-default-evaluations-for-oracle-learning-course-offerings.html) | Defaults task; questionnaire prerequisite and completion design |
| D2 | [Catalog access and enrollment defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/default-access-and-enrollment-for-oracle-learning-catalog-content.html) | Defaults task; access versus enrollment and new-object scope |
| D3 | [Manager-created assignment defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/defaults-for-manager-created-learning-assignments.html) | Defaults task; prior completion handling |
| D4 | [Completion certificate defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/set-completion-certificate-defaults-for-oracle-learning-courses-and-specializations.html) | Defaults task; available template and print behavior |
| D5 | [Learner and community assignment defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/configure-learner-defaults-for-oracle-learning-and-community-created-assignments.html) | Defaults task; learner choices and metrics |
| D6 | [Virtual attendance defaults](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/set-up-attendance-automation-defaults-for-virtual-instructor-led-training-activities.html) | Defaults task; attendance calculation and sync dependency |
| D7 | [Concurrency and execution defaults](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/concurrency-defaults-and-execution-details-for-oracle-learning-scheduled-processes.html#Execution-Details) | Background task; numeric constraints, recommendations and run-as |

Business names in these sources are not REST fields. The resource tables keep
unresolved authority/lookup contracts as TBD. Do not guess lookup codes or APIs.
If FDD, current Oracle behavior and verified target metadata disagree, record
the specific conflict and ask the owner; do not silently overwrite a valid
customer choice. Task flags cannot be overridden merely by UI documentation.

## Foundation dependency map

These are the eight taxonomy foundation mappings, not eight mandatory setup
changes. Read a provider only when its conditional handoff is selected.
Existing skills below are ownership candidates, not newly authorized executors.

| Taxonomy foundation | Conditional need and repository handoff | Readiness boundary |
| --- | --- | --- |
| Application Profile Option Foundation Skill | Calendar/template or other feature enablement; [Common profile values](../../learning-management-common/manage-administrator-profile-values.md), using core.fusion-api.apps-common.profile-options | Keep profile values separate from template content; verify task-specific prerequisites, not blanket enablement. |
| Background Process Foundation Skill | Dependent processing/schedules; [ESS service](../../../../../core/fusion-api/ess-job-submitter/SKILL.md) | Exact supported job contract and existing schedule required; not a settings writer. |
| Alert Foundation Skill | Learning alert rules and delivery | Learning-specific alert provider/binding TBD; Talent Profile notifications are not a substitute. |
| Approval Rules Skill | Requested approval-rule customization; [HCM Tool Approval Rules](../../../hcm-tool/approval-rules/SKILL.md) | Separate approved workflow; no implied rule change from enrollment defaults. |
| Approval Task Skill | Requested approval-task behavior; [HCM Tool Approval Task](../../../hcm-tool/approval-task/SKILL.md) | Separate workflow and task-specific readiness. |
| Application Search Configuration Foundation Skill | Requested search-dependent access experience; [Common search guidance](../../learning-management-common/manage-search-indexes.md) | Search enablement/index publication is separate from catalog view defaults. |
| Audit and Reporting Foundation Skill | Required configuration audit/reporting; [Common audit policies](../../learning-management-common/manage-audit-policies.md) | Exact object/field applicability and provider readiness; no automatic audit-policy changes. |
| HCM Search Views Skill | Requested persona search-view acceptance | Exact Learning consumer/provider binding TBD; do not equate this with an index. |

Additional documentation-derived prerequisites:
questionnaires for evaluations ([HCM Tool questionnaires](../../../hcm-tool/questionnaire/questionnaires/SKILL.md));
approved certificate templates; virtual provider/report readiness and the
attendance sync process; execution-user identity/privileges; and processing
schedules when immediate processing is disabled. These are conditional, not
universal functional-area dependencies. Template/provider/schedule lookup
contracts remain TBD in the resource registry.

[GHR Common](../../../global-human-resources/global-human-resources-common/SKILL.md) is an authoring
pattern only (manifest, task index, scoped guidance, provider handoffs and
workspace outputs), never a Learning prerequisite or runtime dependency.
Catalog master data, audiences and resources remain with the offering's
separate owners. This skill does not create those records.
