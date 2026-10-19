# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Relationship type to edit | Relationship Type | Stop before search | Provide the exact relationship type name; the Oracle example uses Employment | Editing a relationship type | |
| Role and phrase pair | Subject Type, Subject Phrase, Subject Role Singular, Subject Role Plural, Object Type, Object Phrase, Object Role Singular, Object Role Plural | Stop before adding the role and phrase pair | Provide all eight values for the pair; the Oracle example documents Organization / Has contract employees / Contractor / Contractors and Person / Contract Employee of / Contract Employee / Contract Employees | Adding a role and phrase pair | |
| Relationship group | Group Name | Stop before assigning the relationship type to a group | Provide the group name; the Oracle example selects Party Contacts | Assigning the relationship type to a group | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Documented action scope | Validate only the Oracle-documented edit flow: search, edit, add one role and phrase pair, assign a group, then save and close | The supplied source is the Oracle Edit Relationship Types guide | |

## FSM Import Contract

Before an import preview, require one unchanged ZIP with a valid ZIP signature,
exactly one `ASM_SETUP_CSV_METADATA.xml` member, and exactly one
`ObjectShortName` value of `HZ_MANAGE_RELATIONSHIP_TYPES`. Bind the absolute ZIP
path, SHA-256, target environment, `executionRoute=data-loader`, and the
task-local native FSM adapter to the approval envelope.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRT.VALIDATE-DOCUMENTED-INPUT | step | 10 | validate_input | valid->MRT.FIND-RELATIONSHIP-TYPE;invalid->MRT.HANDLE-MISSING-INPUT | none | stop | Editing a relationship type using the documented Oracle guide |
