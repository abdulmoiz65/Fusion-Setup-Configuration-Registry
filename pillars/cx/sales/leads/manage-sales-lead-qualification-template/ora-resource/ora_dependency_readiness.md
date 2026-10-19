# Dependency Readiness

Source basis: Oracle Fusion Cloud Sales, *Create a Lead Qualification Template*
and *Lead Qualification Templates*.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment and task support | Confirm the target identity, release, task code, catalog flags, export privilege, and project destination |
| 2 | Fresh current-data reference export | Complete and validate the task export before inventory, duplicate reconciliation, or package generation |
| 3 | Qualification design | Obtain business approval for the question groups, questions, responses, rating model, weights, and feedback |
| 4 | Reference-data-set scope | Select the template set whose business-unit coverage matches the intended users |
| 5 | Optional task templates | Confirm any task templates before associating them with score outcomes |
| 6 | Data Loader handoff | Bind the final validated package and SHA-256 to the selected task context so Data Loader can build its own immutable preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| target_environment | Verified Fusion environment and supported task | Yes | Always and the environment, release, task code, supported export/import flags, required privilege, and safe project path are confirmed | Satisfied | Environment preflight and effective setup-task catalog | | Prevents exporting from or importing to an unintended or unsupported environment | Correct the environment or privilege before continuing | EnvironmentIdentity, EnvironmentUrl, FusionRelease, TaskCode, catalog flags, project path |
| current_reference_export | Fresh validated current-data task export | Yes | Create, Copy, Review, or Deploy-readiness and the current-data export completed for the verified target environment | Satisfied | shared.setup-export.task-level-export output | | The target environment owns the authoritative CSV schema, metadata, template inventory, and relationship contract | Run the automatic export; use an offline ZIP only after the documented explicit fallback decision | ExportProcessId, ZIP path, ZIP SHA-256, ProcessEnv, ProcessRelease, ExportedAt, inventory count |
| qualification_design | Approved qualification questionnaire | Yes | Create or Copy and the questionnaire is supplied and approved | Satisfied | User-confirmed implementation design | | The template requires ratings, grouped questions, weighted questions, responses, scores, and feedback | Provide the approved questionnaire model | Rating definitions, question groups, questions, weights, responses, scores, feedback |
| reference_data_set | Reference-data set for template availability | Yes | Create or Copy and the set and intended business-unit scope are confirmed | Satisfied | User-confirmed implementation design | | The template set controls which business units can use the qualification template | Confirm the set and its intended business-unit coverage | TemplateSet, intended business units |
| task_template_association | Existing task template association | Conditional | Task recommendations are requested and every associated task template is identified | Satisfied | User-confirmed implementation design | | Associated task templates can recommend follow-up tasks based on the qualification result | Provide each task-template name or omit task-template association | Task template names |
| data_loader_handoff | Final validated package and task context | Conditional | Create or Copy import handoff and TaskContextPath, TaskName, positive TaskSequence, PackagePath, PackageSha256, finalData.archiveSha256, row counts, duplicate evidence, and validation results all refer to the same archive and design | Satisfied | core.data-loader Task Hook contract | | Prevents an unvalidated or changed ZIP from reaching Data Loader preview generation | Rebuild task validation after any package or design change; Data Loader obtains standalone approval later | TaskContextPath, TaskName, TaskSequence, PackagePath, PackageSha256, finalData.archiveSha256, validation results |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every mandatory dependency for the requested operation is confirmed | Yes; continue to read-only lookup and hand the final archive to Data Loader for its separate preview and approval lifecycle |
| Missing | A mandatory design or reference-data-set decision is absent | No |
| Conditional | Optional task recommendations or an import are not requested | Yes, within the operation-specific route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LQT.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->LQT.LOOKUP_TEMPLATE;missing->LQT.RETURN_ISSUES | LQT.VALIDATE | stop | Require target-environment and fresh-export readiness for the requested operation; require questionnaire, set-scope, optional associations, and Data Loader handoff only for Create/Copy; never require a package for Review/Deploy-readiness and never authorize Deploy mutation |
