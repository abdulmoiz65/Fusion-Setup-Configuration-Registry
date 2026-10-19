# Opportunity Marketplace Gigs Configurations Error Handling

Source: Opportunity Marketplace Gigs Configurations SKILL.md and FSCR — Opportunity Marketplace Gigs Configuration.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required code or name is missing | Stop and request the missing value. |
| A copy request lacks an eligibility profile | List active unused Opportunity Marketplace eligibility profiles and require the user to select one; do not copy the source profile. |
| A copy source is missing or ambiguous | Stop; do not derive `_copy` values or filters until exactly one source configuration is identified. |
| A copy request omits both code and name without approving the proposed `_copy` values | Stop after displaying `Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Gig configuration. I am proposing the following values: <source_code>_copy and <source_name>_copy.` Require approval or both replacement values, then require an eligibility-profile selection. |
| The retained code conflicts | Stop and require a unique code. |
| The eligibility profile is already assigned | List active unused Opportunity Marketplace eligibility profiles and require the user to select one. |
| No active unused Opportunity Marketplace eligibility profile is available | Stop and report that no profile can be selected for the new configuration. |
| A reference lookup returns no exact match or multiple matches | Stop; do not select a value automatically. |
| A valid location has no proven FSM geography-element tuple | Stop; do not serialize the LOV `CountryCode` as an element value or use generic `en` as an element-language code. Obtain the hierarchy tuple from current task data and regenerate the preview. |
| A generated availability-context identifier is blank, not 32 uppercase hexadecimal characters, reused, or incorrectly linked to its parent | Correct the generated identifiers and parent-child references, then generate a new preview. |
| The export or candidate archive fails package preflight | Preserve the archive, correct it, and generate a new preview. |
| An approval request lacks a complete tabular candidate preview | Stop; show the root, translation, availability-context, and child-filter candidate rows using business values before requesting import approval. Keep generated identifiers internal. |
| The import process fails | Preserve sanitized diagnostics and stop; do not retry or resubmit automatically. |
| Access is not authorized | Stop and route to the HCM Recruiting security owner. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input or required approval is absent | Request the missing value or exact approval. |
| CONFLICT | A SiteCode or EligibilityName is already used | Require a unique unused value. |
| AMBIGUOUS | A reference has multiple exact matches | Request a more precise valid value. |
| PREFLIGHT_FAILED | The candidate archive or parent-child mapping is invalid | Correct the archive before a new preview. |
| PROCESS_FAILED | core.data-loader reports an import or process failure | Preserve diagnostics and stop without retry. |
| AUTHORIZATION | Approved Fusion access is unavailable | Route to the HCM Recruiting security owner. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Code truncation | State that SiteCode was truncated to its first 200 characters before uniqueness validation. |
| Name truncation | State that SiteName was truncated to its first 100 characters before package generation. |
| Preview approval | Show one `Field`/`Value` confirmation table with target environment, operation, task, code, name, type, sequence, eligibility profile, Location, Job family, Organization, and Job function; then show every candidate translation, availability-context, and child-filter row using business values, archive fingerprint, and import operation required for approval. Do not display generated technical identifiers. |
| Import failure | Show the failure classification, sanitized process diagnostic, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A Gig Configuration create is requested | Do not use direct UI or REST creation; use a validated, approved FSM archive through core.data-loader only. |
| The archive changes after preview or approval | Do not upload or import it; generate a new preview and obtain new approval. |
| Import fails or its completion is uncertain | Do not automatically retry or resubmit. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GC.PREVIEW_IMPORT | decision | 60 | execution_gate | ready_for_approval->GC.IMPORT_READY;preflight_failed->GC.RETURN_ISSUES;approval_missing->GC.RETURN_ISSUES | GC.GENERATE_PACKAGE | stop | A candidate Gig Configuration archive passed design enforcement and its submitted rows are presented in clear tables |
| GC.IMPORT_READY | terminal | 90 | terminal | none | GC.PREVIEW_IMPORT | stop | An immutable tabular preview is valid and the task is awaiting explicit import approval |
| GC.RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | A validation, dependency, lookup, design, preflight, or approval blocker occurs |
