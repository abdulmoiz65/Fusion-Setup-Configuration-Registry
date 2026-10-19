# Manage HTML Email Templates Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Template identity | DesignName; MessageDesignCode for FSM import | Block before preview | Supply a unique display name and a matching unique message-design code for every imported template | Create or import | |
| Template definition | DesignTypeCode; DesignEditorTypeCode for FSM import | Block before preview | Select the intended documented template type and preserve compatible exported parent-row codes | Create or import | |
| Individual template create | Name; Template Type = Campaign user email template or Candidate notification email template; Campaign Purpose or Email Type; Template | Block before preview | Ask for all four UI fields. Name must be unique; Campaign user templates require Campaign Purpose, candidate notification templates require Email Type, and Template selects the complete matching design-metadata baseline. | Create one new template | |
| Existing-template handling | Replace existing templates; or import only new templates | Block before preview when a supplied cross-environment archive contains both target-existing and target-new MessageDesignCode values | Compare the supplied parent rows with a fresh target task-level FSM export. Show the complete Existing template names list and New template names list, then require one explicit handling choice. | Cross-environment FSM import | |
| Recruiting HTML email template listing | List all recruiting HTML email templates; List all HTML email templates; Show recruiting email templates | Block only when the target environment or task export route is not identified | Treat the business-language request as a full task-level FSM export; join parent, metadata, and type rows by MessageDesignCode | List all templates | |
| Import result request | Check the import result; Did the import work?; Were the templates created?; Show import errors | Block only when no unambiguous prior import request is available in the active task context | Use the most recent matching Manage HTML Email Templates import request; when it is unavailable or ambiguous, ask for the import request ID | Post-import result check | |
| Lifecycle or interactive design request | Activate; deactivate; edit the design in the designer; delete | Do not prepare an FSM import or automate the Fusion UI for the request | Explain that this FSM task has no documented status or delete operation; provide the manual Manage HTML Email Templates UI steps | Activate, deactivate, interactive design edit, or delete | |
| Dependent CSV payload | ORA_IRC_CAMP_EMAIL_TEMPL_MSG_DESIGN_METADATA.csv; ORA_IRC_CAMP_EMAIL_TEMPL_MSG_DESIGN_TYPES.csv | Block before preview only when the required baseline is unavailable or supplied dependent files are invalid | When the user does not provide dependent CSV files, generate both files from the documented baseline and parent DesignName/MessageDesignCode | FSM import | |
| FSM package members | ASM_SETUP_CSV_METADATA.xml; parent design CSV; generated or supplied metadata CSV; generated or supplied type-association CSV | Reject archive only when the manifest or parent design CSV is absent, or supplied dependent files are invalid | Materialize the complete dependent CSV payload, then validate the final archive | FSM import | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Dependent CSV files are not provided | Generate the complete metadata and type-association CSV payload from the documented baseline | Set each generated parent reference to the exact parent MessageDesignCode and set TypeCode from the selected Campaign Purpose or Email Type mapping; preserve the baseline metadata values | |
| Dependent CSV files are provided | Require every metadata and type-association row to reference an included parent MessageDesignCode | Preserve the full supplied package for Replace existing; for import only new templates, retain every selected parent row and its matching related rows | |
| The archive has both existing and new templates in the target | Block preview until the user selects Replace existing templates or Import only new templates | For Replace existing, retain all supplied rows; for Import only new templates, remove each existing parent and all matching metadata and type-association rows | |
| Archive changed after preview | Approval is stale | Recalculate SHA-256, preview again, and obtain fresh approval | |
| A plain-language import-result request is received | Valid when one matching prior import request is available | Retrieve that request's current status, counts, and diagnostics through core.data-loader; do not require a request ID from the user unless the prior request is absent or ambiguous | |
| An individual template create is requested | Valid only when Name, Template Type, the applicable Campaign Purpose or Email Type, and Template are all supplied | Generate the FSM parent and dependent rows from the selected UI values and matching complete template baseline | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Display name | Reject blank name and require a unique intended template name | Create or import | |
| Individual create fields | Reject a request missing Name, Template Type, the applicable Campaign Purpose or Email Type, or Template; do not ask the user for MessageDesignCode, DesignTypeCode, DesignEditorTypeCode, or raw DesignMetadata | Create one new template | |
| Template Type | Accept only Campaign user email template or Candidate notification email template; reject any other value | Create one new template | |
| Campaign Purpose or Email Type | Accept only a Campaign Purpose or Email Type mapped to the selected Template Type in ora_defaulting_rules.md; for Candidate notification email template accept Global Template, CE Notification Template, Internal Template, or AdHoc Template | Create one new template | |
| Message design code | Reject blank code and reject mismatched parent, metadata, or type-association references | FSM import | |
| Template type and editor | Preserve exported parent-row codes exactly; do not invent, fill, or alter values from an FSM export | FSM import | |
| Generated metadata CSV | When dependent CSV files are absent, generate the complete metadata row from the prior full-metadata import baseline and replace only its parent code | FSM import | |
| Subject | Treat as optional metadata; do not require, derive, or validate it for FSM import | FSM import | |
| Generated type CSV | When dependent CSV files are absent, generate the type-association row with the parent code and the TypeCode mapped to the selected Campaign Purpose or Email Type | FSM import | |
| Supplied dependent CSV data | Reject supplied reduced, hand-built placeholder, incompatible, or mismatched dependent data | FSM import | |
| Import scope | Require every retained metadata and type-association row to match a retained parent MessageDesignCode; preserve all related rows for each selected parent | Cross-environment FSM import | |
| Listing output | Return one row per MessageDesignCode with Name, Template Type, and the mapped Campaign Purpose or Email Type; do not show Template, Subject, Language, codes, or raw metadata | List all recruiting HTML email templates | |
| Import-result output | Return Succeeded, In progress, or Failed; total, loaded, and failed counts; and every actionable ProcessLog diagnostic when available | Check the import result; Did the import work?; Were the templates created?; Show import errors | |
| Lifecycle status or delete import | Reject; no status or delete field is documented in the task CSV package | Activate, deactivate, or delete | |
| Template Type presentation | Render ORA_CAMP_TEMPLATE_USER as Campaign user email template and ORA_HTML_TEMPLATE_USER as Candidate notification email template | List all recruiting HTML email templates | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HET.VALIDATE_INPUT | step | 10 | validate_input | valid->HET.CHECK_DEPENDENCIES;invalid->HET.HANDLE_ERROR | none | stop | Before task-level FSM export or FSM import preview |
