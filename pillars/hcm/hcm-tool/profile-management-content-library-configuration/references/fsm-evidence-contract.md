# FSM Evidence and Exact-Comparison Contract

Use this contract only for local inspection of an already exported FSM task ZIP and for task-local exact comparison. It does not authorize package creation, upload, import, or any Fusion write.

## Implementation

The deterministic implementation is:

`scripts/profile_content_library_fsm_evidence.py`

It uses the Python standard library only. It has no OAuth, REST, browser, UCM, Data Loader, or Fusion mutation dependency. Business rows remain in memory; the CLI emits only a sanitized evidence summary.

## Supported Tasks

| Task | Task code | Required CSV members |
| --- | --- | --- |
| Content Types | `HRT_MANAGE_PROFILE_CONTENT_TYPES` | `HRT_CONTENT_TYPES_B.csv`, `ORA_HRT_CONTENT_PROPERTY.csv`, `ORA_HRT_CONTENT_TYPE_RLAT.csv` |
| Content Items | `HRT_MANAGE_PROFILE_CONTENT_ITEMS` | `HRT_CONTENT_ITEMS_B.csv`, `ORA_HRT_CONTENT_ITEM_RLAT.csv` |
| Item Catalogs | `ORA_MANAGE_PROFILE_ITEM_CATALOG` | `ORA_TALENT_PROFILE_ITEM_CATALOG.csv`, `ORA_TALENT_CATALOG_CONTENT_ITEM.csv`, `ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv` |
| Educational Establishments | `HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS` | `HRT_SCHOOL.csv` |

Every archive must also contain `ASM_SETUP_CSV_METADATA.xml`. The implementation owns the exact observed header contracts. An unexpected member or column blocks inspection until its provider contract is reviewed; it is never silently ignored.

Item-specific proficiency descriptions remain unsupported because the current Content Items evidence has no provider-owned CSV/readback field contract for that object.

## Evidence Purposes

| Purpose | Permitted use | Readiness rule |
| --- | --- | --- |
| `schema` | Validate archive shape, metadata task identity, members, headers, encoding, and row counts | May use a sanitized alternate-environment export |
| `current-state` | Exact duplicate classification | Requires an unfiltered same-target task export; Content Types and Content Items also require the integrity-validated seed catalog when seeded rows may be omitted; Item Catalog package readiness additionally requires a populated catalog member |
| `readback` | Compare saved values with an approved proposal | Requires a complete populated same-target post-operation export |

Header-only evidence is schema evidence when used alone. A header-only Content Types or Content Items export may be treated as an empty customer layer only when it is explicitly attested as an unfiltered task export, is bound to the exact target, and is combined with a validated seed catalog for the declared task/provider schema. Alternate-environment evidence and header-only evidence for tasks without an approved seed overlay remain schema-only and cannot return a target duplicate disposition or readback verification.

## Integrity-Validated Seed Overlay

The checked-in evidence assets are:

- `assets/seeded-content-types/` for Content Type identities, properties, and relationships.
- `assets/seeded-content-items/` for Content Item identities and minimum collision fields.

Each catalog has a strict manifest containing its source Fusion release, ADE label, generation date, logical source paths and source hashes, per-file hashes, row counts, columns, and provider keys. The source release is provenance only and is never compared with the target. The loader rejects a malformed manifest, unexpected column, changed hash, duplicate or blank provider key, unsafe path, or invalid generation date. Report packaged seeds separately from observed target rows; this baseline is not independent target readback or a live compatibility certification.

Resolution order is always:

1. Read the fresh, unfiltered customer task export for the exact target.
2. Validate the integrity-validated seeded catalog.
3. Overlay fresh rows on the same seeded provider key.
4. Classify either exact key canonically as `exact`, record `match_source` as `customer` or `seeded`, and classify absence across both layers as `not-found`.

The Content Item catalog is an identity/collision catalog, not a complete provider row, readback source, or import template. Neither catalog may be sent to Fusion. Regenerate both catalogs only from the three authoritative seed XML sources using `scripts/generate_seeded_profile_content_library_catalog.py`, and review the ADE label, release, counts, and hashes before committing the generated assets.

## Archive Safety

The inspector fails closed on:

- Missing or unexpected members.
- Nested, absolute, traversal, symbolic-link, or encrypted members.
- Duplicate case-insensitive member names.
- Unsupported member count or uncompressed size.
- Invalid UTF-8, NUL characters, malformed CSV, or mismatched headers.
- Malformed XML, DTD/entity declarations, or a metadata/task-code mismatch.
- Missing target alias for current-state or readback evidence.

The environment inputs are non-sensitive aliases, not URLs or credentials.

## Exact Classification

Allowed duplicate classifications remain:

- `exact`
- `not-found`
- `multiple-exact`
- `evidence-unavailable`

For an exact Content Type or Content Item result, return `match_source` as
`customer` or `seeded`. Source is evidence metadata and must never be encoded
as a new classification value.

Do not evaluate generic name similarity or emit normalized near-match warnings.
Preserve source-declared provider case semantics and real task-specific Name/code
collision blockers. Exact existing keys stop creation even when all values are
equal; report actual matched identifiers from the source, not inferred keys.
The exact keys currently implemented are:

