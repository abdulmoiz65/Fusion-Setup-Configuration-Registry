---
skill_id: "hcm.hcm-tool.profile-management-data-load-migration-and-maintenance"
name: "Profile Management Data Load, Migration, and Maintenance Implementation Guidance"
description: "Prepares, validates, and—after explicit approval—routes one complete supported Profile Management data set through HCM Data Loader."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Data Load, Migration, and Maintenance"
functional_area_code: "CUSTOM_PROFILE_MANAGEMENT_DATA_LOAD_MIGRATION_AND_MAINTENANCE"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "profile_management_data_load_migration_and_maintenance_scope"
  - "profile_management_data_load_migration_and_maintenance_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "profile_data_set_validation_result"
  - "immutable_execution_preview"
  - "approved_execution_preview"
  - "data_load_result"
  - "readback_comparison"
  - "traceability_record"
depends_on:
  - "core.data-loader"
  - "shared.validation.setup-data-validator"
  - "shared.implementation-planning.task-dependency-resolver"
uses_core:
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-data-load-migration-and-maintenance/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-data-load-migration-and-maintenance/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-data-load-migration-and-maintenance/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Prepares and validates supported Profile Management HCM Data Loader artifacts."
  - "Submits an approved HCM Data Loader artifact only through core.data-loader after approval of the final immutable preview."
required_privileges:
  - "Read access required to validate target dependencies and exact target state."
  - "HCM Data Loader upload and initiation privileges only when execution is separately approved."
---

# Profile Management Data Load, Migration, and Maintenance Implementation Guidance

## Purpose

Prepare, validate, and—only after final-preview approval—execute one complete supported person-profile, model-profile, or included content-library data set through HCM Data Loader.

## When to Use

Use when an implementation consultant must create, update, migrate, mass-maintain, translate, attach, synchronize, or validate Profile Management-owned data. Keep a profile root and all required child, relationship, translation, extra-information, flexfield, and attachment rows together as one request.

