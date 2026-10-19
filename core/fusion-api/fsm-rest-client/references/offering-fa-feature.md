skill_id: "shared.implementation-planning.offering-fa-feature-catalog"
name: "Offering FA Feature Catalog"
description: "Fetches the Oracle Fusion offering hierarchy: offerings, functional areas, and features under offerings and functional areas, with product, classification, navigation path, and dependency release availability. Use when the user asks to browse this catalog or export the complete hierarchy."
layer: "shared"
pillar: "Cross-pillar"
type: "export"
execution_mode: "automated"
owner_team: "FSCR implementation platform"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "offering_short_name (optional)"
  - "preview_limit (optional; default 25)"
  - "full_export_request (optional)"
  - "project_id (optional)"
outputs:
  - "hierarchy_preview"
  - "hierarchy_csv (when full export is requested)"
  - "diagnostics"
depends_on:
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.fusion-api.rest-api-client"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Performs read-only Fusion BOSS API calls."
  - "Writes a CSV only when the user explicitly requests the entire list."
required_privileges:
  - "BOSS read access to Common Setup Features."

# Offering FA Feature Catalog

Use this skill to browse or export the hierarchy represented by the
`Offering_FA_Features` report:

`OFFERING`, `FA_FEATURE`, `PRODUCT_FAMILY`, `PRODUCT`, `CLASSIFICATION`, `PATH`,
`FOF_AVAILABLE_RELEASE_VERSION`, and `FOF_EXPIRATION_RELEASE_VERSION`.

## Retrieval rules

1. Enumerate all offerings only with the `availableOfferings` data-object view.
2. For each selected offering, call the functional-area and feature hierarchy
   extractions described in the API contract below.
3. Preserve the extraction relationships and use display names for offering,
   FA/feature, and path values. Use dependency release values when available.
4. Complete the selected offering hierarchy retrieval before enrichment. Enrich
   only returned feature codes, in batches of at most 50, and emit scoped
   progress to stderr before enrichment begins.
5. Default output is a compact preview (25 rows unless the user specifies a
   different limit). Show representative rows and counts, not the full list.
6. Only when the user asks for the entire list, use `--all` to fetch all pages and write a CSV
   under the supplied project workspace (or the caller's explicitly supplied
   output path). Use the exact report column names above.

## Execution

Run the bundled script through the shared BOSS OAuth configuration:

```bash
  python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature.py \
  --properties core/auth/fusionEnv.properties \
  --preview-limit 25
```

For a complete export:

```bash
  python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature.py \
  --properties core/auth/fusionEnv.properties \
  --all \
  --project-id <project_id>
```

For long-running environments, split the complete export into resumable
offering batches:

```bash
  python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature.py \
  --properties core/auth/fusionEnv.properties \
  --all \
  --skip-metadata-enrichment \
  --skip-dependency-enrichment \
  --offering-offset 0 \
  --offering-limit 10 \
  --project-id <project_id> \
  --verbose
```

After all numbered batch CSVs are present in one directory, merge them with
the same script (no Fusion connection is made during merging):

```bash
python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature.py \
  --merge-batches-dir <batch_directory> \
  --output <merged_output.csv>
```

Use the BOSS token (`boss_scope`) and the separate BOSS token cache. Never print
tokens, credentials, or authorization headers. Review the API contract below
before changing endpoint behavior.

## API contract

All calls use the BOSS base URL and `boss_scope`.

| Purpose | Method and endpoint |
|---|---|
| Offering enumeration (only source for the offering list) | `GET /api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings` |
| Functional areas under an offering | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/availableFunctionalAreasByOffering?parentShortName={offering}` |
| Full offering/FA/feature navigation hierarchy | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/availableFeaturesByOffering?parentShortName={offering}` |
| Product and feature metadata | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchFunctionalAreas` and `searchFeatures`, filtered by returned `featureShortName` batches |
| Dependency release enrichment | `GET /api/boss/data/objects/ora/commonSetup/features/v1/dependencies?$filter=availableFlag=true and feature.featureShortName in (...)` for returned-code batches |

`availableOfferings` is the tested view path from the FSM BOSS source:
`features/$views/availableOfferings`. It returns only available root offerings
(`ROOT_NODE`/`OFFERING`) and is sorted by `featureName`.

The extraction flow preserves the prior API behavior. Display names are mapped
from the returned feature names, and code-based path segments are replaced with
their corresponding display names. Dependency release values map to
`availableReleaseVersion` and `expirationReleaseVersion`; the CSV aliases these
to `FOF_AVAILABLE_RELEASE_VERSION` and `FOF_EXPIRATION_RELEASE_VERSION`.

The client should pass `$limit` and `$offset` for pagination, preserving `$` in
query parameter names. `$en` is the locale segment for extraction/data-object
calls where the endpoint contract requires it.

## Failure handling

Classify failures as input validation, authentication/authorization, transport,
Fusion API, pagination, product-enrichment, dependency-enrichment, or artifact
persistence failures. Retry a 401/403 once after refreshing the BOSS token;
do not retry other calls automatically. A partial export must include an errors
array and must not be presented as a complete catalog.

Some BOSS collection endpoints return a zero-byte body for a terminal page
instead of an empty JSON collection. Treat only that empty JSON-decoding
response as end-of-results; surface non-empty malformed responses as actionable
API errors.
