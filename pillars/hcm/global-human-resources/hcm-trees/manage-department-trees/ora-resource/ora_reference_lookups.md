# Manage Department Trees Reference Lookups

## Purpose

Defines the exact Department member and existing-version lookups required before common Trees planning.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_department_members_by_name | A requested hierarchy supplies one or more department names | Each distinct trimmed department name | /hcmRestApi/resources/latest/departmentsLov | DepartmentId, Name | Read through core.fusion-api.apps-common.trees and retain exactly one current exact Name match for each supplied name | DepartmentName to DepartmentId; preserve the requested parent relationship as ParentDepartmentId | Stop the request; do not select a first row or replace a name with a similar match |
| resolve_department_tree_version_by_identity | An existing Department Tree version is read or updated | TreeCode plus TreeVersionName or TreeVersionId | /fscmRestApi/resources/11.13.18.05/fndTreeVersions with the common Trees version finder | TreeVersionId, TreeVersionName, TreeCode, TreeStructureCode, Status, EffectiveStartDate, EffectiveEndDate | Retain exactly one matching version for `PER_DEPT_TREE_STRUCTURE`; it must be Draft for an update | Exact version identity and current values to preserve | Stop before planning when the version is missing, ambiguous, not Draft, or belongs to another tree structure |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Department names resolve uniquely | Return one ID-based hierarchy preserving root and child relationships to the common Trees skill |
| Any name is unresolved or ambiguous | Return the affected names and stop before planning or mutation |
| A node is created or changed | The common Trees skill owns node-operation validation and read-back; do not invoke a task-local tree-node route |
| An existing version is changed | Resolve its current values before defaulting; never use `4712-12-31` as an update default |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPTTREE.RESOLVE_MEMBERS | decision | 3 | reference_lookup | resolved->DEPTTREE.DEFAULTS;not_required->DEPTTREE.DEFAULTS;missing->DEPTTREE.ERROR;ambiguous->DEPTTREE.ERROR | DEPTTREE.CORE_READY | stop | Every request; resolve named members when supplied |
