# Inventory Document Output Preferences Input Validation

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Normalize supplied LOV display values or backend values through the declared exact-match resolvers; normalize active dates to YYYY-MM-DD. |
| Backend-owned validation | Data Loader and Fusion own keys, uniqueness, required system fields, server-side domains, and unsupported combinations. |
| Execution | Data Loader owns preview, approval, and execution. This task resource never performs a direct REST write. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Job set identity | JobSetName or JobSetDisplayName | Block preparation | Resolve exactly one job set and fill JobSetName and JobSetPackageName | Creating a header | resolve_document_job_set |
| Active date | StartDateActive | Let Data Loader report its required-field validation | Supply a calendar date as YYYY-MM-DD | Creating a header | |
| Organization before subinventory | OrganizationId or OrganizationCode or OrganizationName | Block the subinventory lookup only | Resolve exactly one organization before resolving SubinventoryCode | A line supplies SubinventoryCode or SubinventoryName | resolve_inventory_organization |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A display value and a backend value are both supplied for one LOV | Continue only when both identify the same single row | Fill canonical backend values from that row; otherwise stop | |
| Job set is selected | Fill JobSetName, JobSetPackageName, and JobSetDescription from the matched row | Resolve the job only after the job-set values are available | resolve_document_job_set |
| Job is selected | Fill JobName, JobPackageName, JobDescription, and ReportXDOPath from the matched row | Resolve layout and format only with the returned context | resolve_document_job |
| Subinventory is selected | Continue only with a resolved organization | Fill SubinventoryCode from the matching organization-scoped row | resolve_active_subinventory |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Date format | Accept only YYYY-MM-DD for StartDateActive and EndDateActive; preserve a blank EndDateActive | A date is supplied | |
| Attach Document flag | Accept true or false and send Boolean true or false; when blank, apply the documented false default | AttachShippingDocumentFlag is supplied or blank | |
| Job set normalization | Accept JobSetName or JobSetDisplayName and fill the backend JobSetName, JobSetPackageName, and derived description | A job set is supplied | resolve_document_job_set |
| Job normalization | Accept JobName or JobDisplayName and fill JobName, JobPackageName, ReportXDOPath, and derived description | A job is supplied | resolve_document_job |
| Layout normalization | Accept LayoutName and send JobLayout only after ReportXDOPath is resolved | A layout is supplied | resolve_report_layout |
| Format normalization | Accept Label, Name, or ReportFormat and send JobFormat only after JobLayout and ReportXDOPath are resolved | A format is supplied | resolve_report_format |
| Organization normalization | Accept OrganizationId, OrganizationCode, or OrganizationName and send OrganizationId | A line organization is supplied | resolve_inventory_organization |
| Subinventory normalization | Accept SubinventoryCode or SubinventoryName and send SubinventoryCode within the resolved organization | A line subinventory is supplied | resolve_active_subinventory |
| User normalization | Accept PersonId, PersonNumber, Username, or DisplayName and send UserId as PersonId | A line user is supplied | resolve_worker |
| Role normalization | Accept RoleId, RoleCode, or RoleName and send RoleId | A line role is supplied | resolve_job_role |
| Printer normalization | Accept the exact PrinterName and preserve its canonical returned value | A line printer is supplied | resolve_printer |
| Email server normalization | Accept the exact EmailServerName and preserve its canonical returned value | A line email server is supplied | resolve_email_server |
| Print orientation normalization | Accept LookupCode or Meaning and send PrintOrientationCode from the matching standard lookup row | A line orientation is supplied | resolve_print_orientation |
| Print side normalization | Accept LookupCode or Meaning and send PrintSideCode from the matching standard lookup row | A line side is supplied | resolve_print_side |
| Text and number fields | Preserve supplied PrintNumberOfCopies, PrintPages, EmailFrom, EmailReplyTo, EmailTo, EmailCC, EmailBCC, EmailSubject, and EmailMessage for Data Loader and Fusion validation | A line value is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IDOP.VALIDATE_INPUT | step | 10 | validate_input | valid->IDOP.RESOLVE_LOOKUPS;invalid->IDOP.HANDLE_ERROR | none | stop | Before Data Loader preparation |
