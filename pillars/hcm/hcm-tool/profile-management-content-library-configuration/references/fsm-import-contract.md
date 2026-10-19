# Create-Only FSM Import Contract

Read this contract during proposal review when assessing package eligibility.
Applying its package-construction workflow requires an approved GROW-8154 review
proposal and a separate explicit package-preparation request. It supports Content Types,
Content Items, Item Catalog creates including one anchored catalog-owned Content
Item, and Educational
Establishments. Instance Qualifiers remain unsupported.

The contract has two distinct runs:

1. The pillar prepares one immutable project-local FSM ZIP and sanitized
   readiness receipt with
   `scripts/prepare_profile_content_library_fsm_package.py`.
2. A separate `core.data-loader` run validates the same ZIP, invokes Task Hook,
   creates its immutable preview, applies its authoritative approval policy,
   and only then may upload and initiate the FSM import. Same-request explicit
   no-confirmation authority applies only to that identified load after all
   gates pass; otherwise a later contextual approval is required.

Proposal approval, package readiness, Task Hook validation, and Data Loader
submission approval are separate gates. No earlier confirmation authorizes a
later gate.

## Supported Scope

The explicit [new catalog set contract](new-catalog-set-contract.md) adds one
new catalog with all supplied portable children for controlled certification.
Only that separate mode overrides the existing-parent and one-child limits
below. It preserves all other safeguards and has no inherited live verification.

The separate [existing SKILL canary contract](../item-catalogs/references/existing-skill-catalog-certification.md)
adds one non-production SKILL child under a supplied, exactly evidenced existing
custom catalog anchor. It uses an independent certification-only registry,
explicit preview/preparation mode, complete binding and approval. It preserves
the one-parent/one-child limits and does not promote SKILL to general use.

| Task | Task code | Supported operation | Required CSV members |
|---|---|---|---|
| Content Types | HRT_MANAGE_PROFILE_CONTENT_TYPES | Create only | HRT_CONTENT_TYPES_B.csv; ORA_HRT_CONTENT_PROPERTY.csv; ORA_HRT_CONTENT_TYPE_RLAT.csv |
| Content Items | HRT_MANAGE_PROFILE_CONTENT_ITEMS | Create only; legacy-profile contexts only | HRT_CONTENT_ITEMS_B.csv; ORA_HRT_CONTENT_ITEM_RLAT.csv |
| Item Catalogs | ORA_MANAGE_PROFILE_ITEM_CATALOG | Create catalog rows, or one create-only Content Item with one exact existing-catalog anchor; rating descriptions prohibited | ORA_TALENT_PROFILE_ITEM_CATALOG.csv; ORA_TALENT_CATALOG_CONTENT_ITEM.csv; ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv |
| Educational Establishments | HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS | Create only | HRT_SCHOOL.csv |

Every package also contains the exact root member
`ASM_SETUP_CSV_METADATA.xml`. The metadata and ZIP member order come from one
approved same-task baseline and are preserved unchanged.

This V1 contract, including the new-set mode, does not support update, merge, delete, end-date, replacement,
item-specific proficiency-description rows, Item Catalog rating-description rows,
advanced Item Catalog child fields,
Content Item behavior loading, or
Instance Qualifiers.

The standalone Content Items FSM provider is not valid for any enhanced-profile
import. Non-`GOAL` rows retain only their eligible registered read routes and,
when independently supported, the Item Catalog FSM handoff with all narrow
parent/child guards. The complete exported two-member enhanced-profile `GOAL`
shape reached an unguarded companion-document transformation and failed before
loading any row. Resolve and bind `profile_mode` before packaging; keep enhanced
standalone GOAL blocked and never fabricate a translation member. The separately selected
[verified GOAL fallback exception](verified-fallback-contract.md) has its own
four-field single-row contract; it never enters this FSM builder or proves FSM
acceptance. Other historical HDL providers and generic HDL/HSDL/DAT fallback
remain inactive.

## Required Inputs

Apply the [operation-scoped compatibility contract](environment-preflight-contract.md).
Release labels are optional informational metadata, never package prerequisites.
Use unknown where an existing receipt needs a value. All tasks retain exact
task/provider/schema and target checks; none compares a target release against
a seed or provider allowlist. Educational Establishments and catalog-only
packages do not require seed overlays or Content Items REST capability evidence.

The current builder accepts only project-local inputs. This is not permission
to persist customer data. Before requesting any full export, establish that
its complete contents are permitted non-customer synthetic or approved seed
setup data. If that cannot be established, stop before acquisition and record
an `input_validation` blocker for the missing Core data-handling contract.
There is no approved customer-bearing export storage route in this package.
Do not substitute a filtered export, redact required evidence, or move inputs
outside the project to work around this restriction. Template-only metadata
preparation remains separate and must pass its own declared workflow gates.

