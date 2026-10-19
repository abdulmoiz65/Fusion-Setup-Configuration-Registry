# Input Validation

## CSV Column Intent Resolution

| CSV Column | User Intent |
|---|---|
| PJF_PROJECT_ROLE.csv.ProjectRoleName | Project Role Name |
| PJF_PROJECT_ROLE.csv.Description | Description |
| PJF_PROJECT_ROLE.csv.EndDateActive | To Date; ToDate alias; optional end date |
| PJF_PROJECT_ROLE.csv.StartDateActive | From Date; FromDate alias; required start date on create |
| PJF_PROJECT_ROLE.csv.RoleName | Enterprise Role (Name) |
| PJF_PROJECT_ROLE.csv.RoleCommonName | Enterprise Role (Code) |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.PJF_PROJECT_ROLE.ProjectRoleName | Parent Project Role Name from PJF_PROJECT_ROLE.csv or an existing target role |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.Keyword | Explicit free-text keyword; never copied from a selected content item's name |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.Name | Canonical selected predefined requirement name; not required for keyword-only rows |
| Requirements (UI input) | Enter a display name such as Hindi; search the predefined requirement LOV and derive canonical Name, ContentItemId, Type and any required SectionName. A URL or manually supplied item ID is not required from the user |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.RatingShortDescr1 | Rating Level |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.RatingShortDescr2 | Reading Rating Level |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.RatingShortDescr3 | Speaking Rating Level |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.RatingShortDescr4 | Writing Rating Level |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.SectionName | Target qualification section display name from resolve_project_qualification_context; not inferred from ContentTypeName |
| PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.MandatoryFlag | Mandatory qualification Yes or No; write canonical Y or N to CSV |
| PJF_PROJECT_ROLE_TRANSLATION.csv.PJF_PROJECT_ROLE.ProjectRoleName | Parent Project Role Name |
| PJF_PROJECT_ROLE_TRANSLATION.csv.Description | Translated project role description |
| PJF_PROJECT_ROLE_TRANSLATION.csv.Language | Translation language |
| PJF_PROJECT_ROLE_TRANSLATION.csv.ProjectRoleName | Translated Project Role Name |
| PJF_PROJECT_ROLE_TRANSLATION.csv.SourceLang | Translation source language |

**Flexfields**

DFF segment slots are grouped by CSV and data type using inclusive ranges. Individually resolved fields remain in the mapping table and are excluded from these ranges.

