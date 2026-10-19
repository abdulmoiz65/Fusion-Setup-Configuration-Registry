# Instance Qualifiers Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplied configuration | Direct values, blank requirements template, or readable existing file; supplied qualifier set and rows | Return the blank template or identify the required row correction | Capture local supplied configuration without purpose or downstream discovery | Every request | |
| Instance Qualifiers ownership signal | Supplied qualifier set/row fields or exact task/object input | Clarify the supplied object before selection | Accept ordinary language without requiring Fusion task names | Every proposal request | |
| Qualifier-set values | Supplied full set and child identities with source references and mapping status | Retain missing required fields as blockers | Preserve supplied rows; never infer visibility, default, priority or search values | A qualifier-set proposal is requested | |
| Source contract and current state | authenticated structured target; source-backed Profile Types field contract; complete current Profile Types artifact containing qualifier sets and rows; fingerprint | Block exact-match claims and technical proposal completion | Resolve the integrity-validated field contract locally, then request one workflow-approved complete read-only HRT_MANAGE_PROFILE_TYPES export through its owner | Exact duplicate checking or configuration readiness is requested | find_complete_instance_qualifier_evidence |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Supplied qualifier set/row values or an explicit task scope identify the owner | Validated | Check required supplied fields and the source-backed containing evidence contract | |
| Two or more materially different owners or patterns are equally supported | Ambiguous | Ask one concise question about the supplied object or mapping and stop | |
| The request owns content items, item catalogs, rating models, profile types, or person profiles | Unsupported | Route to the owning skill | |
| The request asks for Instance Qualifier current state or readback | Validated with handoff | Keep business ownership here and route only the containing HRT_MANAGE_PROFILE_TYPES read to the Profile Types owner | find_complete_instance_qualifier_evidence |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supplied-object routing | Select from supplied objects and fields without purpose or downstream discovery | Every request | |
| Mapping ledger | Record source, evidence, confidence and confirmation for each mapping; never infer optional values | Every proposal | |
| Source mapping | Preserve local source values, confirm uncertain mappings, and leave optional omissions unchanged | Direct or file input | |
| Environment and release evidence | Resolve the live target from authenticated context; never request screenshots, copied URLs, exact replies, or attestations; never ask for or infer the quarterly release | Fusion-touching phase | |
| Source contract | Use only the 26C Profile Types user keys and non-excluded qualifier fields; P is prompt or key-table sourced and Q is selected qualifier rows; do not infer the source type from a business name | Every technical proposal | resolve_instance_qualifier_field_contract |
| Exactness | Require complete evidence and full equality, not a set-name match | Existing qualifier sets are evaluated | find_complete_instance_qualifier_evidence |
| Scope boundary | Reject downstream profile configuration and all mutation routes in V1; a Profile Types export handoff is evidence containment only | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IQ.CAPTURE_CONFIGURATION | decision | 1 | validate_input | valid->IQ.CHECK_DEPENDENCIES;ambiguous->IQ.RETURN_QUESTION;unsupported->IQ.RETURN_UNSUPPORTED;invalid->IQ.RETURN_BLOCKED | none | stop | Every Instance Qualifiers request, with supplied configuration values or explicit task scope |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- [Instance Qualifier Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/instance-qualifier-sets.html)