- One approved proposal fingerprint.
- One separately approved provider-row fingerprint that binds the exact task,
  target, release, dependency evidence, and every value in every CSV column.
- One fresh, unfiltered same-target current-state task export that acts as the
  customer layer of the duplicate lock.
- For Content Types and Content Items, the integrity-validated seed catalogs,
  with every required manifest SHA-256 included
  in dependency evidence. Fresh rows take precedence over matching seed rows.
- One fresh same-target template-only export, or an explicitly reviewed
  complete export with the identical task/member/header contract, that acts as
  the package baseline.
- Exact provider-row values for every CSV column. The builder never guesses
  `ViewInstanceName`, `GroupingKey`, `ModuleId`, a generated identifier, a
  dynamic field, a Rating Model, or a relationship endpoint.
- Task-specific dependency evidence and fingerprints.
- A safe initialized FDOS project workspace and a reviewed `as_of` timestamp.
- One persisted Core Data Loader task context whose exact task name, task code,
  selected child `skill_path`, offering, functional area, and positive sequence
  match the package task. The task context is required for preview; it is not
  package or submission approval.

The Content Types task can omit Oracle-seeded rows from export. A header-only
Content Types export is not standalone duplicate evidence, but it can be the
empty customer layer when it is explicitly attested as unfiltered, is bound to
the exact target, and is paired with the integrity-validated Content
Types seed catalog. Without all three conditions, package preparation remains
blocked.

The Item Catalog task additionally requires a populated, unfiltered,
same-target current export. The product import body is gated by Profile V2
readiness; binding that populated export's SHA-256 into dependency evidence is
the approved indirect preflight for this phase. A header-only or child-only
archive cannot satisfy this gate.

## Item Catalog optional exports

For ORA_MANAGE_PROFILE_ITEM_CATALOG only, the
[optional-export policy](../item-catalogs/references/optional-export-policy.md)
replaces the mandatory current-state export and fresh-export-baseline requirements
above. Skip pre-import export without attempting it. Omit --current-state-zip with
a bound skipped current_state_receipt (failed is accepted for existing receipts);
reuse a validated package/template with kind reviewed-template when a new baseline
export must not be acquired. Do not fabricate empty current evidence or Profile V2 proof.
Carry unverified target checks into the Core preview. Known collisions and all
remaining package, target, dependency and approval checks remain enforced.
After import, report export failures and try registered REST reads with explicit
coverage limits. Other task contracts and provider-promotion criteria are unchanged.

## Package-Input JSON

The builder accepts one UTF-8 JSON object with these exact top-level keys:

```json
{
  "schema_version": "1.0",
  "operation": "create",
  "task_code": "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
  "proposal_fingerprint": "<64 lowercase hexadecimal characters>",
  "provider_rows_fingerprint": "<64 lowercase hexadecimal characters>",
  "target_environment": "<safe target alias>",
  "fusion_release": "unknown",
  "current_state_receipt": {
    "task_code": "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
    "target_environment": "<same alias>",
    "fusion_release": "unknown",
    "sha256": "<current-state ZIP SHA-256>",
    "captured_at": "<RFC 3339 timestamp>",
    "valid_through": "<RFC 3339 timestamp>",
    "complete": true,
    "unfiltered_task_export": true
  },
  "package_baseline_receipt": {
    "task_code": "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
    "target_environment": "<same alias>",
    "fusion_release": "unknown",
    "sha256": "<baseline ZIP SHA-256>",
    "captured_at": "<RFC 3339 timestamp>",
    "valid_through": "<RFC 3339 timestamp>",
    "kind": "template-only"
  },
  "dependency_evidence": {
    "evidence_fingerprints": []
  },
  "rows": {
    "HRT_SCHOOL.csv": [
      {
        "SchoolCode": "SYNTHETIC_SCHOOL_01",
        "ViewInstanceName": "EstablishmentVO",
        "GroupingKey": "SYNTHETIC_SCHOOL_01",
        "Description": "Synthetic School One",
        "Location": "Example City",
        "Name": "Synthetic School One",
        "PartyId": "",
        "CountryCountryCode": "US",
        "CountryGeographyCode": "US",
        "StateCountryCode": "",
        "StateGeographyCode": "",
        "CountryId": "",
        "EstablishmentId": "",
        "StateProvinceId": ""
      }
    ]
  }
}
```