- **PJF_PROJECT_ROLE.csv**: AttributeCategory, Attribute1-Attribute15.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create, update, validate, export, import, end_date | Block | Ask for supported intent; delete unproven | Every request |  |
| Scope/identity | ProjectRoleName, optional stable RoleCode | Block | Supply exact role identity | Every write | find_project_role |
| Dates | StartDateActive or FromDate; optional EndDateActive or ToDate | Block create | Normalize aliases; preserve omitted update values; reject conflicting aliases | Create/update |  |
| Enterprise Role | RoleCommonName (preferred) and/or RoleName | Preserve omitted | Use the named resolver's canonical result | Association change | resolve_active_enterprise_role |
| Qualifications/translations | Requirements display name or explicit Keyword, mandatory Yes/No, optional proficiency levels; preserve omission | Preserve omitted | Normalize the dialog fields to an explicit child diff; resolve selected item and section where applicable | Child change | resolve_role_children |
| Target/artifacts | TargetEnvironment, current_export, package_template, use_state | Block | Obtain current target evidence | Every write | verify_project_role_package |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Custom role and unique identity | Satisfied | Create/update/end-date | find_project_role |
| Seeded state supplied by role lookup | Evaluate in design gate | Apply protection policy | find_project_role |
| Enterprise Role supplied | Conditional | Resolve one active job or abstract role | resolve_active_enterprise_role |
| Qualifications supplied | Conditional | Require Project Management implementation and valid rows | resolve_role_children |
| End-date/association/removal | Conditional | Require active-use/access evidence | resolve_role_use |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Nonblank unique ProjectRoleName | Accept; else reject | Create/update | find_project_role |
| Dates are parseable and normalized StartDateActive <= nonblank EndDateActive | Reject invalid or conflicting aliases; compare the merged update range, including preserved baseline values. Blank create end date is open-ended; explicit blank update end date is a change | Dates supplied | find_project_role |
| Enterprise Role input has a name or code and the resolver supplies a canonical identity | Accept the resolver output; lookup eligibility belongs to its reference contract | Association supplied | resolve_active_enterprise_role |
| Qualification parent PJF_PROJECT_ROLE.ProjectRoleName matches exactly one PJF_PROJECT_ROLE.csv.ProjectRoleName row or exactly one existing role in the current target baseline | Accept a new or existing custom parent role; else reject. For maximum compatibility, carry an unchanged existing parent row in PJF_PROJECT_ROLE.csv until qualification-only CSV-to-XML wrapper generation is verified | Qualifications supplied | find_project_role |
| Exactly one requirement form is explicit: predefined Requirements display name/Name/ContentItemId or free-text Keyword | Reject empty or mixed forms. Keyword-only rows do not require Name, content-item or rating lookups; their exact target CSV representation must still pass the package gate | Qualifications supplied | resolve_role_children |
| Predefined Requirements display name resolves to a canonical Name and ContentItemId | Search the supported target types, select one exact active candidate, or ask the user to choose among actual matches; do not manufacture identities from wording | Predefined qualification supplied | resolve_active_qualification_requirement |
| SectionName and LOV mode are supplied by the target context resolver | Reuse a uniquely matched item/type/section from any role in the fresh task export; for an unseen section require target selection evidence. Accept a blank section only when the target proves sectionless mode and package shape; never default from content type | Qualifications supplied | resolve_project_qualification_context |
| Supplied rating fields have canonical resolver outputs | Populate RatingShortDescr1 through RatingShortDescr4 in their original columns; reject ratings on keyword-only rows | Ratings supplied | resolve_active_qualification_rating |
| Qualification identity/keyword/section is duplicate-free and MandatoryFlag is explicit | Resolve user intent Yes to Y and No to N, write exactly uppercase Y or N to PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv.MandatoryFlag, and reject any other CSV value | Qualifications supplied | resolve_role_children |
| Exact package members/headers | Accept; else reject | Import | verify_project_role_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.VALIDATE_INPUT | step | 1 | validate_input | valid->PROLE.APPLY_DEFAULTS;invalid->PROLE.RETURN_ISSUES | none | stop | Every Manage Project Roles request |
| PROLE.ROUTE_OPERATION | decision | 5 | evaluate_result | supported->PROLE.RESOLVE_DEPENDENCIES;unsupported->PROLE.RETURN_REFUSAL;invalid->PROLE.RETURN_ISSUES | PROLE.RESOLVE_CHILDREN | stop | After role/reference/child resolution |

## Input and CSV Source Evidence

Source evidence reviewed 2026-10-10 for PJF_MANAGE_PROJECT_ROLES. These
provenance notes explain the existing validation contract; they do not establish
a newly verified target template or authorize execution.

### UI and CSV Provenance

The supplied images establish main-table labels and the qualification dialog's
Requirements, Type, Mandatory Requirement, Proficiency Level and language
Reading/Speaking/Writing labels. ADE view bindings confirm that selecting a
Requirements row derives the content item, type and, in section-aware mode,
section. The screenshots do not prove an item's target ID, section or current
feature mode. No environment-specific role rows or screenshot copy are retained.

CSV member and column mappings were inherited from the target's pre-existing
`ora_input_validation.md`. Original populated-export artifacts and a blank
template were not available for reproduction. Therefore these mappings remain
a working contract guarded by `verify_project_role_package`; they are not
represented as a newly verified target export. Runtime evidence must come from
the shared task exporter and loader preflight, with exact target/task, sanitized
header metadata, conditional member/wrapper checks and an internal immutable
artifact fingerprint. Do not infer blank-template or removal semantics from
the synthetic scenarios.

### Indexed Setup-Object Evidence

Series: `FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64`. Paths below are relative to its
`fusionapps/` root, not files in this FSCR checkout. Evidence is returned indexed
line snippets; development-series behavior must be reconciled with the target.

| Source | Returned indexed evidence | Use and limit |
|---|---|---|
| prj/pjf/db/data/PjfCommon/SetupTaskBusinessObjectSD.xml | Lines 3978-3979 register the project-role qualification child for Manage Project Roles | Confirms registered child/task association, not writable public REST or target ZIP serialization |
| prj/pjf/db/data/PjfCommon/SetupBOReferenceAttributeSD.xml | Lines 4160-4186 reference qualification CONTENT_ITEM, KEYWORD, NAME and PROJECT_ROLE; lines 3203-3208 reference role Name | Supports reference identities; does not independently prove every CSV header |
