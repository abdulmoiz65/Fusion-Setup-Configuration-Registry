# Manage Predefined Links Input Validation

Sources: Confluence page 21736675148, Manage Predefined Links — ORA_IRC_EMP_CAMP_DEEP_LINKS; user-requested FSM export-and-inspect query route.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Export query scope | Requested status filter Active | Stop before export planning | Supply the requested status filter | Current predefined links are queried | |
| Export context | Target Fusion environment and project workspace | Stop before export | Supply the environment and project context required by the routed export skill | Current predefined links are queried | |
| Predefined link name | Name | Stop before create preview | Supply a name | A predefined link is created | |
| Deep link selection | Deep Link Name; ObjectType; Action | Stop before create preview | Supply the explicit deep-link name, ObjectType, and Action | A predefined link is created | |
| Draft-link activation | Operation Activate; DisplayName; ObjectType; Action | Stop before immutable archive preparation | Supply one exact exported Draft row | A predefined link is activated | |
| Draft-link rename | Operation Rename; DisplayName; ObjectType; Action; New DisplayName | Stop before immutable archive preparation | Supply one exact exported Draft row and a nonblank replacement name | A predefined link name is changed | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Requested filter is Active and export context is present | Ready | Continue to FSM export readiness | |
| Requested status filter is missing | Blocked | Supply the status filter to count | |
| Target environment or project workspace is missing | Blocked | Supply the export context | |
| Name is blank during creation | Blocked | Show Enter a value. and require Name | |
| Deep Link is blank during creation | Blocked | Show Select a value. and require Deep Link | |
| Activation target resolves to exactly one exported ORA_DRAFT row | Ready | Continue to mutation baseline validation | |
| Rename target resolves to exactly one exported ORA_DRAFT row and New DisplayName is nonblank | Ready | Continue to mutation baseline validation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name required | The live UI displays Enter a value. when Name is blank | Create is submitted with Name blank | |
| Deep Link required | The live UI displays Select a value. when Deep Link is blank | Create is submitted with Deep Link blank | |
| Query status filter | Accept Active for the requested active-link count | FSM export query is planned | |
| Exported status column | Inspect the downloaded task CSV headers and values before counting; do not assume an undocumented export column name or code | FSM export result is available | |
| Activation fields | Current export identifies the record with DisplayName, ObjectType, Action, and StatusCode; the activation update changes StatusCode from ORA_DRAFT to ORA_ACTIVE | An exact Draft link is activated through FSM import | |
| Rename fields | Current export identifies the record with DisplayName, ObjectType, Action, and StatusCode; the rename update changes DisplayName only | An exact Draft link is renamed through FSM import | |
| Creation fields | Use Link Name as DisplayName; use supplied ObjectType and Action; set StatusCode to ORA_DRAFT | A link is created through FSM import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.VALIDATE_REQUEST | decision | 1 | validate_input | query->MPL.CHECK_REQUEST_READINESS;mutation->MPL.CHECK_MUTATION_BASELINE;invalid->MPL.HANDLE_ERROR | none | stop | A current active-link count, Draft-link activation, or Draft-link rename is requested |
| MPL.EVALUATE_EXPORT_RESULT | decision | 6 | evaluate_result | verified->MPL.RETURN_SUCCESS;issues->MPL.HANDLE_ERROR | MPL.EXPORT_GATE | stop | A downloaded Manage Predefined Links FSM export is inspected |
| MPL.EVALUATE_MUTATION_RESULT | decision | 11 | evaluate_result | verified->MPL.RETURN_MUTATION_SUCCESS;issues->MPL.HANDLE_ERROR | MPL.MUTATION_GATE | stop | A submitted FSM activation or rename import is verified |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
| Name precision, character rules, and duplicate behavior | HCM Communicate implementation owner | Limits create-form prevalidation only | Provide source-backed attribute and validation details |
| Deep Link submitted attribute and type | HCM Communicate implementation owner | Limits deterministic UI-to-service mapping only | Provide JSF, PageDef, backing-bean, or supported contract evidence |
| Exported business-object, CSV header, and Active status representation | Task export owner | The first export must be inspected before a fixed field mapping is authored | Preserve the archive metadata and CSV header/value evidence, then update this rule |