`rows` must contain every required member, including an empty array for a
property or relationship member with no create rows. Every row must contain
every header field exactly once. Material row provenance remains in the
approved proposal; the readiness receipt contains only fingerprints and
counts.

Compute `provider_rows_fingerprint` as SHA-256 over canonical UTF-8 JSON with
sorted keys and compact separators for this exact material body:

```text
schema_version
operation
task_code
proposal_fingerprint
target_environment
fusion_release
dependency_evidence
rows
```

The fingerprint field itself and freshness receipts are excluded. Present the
complete provider rows and this fingerprint for separate package-preparation
approval. Any row, dependency, task, target, release, or proposal-fingerprint
change invalidates that approval.

## Task-Specific Dependency Evidence

### Fingerprint and Approval Sequence

| Evidence | What it binds | Gate and authority |
|---|---|---|
| Preview or task proposal fingerprint | Complete supplied set, target, mappings, dependencies and exact evidence | Review is non-executable. Where the canonical preview applies, PREPARE PACKAGE with its exact fingerprint authorizes only the local package-preparation phase. It does not approve a later unreviewed technical mapping. |
| Provider-row fingerprint | Exact task, proposal fingerprint, target, release, dependencies and every CSV value | Present and obtain the existing separate approval of these exact provider rows before constructing the ZIP. Any material change invalidates this approval. Do not manufacture approval from the earlier preview. |
| Archive SHA-256 and Core Task Hook preview | Final validated immutable ZIP and registered task context | Core Data Loader alone applies its approval or valid same-request auto-approval policy before upload/initiation. Earlier local approvals do not approve submission. |

These are the existing gates, not extra upload approvals. Task-specific Item
Catalog packages use their own proposal/row contract, not the unsupported
combined-set preview surface. A check report or historical approval never
substitutes for any required current artifact binding.

### Content Types

```json
{
  "known_content_type_contexts": ["RELATED_CONTEXT"],
  "allowed_property_pairs": [["FIELD_NAME", "ITEM_TEXT1"]],
  "evidence_fingerprints": ["<content-type-export-sha256>", "<seeded-content-types-manifest-sha256>"]
}
```

- A property must belong to a proposed Content Type and use one approved
  `FieldName`/`ColumnName` pair.
- A relationship source must be proposed in the same package.
- A related Content Type must be proposed in the package or listed in exact
  dependency evidence.
- A proposed `ContextName` must be absent from both the fresh customer layer
  and the integrity-validated seeded Content Types catalog.
- `FreeFormFlag` and `RequiredFlag` accept blank, `Y`, or `N` only.

### Content Items

```json
{
  "profile_mode": "legacy",
  "content_type_contexts": ["COMPETENCY"],
  "content_type_relationships": [["COMPETENCY", "BEHAVIOR", "CHILD"]],
  "rating_model_codes": ["PROFICIENCY"],
  "content_supplier_codes": ["ORA_ADMIN"],
  "applicable_dynamic_fields_by_context": {
    "COMPETENCY": ["ItemText1", "ItemNumber1"]
  },
  "evidence_fingerprints": ["<content-type sha256>", "<rating-model sha256>", "<seeded-content-types-manifest-sha256>", "<seeded-content-items-manifest-sha256>"]
}
```

- `profile_mode` must be exactly `legacy` or `enhanced`. This FSM contract
  accepts Content Items only in legacy mode. In enhanced mode, non-`GOAL`
  retains only registered reads or its separately supported Item Catalog FSM
  handoff under that task's contract, while `GOAL`
  fails closed on the verified companion-document provider defect before a
  package is written.

- Every owning Content Type must resolve exactly.
- `ViewInstanceName` must equal `ContentItem`, and `GroupingKey` must equal
  `<Name>,<ContextName>` as proven by the task export provider contract.
- A supplied `RatingModelCode` must resolve in approved Rating Model evidence.
- A supplied `ContentSupplierCode` must resolve in approved lookup evidence.
- A dynamic field is allowed only when the owning Content Type enables it.
- Required fields declared by a seeded owning Content Type must be nonblank in
  the create row after translating generated IDs to their provider inputs. For
  `COMPETENCY`, this includes `ContextName`, `Name`, `DateFrom`,
  `ContentSupplierCode`, and `RatingModelCode`; Fusion generates
  `ContentItemId`.
- A proposed item key must be absent from the fresh customer layer and the
  seeded Content Item identity catalog.
- Relationship endpoints and the corresponding Content Type relationship must
  resolve exactly.
- Item-specific proficiency-description rows remain unsupported because the
  provider-owned CSV/readback contract is not proven.

### Item Catalogs

