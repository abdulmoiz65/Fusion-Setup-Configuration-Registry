# Regulatory Body HDL

## Scope and business object

`BEN_MANAGE_REGULATORY_BODY` (Manage Regulatory Bodies) uses
the `Organization` HDL business object. The generated root file is
`Organization.dat`; retain that exact filename and the live template's metadata
order. This task creates and maintains regulatory body master records.

Use only the `Organization` root and the operation-required
`OrgUnitClassification` association for a normal regulatory-body
request. Exclude `OrgInformation` and every Organization Information EFF
section from the generated DAT file, even when those sections appear in the
live template or source workbook.

## Classification derivation

Do not ask the requester for `ClassificationCode` or `ClassificationName`, and
do not accept either as configurable input for this task. Before source
construction, use the declared shared REST client to issue this read-only
lookup:

`GET /hcmRestApi/resources/latest/organizationClassificationsLOV?q=ClassificationCode='REGBOD'`

Send `REST-Framework-Version: 9` on this request.

Require exactly one result with a nonblank `ClassificationName`. Populate that
returned `ClassificationName` in both the `Organization` row and its
`OrgUnitClassification` row. Do not hard-code the classification name.

`ClassificationCode` is non-mandatory for create and update rows. Do not
populate the `ClassificationCode` attribute in any generated `Organization.dat`
row, including `Organization` and `OrgUnitClassification` rows.

## Location derivation

Collect one complete location input pair for each create or update row:

- explicit `LocationCode` and `LocationSetCode`; or
- Task Location Name and Location Set Name.

When both explicit code values are supplied, skip `locationsLov` and map them
unchanged to the `Organization` DAT `LocationCode` and `LocationSetCode`
attributes. Do not replace, normalize, or derive either value.

Otherwise, require both location-name values and use the declared shared REST
client for a read-only `GET /hcmRestApi/resources/latest/locationsLov` request
effective on the regulatory body's `EffectiveStartDate`. Set the
endpoint's effective-date parameter to that start date using the live endpoint
contract and send `REST-Framework-Version: 9`. Filter for an exact `LocationName` and exact `SetName` match; do not trim, case-fold, partially match, or select a closest result. Require exactly
one response, then map its `LocationCode` to DAT `LocationCode` and its
`SetCode` to DAT `LocationSetCode`.

Reject a partial code pair, a partial name pair, no pair, zero matches, or
multiple matches. A supplied code pair is authoritative and bypasses the REST
lookup; still let `core.data-loader` validate the final source against live
loader metadata.

For `OrgUnitClassification.Status`, preserve a supplied valid status. If no
status is supplied, default it to `A`. Do not apply `Status` to the
`Organization` row unless the live, operation-specific template requires it.

## Intake and source preparation

1. Establish create, update, inactivate, or supported date-effective operation,
   target environment, and task context. A request to create a source is not
   authorization to load it.
2. Collect the regulatory body name, effective date, explicit status
   when it differs from the default, and one complete location input pair. For
   name-based location input, use the effective start date for the `locationsLov`
   lookup. Resolve an existing organization unambiguously before an update or
   inactivation.
3. Generate and inspect the `Organization` DAT template with
   [core.data-loader](../../../../../../core/data-loader/SKILL.md). Preserve its
   section and attribute order. Stop on missing, ambiguous, or incompatible live
   metadata; do not fall back to another HDL object or a direct REST write.
4. Write date values as `YYYY/MM/DD`. Resolve the classification name from the
   required LOV query and apply the returned value to both applicable sections.
   Leave `ClassificationCode` blank in every DAT row. Apply the `A` status
   default only in `OrgUnitClassification` when status was omitted.

## Validation before approval

- Require an unambiguous organization identity and the fields that live metadata
  requires for the selected operation. Never invent identifiers, effective
  dates, EFF values, or a classification name; obtain the latter from the LOV.
- Verify that an `Organization` MERGE row and at least one operation-required
  `OrgUnitClassification` association are present when the template requires
  them. Validate section names, metadata order, row width, delimiters, dates,
  and field lengths with core.
- Reject a source or prepared DAT archive that includes an `OrgInformation`
  `METADATA` or `MERGE` section.
- Reject any user-supplied `ClassificationCode` or `ClassificationName`; obtain
  the name from the required LOV result and place it in both rows. Leave every
  DAT `ClassificationCode` attribute blank.
- Preserve a supplied `OrgUnitClassification.Status`; otherwise emit `A` in that
  association. Reject a status that current metadata does not support rather
  than silently changing it.
- For location, use an explicit complete `LocationCode`/`LocationSetCode` pair
  unchanged, or map a single exact effective-dated `locationsLov` match. Never
  combine explicit and derived values or choose among multiple matches.
- For updates and inactivations, resolve an exact existing organization and
  effective-date intent. Do not use HDL `DELETE` unless the live contract
  explicitly supports the requested operation and approval covers it.

## Submission, results, and recovery

Use `core.data-loader` for source conversion, schema validation, immutable
archive preparation, approval binding, upload, and status retrieval. Present the
approved archive only after all validation checks pass; source, environment, or
operation changes require fresh validation and approval. Do not bypass core with
a direct REST write.

On input or metadata errors, identify the field and row, correct the source, and
restart validation. On authentication, authorization, transport, or process
failure, follow core's bounded recovery policy. Do not automatically resubmit a
mutation, roll back successful rows, or substitute a different business object.
