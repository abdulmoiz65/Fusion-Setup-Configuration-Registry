# Common taxonomy and source reconciliation

## Identity and provenance

Retrieved the [approved HCM Tool Learning taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-taxonomy/)
on 2026-09-22 (page generated 2026-09-21, PM-reviewed Learning baseline).
Common is cross-offering step 01, stage 1, priority P0, sourced from Common
Applications / ApplCore, task list **Learning Management Common Task List**.
Its Cleared dependency status is planning metadata, not a tenant access check.

The page has 12 ordered steps (7 Learning, 5 cross-offering) and 43 mappings.
Do not confuse mappings with the local catalog's 37 FSM tasks. Common has
**13 mappings: 10 FSM tasks and 3 non-FSM foundations**. The effective catalog
already contains offering ORA_LEARNING_MANAGEMENT and functional area
ORA_LEARNING_MANAGEMENT_COMMON. `pillar-skill-gen` generated the canonical ID
`hcm.learning-management.learning-management-common`; no catalog change was
needed. The cross-offering source does not change the requested HCM/Learning
folder ownership.

The profile-option consumer relationships below were rechecked against the
live taxonomy generated 2026-09-23. Both profile tasks serve Learning
Configurations, Learning Catalog, Learning Assignment, Recommendations and
External Providers. This focused update does not rebaseline the earlier
whole-page counts or change task identities and execution support.

## All Common mappings

Abbreviated consumers below are Learning functional areas. Task identities,
flags and ordering are preserved in the generated metadata. The source's
foundation labels identify providers/capabilities, not new repository skill IDs.

| Task / foundation | Exact catalog code | Source foundation | Needed by | Current handoff / limit |
| --- | --- | --- | --- | --- |
| Manage Profile Options | FND_MANAGE_PROFILE_OPTIONS | Application Profile Option Foundation Skill | Learning Configurations; Learning Catalog; Learning Assignment; Recommendations; External Providers | Inspect definitions via Apps Common profile provider; its parent resource is read-only. Do not recreate delivered definitions to change values. |
| Manage Administrator Profile Values | FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Application Profile Option Foundation Skill | Learning Configurations; Learning Catalog; Learning Assignment; Recommendations; External Providers | Apps Common profile provider for configured value children, with actual level/editability checks. |
| Manage Common Lookups | FND_MANAGE_COMMON_LOOKUPS | Application Lookup Foundation Skill | Learning Catalog; Recommendations; Learning Assignment | Apps Common lookup provider; verify Common category, exact type and seeded restrictions. |
| Manage Value Sets | FND_MANAGE_VALUE_SETS | Application Value Set Foundation Skill | Learning Resources; Learning Catalog; Learning Assignment | Apps Common value-set provider reads definitions and manages supported child values; root creation needs another approved setup route. |
| Manage Descriptive Flexfields | FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Application Flexfield Foundation Skill | Learning Resources; Learning Catalog; Learning Assignment | DFF provider: task export, approved Data Loader FSM import, separate deployment and verification. |
| Manage Applications Core Global Search Configurations | ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Application Search Configuration Foundation Skill | Learning Configurations | Capture global search requirement and current capability evidence; release/build optional; task-specific executable contract unresolved. |
| Manage Applications Core Global Search Suggestion Groups | ORA_FND_SUGGESTION_GROUPS | Application Search Configuration Foundation Skill | Learning Configurations | Capture suggestion group, intended suggestions/personas and current configuration; task-specific executable contract unresolved. |
| Manage Search Indexes | ORA_FND_MANAGE_INDEX_CONFIGURATION | Application Search Configuration Foundation Skill | Learning Configurations | Learning index/segment design plus ingestion dependency; task-specific index mutation contract unresolved. |
| Manage Audit Policies | FND_MANAGE_AUDIT_POLICIES | Audit and Reporting Foundation Skill | Learning Configurations | Audit provider's supported object/field operations; overall Fusion switch and existing field selection require implementor UI evidence. |
| Manage Audit Types | ORA_GMS_MANAGE_AUDIT_TYPES | Audit and Reporting Foundation Skill | Learning Configurations | Catalog mismatch under review: Grants audit-type task is not the Learning audit-policy operation. |
| Data Load and Migration Foundation Skill | Not an FSM task | Shared data-load foundation | Learning Assignment | Learning Record Data Load; HCM Data Loader, HCM Spreadsheet Data Loader, FSM Export, FSM Import, Setup Migration, Integrated Workbooks. Select only a supported object/operation route. |
| Background Process Foundation Skill | Not an FSM task | Shared background-process foundation | Learning Configurations | Scheduled Processes, Background Jobs, Process Monitoring; exact job contract and approval required. |
| Visual Builder and Redwood Extension Foundation Skill | Not an FSM task | Shared extension foundation | Learning Resources; Learning Catalog; Learning Assignment | Visual Builder Studio, VBS Business Rules, Redwood Page Properties, Agent Access on Redwood Pages; approved extension provider must be selected. |

