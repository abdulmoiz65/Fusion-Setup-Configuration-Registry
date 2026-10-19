# Content Items Read-Only Catalog REST Execution

## Purpose

Define the registered, GET-only evidence route used when an enhanced-profile
Content Type is not completely represented by the Content Items FSM export.
This route supports duplicate classification and post-load readback. It never
authorizes ContentItem V2 HDL creation for a context merely because Fusion
advertises a child link.

## Provider Registry

The machine-readable registry is
[`../references/content-item-rest-provider-registry.json`](../references/content-item-rest-provider-registry.json).
The registry binds the parent resource to an ordered, source-backed list of
REST API version candidates and a bounded capability query. Each context entry
then binds one exact `ContextName` to one child relation, an exact
catalog-template selector, trusted-release certification states, and ownership
restrictions.

- A `discovery-required` selector permits only parent catalog discovery. It
  blocks the child GET and every create route.
- A `registered` selector permits the exact child GET for its release.
- `read_certification.status` and `hdl_create_certification.status` are
  independent. Read support never upgrades create support.
- `read_certification.reason` records the release-bound evidence boundary. A
  `read-only` route may safely classify exact codes while still lacking an
  independently compared positive result or a code on every row.
- Live catalog codes, catalog names, opaque keys, customer rows, and target URLs
  do not belong in the checked-in registry.
- A REST API version is a capability selector only. It is never evidence of a
  quarterly Fusion release.

## Read-Only Adapter

Run the adapter from the repository root with Python 3.10 or newer; Python
3.11 or 3.12 is recommended:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/scripts/talent_content_item_catalog_adapter.py capability

python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/scripts/talent_content_item_catalog_adapter.py check \
  --context <EXACT_CONTEXT> \
  --content-item-code <EXACT_CODE>

python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/scripts/talent_content_item_catalog_adapter.py resolve-create-catalog \
  --context COMPETENCY \
  --content-item-code <APPROVED_NEW_CODE> \
  --catalog-code <APPROVED_CATALOG_CODE> \
  --catalog-name <APPROVED_CATALOG_NAME>

python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/scripts/talent_content_item_catalog_adapter.py resolve-certification-catalog \
  --context <CATALOG_PROVIDER_CONTEXT> \
  --content-item-code <APPROVED_NEW_CODE> \
  --content-item-name <APPROVED_NEW_NAME> \
  --catalog-code <APPROVED_CATALOG_CODE> \
  --catalog-name <APPROVED_CATALOG_NAME> \
  --provider-use certification
