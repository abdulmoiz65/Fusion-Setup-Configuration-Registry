# Leave Agreements Defaulting Rules

Redwood defines View, Create, Edit, and Delete of the current leave agreement template, including supported child maintenance. The supplied Agreement and Conversion create evidence grounds the defaults below. Apply create defaults only to new records after their pattern and lookup values are resolved; retain the stored before state for Edit and Delete. Never override an explicit valid user value or treat a loader date control as a date-effective lifecycle.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveStartDate / RangeStartDate | Current system date in YYYY-MM-DD format | A new parent Create omits both values; child Add uses verified stored parent context | No; preserve a requester-supplied date |  |
| AgreementPatternCode | ORA_ANC_CHP_AGRMT | Create explicitly selects Agreement and omits AgreementPatternCode | No | resolve_agreement_pattern_code |
| AgreementPatternCode | ORA_ANC_CHP_CONV | Create explicitly selects Conversion and omits AgreementPatternCode | No | resolve_agreement_pattern_code |
| ManagementTypeCode | UD | Create selects Agreement or Conversion, the value is omitted, and the ANC_SETUP_OBJ_MGMT lookup still confirms the observed read-only User-defined value | No | resolve_agreement_management_type |
| StatusCode | P | Create selects Agreement or Conversion, the value is omitted, and the ANC_SETUP_OBJ_STATUS lookup still confirms Pending | No | resolve_agreement_status |
| PartnerRuleCode | ORA_ANC_NOT_APPL | Create selects Agreement or Conversion, the value is omitted, and the ORA_ANC_PARTNER_RULE lookup still confirms the code | No | resolve_agreement_partner_rule |
| EligibilityRuleCode | ORA_ANC_NOT_APPL | Create selects Agreement or Conversion, the value is omitted, and the ORA_ANC_ELIGIBILITY lookup still confirms the code | No | resolve_agreement_eligibility_rule |
| LegislationCode | US | Create business context explicitly selects United States or a confirmed project policy supplies United States, and the territory lookup confirms US | No | resolve_agreement_legislation |
| EffectiveEndDate | Omit | Ordinary create omits an end date and the current Data Loader template permits omission | No | refresh_leave_agreement_dataloader_contract |

## Pattern-Specific Shape

| Agreement Pattern | Applies When | Parent Values | absenceAgreementPlans Values | Values That Must Remain Absent |
|---|---|---|---|---|
| Agreement | Create or an entitlement row is added or changed | AgreementPatternCode ORA_ANC_CHP_AGRMT; retain the stored pattern for an existing parent | Create requires at least one Target Plan; each new or changed row retains or resolves its exact TargetPlanId | SourceAbsenceTypeId and SourcePlanId |
| Conversion | Create or a source dependency or entitlement row is changed | AgreementPatternCode ORA_ANC_CHP_CONV and a resolved SourceAbsenceTypeId; retain valid stored values unless the current UI permits their change | Every new or changed row has a valid SourcePlanId-to-TargetPlanId mapping within the resolved Source Absence Type | None of the applicable conversion source fields |

A plain parent Edit does not require new entitlement rows, plan identifiers, source values, or create defaults. Review its full stored configuration and validate only dependencies affected by the changed fields. Retain existing child identity and parent binding.

The observed response end date `4712-12-31` is server behavior, not a client default. Do not add it to a Data Loader source unless the current registered template and operation contract require it.

## Current-Version Data Loader Controls

For Create, treat `EffectiveStartDate` as the normalized parent business Start Date. Never accept `effectiveOf` as free-form caller input. Refresh the registered `absenceLeaveAgreementTemplates` Data Loader template before preparation. The existing native Create contract uses `RangeStartDate` as an adapter context; this does not create a date-effective maintenance model. The template and final DAT `METADATA` may retain the physical `EffectiveStartDate` attribute, but its create data-record value remains blank by default.

Edit and Delete address the exact current parent or supported child identity. For Edit, derive `effectiveOf=RangeMode=CORRECTION;RangeStartDate=<verified stored parent Start Date>` from the current read; this is the loader's in-place control, not a user-visible dated Correction action or new operation date. For current whole-object Delete, derive date-free `effectiveOf=RangeMode=ZAP` because Fusion requires the Effective-Of header for DELETION on this date-effective resource. Do not accept a caller-supplied update date, derive UPDATE or a dated Delete mode, or change stored physical dates. Creating a child under an existing parent uses the same verified stored parent Start Date as native child-create context; it never resets the parent date.

The `RestAction` values below are Data Loader DAT controls. They do not authorize a direct REST-client call; every mutation remains exclusively delegated to `core.data-loader` in REST mode.

