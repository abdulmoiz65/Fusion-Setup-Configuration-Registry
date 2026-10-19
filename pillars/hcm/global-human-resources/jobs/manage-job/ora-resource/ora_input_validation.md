# Manage Job Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Job.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, inactivate, or delete-effective-split | Block | Provide one supported operation | Every request |  |
| Existing job selector | Exact JobId, JobCode with set context, or exact JobName with set context | Block | Provide one exact business selector | get, edit, inactivate, or delete-effective-split | find_manage_job |
| Create identity | JobCode and Name | Block | Provide both values | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | Every mutation |  |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |
| Inactivation context | Exact existing job and ActiveStatus `I` | Block | Resolve the target row and provide the inactive status | inactivate | find_manage_job |
| Effective-split deletion range | Exact existing Job, retained EffectiveStartDate, and last deleted EffectiveEndDate | Block | Resolve the complete affected history and provide the inclusive deletion range | delete-effective-split | resolve_job_delete_history |
| Delete confirmation | Explicit confirmation of the displayed effective-split range | Block loader handoff | Show basic details and request confirmation | delete-effective-split | resolve_job_delete_history |
| Translation identity | Language, translated Name, and a date aligned with the base row | Block | Provide the translation values | A translation is requested |  |
| Job EFF row | Generated `FLEX:` discriminator and every configured multirow unique-key segment | Block | Complete the EFF row from the current loader contract | A Job EFF row is supplied |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing target does not resolve to exactly one effective job in its set | Missing | Request one exact ID or set-scoped code or name | find_manage_job |
| A create JobCode already exists in the selected set | Invalid | Stop the duplicate create | find_manage_job |
| The selected reference-data set is unresolved or unsupported | Invalid | Correct the set | resolve_job_reference_data_set |
| A supplied Job Family is unresolved, ineffective, ambiguous, or incompatible with the selected set | Invalid | Correct the Job Family or set | resolve_job_family_for_job |
| A supplied Job Subfamily is unresolved, ineffective, or incompatible with the resolved Job Family | Invalid | Correct the Job Subfamily | resolve_job_subfamily_for_job |
| A supplied valid grade does not already exist | Invalid | Create or correct the grade before loading the job | resolve_job_grade |
| A supplied benchmark job does not resolve to another eligible job | Invalid | Correct the benchmark reference | find_manage_job |
| The Job deletion history is missing, ambiguous, includes the first split, or does not support the requested boundaries | Invalid | Resolve a valid retained start and inclusive deletion end from Job history | resolve_job_delete_history |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Accept common numeric and written date formats. Normalize each valid value to the loader date format; resolve an ambiguous numeric date using the user's stated locale, then the workspace locale when it is known. Show the normalized ISO date in the deletion preview for confirmation. Reject only an invalid date or an ambiguous numeric date when no locale can be determined. | A date is supplied |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Job row and every included child row | Every mutation |  |
| Effective range | Reject an EffectiveEndDate earlier than EffectiveStartDate | Both dates are supplied |  |
| Date-effective history | Require the same JobCode and SetCode on every row, with consecutive nonoverlapping ranges; allow the latest EffectiveEndDate to be blank or `4712/12/31` | A create supplies multiple effective rows |  |
| Set-scoped code | Require JobCode to be unique within the resolved SetCode | create or code change | find_manage_job |
| Primary field lengths | Reject JobCode or SetCode longer than 30 characters, or Name longer than 240 characters | A listed value is supplied |  |
| Active status | Accept only `A` or `I` | ActiveStatus is supplied |  |
| Benchmark exclusivity | Reject BenchmarkJobId or BenchmarkJobCode when BenchmarkJobFlag is Yes | A benchmark job is authored |  |
| Benchmark self-reference | Reject a benchmark reference that identifies the job being authored | A benchmark reference is supplied |  |
| Translation alignment | Require translation effective dates to match a base-language effective row | A translation is requested |  |
| Date-effective split deletion | Allow deletion of one or more noninitial future effective splits only with a Job `MERGE` row and exactly one `SET PURGE_FUTURE_CHANGES Y` directive. Require the resolved JobCode and SetCode identity, EffectiveStartDate to identify the last record to retain, and EffectiveEndDate to identify the last record to delete. Reject an HDL `DELETE`, first-row deletion, and an unbounded or misaligned range. | delete-effective-split | resolve_job_delete_history |
| JobLegislative EFF | Require `FLEX:PER_JOBS_LEG_EFF` to contain the deployed context code | A JobLegislative row is supplied |  |
| Job EFF child create shape | Require every parent-link field, context identity field, effective boundary, multirow key, and fixed/default value declared by the current child template and describe; copy base Job identity only into matching child fields and reject a partially populated child row | A new Job includes JobLegislative or JobExtraInfo | read_job_eff_context |
| JobExtraInfo EFF | Require `FLEX:PER_JOBS_EIT_EFF` to contain the deployed context code | A JobExtraInfo row is supplied |  |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow Job EFF context is supplied |  |
| EFF value set | Resolve a supplied value through the current segment LOV contract using the Job EffectiveStartDate | A supplied Job EFF segment declares a value set | resolve_job_eff_value_set |
| Supported fields | Reject response-only IDs, audit fields, links, and fields absent from the registered Job loader contract | A mutation value is supplied |  |
| Mutation source scope | Keep the Job worksheet, map entry, and base row for create, edit, or inactivate; include JobEvaluation, JobGrade, JobExtraInfo, and JobLegislative only when explicitly modified. For delete-effective-split, keep only the resolved JobCode and SetCode, retained EffectiveStartDate, inclusive EffectiveEndDate, and one supported purge directive; omit child rows and non-key attributes. | create, edit, inactivate, or delete-effective-split |  |
| Verification boundary | Do not treat source generation, transport, or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB.VALIDATE | decision | 1 | validate_input | valid->JOB.READ;missing->JOB.ERROR;invalid->JOB.ERROR;unsupported->JOB.ERROR | none | stop | Every Manage Job request |
