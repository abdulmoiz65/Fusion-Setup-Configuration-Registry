# Location Costing Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | Query, Create, Update, Correct, End Date, Zap, or Delete Record And History. | Stop | Normalize Delete Record And History to Zap. Reject Delete or ED Split because no supported standard contract is supplied. | Every request | |
| Location identity | Exact LocationCode or LocationName. | Stop | Ask for one Location identifier, then resolve it through the governed Location search. | Every request | resolve_location_source |
| Legislative Data Group | LDG search text and, after candidate selection, the exact returned Name or ID. | Stop | Search candidates, request a choice only when needed, and confirm exactly one returned LDG before the Location search. | Every request | search_legislative_data_groups |
| Effective date | ISO date in YYYY-MM-DD or YYYY/MM/DD form. | Stop for a mutation | Normalize once to YYYY-MM-DD for REST and YYYY/MM/DD only when an authorized loader workflow requires it. Query may use the current date when omitted. | Query, Create, Update, Correct, End Date, or Zap | |
| Account distribution | One or more account rows containing the intended Segment values and a percentage or decimal proportion. | Stop | Require account input and normalize each percentage once to a decimal proportion. | Create, Update, or Correct account MERGE | |
| Correct action | Exactly one existing-account MERGE, new-account MERGE, or child DELETE action per immutable import artifact. | Stop | Ask which one action is intended. A later sibling action requires fresh observed state, preview, and approval. | Correct | |
| Correct sequence | A positive SubTypeSequence from the resolved current account, or an explicit matching positive user value when REST omits it. | Stop | Use the returned positive value when present; otherwise request the exact HDL value. Never infer it from row order, identifiers, or percentages. | Correct account MERGE | query_location_costing |
| Zap child identity | CostAllocAccountId from each returned child and CostAllocationRecordId from its exact bound historical parent. SubTypeSequence may be omitted. | Stop | Preserve both physical IDs from query_location_costing_history_accounts for each child DELETE. Do not block the DELETE, ask the user, or infer a value solely because SubTypeSequence is absent. | Zap child DELETE | query_location_costing_history_accounts |
| Destructive confirmation | Literal JSON boolean confirmed=true bound to the exact preview. | Stop | Obtain confirmation only after the complete target scope and immutable artifact are shown. | End Date, Correct child DELETE, or Zap | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| LDG discovery returns no candidate. | Blocked | Report that no matching LDG was found and request corrected search text. | search_legislative_data_groups |
| LDG discovery returns multiple candidates without one exact returned Name. | Selection required | Show only sanitized returned Names and wait for one selection; do not run later lookups. | search_legislative_data_groups |
| Location search returns zero, multiple, incomplete, inconsistent, or additional unpaged results. | Blocked | Narrow the exact Location input and repeat the same governed GET contract. | resolve_location_source |
| Create search evidence is the complete no-Costing pattern. | Valid | Continue on the Create branch. | resolve_location_source |
| Create search evidence is the complete matching active-Costing pattern. | Operation selection required | Show the existing allocation summary and require a new Update or Correct request; do not silently change the operation. | resolve_location_source |
| Create search evidence is partial, mismatched, or outside the selected date. | Blocked | Preserve the invalid pattern and stop; do not substitute a Generic Costing GET. | resolve_location_source |
| Update or Correct has no exact current parent. | Blocked | Stop before design or handoff. | query_location_costing |
| End Date lacks one complete terminal history or targets a non-latest split. | Blocked | Complete the paged history and select its exact latest effective parent. | query_location_costing_history |
| Zap lacks complete terminal history or one bound child expansion per history parent. | Blocked | Complete the history and detail fan-out. | query_location_costing_history_accounts |
| A populated account Segment has no current runtime descriptor. | Blocked | Correct the account input or KFF metadata before preview. This check does not apply to Zap. | resolve_runtime_costing_kff |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| End Date DAT shape | In the final CostAllocationV3.dat, require one parent METADATA and one matching MERGE, with ReplaceLastEffectiveEndDate exactly once as a METADATA attribute and Y in the corresponding MERGE column. Require equal column counts, the selected parent keys and dates, and the requested calendar EffectiveEndDate; reject #RETAIN, #ALL, and #NULL for that end date. Do not render account members. | End Date source validation before preview and handoff | |
| HDL SET instructions | Inspect every instruction in every final DAT member, not only METADATA headers. Reject every SET line for End Date. For other operations, accept only the exact SET command and arguments expressly required by this task's ora_defaulting_rules.md and ora_design_enforcement.md; reject unknown commands, aliases, unsupported arguments, and directives belonging to another operation before loading. | Every HDL source validation before preview and handoff | |
| Operation normalization | Delete Record And History becomes Zap; all other operation text must map to exactly one supported canonical operation. | Every request | |
| Lookup text safety | Accept logical text, spaces, Unicode, and apostrophes; reject carriage return, line feed, percent-encoded input, and finder grammar delimiters such as comma, semicolon, equals, or a vertical-bar character. Reject percent and underscore in LDG LIKE text and in user-supplied LocationName or arbitrary Location search text; the percent wildcard used by a supported Location list/filter mode is system-supplied, never user input. | User text used in a REST query | |
| Date shape | Parse one real calendar date and render it once in the format required by the receiving workflow. | Any supplied date | |
| Proportion | Convert a percentage once; each resulting value must be from 0 through 1 and the requested allocation total must not exceed 1. | Create, Update, or Correct account MERGE | |
| Account row shape | Require at least one populated Segment for a MERGE, reject vertical-bar or line-break characters that would alter a DAT row, and require current template coverage. | Account MERGE | resolve_runtime_costing_kff |
| Correct sequence | Require a positive integer and reject any conflict between user input and returned current state. | Correct account MERGE | query_location_costing |
| Clear token | Permit #NULL only for an explicit existing-account Correct MERGE clear that the current template accepts. | Any account value | |
| Destructive confirmation | Accept only the literal JSON boolean true; truthy strings and numbers do not pass. | End Date, Correct child DELETE, or Zap | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCP.VALIDATE_INPUT | decision | 10 | validate_input | valid->LCP.SELECT_OPERATION;invalid->LCP.HANDLE_ERROR | none | stop | Validate supplied values without invoking Fusion or building an import artifact. |
| LCP.SELECT_OPERATION | decision | 20 | evaluate_result | query->LCP.SEARCH_LDG;create->LCP.SEARCH_LDG;update->LCP.SEARCH_LDG;correct->LCP.SEARCH_LDG;end_date->LCP.SEARCH_LDG;zap->LCP.SEARCH_LDG;invalid->LCP.HANDLE_ERROR | LCP.VALIDATE_INPUT | stop | Select one canonical operation before any network call so later Task Nodes can follow only its branch. |