| Requested Operation | RestAction | effectiveOf | Required Input |
|---|---|---|---|
| Create current template | POST | RangeStartDate=<parent business Start Date> for populated sections that require it under the existing native Create contract | Supplied Start Date or disclosed create-only current-date default; physical EffectiveStartDate remains blank by default |
| Add supported child under existing parent | POST | RangeStartDate=<known stored parent Start Date> only where the existing native child-create contract requires it | Exact current parent binding, new child choices and current section contract; do not request a replacement parent Start Date |
| Edit current parent or supported child | PATCH | `RangeMode=CORRECTION;RangeStartDate=<verified stored parent Start Date>` | Full before state, exact current parent/child identity, UI-permitted changed fields, affected dependencies and current adapter support; no new operation date |
| Delete current parent or supported child | DELETE | RangeMode=ZAP | Exact current parent/child identity, explicit whole-object deletion scope, applicable protection/reference impact and immutable Data Loader approval; no new operation date |

Dated Update, Correction, End date, Delete changes, and caller-selected ZAP business actions are unsupported for this current-version Redwood task. Internal CORRECTION for Edit and date-free ZAP for whole-object Delete are loader controls for the two supported UI actions. Explain an unavailable dated operation and present the applicable View, Create, Edit, or Delete choice; do not silently translate the request or mark all supported operations blocked. A missing Edit or Delete adapter mapping is an execution gap for that supported operation, separate from its business availability.

## Values That Must Not Be Defaulted

| Field or Value | Why It Must Not Be Defaulted | Required Action |
|---|---|---|
| Operation date for Edit or Delete | Current-version maintenance addresses stored identity rather than a new effective slice | Do not ask for or default an operation date; retain the parent Start Date only as stored context |
| EffectiveEndDate for create | The captured create omitted it and does not prove a portable client default | Do not request or synthesize it; omit it unless explicitly supplied and current-contract-valid |
| effectiveOf | It is an internal adapter control, not caller input or a maintenance lifecycle | Create uses its new Start Date; Edit uses CORRECTION with the verified stored parent Start Date; whole-object Delete uses date-free ZAP. Never use UPDATE or a caller-selected update date for Edit |
| Physical EffectiveStartDate data-record value | Header presence does not populate the value or authorize changing the stored Start Date | Leave it blank for Create by default; omit stored-date changes from Edit/Delete unless explicitly permitted by the current UI and adapter |
| Dual-population support for Create | Exposing both attributes does not prove the native create contract accepts both populated simultaneously | Require equal normalized dates and explicit current create-section evidence before permitting dual population; a mismatch always blocks |
| EffectiveEndDate value 4712-12-31 | A returned server value is not a portable create default | Never add it solely because it appeared in an observed response |
| TargetPlanName or TargetPlanId | A new or changed entitlement has a user-selected dependency, not a pattern default | Require an exact retained or resolved identity for each affected row. Resolve supplied names through resolve_target_absence_plan; a plain parent Edit does not require new plan IDs. Never infer a plan from an agreement name, legislation, or first result. |
| SourcePlanName or SourcePlanId | A new or changed Conversion mapping has a selected source dependency | Retain valid stored mappings on plain parent Edit. Resolve supplied source names through resolve_source_absence_plan using the returned Source Absence Type plans link; never construct the URL from its numeric ID or select the first result. |
| Legislative Grouping | It is a legislation-scoped requester choice | Leave it absent unless supplied; resolve the exact business value and clear it when Legislation changes |
| Validation Formula | No portable validation formula default is documented | Leave it absent unless supplied and exactly resolved by formula name |
| Denial Reasons and Withdrawal Reasons | These are ordered business selections, not universal defaults | Leave each list absent unless supplied; resolve the complete list and preserve its order |
| Event Type | It is optional and valid only for Agreement | Leave it absent unless supplied for Agreement; reject it for Conversion |
| Eligibility Formula and Eligibility Profile | The selected Eligibility Rule determines which one is allowed | Populate only the dependency selected by the rule; never default or populate both, and clear stale values when the rule changes |
| Payment Percentage Display Formula | It is a plan-child business selection | Leave it absent unless supplied for that plan item and exactly resolved |
| Override Allowed | It depends on a Payment Percentage Display Formula in the same plan item | Leave it absent unless explicitly supplied after the formula is resolved; never infer Yes or No |
| Certification Name or identifier | Certifications are legislation-scoped child selections | Leave certification children absent unless supplied; resolve each exact name in the current Legislation and clear stale selections when Legislation changes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LA.APPLY_DEFAULTS | step | 120 | apply_default | applied_or_not_needed->LA.VALIDATE_EFFECTIVE_CONTEXT;unresolved->LA.HANDLE_ISSUE | LA.REFRESH_DATALOADER_CONTRACT | stop | Apply only eligible omitted create defaults and create-only pattern-confirmed, lookup-verified coded defaults; Edit/Delete retain before state and receive no create defaults |
