# Manage Person Types Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Person Types.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, delete, or document-specified mutation batch | Block | Provide one supported operation or an ordered mutation batch | Every request |  |
| Read scope | Exact SystemPersonType or UserPersonType, or explicit bounded contains search for one name kind | Block | Provide the name kind and search value | get | find_manage_person_types |
| Existing person-type selector | Exact SystemPersonType and UserPersonType pair | Block | Provide the complete paired business key | edit or delete | find_manage_person_types |
| Create identity | Enabled SystemPersonType and supported UserPersonType | Block | Provide both business-key values | create | find_manage_person_types |
| Edit changes | Exact current pair and at least one supported User Person Type change | Block | Provide the target and intended change | edit | find_manage_person_types |
| Delete target | One exact User Person Type under its System Person Type | Block | Provide the complete pair; do not target a fixed System Person Type | delete | find_manage_person_types |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing paired business key does not resolve exactly once after bounded paging | Missing | Correct SystemPersonType or UserPersonType | find_manage_person_types |
| A create SystemPersonType and UserPersonType pair already exists | Invalid | Stop the duplicate create | find_manage_person_types |
| SystemPersonType is missing, disabled, or ambiguous | Invalid | Correct the System Person Type | resolve_system_person_type |
| Active does not resolve to one enabled current stored value | Invalid | Correct the Active value | resolve_person_type_active |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Effective range | Reject an end date earlier than its start date | Both dates are supplied |  |
| Duplicate key | Evaluate SystemPersonType and UserPersonType together; allow the same user name under a different system type | create | find_manage_person_types |
| Read cardinality | Evaluate every required bounded page before deciding exact-match cardinality | An exact target is required | find_manage_person_types |
| Active stored value | Write only the resolved stored code to ActiveFlag | Active is supplied | resolve_person_type_active |
| Fixed system type | Reject redefining or deleting a fixed System Person Type | A mutation targets the system type | find_manage_person_types |
| Supported shape | Reject unsupported fields or source shapes; never silently omit or invent a value | A mutation source is prepared |  |
| Batch resolution | Reject a batch row that requires an ID, generated value, or state from an earlier row unless the current loader contract supplies an already-resolved stable key | Document-specified mutation batch |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.VALIDATE | decision | 1 | validate_input | valid->PT.DEPENDENCY;missing->PT.ERROR;invalid->PT.ERROR;unsupported->PT.ERROR | none | stop | Every Manage Person Types request |
