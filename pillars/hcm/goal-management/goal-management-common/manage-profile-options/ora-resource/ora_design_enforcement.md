# Goal Management Profile Options Design Enforcement

## Source Basis

The enclosing SKILL.md and ../../dependent-setup-routing.md define provider ownership.
These gates evaluate supplied intent and provider evidence; they do not authorize a write.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Evidence | Require current provider evidence for the exact requested identity and scope. |
| 2 | Ownership | Return read results or route value maintenance to Manage Administrator Profile Values. |
| 3 | Approval boundary | Preserve the provider-owned exact-value preview, approval, execution, and verification workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Profile evidence is returned | Error | query_profile_option_provider_state | Provider evidence is missing, ambiguous, or inconsistent with the requested tenant, product, level, or value | Resolve the provider diagnostic before continuing | No automatic correction |
| A configured value update is requested | Error | query_profile_option_provider_state | The facade attempts to execute the update or treat validation success as approval | Handoff to hcm.goal-management.goal-management-common.manage-administrator-profile-values using FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES; require its provider-owned preview and explicit approval | Routing only |
| Multiple changes are requested | Error | query_profile_option_provider_state | Single-record writes are looped to simulate bulk maintenance | Let the provider select its supported bulk/setup-import workflow | Routing only |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_profile_option_provider_state | Before returning profile evidence or handing off value maintenance | Exact profile identity, tenant definition and scope, applicable value validation, effective value for updates, provider diagnostics | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.ENFORCE_OWNERSHIP | decision | 20 | design_enforcement | passed->MPO.READY;blocked->MPO.HANDLE_ISSUES | MPO.QUERY_PROVIDER | stop | Before returning a read result or a provider-owned update handoff |
