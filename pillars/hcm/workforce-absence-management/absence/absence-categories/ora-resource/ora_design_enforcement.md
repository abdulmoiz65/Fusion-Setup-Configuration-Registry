# Absence Categories Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate task inputs | Require Name, Status, and every conditionally required association value; validate any supplied parent or child effective start date |
| 2 | Resolve non-create target | Resolve one category in the selected effective-date context; historical correction uses its resolved ID and selected prior slice |
| 3 | Apply effective-date defaults and server-owned omission rules | Use the system date for an omitted parent EffectiveStartDate only after explicit consultant confirmation, default an omitted association EffectiveStartDate from the resolved parent date, never default Language, and omit generated create values, meanings and audit fields; retain registered maintenance IDs and observed flex date-key values |
| 4 | Resolve authoritative codes | Resolve Status through commonLookupsLOV and LegislationCode through territoriesLOV using the exact approved endpoints |
| 5 | Validate associated types | Require one existing type effective on the resolved association start date and matching the selected legislation |
| 6 | Normalize date-effective operation | Derive effectiveOf from the selected operation and applicable explicit date; never accept a caller-authored range string |
| 7 | Refresh registered DAT template | Verify effectiveOf on the parent and every included child/DFF section |
| 8 | Validate flexfields | Refresh describe, resolve the existing child through resolve_absence_category_flex_dataloader_contract, and validate the complete registered identity and date range |
| 9 | Hand off validated data | Stop at a validated core.data-loader REST handoff using BusinessObject absenceCategories; do not perform a direct REST mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Parent-category end-date request | Blocker | | The prepared load includes association or flex child data rows, changes an actual absence type, or requires a separate child-maintenance load as a prerequisite | Prepare only the parent absenceCategories payload and leave association handling to HDL internal logic, whether associations exist or not. Preserve the requested parent end date. Inspect history for impact only; do not synthesize child end dates or statuses. Separate explicitly requested association maintenance retains its existing workflow. | Yes |
| Every create request | Blocker | resolve_absence_category_status | Status does not resolve to exactly one ANC_SETUP_OBJ_STATUS row | Supply one supported code or meaning and retain LookupCode | Yes |
| Legislation is supplied or an associated type is included | Blocker | resolve_absence_category_legislation | Legislation does not resolve to exactly one enabled, non-obsolete territory | Supply a unique territory code or display name and retain TerritoryCode | Yes |
| An associated type is included | Blocker | resolve_associated_absence_type | The type is missing, ambiguous, legislation-mismatched, or not effective on the resolved absenceCategoryTypes.EffectiveStartDate | Supply one matching existing AbsenceTypeId or exact type name | Yes |
| General or legislative flexfield data is supplied | Blocker | refresh_absence_categories_describe | Current target-environment describe metadata is unavailable or does not contain the supplied context or segment | Refresh describe and use only current contexts and segments | Yes |
| A correction or update sets an AbsenceCategoriesDDFFlex or AbsenceCategoriesFlex value | Blocker | resolve_absence_category_flex_dataloader_contract | The selected child, requested context, or effective range is missing, ambiguous or mismatched | Resolve the specific missing evidence and continue through Data Loader preparation when ready. Both flex sections are registered for maintenance using AbsenceCategoryId; absence of a distinct child ID is not a reason to prohibit correction or update. | Yes |
| A requested segment is blank on an existing DDF or DFF row | Warning | resolve_absence_category_flex_dataloader_contract | Blank segment content is incorrectly treated as absence of the child record | Prepare PATCH on the resolved child. The first nonblank value does not require child POST. | Yes |
| Every create request | Blocker |  | Language is populated or defaulted by the client | Omit Language and allow Fusion to derive it from the authenticated login context | Yes |
| EffectiveEndDate is omitted by the user | Blocker |  | A client-side EffectiveEndDate default is added or a required resolved flex end date is discarded | Omit ordinary parent defaults. Preserve the existing child end date required by DDF/DFF maintenance; this is retained identity, not a new default or end-date operation. | Yes |
| A date-effective operation is requested | Blocker | normalize_absence_category_effective_of | effectiveOf is caller-authored, does not match the selected operation, or a non-create date/range is defaulted | Derive the exact mapping from ora_defaulting_rules.md; require explicit dates and scope for non-create operations | Yes |
| A create omits Category Effective Start Date | Blocker |  | The system date was applied without explicit consultant confirmation | Display the system date and require confirmation, or collect a supplied date | Yes |
| A create defaults Status to Pending | Blocker | resolve_absence_category_status | Pending is unsupported by current lookup metadata or has not been explicitly confirmed | Require an explicit supported status decision | Yes |
| An association is requested | Blocker | resolve_associated_absence_type | The selected type is inaccessible, inactive, ended, legislation-incompatible, not effective on the association date, duplicated, or has unresolved governing configuration | Resolve the type and category history, correct the date or selection, and retain the evidence before Data Loader preparation | Yes |
| A non-create operation is requested | Blocker | find_absence_category_by_exact_name | The source has no selected effective-dated identity or the identity is ambiguous | Resolve exactly one category and the intended dated slice before DAT preparation | Yes |
| A category taxonomy is proposed | Blocker |  | Policy scope, leave inventory, jurisdiction, reporting purpose, separation rules, or effective date is missing or ambiguous | Record the unresolved decision and do not infer statutory, pay, eligibility, or reporting rules | Yes |
| A proposed group combines types with different statutory reporting by legislation | Warning |  | The supplied policy confirms distinct statutory reporting but the category would obscure it | Recommend legislation-specific categories and retain the reporting rationale | Yes |
| A proposed broad group combines distinct statutory, pay, eligibility, or compliance outcomes | Warning |  | The supplied policy requires those outcomes to remain separately auditable | Warn and propose separate categories or an explicitly governed reporting rollup | Yes |
| A category is proposed to solve eligibility, entitlement, accrual, pay, approval, or plan-balance requirements | Blocker |  | The requested outcome belongs to another Absence setup object | Route the requirement to Absence Plans, Absence Types, eligibility, payroll, or workflow configuration | Yes |
| A date-effective DAT section is included | Blocker | refresh_absence_categories_dataloader_template | An included parent or child/DFF section lacks effectiveOf, an included row differs from its derived row-operation value, or the final immutable DAT is not inspected | Refresh the registered UCM DAT template, apply ora_defaulting_rules.md per row, and inspect the final immutable DAT member. Do not require an unneeded parent row for flex-only correction or an association-only addition. | Yes |
| A Task Hook preview is built for a date-effective archive | Blocker | normalize_absence_category_effective_of | The preview relies on caller-authored `ruleResults` without inspecting the final immutable DAT member | Derive and verify `effectiveOf` from the exact archive before preview; do not accept a declared pass as evidence | No |
| DELETE is requested | Blocker | normalize_absence_category_effective_of | DELETE_CHANGES versus ZAP is not explicit, or ZAP lacks explicit destructive intent | Require the selected deletion scope; require the normal immutable Data Loader approval for ZAP | Yes |
| A write-oriented source contains generated, audit, or meaning fields | Blocker |  | The source invents generated create identifiers or includes audit fields, display meanings, or display flex contexts as writable values | Remove those fields; retain resolved registered surrogate IDs and date-key fields for maintenance | Yes |
| An item or child record is addressed | Blocker |  | A caller constructs an opaque item key instead of following a returned self or canonical link | Retrieve the target row and follow its returned link | Yes |
| Any mutation is requested | Blocker |  | The operation attempts a direct REST POST, PATCH, DELETE, or upsert or bypasses core.data-loader | Route the exact operation through core.data-loader in REST mode using BusinessObject absenceCategories and its preview and approval gates | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_absence_category_by_exact_name | Every non-create request | ResolvedAbsenceCategoryId and one selected effective-dated identity | ora_reference_lookups.md |
| normalize_absence_category_effective_of | Every date-effective request | Derived effectiveOf for each selected row operation and its explicit required input | ora_reference_lookups.md |
| resolve_absence_category_status | Every create request and every associated-type row | ANC_SETUP_OBJ_STATUS LookupCode for each supplied Status | ora_reference_lookups.md |
| resolve_absence_category_legislation | Legislation is supplied or an associated type is included | TerritoryCode | ora_reference_lookups.md |
| resolve_associated_absence_type | Every association request | One available type with matching LegislationCode, effective range, and association date compatibility | ora_reference_lookups.md |
| refresh_absence_categories_describe | Flexfield data is supplied, the environment changed, or captured metadata may be stale | Current parent, child, context, segment, and link contract | ora_reference_lookups.md |
| refresh_absence_categories_dataloader_template | Every date-effective DAT preparation | Current UCM template sections and effectiveOf support | ora_reference_lookups.md |
| resolve_absence_category_flex_dataloader_contract | Every DDF or DFF correction or update | Exact child section, registered category ID, existing effective range, requested operation/date and current segment values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AC.ENFORCE_DESIGN | decision | 110 | design_enforcement | eligible->AC.READINESS_GATE;blocked->AC.HANDLE_ISSUE | AC.CHECK_DEPENDENCIES | stop | After validation, omission rules, lookup resolution, date-effective normalization, template refresh, dependency checks, and metadata refresh |
