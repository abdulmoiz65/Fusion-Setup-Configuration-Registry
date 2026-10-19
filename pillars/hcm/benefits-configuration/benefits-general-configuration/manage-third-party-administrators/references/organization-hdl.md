# Third-Party Administrator Organization HDL

## Scope and business object

`BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR` (Manage Third-Party Administrators)
uses the `Organization` HDL business object. The root file is
`Organization.dat`; retain that exact filename and the live template's metadata
order. This task creates and maintains third-party-administrator master
organizations; do not substitute another HDL object.

Use only the `Organization` root and the operation-required
`OrgUnitClassification` association. Exclude `OrgInformation` and every
Organization Information EFF section from every generated DAT file, even when
present in a live template or source workbook.

## Classification derivation

Do not ask for or accept `ClassificationCode` or `ClassificationName` as task
inputs. Before source construction, use the declared shared REST client for:

`GET /hcmRestApi/resources/latest/organizationClassificationsLOV?q=ClassificationCode='BEN TPA'`

Send `REST-Framework-Version: 9`. Require exactly one result with a nonblank
`ClassificationName`; place that returned value in both the `Organization` and
`OrgUnitClassification` rows. Do not hard-code the name.

`ClassificationCode` is non-mandatory for create and update rows. Leave every
DAT `ClassificationCode` attribute blank, including in `Organization` and
`OrgUnitClassification` rows.

## Location derivation and defaults

For each create or update row, collect either the complete explicit
`LocationCode`/`LocationSetCode` pair, or Task Location Name plus Location Set
Name. If both codes are supplied, use them unchanged and skip `locationsLov`.
Otherwise require both names and issue a read-only
`GET /hcmRestApi/resources/latest/locationsLov` effective on the organization's
`EffectiveStartDate`, with `REST-Framework-Version: 9`. Match `LocationName`
and `SetName` exactly—no trim, case-fold, partial, or closest-match selection.
Require exactly one response and map its `LocationCode` to DAT `LocationCode`
and `SetCode` to DAT `LocationSetCode`.

Reject partial code pairs, partial name pairs, no location pair, and zero or
multiple exact name results. Never combine explicit and derived values.

For `OrgUnitClassification.Status`, retain a supplied metadata-valid value; if
omitted, default it to `A`. Do not apply `Status` to the `Organization` row
unless the live operation-specific template requires it. Use `YYYY/MM/DD` date
format.

## Preflight and DAT validation

- Validate supported operation; selected environment and matching active Run
  Book; nonblank metadata-valid organization name; valid effective date; and
  an unambiguous identity for update or inactivation.
- Reject whitespace-only values, unsupported attributes, DAT delimiters or line
  breaks in scalar values, over-length values, invalid dates, and an update
  without a supported change.
- Use `core.data-loader` to validate current `Organization` metadata, section
  names, metadata order, delimiters, row width, required operation keys, and
  allowed status values. Stop for incompatible or ambiguous metadata.
- Require an `Organization` MERGE row and an operation-required
  `OrgUnitClassification` association. Reject `OrgInformation` `METADATA` or
  `MERGE` sections and populated `ClassificationCode` fields.
- Before preview, ensure both classification names exactly equal the single
  `BEN TPA` LOV result; a missing, zero-row, multi-row, or blank-name lookup is
  a blocking catalog-or-metadata mismatch.

## Submission and recovery

Use `core.data-loader` for source conversion, validation, immutable archive
preparation, approval binding, upload, and status retrieval. Present approval
only after all preflight checks pass; a changed source, environment, operation,
or archive requires fresh validation and approval. Do not use direct REST
writes.

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_authz`, `transport_environment`, `fusion_api`, `artifact_persistence`,
`approval_blocker`, `process_failed`, or `process_timeout`. For a failure,
persist redacted diagnostics with environment, operation, stage, artifact
reference, and safe next action. Do not automatically retry a mutation, roll
back a load, or expose secrets, tokens, full source rows, or protected IDs.
