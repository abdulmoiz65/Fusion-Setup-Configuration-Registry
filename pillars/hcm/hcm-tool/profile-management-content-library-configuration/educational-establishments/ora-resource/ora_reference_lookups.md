# Educational Establishments Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| capture_educational_establishment_supplied_configuration | Supplied configuration needs normalization | Local normalized direct input or locally extracted readable-file values with actual mapping review status | Resolve ownership from supplied establishment fields; preserve exact values, rows, uncertain field mappings and complete-set identity. Never derive institutions from employee data or optional values from comparable setups. | proposal_scope; proposed_values; assumption_ledger; exclusions; source_fingerprint | Show readable incomplete input in preliminary review; clarify ambiguous owning tasks before task selection, and confirm missing values and field mappings before configuration readiness or exact/package work. |
| find_complete_educational_establishment_evidence | Exact duplicate review, or a new-value proposal is requested | Approved values plus one fresh complete current-state Educational Establishments artifact for the exact target | Match only exact `SchoolCode`, then compare every applicable source-supported value. Compare only exact supported identifiers; do not compute or display similarity warnings. | evidence_fingerprint; exact_matches; matched_identifiers; missing_values; comparison_evidence | Missing or incomplete evidence blocks classification. Multiple exact SchoolCode matches block selection and must be disclosed. |
| verify_educational_establishment_fsm_import_contract | A create-only Educational Establishments package or import is requested | Approved proposal, source-authority, and provider-row fingerprints, complete same-target current-state ZIP, reviewed same-task baseline ZIP, exact HRT_SCHOOL provider rows, package readiness receipt, and final ZIP SHA-256 | Require task HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS, exact members/header, unchanged metadata, EstablishmentVO mapping, GroupingKey equal to SchoolCode, explicit geography pairs, no existing keys or generated IDs, exact provider-row fingerprint binding, matching evidence fingerprints, and data_loader_handoff.route equal to core.data-loader | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route | Missing, stale, ambiguous, changed, or mismatched evidence blocks the package/import branch. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One fully equal current establishment is found during proposal review | Return exact with the actual matched identifier; stop creation without reuse or updates |
| No exact establishment is found during proposal review | Continue to a review-only proposal for the missing approved value |
| The exact SchoolCode exists with different applicable values | Classify exact, disclose differences, and block create because V1 does not update |
| No supported exact key matches | Return not-found only from complete evidence; do not compute or display similarity warnings |
| Multiple equally supported matches remain | Stop and require resolution; never select one silently |
| A create-only package passes the exact local contract | Return the immutable package evidence to Task Hook; do not upload from this task rule |
| The package, baseline, current evidence, source authority, or SHA-256 changes | Invalidate readiness and require a new package and Data Loader preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EE.CHECK_EXACT_EXISTING | decision | 3 | evaluate_result | exact->EE.RETURN_EXACT_DUPLICATE;not_found->EE.ENFORCE_DESIGN;multiple_exact->EE.RETURN_BLOCKED;evidence_unavailable->EE.RETURN_BLOCKED | EE.CHECK_DEPENDENCIES | stop | Complete target-bound current-state evidence is available for proposal review |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
