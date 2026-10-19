# Manage Instructors Input Validation

## Source Basis

- OLC-116674 FDD, latest approved version; Jira OLC-120237 is traceability only.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Instructor person | User-provided full name, person number, digit-string person ID, or partial-name search with explicit selection | Block the row before proposal | Ask for one supported identifier; email remains unverified and must not be guessed | Every row | resolve_instructor_person |
| Tenant-required configuration | Required flexfields and accessible Set when enabled | Block creation | Request only the configured missing values | Tenant configuration makes the value mandatory | validate_required_instructor_configuration |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Person is supplied | Require one accessible HCM person and show assignment-derived identity details | Continue or request a precise selection/correction | resolve_instructor_person |
| Person resolves | Detect an existing instructor for the same person | Exclude duplicates and show existing identifier/status | inspect_existing_instructor |
| Supplier is supplied | Outside approved standalone scope | Ask to remove or defer it; never silently omit |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Person provenance | Reject a person derived from job, department, location, supplier, manager, similarity, or another row | Every row |  |
| Person match | Require exactly one accessible HCM person | Person identifier is supplied | resolve_instructor_person |
| Related materials and virtual accounts | Unavailable in standalone increment; ask to defer rather than silently discard | Child data is supplied |  |
| Request shape | Require operation=create and 1 to 20 rows with unique row_id, person kind/value and user_supplied provenance; identifiers are strings | Local intake; bound is an implementation choice, not Fusion limit |  |
| Partial name | Require version-bound explicit label selection even for a single candidate and fresh exact identity resolution | Partial-name discovery supplied | resolve_instructor_person |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IN.VALIDATE_INPUT | step | 1 | validate_input | valid->IN.RESOLVE_REFERENCES;invalid->IN.BLOCKED;failure->IN.FAILED | none | stop | Before preparing an instructor proposal |
