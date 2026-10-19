# Absence Categories Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| absenceCategories.EffectiveStartDate / RangeStartDate | Current system date in YYYY-MM-DD format only after consultant confirmation | Create only: the parent omits both fields, current live parent metadata marks EffectiveStartDate mandatory for new records, and the consultant confirms the displayed system date | No; retain a user-supplied parent effective start date |  |
| absenceCategoryTypes.EffectiveStartDate | Resolved absenceCategories.EffectiveStartDate | An associated-type child row omits EffectiveStartDate | No; retain a user-supplied child effective start date |  |
| Language | No client default; Fusion derives the value from the authenticated login context | Every create request | Not applicable; omit Language from prepared input |  |
| EffectiveEndDate | No client default; preserve the resolved existing end date when required as a DDF/DFF maintenance identity field | EffectiveEndDate was not explicitly supplied by the user | No; omit ordinary parent defaults, but retain the observed child date without changing it | resolve_absence_category_flex_dataloader_contract |
| AbsenceCategoryId | Fusion-generated identifier | Every create request | Not applicable; omit the field |  |
| AncAbsCategoryFAltcd | Fusion-generated alternative code | Every create request | Not applicable; omit the field |  |
| BaseName | Fusion-generated normalized category and legislation base name | Every create request | Not applicable; omit the field |  |
| ManagementTypeCd | Fusion server behavior returned UD for the captured create flow | ManagementTypeCd was not explicitly supplied | No; omit the field and allow Fusion to derive it |  |
| AbsenceCategoriesDDFFlex and AbsenceCategoriesFlex RestAction | PATCH, with MERGE as the DAT directive | A correction or update changes an existing DDF or DFF child row | No; derive from the selected maintenance operation, not from whether its segment value is blank |  |
| Meaning and audit fields | Fusion-derived or system-maintained values | Every create request | Not applicable; omit them |  |

For a create, resolve the parent EffectiveStartDate first. Only when it is omitted, current live parent metadata marks it mandatory for new records, and the consultant explicitly confirms the displayed system date, use that date in YYYY-MM-DD format. Then copy that resolved parent date to each absenceCategoryTypes child that omits its own EffectiveStartDate. Never overwrite an explicitly supplied parent or child effective start date. Non-create operations never default an effective date.

Language and EffectiveEndDate are never populated by a client-side default. Language is always omitted because Fusion derives it from login context. EffectiveEndDate is omitted unless the user explicitly supplies it or the existing child end date is retained as required DDF/DFF maintenance identity.

The supplied BO registration supports maintenance of both flex sections using
AbsenceCategoryId on ANC_ABSENCE_CATEGORIES_F. Preserve the effective range as
well as the category ID. A blank segment on an existing row uses PATCH. The
MERGE_DELETE registration describes DAT operations; it does not make MERGE a
valid RestAction.

## Flexfield Correction and Update Capability

| Requested operation | Parent absenceCategories | AbsenceCategoriesDDFFlex | AbsenceCategoriesFlex |
|---|---|---|---|
| Update | PATCH first at the requested effective date to establish the planned update slice; preserve unchanged parent business values | PATCH with registered category ID, planned slice start, resolved existing slice end, and the same UPDATE effectiveOf | PATCH with registered category ID, planned slice start, resolved existing slice end, and the same UPDATE effectiveOf |
| Correction | PATCH only if parent business fields also change; retain the selected historical slice | PATCH with registered category ID, selected existing slice start/end, and CORRECTION effectiveOf | PATCH with registered category ID, selected existing slice start/end, and CORRECTION effectiveOf |

Include only requested flex sections and changed segments. A parent-only request
does not add flex rows. For an update within an existing slice, use the requested
effective date as the planned slice start and preserve its observed end; do not
invent an end date or extend across an existing later slice. For correction,
use the selected existing slice dates, including the original start when that
is the user's selected correction scope. Keep the selected existing identity
separate from the planned update identity in the preview. A correction never
becomes an UPDATE solely because the correction is performed today.

## Date-Effective Operation Mapping

For parent-category end-dating, apply the parent-only scope rule in
ora_design_enforcement.md. The End date mapping below does not imply a child
operation or a change to the underlying absence type.

Derive `effectiveOf` independently for each row's operation. Never
accept it as a free-form input. A create may default EffectiveStartDate only
when live parent metadata marks it mandatory for new records; never default a
date, range, deletion scope, or destructive decision for a non-create
operation.

| Requested operation | RestAction | effectiveOf | Required input |
|---|---|---|---|
| Create | POST | `RangeStartDate=<EffectiveStartDate>` | EffectiveStartDate; default only when omitted and the live parent metadata requires it |
| Update | PATCH | `RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate>` | Selected effective-dated identity and explicit EffectiveStartDate |
| Correction | PATCH | `RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate>` | Selected effective-dated identity and explicit EffectiveStartDate |
| End date | PATCH | `RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate>` | Resolved AbsenceCategoryId, EffectiveStartDate, Name, LegislationCode, Status; explicit EffectiveEndDate; preserve parent fields under ora_input_validation.md |
| Delete changes | DELETE | `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate>` | Selected effective-dated identity, explicit EffectiveStartDate, and explicit DELETE_CHANGES scope |
| ZAP | DELETE | `RangeMode=ZAP` | Selected category identity, explicit destructive intent, and immutable Data Loader approval |

An existing category can receive a new association without creating a new
category. The association row uses the Create mapping (POST and
RangeStartDate), while an existing parent or flex row uses its own selected
maintenance mapping. Do not copy a parent's UPDATE or CORRECTION RangeMode
onto a newly created association. Existing flex rows participating in the
parent's update continue to share the parent's derived range.

| Requested operation | RestAction | effectiveOf | Required input |
|---|---|---|---|
| Add association to existing category | POST | RangeStartDate=<EffectiveStartDate> | Resolved AbsenceCategoryId, existing AbsenceTypeId, Status and explicit association start date; omit generated AbsenceTypeCateId |
| Update existing association | PATCH | RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate> | Resolved existing AbsenceTypeCateId and parent identity, selected existing association range and explicit update date |
| Correct existing association | PATCH | RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate> | Resolved existing AbsenceTypeCateId and parent identity, selected historical association range and explicit correction date |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AC.APPLY_SERVER_RULES | step | 20 | apply_default | applied_or_not_needed->AC.RESOLVE_CATEGORY_IDENTITY;invalid->AC.HANDLE_ISSUE | AC.VALIDATE_INPUT | stop | After input validation and before lookup resolution; non-create operations do not apply create defaults |
