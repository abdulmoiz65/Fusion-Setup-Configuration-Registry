# Instance Qualifiers Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplied configuration | Preserve local intake and confirmed mappings; identify missing required values without comparable-configuration discovery |
| 2 | Supported field contract | After proposal confirmation, use the packaged Profile Types view contract |
| 3 | Standalone provider classification | Treat the standalone no-column export as a capability mismatch for that provider; do not retry it |
| 4 | Complete current-state evidence | For exact claims, obtain one complete authenticated-target HRT_MANAGE_PROFILE_TYPES read through the owner |
| 5 | Mutation provider readiness | Keep V1 proposal-only because the containing Profile Types workflow has no approved executor contract |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| supplied_configuration_capture | Supplied qualifier configuration | Yes | A review proposal is requested | Verify | Local normalized user input and confirmed file mappings | capture_instance_qualifier_supplied_configuration | All supplied qualifier sets, children and references must survive normalization | Identify exact missing rows or mappings; leave optionals omitted | proposal_scope; proposed_business_rules; assumption_ledger; exclusions |
| instance_qualifier_field_contract | Authoritative Instance Qualifiers proposal and comparison field contract | Yes | Every technical or exact-match proposal | Satisfied | Source-backed Profile Types QualifierSetVO and QualifierVO user keys and exclusions; QualifierTypeCode constants; current Oracle Instance Qualifier Sets guidance | resolve_instance_qualifier_field_contract | The containing provider exposes the exact business identity and comparison fields | Preserve the source fingerprint and reject undocumented fields | supported_fields; identity_fields; value_rules; contract_fingerprint |
| standalone_csv_provider | Standalone HRT_MANAGE_INSTANCE_QUALIFIERS CSV provider | Yes | A standalone export, template, retry, package, or import is requested | Blocked | Retained live data and template exports contain metadata only and report unavailable columns; 26C source says qualifier sets moved under Profile Types in 21A and disables standalone import | | The catalog support flags do not match an executable standalone route | Do not retry or build a standalone package; use the Profile Types containment handoff for read-only evidence | provider_status; blocker_reference; containing_task_code |
| complete_instance_qualifier_evidence | Complete current Instance Qualifiers evidence | Yes | Exact duplicate review, or configuration readiness is requested | Blocked | No complete target-bound HRT_MANAGE_PROFILE_TYPES artifact is retained for this run | find_complete_instance_qualifier_evidence | The standalone metadata-only export cannot prove absence or equality | Request one complete read-only Profile Types export through its owning skill, then compare the exact nested user keys and all supported values | evidence_path; target_identity; evidence_fingerprint; completeness_status |
| mutation_provider | Approved Instance Qualifiers create or import provider | Yes | Creation, import, update, merge, delete, or end-date is requested | Blocked | The containing Profile Types skill has not established an approved setup-provider executor contract | | Source nesting proves containment, not write authorization | Return a supplied-configuration blocked result; do not build an import template or invoke another route | provider_status; blocker_reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The source-backed proposal/comparison field contract exists | Local contract lookup yes; create no |
| Proposal-ready | Supplied object ownership and mappings are unambiguous but technical or exact evidence is incomplete | Preliminary review-only proposal; no exact or create claim |
| Needs evidence | A complete target-bound Profile Types artifact must be obtained | No |
| Blocked | The standalone provider or any mutation request applies | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IQ.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->IQ.CHECK_EXACT_EXISTING;proposal_only->IQ.ENFORCE_DESIGN;field_contract_unavailable->IQ.RETURN_BLOCKED;standalone_provider_unavailable->IQ.RETURN_BLOCKED;evidence_unavailable->IQ.RETURN_BLOCKED;mutation_requested->IQ.RETURN_UNSUPPORTED;blocked->IQ.RETURN_BLOCKED | IQ.CAPTURE_CONFIGURATION | stop | A supplied-configuration Instance Qualifiers proposal or exact review is being resolved |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Tool FSCR taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-tool-fscr-taxonomy/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
