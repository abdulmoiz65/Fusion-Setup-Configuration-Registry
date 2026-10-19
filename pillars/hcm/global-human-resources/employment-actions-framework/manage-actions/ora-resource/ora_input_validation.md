# Action Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Actions.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, copy, edit, or delete | Block | Provide one supported operation | Every request |  |
| Read scope | Optional Action Code, exact action name, or explicit bounded list request | Return the bounded collection when no exact selector is requested | Provide an exact selector when one record is required | get | find_manage_actions |
| Create identity | Unique Action Code, Action Type, name, and effective dates | Block | Provide all mandatory create values | create |  |
| Existing action selector | Exact Action Code, action name, or association identity | Block | Provide one exact selector | copy, edit, or delete | find_manage_actions |
| Copy definition | New unique Action Code, exact source Action, and explicit association allow-list | Block | Provide the new code, source, and associations to copy | copy | find_manage_actions |
| Edit changes | At least one explicit Data Loader-supported change | Block | Provide the intended change | edit |  |
| Delete operation | Registered-object-supported delete for one exact target | Block | Provide the exact target and supported delete scope | delete | find_manage_actions |
| Association values | Exact parent Action and association, matching Action Type, and supplied Country, Action Reason, assignment status, or role | Block | Provide every value required by the requested association | An association is requested | resolve_action_common_lookup |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing Action, copy source, or association does not resolve exactly once | Missing | Provide one exact selector | find_manage_actions |
| A create or copy Action Code matches an existing Action | Invalid | Stop the duplicate create or copy | find_manage_actions |
| A supplied configured value is missing, disabled, ineffective, ambiguous, or incompatible | Invalid | Correct the configured value | resolve_action_common_lookup |
| A supplied Country does not resolve to one canonical code | Invalid | Correct the Country | resolve_action_country |
| A role mapping does not resolve to one active exact role | Invalid | Correct the role | resolve_action_role |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Effective range | Reject an End Date earlier than Start Date | Both dates are supplied |  |
| Association date scope | Allow an effective-date change only on the matching action-reason usage row; reject a global Action Reason change | An association date changes | find_manage_actions |
| Role mapping shape | Require exact parents, matching Action Type, one active role, and a registered row shape and key set | An action-reason role mapping is supplied | resolve_action_role |
| Registered source contract | Reject unsupported fields, grouping keys, cardinalities, source keys, or multi-value encodings | A mutation source is prepared |  |
| Prohibited supplied values | Reject generated IDs, audit fields, links, and partial keys | Any such value is supplied |  |
| Copy workbook scope | Require the parent and only allow-listed ActionReasonUsages rows in the same workbook; omitted children are not copied | copy |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACT.VALIDATE | decision | 1 | validate_input | valid->ACT.DEPENDENCIES;missing->ACT.ERROR;invalid->ACT.ERROR;unsupported->ACT.ERROR | none | stop | Every Manage Actions request |
