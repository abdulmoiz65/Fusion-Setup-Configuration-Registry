# Goal Management Profile Options Input Validation

## Source Basis

The enclosing SKILL.md owns the Goal Management delegation and semantic-intake contract.
Input shape is checked locally; tenant validity is established by the provider lookup.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Profile identity | Exact consultant-supplied ProfileOptionName or profile_option_name resolved by the existing semantic-intake resolver | Block provider lookup | Resolve behavior through the existing intake resolver and its profile-option-semantic-catalog.json; request clarification for unresolved or ambiguous intent | Before a profile lookup |  |
| Requested operation | read_definition, read_effective, or a value-update intent | Ask for the intended operation | Preserve the supplied read or update intent | Every request |  |
| Update intent | Exact requested value and level, supplied or explicitly recorded by semantic intake | Block update handoff | Clarify missing intent; retain the resolver's profile-specific mapping and level provenance | A value update is requested |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact nonblank identity | Pass the resolved or supplied code unchanged; do not restrict exact codes to the semantic catalog | Before provider lookup |  |
| Semantic resolution status | Require resolved status for behavior-based requests; neutral, contradictory, uncertain, or ambiguous wording requires consultant confirmation | Behavior supplied instead of an exact code |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.VALIDATE_INPUT | step | 5 | validate_input | valid->MPO.QUERY_PROVIDER;blocked->MPO.HANDLE_ISSUES | none | stop | Before a Goal Management profile read or update handoff |
