# Profile Rating Models Defaulting Rules

## Defaulting Precedence

| Task Code | Task Name | Priority | Condition | Required Action | Outcome |
|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 1 | A valid explicit value is supplied | Preserve it | preserved |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 2 | An approved current-project decision exists for the same business use | Propose it with project evidence and review status | proposed |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 3 | Discovery returns one materially dominant compatible pattern | Propose its compatible convention with resolver evidence; never call it exact reuse yet | proposed |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 4 | A documented product rule or exactly one consumer exclusion applies | Apply the rule or exclusion and record its source | applied |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 5 | Business meaning is explicit and deterministic generation is safe | Generate a review-only value and label it deterministic | proposed |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 6 | Material alternatives remain equally supported or a required value has no safe proposal | Apply no value and return one business ambiguity | business_ambiguity |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 7 | No rule applies | Make no change | not_required |

## Standard Defaults and Exclusions

| Task Code | Task Name | Field | Default or Exclusion | Applies When | Can User Override? | If Unavailable or Invalid |
|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Operation | create_or_reuse | V1 request | No | Block |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Consumers | Infer a review-required consumer or consumer union from explicit business language | One interpretation is materially stronger and does not rely on model data alone | Yes | Ask one business question when interpretations would change behavior |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Code, name and description | Generate a review-only proposal from explicit business wording and one proven naming convention; otherwise use a clearly labeled deterministic name/code proposal | The user did not supply technical identity and the proposal does not overwrite an explicit value | Yes | Do not invent an enterprise convention; ask only when competing identities have business impact |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Level labels, descriptions and numeric sequence | Propose from an explicit ordered scale or one dominant compatible pattern; whole-number sequence may be generated only when the scale direction and meaning are explicit | Initial business statement omitted technical level fields | Yes | Ask one business question when count, order, direction or meaning is ambiguous |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Base language | Propose only from proven target metadata or one compatible current-project/environment convention | Language was not stated | Yes | Leave review required when evidence is absent or conflicting |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Review points and ranges | Exclude | No selected consumer requires a calculated Performance mapping or explicit review points | No | Block conflicting supplied values |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Rating categories | Exclude | Talent Review does not require categories | No | Block conflicting supplied values |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Direct model distributions | Exclude | Compensation does not require them | No | Never substitute a Performance target distribution |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Performance target distribution | Handoff only; never model-owned | Performance requirements include it | No | Block if represented as a direct model distribution |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | End date | No default | End date is omitted | Yes | Leave open-ended; never invent a date |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Precision, rounding, categories, distributions and translations | No execution default | A resolved consumer requires the value and no explicit, project-approved, or dominant compatible pattern supports a proposal | No | Ask one business-impact question before normalization; never silently execute an assumption |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.DEFAULTS | decision | 3 | apply_default | applied->PRM.PROPOSAL;preserved->PRM.PROPOSAL;proposed->PRM.PROPOSAL;not_required->PRM.PROPOSAL;business_ambiguity->PRM.PROPOSAL;blocked->PRM.ERROR | PRM.DISCOVER | stop | Build a provenance-backed review-only proposal after business-intent validation and pattern discovery |
