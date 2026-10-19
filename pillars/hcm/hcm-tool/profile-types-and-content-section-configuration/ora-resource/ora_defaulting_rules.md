# Profile Types and Content Section Configuration Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Resolution precedence | Explicit user value; approved project decision; one dominant comparable; documented Oracle rule or safe exclusion; deterministic review-only generation | A technical value is absent | No | resolve_profile_business_context |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Comparable configuration | No comparable selected | No single source-backed comparable is clearly dominant | No | find_dominant_profile_configuration |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Profiles V2 seeded target | No default | No exact seeded type is explicitly supplied or resolved from approved evidence | No | |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Optional component group | Omitted | No explicit value, approved decision, dominant comparable, or documented rule supports it | No | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.PROPOSAL | decision | 3 | apply_default | review_complete->PTCS.NORMALIZE;clarification_required->PTCS.CLARIFY | PTCS.DISCOVERY | stop | Discovery yields one safe review-only proposal |
