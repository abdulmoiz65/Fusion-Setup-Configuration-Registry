# Native Profile Types FSM Package Contract

Use a validated native FSM CSV export for the `HRT_MANAGE_PROFILE_TYPES` setup
object as the package-shape template. The archive must contain exactly one
`ASM_SETUP_CSV_METADATA.xml` marker identifying that setup object. Do not use a
handmade blank ZIP, rename unrelated CSV files, or treat example rows as
configuration defaults.

The validated native metadata marker is also the provider-registration
evidence for this task. Require it to declare `HRT_MANAGE_PROFILE_TYPES`, the
task-owned business-object graph and node paths, and a nonblank migration
service registration. Preserve the marker byte-for-byte in the candidate.
Confirm the target environment exposes `ImportSupportedFlag=Y` through the
documented task CSV import capability GET before preview. These checks support
the create-only FSM route; they do not authorize a direct HCM REST write,
update, delete, merge, or overwrite.

## Recognized Members

The validated package shape can include these task-owned members. Include only
the members and rows required by the approved scope while preserving the native
filenames and metadata relationships.

- `HRT_PROFILE_TYPES_B.csv`
- `HRT_PROFILE_TYPES_B_TRANSLATION.csv`
- `ORA_HRT_PROFILE_TYPE_SECTIONS.csv`
- `ORA_HRT_PROFILE_TYPE_SECTIONS_TRANSLATION.csv`
- `ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE.csv`
- `ORA_HRT_PROFILE_TYPE_SECTION_PROPS.csv`
- `ORA_HRT_PROFILE_TYPE_SECTION_PROPS_TRANSLATION.csv`
- `ORA_HRT_PROFILE_TYPE_SUBSCRIBER_PROFILE_TYPE_SECTION_PROP.csv`
- `ORA_HRT_PROFILE_TYPE_SUBSCRIBER_PROFILE_TYPE_SECTION_PROP_TRANSLATION.csv`
- `ORA_TALENT_PROFILE_TYPE_SECTION_QUALIFIER_SET.csv`
- `ORA_TALENT_PROFILE_TYPE_SECTION_QUALIFIER_SET_TRANSLATION.csv`
- `ORA_TALENT_PROFILE_TYPE_SECTION_QUALIFIER.csv`
- `ORA_TALENT_PROFILE_TYPE_SECTION_QUALIFIER_TRANSLATION.csv`
- `ASM_SETUP_CSV_METADATA.xml`

## Validation Rules

- Confirm the ZIP is structurally valid and contains no unsafe member paths.
- Confirm the metadata setup object is exactly `HRT_MANAGE_PROFILE_TYPES`.
- Require `ASM_SETUP_CSV_METADATA.xml` content to remain byte-for-byte identical
  to the selected native source-template archive during candidate construction;
  renaming or copying a candidate does not satisfy semantic validation.
- Inspect every parent, section, property, content-source, qualifier,
  subscriber-property, and translation row against the approved business
  scope. Structural validity alone is not sufficient.
- Treat `ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE.csv` as the section-to-subscriber
  assignment. When a subscriber is explicitly supplied, require exactly one
  content-source row matching its exact profile type, content context, section
  context, and predefined source code. Subscriber-property rows configure that
  relationship; they do not create it.
- Reject every subscriber-property row without exactly one matching content-
  source relationship and every subscriber-property translation without
  exactly one matching base subscriber-property row. A content-source
  relationship may omit subscriber-property rows only when the request supplied
  no subscriber attribute selections.
- Reject a custom parent profile type for a Profiles V2 outcome. Do not rewrite
  `ProfileTypeCode` or `ProfileUsageCode` into a seeded profile-type key.
- Run the exact duplicate lookup for every candidate content section. The gate
  clears only when every candidate has zero exact matches. If any one section
  is an exact duplicate, reject the entire archive; do not partially import its
  new sections or offer approval to update, merge, overwrite, resubmit, or add
  child rows. Continue only with a new archive that excludes every duplicate
  and completes a fresh validation and approval cycle. Multiple exact rows for
  any candidate are ambiguous and also reject the entire archive.
- Preserve the exact validated archive bytes and SHA-256 from preview through
  submission. Any content change requires a new validation and approval cycle.
- Use the archive only through Core Data Loader's Task Hook and authorized
  task-level adapter. A reusable example must never contain customer-specific
  or production-sensitive values.

## New Person Section Key Resolution

The owning `HRT_PROFILE_TYPES_B` row uses `ProfileUsageCode=P` for Person
profiles; Model profiles use `M`. Populate a missing usage code from the
validated profile classification and reject conflicting supplied values.
Do not confuse this classification with a profile ID or a parent section.
Other required owner metadata and import validation remain independent gates.

Require the owning profile name (`HRT_PROFILE_TYPES_B.Description`), start
date (`DateFrom`), and end date (`DateTo`) when preparing the package. Use the
verified owning-profile reference or explicit approved values; format dates
as `YYYY/MM/DD`, validate calendar dates, and require `DateFrom <= DateTo`.
The PERSON profile name is `Person`, distinct from a new section name such as
`FSCR Education`. A populated section name does not satisfy the owner name.
Do not infer an environment-independent start/end date from a lookup or clock.

