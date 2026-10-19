# Learning setup capability assessment and handoffs

Preserves the PM FDD version 7 C1–C8 setup scope formerly held by the offering
parent. This is discovery and handoff guidance, not an expansion of Common's
ten FSM tasks or execution authority.

For general setup, return a compact capability summary plus the
[item-by-item setup inventory](setup-inventory.md), including existing,
missing and unverified configuration. A capability summary alone is not the
requested configured/missing list. For specific requests, select only applicable capabilities;
do not make the customer complete all eight before independent work.

## Offering-wide intake and response

For “enable/configure Oracle Learning” or a brand-new-pod request, start with
the offering scope below, not a self-paced-versus-instructor-led choice or the
Common task list alone. This is an assessment menu, not a mandatory execution
sequence. Ask for the pod name/URL and whether the initial rollout covers the
complete offering or selected areas only when those decisions are unknown.
If scope is undecided, offer a complete assessment and prioritize with the user.
Release/build is optional; detailed delivery, calendar, provider and audience
questions follow within the relevant selected area.

Use the current effective offering catalog and each owning skill's task index
and readiness guidance, not prior conversational summaries, to keep this menu
current. Reuse accepted project decisions unless the user requests a fresh
start; never reuse historical tenant observations as a fresh baseline.

| Functional Area Code | Functional Area | Assessment Scope |
| --- | --- | --- |
| ORA_LEARNING_MANAGEMENT_COMMON | Learning Management Common | Profile definitions and values, lookups, value sets, DFFs, global search, suggestion groups, indexes and applicable audit settings; retain the Audit Types catalog-identity gap. |
| ORA_LEARNING_MANAGEMENT_HCM_SECURITY_PROFILE | Learning Management HCM Security Profile | Person security profiles, intended data visibility, and assignment of security profiles to roles. |
| ORA_LEARNING_MANAGEMENT_HCM_TOOL | Learning Management HCM Tool | Question Library, Questionnaire Templates, Questionnaires and Manage Approval Transactions for Human Capital Management; retain applicable Search Views handoffs separately. |
| ORA_LEARNING_MANAGEMENT_LOCATIONS | Learning Management Locations | Required locations. |
| ORA_LEARNING_CONFIGURATIONS | Learning Configurations | Learning defaults and background processing, including evaluations, enrollment, assignments, certificates, attendance, conversations, calendar templates and alerts. |
| ORA_LEARNING_RESOURCES | Learning Resources | Instructors, classrooms and training suppliers. |
| ORA_LEARNING_AUDIENCE | Learning Audience | Learning audience criteria and user groups. |
| ORA_LEARNING_CATALOG | Learning Catalog | [Manage Self-Paced Learning](../../learning-catalog/self-paced-learning/SKILL.md), [Manage Events](../../learning-catalog/events/SKILL.md), [Manage Courses](../../learning-catalog/courses/SKILL.md), [Manage Learning Paths](../../learning-catalog/learning-paths/SKILL.md), [Manage Official Communities](../../learning-catalog/official-communities/SKILL.md), [Manage Categories](../../learning-catalog/categories/SKILL.md), [Manage Topics](../../learning-catalog/topics/SKILL.md) and [Manage Catalog Administration Profiles](../../learning-catalog/manage-catalog-administration-profiles/SKILL.md). |
| ORA_LEARNING_ASSIGNMENT | Learning Assignment | Learning Assignment Profiles and Learning Records. |
| ORA_RECOMMENDATIONS | Recommendations | Recommendation profiles. |
| ORA_EXTERNAL_PROVIDERS | External Providers | Required external-provider configuration. |

Self-Paced Learning is a Catalog task, not an alternative to Catalog setup.
Delivery preferences refine the selected tasks and resources; they do not
exclude courses, paths, profiles, audiences or other functional areas by
themselves. Keep the exact current task names rather than substituting older
offering/specialization terminology for Events or Learning Paths.

### Execution coverage disclosure

