# Manage Expense Report Templates Design Enforcement

## Preparation and Review

When intake passes, automatically produce the normalized design and internal
preservation/execution contracts, then obtain the declared fresh baseline and
build the candidate. There are no separate contract-production, contract-review,
or candidate-build decisions. Exact-artifact import approval remains mandatory.

Use the baseline-bound builder and `references/import-candidate-contract.md`.
Create a separate CSV review workbook plus the exact extracted CSV files and
a checksum manifest. Every CSV member must be reviewable without truncating
rows or changing headers, order, leading zeros, dates, or code strings.
CSV content beginning with formula characters must be stored as text in Excel.
The review workbook is never submitted to FSM.

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Target-resolved new template/type | Blocking | export_preservation_baseline | Identity is absent but a required create value is missing, or the identity match is ambiguous | Supply missing values or correct the identity | Yes |
| Target-resolved existing template/type | Blocking | export_preservation_baseline | Zero/multiple matches after classification, rename/removal request, or unintended changes | Use a unique existing identity and preserve unrequested fields | Yes |
| Source normalization | Blocking | | Supplied values are silently discarded, code-guessed, or overwritten with unselected seeds | Retain provenance and resolve each issue | Yes |
| Conditional sections | Blocking | | Child rows conflict with disabled controls or lack scope | Correct the owning template/type and control | Yes |
| Task support | Blocking | | A requested field or child mapping lacks a verified builder contract | Report the exact limitation before packaging; obtain correction | Yes |
| Candidate construction | Blocking | export_preservation_baseline | Baseline checksum/identity mismatches or protected rows/members change | Reconcile and rebuild from a fresh baseline | Yes |
| CSV review | Blocking | | Review contents differ from the final ZIP, omit a CSV, or contain evaluated source formulas | Regenerate review and verify bytes/rows | Yes |
| Submission | Blocking | | Validation failed, approval/envelope absent, stale hash, or environment differs | Revalidate and obtain approval of the exact reviewed ZIP | No |
| Corrections | Blocking | | An edited/rebuilt artifact reuses prior approval or replays a successful create | Reconcile outcomes, rebuild and obtain new approval | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| export_preservation_baseline | Preparation after complete intake and before candidate construction | Same-environment baseline; exact identities; schema; row hashes; ProcessId and ZIP checksum | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMERT.PREPARE_CANDIDATE | step | 9 | design_enforcement | built_and_reviewable->EXMERT.VALIDATE_CANDIDATE;invalid->EXMERT.NEEDS_CORRECTION;failed->EXMERT.BLOCKED | EXMERT.EXPORT_BASELINE | stop | Build the baseline-bound ZIP and complete CSV review automatically after validating all values and references |
