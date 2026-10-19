# Item Catalogs Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| capture_item_catalog_supplied_configuration | Supplied catalog values require normalization | Direct values, blank-template rows, or readable existing files with exact provenance and confirmed mappings | Preserve the complete supplied set. Do not infer optional values, discover business purpose, or suggest comparable configuration. | proposal_scope; proposed_values; assumption_ledger; exclusions; source_references | Ask only for missing required values or ambiguous mappings; keep the set non-executable until confirmed. |
| find_complete_item_catalog_evidence | Exact-identifier review, duplicate review, configuration readiness, or catalog-only package preparation is requested | Approved request and optional fresh complete exact-target export | Match catalog identity by exact `(ContextName, ContentValueSetCode)`, compare `ValueSetName` and `ValueSetDescription`, and separately detect a normalized catalog-name collision within the owning Content Type | exact_key_contract_reference; evidence_fingerprint; target_identity; freshness_status; completeness_status; exact_matches; name_collision_count; missing_values; comparison_evidence | Unavailable export prevents exact claims but does not block import under ../references/optional-export-policy.md; record skipped/failed and unverified checks. Known matches/collisions still block create. |
| resolve_item_catalog_rating_model | A Rating Model is applicable to review and an approved resolver contract exists | Approved business rating requirement plus complete authoritative Rating Model evidence | Require one exact portable Rating Model key and return only a source-supported value accepted by the task contract | rating_model_identity; supported_reference_value; evidence_reference | If no exact match or many matches exist, remain blocked. Never infer an ID or choose a near match. |
| verify_item_catalog_fsm_import_contract | An Item Catalog package or import is requested | Approved proposal/provider-row fingerprints, optional export or skipped/failed receipt, exact Content Type evidence, reviewed package/template, exact rows, provider registry, readiness receipt and ZIP hash; existing SKILL canary additionally supplies current parent evidence and its independent candidate registry | Validate task ORA_MANAGE_PROFILE_ITEM_CATALOG, exact members/header/metadata, grouping, blank generated/seed fields, supported scope and Core handoff. Apply ../references/optional-export-policy.md for ordinary imports. For item-catalog-existing-skill-canary-v1, apply ../references/existing-skill-catalog-certification.md and the explicit existing-skill mode: validate the supplied current evidence, exact unchanged parent and absent child, candidate registry, complete binding and approval; do not initiate an export. A reviewed-template establishes schema only. Preserve provider, supplier, classification/mapping/count/fingerprint/approval contracts. Known collisions and contradictions still block. | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; profile_v2_evidence_sha256; provider_registry_sha256; data_loader_route; catalog_set_fingerprint; catalog_set_capability; catalog_set_registry_sha256 | Invalid package, wrong task/target, unsupported fields, known collisions or changed approvals block. Missing current evidence blocks the existing SKILL canary; ordinary optional-export gaps remain nonblocking. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| item-catalog-existing-skill-canary-v1 is selected | Its supplied-current-evidence requirement takes precedence over generic optional-export continuation below. Reuse eligible evidence or stop; never automatically export, manufacture an existing parent, or substitute a new catalog. |
| Preparing an import | Skip pre-import export without attempting it; use a supplied/reusable reviewed template, record skipped status and disclose unverified target checks |
| One fully equal current catalog matches a proposed catalog create | Display the actual matched identifier and block duplicate catalog creation; do not authorize reuse. A valid unchanged parent anchor for an approved child-create route is not a proposed catalog create; validate its child and parent through verify_item_catalog_fsm_import_contract instead. |
| No exact catalog or owning-type/name collision is found and dependencies are ready | Continue to one review-only proposal or, on a separate approved package run, catalog-only package preparation |
| Current evidence is stale, partial, unbound, schema-only, or not populated | Treat it as evidence-unavailable, not as an empty catalog |
| No complete evidence is supplied for an otherwise clear outcome | Exact classification remains unavailable. A separately requested import may continue with disclosed gaps under the optional-export policy. |
| Rating Model resolution is unavailable or ambiguous | Stop the affected rating-description review; do not package that row |
| A catalog-only package passes the exact local contract | Return immutable package evidence to Task Hook; do not upload from this task rule |
| The package, release, target, evidence, baseline, provider rows, or SHA-256 changes | Invalidate readiness and require a new package and Data Loader preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IC.CHECK_EXACT_EXISTING | decision | 3 | evaluate_result | exact->IC.RETURN_EXACT_DUPLICATE;not_found->IC.ENFORCE_DESIGN;multiple_exact->IC.RETURN_BLOCKED;evidence_unavailable->IC.ENFORCE_DESIGN | IC.CHECK_DEPENDENCIES | stop | Proposed catalog-create identities are evaluated, not unchanged parent anchors in child-create routes; those route through verify_item_catalog_fsm_import_contract. Unavailable optional export continues only where the selected capability permits it. |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