Do not use this skill to design Profile Types, Content Sections, Content Library definitions, or Rating Models; configure or test downstream products; delete data; write through REST; or infer missing business values.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Profile Management Data Load, Migration, and Maintenance` (`CUSTOM_PROFILE_MANAGEMENT_DATA_LOAD_MIGRATION_AND_MAINTENANCE`)

## Supported scope

Artifact-enabled routes are deliberately limited to the target-confirmed
`Talent Profile` root and `Talent Profile Translation` sections. The following
documented concepts can be accepted as intake but are provider-blocked for
artifact generation until their exact downloaded target templates and metadata
contracts are retained: Content Item, Content Item Relationship, Content Item
Translation, Content Item Rating Description Translation, Talent Model Profile
Extra Information Translation, standalone Model Profile Extra Information, and
Profile Attachment.

Use [dependency handoffs](references/dependency-handoffs.md) to determine the
owning skill, required exact evidence, and fail-closed behavior for every
Profile Management prerequisite. This skill consumes those prerequisites; it
does not configure Profile Types, content sections, content library, rating
models, flexfields, attachment foundation, search operations, or security.

`ContentItemTranslation` returned a metadata-detail HTTP 500, and no exact
registered discriminator was returned for rating-description or model-extra-
information translations. Content Item is a separate HDL root family with
Value Set ID and Value Set Name; it is not inferred as a `TalentProfile`
`ProfileItem` section. Treat all of these routes as provider-blocked until the
Talent Management business object is refreshed, the applicable files are
downloaded, and preflight succeeds; do not invent a standalone HDL object name
or field mapping.

Conditional operations are `Enable and Deploy HRT_PROFILE_ITEMS Context`,
`Validate ATTRIBUTE_CATEGORY`, supported attachment processing, `Update Profile
Search Keywords`, `Synchronize Profile Search Keywords Index`, and (only when
needed) `Optimize Profile Search Keywords Index`. Each remains blocked until
its dependency status, immutable preview, explicit approval, monitoring
contract, and supported readback are available. Do not schedule any search
process merely because a load completed.

HCM Spreadsheet Data Loader is documented by Oracle but is explicitly
unsupported by this implementation. Its spreadsheets are intake templates only;
this skill has no HSDL workbook execution client. Approved writes route only
through `core.data-loader`.

This functional area has no effective-catalog setup tasks. The FusionApps resource-authoring workflow cannot create `ora-resource` files because its required task-representation resolver has no setup-task target; no invalid resource registry is generated.

## Inputs

- `implementation_objective`
- `project_context`
- `profile_management_data_load_migration_and_maintenance_scope`
- `profile_management_data_load_migration_and_maintenance_requirements`
- `target_environment`
- `requested_operation`
- `profile_data_source`
- `explicit_final_preview_approval`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `profile_data_set_validation_result`
- `immutable_execution_preview`
- `approved_execution_preview`
- `data_load_result`
- `readback_comparison`
- `traceability_record`

## Execution workflow

1. Preserve the supplied source under its SHA-256-prefixed name and determine the target environment, operation, root record type, and supported object set. Accept direct input, a standard spreadsheet, or a readable supplied file. For CSV, report unmapped columns as a mapping-review uncertainty and fail closed; do not invent values from unreadable or ambiguous content.
2. Validate the complete request with `scripts/profile_management_data_set.py`. It is a local, no-network contract check and cannot upload, initiate, or modify Fusion data.
3. Confirm required fields, identifiers, parent/child references, translation language values, attachment constraints, `HRT_PROFILE_ITEMS` context status, and owning-skill dependencies. For every model-profile artifact, require owner-provided evidence of the selected Profile Type, every requested enabled additional-information flag, each active Section ID/Name, and each applicable Value Set. For a future `ProfileItem` route, use the live `FLEX:HRT_PROFILE_ITEMS` metadata and a deployed context field; do not treat `ATTRIBUTE_CATEGORY` as a confirmed template attribute. For every translation row, resolve the supplied language against the target's installed-language LOV and use only the returned canonical `LanguageCode`. Revalidate after every change.
4. Obtain an exact documented target result. Stop creates on an exact existing record; require exactly one target for update or mass maintenance; stop a colliding migration unless approved reconciliation behavior is documented. Never use fuzzy matching, implicit upsert, deletes, or child removal.
5. Present the entire immutable preview: source reference, target, operation, object set, mappings, supplied and omitted optional components, validation and target-check results, dependency state, conditional actions, and exclusions.
6. Obtain explicit approval immediately before persistence. A prior instruction, file upload, silence, or approval of an incomplete preview is not approval.
7. For a model-profile import, first resolve an approved AI Studio workflow agent whose declared capability exactly covers the selected operation, object set, immutable-preview approval, monitoring, and supported readback. Use that agent only when its provider contract proves it will use a supported HCM Tool execution surface and preserves the same approval boundary. If no such agent is available, route the approved artifact only through `core.data-loader`. Do not call REST writes, direct database access, ADF/Redwood/browser automation, or an independent migration client.
8. Monitor to a terminal result, perform supported readback, compare it with the approved preview, and report every discrepancy. Do not claim verified success without readback.

## Validation and safety

- Use only artifact-enabled sections with a retained target template and selected operation's documented fields and keys. Do not convert a documented concept into an HDL section without that evidence.
- Do not infer profile values, content, identifiers, dates, mappings, relationship rows, translations, flexfield values, or attachment metadata.
- Treat Profile Rating Model Configuration, Profile Management Content Library Configuration, Profile Types and Content Section Configuration, Data Load and Migration Foundation, Application Attachment Foundation, Application Flexfield Foundation, and Background Process Foundation as owned dependencies.
- Persist only redacted source references, fingerprints, mappings, validation outcomes, preview/approval state, execution identifiers, and readback comparison. Never persist credentials, tokens, full payloads, or unnecessary person-profile data.
- On a failed job, retain sanitized process status and errors. Never retry upload, import, deployment, attachment processing, or synchronization without idempotency or new explicit approval.
- Treat an unavailable, ambiguous, or incomplete AI Studio workflow capability as a provider-readiness blocker and fall back to the approved HCM Data Loader path; never infer an agent name, endpoint, or execution contract.

## Preflight

Before any Fusion-changing action, confirm the environment identity, requested operation, supported HDL object set, readable source, exact target result, required dependency readiness, required privileges, immutable artifact path, and whether the request is validation, preview, or live execution. Stop on an unsupported object, ambiguous mapping or target, missing prerequisite, unsafe path, destructive request, or missing final-preview approval.

## Failure handling

Classify durable failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`.

