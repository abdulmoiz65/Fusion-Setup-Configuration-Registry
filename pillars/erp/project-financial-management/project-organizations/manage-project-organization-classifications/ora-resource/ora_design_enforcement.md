# Design Enforcement

**Omitted classification input means preserve existing state.**

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | REST state first | Resolve one exact effective organization and PTO/PEO independently |
| 2 | Explicit scope | Add only requested missing classifications; never recreate an existing one |
| 3 | Request permissions | Enable to Y; new PTO omissions to N; no export read/default/comparison |
| 4 | Original update identity | Existing PTO updates retain verified keys and only supplied columns |
| 5 | Approval/verification | Immutable delta, core HDL approval/load and post-load readback |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Identity/existence | Blocker | find_existing_project_organization | Missing, ambiguous, incomplete, inactive or conflicting REST state | Stop; never infer absence from export | No |
| New PTO permissions | Blocker | | Values are obtained/defaulted/compared from export or missing user fields cause export lookup | Use request Enable/Y, Disable/N and omitted N; all-N does not block local preparation | Yes |
| Existing classification | Blocker | find_existing_project_organization | A new row is generated for REST-confirmed existing PTO/PEO | Preserve existing classification; update only explicitly supplied PTO permissions | No |
| Existing PTO update: legacy supplied permissions or bulk update_existing_pto_permissions=true with supplied permissions | Blocker | resolve_existing_pto_update_identity | Original authoritative information-row keys are missing/ambiguous/conflicting | Stop this explicit update; bulk without opt-in bypasses existing-update identity requirements; never fabricate keys, owner or receipt or trigger a permission export | No |
| Omission | Blocker | | Omitted classification creates a row or omitted existing permission emits a column | Preserve omissions; no confirmation or inferred update | No |
| Parent/delta | Blocker | verify_classification_archive | Parent MERGE, unrequested classification or unsupported headers | Metadata anchor only; regenerate exact approved delta | Yes |
| New keys | Blocker | verify_classification_mapping | Replacement existing key or unpersisted/colliding/stale new mapping | Reuse original update keys and persist only new keys | No |
| Bulk parent bindings | Blocker | verify_classification_mapping | Reused baseline, repeated parent, wrong target/run, missing timezone timestamp or stale delta mapping | Require fresh independent baseline and mapping per organization; globally unique keys | No |
| Bulk layouts | Blocker | verify_classification_archive | Multiple information layouts, missing new-PTO information pair or role mixing | One PEO ZIP and one PTO ZIP maximum; compatible explicit update columns only; never populate omitted existing permissions | No |
| Bulk atomic preparation | Blocker | verify_classification_archive | A failed entry is skipped, partial ZIP generated or no-op organization emits a row | Validate every entry before writing; exclude no-ops from artifacts and approvals | No |

## Classification Delta Contract

REST alone determines PTO/PEO existence. PTO only, PEO only and both are supported; omitted targets remain unchanged. Supplied permission fields express PTO intent. A requested missing PEO emits one PEO row; existing PEO emits none. Requested missing PTO emits one PTO classification/information pair. User Enable/Enabled/Y becomes Y, Disable/Disabled/N becomes N, Boolean input is normalized equivalently, and omitted new PTO flags default N. These values never depend on an export; all-N may proceed locally under the latest user instruction and any actual Fusion rejection is retained without replay.

An active, effective prior classification from the governed REST baseline establishes the existing organization's eligibility. PTO or PEO itself can be that prior classification; do not require an unrelated third classification before adding the other requested missing role. All identity, completeness, active/effective, ambiguity and conflicting-state checks remain mandatory.

For an existing PTO in a legacy single request, supplied permissions express an explicit update. In a bulk request, supplied permissions update an existing PTO only when that entry also sets update_existing_pto_permissions=true. Without bulk opt-in, preserve the existing PTO even when new-PTO permission values accompany a BOTH request; do not require original update keys or emit information rows for it. For an explicit update, write supplied permissions directly as a partial OrgInformation MERGE using original verified keys; omitted columns preserve target values. Do not read or compare previous permissions or claim a matching-value no-op. No permissions supplied means no information update. No requested mutation means no artifact. Never create a duplicate classification to work around missing update identity or missing export data.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_existing_project_organization | Every request | Exact complete active REST state | ora_reference_lookups.md |
| resolve_existing_pto_update_identity | Existing PTO with supplied permissions in a legacy single request; bulk also requires update_existing_pto_permissions=true | Authoritative original OrgInformation identity, not flags | ora_reference_lookups.md |
| verify_classification_mapping | Mutation | Stable keys and baseline/request binding | ora_reference_lookups.md |
| verify_classification_archive | Preview | Exact request-derived delta and checksum | ora_reference_lookups.md |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.ENFORCE_DESIGN | decision | 12 | design_enforcement | pass->PORGCLASS.EXECUTION_GATE;blocked->PORGCLASS.RETURN_REFUSAL;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.RESOLVE_DEPENDENCIES | stop | Validate every organization then generate at most two role-separated ZIPs; allow multiple parent IDs, unique keys and matching new PTO information pairs; no-op entries emit nothing; enforce one compatible PTO layout |
