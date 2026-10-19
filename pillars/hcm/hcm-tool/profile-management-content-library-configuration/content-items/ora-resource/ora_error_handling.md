# Content Items Error Handling and Proposal Gate

Original GROW-8154 V1 acceptance remains FSM-only and FSM is preferred. The separately selected [verified GOAL fallback exception](../../references/verified-fallback-contract.md) may use only its verified single-row HDL provider through Core Data Loader. It is not FSM acceptance or submission approval. Other historical HDL branches remain unreachable. Exact existing identifiers stop creation, even when supplied fields are equal.
## Error Situations

| Situation | What Should Happen |
|---|---|
| Supplied objects or mappings are genuinely ambiguous | Ask one concise configuration-mapping question and stop |
| The selected operation's required authenticated target or capability check fails | Block that operation and report the actual failure. A missing Talent Catalog REST probe does not block FSM export/loader work; unknown quarterly metadata does not by itself block reads. Never substitute a screenshot or user attestation for verified target evidence. |
| Release metadata is unavailable | Keep release metadata unknown and continue; validate actual provider/schema and target evidence, not release eligibility |
| Technical XLSX business-object discriminators or roots share a case-insensitive first-30-character prefix | Create no workbook; prefer a valid FSM route, otherwise require an explicit DAT request |
| Fresh customer items, integrity-validated seed catalogs, owning types, or relationship endpoints are incomplete or ambiguous | Report an evidence blocker and stop |
| A required provider row, dependency, package, or loader shape is not evidenced | Report the exact failed contract; never infer or invoke the internal service |
| FSM is selected for a non-GOAL Content Item on an enhanced-profile target | Classify a catalog/provider mismatch; evaluate only the separately eligible Item Catalog FSM handoff. Other historical HDL providers remain inactive. |
| FSM is selected for a GOAL Content Item on an enhanced-profile target | Classify a catalog/provider mismatch and stop before package construction; the exported two-member shape has a verified companion-document transformation failure, so do not fabricate a translation member or replay the failed request |
| GOAL HDL is selected for ordinary use while its provider is certification-only | Report a scope/provider blocker and stop before package construction; only an explicit controlled certification run may use that lifecycle |
| GOAL HDL evidence is metadata-only, filtered, stale, target-mismatched, multi-context, changed, or has an exact code/name collision | Report the exact evidence blocker and stop; do not substitute an Item Catalog, another context, the failed FSM create route, or an expired receipt |
| GOAL HDL contains catalog/value-set, supplier, Rating Model, source-system, generated-ID, relationship, translation, proficiency, or extra fields | Report an input-validation/provider-contract failure and stop; these references are intentionally absent from the certified four-field candidate rather than unresolved |
| Item Catalog GET returns zero or multiple active Competency catalogs | Report an evidence blocker and stop without guessing a catalog |
| A registered child read returns incomplete pagination, a wrong code, or a missing/multiple child link | Mark evidence unavailable and stop; never interpret the partial response as zero matches |
| A context is read-certified but lacks an eligible creation capability | Permit only the registered GET evidence path. Check independent narrow/new-set FSM registries rather than using historical HDL status as a blanket blocker; SKILL may use its certification-only complete new-set contract. |
| Catalog provider use is general while lifecycle is certification-only | Report a provider-lifecycle blocker and stop; only an explicit controlled certification run may use that lifecycle |
| Catalog receipt is stale, code/name incomplete, seed-colliding, catalog-blocked, or fixed values differ | Report the exact evidence or provider-contract blocker and stop; do not repair the row or substitute another catalog |
| Proposal or package confirmation is presented as execution approval | Apply Core Data Loader's authoritative approval policy to the current immutable preview; proposal/package confirmation alone is never submission authority |
| GOAL fallback is requested after any submitted, accepted, partial, failed, timed-out or unknown mutation | Hold the exception, preserve IDs and ProcessLog, and use the owning status/diagnosis workflow. Never automatically fail over or retry. |
| Strict FSM-only acceptance or an unselected fallback is requested | Keep GOAL FSM creation held; offer the verified exception separately when appropriate without silently selecting it or claiming FSM acceptance. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required supplied configuration or approved item value is absent, or an unsupported target-specific source-system field is supplied | Correct the named value; remove SourceSystemOwner and SourceSystemId when the complete ContentItem V2 user key is available |
| evidence_blocker | A task export is stale, filtered, target-mismatched, or ambiguous; a seed catalog is missing, malformed, or changed; or an exact reference is unavailable | Obtain a fresh unfiltered export and validate or regenerate the matching catalog |
| scope_or_provider_blocker | Work belongs elsewhere, an unsupported object/mutation is requested, or the create-only FSM contract is incomplete | Route the work or correct the named import gate |
| catalog_or_metadata_mismatch | Profile mode and selected provider conflict, Item Catalog identity is ambiguous, or ContentItem V2 metadata differs | Refresh exact metadata/evidence and rebuild through the supported route |
| provider_lifecycle_blocker | GOAL or catalog-provider general use is requested before controlled-load, fresh-readback, and duplicate-lock evidence has promoted the exact provider to verified | Keep general use blocked; complete the separate certification lifecycle without changing the package contract |
| auth_expired_or_invalid | Authentication cannot be established after the one managed refresh | Reauthenticate through the selected core service and rerun only the read |
| authorization_or_privilege | Fusion returns a repeated HTTP 403 after managed refresh | Verify the documented view privilege and stop |
| transport_or_environment | The selected environment does not match or a read-only connection fails after bounded retries | Correct the target binding or transport and rerun only the read |
| fusion_api_error | Fusion returns a malformed or failed read response, or the ContentItem V2 data load fails | Persist sanitized status/error evidence and stop; never replay the load automatically |
| artifact_persistence | Proposal or evidence records cannot be persisted safely | Stop and disclose the artifact failure |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Proposal review | Supplied configuration, scope, normalized item values, owning type, provenance, evidence fingerprint, exact results and actual matched identifiers, relationships, assumptions, exclusions, and unresolved decisions |
| Exact duplicate result | Actual matched identifier, evidence binding, and blocked creation; no reuse recommendation |
| Blocked result | Failure class, missing evidence or decision, and one safe next action |
| Import handoff | Exact task, package name and SHA-256, approved provider-row and readiness fingerprints, target alias, create-only effect, core.data-loader route, Task Hook result, and approval state |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Proposal or package is accepted | Do not interpret acceptance as authorization to upload, import, update, merge, delete, or end-date |
| A direct or internal write route is requested | Do not invoke Fusion REST mutation, the internal migration service, HSDL, or browser automation. Use standard REST only for the declared read-only catalog/readback lookup, and route every FSM or HDL write only through core.data-loader after Task Hook and preview approval. |
| Sensitive values are encountered | Do not persist credentials, tokens, employee data, private keys, or sensitive payloads |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CI.BUILD_REVIEW_PROPOSAL | decision | 7 | execution_gate | prepared->CI.RETURN_PROPOSAL;confirmation_or_execution_requested->CI.RETURN_UNSUPPORTED;blocked->CI.RETURN_BLOCKED | CI.ENFORCE_DESIGN | stop | A compliant review-only Content Items proposal is ready to fingerprint |
| CI.RETURN_PROPOSAL | terminal | 8 | terminal | none | CI.BUILD_REVIEW_PROPOSAL | stop | A fingerprinted review-only proposal is returned with no execution authorization |
| CI.RETURN_EXACT_DUPLICATE | terminal | 9 | terminal | none | CI.CHECK_EXACT_EXISTING | stop | An actual matched existing item identifier is displayed and creation is blocked; no reuse recommendation |
| CI.RETURN_QUESTION | terminal | 10 | terminal | none | CI.CAPTURE_CONFIGURATION | stop | One concise technical-scope clarification is required |
| CI.RETURN_BLOCKED | terminal | 11 | terminal | none | none | stop | Input, evidence, exactness, dependency, design, or persistence is blocked |
| CI.RETURN_UNSUPPORTED | terminal | 12 | terminal | none | none | stop | The request is out of scope, uses an unsupported object/mutation, or bypasses the approved create-only route |
| CI.RETURN_IMPORT_READY | terminal | 15 | terminal | none | CI.ENFORCE_FSM_IMPORT | stop | Task validation returns the exact create-only package evidence to core.data-loader for immutable preview; no upload is authorized |
| CI.RETURN_IMPORT_BLOCKED | terminal | 16 | terminal | none | none | stop | The create-only package or Data Loader handoff contract is invalid, stale, changed, unsupported, or incomplete |
| CI.RETURN_HDL_IMPORT_READY | terminal | 20 | terminal | none | CI.ENFORCE_HDL_IMPORT | stop | Task validation returns the exact create-only ContentItem V2 HDL package evidence to core.data-loader for immutable preview; no upload is authorized |
| CI.RETURN_HDL_IMPORT_BLOCKED | terminal | 27 | terminal | none | none | stop | The HDL package, provider lifecycle, Item Catalog or GOAL FSM evidence, zero-match lock, metadata validation, or Data Loader handoff is invalid, stale, changed, ambiguous, duplicate, or incomplete |
| CI.RETURN_GOAL_HDL_IMPORT_READY | terminal | 26 | terminal | none | CI.ENFORCE_GOAL_HDL_IMPORT | stop | Task validation returns the exact lifecycle-gated GOAL ContentItem V2 HDL package evidence to core.data-loader for immutable preview; no upload is authorized |
| CI.RETURN_ITEM_CATALOG_FSM_HANDOFF | terminal | 28 | terminal | none | CI.HANDOFF_ITEM_CATALOG_FSM | stop | Content Items returns the approved business definition and evidence to Item Catalogs. Item Catalogs owns the FSM package, Task Hook task identity, Data Loader preview, and parent-no-drift readback; no upload is authorized here. |
| CI.RETURN_ITEM_CATALOG_FSM_BLOCKED | terminal | 29 | terminal | none | CI.HANDOFF_ITEM_CATALOG_FSM | stop | The selected narrow or independent new-set Item Catalog capability, scope, target or required bindings are invalid. Missing optional pre-import export is not itself a blocker. Stop without falling back to HDL, creating a package, or uploading. |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Common Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
