# Item Catalogs Error Handling and Approval Gates

## Error Situations

| Situation | What Should Happen |
|---|---|
| item-catalog-existing-skill-canary-v1 lacks valid supplied current evidence | Stop certification with evidence_blocker under ../references/existing-skill-catalog-certification.md; this exception takes precedence over generic optional-export continuation below. Do not export automatically, switch to new-catalog mode, or trim a supplied batch. |
| Supplied object ownership is genuinely ambiguous | Ask the one concise configuration-mapping question and stop without selecting a task |
| Authenticated structured environment checks are unavailable | Report preflight blocked; never replace identity/access checks with a screenshot, address-bar image, copied URL, exact reply, or user attestation; the bound new-set classification confirmation cannot establish authentication |
| Release metadata is unavailable | Keep the release unknown and continue the declared operation; release metadata is not a gate |
| The request is owned by another skill | Name the owner and produce no Item Catalog proposal |
| Current evidence is stale, partial, unbound, schema-only, or not populated | Do not claim empty target or Profile V2 readiness. Reject invalid evidence supplied for validation; skipped/failed acquisition may continue under optional-export policy with gaps disclosed. |
| Rating Model resolution is unavailable for supplied rating descriptions | Classify a dependency blocker without inventing an ID; do not package the row |
| A rating-description row, advanced child field, update, merge, delete, end-date, or direct provider route is requested | Return unsupported and name the narrow Item Catalog FSM / `core.data-loader` boundary |
| Required parent values or registered context/supplier are missing, or a known collision exists | Block invalid input or known collision. Unavailable export alone is nonblocking; do not invent parent values or claim equality/absence. |
| A required provider row, dependency, package or Task Hook shape is not evidenced | Report the exact failed contract; never infer or repair it |
| Proposal or package confirmation is presented as execution approval | Apply Core Data Loader's authoritative approval policy to the current immutable preview; proposal/package confirmation alone is never submission authority |
| Import fails, times out, or reports partial success | Persist status and ProcessLog when available; do not retry because the product provider can commit before later translation failure |
| Readback is missing, multiple, or mismatched | Report differences and coverage. On skipped/failed export try registered REST reads; return partially_verified or verification_incomplete. Never hide an observed mismatch or auto-correct. |
| A new-set terminal failure has missing or invalid ProcessLog or partial readback | Preserve process_failed, accepted IDs and the original failure; append the evidence gaps without converting failure to success or erasing it with a generic blocker |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required supplied configuration or provider input is absent or invalid | Correct the named input |
| transport_or_environment | Authenticated target identity or required structured capability evidence is unavailable | Restore the declared authenticated context or structured check |
| business_ambiguity | Two or more ownership patterns remain equally supported | Ask the missing configuration-mapping question |
| owner_mismatch | The requested outcome belongs to another skill | Route to the named owner without a partial Item Catalog proposal |
| evidence_blocker | Required Content Type, package-format or target evidence is invalid; optional export failure is instead a warning | Resolve required evidence; report export failure and continue authorized import or registered read-only verification |
| dependency_blocker | An exact source-backed dependency is unavailable | Establish the approved resolver and retry review |
| catalog_or_metadata_mismatch | Task, member, header, metadata, provider row, parent anchor, key, grouping, generated field, lifecycle, or child scope fails | Rebuild locally from exact approved inputs |
| approval_blocker | Proposal/package approval is reused for submission or the preview changed | Build a new immutable Data Loader preview and apply Core's authoritative approval policy for that identified load |
| process_failed_or_timeout | The separately approved import fails, times out, or is partial | Persist safe diagnostics and require explicit review; never auto-retry |
| readback_mismatch | Fresh full export differs from approved portable catalog or Content Item values, including parent drift | Report differences and stop without correction |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Proposal review | Supplied configuration, scope, mapping review status, approved catalog values, provenance, evidence status/fingerprint, dependencies, assumptions, exclusions, and unresolved decisions |
| Preliminary scope proposal | State that exact/reuse/new-value disposition is unavailable until approved values and complete evidence are supplied |
| Exact duplicate result | Actual matched `(ContextName, ContentValueSetCode)` identifier, evidence binding, and blocked creation; no reuse recommendation |
| Package readiness | Exact task, package hash, provider-row/readiness fingerprints, target, Core route, Task Hook/approval state, pre_import_export and unverified_checks |
| Blocked result | Failure class, evidence/dependency/contract gap, and one safe next action |
| Readback | Separate process/verification status, export failures, REST attempts, compared fields, differences, remaining gaps and no-auto-retry status |
| New-set retained lifecycle verification | Use the parent new-catalog-set contract after the owning status/readback workflows; disclose archive and complete-set fingerprints, accepted IDs, terminal state, complete parent/all-child comparison and evidence gaps; local hashes do not authenticate the source or promote the provider |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Proposal or package is accepted | Do not interpret acceptance as authorization to upload, import, update, merge, delete, or end-date |
| A direct or internal write route is requested | Do not invoke Fusion SOAP/REST, FSM endpoints, HDL, HSDL, browser automation, or the migration service; route only through `core.data-loader` after Task Hook and preview approval |
| A full export is supplied as a payload | Do not submit it; use it only as evidence/baseline and rewrite all CSVs from approved rows |
| Rating-description rows, advanced child fields, or multiple children outside explicit new-set mode are supplied | Do not package them; retain the complete set as blocked scope. Explicit new-set mode alone permits multiple portable children with one intended-new parent under its separate certification-only contract; skipped export does not establish absence |
| Sensitive values are encountered | Do not persist credentials, tokens, employee data, private keys, sensitive payloads, or full business export rows |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IC.BUILD_REVIEW_PROPOSAL | decision | 5 | execution_gate | prepared->IC.RETURN_PROPOSAL;confirmation_or_execution_requested->IC.RETURN_UNSUPPORTED;blocked->IC.RETURN_BLOCKED | IC.ENFORCE_DESIGN | stop | A compliant review-only Item Catalogs proposal is ready to fingerprint |
| IC.RETURN_PROPOSAL | terminal | 6 | terminal | none | IC.BUILD_REVIEW_PROPOSAL | stop | A fingerprinted review-only proposal is returned with no package or execution authorization |
| IC.RETURN_EXACT_DUPLICATE | terminal | 7 | terminal | none | IC.CHECK_EXACT_EXISTING | stop | An exact existing catalog identifier is displayed; creation is blocked even when supplied values are equal |
| IC.RETURN_QUESTION | terminal | 8 | terminal | none | IC.CAPTURE_CONFIGURATION | stop | One concise supplied-object mapping question is required |
| IC.RETURN_BLOCKED | terminal | 9 | terminal | none | none | stop | Input, evidence, exactness, dependency, design, package, or persistence is blocked |
| IC.RETURN_UNSUPPORTED | terminal | 10 | terminal | none | none | stop | The request is out of scope, uses unsupported rating-description or advanced child rows or mutation, or tries to bypass approval separation |
| IC.RETURN_IMPORT_READY | terminal | 13 | terminal | none | IC.ENFORCE_FSM_IMPORT | stop | Task validation returns exact catalog-only, phase-one anchored Content Item, or explicit controlled new-set package evidence to `core.data-loader` for immutable preview; no upload is authorized |
| IC.RETURN_IMPORT_BLOCKED | terminal | 14 | terminal | none | none | stop | The Item Catalog package or Data Loader handoff contract is invalid, stale, changed, or incomplete |

## Sources

- [GROW-8154 FDD v3, AC1–AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Common Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