Common collectively supports Configurations, Catalog, Recommendations,
Assignment, Resources and External Providers. Security Profile, Data Role, HCM Tool and Locations
are separate cross-offering steps. Learning CAP maintenance is not a new Common
FSM task. Do not move those tasks into this list or borrow Recruiting task IDs.

Use the [profile-option consumer handoff](dependencies.md#profile-option-consumer-handoffs)
to assess applicable settings and retain gaps in undelivered consuming workflows.

## Task guidance and readiness

- Search task CSV flags are N even though export/import is Y. Their generated
  REST mode and blank businessObject are scaffolding, not registered loader
  support. No sample download, invented endpoint or CSV override is permitted.
  Obtain a complete task contract from the provider/catalog owner first.
- [Manage Search Indexes](../manage-search-indexes.md#learning-index-readiness)
  owns Learning DFF/index/ingestion guidance and the separate Search Views handoff;
  its [publication guidance](../manage-search-indexes.md#configuration-and-publication)
  distinguishes saved edits, published metadata and search acceptance.
  [Oracle Text maintenance](../manage-search-indexes.md#oracle-text-maintenance-is-a-separate-operation)
  is a separate background-process handoff, not OSCS ingestion.
- [Manage Audit Policies](../manage-audit-policies.md#learning-audit-scope-and-evidence)
  owns supported Learning audit scope and API/UI evidence boundaries.
- [Manage Audit Types](../manage-audit-types.md#resolve-learning-applicability-before-execution)
  retains the Grants/Learning identity discrepancy and catalog-owner next action.
- [Non-FSM foundation handoffs](setup-capability-handoffs.md#non-fsm-foundation-handoffs)
  own data-load, background-process and extension questions and provider limits.

## Source precedence and coverage

| Source | Use and limits |
| --- | --- |
| Approved taxonomy above and effective local catalog | Functional-area membership, task identity, consumers and flags. A name match or roadmap clearance does not prove execution support. |
| [PM Learning Setup FDD](https://confluence.oraclecorp.com/confluence/display/VS/OLC-115246+FDD%3A+Learning+Setup+Skill), page 21511838840, version 7, updated 2026-09-14, reread 2026-09-22 | Business questions and GB-01–GB-16 proposal/review behavior. C1/C2/C4 and C5 dependencies inform Common; C6 CAP, C7 Learning Configurations and C8 Talent profiles remain handoffs. |
| Existing offering setup guidance and references, reviewed 2026-09-21 | Migrated into corresponding Common task files, workflow and capability handoffs. The old CUSTOM_LEARNING_SETUP grouping is not the new Common taxonomy. The offering reference indexes have been retired; guidance and scenarios remain in Common, with a compatibility link at the previous acceptance-test path. |
| FDD attachments: oracle_learning_profile_options_triage.xlsx (21940378693), oracle-learning-extensible-lookups-guidance.xlsx (21940378739), catalog-administration-profile-skill-requirements.md (21940378766) | Live metadata rechecked 2026-09-22: all version 1. Re-read the previously retrieved profile (18,027 bytes) and lookup (15,690 bytes) workbooks matching those IDs/sizes; no attachment edit. Per-code review and source conflicts live in their task files. CAP scenarios remain with its existing child and C6 handoff; examples are not current tenant values. |
| [Common Applications Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/common-applications-foundation-skill-baseline/), baseline reference reviewed 2026-09-18 | Shared ownership and provider handoffs. Earlier profile-options.lookup, profile-options.value-sets and profile-options.descriptive-flex labels refer to the separate current Apps Common providers; task codes, provider routing keys and business-object names remain distinct. |
| [Current Oracle Learning configuration guide](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/index.html), reviewed 2026-09-22 | Current product behavior, not tenant state. Review current provider capability metadata before execution; target release/build is optional context. |
| [Profile options for Oracle Learning](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/profile-options-for-oracle-learning.html#u30266299), rechecked 2026-09-22 | All 33 published codes are covered in Manage Administrator Profile Values. Clarified search modes, retake scope, diagnostic values and content exclusions. FND_LANGUAGE and Communities retain their separately sourced applicability checks; the page does not establish PM review categories or target values. |
| [Extensible lookups for Oracle Learning](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/extensible-lookups-for-oracle-learning.html#u30266300), rechecked 2026-09-22 | All 30 published types are covered in Manage Common Lookups. Clarified consumer/action distinctions without changing the PM workbook's review buckets or permitting seeded-data changes. |
| [Descriptive flexfields for Oracle Learning](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/descriptive-flexfields-for-oracle-learning.html#u30266300), rechecked 2026-09-22 | All six code-to-object mappings agree with Manage Descriptive Flexfields. This overview supplies no deployment identifiers or export schema; [DFF verification](dff-verification.md) binds inspection to the existing core/shared provider and checks actual returned metadata. |
| [Manage Values (Applications Common 26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oaext/manage-values.html) and [HCM Overview of Value Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/overview-of-value-sets.html), reviewed 2026-09-22 | Manage Value Sets now covers definition-versus-value scope, validation choices, protection, security and implementer UI guidance. Linked validation/usage references support dependency and deployment checks. Product documentation does not add a root-definition writer, browser fallback or new registered execution route. |
| [Overview of Search Indexes (Applications Common 26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-search-indexes.html), [Add Extensible Attributes to Search Indexes (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/add-extensible-attributes-to-search-indexes.html) and [Remove Extensible Attributes from Search Indexes (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/remove-extensible-attributes-from-search-indexes.html), reviewed 2026-09-22 | Manage Search Indexes distinguishes selection for additions from deselection for removals, with both limited to non-predefined attributes and requiring Publish after Save and Close. Publication remains distinct from ingestion/acceptance. Baseline/delta and pending-edit safeguards apply the Common workflow to this task. The UI procedures do not resolve the missing provider contract or authorize a browser/REST fallback. |
| [24B Learning considerations](https://docs.oracle.com/en/cloud/saas/readiness/hcm/24b/lear-24b/24B-learning-wn-t57007.htm), reviewed 2026-09-22 | Historical Explore/Browse Redwood reingestion prerequisite using fa-hcm-learningitem. Not evidence of current tenant state or a mandate to rerun an already completed upgrade step. |
| [25B catalog DFF search filters](https://docs.oracle.com/en/cloud/saas/readiness/hcm/25b/lear-25b/25B-learning-wn-f38613.htm), [current Learning setup](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/set-up-oracle-learning.html) and [current initial-ingestion guide](https://docs.oracle.com/en/cloud/saas/human-resources/faeos/run-initial-data-ingestion.html), reviewed 2026-09-22 | Catalog liFlexFields mapping, page prerequisites, supported search uses and index-to-view dependencies. Distinguish initial initialization from change-driven reingestion. Historical rollout/patch notes are not current-release prerequisites. Select only feature-relevant indexes; no blank-parameter full ingestion or new ESS execution binding. |
| [Optimize Learning Text Indexes](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/optimize-learning-text-indexes.html), reviewed 2026-09-22 | Separate Oracle Text maintenance, monthly frequency restriction and Support-only recreation with search downtime. Not an OSCS refresh or automatic authorization to submit/reschedule jobs. |
| Oracle_Learning_Security_Decision_Support.xlsx and Decision support for Oracle Learning security.docx, user supplied, read 2026-09-22 | Security discovery and mappings; see sheet/row provenance in security-decisions.md. Not verified role codes, production approvals or assignment artifacts. |

When sources disagree, preserve the disagreement and its affected scope.
Current Oracle documentation establishes product support; the target provider
establishes actual metadata and current state; customer decisions select the
desired design. Neither overrides taxonomy identity silently. Optional missing
business information prompts a focused question or deferral; an unavailable
technical route stops only the dependent external operation.

## FDD requirement ownership and limits

The full live page remains version 7, updated 2026-09-14, on the 2026-09-22
deep review. Use its requirements and business decisions, not sample dialogue
counts, blank placeholder tables or accidental provider names. The table below
keeps this review traceable without copying the FDD into the skill.

| FDD requirement | Maintained Common guidance | Verification / boundary |
| --- | --- | --- |
| GB-01–GB-03: intent, supported input and files as data | [Workflow intake](workflow.md#intake-and-focused-questions) | S01–S03; source content never authorizes execution. |
| GB-04–GB-06: validation, source separation and baseline | [Validation summary](workflow.md#implementer-facing-validation-and-confirmation), task-specific column mapping and provider reads | S04–S05, D02–D03; unread values remain Not validated. |
| GB-07–GB-09: focused questions, recommendations and dependencies | [Profile entry paths](../manage-administrator-profile-values.md#entry-paths-and-baseline-aware-questions), BQ-01–BQ-09 and [capability handoffs](setup-capability-handoffs.md) | S06–S15, D01, D04; retain valid exceptions and optional deferrals. |
| GB-10–GB-12: delta, immediate approval and one submission | [Proposal/result contract](workflow.md#proposal-and-result-contract) | S16–S17, D05; counts come from current keys and supported operations. |
| GB-13–GB-16: readback, actionable issues, audit and responses | [Results](workflow.md#proposal-and-result-contract), [diagnostics](workflow.md#issues-and-diagnostics) and [confirmation](workflow.md#implementer-facing-validation-and-confirmation) | S18–S20; no success from acceptance, no duplicate execution. |
| C1 and scenarios 1.1–1.3 | [Administrator profile values](../manage-administrator-profile-values.md), with [definition handoff](../manage-profile-options.md) | Source contradictions are resolved explicitly in the task's conflict table; not every illustrated value is a supported enum. |
| C2 and lookup workbook | [Lookup proposal intake](../manage-common-lookups.md#from-review-guidance-to-value-proposals) and per-type review | S14–S15, D06–D07; type guidance is not executable lookup-value data. |
| C4, including value sets | [DFFs](../manage-descriptive-flexfields.md) and [value sets](../manage-value-sets.md) | S21; FDD supplies the Oracle DFF reference, not new payload fields or an export-evidence binding. Existing guidance remains applicable. |
| C3, C5, C6, C7, C8 | [Capability handoffs](setup-capability-handoffs.md), security and search task guidance | S21–S24, D08; CAP's mistaken profile-provider reference grants no execution authority. |
| Audit, global search and suggestion tasks; unfinished FDD sections | Current Common taxonomy and each task's existing contract | No new FDD-specific requirements inferred. Keep the five incomplete resource contracts fail-closed. |

S01–S24 and D01–D08 are [behavioral review scenarios](../tests/learning-setup-acceptance.md),
not a claim of automated tenant acceptance. The FDD's acceptance-criteria and
API sections remain incomplete; this reconciliation does not invent their
missing designs or mark the OLC-100310 dependency resolved.
