# Receiving Document Output Preferences Reference Lookups

Sources: provided Redwood document-output-preferences flow and read-only OpenAPI metadata from the configured Fusion target.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_job_set | Job set is supplied | Job set display name or code; ProductCode=RCV | /fscmRestApi/resources/11.13.18.05/shippingDocumentJobSetsLOV | JobSetDisplayName, JobSetName, JobSetPackageName, ProductCode | Match one RCV record by supplied display name or code | JobSetName, JobSetPackageName | Stop and request one receiving job set |
| resolve_job | Job is supplied | Job display name or code; ProductCode=RCV and resolved job-set context | /fscmRestApi/resources/11.13.18.05/shippingJobDefinitionsLOV | JobDisplayName, JobName, JobPackage, Description, ReportXDOPath, ProductCode | Match one RCV record by supplied display name or code in resolved context | JobName, JobPackageName, JobDescription, ReportXDOPath | Stop and request one receiving job |
| resolve_job_layout | Layout is supplied | Layout name and resolved job context | /fscmRestApi/resources/11.13.18.05/shippingReportLayoutsLOV | LayoutName, ReportTemplateId, ReportXDOPath | Match one layout in the resolved job context | JobLayout and ReportTemplateId context | Stop and request one layout for the resolved job |
| resolve_job_format | Format is supplied | Format label or name and resolved layout plus ReportXDOPath context | /fscmRestApi/resources/11.13.18.05/shippingReportFormatsLOV | Name, Label, ReportFormat, ReportTemplateId | Match one format in the resolved layout context | JobFormat | Stop and request one format for the resolved layout |
| resolve_organization | Organization is supplied | Organization name or ID | /fscmRestApi/resources/11.13.18.05/inventoryOrganizationsLOV | OrganizationId, OrganizationName | Match one secured organization by supplied name or ID | OrganizationId, OrganizationCode context | Stop and request one accessible organization |
| resolve_subinventory | Subinventory is supplied | Subinventory name or code and resolved OrganizationId | /fscmRestApi/resources/11.13.18.05/activeSubinventories | SubinventoryCode, SubinventoryName, OrganizationId | Match one active subinventory in the resolved organization | SubinventoryCode | Stop and request one active subinventory for the organization |
| resolve_user | User is supplied | User name or person identifier | /hcmRestApi/resources/11.13.18.05/workersLov | PersonId, UserName, display attributes | Match one worker by supplied user name or identifier | UserId from PersonId | Stop and request one user |
| resolve_role | Role is supplied | Role name or ID | /hcmRestApi/resources/11.13.18.05/rolesLOV | RoleId, RoleName, ActiveFlag, JobRole | Match one active job role by supplied name or ID | RoleId | Stop and request one active job role |
| resolve_printer | Printer is supplied | PrinterName | /fscmRestApi/resources/11.13.18.05/printersLOV | PrinterName | Match one printer name exactly | PrinterName | Stop and request one printer |
| resolve_email_server | Email server is supplied | EmailServerName | /fscmRestApi/resources/11.13.18.05/shippingBIPEmailServersLOV | EmailServerName | Match one email-server name exactly | EmailServerName | Stop and request one email server |
| resolve_print_orientation | Print orientation is supplied | Meaning or LookupCode; LookupType=ORA_WSH_DOC_ORIENTATION | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV | Meaning, LookupCode, LookupType | Match one value within the declared lookup type | PrintOrientationCode | Stop and request one valid orientation |
| resolve_print_side | Print side is supplied | Meaning or LookupCode; LookupType=ORA_WSH_DOC_PRINT_SIDE_TYPE | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV | Meaning, LookupCode, LookupType | Match one value within the declared lookup type | PrintSideCode | Stop and request one valid print side |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A dependent LOV value is supplied | Resolve its parent context first and rerun the child resolver if that context changes. |
| A resolver returns no or multiple records | Stop; do not guess, fuzzy-match, or select the first returned record. |
| A directly supplied code and display value disagree | Stop and require a pair that resolves to the same record. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| RCDOP.RESOLVE_LOVS | decision | 20 | reference_lookup | resolved->RCDOP.DATA_LOADER_GATE;unresolved->RCDOP.RETURN_ISSUES | RCDOP.VALIDATE_INPUT | stop | A supplied field has a resolver in this file | resolve_job_set |
