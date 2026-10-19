# Manage Resource Lookups Input Validation

## Source Basis

- [Overview of Lookups](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html#Using-Lookups-in-Applications)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Lookup request identity | Lookup type and requested operation | Block validation | Provide the exact lookup type and whether the request is to view or change it | Every request |  |
| Lookup-code change | Lookup code and translated meaning | Block validation | Provide both values before planning a code change | Creating or changing a lookup code |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Lookup code contains spaces | Block the request and request an underscore-separated code | Creating or changing a lookup code |  |
| Lookup type and operation are present | Continue to dependency validation | Every request |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRL.VALIDATE_INPUT | step | 1 | validate_input | valid->MRL.RESOLVE_ACCESS;missing_or_invalid->MRL.RETURN_ISSUES | none | stop | Every request |
