# Performance Templates REST guidance

This reference explains resource ownership, field mappings, and validation
boundaries for the task's declared REST route. Validate supported operations,
writable fields, required values, and defaults against fresh Describe metadata
from the configured environment. UI behavior and effective privileges must be
verified for the target release; this reference does not replace those checks.

## Resource and child ownership

The backend declares `talentPerformanceTemplates` as unlisted. Its availability
does not establish a supported public integration contract. Permit operations
only through the task's declared route and target metadata; do not assume that
ordinary root `DELETE` is available.

Use `/hcmRestApi/resources/11.13.18.05/talentPerformanceTemplates` only through
the selected shared REST workflow and configured environment. Resolve child
links from the owning record. The child suffixes below are relative to a
template singleton and include the ADF `child` segment.

| Object | Owning accessor suffix | Row identity |
| --- | --- | --- |
| Alerts | `child/alerts` | `ProcessStepId` |
| Template eligibility | `child/eligibilityProfiles` | `TalentEligibilityProfileObjectId` |
| Roles | `child/roles` | `TmplRoleId` |
| Sections | `child/sections` | `SectionId` |
| Section items | `child/sections/{SectionId}/child/items` | `ItemId` |
| Section role actions | `child/sections/{SectionId}/child/roleActions` | `TmplRoleActionId` |
| Periods | `child/periods` | `TmplPeriodId` |
| Period document types | `child/periods/{TmplPeriodId}/child/documentTypes` | `TmplPeriodDocumentTypeId` |
| Period due dates | `child/periods/{TmplPeriodId}/child/dueDates` | `TmplPeriodDateId` |
| Period eligibility | `child/periods/{TmplPeriodId}/child/eligibilityProfiles` | `TalentEligibilityProfileObjectId` |
| Period questionnaires | `child/periods/{TmplPeriodId}/child/questionnaires` | `TmplPeriodQstnrId` |

The child hierarchy does not override target operation permissions.
Inspect target metadata before permitting create, patch, or delete. Never
accept a child ID from another template, section, or period as proof of
ownership.

## Root custom operations

The task execution contract declares the following actions, subject to target
metadata and privileges:

| Method | Inputs / behavior to verify |
| --- | --- |
| `findByAdvancedSearchQuery` | Search filters, limit, offset and sort; supported sort fields are Name, DateFrom and DateTo |
| `duplicatePerformanceTemplate` | `templateDefinitionId`, `newTemplateName`, `copyPeriods`, `periods`; verify the copied child graph and period choices |
| `deletePerformanceTemplate` | `templateDefinitionId`; checks document use and removes the owned graph; verify absence after success |
| `submitEssRequestForTemplate` | `templateDefinitionId`; returns a request ID, which is submission evidence, not completion |
| `getFastFormulaList` | No inputs; read-only formula lookup; return eligible formula choices without claiming a template mutation |

Inspect the target action metadata for the exact invocation shape. Do not
invent an item-level action URL or call ordinary root DELETE. A no-match
custom delete can return without deleting anything, so pre-read and post-read
evidence are required. Do not replay a timed-out mutation automatically.

## Keep REST fields separate from FSM and entity fields

REST names come from the resource contract, not the entity attribute or CSV
heading. Use the live Describe allowlist as the final payload gate. Do not
assume that source attributes such as `SetId`, `BusinessGroupId`,
`ObjectVersionNumber`, `SearchTerms`, or `IncludeTalentReviewCalibrationFlag`
are exposed or writable on the target. Use only finders declared by target
metadata; do not infer `findByWord` support from a backend declaration.

