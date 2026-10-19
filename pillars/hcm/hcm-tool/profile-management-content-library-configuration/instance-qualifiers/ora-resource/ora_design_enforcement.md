# Instance Qualifiers Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supplied object | Resolve qualifier set and row scope from supplied fields and exclude nearby scope |
| 2 | Preserve supplied configuration | Keep the complete local parent/child request and exact source provenance |
| 3 | Confirm mappings | Show uncertain source-to-field mappings and require confirmation before creation |
| 4 | Establish source authority | After confirmation, require the packaged Profile Types qualifier view contract for technical normalization |
| 5 | Enforce provider boundary | Never use or retry the standalone no-column task as an independent provider |
| 6 | Check exact duplicates | Apply full qualifier user keys only after normalization and complete containing evidence; every exact duplicate blocks creation |
| 7 | Bind review | Freeze approved business rules, source-derived fields, provenance, evidence, exclusions, and fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every technical proposal | Blocker | resolve_instance_qualifier_field_contract | The Profile Types view contract is unavailable, or supplied fields are outside the supported contract | Obtain the matching authoritative source; do not invent a template | No automatic fix |
| Every supplied value and mapping | Blocker | | Source provenance is missing or an omitted optional was added | Restore source provenance or remove inferred data; preserve unresolved mappings for preliminary review | Yes, before proposal |
| Fusion-touching phase | Blocker | | Authenticated structured environment checks are unavailable, a screenshot or attestation is substituted, or required target evidence is missing | Return a preflight blocker; record release only from trusted metadata | No automatic fix |
| A standalone export, template, retry, or package is considered | Blocker | | HRT_MANAGE_INSTANCE_QUALIFIERS is treated as an independent CSV provider despite the confirmed no-column signature and 21A-plus source lifecycle | Stop that route and use the Profile Types owner for a containing read-only export only | Yes, by correcting the route |
| Existing configuration is considered | Blocker | find_complete_instance_qualifier_evidence | Complete Profile Types evidence is missing or any exact candidate exists | Obtain exact containing evidence; every exact match blocks creation and retains its identifier | No automatic fix |
| A configuration-ready proposal is prepared | Blocker | | A required qualifier value or source mapping is unresolved | Preserve the supplied values and alternatives in preliminary review; require a decision before configuration readiness | Yes, before configuration readiness |
| Every proposal | Blocker | | Downstream profile design or a mutation route is included | Split the design scope and keep this child review-only | Yes, by changing scope |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_instance_qualifier_field_contract | Every technical proposal | supported_fields; identity_fields; value_rules; contract_fingerprint | ora_reference_lookups.md |
| find_complete_instance_qualifier_evidence | Existing-set comparison after contract readiness | exact_matches; matched_identifiers; comparison_evidence; evidence_fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IQ.ENFORCE_DESIGN | decision | 4 | design_enforcement | compliant->IQ.BUILD_REVIEW_PROPOSAL;blocked->IQ.RETURN_BLOCKED | IQ.CHECK_DEPENDENCIES | stop | A complete supplied-configuration review proposal is being prepared |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Instance Qualifier Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/instance-qualifier-sets.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
