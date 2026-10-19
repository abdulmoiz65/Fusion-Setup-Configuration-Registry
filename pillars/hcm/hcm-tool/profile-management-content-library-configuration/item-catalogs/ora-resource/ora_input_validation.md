# Item Catalogs Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplied configuration | Catalog values, child rows and relationships supplied directly, in the blank template, or in a readable existing file; dates only when supported and applicable | Identify missing required values or unconfirmed mappings; preserve all supplied rows | Use the parent supplied-configuration contract; do not discover business purpose, consumers, workforce design, or comparable defaults | Every supplied-configuration request | |
| Item Catalog ownership signal | Supplied catalog objects and confirmed parent/child mappings, or an explicit task name/code | Ask for the missing object or relationship mapping when ownership is ambiguous | Route from supplied object fields and confirmed mappings; route another owner's request away | Every request | |
| Catalog values | Approved catalog name and code; memberships, rating descriptions, or behavior-catalog values when relevant to review | Keep an initial scope proposal preliminary; block configuration-readiness claims | Supply approved values and leave omitted optional values omitted | Configuration-ready proposal is requested | |
| Exact-match evidence | Authenticated structured target context; freshness and completeness status; full Item Catalog export; artifact fingerprint | Keep the scope proposal preliminary and block exact-match classification | Obtain a workflow-approved populated full export without substituting screenshots, copied URLs, exact replies, or attestations for authenticated identity or complete export evidence | Exact-identifier review, duplicate review, or configuration readiness is requested | find_complete_item_catalog_evidence |
| Item Catalog FSM package | Approved fingerprints; exact task/authenticated target; optional export or skipped/failed receipt; Content Type evidence; validated same-task template; three CSV members; ZIP hash and receipt | Block missing required package inputs, not optional export | Use parent FSM contract and ../references/optional-export-policy.md | Catalog creation or import is requested | verify_item_catalog_fsm_import_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Supplied configuration or an explicit task identifies Item Catalogs | Owned or expert | Check dependency readiness | |
| Two or more ownership patterns remain equally supported | Ambiguous | Ask the one concise configuration-mapping question and stop | |
| The request owns new content definitions, Rating Model creation, Profile Types or sections, Educational Establishments, or profile assignments | Another owner | Name and route to the owning skill without an Item Catalog proposal | |
| A create request contains one catalog-owned Content Item with one exact existing-catalog anchor, one registered context, one approved supplier, and no advanced child values | Item Catalog FSM child-ready | Validate supplied parent/child fields and provider lifecycle; perform target collision checks when evidence is available | verify_item_catalog_fsm_import_contract |
| A create request contains rating-description rows or dynamic, relationship, translation, or generated child fields; or, outside the explicit new-set contract, multiple children or a child without an exact existing anchor | Unsupported child scope | Stop; retain those rows for the next semantic phase | |
| Proposal or package confirmation is presented as Data Loader submission approval | Invalid | Stop; only approval of the current immutable `core.data-loader` preview can authorize upload | |
| Required supplied configuration or confirmed mapping is absent, conflicting, or invalid | Invalid | Identify the invalid input and stop | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Existing SKILL canary binding | Require item-catalog-existing-skill-canary-v1, the independent registry hash, exactly one parent anchor and one child, and complete mappings/group counts; apply ../references/existing-skill-catalog-certification.md, including mandatory supplied current evidence. Preview requires no preparation approval; preparation additionally requires the exact PREPARE EXISTING SKILL CANARY fingerprint statement. Import retains separate Core approval. | Explicit existing-skill canary preview, package or import | verify_item_catalog_fsm_import_contract |
| Supplied-configuration routing | Route only supplied objects and confirmed mappings; never require business-purpose or downstream-consumer discovery | Every supplied-configuration request | |
| Mapping and provenance ledger | Record exact source references and confirmed mappings; leave missing optional values omitted | Every supplied set | |
| Complete-set preservation | Preserve all parent, child, relationship, description, translation, and date rows; block missing required values without inventing replacements | Direct, template, and existing-file intake | |
| Environment and release evidence | Resolve the live target from authenticated context; never substitute screenshots, copied URLs, exact replies, or attestations for identity/access evidence; permit only the bound new-set classification confirmation under ../../references/new-catalog-set-contract.md; never ask for or infer the quarterly release | Fusion-touching phase | |
| Exactness | Compare `(ContextName, ContentValueSetCode)` exactly and every approved catalog business field; a normalized name collision in the owning Content Type blocks create | Existing catalogs are evaluated | find_complete_item_catalog_evidence |
| Provider row completeness | Require exact headers/grouping, blank generated fields, supplied intended parent values and empty rating descriptions. New-parent absence and anchored-parent equality remain unverified without current evidence. | Item Catalog package or import | verify_item_catalog_fsm_import_contract |
| Complete new catalog set | For explicit new-set mode require the separate registry SHA-256, controlled-certification use, Core-authenticated target identity and workflow-established or explicitly user-confirmed non-production classification; validate any target_classification_confirmation under ../../references/new-catalog-set-contract.md, source fingerprint, confirmed complete row mappings, all 14 group counts, full catalog_set_fingerprint and exact PREPARE CATALOG SET approval; retain every unsupported supplied row as a blocker | New-set preview, package or import | verify_item_catalog_fsm_import_contract |
| Profile V2 evidence | Bind populated export when supplied; otherwise allow null profile_v2_evidence_sha256 and disclose indirect preflight not performed | Item Catalog package or import | verify_item_catalog_fsm_import_contract |
| Approval separation | Proposal and package confirmation cannot approve upload; the current `core.data-loader` immutable preview uses Core's authoritative approval policy: valid same-request auto-approval for the identified load or later contextual approval | Item Catalog import | verify_item_catalog_fsm_import_contract |
| Rating dependency | Never invent `RatingModelId`; require a source-backed exact portable Rating Model reference for review, and do not package rating-description rows | A rating model is applicable | resolve_item_catalog_rating_model |
| Scope boundary | Reject Rating Model creation, Content Item business-value invention, downstream profile design, rating descriptions, advanced child fields, and every direct mutation route | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IC.CAPTURE_CONFIGURATION | decision | 1 | validate_input | owned_or_expert->IC.CHECK_DEPENDENCIES;ambiguous->IC.RETURN_QUESTION;another_owner->IC.RETURN_UNSUPPORTED;invalid->IC.RETURN_BLOCKED | none | stop | Every Item Catalogs request, including direct values, blank-template rows, and existing-file intake |
| IC.VALIDATE_FSM_IMPORT | decision | 11 | validate_input | valid->IC.ENFORCE_FSM_IMPORT;invalid->IC.RETURN_IMPORT_BLOCKED;changed->IC.RETURN_IMPORT_BLOCKED | IC.CHECK_DEPENDENCIES | stop | A catalog-only, phase-one anchored Content Item, or explicit controlled new-set FSM package is presented to Task Hook for `core.data-loader` preview |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [Item Catalogs business-intent routing](../references/business-intent-routing.md)
