# Manage Organization Trees Reference Lookups

## Purpose

Defines the exact Organization member and existing-version lookups required before common Trees planning.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_organization_members_by_name | A requested hierarchy supplies one or more organization names | Each distinct trimmed organization name | /hcmRestApi/resources/latest/organizationsLov | OrganizationId, Name | Read through core.fusion-api.apps-common.trees and retain exactly one current exact Name match for each supplied name | OrganizationName to OrganizationId; preserve the requested parent relationship as ParentOrganizationId | Stop the request; do not select a first row or replace a name with a similar match |
| resolve_organization_tree_version_by_identity | An existing Organization Tree version is read or updated | TreeCode plus TreeVersionName or TreeVersionId | /fscmRestApi/resources/11.13.18.05/fndTreeVersions with the common Trees version finder | TreeVersionId, TreeVersionName, TreeCode, TreeStructureCode, Status, EffectiveStartDate, EffectiveEndDate | Retain exactly one matching version for `PER_ORG_TREE_STRUCTURE`; it must be Draft for an update | Exact version identity and current values to preserve | Stop before planning when the version is missing, ambiguous, not Draft, or belongs to another tree structure |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Organization names resolve uniquely | Return one ID-based hierarchy preserving root and child relationships to the common Trees skill |
| Any name is unresolved or ambiguous | Return the affected names and stop before planning or mutation |
| A node is created or changed | The common Trees skill owns node-operation validation and read-back; do not invoke a task-local tree-node route |
| An existing version is changed | Resolve its current values before defaulting; never use `4712-12-31` as an update default |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORGTREE.RESOLVE_MEMBERS | decision | 3 | reference_lookup | resolved->ORGTREE.DEFAULTS;not_required->ORGTREE.DEFAULTS;missing->ORGTREE.ERROR;ambiguous->ORGTREE.ERROR | ORGTREE.CORE_READY | stop | Every request; resolve named members when supplied |
