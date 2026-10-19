# Time Rule Templates Dependency Readiness

Source: Supplied Time Rule Templates ASM_SETUP_CSV_METADATA.xml, the CSV template reports, the task metadata declaring CSV export and import support, and the user-required end-to-end FSM CSV import route through core.data-loader.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Time Rule Templates export | Refresh and read the parent, input, usage, and applicable translation CSV objects before matching |
| 2 | Fresh package contract | Use the fresh export for exact object headers and `ASM_SETUP_CSV_METADATA.xml`; prepare create rows from normalized intent and update rows from the verified current graph plus the explicit change set |
| 3 | ORA_HWM_RULE_TMPLT parent | Prepare the parent before inputs, usages, or translations |
| 4 | ORA_HWM_RULE_TMPLT_INPUT children | Prepare ordered input rows for their exact template parent |
| 5 | ORA_HWM_RULE_TMPLT_USAGE children | Prepare ordered usage rows for their exact template parent |
| 6 | Translation children | Prepare only applicable translation rows after their parent path exists |
| 7 | Data Loader validation and preview | Build one minimal immutable FSM CSV ZIP, validate TaskCode ORA_HWM_MANAGE_RULE_TEMPLATES through core.data-loader, and display the exact archive SHA-256 and create or update operation |
| 8 | Complete Summary | Generate the business-only Complete Summary and Defaults Applied details from verified values and defaults actually applied; omit blank, null, unused, metadata-only, and technical package values |
| 9 | Validated package link | Display a clickable link to the exact validated FSM ZIP outside the business summary |
| 10 | Explicit import approval | Bind approval to the exact proposal, dependent Time Rule relationship when supplied, target environment, immutable archive SHA-256, and core.data-loader preview |
| 11 | Data Loader import | Route the approved archive through core.data-loader for upload, initiation, monitoring, and terminal-result retrieval; do not call a direct FSM import adapter or invent a direct REST write |
| 12 | Import verification | Refresh the authoritative export and verify the approved parent, inputs, usages, and applicable translations before releasing the template for Time Rule use |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TIMETMPLT.CURRENT_EXPORT | Complete current Time Rule Templates setup-task export from the target Fusion environment | Yes | Before every compatibility lookup | Lookup | User-authorized current setup-task export | find_compatible_time_rule_template | Matching must use authoritative current functional configuration | Refresh all parent, child, and applicable translation CSV objects together | Match category, TemplateName, formula, inputs, outputs, behavior differences |
| TIMETMPLT.SCHEMA_CONTRACT | Current CSV schema and metadata contract | Yes | When preparing a package | Verify | Fresh Time Rule Templates export | read_template_schema_contract | A prepared package can omit supported fields or alter explicit blank, zero, or null literals without a current schema contract | Use current headers and unchanged metadata; prepare create rows from normalized intent and update rows from the verified graph and explicit change set, then validate row width and links | Fresh export identity; headers; metadata identity; field-state validation evidence |
| TIMETMPLT.BATCH_ORDER | Parent and child CSV processing order | Yes | When preparing a CSV package | Satisfied | Supplied ASM_SETUP_CSV_METADATA.xml |  | The metadata defines the parent and translation node at sequence 1, inputs at sequence 2, and usages at sequence 4 in the TimeRuleTemplate batch | Preserve parent-before-child order and exact alternate-key paths | ORA_HWM_RULE_TMPLT, ORA_HWM_RULE_TMPLT_INPUT, ORA_HWM_RULE_TMPLT_USAGE, applicable translations |
| TIMETMPLT.CREATE_OR_UPDATE | Approved Time Rule Template FSM import and refreshed-export verification | Conditional | A user-confirmed exact-match create, no fully compatible template, or an existing template update is requested | Import with Approval | Exact proposal, immutable BOM-free CSV ZIP, validated business-only Complete Summary and Defaults Applied details, task metadata declaring CSV import support, and core.data-loader |  | Creates and updates are setup-data CSV imports and must be verified before a dependent Time Rule can use the result | Validate the package through core.data-loader, generate the business-only summary, link the immutable archive, approve its preview, submit it once through Data Loader, and stop if import or verification fails | Verified TemplateName, RuleTmpltsId when exported, normalized template behavior, business summary, archive SHA-256, process result, verification evidence |
| TIMETMPLT.FINAL_COMPLETION | Task-authorized asynchronous status monitoring and read-back verification | Yes | An approved Time Rule Templates create, update, import, load, or documented dependent submission is accepted | Verify | Accepted request identity, approved immutable artifact, core.data-loader status route, authoritative Time Rule Templates export, and active workflow context | monitor_and_verify_approved_async_time_rule_template_request | Submission acceptance alone is not final success | Immediately issue the initial task-authorized status request; while the status is In progress or not yet available, issue follow-up status requests. On documented terminal success, read back and verify supported approved template values, label only defaults as Default, and present standalone results when no one active documented parent exists. When exactly one active documented parent establishes this task as a prerequisite, retain its identity and safe resume stage, state that the prerequisite is verified and ready to resume it, and ask “Would you like to resume {parent workflow}?” Return `resume_requested` only after confirmation. | Accepted request ID, terminal status, read-back evidence, verified values, defaulted values, parent identity and safe resume stage when applicable, mismatch or failure evidence |
| TIMETMPLT.FSM_IMPORT_ROUTE | Mandatory FSM CSV import route | Yes | Before every live create or update | Ready | core.data-loader, immutable validated Time Rule Templates CSV ZIP, and exact import approval |  | A direct REST create or update endpoint is not required when the supported FSM CSV route is available | Do not upload or initiate until the exact core.data-loader preview is approved; never invoke the FSM adapter directly | TaskCode=ORA_HWM_MANAGE_RULE_TEMPLATES, archive path, SHA-256, task-validation envelope, import result, verification evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Exact matches disclosed | One or more verified templates support every applicable requested characteristic | Show every candidate and ask whether the user still wants a new template |
| Confirmed exact-match create | The user confirms a new template after disclosure | Build the normalized requested configuration against the fresh schema, validate the immutable archive, then require exact import approval |
| Partial match | At least one applicable characteristic is missing, conflicting, or unverified | Lookup complete; automatic reuse blocked |
| No match | No fully compatible template exists | Proposal and FSM CSV package may be prepared; import waits for exact core.data-loader preview approval |
| Lookup failure | The authoritative export cannot be read or normalized | No selection, proposal import, or creation is allowed |
| Blocked | Data Loader route, package validation, immutable preview approval, import result, or refreshed-export verification is missing | No live create or update and no dependent Time Rule use is allowed |
| Final completion monitoring | An approved asynchronous request is In progress or not yet available | Continue task-authorized status requests until a documented terminal status; do not request separate user status authorization or submit again |
| Parent context required | Parent contexts are multiple, conflicting, stale, incomplete, or undocumented | Stop and ask the user to identify the intended workflow; do not infer a handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMETMPLT.CREATE_DEPENDENCY | step | 4 | resolve_dependency | ready->TIMETMPLT.COMPLETE_SUMMARY;blocked->TIMETMPLT.DEPENDENCY_ERROR | TIMETMPLT.PROPOSAL_GATE | stop | A complete create or update proposal exists and its immutable FSM CSV ZIP must be validated and previewed through core.data-loader |