```

The adapter resolves target identity from the authenticated Fusion properties
used by the core REST client. Optional `--target-environment` and
`--fusion-release` values are backward-compatible expert assertions: they
must equal authenticated or trusted metadata and can never supply missing
preflight evidence. Never ask the user for either assertion.

Use `sample --context <EXACT_CONTEXT>` only during certification. It reads at
most one item per owning catalog, reports the safe field names and allowlisted
sample fields, and never claims complete duplicate coverage.

The adapter invokes `core.fusion-api.rest-api-client` and exposes no mutating
method. It does not force the Data Loader-specific REST framework header,
because the Talent Catalog response must retain Fusion's child hypermedia
links. When project-local
evidence is required, supply `--project-root project/<project_id>` and a
relative `--output` path. Both arguments are required together.

`resolve-create-catalog` is still GET-only. It runs only for an independently
create-certified registry context, resolves exactly one catalog by the
approved exact code/name pair, rejects an explicitly inactive catalog, proves
zero exact item-code matches across every owning catalog, and emits the exact
`item_catalog_evidence` shape consumed by the HDL package builder. Discovery,
exact checks, samples, and create-catalog resolution use one stable catalog
identity fingerprint.

`resolve-certification-catalog` is also GET-only. It additionally loads the
strict `content-item-catalog-hdl-provider.json` lifecycle contract, proves both
the exact code and V2 name are absent across every owning catalog, proves both
are absent from the release-matched seed catalog, enforces inactive and
context-specific catalog ownership blocks, and binds the release-fixed row
fields and supplier/Rating Model values into a fresh receipt. Certification
use accepts `certification-only` or `verified`; general use accepts only
`verified`.

## Environment and Capability Preflight

1. Load authenticated Fusion context through the existing core REST client
   configuration and emit only a sanitized environment fingerprint.
2. Never request screenshots, browser address-bar images, copied URLs, exact
   confirmation replies, or user attestations. If authenticated context is
   unavailable, return `preflight-blocked`.
3. Record quarterly release only when trusted authenticated metadata supplies
   it. Never infer `26C` from `11.13.18.05`, hostname, documentation, or
   current date.
4. Attempt only the registry-declared API candidates and their exact bounded
   GET query. Select the first structurally valid response. Authentication,
   authorization, or transport failure stops immediately; exhausted candidates
   return `capability-blocked`.
5. Require trusted release metadata only for a later release-bound provider,
   seed, certification, or create decision. A read capability receipt may
   correctly report `release_status: unknown`.

## Execution Contract

1. Complete the authenticated environment and bounded capability preflight.
2. Resolve the exact registry context and any required trusted-release
   lifecycle evidence before a child request.
3. Read and fully page the selected `talentContentItemCatalogs` parent collection.
4. Select every catalog matching the registered exact template ID and name.
5. From each selected parent item, require exactly one Fusion-returned link
   whose `rel=child` and `name` equals the registry child relation.
6. Reuse the returned path containing the opaque parent key. Never calculate,
   concatenate, decode, or persist that key.
7. Send exact single-quoted `ContentItemCode` and, for certification, `Name`
   filters; escape embedded single quotes by doubling them and recheck every
   returned value locally.
8. Exhaust every page. A missing `hasMore`, inconsistent count or offset,
   empty page with `hasMore=true`, repeated offset, or failed page makes
   coverage unavailable; never treat a partial read as zero matches.
9. Return only the requested exact rows' allowlisted comparable fields,
   catalog code/name, stable identity fingerprints, counts, certification
   states, timestamps, and a canonical evidence SHA-256. Do not return links,
   opaque IDs, full catalog rows, authorization material, or unrelated items.
10. Recursively inspect both stdout and persisted results for credential keys,
   bearer/JWT/private-key patterns, and long base64-shaped values. Fail closed
   with a sanitized diagnostic instead of rendering the material.

## Exact Result Handling

| Result | Required action |
| --- | --- |
| Zero exact matches across every owning catalog | Return `not-found`; a proposal may continue, but create remains controlled by the independent HDL certification and package workflow. |
| One exact match | Return `exact` and reuse or verify it without mutation. |
| More than one exact match | Return `multiple-exact` and stop for authoritative disambiguation. |
| Selector, catalog, child link, fields, pagination, authentication, or transport unavailable | Return a classified blocker; never claim absence. |

`ContentItemCode` is the common exact key but is nullable in some live child
responses. A successful not-found query proves the registered route and
coverage for that requested code; it does not prove that name-only rows can be
found by code. Certification therefore requires a separate exact `Name` query
and zero matches for both keys. Never fall back to fuzzy name matching.

## Read Certification Gate

Promote a context from `candidate` only after a release-bound forward test
proves its exact template mapping, child relation, bounded fields, pagination,
quoted filtering, zero/one/multiple outcome handling, wrong-catalog failure,
sanitization, and comparison to an approved product source. Store the target
evidence in the project workspace, not in this reusable skill.

## Create Certification Gate

Use `hdl_create_certification.status: certification-only` only after release
source, the live child contract, exact row fields/fixed values, dual-key
absence, release-seed absence, and catalog ownership are established. Promote
that exact context to `verified` only after one separately approved controlled
load, one fully equal exact REST readback, one fully equal fresh complete Item
Catalog export readback, and a repeated request blocked as an existing key.

The catalog-bound ContentItem V2 HDL create providers are verified for
`BEHAVIOR`, `CERTIFICATION`, `COMPETENCY`, `DEGREE`, `EDUCATION_LEVEL`,
`HONOR`, `LANGUAGE`, `MEMBERSHIP`, and `PROJECT`; no registered catalog
provider remains `certification-only`. `EDUCATIONAL_ESTABLISHMENT` stays with
its separate task; `SKILL` remains blocked only in this historical HDL contract.
Its independent [new-set FSM route](../../item-catalogs/references/skill-catalog-creation.md)
supports controlled creation of a new custom catalog and items, not Skills Center configuration. `PROJECT` uses the
source-aligned Projects template and does not authorize a free-form
`SPECIAL_PROJECT` entry. Language must use a customer-owned catalog and must
not replace a release-seeded code or name. This HDL lifecycle is independent
of the Item Catalog FSM registry and never bypasses the fresh evidence,
immutable package, Task Hook, or Core Data Loader gates.

After the routed external-read step is active, produce the pre-load receipt
with `talent_content_item_catalog_adapter.py resolve-certification-catalog` and
the exact context, item code, V2 name, catalog code, and catalog name. After a
separately approved controlled load, produce an exact REST receipt with
`talent_content_item_catalog_adapter.py check-identity`, obtain a new complete
unfiltered `ORA_MANAGE_PROFILE_ITEM_CATALOG` export from the same target, and
run `prepare_catalog_content_item_hdl_package.py verify-readback`. The verifier
fails closed on a metadata-only, filtered, incomplete, stale, wrong-target, or
differing export and never promotes lifecycle status by itself; promotion also
requires the Core Data Loader controlled-load receipt and duplicate-rerun lock.

## Error Handling

- Let the core REST client refresh one managed cached token after a 401 or 403.
  A repeated authentication response stops the route.
- Retry a read-only transport failure at most twice. Do not retry input,
  catalog, metadata, privilege, or Fusion API failures automatically.
- Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
  `auth_expired_or_invalid`, `authorization_or_privilege`,
  `transport_or_environment`, `fusion_api_error`, or
  `artifact_persistence`.
- This adapter has no polling and no Fusion write, upload, or load capability.

## Sources

- [Oracle Fusion Cloud HCM REST API - Talent Content Item Catalogs](https://docs.oracle.com/en/cloud/saas/human-resources/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