The linked Catalog tasks have child routes, but each requested operation
still needs its own readiness and approval checks. The current
[Catalog skill](../../learning-catalog/SKILL.md#deferred-scope) defers Manage Access Groups,
which remains visible as deferred scope rather than a supported creation route.
Official Communities, Categories and Topics route to their linked children;
unverified registration, privileges or operation support block only the
affected operation. Catalog Administration
Profiles belongs to Catalog even when Common captures C6 security decisions.

[Learning Configurations](../../learning-configurations/SKILL.md#execution-readiness-and-read-order)
supports planning but currently has deferred live task bindings. Other areas
also require their owning supported workflow; catalog membership alone does
not prove automation. Report the affected operation, owner and next action
without bypassing a missing route or stopping independent planning.

Learning Assignment, Recommendations and External Providers have catalog scope
but no dedicated consuming skills in this package. Include their confirmed
Application Profile Option Foundation dependency in the assessment using the
[profile-option consumer handoff](dependencies.md#profile-option-consumer-handoffs).
Keep the consumer's missing workflow and unresolved option requirements visible
in the inventory; foundation readiness alone does not enable that workflow.

### From scope to the first inventory

Explain that a new pod is not an empty baseline. After the routed read
prerequisites pass, assess selected items using fresh permitted evidence and
deliver the [item-by-item inventory](setup-inventory.md) before proposing changes.
Include exact codes/identifiers, names/purposes, applicability, current values,
required values or decisions, gaps, next actions and approval state. Unread
items remain Not validated, not missing; retain unchanged and deferred rows.
Then propose only supported, applicable changes, obtain the provider's approval
and verify results. A broad setup request does not authorize sample catalog
creation, assignments, role grants, imports or scheduled-process submissions.

Also assess conditional prerequisites/outcomes and the non-FSM data migration,
background-processing and page-extension handoffs below. Keep Common's detailed
inventory separate from other areas' work products and return their references
to the offering; this overview does not transfer execution ownership to Common.

## Capability selection and readiness

| PM capability | Learning supplies | Owning guidance and boundary |
| --- | --- | --- |
| C1 Profile options | Business choices, exact code, level/target and desired value | [Profile definitions](../manage-profile-options.md) and [administrator values](../manage-administrator-profile-values.md). Configured values differ from effective session values. |
| C2 Common lookups | Applicable review buckets, governed codes/meanings and consumer impact | [Common lookups](../manage-common-lookups.md); verify category and editability. |
| C3 Learning security roles | Personas, identities or unresolved identity references, required actions and data scope | [Security decisions](security-decisions.md), then Security Role Guidance and the separate HCM Security Profile/Data Role workflows. Common does not assign roles. |
| C4 DFFs and value sets | Object/context/segment design, compatible values, dependencies and acceptance cases | [DFFs](../manage-descriptive-flexfields.md) and [value sets](../manage-value-sets.md); child-value support does not authorize root value-set creation. |
| C5 Oracle Search Indexes | Search/filter requirement and verified DFF/index/view dependencies | [Search indexes](../manage-search-indexes.md); global search and suggestion groups are separate tasks, while Search Views belong to the HCM Tool handoff. |
| C6 Catalog Administration Profiles | Ownership boundaries, contributors, visibility, existing items and default-profile decisions | [Existing CAP child](../../learning-catalog/manage-catalog-administration-profiles/SKILL.md), task CUSTOM_MANAGE_CATALOG_ADMINISTRATION_PROFILES, now catalogued under ORA_LEARNING_CATALOG. Keep its per-operation contracts unchanged. |
| C7 Non-provider Learning configurations | One design and current-to-proposed comparison per selected topic | [Learning Configurations](../../learning-configurations/SKILL.md) (ORA_LEARNING_CONFIGURATIONS), as detailed below; no new executor in Common. |
| C8 Learning prerequisites/outcomes | Intended sections/fields and Talent profile dependencies | Profile-type design below; do not confuse Talent/Model Profiles with CAPs or invent a mutation provider. |

Provider availability does not prove target readiness. The FDD's OLC-100310
dependency is neither a universal refusal for supported operations nor
permission to invent an endpoint for the rest. Current resource-graph gaps
and provider gates remain in force. Advisory assessment is not end-to-end
automation.

The C6 requirement paragraph in FDD version 7 names Manage Administrator Profile
Values as its executor. That conflicts with its CAP capability, scenarios and
the catalog task. Treat this as a source routing discrepancy: hand CAP intent
to the existing CAP child, never to the profile-value provider. Common does not
create CAPs, assign contributors/roles or adopt the sample's synthetic empty
baseline. Preserve the discrepancy for PM review without changing the child.

External provider configuration, audiences/groups, resources, catalog master
data, assignments and other transactions are outside Common's own task scope,
not outside the offering-wide assessment. Capture their applicability and route
selected work through the offering's owning child workflow.
Preserve the working Audience Data Loader/criteria contracts. Approval-rule
customization is separate HCM Tool work, not an implicit Common setup change.

## C7: non-provider task intake

Hand off to [Learning Configurations](../../learning-configurations/SKILL.md)
with known decisions and evidence. Its task files own detailed defaults and
background-processing guidance; preserve the intake below for Common callers.
The child includes a full configuration inventory and explicitly incomplete
live contracts, not a new execution fallback.

The current catalog has two tasks in ORA_LEARNING_CONFIGURATIONS:
`CUSTOM_CONFIGURE_LEARNING_DEFAULTS` and
`CUSTOM_CONFIGURE_BACKGROUND_PROCESSING`. Both have CSV and export/import
support false. The older CUSTOM_LEARNING_SETUP grouping and five individual
task identities must not be used as the current catalog route.

Preserve the FDD's five business topics below without pretending each is a
separate current FSM task. The first four require the Learning Configurations
owner to bind the requested fields to the supported defaults/configuration
workflow; the taxonomy does not by itself prove those fields or operations.

| Topic | Ask only for unresolved decisions | Completion evidence to request |
| --- | --- | --- |
| Conversation defaults | Which Learning conversation behavior, audience and default should change? Resolve actual current fields; do not reinterpret this as AI-agent deployment. | Before/after values and the agreed persona scenario. |
| Calendar event templates | Which learner/instructor templates, languages, event details and delivery channels? Keep profile enablement separate from template content. | Approved template revision and a sample event/ICS for each audience. |
| Assignment and catalog defaults | Which exact defaults/populations, and what new/existing-item behavior? Obtain current supported fields first. | Saved defaults plus representative creation/assignment behavior; do not assume existing records were rewritten. |
| Alerts | Which alerts, recipients, conditions, timing and channel? Reconcile with calendar integration and notification-pattern choices. | Configuration, processing evidence and expected delivery/non-delivery cases. |
| Background processing | Which process, workload, schedule/timezone and concurrency requirement? Reuse a suitable schedule. | Exact approved job/parameters/schedule, terminal status and downstream effect when an executor is declared. |

Do not flip flags, invent import modes/business objects or substitute generic
REST/ESS calls. Preserve a design proposal and identify the missing task
contract and owner. Recommendations require source-confirmed fields and
permitted values; never invent concurrency defaults or job identifiers.
An alert configuration does not prove delivery, and a submission does not
prove process completion.

## C8: prerequisites and outcomes

Confirm Talent Management availability and whether the requirement concerns
prerequisites, outcomes or both. Capture relevant content sections, displayed
fields and intended Learning pages. The reviewed
[Oracle setup guidance](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/set-up-oracle-learning.html)
distinguishes the Prerequisite profile type from Person sections with the
Learning Outcomes subscriber. Check Dynamic Skills applicability separately.
Do not confuse these with CAPs or create worker/person records to configure
them. Keep the design pending a selected profile-type workflow, and validate
administrator setup and learner-facing behavior after authorized configuration.

## Non-FSM foundation handoffs

These three approved taxonomy mappings have no invented FSM task codes:

- **Data Load and Migration Foundation Skill**: Learning Assignment / Learning
  Record Data Load; capture object, operation, source data/artifact, target and
  reconciliation needs. Use its declared Data Loader route. HDL, HSDL, FSM
  export/import, setup migration and integrated workbooks are available only
  when the selected provider explicitly supports that operation.
- **Background Process Foundation Skill**: Learning Configurations; capture the
  exact job contract, parameters, existing schedule, timezone and monitoring
  requirements. Use the selected ESS or already-declared loader workflow,
  never a job package inferred from a display name. The reviewed
  [process guidance](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/scheduled-background-processes-for-oracle-learning.html)
  distinguishes Oracle-managed/customer-scheduled and Support-only jobs.
  Verify language prerequisites, avoid duplicate schedules, and monitor the
  original request rather than resubmitting an uncertain operation.
- **Visual Builder and Redwood Extension Foundation Skill**: Learning Resources,
  Catalog and Assignment; capture page, persona, business rule/page property,
  agent-access requirements and publication environment. Select an approved
  extension workflow before changing/publishing anything. Profile enablement
  does not deploy an extension or grant agent access. No extension executor
  is supplied by this Common skill.

## Coverage and evidence limits

The FDD elaborates C1/general behavior, supplies C2 workbook guidance and C4
product references, and supplies C6 attachment/FDD guidance owned by the CAP
child. C3/C5/C7/C8 require the appropriate supported execution contracts beyond
this intake. Record unsupported or uncertain steps explicitly and ask users
only for business information they can provide, not for a guessed API.
Use [Common workflow](workflow.md) for source handling, proposals and results.
