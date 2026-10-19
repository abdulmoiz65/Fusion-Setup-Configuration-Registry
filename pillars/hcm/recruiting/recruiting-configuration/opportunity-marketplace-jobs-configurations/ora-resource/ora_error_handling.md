# Opportunity Marketplace Jobs Configurations Error Handling

Source: Opportunity Marketplace Jobs Configurations SKILL.md, adapted from the approved Gig Configuration create and copy contract.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required code, name, or eligibility profile is missing | Stop and request the missing value. |
| A copy request lacks an eligibility profile | List active unused Opportunity Marketplace eligibility profiles and require a selection; do not copy or select the source profile automatically. |
| A copy source is missing or ambiguous | Stop; do not derive _copy values or filters until exactly one source configuration is identified. |
| A copy request omits both code and name without approving the proposed _copy values | Stop and display the mandatory-values proposal for `<source_code>_copy` and `<source_name>_copy`; require approval or both replacement values. |
| The retained code conflicts or the eligibility profile is already assigned | Stop and require a unique code. When the eligibility profile is already assigned, list active unused profiles and require a selection. |
| A Job function or Recruiting Type display Meaning returns no exact match or multiple matches | Stop; do not select a value automatically; request a valid display value. |
| A valid location has no proven FSM geography-element tuple | Stop; do not serialize the LOV `CountryCode` as an element value or use generic `en` as an element-language code. Obtain the hierarchy tuple from current task data and regenerate the preview. |
| A generated availability-context identifier is blank, not 32 uppercase hexadecimal characters, reused, or incorrectly linked to its parent | Correct the generated identifiers and parent-child references, then generate a new preview. |
| The valid fresh export has zero Recruiting Type child data rows | Continue through the approved bootstrap rule in ora_defaulting_rules.md; persist DefaultFlag: N and reason: No Recruiting Type rows exist in the fresh Jobs Configuration export; applied approved bootstrap default. Do not block solely because a source DefaultFlag row is absent, and do not ask the user for DefaultFlag. |
| A populated fresh Recruiting Type member has no unambiguous established DefaultFlag | Stop for package-contract correction; do not apply the zero-row bootstrap or ask the user for DefaultFlag. |
| A candidate Recruiting Type DefaultFlag differs from the derived value or its decision evidence is missing | Reapply ora_defaulting_rules.md, correct the candidate and validation/preflight artifact, then regenerate the immutable preview and obtain approval. Never request a user-provided DefaultFlag. |
| The Recruiting Type member or DefaultFlag column is missing, malformed, or from a stale export | Stop for a valid fresh package; this is not a zero-row bootstrap case. |
| The export or candidate archive fails package preflight | Preserve the archive, correct it, and generate a new preview. |
| The import process fails | Preserve sanitized diagnostics and stop; do not retry or resubmit automatically. |
| Access is not authorized | Stop and route to the HCM Recruiting security owner. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input or required approval is absent | Request the missing value or exact approval. |
| CONFLICT | A SiteCode or EligibilityName is already used | Require a unique unused value. |
| AMBIGUOUS | A reference has multiple exact matches | Request a more precise valid value. |
| PREFLIGHT_FAILED | The candidate archive, child-row mapping, Recruiting Type row, or required defaulting evidence is invalid; zero source Recruiting Type rows alone are not a failure | Correct the archive or evidence before a new preview; use the approved bootstrap rule when applicable. |
| PROCESS_FAILED | core.data-loader reports an import or process failure | Preserve diagnostics and stop without retry. |
| AUTHORIZATION | Approved Fusion access is unavailable | Route to the HCM Recruiting security owner. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Code truncation | State that SiteCode was truncated to its first 200 characters before uniqueness validation. |
| Name truncation | State that SiteName was truncated to its first 100 characters before package generation. |
| Preview approval | Show only one Field/Value table with target environment, operation, task, code, name, type, sequence, eligibility profile, location, job family, organization, job function, and Recruiting Type. Do not show Source, generated technical identifiers, or translation, availability-context, or child-filter candidate rows. Show the archive fingerprint and ask whether to submit the reviewed archive. |
| Import failure | Show the failure classification, sanitized process diagnostic, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A Job Configuration create is requested | Do not use direct UI or REST creation; use a validated, approved FSM archive through core.data-loader only. |
| The archive changes after preview or approval | Do not upload or import it; generate a new preview and obtain new approval. |
| Import fails or its completion is uncertain | Do not automatically retry or resubmit. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JC.PREVIEW_IMPORT | decision | 60 | execution_gate | ready_for_approval->JC.IMPORT_READY;preflight_failed->JC.RETURN_ISSUES;approval_missing->JC.RETURN_ISSUES | JC.GENERATE_PACKAGE | stop | A candidate Job Configuration archive passed design enforcement |
| JC.IMPORT_READY | terminal | 90 | terminal | none | JC.PREVIEW_IMPORT | stop | An immutable preview is valid and the task is awaiting explicit import approval |
| JC.RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | A validation, dependency, lookup, design, preflight, or approval blocker occurs |
