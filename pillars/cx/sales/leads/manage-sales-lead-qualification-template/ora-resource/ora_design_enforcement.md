# Design Enforcement

Source basis: Oracle Fusion Cloud Sales, *Create a Lead Qualification Template*,
*Lead Qualification Templates*, and the environment-bound task CSV export
required by this skill.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm evidence freshness | Use the current run's validated target-environment export and live lookup |
| 2 | Confirm template identity | Reconcile the operation-specific exact-name result before creating or changing a template |
| 3 | Isolate the package | Retain exactly one proposed Lead template and its dependency closure with new identifiers |
| 4 | Confirm availability scope | Verify that the selected template set represents the intended business units |
| 5 | Review the scoring model | Confirm ratings, response scores, feedback, score ranges, and total question weight form one coherent model |
| 6 | Protect deployed templates | Use a copy when a deployed template requires changes to locked attributes |
| 7 | Bind final archive | Require package design and SHA-256 to remain unchanged through Data Loader Task Hook validation; Data Loader owns the later approval |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LQT.DESIGN.EVIDENCE | Create, Copy, or Review | Error | reconcile_lead_template_name_evidence | The reference export is stale, belongs to another environment or release, changed after inventory, or disagrees with the live lookup | Run a fresh current-data task export and repeat inventory and exact-name reconciliation | Yes, before preview |
| LQT.DESIGN.CREATE_NAME | Create | Error | find_assessment_template_by_exact_name | Either evidence source contains an exact Lead qualification-template name match | Choose a new name or use Copy with a distinct new name | Yes, before preview |
| LQT.DESIGN.EXISTING_TARGET | Copy, Review, or Deploy-readiness | Error | find_assessment_template_by_exact_name | Exactly one consistent Lead qualification template was not resolved | Correct the template name or business-unit context | Yes, before review or preview |
| LQT.DESIGN.PACKAGE_ISOLATION | Create or Copy | Error | inventory_lead_templates_from_reference_export | The package contains an existing template, an unrelated setup record, inherited audit values, reused identifiers, or more than one proposed template | Rebuild from fresh export headers and relationships with new identifiers and only the proposed template dependency closure | Yes, before preview |
| LQT.DESIGN.SET_SCOPE | Create or Copy | Error | | The selected template set does not represent the intended business-unit availability | Select the reference-data set that owns the intended business units; use Common Set only when enterprise-wide availability is explicitly intended | Yes, before preview |
| LQT.DESIGN.SCORING | Create, Copy, or Deploy-readiness | Error | | Ratings, response scores, feedback, score ranges, or question weights do not form the reviewed qualification model, or total question weight is not exactly 100 | Correct the rating, response, weight, and score-range design before package preview or readiness review | Yes, before preview or review |
| LQT.DESIGN.DEPLOYED_COPY | A deployed template needs a locked attribute changed | Error | find_assessment_template_by_exact_name | The plan attempts to edit the deployed template directly | Copy the deployed template and import the copy through Data Loader; actual deployment remains blocked until a validated FSM deployment contract exists | Yes, through Copy only |
| LQT.DESIGN.MUTATION_ROUTE | Any requested create, copy, update, or deploy side effect | Error | | The operation would use Fusion REST, browser automation, assisted Setup and Maintenance, or an importer outside core.data-loader | Use a validated export-derived FSM package through core.data-loader; if the FSM contract cannot represent the operation, refuse it | No |
| LQT.DESIGN.IMMUTABLE_ARCHIVE | Create or Copy Data Loader handoff | Error | | The package SHA-256, finalData.archiveSha256, reference export hash, row counts, template design, duplicate evidence, or environment differs from the final validated archive evidence | Revalidate the final archive and restart Data Loader Task Hook preview generation; Data Loader obtains approval after this graph | Yes, before Data Loader preview |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| LQT.DESIGN | inventory_lead_templates_from_reference_export | Before Create, Copy, Review, or Deploy-readiness | Reference ZIP SHA-256, inventory count, Name, AssessTemplateNumber, SetId, StatusCode, exact match count | ora_reference_lookups.md |
| LQT.DESIGN | find_assessment_template_by_exact_name | Before every supported operation | AssessTemplateId, Name, AssessedObjTypeCode, ObjectVersionNumber, exact match count | ora_reference_lookups.md |
| LQT.DESIGN | reconcile_lead_template_name_evidence | Before Create, Copy, Review, or Deploy-readiness routing | Exported exact match count, live exact match count, evidence timestamps, stale-evidence flag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LQT.DESIGN | decision | 5 | design_enforcement | pass->LQT.EXECUTION_GATE;fail->LQT.RETURN_ISSUES | LQT.ROUTE | stop | Before final Create/Copy Data Loader handoff or read-only Review/Deploy-readiness output |
