# Manage Instructors Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | HCM person | Resolve exactly one accessible person and retrieve assignment details |
| 2 | Existing instructor | Confirm the person is not already represented by an instructor resource |
| 3 | Standalone scope | Supplier/child inputs must be removed or deferred explicitly |
| 4 | Tenant configuration | Resolve required flexfields and accessible immutable Set when enabled |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| IN.PERSON | Accessible HCM person | Yes | Every row | Lookup or Blocked | User-provided person identifier | resolve_instructor_person | An instructor must link to an existing person | Supply or select one exact person | PersonId and verified identity/assignment fields |
| IN.DUPLICATE | Existing instructor check | Yes | Person resolves | Lookup or Blocked | Resolved PersonId | inspect_existing_instructor | Prevents a second instructor resource for one person | Use the existing instructor or change the person | Existing instructor ID/number/status |
| IN.CONFIG | Root-only Set scope and flexfields | Yes | Before every create | Lookup or Blocked | Recorded explicit user Set deferral and current live metadata | validate_required_instructor_configuration | Scope deferral is not a disabled tenant setting; required custom values remain enforced | Only the optional-global/no-context-default contract is implemented; required or supplied custom inputs block pending mapping | configuration_validated result bound to current target and scope |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Person is unique, no instructor exists, and applicable references validate | Yes |
| Selection required | Person or supplier is ambiguous | Lookup yes; create no |
| Blocked | Person is invalid/inaccessible, duplicate exists, or required tenant value fails | Lookup yes; create no |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IN.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->IN.ENFORCE_DESIGN;selection_required->IN.BLOCKED;duplicate->IN.BLOCKED;blocked->IN.BLOCKED;failure->IN.FAILED | IN.RESOLVE_REFERENCES | stop | After applicable reference lookups complete |
