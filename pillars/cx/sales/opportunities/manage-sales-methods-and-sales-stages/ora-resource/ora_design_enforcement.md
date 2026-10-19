# Manage Sales Methods and Sales Stages Design Enforcement

These rules preserve documented Sales behavior and prevent unrelated runtime
product-line concepts from being treated as setup metadata.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Validate sales-method design | Confirm set usage, stage order, statuses, quota factors, and win probabilities |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| A stage represents an opportunity still in progress | Blocker |  | Stage status is not Open | Use Open for every in-progress stage | Yes |
| An existing sales method is unused | Blocker |  | The design attempts to delete the sales method | Disable the unused method because created methods cannot be deleted | Yes |
| A sales stage has already been used by opportunities | Blocker |  | The design disables that stage | Retain the used stage and design a replacement without disabling historical use | Yes |
| Forecast inclusion depends on win probability | Warning |  | Stage win probabilities do not support the approved forecast threshold | Review default stage probabilities so eligible opportunities are not omitted accidentally | Yes |
| A review-only proposal contains assumed values | Blocker |  | The proposal is used for import before every assumption is approved or corrected | Present all values and provenance in one review request; regenerate validation after any correction | Yes |
| A new sales method or set change is drafted or reviewed | Blocker |  | Set selection is absent; Common Set was inferred or paired with a supplied non-Common identity; SetId is malformed/nonpositive; SetCode is blank; supplied SetId/SetCode conflict; or a different set lacks an exact Set ID or Set Code | Ask whether Common Set should be used or a different set should be selected; preserve one confirmed exact choice and do not treat set confirmation as mutation approval | Yes |
| A sales-method package is prepared or handed off | Blocker | verify_sales_methods_final_package | The confirmed set is unknown in exact-target evidence, cross-environment, or differs from the identified update target, fresh baseline, or package row | Reconfirm one exact set, rebuild the package from the fresh exact-target export, and reject rather than substitute a set | Yes |
| Any stage will be written to MOO_SALES_STAGE.csv | Blocker |  | PhaseCd is blank on one or more stage rows | Show every affected stage row and supply a reviewed or exact target-baseline PhaseCd before package validation | Yes |
| A create-stage row will be written to MOO_SALES_STAGE.csv | Blocker |  | StageNumber is blank or duplicates another submitted StageNumber | Assign one stable, unique StageNumber per stage; rebuild, validate, checksum, and hand the corrected immutable package to Core Data Loader | Yes |
| An FSM CSV package is prepared | Blocker |  | ASM_SETUP_CSV_METADATA.xml, the member graph, or CSV headers were hand-authored, minimized, or differ from a fresh same-target export | Re-export the task, preserve the complete metadata XML and all exported member headers, retain header-only unused child CSVs, rebuild, validate, checksum, and hand off the immutable package | Yes |
| A reviewed stage PhaseCd changes during package preparation | Blocker |  | The immutable package no longer matches the approved design | Rebuild and revalidate the package, recalculate its SHA-256, and restart the Core Data Loader preview lifecycle | Yes |
| An immutable FSM package is ready for handoff | Blocker |  | Exact target/task identity, reopened package SHA-256, fresh export receipt, complete metadata/member/header graph, reviewed row delta, task-local validation result, persisted TaskContextPath, positive TaskSequence, or exact context-to-skill/task resolution is missing or inconsistent | Correct and revalidate the complete package, generate or refresh the project task context from its resolved setup-task plan, and require that context to resolve to this exact skill/task before handing it to Core Data Loader; never hand-author or synthesize context | Yes |
| Before Core Data Loader handoff | Blocker |  | This child skill requests package approval, constructs a Task Hook approval, or treats design review as upload authorization | Hand off only the validated immutable package; Core Data Loader creates the Task Hook-bound preview and later requests standalone approve | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_sales_methods_final_package | Package preparation or handoff includes a sales-method set identity | SetSelectionDecision, exact SetId/SetCode, target/baseline/package-row agreement, immutable package receipt | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_METHODS.DESIGN | decision | 3 | design_enforcement | review_ready->OPP.SALES_METHODS.RETURN_READY;package_candidate->OPP.SALES_METHODS.PACKAGE_READY;blocked->OPP.SALES_METHODS.RETURN_MISSING | OPP.SALES_METHODS.DEFAULT | stop | Validate the complete proposal, including wrong or conflicting set identity; return a reviewed design when no package exists, or send a final package candidate through executable readiness before handoff |
