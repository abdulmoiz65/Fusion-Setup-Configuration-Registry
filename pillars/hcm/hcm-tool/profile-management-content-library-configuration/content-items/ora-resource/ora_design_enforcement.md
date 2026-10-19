# Content Items Design Enforcement

Original GROW-8154 V1 acceptance remains FSM-only and FSM is preferred. The separately selected [verified GOAL fallback exception](../../references/verified-fallback-contract.md) may use only its verified single-row HDL provider through Core Data Loader. It is not FSM acceptance or submission approval. Other historical HDL branches remain unreachable. Exact existing identifiers stop creation, even when supplied fields are equal.
## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supplied object ownership | Route supplied Content Item fields and confirmed relationships without requiring Fusion terminology; exclude nearby task scope |
| 2 | Capture supplied values | Accept direct values, a blank template, or a readable existing file with exact provenance; no business-purpose discovery or comparable defaults |
| 3 | Build complete configuration review | Preserve the supplied complete set and source mappings; ask only for missing required values or ambiguous mappings |
| 4 | Normalize after confirmation | Resolve supported item fields, parents, and endpoints without authorizing execution |
| 5 | Report exact existing identifiers | Apply exact-match rules only after technical normalization and complete current evidence |
| 6 | Minimize and bind | Propose only missing approved values and freeze provenance, evidence, exclusions, and fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Explicit SKILL creation | Blocker | | Creation uses historical HDL, the narrow existing-parent route, production/general-use, or includes Skills Center configuration | Route the complete request to ../item-catalogs/references/skill-catalog-creation.md and its independent new-set FSM contract. Keep SKILL unchanged; do not substitute COMPETENCY. | Only via a separately reviewed new-set package |
| Every configuration-ready item proposal | Blocker | find_complete_content_item_evidence | The owning content type is missing or ambiguous | Resolve one exact owning type | Yes, before configuration readiness |
| Every inferred value | Blocker | | Value, source, sanitized evidence, confidence, materiality, or review status is absent | Complete the assumption ledger or mark the value unresolved | Yes, before proposal |
| Fusion-touching phase | Blocker | | The selected workflow's required authenticated target, privilege or capability check fails, or an attestation substitutes for actual evidence | Apply operation-scoped preflight. Require a bounded Talent Catalog GET only for REST evidence, not FSM export/loader work. Unknown quarterly metadata alone is not a blocker; preserve seed/provider compatibility at its dependent step. | No automatic fix |
| Technical Data Loader XLSX | Blocker | | Two discriminators or roots share a case-insensitive first-30-character prefix | Prefer a valid FSM route; otherwise require an explicit DAT request and create no workbook | Yes, before workbook generation |
| Existing content is considered | Blocker | find_complete_content_item_evidence | A customer export is filtered or target-mismatched, a source-backed seed catalog is invalid, multiple exact candidates remain, or a complete fresh row differs on an applicable value | Resolve both evidence layers; display actual matched identifiers and block creation on any exact match. A seed identity match does not prove full row equality | No automatic fix |
| A configuration-ready relationship is requested | Blocker | find_complete_content_item_evidence | Either endpoint, relationship meaning, or ownership is unresolved | Retain the supplied relationship and uncertainty in preliminary review; confirm exact endpoints and ownership before configuration readiness | Yes, before configuration readiness |
| Every configuration-ready proposal | Blocker | | A material value or source-to-field mapping is unresolved | Keep every supplied value and unresolved mapping visible in preliminary review; require confirmation before configuration readiness, exact claims, or package work | Yes, before configuration readiness |
| Every request | Blocker | | Downstream profile configuration or another task's execution is included | Retain the complete request boundary and identify routed-away scope; do not execute it as Content Items | No automatic scope change |
| Create-only FSM package or import | Blocker | verify_content_item_fsm_import_contract | Profile mode is not legacy; the package changes metadata/member/header shape, carries a key present in fresh or seeded evidence or a generated ID, omits an owning seeded type's required input, uses an unverified Content Supplier code, lacks both seed-manifest fingerprints or exact Content Type/Rating Model/dynamic-field/relationship evidence or its approved provider-row fingerprint, includes an unsupported object, is not bound to the approved proposal and target, or bypasses core.data-loader | For legacy mode, rebuild from the reviewed baseline and start a new Core Data Loader preview; for enhanced GOAL, require a corrected or independently certified provider | Yes, before preview; never by runtime repair |
| Profile-mode route selection | Blocker | resolve_content_item_provider_mode | Profile mode is unknown, or any enhanced-profile row is assigned to FSM | Resolve same-target mode. Use the supported legacy or independently eligible Item Catalog FSM route; enhanced GOAL may evaluate only the explicitly selected verified fallback. Other HDL routes and every ownership or provider mismatch remain blocked. | Yes, before package construction |
| Read provider selection | Blocker | select_content_item_evidence_provider | A non-GOAL enhanced context is unregistered, its exact template selector is unresolved, or the provider result is partial | Register and read-certify the exact provider/context route; do not reuse GOAL-only FSM evidence | Yes, before proposal or readback |
| Enhanced-profile HDL package or import | Historical contract only; not selectable in GROW-8154 V1.  Blocker | verify_content_item_hdl_import_contract | The exact provider route/lifecycle is not eligible; the exact nonblocked Item Catalog or provider-specific zero-match evidence is missing/stale/ambiguous; a live or seeded code/name collision exists; row fields/fixed values differ; an unsupported technical character or source-system key is present; DateFrom is not YYYY/MM/DD; live metadata validation fails; package hash differs; or the route bypasses core.data-loader | Preserve the verified Competency route. For a catalog provider, rebuild only from a fresh lifecycle-bound dual-key receipt and exact checked-in row contract. | Yes, before preview; never by runtime repair |
| Enhanced-profile GOAL HDL package or import | Explicit verified GOAL fallback exception only. Blocker | verify_goal_content_item_hdl_import_contract | Exception selection is absent, strict FSM-only is requested, lifecycle is not verified, or prior mutation state is not not_submitted; the fresh complete GOAL FSM receipt is absent/stale/changed/filtered/multi-context/alternate-target; an exact code or name exists; the row is not the exact four-field GOAL shape; a value-set/catalog, supplier, Rating Model, source-system, generated-ID, relationship, translation, proficiency, or extra field is present; row count is not one; live ContentItem source/schema validation fails; provider/receipt/row/archive fingerprint changes; or the route bypasses core.data-loader | Reinspect the exact routed export and rebuild only through the isolated GOAL provider. Do not broaden its lifecycle or repair provider rows at runtime. | Yes, before preview; never by runtime repair |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_complete_content_item_evidence | Owning-type, existing-item, and relationship comparison | content_type_identity; exact_matches; matched_identifiers; relationship_matches; comparison_evidence | ora_reference_lookups.md |
| verify_content_item_fsm_import_contract | Create-only package and Data Loader handoff | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route | ora_reference_lookups.md |
| resolve_content_item_provider_mode | Every package route | profile_mode; provider_route; evidence_reference | ora_reference_lookups.md |
| select_content_item_evidence_provider | Every duplicate or readback route | evidence_provider; registry_entry; coverage_expectation | ora_reference_lookups.md |
| verify_content_item_hdl_import_contract | Historical contract only; not selectable in GROW-8154 V1.  Enhanced-profile Competency or catalog-provider package and Data Loader handoff | provider_lifecycle; provider_contract_sha256; current_state_receipt_sha256; package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; source_type; business_object; data_loader_route | ora_reference_lookups.md |
| verify_goal_content_item_hdl_import_contract | Explicit verified GOAL fallback exception only. Enhanced-profile GOAL provider certification and Data Loader handoff | provider_lifecycle; package_path; package_sha256; provider_contract_sha256; current_state_receipt_sha256; evidence_fingerprint; provider_rows_fingerprint; readiness_fingerprint; source_type; business_object; data_loader_route | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CI.ENFORCE_DESIGN | decision | 6 | design_enforcement | compliant->CI.BUILD_REVIEW_PROPOSAL;blocked->CI.RETURN_BLOCKED | CI.CHECK_DEPENDENCIES | stop | A preliminary supplied-configuration scope or not-found configuration proposal is being prepared |
| CI.ENFORCE_FSM_IMPORT | decision | 14 | design_enforcement | compliant->CI.RETURN_IMPORT_READY;blocked->CI.RETURN_IMPORT_BLOCKED | CI.VALIDATE_FSM_IMPORT | stop | The exact create-only Content Items FSM package is being validated immediately before the Core Data Loader preview |
| CI.ENFORCE_HDL_IMPORT | decision | 19 | design_enforcement | compliant->CI.RETURN_HDL_IMPORT_READY;blocked->CI.RETURN_HDL_IMPORT_BLOCKED | CI.VALIDATE_HDL_IMPORT | stop | The exact enhanced-profile create-only ContentItem V2 HDL package is being validated immediately before the Core Data Loader preview |
| CI.ENFORCE_GOAL_HDL_IMPORT | decision | 25 | design_enforcement | compliant->CI.RETURN_GOAL_HDL_IMPORT_READY;blocked->CI.RETURN_HDL_IMPORT_BLOCKED | CI.VALIDATE_GOAL_HDL_IMPORT | stop | The exact enhanced-profile GOAL lifecycle-governed ContentItem V2 HDL package is being validated immediately before the Core Data Loader preview |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Content Items](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-items.html)
- [Competency-to-Behavior Relationships](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/considerations-for-associating-behaviors-with-competencies.html)
