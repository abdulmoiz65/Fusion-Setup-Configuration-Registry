# Instance Qualifiers Error Handling and Proposal Gate

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied object or source-to-field mapping is ambiguous | Ask one concise question about the supplied object or mapping and stop |
| Authenticated structured environment checks are unavailable | Report preflight blocked; never request a screenshot, address-bar image, copied URL, exact reply, or user attestation |
| Quarterly release metadata is unavailable | Preserve unknown and continue local supplied-configuration normalization or preliminary review using supported fields. Do not infer a release, claim exact absence or enable the unsupported standalone provider; containing evidence remains owned by Profile Types. |
| Supported fields or identity rules are unavailable | Classify a source-contract blocker and stop before technical normalization |
| Standalone data or template export contains only metadata and unavailable-column warnings | Classify a catalog-capability mismatch; do not retry and do not infer zero configuration |
| Current Profile Types evidence is absent or uninterpretable | Classify an evidence blocker; do not infer no existing values |
| Proposal confirmation or execution is requested | State that V1 confirmation reviews only and cannot authorize creation or import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required supplied qualifier input is absent or invalid | Correct the named object or row input |
| transport_or_environment | Authenticated target identity or required structured capability evidence is unavailable | Restore the declared authenticated context or structured check |
| source_contract_blocker | Source-backed technical fields or identity rules are not authoritative | Obtain one versioned product-authoritative contract |
| catalog_capability_mismatch | Catalog flags advertise standalone CSV support but the live export and 21A-plus provider source show that qualifier data is contained by Profile Types | Stop standalone retries and identify the HRT_MANAGE_PROFILE_TYPES evidence handoff |
| evidence_blocker | Complete target-bound Profile Types evidence is unavailable or ambiguous | Obtain an interpretable complete read through the Profile Types owner |
| scope_or_provider_blocker | Work belongs elsewhere or mutation lacks an approved containing provider | Route the design scope or retain the supplied-configuration result for later implementation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Supplied-configuration review | All supplied sets and children, exact containing references, source mappings, optional omissions, standalone/containing-provider blockers and next evidence needed |
| Technical proposal | Supported contract fingerprint, complete-evidence fingerprint, exact result, actual matched identifiers, and every source-derived field |
| Blocked result | Failure class, standalone or containing-provider status, unavailable contract or evidence, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Proposal is accepted | Do not interpret acceptance as authorization to create, import, update, merge, delete, or end-date |
| A standalone retry, guessed template, or direct write is requested | Do not retry the no-column standalone task, invent fields, or invoke Fusion REST, FSM import, loaders, or browser automation |
| Sensitive values are encountered | Do not persist credentials, tokens, employee data, private keys, or sensitive payloads |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IQ.BUILD_REVIEW_PROPOSAL | decision | 5 | execution_gate | prepared->IQ.RETURN_PROPOSAL;confirmation_or_execution_requested->IQ.RETURN_UNSUPPORTED;blocked->IQ.RETURN_BLOCKED | IQ.ENFORCE_DESIGN | stop | A compliant review-only Instance Qualifiers proposal is ready to fingerprint |
| IQ.RETURN_PROPOSAL | terminal | 6 | terminal | none | IQ.BUILD_REVIEW_PROPOSAL | stop | A fingerprinted review-only proposal is returned with no execution authorization |
| IQ.RETURN_EXACT_DUPLICATE | terminal | 7 | terminal | none | IQ.CHECK_EXACT_EXISTING | stop | An exact qualifier set blocks creation; display its matched identifier |
| IQ.RETURN_QUESTION | terminal | 8 | terminal | none | IQ.CAPTURE_CONFIGURATION | stop | One concise technical-scope clarification is required |
| IQ.RETURN_BLOCKED | terminal | 9 | terminal | none | none | stop | Input, source contract, evidence, dependency, design, or persistence is blocked |
| IQ.RETURN_UNSUPPORTED | terminal | 10 | terminal | none | none | stop | The request is out of scope or attempts execution in proposal-only V1 |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Common Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
