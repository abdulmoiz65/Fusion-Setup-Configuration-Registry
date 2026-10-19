# Instance Qualifiers Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| capture_instance_qualifier_supplied_configuration | Supplied configuration needs normalization | Local normalized direct input or locally extracted readable-file values and confirmed mappings | Resolve ownership from supplied qualifier set and row fields; preserve exact values, full keys, source rows and complete-set identity. Never infer qualifier configuration from comparable setups. | proposal_scope; proposed_business_rules; assumption_ledger; exclusions; source_fingerprint | Clarify the supplied object or mapping; retain missing required values as blockers. |
| resolve_instance_qualifier_field_contract | A technical proposal or exact comparison is requested | Fusion 26C Profile Types QualifierSetVO and QualifierVO definitions and user keys; QualifierTypeCode constants; current Oracle Instance Qualifier Sets guidance | Require the integrity-validated Profile Types view contract. Set identity is QualifierSetCode plus ProfileTypeCode plus ContextName plus SectionContext. Child identity adds QualifierCode. Reject excluded IDs and audit fields. Preserve P for prompt or key-table source and Q for selected qualifier rows without silent defaulting. | supported_fields; identity_fields; value_rules; contract_fingerprint | Incompatible source definitions or an unknown supplied field keeps readiness blocked. |
| find_complete_instance_qualifier_evidence | The field contract is ready and exact duplicate review or proposal is requested | Approved request plus one complete same-target HRT_MANAGE_PROFILE_TYPES export obtained through the Profile Types owner | Locate qualifier sets nested below the exact Profile Type Section. Match the full set user key, then the full child user key, and compare every applicable supported set and child value. Use only the full supported key; do not compute or display similarity warnings. | evidence_fingerprint; exact_matches; matched_identifiers; missing_values; comparison_evidence | A standalone HRT_MANAGE_INSTANCE_QUALIFIERS metadata-only export is never complete evidence. No complete Profile Types artifact or multiple exact provider-key matches blocks selection. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The integrity-validated field contract is unavailable | Stop before technical fields, template shapes, exact-match claims, or proposal values are produced |
| A standalone export has the no-column signature | Classify catalog-capability mismatch, do not retry, and identify HRT_MANAGE_PROFILE_TYPES as the read-only containing-evidence handoff |
| A complete Profile Types artifact is unavailable | Stop before absence, reuse, or equality claims; do not treat standalone metadata as zero rows |
| One fully equal current set is found after readiness | Return exact with the actual matched identifier; stop creation without reuse or updates |
| No exact set is found after readiness | Continue to one review-only proposal |
| Multiple or partially equal sets remain | Disclose differences and stop; never select silently |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IQ.CHECK_EXACT_EXISTING | decision | 3 | evaluate_result | exact->IQ.RETURN_EXACT_DUPLICATE;not_found->IQ.ENFORCE_DESIGN;multiple_exact->IQ.RETURN_BLOCKED;evidence_unavailable->IQ.RETURN_BLOCKED | IQ.CHECK_DEPENDENCIES | stop | A source-backed field contract and complete target-bound evidence are available |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Instance Qualifier Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/instance-qualifier-sets.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
