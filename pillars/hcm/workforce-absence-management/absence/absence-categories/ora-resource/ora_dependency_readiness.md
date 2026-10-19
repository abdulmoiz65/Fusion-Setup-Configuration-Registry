# Absence Categories Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Selected category identity | For every non-create request, resolve one category and its selected effective-dated slice by exact name or previously resolved ID, and legislation when supplied |
| 2 | Category status | Resolve the supplied status through ANC_SETUP_OBJ_STATUS and retain LookupCode |
| 3 | Legislation | When supplied or required by an associated type, resolve one territory and retain TerritoryCode |
| 4 | Associated absence type | When supplied, resolve one existing type that matches legislation and is effective on the resolved association start date, which inherits the category start date when omitted |
| 5 | Flexfield metadata | When flexfield values are supplied, refresh absenceCategories describe and validate contexts and segments |
| 6 | Existing flex row and registration | For correction or update, resolve the requested child, registered category ID and effective date range |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_category_identity | Selected absence category | Yes | Every non-create request | Lookup | Exact category Name or previously resolved ID, selected effective date, and optional LegislationCode | find_absence_category_by_exact_name | Maintenance must target one exact category and the intended effective-dated slice | Supply the exact category name and, if necessary, legislation and the historical correction date | ResolvedAbsenceCategoryId and selected slice identity |
| category_status | Category status lookup | Yes | Every create request | Lookup | Supplied Status code or meaning | resolve_absence_category_status | Fusion stores the ANC_SETUP_OBJ_STATUS LookupCode rather than the display meaning | Supply one status code or meaning | Status: LookupCode |
| legislation | Territory lookup | Conditional | Legislation is supplied or an associated type is included | Lookup | Supplied territory code or display name | resolve_absence_category_legislation | Fusion stores TerritoryCode and the associated type must match the selected legislation | Supply one territory code or display name | LegislationCode: TerritoryCode |
| associated_absence_type | Existing absence type | Conditional | An absenceCategoryTypes item is included | Lookup | Supplied AbsenceTypeId or exact Name plus resolved LegislationCode and resolved absenceCategoryTypes.EffectiveStartDate | resolve_associated_absence_type | The association requires an existing type effective on the association date and matching legislation | Supply one existing type ID or exact name and a legislation | absenceCategoryTypes.AbsenceTypeId: AbsenceTypeId |
| flexfield_metadata | Current absenceCategories describe | Conditional | General or legislative flexfield data is supplied | Verify | Live target-environment metadata | refresh_absence_categories_describe | Flex contexts and segment names are deployment-specific | Refresh describe before accepting any flexfield context or segment | Current flexfield contract |
| flexfield_identity | Existing DDF or DFF row | Conditional | A correction or update includes AbsenceCategoriesDDFFlex or AbsenceCategoriesFlex | Lookup | Supplied BO registration and live target-environment child/template evidence | resolve_absence_category_flex_dataloader_contract | The category ID and effective range identify the registered child record | Resolve the existing row and preserve all date-key fields before preparing its change | AbsenceCategoryId, existing child start/end dates, context and current requested values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required code, type identity, date alignment, and metadata are resolved exactly once | No further lookup; no dependency creation |
| Lookup | A documented status, territory, type, or describe resolver can determine the required value | Read-only lookup only |
| Blocked | A required value is missing, ambiguous, mismatched, ineffective, or unsupported by current metadata | No; stop and request correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AC.CHECK_DEPENDENCIES | decision | 100 | resolve_dependency | ready->AC.ENFORCE_DESIGN;blocked->AC.HANDLE_ISSUE | AC.RESOLVE_FLEX_ROW | stop | After all applicable live lookups, date-effective template checks, and metadata checks |