| Context | REST field | Other name that must not be copied into this REST payload |
| --- | --- | --- |
| Root | `Status` | Entity/FSM `StatusCode` |
| Root, only if target exposes it as writable | `SetId` | FSM `SetCode`; omit SetId when target metadata does not permit it |
| Root | `AutoPopulateMatrixMgrFlag` | `AutoPopulateMmFlag` |
| Root | `UseCalculatedRatingsOnlyFlag` | `UseCalcRatingsOnlyFlag` |
| Root | `PcpnFeedbackRequestFlag` | `PcpnFeedbackReqFlag` |
| Root | `WkrSeeMgrPcpnsFlag` | `WrkSeeMgrPcpnFlag` |
| Root | `TotalMinimumPcpns`, `TotalMaximumPcpns` | `TotalMinParticipants`, `TotalMaxParticipants` |
| Root | `ShowWkrCalculatedRatingsFlag`, `ShowMgrCalculatedRatingsFlag` | `ShowWkrCalcRatingFlag`, `ShowMgrCalcRatingFlag` |
| Template role | `MinimumNumberPcpns`, `MaximumNumberPcpns` | `MinimumNumPcpns`, `MaximumNumPcpns` |
| Period | `AvailableToUseFlag` | UI label or inferred `AvailableFlag` |
| Questionnaire / role action | `TmplRoleId` | Standalone performance `RoleId` or CSV `UserRoleTypeCode` |
| Role action | `ViewMgrQstnrScoresCode`, `ViewOwnQstnrScoresCode`, `ViewPcpnQstnrScoresCode`, `ViewWkrQstnrScoresCode` | Inferred score fields ending in `Flag` |
| Item | `MinimumWeight`, `TargetPerformanceRatingId`, `TargetProficiencyRatingId` | `MinWeight`, `TargetPerfRevRatingId`, `TargetProfRevRatingId` |

Questionnaire creation needs the owning period plus `QuestionnaireId`,
`TmplRoleId` and `SectionId`. Resolve the template role and questionnaire
section within the same template. Read-only role-action display fields include
`RoleId`, `RoleName` and `RoleTypeCode`.

Eligibility associations use `EligibilityProfileId` and boolean
`RequiredFlag`, with `TalentObjectId`/`TalentObjectType` identifying the owner.
The template and period accessors supply different owner contexts. Do not
retarget an existing association by patching its create-only owner fields.
Reject a duplicate profile within the same object ID and object type.

Check create and upsert support separately for the requested collection.
Upsert is not a safe default for an ordinary create:
only select it when the task execution contract, exact matching identity and
approved business effect explicitly allow it.

Root create requires `Name`, `DocumentTypeId`, and any additional mandatory
fields without defaults in target metadata. Supply `StarRatingEnabledFlag`
when it is required without a server default. Preserve a server default for
`DateFrom` when declared; require a value when mandatory without a default.
Do not request a generated primary key from the administrator. A process flow
is required when a period exists; do not require it for every incomplete
definition solely because a completed template needs one.

Do not submit generated keys, business-group values, object-version values,
joined secondary-entity fields, display names, lifecycle flags or ESS result
fields merely because an entity attribute appears updateable. Preserve the
target concurrency mechanism selected by the execution contract separately.

## Validation and execution boundaries

For PATCH, validate a fresh existing record merged with supplied changes.
Omitted fields retain their values. Explicit null is a requested clear and
must satisfy mandatory and dependent-field rules. Create defaults must not
overwrite omitted update fields.

Validation warnings must remain distinguishable from blocking errors.
Examples include star-rating/model-level warnings, inactive section/role
warnings, and the section performance-rating-model warning. Record the actual
target severity and message instead of treating every validation as an error.

An in-use flag alone is not a blanket edit prohibition. Oracle documents
specific permitted edits and an update process for existing documents. Due
date edits affect newly created documents; existing-document dates require
separate maintenance. See [Options for Updating In Use Performance Templates](https://docs.oracle.com/en/cloud/saas/talent-management/faupm/options-for-updating-in-use-performance-templates.html).

The current `PT.*` rule graph validates and prepares approval. It contains no
REST mutation executor. Reaching `PT.DONE` is not proof of create, patch,
delete, duplicate or process completion. The task's declared FSM import route
continues through `core.data-loader`. A direct REST mutation requires a
separately declared task execution contract and all its gates; otherwise
persist an execution-route blocker and stop before the external action.
