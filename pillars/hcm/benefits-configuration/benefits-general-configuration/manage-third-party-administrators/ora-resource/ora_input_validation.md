# Manage Third-Party Administrators Input Validation

| Requirement | Applies when | Blocking result |
|---|---|---|
| Operation | Every request | Require sample, create, update, or inactivate. |
| Environment and task context | Validation or load | Require selected environment and matching active Run Book before mutation. |
| Organization name | Create | Require a nonblank, current-metadata-valid value. |
| Identity | Update or inactivate | Require exactly one existing organization; never choose the first name match. |
| Effective date | Date-effective operation | Require one valid date and applicable effective row. |
| Location | Create or update when required | Require both explicit codes or both task location names; reject mixed or partial pairs. |

Reject blank or whitespace-only required values, unsupported attributes, DAT
delimiters or line breaks, values beyond current metadata lengths, invalid
dates, and update requests with no supported change. `ClassificationCode` and
`ClassificationName` are not inputs; reject overrides. Validate section names,
metadata order, row width, delimiters, and operation keys with `core.data-loader`.
Return `valid`, `missing`, `invalid`, `ambiguous`, or `unsupported`; anything
other than `valid` blocks preview.
