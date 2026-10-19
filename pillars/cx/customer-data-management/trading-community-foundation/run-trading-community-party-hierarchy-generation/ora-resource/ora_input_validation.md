# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Preview parameters | hierarchy_type and flattening_method | Ask once for all unresolved required values, show all four hierarchy-type options and both flattening-method options, or accept an explicit request to use Oracle defaults | Normalize documented business labels into the canonical values owned by the task skill | Every new preview |  |
| Optional hierarchy scope | hierarchy_name and hierarchy_version | Preserve each omitted value as null; propose all hierarchies and active/default version in the consolidated confirmation | Use exact hierarchy-name text and pass the exact supplied Version value unchanged as argument3; do not create a separate optional-field intake round | A name or version is supplied or omitted |  |
| Target environment | Exactly one Fusion environment | Stop before any live lookup or submission | Automatically select the environment when exactly one is configured; ask for selection only when none or multiple are resolvable | Live lookup, request tracking, or submission |  |
| Execution controls | execution_intent, execution_approval, project_id for submission, optional wait_seconds and poll_interval | Return preview only or stop before live execution | Preserve explicit run intent while collecting missing parameters; obtain one consolidated approval only after parameters, target, payload, and tracking details are complete | Execute or resume |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| hierarchy_type is supplied | Accept each documented type for preview and execution | Map CUSTOMER to HZ_CUSTOMER_HIERARCHY, DUNS_AND_BRADSTREET to HZ_DNB_HIERARCHY, PARTNER to HZ_PARTNER_HIERARCHY, and TRADING_COMMUNITY_PARTY to HZ_PARTY_HIERARCHY |  |
| flattening_method is supplied | Accept Incremental or Force for preview and execution | Map INCREMENTAL to INCREMENTAL_FLATTENING and FORCE to FORCE_FLATTENING |  |
| hierarchy_name is supplied | Preserve the exact scalar text as argument2; use null when omitted | Do not perform an LOV lookup or invent an identifier |  |
| hierarchy_version is supplied | Treat the exact supplied value as argument3 | Preserve and pass the value unchanged; do not ask for a separate internal identifier |  |
| Live submission is requested | Build the payload for every documented hierarchy-type and flattening-method combination | Stop on a value outside the documented set, unresolved target, or approval blocker |  |
| Exactly one configured target is available | Resolve it automatically before the approval preview | Include the exact environment in the single consolidated approval; do not ask for a separate environment confirmation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| hierarchy_type | Accept only CUSTOMER, DUNS_AND_BRADSTREET, PARTNER, or TRADING_COMMUNITY_PARTY after plain-language normalization; allow all four for execution | Every preview |  |
| partner wording | Normalize partner, partner hierarchy, or partner hierarchies to PARTNER; require the Trading Community Party wording for TRADING_COMMUNITY_PARTY | Natural-language intake |  |
| hierarchy_name | Preserve the exact nonempty user-supplied name; reject control characters, never derive an internal identifier, and use null when omitted | Every preview |  |
| hierarchy_version | Preserve the exact nonempty user-supplied Version value and send it unchanged as argument3 | Every preview and execution |  |
| flattening_method | Accept only INCREMENTAL or FORCE after plain-language normalization; map full mode or full flattening to FORCE and allow both for execution | Every preview |  |
| explicit broad scope | Set all_hierarchies_explicit from explicit all-hierarchy language or from the user's direct confirmation of a consolidated preview that visibly states all hierarchies | No hierarchy name is supplied |  |
| explicit force | Set force_flattening_explicit from explicit Force Flattening/full mode language or from the user's direct confirmation of a consolidated preview that visibly states Force impact | FORCE is selected |  |
| unknown fields | Reject any field outside the four business parameters and the two preview authorization facts | Builder input |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PHG.VALIDATE | step | 1 | validate_input | valid->PHG.APPLY_DEFAULTS;invalid->PHG.RETURN_ISSUES | none | stop | Before defaulting, lookup resolution, preview, request tracking, or submission. |
