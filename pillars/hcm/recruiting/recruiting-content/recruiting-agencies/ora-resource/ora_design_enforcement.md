# Recruiting Agencies Design Enforcement

## Purpose

Defines mandatory agency-only, exact-identity, lookup, package-proof, preservation, and approval gates.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Keep agency-only scope | Reject agent, account, role, relationship, deletion, direct REST, and database requests |
| 2 | Validate enabled values | Resolve Referral Type, Contract Type, and Exclusivity Length through APPS_COMMON_LOOKUPS |
| 3 | Preserve operation intent | Never convert Create to Update or Update to Create |
| 4 | Preserve proven structure | Use only the current target-release agency CSV header, metadata, and package members |
| 5 | Freeze the preview | Compute SHA-256 and bind target, task, Agency Name, operation, and effective values before approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Agent or agency-agent work is requested | Error | | Agent rows, coverage, accounts, passwords, roles, or relationships are requested | Remove agent scope; the FSM package contains agency data only | Yes, by the user |
| Allow Internal Candidate Search is requested | Error | | The field is not represented in the verified agency CSV | Maintain it manually in Fusion | No |
| Referral Type is required or supplied | Error | resolve_referral_type | No exact single enabled match exists | Enter a currently enabled code or meaning | Yes, by the user |
| Contract Type is supplied | Error | resolve_contract_type | No exact single enabled match exists | Enter a currently enabled code or meaning | Yes, by the user |
| Resulting Referral Type is Person Specific | Error | resolve_exclusivity_length | Exclusivity Length is absent or unresolved | Enter a currently enabled Exclusivity Length | Yes, by the user |
| Create is requested | Error | verify_agency_identity | The fresh export has any exact Agency Name match | Use a different name or submit a separate explicit Update | No |
| Update is requested | Error | verify_agency_identity | The fresh export does not have exactly one exact Agency Name match | Enter one exact existing Agency Name | No |
| Create package is generated | Error | verify_agency_status | StatusCode remains blank after defaulting | Apply ORA_ACTIVE when Status was omitted or use a target-valid supplied value | No |
| Candidate package is generated | Error | verify_fresh_agency_export | Header, metadata, package member, source fingerprint, or target evidence is missing or stale | Rebuild from a fresh verified target export | No |
| Update omits a field | Error | verify_fresh_agency_export | Omission is treated as clearing or deletion | Preserve the exported value | No |
| Import is requested | Error | verify_candidate_agency_zip | Artifact, target, operation, Agency Name, effective values, fingerprint, or approval does not match | Produce and approve a new immutable preview | No |
| Direct REST, database, delete, undocumented lifecycle, or automatic retry is requested | Error | | The requested route is outside the supported contract | Use the guarded FSM workflow or remove the request | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_referral_type | Referral Type validation | Enabled LookupCode and Meaning | ora_reference_lookups.md |
| resolve_contract_type | Contract Type is supplied | Enabled LookupCode and Meaning | ora_reference_lookups.md |
| resolve_exclusivity_length | Person Specific or Exclusivity Length supplied | Enabled LookupCode and Meaning | ora_reference_lookups.md |
| verify_agency_identity | Create or Update | Exact Agency Name classification and exported Update row | ora_reference_lookups.md |
| verify_agency_status | Status supplied or Update preserves it | Validated or exported StatusCode | ora_reference_lookups.md |
| verify_fresh_agency_export | Package generation | Target, metadata, member/header inventory, rows, and fingerprint | ora_reference_lookups.md |
| verify_candidate_agency_zip | Import handoff | Immutable fingerprint, exact approval, and target | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.CHECK_DESIGN | decision | 60 | design_enforcement | passed->RA.PREVIEW_IMPORT;blocked->RA.HANDLE_ISSUES | RA.CHECK_DEPENDENCIES | stop | Create, Update, or Import after dependency readiness |
