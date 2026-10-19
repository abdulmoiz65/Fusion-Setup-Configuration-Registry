# Manage Sales Methods and Sales Stages Input Validation

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use these task-scoped rules for Manage Sales Methods and Sales Stages under the
Opportunities functional area. The source basis is Oracle's
[Manage Sales Methods and Stages](https://docs.oracle.com/en/cloud/saas/sales/fadsi/manage-sales-methods-and-stages.html)
guidance plus a fresh same-target task export for exact CSV members, headers,
current method and stage values, `StageNumber`, and `PhaseCd` evidence.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Sales method | Operation, Name, optional Description, SetSelectionDecision, exact SetId or SetCode when a different set is selected, optional Close Window, Sales Motion | Ask whether Common Set should be used or a different exact Set ID or Set Code should be selected; other missing fields may use a review-only proposal | Preserve an exact current set only for an identified update target; otherwise require explicit Common Set confirmation or a different exact set identity, then use normal review-draft precedence for remaining values | Creating or editing a sales method |  |
| Sales stages | Name, required PhaseCd for every CSV stage row, optional Description, Status, Order, Quota Factor, Disable, Win Probability, optional Duration for Classic Sales, optional Additional Required Fields | Generate a complete review-only proposal | Populate every applicable field from user input, exact current baseline, documented defaults, then the synthetic sample profile; show non-applicable fields explicitly and block import until reviewed | Creating or editing stages |  |
| Immutable FSM package handoff | Exact target and release, TaskCode fixed to MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES, TaskName fixed to Manage Sales Methods and Sales Stages, selected skill path, final package path and reopened SHA-256, fresh same-target exact-task export receipt, exact ASM ObjectShortName identity, complete member inventory, exact headers and order, reviewed method/stage delta, current-state lock, dependency and unrelated-row preservation, validation result, persisted TaskContextPath, and positive TaskSequence | Block Core Data Loader handoff | Refresh the exact task export, rebuild the smallest reviewed delta, reopen the ZIP, validate its final bytes and exact task identity, and resolve the persisted project context to the exact selected skill/task | FSM package is ready for Core Data Loader | verify_sales_methods_final_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| Quota Factor is supplied | Accept for preview; Oracle requires an entry even though it is used only for legacy reports | Validating a sales stage |  |
| PhaseCd is blank on any MOO_SALES_STAGE.csv row | Reject package readiness and list every affected stage row; PhaseCd is required for Redwood and Classic CSV imports | Validating an immutable CSV package |  |
| PhaseCd is supplied on every MOO_SALES_STAGE.csv row | Preserve the exact reviewed or target-baseline code in the immutable package | Validating an immutable CSV package |  |
| StageNumber is blank or duplicated on a create-stage row | Reject package readiness; list every affected stage row and require a unique nonblank StageNumber before Core Data Loader handoff | Validating an immutable CSV package |  |
| ASM_SETUP_CSV_METADATA.xml is missing, hand-authored, minimized, or lacks the fresh same-target export's complete business-object and migration-object metadata graph | Reject package readiness; do not infer CSV-to-business-object mapping from filenames alone | Validating an immutable CSV package |  |
| ZIP member names, member count, or CSV headers differ from the fresh same-target task export | Reject package readiness; retain every exported member and its exact header, using header-only child files when no approved child rows are needed | Validating an immutable CSV package |  |
| Complete export-derived metadata graph, member list, and headers match the fresh same-target export | Continue package validation; modify only the approved data rows and preserve the FSM contract | Validating an immutable CSV package |  |
| TaskCode, target, release, exact TaskName, final package path, reopened SHA-256, exact ASM ObjectShortName identity, complete member/header receipt, reviewed row delta, current-state lock, or dependency/unrelated-row preservation is missing or inconsistent | Reject handoff; correct the package or task binding and rerun executable package validation | Before every Core Data Loader handoff | verify_sales_methods_final_package |
| TaskContextPath is blank or TaskSequence is nonpositive | Reject handoff; generate or refresh the persisted project task context from the resolved setup-task plan | Before every Core Data Loader mutation handoff | verify_sales_methods_final_package |
| The persisted context does not resolve to this exact skill path, TaskCode, TaskName, offering, and functional area | Reject handoff; correct the project task mapping and refresh its planning artifacts; never hand-author or synthesize a context entry | Before every Core Data Loader mutation handoff | verify_sales_methods_final_package |
| A package approval or Task Hook approval is requested by this child skill before handoff | Refuse the child-level approval gate; hand the validated immutable package to Core Data Loader, which creates the Task Hook-bound preview and later requests standalone approve | Before Core Data Loader handoff |  |
| Duration is supplied | Accept only for a Classic Sales implementation | Validating a sales stage |  |
| One or more applicable values are absent at initial intake | Continue to a review-only draft and record provenance for every populated value | Drafting before user review |  |
| One or more values remain assumed for review | Present the full proposal, but reject import readiness until the user approves or corrects every assumption | Reviewing a generated proposal |  |
| Set is absent and the user has not confirmed Common Set or selected a different exact SetId or SetCode | Stop the set-dependent draft and ask one explicit choice: use Common Set, or provide a different exact Set ID or Set Code | Creating a new sales method or changing its set |  |
| Common Set is inserted from a documented product default, synthetic sample, environment convention, or implementation assumption without user confirmation | Reject the inferred value and return to the explicit set-choice question; Common Set confirmation does not authorize import | Drafting, package preparation, or review |  |
| SetId is malformed/nonpositive, SetCode is blank, SetId and SetCode identify different sets, or confirmed Common Set is paired with a non-Common set identity | Reject the set-dependent draft or package; show the conflicting sanitized values and request one valid explicit set decision | Drafting, package preparation, review, or handoff | verify_sales_methods_final_package |
| A sales-method package row's set differs from the confirmed choice, identified update target, fresh baseline, or selected target environment | Reject package readiness as a set identity/scope mismatch; never replace it with Common Set, another environment's set, or a close match | Validating an immutable CSV package | verify_sales_methods_final_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_METHODS.VALIDATE | step | 1 | validate_input | complete->OPP.SALES_METHODS.DEFAULT;incomplete->OPP.SALES_METHODS.DEFAULT;invalid->OPP.SALES_METHODS.RETURN_FAILED | none | stop | Every sales-method or sales-stage setup request; incomplete non-set intake may continue to a review-only draft, but missing, malformed, unknown, or conflicting set identity must be returned to the user |
