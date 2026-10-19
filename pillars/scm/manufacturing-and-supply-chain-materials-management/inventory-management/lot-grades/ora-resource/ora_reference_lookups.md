# Lot Grades Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood inventory-lot-serial setup lot-grades page and dynamic layout | GradeCode, Description, and GradeDisabledCode are text or checkbox fields; no LOV-backed control is defined for this task |
| User decision | Do not add a lookup resolver for Lot Grades |

## Lookup Decision

| Candidate | Decision | Reason |
|---|---|---|
| Lot Grades fields | Not selected | No Redwood LOV field or approved display-value-to-system-value lookup contract exists for this task |

No local or live lookup resolver is defined for this task. Data Loader receives canonical values after the approved Active checkbox normalization.