Retry only bounded read-only transport calls, and refresh a managed cached token once after a 401 or 403. Never retry a live HCM Data Loader upload, initiation, deployment, attachment operation, or synchronization without idempotency or fresh explicit approval. On timeout, stop and persist the environment, operation, ProcessId or requestId, last status, elapsed wait, and one safe next-check path. On terminal failure, retrieve available sanitized process logs or status diagnostics; preserve partial results in an `errors` array and do not report success.

## Local contract and tests

`schemas/profile-management-data-set.schema.json` defines the sanitized request shape. Run the local validator with:

```text
python scripts/profile_management_data_set.py path/to/request.json
```

Add `--require-final-approval` only to verify that a completed immutable preview carries explicit approval. This command is local and never sends a request to Fusion.

### Three supported intake modes

1. **CSV export/import:** use the documented CSV interchange template to capture or exchange a complete request. It is not an HDL payload and cannot be submitted to Fusion directly.
2. **Guidelines and templates:** provide the default spreadsheet intake or the CSV interchange template, together with supported-object and identifier guidance. Do not require a business justification.
3. **Business-intent guidance:** accept a business-language request only to explain the skill boundary, identify dependency owners, and offer the intake template. Do not recommend profile design, Profile Types, Content Sections, Rating Models, content items, or downstream configuration.

### AC2 conversational intake resolution

Use the local AC2 resolver for a consistent non-authorizing response to broad
direct-entry, template, CSV-export, and CSV-import phrasing. It returns the
selected intake mode, supported scope, provider-blocked objects, outstanding
inputs, the safe next action, and `no load initiated`. A template request
returns the default XLSX template path and concise Request/Records guidance;
the caller attaches that existing workbook to the user-facing response.

```text
python scripts/ac2_prompt_resolution.py "Give me an Excel template for a model profile"
python scripts/ac2_prompt_resolution.py "Validate this CSV" --source path/to/intake.csv --preserve-source-dir path/to/evidence
```

See [AC2 prompt outcomes](references/ac2-prompt-outcomes.md) for supported
phrasing and expected non-authorizing outcomes.

Create a CSV template locally with:

```text
python scripts/profile_management_data_set.py --create-csv-template path/to/profile-management-intake.csv
```

Import and validate a completed CSV locally with:

```text
python scripts/profile_management_data_set.py --import-csv path/to/profile-management-intake.csv --output-json path/to/request.json
```

Use [test prompts](references/skill-wiki-test-prompts.md) for the documented acceptance-test conversations.

The default fillable spreadsheet intake is [profile-management-data-load-intake.xlsx](templates/profile-management-data-load-intake.xlsx). It captures request metadata and repeating supported records, but is not an HDL payload or execution authorization. Mapping review records the live `TalentProfile` section, parent `ProfileCode`, language lookup requirement, DFF-context requirement, attachment metadata requirement, provider-blocked route, or `confirmation-required` state; it must not invent unresolved HDL child attributes.

For human-authored DOCX, PDF, TXT, or Markdown, accept either a structured JSON request or a narrow key/value form with request metadata followed by supported object headings and `Key: Value` rows. Unrecognized prose is reported as a confirmation-required source uncertainty.

### Translation-language preflight

Before generating a translation DAT, resolve the supplied language in the target environment. This is a read-only call to the documented installed-language LOV and does not upload or initiate a load:

```text
python scripts/resolve_installed_language.py --language-code es --token-cache auto --no-open-browser
```

Use `canonicalLanguage` from a `resolved` response in the DAT `Language` field. A `blocked` response means the language is absent, not fully installed, or ambiguous in that environment; do not create a replacement archive until a valid target language is supplied or installed by the language-setup owner.

For a controlled test-language choice, list the fully installed target values without changing Fusion:

```text
python scripts/resolve_installed_language.py --list-installed --token-cache auto --no-open-browser
```

### Child dependency preflight

Before preparing a child archive, use the documented read-only resolver for an
exact Profile Type Section or Content Item match. It never uploads or initiates
a load:

```text
python scripts/profile_dependency_preflight.py --dependency profile-content-section --profile-type-id <returned-profile-type-id> --section-name <exact-section-name> --token-cache auto --no-open-browser
python scripts/profile_dependency_preflight.py --dependency content-item --content-item-id <returned-content-item-id> --content-item-name <exact-content-item-name> --token-cache auto --no-open-browser
```

