# Read-Only REST Verification

Use this route to list the sections configured for a seeded profile type, or to
determine whether a requested profile content section and its related
configuration already exist in an authenticated Fusion environment.
It is an evidence-gathering route, not a configuration, export, or execution
route.

## Executable Diagnostic Workflow

Select `ptcs.read-only-verification` explicitly for a current-state check. It is
separate from the configuration/import Task Hook graph, whose unresolved
provider contracts remain blocking for configuration. Its entry point is
`scripts/verify_content_section.py`; it never reads or overrides that graph.

Supply a JSON object through `--input-stdin` (or `--request <file>`), first with
`--dry-run`, then run the same input only after the plan succeeds. A dry run
does not read credentials or contact Fusion. Example synthetic request:

```json
{
  "operation": "verify_profile_content_section",
  "method": "GET",
  "environment": "TEST_ALIAS",
  "profile_type_id": 1,
  "profile_type_key": "PERSON",
  "section_name": "Example Certifications",
  "content_type_id": 103,
  "template_name": "Certification",
  "expected_attributes": {"ApprovalRequiredFlag": true},
  "effective_date": "2026-10-01"
}
```

The content-type identity in the example is illustrative; use evidence for the
selected instance and require its exact live template match. Do not persist
technical IDs or raw source responses in project artifacts. Use stdin for
transient IDs. The helper does not write response files.

Property and content-item assignment comparison need a supported Profile Types
metadata provider and are rejected before the client is constructed. When
`expected_subscribers` supplies exact subscriber codes, the helper reads the
public subscriber LOV to establish catalog presence only; it records the
per-section assignment as `unverifiable`. Unknown fields, write methods,
bodies, action paths, or unsupported comparisons are rejected before the client
is constructed. The helper supports the section
LOV's documented Person, Job, Position, Organization, Requisition, and
Prerequisite identities; Template and Guide are not automated targets. It does not
automate model-parent or subscriber synchronization-flag comparison; do not
claim those are covered, or silently discard a request for them.

The helper uses the shared core OAuth cache reader and REST client, but does not
initiate login or refresh tokens. Missing/expired credentials or HTTP 401/403
require a separately selected Fusion login. Every GET has a 20-second timeout;
new requests stop after a 120-second run budget. Collections are limited to 50
pages of 100 rows. Failed/repeated/malformed pages return blocked rather than
not_found. The primary existence/approval read is the documented
`profileTypeSectionsLOV` finder `findByProfileTypeId;ProfileTypeId=<id>`.
Require every returned row to preserve the exact profile ID. Map `Name` to
section name and `DefaultFlag` to the default-section comparison; do not infer
`ActiveFlag`, which this LOV does not expose. This is a planned primary read,
not a fallback after a failed child-resource call. The exact ID/key mapping is
validated against the documented LOV enum before authentication.

The public section LOV and public subscriber LOV are the only configuration
sources used by this helper. They do not supply section properties, active
state, subscriber assignments, or the owning profile-type row. See the current
[Oracle section LOV contract](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-profiletypesectionslov-get.html).

Return `complete`, `partial`, or `blocked` separately from section existence.
`complete` means the read comparison finished, not that configuration is ready.
An existing section can have unverifiable children. Return the successful
evidence and the failed stage without erasing partial results. A future
effective date remains unverifiable. The terminal report must not trigger a
preview, export, import, or another write.

## List Sections Without Knowing Their Names

For questions such as "which sections are currently configured for Job?", use
the same helper and dry-run-first sequence with this inventory request:

```json
{
  "operation": "list_profile_content_sections",
  "method": "GET",
  "environment": "TEST_ALIAS",
  "profile_type_id": 2,
  "profile_type_key": "JOB"
}
```

Do not require a section name, context, template, content-type identity, export
or import. This operation accepts only the fields above; section filters and
comparison inputs are rejected before authentication. Use the separate exact
verification operation for comparisons, optionally using a returned
`SectionContext` as its business identity.

The helper reads the same documented `findByProfileTypeId` finder, validates
every returned profile identity and completes all pages. It returns `sections`
with `SectionName`, `SectionContext`, `ApprovalRequiredFlag`, and
`DefaultSectionFlag` (mapped from `DefaultFlag`), plus `section_count` and
pagination status. Missing/null flags are returned as null, never inferred as
false. Internal surrogate IDs and extra response fields are not displayed.
Malformed/duplicate identities, incomplete pagination or a failed page block
the inventory: no partial rows or misleading zero count are published.

`coverage=section_inventory_only` and `existence_status=not_evaluated` distinguish
an inventory from a named-section comparison. A successful empty inventory has
`section_count=0`; a blocked one has a null count. Completeness means all LOV
pages visible to the authenticated user were read, not that permissions exposed
every configuration row. This does not expose section properties, active state,
subscriber assignments or the owning profile-type configuration. Do not label
it a complete editable snapshot or infer import/update readiness. Do not persist
these customer section rows in project artifacts; use only a sanitized outcome
for continuity. A populated FSM export is a separate explicit request and
approval, not an automatic next step.

## Hard Method Boundary

- Every Fusion business-resource request in this route must use HTTP `GET`.
- Reject `POST`, `PUT`, `PATCH`, `DELETE`, request bodies, action endpoints, and
  any instruction that combines verification with a write before making a
  Fusion request.
- Do not invoke setup export/import, Core Data Loader, browser automation, or an
  alternate provider from this route. A missing read capability produces
  `blocked`; it never authorizes a fallback.
