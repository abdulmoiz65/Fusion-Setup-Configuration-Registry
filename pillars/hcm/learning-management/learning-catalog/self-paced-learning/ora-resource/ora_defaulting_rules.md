# Self-Paced Learning Defaulting Rules

Defaults are visible in the preview, target-validated where they become REST
values, and never overwrite an explicit compatible user value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Demonstration batch size | 10 | Demonstration generation is requested without a count | No; accept an explicit integer from 1 through 10 and reject a larger or smaller value | |
| Demonstration topic | Supplied industry, domain, or topic; otherwise clearly labeled generic learning examples | Demonstration candidates are generated | No | |
| Demonstration title and description | Generated unique reviewable values with candidate provenance | Demonstration candidates are generated | No; preserve explicit user values | |
| Demonstration expected effort | Generated reviewable estimate | Demonstration candidates are generated | No; preserve an explicit supported value | |
| Demonstration content intent | Article plus URL intent | Demonstration candidates are generated | No; an explicit supported content intent wins | resolve_self_paced_lookup_value |
| Demonstration Objective | Generated preview-only text that is omitted from REST | Demonstration candidates are generated | No; preserve for preview but never serialize it | |
| Demonstration Ideal Learner | Generated preview-only text that is omitted from REST | Demonstration candidates are generated | No; preserve for preview but never serialize it | |
| Demonstration catalog profile | The one verified active usable target profile whose system-default flag is affirmative | Demonstration candidate needs a profile and none is supplied | No; an explicit exact usable profile wins | resolve_self_paced_catalog_profile |
| learningItemStatus | ORA_DRAFT | Parent create follows the FDD draft-first flow | No; an explicit supported intent remains separate and publish is never implied | resolve_self_paced_lookup_value |
| Deep-insert content status | Fusion derives ORA_ACTIVE | Parent create includes content | No; omit status from the artifact and verify readback | |
| Deep-insert content autoCommit | Fusion derives Y | Parent create includes content | No; omit autoCommit from the artifact and verify readback | |
| Activation behavior | Separate explicit operation | Every create or update | No; activation is never implied and the collection publish action is distinct | |
| Content publish behavior | Separate explicit operation | Content publishing is requested | No; never substitute it for item activation | |
| Row identifier | Stable input row number or generated candidate identifier | Multi-row or demonstration input lacks a business row label | No; preserve a unique supplied row identifier | |

## No-Default Rules

| Field | Why No Default Is Allowed | Required Action |
|---|---|---|
| learningItemNumber | A generated business key can collide or violate the customer's convention | Supply or explicitly approve a generated number after exact collision checks |
| learningItemVisibility | REST creation requires visibility and no portable target-safe business default is established | Supply a visibility intent and resolve its exact enabled code |
| Owner | Person identity and assignment cannot be inferred | Supply an exact person identifier when owner is needed |
| Language | A label or locale cannot safely establish the target code and serialization | Supply a label or code and run the live language resolver |
| Effective dates | Business timing must be intentional | Supply dates when the business scenario requires them |
| Content URL | Generated or guessed URLs can be unreachable, unauthorized, or misleading | Supply or explicitly approve a reachable allowed-protocol URL |
| Objective and Ideal Learner persistence | Confirmed Self-Paced REST schemas do not contain these fields | Keep them preview-only and explicitly accept omission before execution |

## Override Rules

| Situation | What Happens |
|---|---|
| User supplies a compatible value | Preserve it and validate it instead of applying the default |
| User supplies an incompatible value | Block the affected row and explain the exact correction; do not silently replace it |
| Default depends on live target state | Resolve and freeze the exact evidence in the preview before approval |
| Default evidence changes | Mark the preview stale and obtain new approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPL.APPLY_DEFAULTS | decision | 40 | apply_default | applied->SPL.ENFORCE_DESIGN;preserved->SPL.ENFORCE_DESIGN;blocked->SPL.HANDLE_ERROR | SPL.RESOLVE_REFERENCES | stop | Validated inputs omit only a documented safe default or contain an explicit compatible value |
