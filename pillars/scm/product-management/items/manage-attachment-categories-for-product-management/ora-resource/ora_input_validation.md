# Attachment Category Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Attachment category identity | Category Name, User Name; Description is optional | Return a structured `input_validation` failure and block preview | Identify each missing required field in the failure response; stop output generation | Creating or updating an attachment category | |
| Attachment entity assignment | Entity Name | Default to ITEM_ENTITY and request user approval of that entity before preview | Continue to the entity default and approval gate only after the skill's New Category Preflight confirms the category name is available | Creating an attachment category | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Entity Name is supplied and is an allowed value | Input validation passes | Apply Product Model defaults | |
| Entity Name is missing | Input validation passes conditionally | Set Entity Name to ITEM_ENTITY, then ask the user to approve that value; stop until approval is received | |
| Entity Name is not an allowed value | Input validation failure | Ask the user to provide one of the allowed Entity Name values | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Entity Name must be ITEM_ENTITY, ITEM_REVISION_ENTITY, EGO_ENGINEERING_CHANGES_B, or ITEMCLASS_ENTITY | Block preview and ask for one of the allowed values when it does not match exactly | Entity Name is supplied | |
| Category availability preflight | Require the skill's New Category Preflight to have completed with a fresh, complete baseline and zero exact Category Name matches. Stop before this local validation node if that evidence is absent. | Creating an attachment category | |

When Entity Name is omitted after the category name is confirmed available, set it to `ITEM_ENTITY` and ask the user to approve that exact value. Wait for explicit approval before validation passes or any preview, package preparation, or submission. If rejected, ask for an allowed Entity Name and rerun validation. This approval does not replace approval for a later Fusion mutation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALIDATE_ATTACHMENT_CATEGORY_INPUTS | decision | 15 | validate_input | valid_or_default_approved->APPLY_PRODUCT_MODEL_DEFAULTS;missing_or_invalid_or_default_rejected->RETURN_ISSUES | none | stop | After the skill's New Category Preflight confirms the Category Name is available; default an omitted Entity Name to ITEM_ENTITY and wait for user approval before passing validation |
