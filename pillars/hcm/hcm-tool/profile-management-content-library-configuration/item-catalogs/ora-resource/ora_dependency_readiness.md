# Item Catalogs Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplied-configuration capture | Capture direct values, blank-template rows, or a readable existing file with provenance; confirm mappings and preserve omitted optional values |
| 2 | Proposal ownership | Require supplied catalog objects and confirmed ownership; no business-purpose discovery |
| 3 | Exact-key contract | Use `(ContextName, ContentValueSetCode)` for catalog identity and `(ContextName, Name, ContentValueSetCode)` for the narrow child |
| 4 | Optional current evidence | Use complete target evidence for exact claims; skipped/failed export is nonblocking for import with disclosed gaps |
| 5 | Content Type and Profile V2 evidence | Resolve owning Content Types; unavailable export-based Profile V2 proof must not be claimed as verified |
| 6 | Content Item FSM provider | For one catalog-owned Content Item, require the packaged provider registry, eligible lifecycle, exact anchor, and approved supplier |
| 7 | Rating Model reference | Resolve an exact approved Rating Model only for review of catalog-specific rating descriptions; those rows remain non-executable |
| 8 | Provider readiness | For a separate package request, require the local FSM package receipt and mandatory `core.data-loader` handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_skill_canary_provider | Existing custom SKILL catalog certification | Conditional | item-catalog-existing-skill-canary-v1 is explicitly selected | Verify | Supplied same-target current evidence, candidate registry and authenticated non-production target evidence under ../references/existing-skill-catalog-certification.md | verify_item_catalog_fsm_import_contract | This controlled test must prove the existing parent; generic optional-export continuation does not waive that prerequisite | Require the existing-catalog certification binding; missing evidence stops without export. This scoped dependency takes precedence over generic optional-evidence guidance. | catalog_set_fingerprint; catalog_set_capability; catalog_set_registry_sha256; parent_anchor_key; target_evidence_reference |
| supplied_configuration_capture | Source-backed supplied Item Catalog configuration | Yes | Direct values, a blank template, or an existing file is supplied | Verify | Supplied values with exact source provenance, confirmed mappings, and source-backed field semantics | capture_item_catalog_supplied_configuration | The complete supplied set and mappings must survive intake; optional values must not be inferred | Return one complete review-only set or a precise missing-value/mapping question | proposal_scope; proposed_values; assumption_ledger; exclusions |
| approved_item_catalog_exact_key_contract | Approved source-backed catalog provider-key contract | Conditional | Exact-identifier review, duplicate review, configuration readiness, or catalog-only package preparation is requested | Confirmed | Fusion migration `UserKey` and populated task export | find_complete_item_catalog_evidence | Catalog identity is `(ContextName, ContentValueSetCode)`; child keys do not authorize child mutation | Use only the catalog key and compare all approved catalog business fields | catalog_exact_key_contract; contract_source |
| complete_item_catalog_evidence | Complete current Item Catalogs evidence | Conditional | Exact current-state claims are requested; not required merely to import | Verify | Workflow-approved complete current-state read bound to the exact target | find_complete_item_catalog_evidence | An unbound, stale, partial, or schema-only artifact cannot establish current state | Record skipped/failed export and continue import checks; exact classification remains unavailable | evidence_path; target_identity; evidence_fingerprint; freshness_status; completeness_status |
| exact_content_type_reference | Exact owning Content Type and evidence fingerprint | Conditional | A catalog, anchored-child or explicit controlled new-set package is requested | Verify | Approved Content Type evidence | verify_item_catalog_fsm_import_contract | The provider resolves `ContextName`; a guessed context can attach the catalog to the wrong type or fail | Resolve every proposed context exactly and bind the evidence fingerprint | content_type_contexts; content_type_evidence_fingerprints |
| profile_v2_readiness | Optional indirect Profile V2 export preflight | Conditional | Current-state export is available | Verify | Fresh populated same-target export when supplied | verify_item_catalog_fsm_import_contract | Profile V2 is a product feature gate; export is an indirect observation, not an import transport prerequisite | Bind valid export evidence when present; otherwise allow null profile_v2_evidence_sha256 and disclose unverified preflight | profile_v2_evidence_sha256; evidence_fingerprints |
| exact_rating_model_reference | Exact Rating Model reference and supported task value | Conditional | Catalog-specific rating descriptions are reviewed | Verify | Approved Rating Model evidence | resolve_item_catalog_rating_model | Choosing an ID or similarly named model would invent configuration | Obtain one exact portable model match; do not package the rating-description row | rating_model_identity; supported_reference_value; evidence_reference |
| catalog_content_item_provider | Source-backed Item Catalog Content Item FSM provider | Conditional | One catalog-owned Content Item is requested | Verify | Registered lifecycle, supplier contract, supplied exact parent values and optional current evidence | verify_item_catalog_fsm_import_contract | The root graph contains base children and commits before later translation handling; the child value set resolves from its parent logical row | Validate supported context/fields; reject known collisions; disclose unavailable duplicate and parent comparisons | provider_registry_sha256; lifecycle; parent_anchor_key; supplier_code; child_provider_key |
| new_catalog_set_provider | Separate complete new catalog set capability | Conditional | Explicit new-set mode is requested | Verify | Separate registry, complete proposal, authenticated target, controlled non-production classification and optional current evidence | verify_item_catalog_fsm_import_contract | Parent logical-row resolution supports controlled testing but does not establish runtime certification | Validate intended-new parent and all children with mapping/count/fingerprint/approval contracts; no absence claim without evidence | catalog_set_fingerprint; catalog_set_capability; catalog_set_registry_sha256; target_evidence_reference |
| mutation_provider | Approved Item Catalogs create-only FSM provider | Yes | Catalog creation or import is requested | Verify | Approved fingerprints, optional export receipt, exact Content Type evidence, reviewed package/template and immutable receipt | verify_item_catalog_fsm_import_contract | The local builder owns catalog, narrow child or explicit controlled new-set package preparation and `core.data-loader` owns Task Hook, preview, approval, upload, and initiation | Apply optional-export policy plus remaining package/Core checks; no direct mutation fallback | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Proposal-ready | Ownership is unambiguous but approved values or complete evidence are not yet supplied | Preliminary scope proposal only; no exact or create claim |
| Satisfied | Required package/Core checks pass and optional export gaps are disclosed | Exact claims only with sufficient evidence; import only through core.data-loader |
| Needs evidence | Required Content Type, package format or target/access evidence is missing or invalid | Block dependent required checks; skipped/failed optional export is disclosed and does not itself block import |
| Blocked | Evidence, dependencies, package validation, or an unsupported rating-description/advanced-child/mutation route is unresolved | No affected exact/configuration-ready claim or create action |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IC.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->IC.CHECK_EXACT_EXISTING;proposal_only->IC.ENFORCE_DESIGN;import_ready->IC.VALIDATE_FSM_IMPORT;rating_model_unresolved->IC.RETURN_BLOCKED;unsupported_child_rows->IC.RETURN_UNSUPPORTED;unsupported_mutation->IC.RETURN_UNSUPPORTED;blocked->IC.RETURN_BLOCKED | IC.CAPTURE_CONFIGURATION | stop | A supported Item Catalogs proposal, catalog-only create request, phase-one anchored Content Item request, or explicit controlled new-set request has been normalized |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Tool FSCR taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-tool-fscr-taxonomy/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
