# Manage Beneficiary Organizations Input Validation

## Required inputs

| Requirement | Applies when | Required action if missing or invalid |
|---|---|---|
| Operation | Every request | Require a supported operation: sample, create, update, or inactivate. |
| Target environment and task context | Every request that validates or loads | Require a selected environment and active matching Run Book before a mutation. |
| Organization name | Create | Require a nonblank name accepted by current `Organization` metadata. |
| Existing organization identity | Update or inactivate | Require exactly one resolved organization; do not select the first name match. |
| Effective-date intent | Create, update, or inactivate when metadata requires it | Require one valid date and resolve the applicable date-effective row. |
| Changed values | Update or inactivate | Require at least one supported requested change. |
| Classification association | Create and update when metadata requires it | Require an `OrgUnitClassification` row and exactly one successful `HR_BEN` LOV result with a nonblank classification name. |
| Location input | Create or update when location is supplied or required | Require both `LocationCode` and `LocationSetCode`, or both Task Location Name and Location Set Name; reject a mixed or partial pair. |

## Field checks

- Reject blank or whitespace-only required values, invalid dates, unsupported
  attributes, DAT delimiters or line breaks in scalar values, and values that
  exceed the current metadata length.
- Validate every row, exact section name, metadata order, delimiter count, and
  operation-specific key using `core.data-loader`.
- Reject `OrgInformation` sections in a source or generated DAT archive.
- `ClassificationCode` and `ClassificationName` are not user inputs. Reject an
  attempted override; derive the name through the LOV lookup and leave the DAT
  `ClassificationCode` attribute blank.
- Preserve a supplied `OrgUnitClassification.Status` only when current metadata
  accepts it; otherwise stop rather than coercing it.
- An explicit complete `LocationCode`/`LocationSetCode` pair bypasses the
  location LOV and is mapped unchanged. For names, require one exact,
  effective-dated `locationsLov` result before source construction.
- Return `valid`, `missing`, `invalid`, `ambiguous`, or `unsupported`, with a
  field-level recommended action. Any result other than `valid` blocks preview.
