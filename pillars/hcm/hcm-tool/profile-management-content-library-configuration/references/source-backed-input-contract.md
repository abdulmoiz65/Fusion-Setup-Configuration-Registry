# Source-Backed Input Contract

## Purpose

Define the local intake contract for conversation, the governed multi-sheet XLSX workbook, the optional flat CSV, or another readable source file. This contract normalizes requirements only. It is not an FSM, HDL, HSDL, REST, or provider payload and never authorizes Fusion mutation.

Offer direct values, a blank requirements template, or an existing readable
file. Capture supplied configuration without business-purpose or downstream
discovery. A non-governed readable document requires host extraction with exact
source references and confirmed mappings; the CSV/XLSX helpers do not parse
arbitrary Word or PDF files. Keep uncertain mappings blocked before creation.

## Governed Blank Template

Use [the multi-sheet XLSX template](../templates/profile-management-content-library-configuration-intake.xlsx) by default for repeating rows; use [the flat CSV template](../templates/profile-management-content-library-configuration-intake.csv) only when one-sheet intake is preferable. Keep one `complete_set_id` across all rows belonging to the same request. The workbook normalizer derives task and record type from the governed sheet and preserves safe filename, sheet/row, source reference, supplied review status, and SHA-256 source fingerprint.

Run local validation from the repository root:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/normalize_profile_content_library_workbook.py <input.xlsx>

