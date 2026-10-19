# Country Security Profile Error Handling

Unsupported failures remain blocking.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A profile Name is unavailable or ambiguous | Stop before preview, CSV package generation, or import. For a rename, verify the old exact Name and supplied current ID first, then require zero exact matches for the proposed new Name. |
| A genuine rename has an available new Name | Report `rename CSV identity mapping unverified` and stop before CSV preview or import. Do not infer parent or child update keys from REST IDs or generated GroupingKeys. |
| Required profile or country CSV value is invalid | Classify as input validation and request the corrected value |
| No country is included in the profile | Classify as input validation and require at least one CountryName |
| Country lookup returns zero or multiple matches | Stop and request a disambiguating CountryName; do not invent a CountryCode |
| Profile lookup returns zero or multiple matches | Stop and request an unambiguous profile identity |
| A CSV package is missing a required template member or uses unsupported columns | Classify as an input validation error; regenerate from the current template export |
| A child logical row uses CountrySecurityProfileMigration, does not match the parent Name references, has a nonconforming GroupingKey, or reuses another new-row GroupingKey | Classify as a design-enforcement failure; rebuild the child row with CountrySecurityProfileCountryMigration, the exact parent Name references, and its own distinct generated GroupingKey; do not retry the package |
| A live create or update is requested | Require the current target-environment task-template CSV package, immutable ZIP preview, exact approval, one core.data-loader-authorized task-level CSV import, and process-log verification before reporting a result |
| A request or response failure is not documented by the supplied source | Stop and retain only sanitized diagnostics for source-authoring correction |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | A required field violates the describe contract | Correct the supplied input |
| Fusion API | The profile lookup fails | Stop and report sanitized diagnostics |
| input validation | A country association is missing or its CSV values do not match the supported template columns | Supply at least one CountryName and its resolved CountryCode in the template layout |
| catalog mismatch | A parent or child logical row does not use the template-supported ViewInstanceName mapping | Rebuild a new package and obtain new approval before import |
| transport/environment | A request or response failure is not documented by the supplied source | Stop and preserve sanitized diagnostics |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Blocked result | Task identity, failed rule, missing contract, and sanitized next action |
| Diagnostics | Do not expose credentials, tokens, or protected runtime data |
| Any response | Do not display internal IDs, including profile, child-row, lookup, process, request, content, or data-set identifiers; retain them only in sanitized internal evidence when needed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The supported CSV template is unavailable or does not match the package | Do not invent CSV columns, keys, or package metadata |
| No country is supplied or a CountryName does not resolve uniquely | Do not create a country security profile without a resolved country association |
| Profile identity is ambiguous | Do not select a profile by guesswork |
| Failure or result is uncertain | Do not retry or claim completion from the supplied describe contract alone |
| A direct REST create or update is requested | Do not send POST, PATCH, PUT, or DELETE to countrySecurityProfiles; prepare and approve a task-level CSV import instead |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.READY | terminal | 9 | terminal | none | CSP.READINESS | continue | All task-local validation, lookup, and readiness checks are ready |
| CSP.ERROR | step | 10 | error_handler | stopped->CSP.BLOCKED | none | stop | Any task-local validation, lookup, or readiness gate fails |
| CSP.BLOCKED | terminal | 11 | terminal | none | none | stop | The request is blocked after diagnostics |
