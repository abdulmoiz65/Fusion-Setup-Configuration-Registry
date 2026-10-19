# Questionnaire HDL metadata discovery

Use this procedure for every Question Library, Questionnaire Templates, and
Questionnaires HDL contract resolver, including create, copy, update, and
status-only inactivation. It separates pillar-authored discovery from the
unchanged shared Data Loader validation. It does not introduce a new load route.

## Pillar-owned read-only discovery

1. Use the task's declared `resolve_*_hdl_contract` lookup and its exact
   `*_business_object_filter` through `core.fusion-api.rest-api-client`.
   Read that client's standard Fusion REST instructions first. Send `GET` to
   `/hcmRestApi/resources/latest/dataLoaderBusinessObjects` with repeated
   `--query` options for `finder=findDataLoaderBos`, the entire `q` expression
   as one value, `onlyData=false`, `limit=500`, and the current `offset`.
   Link-bearing discovery is mandatory: `onlyData=true` can suppress the
   returned item links needed to resolve the authoritative detail contract.
   Include `--header "REST-Framework-Version=9"` on every request.
2. Do not add a `ProductAreaCode` predicate to pillar-authored requests. Product
   area is not a portable Question, QuestionnaireTemplate, or Questionnaire
   key. Never ask the user to supply it to create, copy, update, or inactivate
   one of these objects.
3. Follow every filtered page until `hasMore=false`, using the actual returned
   row count to advance offset. Non-advancing repeated whole pages, missing
   completion evidence, malformed items, or an empty page with `hasMore=true`
   block the lookup. Deduplicate only byte-equivalent repeated rows across
   otherwise progressing pages.
4. Apply the task's exact case-sensitive discriminator/template rule after
   pagination, then group matching rows by the nonblank tuple
   `(BusinessObjectId, BusObjTopDiscriminator)`. That tuple is the business
   registration identity. Rows with the same tuple but different `TemplateId`,
   `UcmContentId`, or timestamps are technical template references for one
   registration and are not ambiguity. Zero identities, a candidate with no
   complete identity, or multiple distinct identity tuples blocks. Broad
   `LIKE` matches remain discovery candidates only; translation artifacts
   require their own exact registration.
5. Run the pillar-local
   [HDL metadata resolver](../scripts/resolve_hdl_metadata_registration.py)
   with `discover` against the complete saved page responses. Follow only its
   selected returned `canonical`
   link, or its `self` link when no canonical link was returned. Run
   `verify-detail` against that response and require the detail to repeat the
   selected BusinessObjectId, establish the exact case-sensitive discriminator
   and filename, and identify the current `TemplateId` and `UcmContentId`.
   Never choose a finder row as current by first occurrence, greatest ID, or
   newest timestamp. Require current component, attribute, user-key, mandatory,
   operation, and fresh UCM DAT-template evidence. Missing or conflicting
   evidence blocks DAT generation; a sample DAT is not a substitute. Keep
   IDs/links transient and retain sanitized evidence and hashes in the task's
   existing validation result.

The standard REST client supports this explicit query. The shared Data Loader
metadata helper does not expose a custom `q` option; do not instruct an operator
to pass this filter to that helper or invent an override argument.

## Shared-loader compatibility and final gate

The shared helper currently applies its own product-area restriction. That is
an upstream implementation limitation, not a Questionnaire business input.
The no-predicate rule above governs pillar-authored requests; it is not a
requirement to edit or reject the shared helper merely by inspecting its source.

Use the unchanged `core.data-loader` metadata/schema validation for the exact
discriminator, with its normal live checks. Compare its resolved registration
with the pillar discovery result in the same target, retaining BusinessObjectId
and case-sensitive discriminator transiently for comparison, not merely display
name. Reconcile the registered filename, template hash, and relevant component
and operation contract; an unresolved identity or contract difference blocks.
Continue only if both resolve the same single exact registration and its current complete contract
passes. A product-area predicate in the helper's implementation alone is not a
blocker and does not invalidate an otherwise successful validation.

Do not patch or monkeypatch core, inject a query-rewriting transport, fake a
registration, supply a cached schema as live evidence, or reproduce upload and
initiation in this pillar. In particular, this resolver requires no change to
`core/runbook`, `core/data-loader`, or a repository-level schema, and it must not
add questionnaire-specific fields to project Run Book state. Shared
helper-owned detail/schema requests remain owned by core; the pillar
returned-link rule is not a request to rewrite them. Core's normal live
revalidation, Task Hook checks, immutable preview, standalone approval, and
unchanged-artifact verification remain mandatory before upload.

## Result classification

| Pillar discovery | Shared-loader result | Action |
|---|---|---|
| One exact complete registration | Same exact registration and valid live schema | Continue normal task validation; no ProductAreaCode question or source-inspection blocker |
| One exact complete registration | No exact registration | Block with `shared_loader_registration_mismatch`; report that pillar discovery found the object but the shared lookup did not. Do not claim that the object is unregistered. Identify filter exclusion only when returned evidence proves it; otherwise record the cause as unresolved. |
| One exact complete registration | Different or ambiguous registration, incomplete schema, failed request, or invalid payload | Block at the actual failed gate; do not replace core evidence with pillar evidence |
| Zero or multiple exact registrations, failed request, or incomplete pagination | Any | Block at pillar discovery; a narrower shared lookup cannot override this result |

For a mismatch, record the expected discriminator/template, target, discovery
scope/completion, sanitized exact-match counts, shared-helper outcome, and
failure class in the existing validation diagnostic. Preserve auth/authz,
transport/environment, and Fusion API errors instead of relabeling them as
missing registrations. Use `catalog mismatch` only for an observed registration
or contract mismatch. Do not claim the entire unfiltered catalog was searched.

A registration genuinely excluded by the unchanged shared helper cannot be
loaded through this workflow using pillar edits alone. Stop before generation
or upload when this is known. Resolving that upstream limitation requires an
approved shared-helper enhancement or target-side correction outside this
change; do not retry a live load or bypass the final gate.
