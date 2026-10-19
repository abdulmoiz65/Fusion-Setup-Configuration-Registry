# Assign Security Profiles to Role Defaulting Rules

Source: HCMDS Assign Security Profiles to Role Skill, version 5.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Delegation Allowed | False | Creating a new data role and Delegation Allowed is not specified | No | resolve_delegation_allowed_yes_no |
| Role Name | Derive a display name from the inherited job role and at least one security-scope descriptor; keep the display name below 100 characters | Creating a new data role and Role Name is not specified | No; retain a user-supplied Role Name | derive_available_data_role_name_and_code |
| Role Code | Derive normalized uppercase underscore tokens with the existing `_DATA` convention from the inherited job role and at least one security-scope descriptor | Creating a new data role | Yes; ignore every user-supplied data-role Role Code | derive_available_data_role_name_and_code |

The security-scope descriptor may be an audience, a hierarchy type or level, or
another configuration qualifier that distinguishes the data role. Do not derive
an identity when no meaningful descriptor is available. Do not append numeric
or timestamp suffixes: a derived display name and internally derived role code
must each be unique and available before preview or import.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ASPR.APPLY_DEFAULTS | decision | 2 | apply_default | defaults_applied->ASPR.LOOKUP_MAPPINGS;blocked->ASPR.ERROR | ASPR.VALIDATE | stop | A new data role is being created or updated and defaultable values have been evaluated |
