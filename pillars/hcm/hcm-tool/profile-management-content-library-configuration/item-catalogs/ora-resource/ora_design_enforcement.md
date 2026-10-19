# Item Catalogs Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supplied object ownership | Route supplied catalog fields and links without requiring Fusion terminology; exclude nearby task scope |
| 2 | Capture supplied values | Accept direct values, the blank template, or a readable existing file; preserve the complete set and source provenance |
| 3 | Build complete configuration review | Record every supplied value and mapping with source, sanitized evidence, and review status; omit absent optional values |
| 4 | Normalize after confirmation | Convert the confirmed proposal to supported Item Catalog fields without authorizing execution |
| 5 | Evaluate available evidence | Reject known collisions; skipped/failed export records unverified target checks |
| 6 | Bind package scope | For a separate package run, freeze exact rows, baseline, target, and fingerprints |
| 7 | Preserve approval separation | Return package readiness only to Task Hook; require a new `core.data-loader` preview and its authoritative approval policy for the identified load |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| SKILL child creation | Blocker | verify_item_catalog_fsm_import_contract | Missing explicit controlled capability, production/general-use, a predefined/managed catalog, or an existing-parent request outside item-catalog-existing-skill-canary-v1 | Select the user's intended parent strategy through ../references/skill-catalog-creation.md. An existing custom parent permits only the separately approved one-child canary under ../references/existing-skill-catalog-certification.md with supplied current evidence. Keep all six rows in review until a separate canary is explicitly selected; never substitute a new catalog, trim a batch or claim runtime certification. | Before a new capability-bound preview only |
| A preliminary scope proposal | Warning | | Approved values or complete evidence are not yet supplied | Label the proposal preliminary and make no existing-value, reuse, or new-value claim | No automatic fix |
| Fusion-touching phase | Blocker | | Authenticated structured environment checks are unavailable, a screenshot or attestation is substituted for authenticated identity/access, or required target evidence is missing | Return an identity/access preflight blocker; the bound new-set user classification confirmation is permitted under ../../references/new-catalog-set-contract.md but cannot replace those checks; release may remain unknown | No automatic fix |
| An exact current-state or duplicate-absence claim | Blocker | find_complete_item_catalog_evidence | Current evidence is missing, stale, partial, unbound, schema-only, or ambiguous | Obtain supported evidence for the claim; import may proceed without the claim under ../references/optional-export-policy.md | No automatic fix |
| Existing configuration is considered | Blocker | find_complete_item_catalog_evidence | Multiple exact candidates, a proposed-create key/name collision, or any applicable business value difference remains | Display matched identifiers and block duplicate creation, even for equal values. An unchanged parent anchor in an approved child-create route is not a proposed catalog create; validate that anchor through verify_item_catalog_fsm_import_contract. Never choose replacement names/codes. | No automatic fix |
| A Rating Model is applicable to review | Blocker | resolve_item_catalog_rating_model | The exact portable model reference cannot be resolved | Establish the approved resolver evidence; never guess `RatingModelId` | No automatic fix |
| Item Catalog FSM package or import | Blocker | verify_item_catalog_fsm_import_contract | Invalid metadata/header/member shape, unsupported scope, wrong target, known collision/parent contradiction, missing required Content Type/provider-row bindings or bypass of Core. Ordinary imports retain optional-export continuation; item-catalog-existing-skill-canary-v1 instead requires supplied current evidence. Preserve capability classification, mappings, counts, fingerprints and approval. | Rebuild from the reviewed baseline and start a new Core Data Loader preview; missing canary evidence stops without an automatic export | Yes, before preview; never by runtime repair |
| Every proposal | Blocker | | A material mapping lacks provenance or review status, two patterns are equally supported, or work belongs to another skill | Ask only the missing configuration-mapping question or route the work; never silently select | Yes, before proposal |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_complete_item_catalog_evidence | Existing-catalog comparison | exact_key_contract_reference; exact_matches; name_collision_count; comparison_evidence; evidence_fingerprint | ora_reference_lookups.md |
| resolve_item_catalog_rating_model | A Rating Model is applicable to review | rating_model_identity; supported_reference_value; evidence_reference | ora_reference_lookups.md |
| verify_item_catalog_fsm_import_contract | Item Catalog package and Data Loader handoff | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; profile_v2_evidence_sha256; provider_registry_sha256; data_loader_route | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IC.ENFORCE_DESIGN | decision | 4 | design_enforcement | compliant->IC.BUILD_REVIEW_PROPOSAL;blocked->IC.RETURN_BLOCKED | IC.CHECK_DEPENDENCIES | stop | A preliminary scope proposal or a not-found configuration proposal is ready for design enforcement |
| IC.ENFORCE_FSM_IMPORT | decision | 12 | design_enforcement | compliant->IC.RETURN_IMPORT_READY;blocked->IC.RETURN_IMPORT_BLOCKED | IC.VALIDATE_FSM_IMPORT | stop | The exact catalog-only, phase-one anchored Content Item, or explicit controlled new-set FSM package is being validated immediately before the Core Data Loader preview |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Using Enhanced Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/using-enhanced-talent-profiles.pdf)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
