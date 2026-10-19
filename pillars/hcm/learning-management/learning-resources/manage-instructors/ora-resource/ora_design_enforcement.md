# Manage Instructors Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve person intent | Use only a user-provided person identifier and verified HCM identity |
| 2 | Prevent duplicate | Exclude a person who already has an instructor resource |
| 3 | Evaluate assignment | Only ACTIVE enabled; block unresolved inactive/terminated/suspended behavior |
| 4 | Build proposal | Show verified identity, assignment status, warnings, blockers, and exact action |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every instructor row | Blocker | resolve_instructor_person | Person was inferred, is blank, or does not resolve uniquely | Require a supported user-provided identifier | Yes |
| Person resolves | Blocker | inspect_existing_instructor | Existing instructor is found | Use the existing instructor or select another person | No |
| Supplier, materials or virtual account supplied | Blocker |  | Outside standalone scope | Ask to remove or defer explicitly | Yes |
| Assignment is not ACTIVE | Blocker | resolve_instructor_person | FDD/UI contract conflict is unresolved | Report unsupported input; acceptance of a warning does not resolve the contract | No |
| Rows alias the same person | Blocker | resolve_instructor_person | Multiple rows have one verified PersonId | Revise proposal to one row for that person | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_instructor_person | Every row | Verified person and assignment fields | ora_reference_lookups.md |
| inspect_existing_instructor | After person resolution | Existing instructor identity/status | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IN.ENFORCE_DESIGN | decision | 4 | design_enforcement | passed->IN.APPROVAL_GATE;blocked->IN.BLOCKED;failure->IN.FAILED | IN.CHECK_DEPENDENCIES | stop | Before displaying the versioned proposal |