- Use `core.fusion-api.rest-api-client` with an explicit `--method GET`. Never
  pass `--body` or `--body-file`.
- Use only stable logical resource paths under
  `/hcmRestApi/resources/11.13.18.05`. Never copy or persist a host, session
  cookie, authorization header, token, or opaque `/rest/rv:<value>/...` route
  from browser traffic.

Authentication is a prerequisite. The method ledger for the Fusion business
resources must contain only `GET`; authentication transport and token material
must not be recorded as verification evidence.

## Request Contract

For exact section verification, require (inventory instead uses the contract
above):

- authenticated source environment identity;
- one exact seeded profile type ID and key from the scope mapping;
- exact `SectionContext`, when known; otherwise exact `SectionName` and
  `ContentTypeId`;
- expected related values that the user wants checked, such as template,
  section flags, properties, content-item catalog, subscriber assignment, or
  model-parent section.

Do not turn an omitted expected value into a default. Mark it `not_requested`.
An effective date is not exposed by the observed content-section setup reads;
report it as `unverifiable` instead of inferring it.

## Capability and Evidence Sequence

Run only the GETs needed for the requested comparison. Use bounded `fields`,
`onlyData=true`, deterministic ordering, and complete pagination.

| Evidence | GET resource | Rule |
|---|---|---|
| Primary section search and seeded identity | `/hcmRestApi/resources/11.13.18.05/profileTypeSectionsLOV` with `finder=findByProfileTypeId;ProfileTypeId={ProfileTypeId}` | Validate the exact requested ID/key against the documented enum; require returned ProfileTypeId to match. Page fully, then compare SectionContext or Name plus ContentTypeId and requested exposed flags. |
| Predefined template | `/hcmRestApi/resources/11.13.18.05/profileTypeSectionsLOV` with `finder=findTemplateSections` | Follow every page and match exact template `Name` and `ContentTypeId`. Preserve the returned `SectionId` as template identity only. The returned runtime catalog, not a hardcoded screenshot list, is authoritative for that environment. |
| Subscriber catalog | `/hcmRestApi/resources/11.13.18.05/talentProfileSectionSubscribersLOV` | For every requested exact `SourceCode`, fully paginate and require zero or one matching catalog row. Report `matches` only when every code resolves once; catalog presence does not prove assignment to the section, which remains `unverifiable`. |

The helper deliberately does not use a supplied HAR or browser traffic as a
provider contract. Absence of a public configuration resource is `blocked`, not
evidence that defaults or a header-only owner row are safe.

## Pagination and Exact Matching

For every collection:

1. Start at offset zero with a bounded limit.
2. Continue using the returned paging state until the last response has
   `hasMore=false`.
3. Treat a failed page, repeated page, missing paging state, or incomplete
   capture as `blocked`.
4. Apply exact matching only after the complete collection is available.

Section existence states are:

- `exists`: exactly one target section matches;
- `not_found`: the fully paginated target collection contains no exact match;
- `ambiguous`: more than one target section matches;
- `blocked`: capability, authorization, transport, response-shape, or
  pagination evidence is incomplete.

When the section exists, compare requested related configuration independently.
Use `matches`, `differs`, `unverifiable`, or `not_requested` for each component.
Key property rows by the tuple `FieldName`, `ColumnName`,
`SourceProfileTypeCode`, and `SourceCode`, preserving null as a distinct key
value. Compare requested values such as display mode, label/custom label,
display order, required/search/default values, input type, and value-set
reference. Do not expect a create payload and readback to have the same row
count because Fusion can normalize or omit submitted nested rows.

For a model section, `exists` does not by itself prove correct inheritance.
Compare the target `ParentSectionId` or returned parent context to exactly one
eligible Person section. The HAR validates this pattern only for Job; other
model types remain runtime-capability-gated.

## Result Contract

Return a machine-readable result and a short business summary with:

```json
{
  "operation": "verify_profile_content_section",
  "read_only": true,
  "methods_used": ["GET"],
  "writes_performed": false,
  "source_environment": "configured alias",
  "target": {
    "profile_type_id": 1,
    "profile_type_key": "PERSON",
    "section_context": "requested exact context",
    "section_name": "requested exact name",
    "content_type_id": "requested exact ID"
  },
  "existence_status": "exists | not_found | ambiguous | blocked",
  "pagination_complete": true,
  "component_results": {
    "template": "matches | differs | unverifiable | not_requested",
    "section_attributes": "matches | differs | unverifiable | not_requested",
    "properties": "matches | differs | unverifiable | not_requested",
    "content_item_catalog": "matches | differs | unverifiable | not_requested",
    "subscriber_catalog": "matches | differs | unverifiable | not_requested",
    "subscriber_assignments": "matches | differs | unverifiable | not_requested",
    "model_parent": "matches | differs | unverifiable | not_requested"
  },
  "differences": [],
  "unverifiable": [],
  "next_action": "none; read-only verification is complete"
}
```

Do not persist raw responses, access tokens, cookies, authorization headers,
opaque runtime route values, customer-sensitive rows, or surrogate IDs in the
project workspace. Persist only the sanitized comparison, method ledger,
source alias, pagination status, and non-sensitive evidence summary as a
`validation_result` when project continuity requires it.

The route ends after this report. A later configuration, export, or import
request is a new routed operation with its own prerequisites and approvals.
