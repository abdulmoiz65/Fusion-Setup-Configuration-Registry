# Label Output Preferences Input Validation

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Label route | Apply these rules only when ProductCode is LABEL. The Redwood page does not offer header creation for this route. |
| Local validation ownership | Preserve source values for the documented Label line fields. No user-friendly alias, default, or client-side conversion is evidenced. |
| Backend-owned validation | Data Loader and Fusion own required fields, record identity, server-side domains, and business-rule validation. |
| Execution | Core Data Loader owns preparation, preview, approval, and execution. This task resource does not perform a direct REST write. |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Label header identity | Accept JobSetName or LabelType as the UI-friendly JobSetDisplayName. Resolve a supplied job-set name or display value to exactly one LABEL header; when both are supplied, require them to identify the same header. Fill HeaderId and JobSetName. | Creating or updating Label preference lines | resolve_label_output_header |
| Organization normalization | Accept OrganizationId or OrganizationName. Resolve a supplied ID or display name to exactly one secured OrganizationId. | A line supplies an organization | resolve_inventory_organization |
| User normalization | Accept UserId or UserName as the UI-friendly DisplayName. Resolve either to one active worker and fill UserId. Reject a line that also supplies a job role. | A line supplies a user | resolve_user |
| Job role normalization | Accept RoleId or RoleName. Resolve either to one active job role and fill RoleId. Reject a line that also supplies a user. | A line supplies a job role | resolve_job_role |
| Printer normalization | Accept PrinterName only. Validate the supplied printer through the PrinterName LOV before Data Loader handoff. | A line supplies a printer | resolve_printer |
| Print orientation normalization | Accept PrintOrientationCode or PrintOrientation as the UI-friendly Meaning. Resolve either to one LookupCode; when both are supplied, require them to identify the same row. Fill PrintOrientationCode. | A line supplies print orientation | resolve_print_orientation |
| Print side normalization | Accept PrintSideCode or PrintSide as the UI-friendly Meaning. Resolve either to one LookupCode; when both are supplied, require them to identify the same row. Fill PrintSideCode. | A line supplies print side | resolve_print_side |
| Email server normalization | Accept EmailServerName only. Validate the supplied value through the Email Server LOV before Data Loader handoff. | A line supplies an email server | resolve_email_server |
| Text and numeric field routing | Preserve PrintNumberOfCopies, EmailFrom, EmailTo, EmailCC, EmailBCC, EmailSubject, EmailMessage, EmailReplyTo, FaxServer, FaxNumber, PrintPages, and PrintTray as supplied. Fusion and Data Loader own their final validation. | A Label preference line is prepared | |
| Number of labels | Preserve PrintNumberOfCopies as a numeric value; Data Loader and Fusion validate its permitted range. | PrintNumberOfCopies is supplied | |
| Conditional subinventory | For LABEL, accept SubinventoryCode unless JobSetName is LpnContentLabelJobSet or LpnLabelJobSet. When the field applies, resolve OrganizationId first. Accept SubinventoryCode or SubinventoryName only through the declared exact-match resolver. | SubinventoryCode or SubinventoryName is supplied | resolve_active_subinventory |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOP.VALIDATE_INPUT | step | 10 | validate_input | valid->LOP.RESOLVE_LOOKUPS;invalid->LOP.HANDLE_ERROR | none | stop | Before Data Loader preparation for a Label preference line |
