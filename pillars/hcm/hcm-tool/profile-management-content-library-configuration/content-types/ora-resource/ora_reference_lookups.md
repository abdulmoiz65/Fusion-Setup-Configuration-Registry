# Content Types Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| capture_content_type_supplied_configuration | Supplied configuration needs normalization | Local normalized direct input or locally extracted readable-file values and confirmed mappings | Resolve ownership only from supplied type, property and relationship fields. Preserve exact values, source rows and complete-set identity; do not derive missing values from a baseline or default. | proposal_scope; proposed_values; assumption_ledger; exclusions; source_fingerprint | Clarify the supplied object or mapping; retain missing required values as blockers. |
| find_complete_content_type_evidence | Exact duplicate review, or a new definition is proposed | Approved request plus one fresh workflow-approved unfiltered Content Types task export for the exact target and the checked-in seed catalog for the declared task/provider schema | Match exact `ContextName` in the fresh customer layer first and the seeded layer second. A fresh row overrides the same seed key; missing fresh properties or relationships are filled from seed. Then compare the full applicable header, properties, translations, and owned relationships. Use only the provider's exact key semantics; no similarity analysis. | customer_evidence_fingerprint; seed_manifest_fingerprint; evidence_source; exact_matches; matched_identifiers; missing_values; comparison_evidence | A filtered or target-mismatched export, missing or wrong-task catalog, invalid manifest/hash, or multiple provider-key matches blocks selection. |
| verify_content_type_fsm_import_contract | A create-only Content Types package or import is requested | Approved proposal and provider-row fingerprints, fresh unfiltered same-target Content Types ZIP, integrity-validated seed catalog manifest, reviewed same-task baseline ZIP, exact provider rows, approved property pairs and relationship contexts, package readiness receipt, and final ZIP SHA-256 | Require task HRT_MANAGE_PROFILE_CONTENT_TYPES, exact members and headers, unchanged metadata, no key in fresh or seeded evidence, unique property ContextName/FieldName identities, one relationship per portable endpoint-context pair regardless of RelationshipCode, no generated IDs, consistent parent and endpoint aliases, supplied relationship DateFrom, create rows only, exact provider-row fingerprint binding, both evidence fingerprints, and data_loader_handoff.route equal to core.data-loader | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; seed_manifest_fingerprint; data_loader_route | Missing, stale, filtered, ambiguous, changed, tampered, or mismatched evidence blocks the package/import branch. ColumnName is not a property identity discriminator. The dated physical relationship key does not authorize multi-date lifecycle operations. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One fully equal fresh customer definition is found | Return canonical classification exact with match source customer and route outcome exact_from_customer; stop creation and display the actual matched identifier |
| No fresh key but one fully equal seeded definition is found | Return canonical classification exact with match source seeded and route outcome exact_from_seeded; stop creation and display the actual matched identifier |
| No exact definition exists in either layer | Continue to design enforcement for one review-only proposal |
| No supported exact key matches | Return not-found only from complete evidence; do not compute or display similarity warnings |
| Multiple equally supported definitions remain | Stop for resolution; do not select one |
| A create-only package passes the exact local contract | Return the immutable package evidence to Task Hook; do not upload from this task rule |
| The package, baseline, customer evidence, seed catalog, release, or SHA-256 changes | Invalidate readiness and require a new package and Data Loader preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CT.CHECK_EXACT_EXISTING | decision | 3 | evaluate_result | exact_from_customer->CT.RETURN_EXACT_DUPLICATE;exact_from_seeded->CT.RETURN_EXACT_DUPLICATE;not_found->CT.ENFORCE_DESIGN;multiple_exact->CT.RETURN_BLOCKED;evidence_unavailable->CT.RETURN_BLOCKED | CT.CHECK_DEPENDENCIES | stop | The fresh unfiltered target customer layer and integrity-validated seeded catalog are available |

## Sources

- Bounded native jkaribee_v2 source: ContentTypePropertyVO.xml v2 (UserKey ContextName,FieldName); ContentTypeRelationshipVO.xml and ContentTypeRelationshipEO.xml v6 (portable endpoint key, required DateFrom, optional DateTo, equal-date comparison). Source-only evidence does not prove deployed runtime acceptance.

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Content Types](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-types.html)
- [Content Type Properties](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-type-properties.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
