# Goal Management Profile Options Provider Lookup

## Source Basis

The enclosing SKILL.md defines the canonical provider and its read_definition and
read_effective operations. The semantic catalog supplies planning candidates only;
the provider owns tenant lookup mechanics and validates current tenant state.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_profile_option_provider_state | After input validation for a profile read or value-update handoff | Exact ProfileOptionName; operation intent; requested level and value when applicable; target environment from the active workflow | Delegate read_definition and, for effective-value reads or updates, read_effective to core.fusion-api.apps-common.profile-options; the provider selects its supported read endpoint | Profile definition, product ownership, permitted levels and values, effective value and scope provenance when applicable, validation diagnostics | Require one exact supplied or resolved profile code in the target tenant; check the requested scope and value through the provider | Current definition, effective value when applicable, validated scope/value evidence, provider gap | Return validation_gap for unknown or ambiguous identity; return PROVIDER_SKILL_UNAVAILABLE when the capability is absent; stop without constructing a substitute request |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact code is supplied | Preserve it unchanged even when it is absent from the semantic catalog. |
| Behavior is resolved by intake | Validate the candidate code, product, stored value, and declared default level against tenant metadata; catalog resolution alone is insufficient. |
| Lookup is invoked | Use only the provider's declared read workflow; this task does not perform mutations. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.QUERY_PROVIDER | step | 10 | reference_lookup | resolved->MPO.ENFORCE_OWNERSHIP;blocked->MPO.HANDLE_ISSUES;failure->MPO.HANDLE_ISSUES | MPO.VALIDATE_INPUT | stop | Before returning profile evidence or handing off a value update |