python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/normalize_profile_content_library_intake.py <input.csv>
```

The command prints sanitized normalized JSON. It has no network client and performs no Fusion operation.

A readable XLSX row whose supplied `record_type` or `task_code` conflicts with
its governed worksheet is retained with those supplied values and exact
sheet/row provenance. `mapping_conflicts` identifies the conflicting fields;
the row has `mapping_readiness: unmapped-requires-confirmation` and the complete
request stays blocked. The helper fills blank type/task cells from the sheet
only when there is no conflict. Never silently remap or discard conflicting
rows. Confirm the correction, normalize the full source again and regenerate
any dependent preview/approval; the correction changes the fingerprint.

Readable rows with a missing or unsupported `record_type` remain in
`unmapped_records`, with their supplied values and file/row provenance. They
have no inferred owning task. Review consumers must show both `records` and
`unmapped_records`; `source_record_count` counts both nonblank collections.
An unreadable header leaves that count unknown (`null`), not zero. A blank
governed template has zero rows. Unmapped rows keep the request blocked until
the user confirms their mapping; never pass only the mapped subset into an
exact check, package, or execution workflow.

Record review status and canonical field-mapping status are different fields.
An unconfirmed technical mapping has canonical `mappings[].status: uncertain`;
its associated intake record may have `review_status: inferred-pending-review`.
Only actual mapping confirmation permits `status: confirmed`. Do not copy a
record review-status string into the canonical mapping enum or infer a
confirmation merely because a record was supplied.

## Worked Local Mapping Example

For a synthetic `Content Types!2` row with `local_key=ct-one`,
`name=Synthetic Type One`, `code=SYN_CT_ONE`, and no supplied description,
confirm that `code` maps to the provider's Content Type context identifier.
The corresponding canonical `objects.content_types` row fragment is:

```json
{
  "local_key": "ct-one",
  "provider_key": {"type": "content-type-context", "values": ["SYN_CT_ONE"]},
  "values": {"name": "Synthetic Type One", "context_name": "SYN_CT_ONE"},
  "source_references": ["Content Types!2"],
  "review_status": "confirmed"
}
```

The mapping entry is `source_reference: Content Types!2`,
`target: content_types`, `status: confirmed` only after actual confirmation.
Before that, retain the supplied code in review input and use `status: uncertain`.
Do not add a blank description to the canonical values. Preserve the workbook's
safe filename and actual source SHA-256 in the enclosing source record and all
14 group arrays in the enclosing objects record. This fragment is not a complete
executable contract: required-field validation, dependencies, fresh exact checks,
provider readiness and immutable approval must still be established. Never fill
those checks with invented passed/not-found results to make the example execute.

## Template Columns

| Column | Required behavior |
|---|---|
| complete_set_id | One nonblank identifier shared by every row in one request |
| task_code | Exact setup task code owning the row |
| record_type | One record type from the readiness matrix below |
| local_key | Request-local stable identifier for an independently identifiable row |
| parent_local_key | Request-local parent identifier when the parent is supplied in the same set |
| parent_exact_reference | Exact externally evidenced parent reference when the parent is not supplied in the same set |
| related_local_key | Request-local related endpoint when supplied in the same set |
| related_exact_reference | Exact externally evidenced related endpoint when not supplied in the same set |
| name | Approved business name, translated name, property name, or proficiency level label as defined by the record type |
| code | Approved business code when supplied |
| description | Approved description when supplied |
| value | Approved property or other source value when the record type uses it |
| language | Supplied translation language when applicable |
| effective_start_date | ISO `YYYY-MM-DD` start date when applicable |
| effective_end_date | ISO `YYYY-MM-DD` end date when applicable; must not precede the start date |
| sequence | Positive integer when the source explicitly supplies an ordered row |
| relationship_code | Supplied relationship code for relationship records |
| location | Approved establishment location when applicable |
| country_code | Supplied establishment country code when applicable |
| country_geography_code | Exact country geography code paired with `country_code` when supplied |
| state_country_code | Exact state-country code paired with `state_geography_code` when supplied |
| state_geography_code | Exact state geography code; requires the complete country pair |
| free_form_flag | `Y` or `N` when explicitly supplied; a free-form Content Type cannot own properties, relationships, or items |
| attribute_label | Source-backed Content Type property label |
| column_name | Exact source-backed Content Type property storage column |
| default_value | Explicit property default; blank never creates an implicit default |
| required_flag | `Y` or `N` when explicitly supplied for a property |
| display_code | Exact source-backed property display code |
| view_attribute_name | Exact source-backed property view attribute |
| rating_model_code | Exact approved Rating Model code when the object supports it |
| rating_level_code | Exact approved rating level for an item-specific description |
| mandatory_flag | `Y` or `N` when explicitly supplied for a relationship |
| rating_interaction_type | Exact source-backed interaction type for a Content Type relationship |
| content_supplier_code | Exact supplied Content Item supplier code |
| additional_values_json | Optional JSON object of source-backed scalar dynamic values; nested objects and arrays are rejected |
| source_reference | Human-reviewable source reference; never a credential, token, employee row, or sensitive endpoint |
| review_status | `supplied`, `inferred-pending-review`, `confirmed`, `blocked`, or `not-applicable` |

Blank optional cells do not establish defaults. The proposal must disclose omissions and unavailable mappings.

Capture optional item-specific proficiency descriptions only when supplied and
supported with verified existing applicable Rating Model and level references.
Translations and effective dates are also conditional on source-backed task
support; capture readiness is distinct from an approved execution route.

## Field-Evidence and Readiness Matrix

| Record type | Owning task | Proposal-intake fields supported by current evidence | Evidence basis | Stage 3 readiness |
|---|---|---|---|---|
| content_type | Content Types | local key, name, description, source-backed free-form/property values captured through child rows | Configured export schema for HRT_CONTENT_TYPES_B; Oracle Content Types guidance | Source-backed proposal intake; exact tenant disposition still requires complete current evidence |
| content_type_property | Content Types | parent reference, property name, supplied value | Configured export schema for ORA_HRT_CONTENT_PROPERTY; Oracle Content Type Properties guidance | Source-backed proposal intake; no provider payload mapping |
| content_type_relationship | Content Types | exact source/related references, relationship code and supplied effective start date | Configured export schema for ORA_HRT_CONTENT_TYPE_RLAT; ContentTypeRelationshipVO/EO required DateFrom; Oracle relationship guidance | Source-backed proposal intake; missing required dates retain rows as blocked, never defaulted; no provider payload mapping |
| content_item | Content Items | parent Content Type reference, local key, name, code, description, dates, source reference | Configured complete export schema for HRT_CONTENT_ITEMS_B; Oracle Content Items guidance | Source-backed proposal intake and exact comparison. Creation requires the supported legacy FSM contract or eligible enhanced Item Catalog FSM handoff with its exact mode, evidence and approval gates. No generic HDL fallback: only an explicitly selected GOAL request may separately qualify under the [verified four-field single-row exception](verified-fallback-contract.md); it does not prove FSM-only acceptance. |
| content_item_relationship | Content Items | exact source/related item references, relationship code, dates | Configured complete export schema for ORA_HRT_CONTENT_ITEM_RLAT; Oracle relationship guidance | Source-backed proposal intake and exact comparison. Supported legacy relationship rows require approved endpoint/type-relationship evidence and the FSM package contract; enhanced and richer full-set paths remain blocked until independently supported. |
| content_item_translation | Content Items | parent item, language, translated name/description | GROW-8154 conceptual scope and approved source labels | Captured for review, but exact provider field/readback mapping is blocked |
| content_item_proficiency_description | Content Items | parent item, proficiency label, description, optional sequence | GROW-8154 conceptual scope and approved source labels | Captured for review, but Rating Model/provider field mapping is blocked |
| item_catalog | Item Catalogs | `ContextName`, `ContentValueSetCode`, `ValueSetName`, optional `ValueSetDescription`, plus source-backed view/grouping values only during package preparation | Fusion Item Catalog migration provider, populated full export, Jira, and Oracle Item Catalog concepts | Capture for review and exact comparison; catalog-only create package is allowed through the parent FSM contract after separate approval; one new catalog with supplied portable children uses only the separate [controlled new-set contract](new-catalog-set-contract.md) |
| item_catalog_membership | Item Catalogs | Exact existing parent key, `ContextName`, `ContentValueSetCode`, `Name`, `ContentItemCode`, supplier, dates, description, and source reference | Fusion export/provider source, source-backed FSM child registry, and approved Content Items business values | One create-only child package is allowed only with an exact parent anchor, lifecycle/provider evidence, and separate approval; advanced child fields remain blocked. The separate [controlled new-set contract](new-catalog-set-contract.md) permits all supplied portable children of one new parent with its own source/mapping/approval binding |
| item_catalog_rating_description | Item Catalogs | Comparison fields are source-backed, but no create mapping is approved in this phase | Fusion export/provider and Rating Model evidence; child mutation remains gated | Capture for review and exact comparison; block package rows |
| behavior_item_catalog | Item Catalogs | Catalog identity fields; portable behavior children require the separate controlled new-set package contract | Jira, Oracle behavior-catalog concepts, and the Item Catalog provider contract | Capture for review; the default catalog identity package has empty child members. A new catalog with portable children requires the explicit [controlled new-set contract](new-catalog-set-contract.md); competency-behavior relationships remain blocked |
| competency_behavior_relationship | Content Items | Exact competency and behavior references plus relationship code and dates | Jira and Oracle competency-to-behavior relationship concepts | Capture for review; block persistence preview until exact provider/readback contract is proven |
| instance_qualifier_set | Instance Qualifiers | QualifierSetCode, ProfileTypeCode, ContextName, SectionContext exact user key; Description, QualifierTypeCode, and KeyTableName proposal values | Fusion 26C Profile Types QualifierSetVO user key and exclusions, qualifier type constants, Oracle guidance, and the standalone no-column diagnostic | Source-backed proposal and comparison mapping; exact tenant disposition requires a complete HRT_MANAGE_PROFILE_TYPES artifact and standalone mutation remains blocked |
| instance_qualifier | Instance Qualifiers | Parent set user key plus QualifierCode exact child key; Description, QualifierSeqNumber, employee and manager view/default flags, and SearchFlag | Fusion 26C Profile Types QualifierVO user key and exclusions plus Oracle priority, visibility, search, and default guidance | Source-backed proposal and comparison mapping; exact tenant disposition requires a complete HRT_MANAGE_PROFILE_TYPES artifact and all mutation remains blocked |
| educational_establishment | Educational Establishments | local key, SchoolCode, Name, Description; optional Location and exact paired country/state geography codes; source reference | Migration EstablishmentVO and entity declarations plus the complete HRT_SCHOOL export schema | Capture supplied values for review. The supported FSM package requires SchoolCode, Name and source-required Description; preserve omitted Location/geography. Package and create remain subject to current target, same-task baseline, exact evidence and Core Data Loader gates. |

Configured export field existence is evidence for proposal capture and read-only comparison only. It does not establish required create fields, supported enums, size limits, privileges, idempotency, error semantics, or canonical readback.

## Validation Rules

1. Require the exact template header and exactly one complete set per input file.
2. Require task code and record type to agree.
3. Preserve every source row; do not silently rename, trim into a different value, or drop a nonblank field.
4. Require request-local parents and relationship endpoints to exist, or require an explicit exact external reference.
5. Reject duplicate local identities and exact duplicate rows.
6. Validate ISO dates, date order, and positive integer sequences.
7. Validate `Y`/`N` flags, geography pairs, scalar-only dynamic JSON, no self-relationships, and only one relationship type for a Content Type pair.
8. Keep `inferred-pending-review` and `blocked` rows out of a configuration-ready proposal.
9. Return visible persistence blockers for unsupported Item Catalog child rows, Competency-to-Behavior, Instance Qualifier, translation, or proficiency mappings whose provider-owned contract is unresolved.
10. Never infer Rating Models, lookups, value sets, profile options, technical IDs, defaults, or loader fields.
11. Never modify the supplied source file.

## Normalized Result

The local normalizer returns:

- `template_ready` for an untouched blank template;
- `normalized` when every supplied row passes the evidence-ready intake contract;
- `blocked` with explicit errors or readiness blockers otherwise.

Every result includes input method, safe source file, source SHA-256, complete-set identity, selected task codes, normalized records with sheet/row or CSV-row provenance, mapping readiness, errors, and blockers. Source documents and customer-sensitive extracted content must not be persisted in a project workspace. The result is intake evidence, not a duplicate result, approval, or execution preview.