For a generated Person content section, leave the section row's `SectionId`,
`ProfileTypeId`, and `ContentTypeId` empty. Do not write the literal `#null` to
`ContentTypeId`: the FSM importer must resolve the new section from its business
keys and propagate that resolved parent identity to the property children.

Leave each property row's `SectionId`, `ProfileTypeId`, and `ContentTypeId`
empty, and require its four prefixed parent keys to match the generated section
exactly: parent `ProfileTypeCode`, `ContentTypeContextName`, `ProfileTypeCode`,
and `SectionContext`. Apply the same business-key relationship rule to section
and property translations. A mismatch or a literal-null parent relationship is
an input-validation blocker before immutable preview.

After an approved import succeeds, fully paginate the documented
`profileTypeSectionsLOV` `findByProfileTypeId` read and require exactly one row
with the approved `ProfileTypeId` and `SectionContext`. Compare the returned
name, content type, template flag, approval flag, and default flag when exposed.
Missing, ambiguous, incomplete, or different readback is not successful
persistence.

## Non-Person Content-Section Parent Anchors

### REST-derived alternative

For Model sections prepared from an empty native template and REST metadata,
validate with `validate_fsm_parent_anchors.py <candidate.zip>
--source-template-archive <native-empty-template.zip>
--parent-lookup-json <complete-person-sections.json>
--rest-parent-evidence <evidence.json>`. This validation-only mode must not use
`--output` or `--source-section-context`. The archive-derived mode below is
unchanged and applies when a populated source-template row is available.

The evidence object contains `parent_profile_type_id: 1`, the exact
`target_profile_type_id` and `target_profile_type_code`, `sections` entries with
`section_context` and the independently approved `person_section_context`, and
complete `content_types` and `target_sections` REST response objects. Capture
these through the declared core REST client: Person `contentSections` with
`findParentSections;ModelProfileTypeId=<target>`, `contentTypesLOV`, and the
target profile's `contentSections`. Each collection must report `hasMore=false`.
Bind the collection owner IDs to the actual requested paths; never infer them
from the candidate. Do not derive the approved parent selection from candidate
parent fields. Keep raw evidence in temporary storage outside project artifacts.

The validator checks every Model row, exact active Person match, content type
and context, seeded target identity, absence of existing target/parent use,
portable parent keys, empty parent surrogate IDs, and unchanged native metadata.
This clears only the parent-anchor gate; template/property eligibility, archive
scope, environment, privilege, Task Hook and import approval remain independent.

### Archive-derived relationship

Before preview, validate each generated section for a seeded profile type other
than `PERSON` against exactly one active source-template row selected by the
explicit source `SectionContext`, with the same `ProfileTypeCode` and
`ContentTypeContextName`. This applies to every supported non-Person target, not
only `JOB`. The source row must have `ActiveFlag=Y`,
`TemplateBasedSectionFlag=Y`, and a nonblank
`ParentSectionSectionContext`. Do not erase those values while filtering or
renaming the section.

Resolve that parent section using the documented
`findByProfileTypeId;ProfileTypeId=1` finder. Consume the complete paginated
Person-section result and require exactly one row with `ProfileTypeId=1` and an
exact `SectionContext` match. Do not require `TemplateFlag=true` on the Person
parent: the live resource can return it as null for that row. When the provider
returns an explicit active flag, it must be true. Zero or multiple matches block
normalization and preview. `findTemplateSections` is not a substitute for this
parent check because it can return seeded `TEMPLATE_*` rows under profile type 5.

Normalize the generated row from the resolved business keys, never from a new
section name:

| CSV field | Required normalized value |
|---|---|
| ParentSectionProfileTypeCode | PERSON |
| ParentSectionContextName | Exact ContentTypeContextName of the resolved source template |
| ParentSectionSectionContext | Exact SectionContext returned for the Person template |
| TemplateBasedSectionFlag | Y |
| ParentSectionId | Empty; do not copy or invent a surrogate ID |
| ParentSectionContentTypeId | Empty; do not copy or invent a surrogate ID |

For the delivered competency relationship, the resulting business-key tuple is
`PERSON`, `COMPETENCY`, `PERSON_COMPETENCY`. A non-Person row must never reach
immutable preview when any of the three parent business-key fields or
`TemplateBasedSectionFlag` is blank or differs from the resolved parent.

When no exact active Person section exists, return the missing prerequisite to
the skill. The skill discloses it and requests explicit approval to add the
Person section to the implementation scope. After approval, the FSM processing
layer owns missing-parent package construction and parent-before-target
ordering. When the Person section already exists, the REST-metadata candidate
builder may construct one target section and must reject a second use of that
parent in the same target profile type. This validator does not create the
Person section, split the archive, or replace Core Data Loader's final approval
gate.

Run `scripts/validate_fsm_parent_anchors.py` with the candidate ZIP, the current
source-template ZIP, the exact source section context, and the complete read-only
`findByProfileTypeId` Person response. Never choose among multiple active source
sections using content type alone.
Use `--output` only while constructing a new candidate before preview. The
normalizer restores and preserves the source-template metadata-marker content
byte-for-byte and preserves unrelated candidate member content; the new archive
must complete the full validation and approval cycle.