```json
{
  "content_type_contexts": ["COMPETENCY"],
  "content_type_evidence_fingerprints": ["<content-type-evidence-sha256>"],
  "profile_v2_evidence_sha256": "<fresh-populated-item-catalog-export-sha256>",
  "item_catalog_content_item_contexts": ["COMPETENCY"],
  "content_supplier_codes": ["C"],
  "item_catalog_content_item_provider_sha256": "<source-backed-provider-registry-sha256>",
  "item_catalog_content_item_provider_use": "controlled-certification",
  "evidence_fingerprints": ["<fresh-populated-item-catalog-export-sha256>", "<content-type-evidence-sha256>"]
}
```

- Every owning `ContextName` must resolve in approved Content Type evidence.
- `ViewInstanceName` must equal `ContentTypeValueSet`.
- `GroupingKey` must equal `<ContextName>,<ContentValueSetCode>`.
- The exact create-only provider key is `(ContextName,
  ContentValueSetCode)`. It must be absent from the fresh full export.
- A case/whitespace-normalized `ValueSetName` collision within the owning
  Content Type blocks creation even when the provider code differs.
- `ModuleId`, `SeedDataSource`, `ContentTypeId`, and `ContentValueSetId` must
  remain blank.
- For a catalog-only create, both child-member arrays must be empty. For a
  phase-one Content Item create, carry exactly one parent anchor matching one
  current catalog by `(ContextName, ContentValueSetCode)` and one child by
  `(ContextName, Name, ContentValueSetCode)`; the child must carry the same
  parent values in both dotted and local fields, use `ContentItem`, serialize
  `GroupingKey` as `<Name>,<ContextName>,<ContentValueSetCode>`, and leave the
  rating-description member empty.
- The parent anchor must match current portable catalog values exactly, but its
  generated `ModuleId` remains blank in the upload. Base children are included
  in the root graph; the root graph commits before later translation handling.
  The child value set resolves through its parent logical row. Do not describe
  a separate parent-only commit before base children.
- The child requires a registered lifecycle-gated context, exact allowed
  supplier, lifecycle-compatible `item_catalog_content_item_provider_use`, ISO
  input date, code of at most 30 letters/digits/underscores, zero current code
  collisions, and zero case-insensitive same-catalog name collisions. A
  `certification-only` provider accepts only `controlled-certification`; only a
  `verified` provider may receive `general-use`. A catalog-only package must
  use `not-applicable`. Dynamic, Rating Model, translation, relationship, and
  generated child fields remain blank.
- Prior task-provider evidence records product version `11.13.26.10.0` and
  quarterly `26C` separately. These are provenance, not eligibility gates.
  Both anchored-child and catalog-only packages validate their actual same-target
  baseline and current evidence against the exact member/header/provider contract.

### Educational Establishments

Do not require a quarterly label, Profile V2 evidence, Talent Catalog REST
probe or seed overlay. This task uses its own supported FSM export/baseline and
exact SchoolCode evidence; missing or conflicting task/provider evidence still
blocks packaging. Preserve unknown release explicitly when metadata is absent.

```json
{
  "evidence_fingerprints": []
}
```

- `ViewInstanceName` must equal `EstablishmentVO`.
- `GroupingKey` must equal `SchoolCode`.
- Country and state geography fields must be supplied as complete pairs.
- Generated identifiers remain blank.

## Duplicate and Create-Only Lock

The builder reopens the fresh unfiltered customer-layer archive, validates the applicable source-backed seed catalogs, and blocks exact provider-key collisions:

- a Content Type with an exact `ContextName` in the fresh or seeded layer;
- a legacy Content Item with exact `(ContextName, Name)` provider identity or a `(ContextName, ContentItemCode)` collision in the fresh or seeded layer;
- an existing Content Item relationship with the exact source/related type and item endpoints, regardless of RelationshipCode;
- an Item Catalog with an exact `(ContextName, ContentValueSetCode)` or an
  owning-Content-Type/catalog-name collision;
- an Educational Establishment with an existing exact `SchoolCode`;
- duplicate create keys inside the proposed package; and
- any nonblank Fusion-generated identifier or `ModuleId` field.

Do not evaluate generic name similarity or disclose fuzzy/normalized near-match
warnings. Preserve source-declared exact case semantics and real Item Catalog
Name/code collision guards. An existing exact key blocks creation and is never
converted into reuse, update or merge behavior.

