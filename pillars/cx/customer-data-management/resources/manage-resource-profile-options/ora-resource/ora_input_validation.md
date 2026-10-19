# Manage Resource Profile Options Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Profile value change identity | ProfileOptionName, level, scope key, and requested ProfileOptionValue | Block validation | Provide every changed FND_APP_PROFILE_VALUE row and its target value | Every FSM profile-value import |  |
| Supported profile level | SITE, PRODUCT, or USER | Block validation | Provide a supported level and its exact scope key | Every FSM profile-value import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Duplicate profile-value target | Block validation when ProfileOptionName, level, and scope key occur more than once with different requested values | Every FSM profile-value import |  |
| Requested value is non-empty | Continue to profile resolution | Every FSM profile-value import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.VALIDATE_INPUT | step | 1 | validate_input | valid->RPO.RESOLVE_PROFILE;missing_or_invalid->RPO.RETURN_ISSUES | none | stop | Every FSM profile-value import |
