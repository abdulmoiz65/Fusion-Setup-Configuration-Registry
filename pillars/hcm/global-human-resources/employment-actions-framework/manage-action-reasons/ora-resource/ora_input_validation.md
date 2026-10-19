# Action Reason Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Action Reasons.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Read scope | Optional Reason Code, exact action-reason name, or explicit bounded list request | Return the bounded collection when no exact selector is requested | Provide an exact selector when one record is required | get | find_manage_action_reasons |
| Create identity | Unique Reason Code, name, and effective start date | Block | Provide all three values | create |  |
| Existing reason selector | Exact Reason Code, action-reason name, or association identity | Block | Provide one exact selector | edit or delete | find_manage_action_reasons |
| Edit changes | At least one explicit Data Loader-supported change | Block | Provide the intended change | edit |  |
| Delete operation | Registered-object-supported delete for one exact target | Block | Provide the exact target and supported delete scope | delete | find_manage_action_reasons |
| Usage association | Exact Action and Action Reason, plus supplied Country, role, or configured values | Block | Provide every value required by the requested association | An association is requested | resolve_action_reason_action |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing Action Reason or association does not resolve exactly once | Missing | Provide one exact selector | find_manage_action_reasons |
| A create Reason Code matches an existing Action Reason | Invalid | Stop the duplicate create | find_manage_action_reasons |
| A supplied configured value is missing, disabled, ineffective, ambiguous, or incompatible | Invalid | Correct the configured value | resolve_action_reason_common_lookup |
| A supplied Country does not resolve to one canonical code | Invalid | Correct the Country | resolve_action_reason_country |
| A supplied role does not resolve to one active exact role | Invalid | Correct the role | resolve_action_reason_role |
| An association Action does not resolve to one current compatible Action | Invalid | Correct the Action | resolve_action_reason_action |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Date format | Normalize an unambiguous loader date to yyyy/MM/dd; reject an invalid or ambiguous date | A date is supplied |  |
| Effective range | Reject an End Date earlier than Start Date | Both dates are supplied |  |
| Registered source contract | Reject unsupported columns, keys, field types, cardinalities, writable values, or operations | A mutation source is prepared |  |
| Prohibited supplied values | Reject generated IDs, audit fields, links, partial keys, invented associations, and multi-value encodings | Any such value is supplied |  |
| Description support | Block when Description is requested but absent from current ActionReasons metadata; omit it only after explicit approval | Description is requested |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.VALIDATE | decision | 1 | validate_input | valid->AR.DEPENDENCIES;missing->AR.ERROR;invalid->AR.ERROR;unsupported->AR.ERROR | none | stop | Every Manage Action Reasons request |