Content Type properties use `(ContextName, FieldName)` identity, not ColumnName;
their ContextName must match the containing header. Content Type relationships
allow one portable endpoint-context pair per create-only proposal, independent
of RelationshipCode. Their ContextName/ContextName1 aliases must match the
portable endpoints. Legacy Content Item relationship Name/ContextName aliases
must match its source endpoint. Require explicitly supplied DateFrom for Content
Type relationships and legacy Content Item/relationship rows; do not rely on
provider date defaults. DateTo remains omitted when not supplied, and equal
start/end dates remain valid. These guards do not approve full dated lifecycle
support or extend the one-parent/one-child Item Catalog route.

## Local Package Preparation

Run from the repository root, after every input and storage prerequisite above
has passed:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/prepare_profile_content_library_fsm_package.py \
  --project-root project/<project_id> \
  --task-code <supported-task-code> \
  --proposal-json <project-local-proposal.json> \
  --proposal-fingerprint <approved-proposal-sha256> \
  --provider-rows-fingerprint <approved-provider-rows-sha256> \
  --current-state-zip <fresh-complete-export.zip> \
  --baseline-zip <fresh-template-or-reviewed-export.zip> \
  --as-of <rfc3339-timestamp> \
  --output-zip <project-local-output.zip> \
  --readiness-report <project-local-readiness.json>
```

Every input and output must resolve inside the selected project workspace. The
builder preserves the baseline metadata bytes, member order, member metadata,
compression choice, CSV header order, header quoting, newline style, and BOM
choice. It writes only the approved create rows and reopens the final ZIP for
exact validation.

The sanitized readiness report contains package/member/header hashes, row
counts, and sanitized seed-catalog summaries including manifest hashes, not
business rows, XML contents, credentials, URLs, or Base64 data.
It also contains the exact Task Hook `finalData` object and task-context
requirements needed for the separate Data Loader preview. The positive
sequence is selected from the persisted task context; the builder does not
invent it.

## Core Data Loader Handoff

`package_ready_for_core_data_loader_preview` is not execution approval. Start a
separate mandatory `core.data-loader` run with the exact ZIP path and task
context:

1. Revalidate the exact package bytes and SHA-256.
2. Resolve exactly one entry from the persisted task context using the task
   name and positive sequence in the readiness receipt requirements. Require
   the same task code, child `skill_path`, `HCM Tool` offering, and `Profile
   Management Content Library Configuration` functional area.
3. Invoke Task Hook `data-load` for that exact task name and sequence.
4. Execute the compiled task rules and collect ordered `ruleResults`.
5. Build the Task Hook immutable preview using the exact `task_hook_final_data`
   object from the readiness receipt.
6. Stop and ask `Do you want to proceed with submitting the reviewed archive?`
   unless the same explicit package/execution request includes unambiguous Core
   Data Loader auto-approval wording for only the identified load or exact
   test-only Item Catalog batch.
7. After one standalone affirmative answer, or under that exact same-request
   auto-approval, approve and verify the same preview and archive through Task
   Hook.
8. Pass the unchanged Task Validation envelope to
   `core/data-loader/scripts/upload_and_initiate.py` using
   `--task-validation-envelope` and `--approve-upload`.
9. Upload to the FSM UCM account and initiate with `sourceType: FSM` exactly as
   defined by `core.data-loader`.
10. Return after accepted initiation. Monitor only when the user separately asks
   for status. For an exact test-only Item Catalog composite request, the user's
   batch instruction must explicitly include terminal monitoring and readback;
   the pillar-local runner then invokes the unchanged Core status CLI as the
   separately selected monitoring operation after initiation returns.
11. For verification, obtain a fresh same-target task export and compare it
    through the existing FSM readback contract. Never auto-correct a mismatch.

Any change to the proposal, task context, target, evidence, baseline, package,
Task Hook results, or archive SHA-256 invalidates the preview and approval.

The optional Item Catalog composite route is defined in
`../item-catalogs/references/test-only-composite-batch.md`. It cannot apply to
another setup task, a production environment, general-use provider promotion,
or session-wide authorization. It does not change Core Data Loader behavior.

## Failure Classes

| Failure class | Examples | Required behavior |
|---|---|---|
| input_validation | Missing row field, unsupported operation, duplicate key, invalid date or flag | Stop before publication |
| catalog_or_metadata_mismatch | Wrong task, metadata, member, header, stale or incomplete current evidence | Obtain and review fresh task evidence |
| artifact_persistence | Unsafe path, corrupt ZIP, overwrite conflict, write failure | Preserve existing files and stop |
| approval_blocker | Proposal or package approval presented as Data Loader submission approval | Build a new immutable Data Loader preview and request separate approval |

The task-specific builder never retries, authenticates, uploads, initiates,
polls, or modifies Fusion.
