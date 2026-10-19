# Manage Email Templates Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Template identity | DesignName | Block preview | Supply a nonblank, unique visible template name | A template is created or imported | |
| Parent and dependent identity | Generated MessageDesignCode and matching DesignMetadata parent reference | Block preview | Generate a unique code using `ora_defaulting_rules.md`, then rebuild the linked parent and metadata rows so every metadata row resolves to one included parent | FSM import preview | |
| Template type and editor | DesignTypeCode and DesignEditorTypeCode | Block preview | Use the matching hardcoded Campaign mapping from `ora_defaulting_rules.md` | Standard Campaign template creation | |
| Design metadata | Complete DesignMetadata value from the selected editor default | Block preview | Use the matching hardcoded Campaign default; do not derive it from another editor or type | Standard Campaign template creation | |
| Archive integrity | Parent CSV, metadata CSV, types CSV, and ASM_SETUP_CSV_METADATA.xml | Reject the archive before preview | Retain all required archive members and linked rows | FSM import preview | |
| Status transition | One or more exact existing Campaign templates, each current status, and each new status | Block preview | Start with a fresh task export and change only each selected parent's DesignStatusCode to ORA_ACTIVE or ORA_INACTIVE | Existing Campaign template activation or inactivation | |
| Cross-environment archive | Unmodified task-level FSM ZIP from the source environment | Block preview | Preserve the archive members and values exactly; validate the parent/dependent links and selected editor metadata before target import | Import from another Fusion environment | |
| General document input | Any requester-supplied document format | Do not treat it as import-ready | Analyze only source-backed template facts and identify missing required FSM members or mappings | Analysis or import preparation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Campaign Communication Template is selected | Verify | Confirm DesignTypeCode is ORA_EMP_CAMP_TEMPLATE_USER and use the selected editor's hardcoded mapping | |
| Express Communication Template is selected | Blocked | Obtain a representative Express template export before mapping its DesignTypeCode or editor-specific DesignMetadata | |
| Basic Editor or Advanced Block Editor is selected for Campaign | Verify | Use the complete hardcoded minimal layout JSON only when the selected editor and template type match | |
| HTML Editor is selected for Campaign | Verify | Use blank `DesignMetadata` with `MessageLanguage` `US` and `DefaultLanguageFlag` `Y`; do not substitute Basic, Advanced, or target-template metadata | |
| Any metadata row lacks an included MessageDesignCode parent | Blocked | Rebuild the linked CSV rows before preview | |
| Existing Campaign template statuses are changed | Verify | Require one exact current-export row per selected template; retain all CSV rows and members except selected rows' DesignStatusCode values | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DesignName | Require a nonblank, unique visible template name | A template is created or imported | |
| MessageDesignCode | Generate a nonblank key of at most 32 characters from the declared name/timestamp/nonce rule; require every related metadata row to match it and reject a target-export conflict | Standard Campaign template creation and FSM import | |
| DesignTypeCode | For Campaign Communication Template, require the hardcoded value ORA_EMP_CAMP_TEMPLATE_USER. Express templates are unsupported by this FSM route; do not infer their value | Standard Campaign template creation | |
| DesignEditorTypeCode | Require the hardcoded mapping ORA_BASIC, ORA_ADVANCED, or ORA_HTML that matches the selected UI editor | Standard Campaign template creation | |
| DesignMetadata | Require the hardcoded selected-editor value in `ora_defaulting_rules.md`. Do not substitute Basic or Advanced metadata for HTML, or Campaign metadata for Express | Standard Campaign template creation | |
| MessageLanguage and DefaultLanguageFlag | Require US and Y for Basic or Advanced; require US and Y for HTML | Standard Campaign template creation | |
| DesignStatusCode | For controlled status transitions, require exactly one target parent row per selected template from a fresh target export; allow only ORA_ACTIVE or ORA_INACTIVE and reject any other changed field, CSV row, or archive member | Existing Campaign template activation or inactivation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMET.VALIDATE_INPUT | decision | 10 | validate_input | valid->HCMET.CHECK_DEPENDENCIES;invalid->HCMET.RETURN_ISSUES | none | stop | Before task-level FSM export or FSM import preview |
