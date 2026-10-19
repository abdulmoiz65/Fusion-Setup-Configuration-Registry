# Content Types Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supplied object | Select the task from supplied type, property or relationship values and exclude nearby scope |
| 2 | Preserve supplied configuration | Keep the complete local parent/child set and exact source provenance |
| 3 | Confirm mappings | Show uncertain source-to-field mappings and require confirmation before creation |
| 4 | Normalize after confirmation | Convert the confirmed proposal to supported Content Type fields without authorizing execution |
| 5 | Check exact duplicates | Apply exact-match rules only after technical normalization and complete current evidence; stop on every exact duplicate |
| 6 | Bind review | Freeze normalized values, provenance, evidence, assumptions, exclusions, and fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | | The supplied object scope is ambiguous | Clarify the supplied object scope, or route an explicit out-of-scope request; retain uncertain field mappings in preliminary review | Yes, before scope confirmation |
| Every supplied value and mapping | Blocker | | Source provenance is missing or an omitted optional value was added | Restore source provenance or remove inferred data from the local proposal; preserve unresolved mappings for preliminary review | Yes, before proposal |
| Fusion-touching phase | Blocker | | Authenticated structured environment checks are unavailable, a screenshot or attestation is substituted, or required target evidence is missing | Return a preflight blocker; record release only from trusted metadata | No automatic fix |
| Existing configuration is considered | Blocker | find_complete_content_type_evidence | The customer export is filtered or target-mismatched, the source-backed seed catalog is invalid, or any exact candidate exists | Resolve both evidence layers; every exact match blocks create and retains its matched identifier | No automatic fix |
| A configuration-ready proposal is prepared | Blocker | | A required value or source mapping is unresolved | Preserve the supplied values and alternatives in preliminary review; require a decision before configuration readiness | Yes, before configuration readiness |
| Every proposal | Blocker | | The proposal includes a rating model, profile type, profile section, person profile, or downstream configuration | Remove and route the out-of-scope work | Yes, by splitting scope |
| Create-only FSM package or import | Blocker | verify_content_type_fsm_import_contract | The package changes metadata/member/header shape, carries a key present in fresh or seeded evidence or a generated ID, lacks the customer-export or seed-manifest fingerprint, lacks exact provider/dependency evidence or its approved provider-row fingerprint, is not bound to the approved proposal and target, or bypasses core.data-loader | Rebuild from the reviewed baseline and start a new Core Data Loader preview | Yes, before preview; never by runtime repair |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_complete_content_type_evidence | Existing-definition comparison | exact_matches; matched_identifiers; comparison_evidence; evidence_fingerprint | ora_reference_lookups.md |
| verify_content_type_fsm_import_contract | Create-only package and Data Loader handoff | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CT.ENFORCE_DESIGN | decision | 4 | design_enforcement | compliant->CT.BUILD_REVIEW_PROPOSAL;blocked->CT.RETURN_BLOCKED | CT.CHECK_DEPENDENCIES | stop | A complete supplied-configuration review proposal is being prepared |
| CT.ENFORCE_FSM_IMPORT | decision | 12 | design_enforcement | compliant->CT.RETURN_IMPORT_READY;blocked->CT.RETURN_IMPORT_BLOCKED | CT.VALIDATE_FSM_IMPORT | stop | The exact create-only Content Types FSM package is being validated immediately before the Core Data Loader preview |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Content Type Relationships](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/examples-of-content-type-relationships.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
