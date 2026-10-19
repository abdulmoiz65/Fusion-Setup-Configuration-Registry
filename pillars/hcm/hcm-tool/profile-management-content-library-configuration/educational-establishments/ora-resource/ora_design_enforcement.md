# Educational Establishments Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supplied object | Resolve establishment reference scope from the supplied fields and exclude nearby scope |
| 2 | Preserve supplied configuration | Keep the complete local request and exact source provenance |
| 3 | Confirm mappings | Show uncertain source-to-field mappings and require confirmation before creation |
| 4 | Normalize after confirmation | Convert the confirmed proposal to approved establishment fields without authorizing execution |
| 5 | Check exact duplicates | Apply exact-match rules only after normalization and complete current evidence; stop on every exact duplicate |
| 6 | Bind review | Freeze normalized values, provenance, evidence, assumptions, exclusions, provider blockers, and proposal fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every configuration-ready new value | Blocker | | The approved source or value review status is unresolved | Identify and approve the source before configuration readiness | Yes, before configuration readiness |
| Every supplied value and mapping | Blocker | | Source provenance or actual mapping review status is missing, or an omitted optional was added | Preserve exact source provenance and the actual unresolved or confirmed status; remove invented optional values | Yes, before proposal |
| Fusion-touching phase | Blocker | | Authenticated structured environment checks are unavailable, a screenshot or attestation is substituted, or required target evidence is missing | Return a preflight blocker; record release only from trusted metadata | No automatic fix |
| Existing configuration is considered | Blocker | find_complete_educational_establishment_evidence | Evidence is incomplete or any exact candidate exists | Resolve exact evidence; every exact match blocks creation and retains its identifier | No automatic fix |
| Every configuration-ready proposal | Blocker | | A required value or source-to-field mapping is unresolved | Keep supplied values and unresolved mappings visible in preliminary review; require confirmation before configuration readiness, exact claims, or package work | Yes, before configuration readiness |
| Every request | Blocker | | Employee education records, degrees or fields of study, profile sections, another skill's configuration, update, merge, delete, or end-date is included | Split and route the out-of-scope work | Yes, by changing scope |
| Create-only FSM package or import | Blocker | verify_educational_establishment_fsm_import_contract | The package changes metadata/member/header shape, carries an existing key or generated ID, infers geography, lacks an approved exact provider-row fingerprint, is not bound to the approved proposal/source/target, or bypasses core.data-loader | Rebuild from the reviewed baseline and start a new Core Data Loader preview | Yes, before preview; never by runtime repair |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_complete_educational_establishment_evidence | Existing-establishment comparison | exact_matches; matched_identifiers; missing_values; comparison_evidence; evidence_fingerprint | ora_reference_lookups.md |
| verify_educational_establishment_fsm_import_contract | Create-only package and Data Loader handoff | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EE.ENFORCE_DESIGN | decision | 4 | design_enforcement | compliant->EE.BUILD_REVIEW_PROPOSAL;blocked->EE.RETURN_BLOCKED | EE.CHECK_DEPENDENCIES | stop | A preliminary or configuration-ready supplied-configuration review proposal is being prepared |
| EE.ENFORCE_FSM_IMPORT | decision | 12 | design_enforcement | compliant->EE.RETURN_IMPORT_READY;blocked->EE.RETURN_IMPORT_BLOCKED | EE.VALIDATE_FSM_IMPORT | stop | The exact create-only Educational Establishments FSM package is being validated immediately before the Core Data Loader preview |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Using Enhanced Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/using-enhanced-talent-profiles.pdf)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
