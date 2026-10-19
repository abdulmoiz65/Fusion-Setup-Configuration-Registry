# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| UOM class creation record | ClassCode, ClassName, BaseUnitOfMeasure, BaseUOMCode | Block | Provide every required value. | Creation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ClassCode is no more than 10 characters and ClassName is no more than 10 characters | Return correction; do not perform a lookup. | Creation values are present |  |
| BaseUnitOfMeasure is no more than 25 characters and BaseUOMCode is no more than 3 characters | Return correction; do not perform a lookup. | Creation values are present |  |
| ClassCode or ClassName has one uniquely high-confidence spelling candidate under `ora_design_enforcement.md` | Return the probable typo and suggested spelling; require the user to confirm or replace it. Do not run a lookup, generate a sample, create a preview, or submit a write. | Creation values are present | check_probable_typo |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UMC.VALIDATE | decision | 1 | validate_input | valid->UMC.ASSESS_CLASS_SEMANTICS;invalid->UMC.HANDLE_ISSUE | none | stop | Creation |
