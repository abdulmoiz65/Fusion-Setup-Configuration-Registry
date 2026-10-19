# REST Metadata to FSM Candidate ZIP

Use this workflow only after the business proposal has been reviewed and the
requested profile type, content-section template, name, description, flags,
property presentation, and subscribers are known. It prepares a new,
review-only `HRT_MANAGE_PROFILE_TYPES` candidate ZIP; it does not submit an
import or change Fusion.

## Source Contract

Obtain every Fusion response with GET through
`core.fusion-api.rest-api-client`. Use the stable logical resource paths below,
not a browser-captured `/rest/rv:<opaque-value>/...` URL. Never copy request
headers, bearer tokens, cookies, or session values into input files.

| Evidence | Logical GET | Required result |
| --- | --- | --- |
| Template catalog | `profileTypeSectionsLOV` with `finder=findTemplateSections` | Fully paginated rows including exact `Name`, `SectionId`, `ContentTypeId`, `ProfileTypeId`, and `TemplateFlag` |
| Person/template properties | `talentProfileTypes/5/child/contentSections/{TemplateSectionId}/child/properties` | For a Person target, a fully paginated response filtered to `SourceProfileTypeCode IN ('P','B')`, plus the documented column and field exclusions |
| Target sections | `talentProfileTypes/{TargetProfileTypeId}/child/contentSections` | Fully paginated created sections used for duplicate checks |
| Profile type parent | `talentProfileTypes/{TargetProfileTypeId}` or one exact row from its collection GET | Required for every target because the native template/spec ZIP is header-only; include the profile code, description, summary, status, usage, dates, and approval flag |
| Person parents | `talentProfileTypes/1/child/contentSections` with `finder=findParentSections;ModelProfileTypeId={TargetProfileTypeId}`, or the runtime-confirmed equivalent | Required for every non-Person target; rows must expose `SectionId`, `SectionContext`, `ContentTypeId`, and `ActiveFlag` |
| Selected Person base properties | `talentProfileTypes/1/child/contentSections/{PersonSectionId}/child/properties` | Required for every non-Person target; fully paginated rows filtered to `SourceProfileTypeCode IN ('B') and SourceCode is null` |
| Model-only template properties | `talentProfileTypes/5/child/contentSections/{TemplateSectionId}/child/properties` | Required for every non-Person target; fully paginated rows filtered to `SourceProfileTypeCode IN ('M')` |
| Subscriber catalog | `talentProfileSectionSubscribersLOV` | Required only when a subscriber assignment is requested; each requested description or code must resolve to one row with `SourceCode` and `SourceId`. Use the selected template's exact `ContentTypeId` for the content-source relationship; if the LOV exposes a content type, it must match |

The properties request observed in the Profile Types UI applies a reusable
Person filter:

```text
SourceProfileTypeCode IN ('P','B')
AND ColumnName NOT IN ('COUNTRY_ID','STATE_PROVINCE_ID')
AND FieldName NOT IN ('NEXT_MOVE_LOCATION2')
```

The template is selected by the path's `TemplateSectionId`, not by the `q`
value. For a non-Person target, do not reuse one broad template response for
both property classes. First resolve the exact active Person section. Read its
`B` properties with `SourceCode is null`, then read the template section's `M`
properties. The builder validates both responses independently, merges their
rows, and preserves each property's `FieldName`, `ColumnName`,
`SourceProfileTypeCode`, `SourceCode`, input type, label, display mode, display
order, label key, and value-set identity. Subscriber-scoped Person rows are not
eligible for this merge.

Some catalog-backed templates expose the mutually exclusive leading pair
`CONTENT_ITEM_ID` and `NAME` at the same display position. Preserve the mode
returned by Fusion: catalog-based entry has `CONTENT_ITEM_ID=VALUESET` with a
blank `NAME` input type, while free-form entry has `NAME=TEXT` with a blank
`CONTENT_ITEM_ID` input type. Accept a blank type only for that exact paired
shape; any other blank or unsupported input type blocks preparation. Because
the leading mode cannot be changed after section creation, require the user to
choose catalog-based or free-form behavior when both patterns are possible.

The created-Person-sections collection may include both active and inactive
rows because its observed query does not explicitly filter `ActiveFlag`. The
builder always rejects an inactive Person parent. It also rejects a target
when the same Person `SectionId` or `SectionContext` is already represented in
that target profile type. This preserves the per-profile-type uniqueness rule:
one Job section, one Position section, and so on for the same Person section.

## Native Package Contract

REST metadata does not replace the native FSM archive contract. Before making a
live call, inspect the selected project's Profile Types export folder for an
existing native `HRT_MANAGE_PROFILE_TYPES` template/spec ZIP. It is reusable
only when ZIP integrity passes, exactly one `ASM_SETUP_CSV_METADATA.xml` marker
identifies `HRT_MANAGE_PROFILE_TYPES`, all required CSV members are present,
and every CSV contains a header with zero data rows. Record the archive's
SHA-256. If more than one valid candidate exists, select the newest archive
from the same environment only when its provenance is unambiguous; otherwise
stop for review.

When no valid reusable archive exists, route through
`shared.setup-export.task-level-export` in `--template-only` mode. Present the
exact source environment, Profile Types task and code, template-only operation,
and output directory, then obtain explicit approval immediately before creating
the Fusion export process. Do not use a current-data export as the structural
source and do not create another template export when a valid reusable archive
already exists.

Supply the validated empty native template/spec ZIP to the builder. It uses it
only for:

- the exact CSV headers;
- the complete native member inventory; and
- the unchanged `ASM_SETUP_CSV_METADATA.xml` bytes.

The selected seeded profile-type parent is normally resolved from complete REST
metadata because the native source has no data rows. If that declared provider
fails or omits a required owner field, a separately approved current-data FSM
export may provide reference evidence only. Confirm a safe exact filter before
offering it; without one, disclose and obtain explicit approval for a broader
full-task export. Preserve that export unchanged and use
`scripts/extract_owner_profile_reference.py` to derive exactly one validated
owner-row JSON reference. Pass the JSON as `--profile-types-response`; never
use the current-data export as `--source-template-zip`, modify it, or import it.

The builder preserves all native template members, replaces only the task CSVs
that receive approved candidate rows, and never copies customer configuration
into the candidate. It refuses malformed or nonempty template ZIPs, unsafe
members, incomplete REST pagination, ambiguous matches, missing profile
parents, unsupported property types, duplicate sections, inactive Person
parents, missing subscriber dependencies, and output overwrite.

For non-Person output, CSV parent linkage uses portable business keys:

```text
ParentSectionProfileTypeCode = PERSON
ParentSectionContextName = resolved content-type context
ParentSectionSectionContext = exact active Person SectionContext
ParentSectionId = empty
ParentSectionContentTypeId = empty
TemplateBasedSectionFlag = Y
```

`AttributeLabelKey` is preserved when Fusion returns it. A null value remains
blank; the builder never fabricates a resource key from the visible label.

## Request JSON

Required fields:

```json
{
  "target_profile_type_id": 1,
  "target_profile_type_code": "PERSON",
  "template_name": "Honor",
  "section_name": "FSCR Honor",
  "section_context": "PERSON_FSCR_HONOR",
  "description": "Captures honors and awards relevant to field service technicians.",
  "active": true
}
```

Optional fields include `content_type_id`, `content_type_context_name`,
`approval_required`, `default_section`, `section_item_required`,
`display_order`, `section_layout`, `linkedin_enabled`,
`skill_recommend_enabled`, `property_overrides`, `subscribers`, `translations`,
and `source_language`.

When the validated native source is an empty template/spec ZIP, the builder
requires source-backed owning Profile Type metadata, including Description,
Summary, status, dates, approval, ModuleId, and Person auto-create fields when
present in the native header. `ProfileUsageCode` follows the confirmed profile
classification: `P` for Person, `M` for Model. The builder derives a missing or
blank usage code only after validating the supported ID/code pair, and rejects
conflicting supplied `ProfileUsageCode` or `UsageCode` values. Other missing
REST fields remain a preparation blocker unless a separately approved unchanged
current-data FSM export is extracted into an exact validated owner reference;
they are not evidence that blank cells are safe to import. A supplied reference may
provide values only after its provenance, target identity, and applicability
are verified; lookup-definition dates and ModuleId are not profile values.
Do not start that export automatically, and do not use it as the candidate
archive. The archive must leave `AutoCreateFlag` empty for every Model profile, even if legacy
metadata or `AutoCreatePersonProfileFlag` supplies Y/N. This model-specific
exception does not change the Person requirement or any other required field.
The archive
base must remain the native empty template. Structural validation does not
prove Oracle import/update semantics. The owning Profile Type row is distinct
from a parent section: Person sections have no parent; only Model sections do.

Every non-Person request must also identify the exact Person source through
`person_section_id` or `person_section_context`. Property overrides may change
only `display`, `required`, `custom_label`, or `default_value`, and must identify
the property by `field_name` plus optional `column_name`.

When the owner-metadata fallback has separately passed export approval, first
extract the exact owner row without writing it:

```text
python3 scripts/extract_owner_profile_reference.py \
  --reference-export <unchanged-current-profile-types-export.zip> \
  --profile-type-id 2 \
  --profile-type-code JOB \
  --output <job-owner-reference.json> \
  --dry-run
```

Only after `status=planned`, rerun without `--dry-run`. The JSON output is the
only derived artifact; the export ZIP remains byte-for-byte unchanged. Pass the
JSON to the builder using `--profile-types-response`.

## Local Preparation

First validate without writing:

```text
python3 scripts/build_fsm_profile_type_section_zip.py \
  --request request.json \
  --templates-response templates.json \
  --properties-response properties.json \
  --target-sections-response target-sections.json \
  --source-template-zip source-profile-types.zip \
  --output candidate.zip \
  --dry-run
```

For a non-Person section, add `--person-sections-response`. When subscribers
are requested, add `--subscriber-response`. Also add
`--person-properties-response` with the complete selected-Person-section `B`
property response; `--properties-response` must contain the complete `M`
template-property response. Always add `--profile-types-response` because a
native template/spec export has no seeded profile-type data row. Remove
`--dry-run` only after the plan reports `status=planned`. The output must be a
new path under the selected project's Profile Types export folder.

The script returns a machine-readable summary with the exact template
`SectionId`, content type, target type, Person parent when applicable, row
counts, validation checks, output path, and SHA-256. Raw REST responses are not
copied into the ZIP or result.

After preparation, run the existing parent-anchor and subscriber-closure
validators as applicable. The resulting ZIP remains a review artifact until
Core Data Loader completes its independent Task Hook validation, immutable
preview, approval, and submission gates.

Oracle references:

- [Profile Type Sections List of Values](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-profiletypesectionslov-get.html)
- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