The resolver fails closed on zero or multiple matches. Profile Type codes are
not mapped to numeric IDs by this skill: obtain the exact code/ID pair from
the owning Profile Types configuration and retain it in the model-profile
configuration evidence. `HRT_PROFILE_ITEMS` DFF
context/value, attachment data type, and model-profile relationship-target
routes remain blocked until their owners publish an exact supported read-only
contract. Do not substitute an inferred endpoint, UI automation, or database
query.

Before enabling an artifact route, confirm its exact target Data Loader schema
with the child-schema preflight. A `blocked` response is a provider or template
contract blocker, not permission to infer an HDL section or field mapping:

```text
python scripts/profile_child_metadata_preflight.py --selection talent-profile-translation --token-cache auto --no-open-browser
```

### Exact target preflight

Before a create, update, migration, or artifact preview, perform a read-only
exact ProfileCode lookup. Use the returned `status` as the request
`target_check.status`: `not-found` permits a create, `exactly-one` is required
for update or mass maintenance, and `ambiguous` blocks all artifact work.

```text
python scripts/profile_exact_match.py --profile-code <exact-profile-code> --token-cache auto --no-open-browser
```

For a model-profile artifact, first validate the exact evidence obtained from
the owning Profile Types and Content Section capability. This is local and
never contacts Fusion:

```text
python scripts/profile_dependency_preflight.py --dependency model-profile-configuration --model-profile-evidence-json path/to/model-profile-configuration-evidence.json
```

The evidence must contain an exactly-one Profile Type code/ID, each requested
additional-information flag with `enabled` status, each requested active
Section ID/Name, and exactly-one applicable Value Set evidence or an explicit
`not-applicable` value, plus an owner, source reference, and observation time.
The resulting resolved evidence and its SHA-256 must be supplied as
`model_profile_configuration`; artifact preparation verifies that it matches
the Talent Profile root before producing a preview.

### Approved-versus-saved Talent Profile readback

After a terminal-success Talent Profile load, compare the approved DAT with a
read-only exact Fusion profile query. The comparison is verified only when the
query returns exactly one profile and every approved field is returned and
matches. Missing or unreadable fields leave AC6 not verified; they must never
be treated as a match.

For GROW-8164 AC6 model-profile root verification, use the dedicated read-only
HCM Extract contract in
[`references/fscr-grow-8164-ac6-model-profile-readback-extract.md`](references/fscr-grow-8164-ac6-model-profile-readback-extract.md).
It is the AC6 evidence path when the approved DAT contains fields outside the
documented `profilesLov` response. Compare the immutable approved DAT with its
one-profile CSV output using:

```text
python scripts/profile_root_extract_readback_comparison.py --approved-dat path/to/TalentProfile.dat --extract-csv path/to/FSCR_GROW_8164_AC6_MODEL_PROFILE_READBACK.csv
```

The comparator requires a unique exact `ProfileCode` row and a CSV column for
every populated DAT root field. It only normalizes integer identifier values;
all other values must be exact. A missing field, empty returned value, duplicate
row, or mismatch leaves AC6 not verified.

The official model-profile read-only catalog exposes `talentProfileItemsLOV`,
which supports exact `ProfileItem` readback for its documented fields. Use:

```text
python scripts/profile_item_readback_comparison.py --profile-id <returned-profile-id> --expected-json path/to/approved-readable-profile-item.json --token-cache auto --no-open-browser
```

No supported readback contract has been established for `ProfileRelation`,
`ModelProfileExtraInfo`, `ProfileAttachment`, or `TalentProfileTranslation`.
Those routes remain unverified until a documented contract and exact fields are
available. `ProfileItem` readback is a future-route diagnostic only until the
corresponding target HDL template is confirmed.

```text
python scripts/profile_readback_comparison.py --approved-dat path/to/TalentProfile.dat --token-cache auto --no-open-browser
```

## Source basis

- HCM Tool FSCR taxonomy and HCM Tool foundation baseline
- GROW-8164
- Oracle documentation: [Uploading Talent Profile Data](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/uploading-talent-profile-data.html); [How You Upload Talent Profile Data](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-upload-talent-profile-data.html); [Using Enhanced Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/using-enhanced-talent-profiles.pdf)

Track token usage for every generated project artifact or skill-run record using the manifest policy.