- Educational Establishment: `SchoolCode`
- Legacy Content Item provider identity: `(ContextName, Name)`, with a separate exact `(ContextName, ContentItemCode)` collision guard
- Legacy Content Item relationship: source and related type/item endpoints; `RelationshipCode` is a compared attribute, not a discriminator
- Content Type: `ContextName`, followed by an exact comparison of the header, properties, and relationships
- Item Catalog: `(ContextName, ContentValueSetCode)`, followed by an exact
  comparison of `ValueSetName` and `ValueSetDescription`; a normalized catalog
  name within the same Content Type separately blocks create

Create-provider guarantees are defined only by the separately reviewed
[FSM import contract](fsm-import-contract.md). Evidence keys alone do not
authorize package preparation or import.

## Task-Specific Validation

Supplied `DateFrom` and `DateTo` values must be valid calendar dates in exact
`YYYY-MM-DD` form. Compact dates and ISO week dates are not this input contract.
Validate supplied dates before duplicate classification or approved-value
readback; matching malformed values in an export must not produce verification.
This does not change the separate comparison of canonical approved dates with
the provider's supported `YYYY/MM/DD` export representation. Preserve omitted
optional dates, permit equal bounds, and reject an end date before its start.

### Educational Establishments

- Require `SchoolCode` and `Name`.
- Require explicit country code/geography and state code/geography pairs when supplied.
- Never infer state or country from `Location`.
- Treat generated IDs as readback-only.

### Content Items

- Require `ContextName`, `ContentItemCode`, and `Name`.
- Require owning Content Type evidence before accepting dynamic item attributes.
- Check the source-declared `(ContextName, Name)` identity and the separate `(ContextName, ContentItemCode)` guard in fresh customer and applicable seeded evidence. Either collision blocks create, including a matching Name with a different code. Report identifiers from matching source rows; conflicting Name/code matches must not be collapsed to one candidate.
- Require verified read-only Rating Model evidence when `RatingModelCode` is supplied.
- Require exact item endpoints and the corresponding Content Type relationship before accepting an item relationship.
- Relationship `Name` and `ContextName`, when supplied, must agree with the source endpoint. The resolved endpoint pair is unique independently of relationship code or dates. A supported legacy FSM package requires explicitly supplied `DateFrom` for both item and relationship rows; never fill it from the current date.
- Keep item-specific proficiency descriptions blocked.

### Item Catalogs

- Require `ContentValueSetCode`, `ContextName`, and `ValueSetName`.
- Require `ViewInstanceName` equal to `ContentTypeValueSet` and `GroupingKey`
  equal to `<ContextName>,<ContentValueSetCode>` when provider rows are present.
- Compare exact `(ContextName, ContentValueSetCode)` first, then compare all
  portable catalog business fields.
- Treat an owning-Content-Type/catalog-name collision as a create blocker, not
  as reusable identity.
- Require a fresh populated full export for package and post-import readback.
- A phase-one catalog-owned Content Item may be classified and read back only
  with one exact parent `(ContextName, ContentValueSetCode)` anchor and child
  `(ContextName, Name, ContentValueSetCode)` key. Treat `ContentItemCode` as a
  full-export collision guard and a normalized same-catalog name as a blocker.
  Compare portable child fields and verify parent no-drift after import.
  Rating-description writes remain blocked.

### Content Types

- Require `ContextName` and `ContentTypeName`.
- Require an approved `FieldName`/`ColumnName` contract for each property.
- Property identity is `(ContextName, FieldName)`, not ColumnName. A supplied property ContextName must agree with its containing parent.
- Require exact relationship endpoints. The portable relationship user key is the endpoint-context pair, not RelationshipCode; do not allow duplicate pairs in a create-only proposal. Supplied ContextName/ContextName1 aliases must agree with those endpoints.
- Require supplied relationship DateFrom before configuration readiness; DateTo remains optional and may equal DateFrom. The physical dated alternate key does not authorize a multi-date lifecycle workflow.
- Never guess `ViewInstanceName`, `GroupingKey`, or `ModuleId`.
- Treat a header-only export as `evidence-unavailable` unless it is an attested unfiltered same-target customer layer combined with the integrity-validated Content Types catalog.

These local guards follow the inspected v2 ContentTypePropertyVO (v2),
ContentTypeRelationshipVO/EO (v6), ContentItemVO (v6), and
ContentItemRelationshipVO/EO (v4). They do not certify deployed provider case
semantics, full-set persistence or live readback. No generic normalization is
introduced for legacy names; the enhanced Item Catalog provider keeps its
separately declared Name/code collision semantics.

## Readback

Readback returns `verified-with-derived-fields`, `mismatch`, `missing`, `multiple`, or `unavailable`. It reports differing field names without persisting complete current rows and never auto-corrects a mismatch.

## CLI

Run from the repository root:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/profile_content_library_fsm_evidence.py <export.zip> \
  --task-code HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS \
  --source-environment-alias NONPROD_A \
  --target-environment-alias NONPROD_A \
  --fusion-release 27B \
  --purpose current-state \
  --unfiltered-task-export
```

The CLI reads the archive and prints a sanitized JSON summary. A blocked contract returns a nonzero exit code. It does not create an artifact automatically.
