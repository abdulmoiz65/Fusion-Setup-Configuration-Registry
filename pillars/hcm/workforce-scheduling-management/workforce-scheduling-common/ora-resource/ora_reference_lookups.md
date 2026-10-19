# Workforce Scheduling Common Provider Lookups

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 31 August 2026

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_profile_option_provider_state | A Workforce Scheduling profile-option change is being considered. | Provider product/team Common Applications / ApplCore; profileOptionCode supplied by the consuming skill; FSM source reference Manage Administrator Profile Values. | Invoke core.fusion-api.apps-common.profile-options through manage-profile-options. | Provider current state, product-recommended state, validation result, and unresolved gap. | Pass the consuming skill's profileOptionCode unchanged. Manage Administrator Profile Values is traceability only and cannot be substituted for the supplied identifier. | Before state, recommended state, validation result, after state when changed, and provider gap. | Stop before recommendation or change; request profileOptionCode from the consuming skill or report the provider gap. |
| query_lookup_provider_state | A Workforce Scheduling lookup change is being considered. | Provider product/team Common Applications / ApplCore; lookupType supplied by the consuming skill; FSM source references Manage Common Lookups and Manage Extended Lookup Codes; supplied lookup-source labels Common Lookups and HCM Extended Lookup Code. | Invoke core.fusion-api.apps-common.lookups.references through manage-lookups. | Provider current state, product-recommended state, validation result, and unresolved gap. | Pass the consuming skill's lookupType unchanged. Source references and lookup-source labels cannot be substituted for the supplied identifier. | Before state, recommended state, validation result, after state when changed, and provider gap. | Stop before recommendation or change; request lookupType from the consuming skill or report the provider gap. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A provider-backed configuration change is proposed. | Invoke the named provider first and retain the provider-returned evidence. |
| The provider reports no required difference. | Return the before state and validation result; do not apply a change. |
| The provider reports a required difference. | Present the current and recommended state, then obtain user confirmation immediately before the provider-owned change. |
| The consuming skill omits the identifier or provider evidence is incomplete. | Return the unresolved provider gap and stop. Do not construct a fallback request or clone provider behavior. |
