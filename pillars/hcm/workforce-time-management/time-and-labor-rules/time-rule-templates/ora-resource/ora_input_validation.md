# Time Rule Templates Input Validation

Source: User-provided template-first Time Rule authoring requirements, the required FSM CSV import route through core.data-loader, and the supplied Time Rule Templates ASM_SETUP_CSV_METADATA.xml, ORA_HWM_RULE_TMPLT, ORA_HWM_RULE_TMPLT_INPUT, ORA_HWM_RULE_TMPLT_USAGE, and translation CSV template reports.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Normalized template capability request | Requested condition, calculation behavior, RuleType or Classification, FormulaName and FormulaId, ProcessType, RuleExecType, TemplateType, required inputs and parameters, required outputs and usages, RunSummationLevel, RunTbbLevel, Time Category handling, result or payroll time-type behavior, and effective context | Stop before compatibility matching | Capture every applicable characteristic and identify any characteristic not represented by the current export | Always | find_compatible_time_rule_template |
| Template update identity | Exact existing TemplateName, current exported parent and child configuration, proposed changed fields, and unchanged fields to preserve | Stop before update proposal or package preparation | Resolve exactly one current exported template and calculate the explicit before-and-after change set | An existing Time Rule Template update is requested | find_compatible_time_rule_template |
| User-confirmed template create | Candidate disclosure, explicit confirmation to create despite one or more exact functional matches, requested new TemplateName, and normalized requested values | Do not prepare a package | Show every exact match and require confirmation to create; do not select or copy a source record | A requested create has one or more exact functional matches | find_compatible_time_rule_template |
| Template proposal | TemplateName, Description, Classification, TemplateType, ProcessType, FormulaName, FormulaId, RuleExecType, RunSummationLevel, RunTbbLevel, EffectiveStartDate, EffectiveEndDate, ordered inputs and parameters, ordered outputs and usages, Time Category handling, and result or payroll time-type behavior | Do not request approval and do not prepare an import | Complete the proposal from authorized source data and clearly mark unresolved fields | No fully compatible template exists | |
| Approval-bound proposal identity | Target Fusion environment, normalized template proposal, intended create operation, dependent Time Rule proposal when supplied, and proposal fingerprint | Treat approval as missing | Display the complete proposal and obtain explicit approval for the exact fingerprint | A new template is required | |
| Business-only approval summary | Every verified user-provided business value and every default actually applied, using business labels and populated child sections only | Do not link the package or request approval | Generate Complete Summary and Defaults Applied after package validation; omit blank, null, unused, metadata-only, and technical package values | Every live create or update | |
| FSM CSV import identity | TaskCode=ORA_HWM_MANAGE_RULE_TEMPLATES, TaskName=Time Rule Templates, operation=create or update, immutable CSV ZIP path, archive SHA-256, and core.data-loader task-validation envelope | Do not create an approval preview or submit an import | Prepare the setup-data CSV package for the exact task, validate it through core.data-loader, and bind the preview to the immutable archive | Every live create or update | |
| CSV package encoding and first headers | Every Time Rule Templates CSV file is UTF-8 without a byte-order mark; the exact first header is TemplateName for ORA_HWM_RULE_TMPLT.csv and ORA_HWM_RULE_TMPLT.TemplateName for ORA_HWM_RULE_TMPLT_INPUT.csv, ORA_HWM_RULE_TMPLT_USAGE.csv, ORA_HWM_RULE_TMPLT_TRANSLATION.csv, ORA_HWM_RULE_TMPLT_INPUT_TRANSLATION.csv, and ORA_HWM_RULE_TMPLT_USAGE_TRANSLATION.csv | Reject the entire package before import | Rewrite every CSV as UTF-8 without BOM, then re-read the first three bytes and parse the exact first header of every included file | Before any Time Rule Templates CSV import is previewed or submitted | |
| Fresh schema and field states | A fresh export supplies exact object headers and metadata. Create rows come from normalized intent; update rows retain unchanged fields from one verified current template graph and an explicit change set. Explicit blank strings, `0`, and `#null` retain their literal value | Stop preparation | Reprepare against the fresh export contract and validate the archive; do not clone a source record for a create | When creating or updating a Time Rule Template from an exported baseline | read_template_schema_contract |
| FSM package structure | The ZIP contains ASM_SETUP_CSV_METADATA.xml unchanged from the fresh export, a nonempty ORA_HWM_RULE_TMPLT.csv, and only requested child CSV objects declared by that export; every included CSV has its exact exported headers and equal-width rows | Reject the package before preview or approval | Reprepare the minimal package with the current headers and metadata; reject extra files, duplicate or blank parent TemplateName values, and orphan child rows | Every create or update package | read_template_schema_contract |
| ORA_HWM_RULE_TMPLT CSV row | TemplateName, ViewInstanceName, GroupingKey, ProcessType, RunSummationLevel, RunTbbLevel, TemplateType, FormulaName, FormulaId, EffectiveStartDate, EffectiveEndDate | Reject the row | Supply all fields marked required by the attached parent template report | When preparing an ORA_HWM_RULE_TMPLT row | |
| ORA_HWM_RULE_TMPLT_INPUT CSV row | ORA_HWM_RULE_TMPLT.TemplateName, InputName, ViewInstanceName, GroupingKey, DisplaySequence, ValueSetCode, ValueSetId1 | Reject the row | Supply all fields marked required by the attached input template report | When preparing an ORA_HWM_RULE_TMPLT_INPUT row | |
| ORA_HWM_RULE_TMPLT_USAGE CSV row | ORA_HWM_RULE_TMPLT.TemplateName, OutputName, UserDefinedOutName, ViewInstanceName, GroupingKey, DisplaySequence, ValueSetCode, ValueSetId1, TmAtrbFldSetId | Reject the row | Supply all fields marked required by the attached usage template report | When preparing an ORA_HWM_RULE_TMPLT_USAGE row | |
| Translation CSV relationship | The exact parent TemplateName header plus the child InputName or OutputName header where applicable, and the translation attributes documented in ASM_SETUP_CSV_METADATA.xml | Reject an orphan or ambiguous translation row | Resolve the row to exactly one parent, input, or usage row using its alternate-key path | When an applicable translation CSV contains data rows | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The current target-environment Time Rule Templates export cannot be read completely | Lookup failure | Stop without selecting, proposing, or creating a template | find_compatible_time_rule_template |
| One or more fully compatible verified templates are found | Candidate disclosure required | Display every matching template and ask whether the user still wants a new template | find_compatible_time_rule_template |
| The user declines a new template after exact-match disclosure | Reuse ready | Reuse the selected exact match | find_compatible_time_rule_template |
| The user confirms a new template after exact-match disclosure | Create proposal required | Build the normalized requested configuration against the fresh schema; do not copy a source row | find_compatible_time_rule_template |
| Exactly one requested update target is found | Update proposal required | Display the current configuration and complete proposed change set, then prepare the FSM CSV package through core.data-loader | find_compatible_time_rule_template |
| More than one fully compatible or any partial-only candidate is found | User selection required | Display every candidate and material difference; do not select or create automatically | find_compatible_time_rule_template |
| No fully compatible template is found | Proposal required | Display the complete proposed template and its dependent Time Rule relationship, then wait for explicit approval | find_compatible_time_rule_template |
| A child input, usage, or translation row does not resolve to exactly one parent path | Invalid | Stop and correct the alternate key or grouping key | |
| Any CSV starts with hexadecimal bytes EF BB BF or its parsed first header differs from the file-specific expected header | Invalid package encoding | Stop before import; create a new BOM-free package and repeat full package validation | |
| Effective-date or formula compatibility cannot be established from authorized source data | Blocked | Stop preparation until the missing compatibility evidence is supplied | |
| A live create or update is requested without a validated immutable FSM CSV ZIP and core.data-loader preview | Import blocked | Route the package through core.data-loader validation and preview before requesting import approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| TemplateName is not used as the sole compatibility match | Compare the normalized parent, ordered inputs, ordered usages, formula, condition support, execution, summation, reporting, Time Category, result or payroll time-type, parameter, and context characteristics | During lookup | find_compatible_time_rule_template |
| Fully compatible semantics | Every applicable requested characteristic is supported without an undisclosed functional gap | During lookup | find_compatible_time_rule_template |
| Exact-match create authorization | Require explicit confirmation after every exact match is disclosed | Before package preparation | find_compatible_time_rule_template |
| Partial compatibility semantics | Any missing, conflicting, or unverified applicable characteristic prevents automatic reuse | During lookup | find_compatible_time_rule_template |
| DisplaySequence values are positive integers and unique within the parent input or usage scope | Reject invalid or duplicate ordering | For ordered child rows | |
| EffectiveStartDate and EffectiveEndDate use a source-supported date format | Reject invalid date values | For parent rows | |
| UTF-8 BOM exclusion | Read the first three bytes of every included CSV and reject EF BB BF; a visual header check alone does not pass | Every CSV package | |
| File-specific first-header identity | Parse the first header after the byte check and require the exact documented header for that file | Every CSV package | |
| CSV row width | Parse every included Time Rule Templates CSV with the same CSV parser used for package validation; require each data row to contain exactly the number of fields in that file's header, including trailing empty fields | Before any package is previewed, approved, or submitted | |
| Parent and child package linkage | Require each included child row's parent TemplateName to resolve to exactly one included parent; require nonblank ViewInstanceName and GroupingKey on parent and child rows | Before any package is previewed, approved, or submitted | |
| Schema-driven field preservation | Use the fresh export's exact headers and preserve every supplied literal value, including trailing blanks, `0`, and `#null`; do not add, remove, reorder, or infer fields | When generating a Time Rule Template package | read_template_schema_contract |
| Proposal completeness | The displayed proposal includes every required template detail and explains how the dependent Time Rule will use it | Before requesting approval | |
| Business-only summary completeness | Complete Summary contains every verified user-provided business value and Defaults Applied contains every default actually applied; both omit blank, null, unused, metadata-only, and technical package values | After package validation and before package linking or approval | |
| Approval freshness | Approval is valid only for the exact proposal fingerprint and target Fusion environment; any material change requires a new display and approval | Before import handoff | |
| Import-route enforcement | Treat Time Rule Template creation and updates as FSM setup-data CSV imports through core.data-loader; the absence of a direct REST create or update endpoint is not a validation failure | Every live create or update | |
| Created-template verification | A refreshed authoritative export must reproduce the approved parent, ordered inputs, and ordered usages before the template is released for Time Rule use | After an approved import | find_compatible_time_rule_template |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMETMPLT.VALIDATE_REQUIREMENTS | decision | 1 | validate_input | valid->TIMETMPLT.FIND_MATCH;invalid->TIMETMPLT.INPUT_ERROR | none | stop | Always |
