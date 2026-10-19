# Reference Lookups

Source: Oracle SCM business-object reference for Financial Orchestration System Options and developer-provided configured business-object details.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_system_options_record | Before preparing a System Options change | None | fscmRestApi/resources/latest/financialOrchestrationSystemOptions | SystemOptionId | Use GET and require zero or one Financial Orchestration System Options record | SystemOptionId | Zero records: select create in the separately approved workflow. One record: select update in the separately approved workflow. More than one record: stop and investigate. |
| resolve_validation_organization | Item Validation Organization is supplied | OrganizationName | fscmRestApi/resources/latest/financialOrchestrationItemOrganizationsLOV?q=OrganizationName='{OrganizationName}'&fields=OrganizationId,OrganizationName,OrganizationCode | OrganizationName; OrganizationCode; OrganizationId | Return exactly one record whose OrganizationName equals the user-provided organization name | validationOrganizationId: OrganizationId; validationOrganizationName: OrganizationName; validationOrganizationCode: OrganizationCode | Stop and ask for a valid, exact organization name when no record matches; stop and ask for a more specific value when multiple records match. |
| resolve_service_item | Configure service items for global purchase processing is true | validationOrganizationId; selected Service Item | fscmRestApi/resources/latest/financialOrchestrationServiceItemsLOV?onlyData=true&q=OrganizationId={validationOrganizationId}&fields=Description,InventoryItemId,ItemNumber,OrganizationCode,OrganizationId&limit=25&offset=0 | Description; InventoryItemId; ItemNumber; OrganizationCode; OrganizationId | Filter by the resolved OrganizationId, then require the user to select exactly one returned Service Item | serviceItemId: InventoryItemId; serviceItemNumber: ItemNumber; serviceItemOrganizationId: OrganizationId | Stop when no items are returned for the organization or the user has not selected exactly one returned item. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup request path or match rule is not source-backed | Stop before lookup execution; do not infer a Fusion REST endpoint or matching behavior. |
| A documented lookup resolves no or multiple records | Stop and request a precise reference value. |
| The configured business-object description is known to be inaccurate | Use financialOrchestrationSystemOptions and ORA_FOS_SYSTEM_OPTION as the configured identity; do not use the description to select the business object. |
| A System Options change is required after the GET check | Route the create or update through the separately approved `core.data-loader` workflow. |
| A live request is prepared | Use the configured Fusion REST base URL and the documented `resources/latest` path; do not substitute a pod or legacy `rest/rv` path. |
| An update is prepared | Re-read the exact resolved SystemOptionId immediately before preparing the Data Loader update row and retain its current version. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.SO.RESOLVE_RECORD | step | 25 | reference_lookup | existing->FOS.SO.DONE;missing->FOS.SO.DONE;multiple->FOS.SO.HANDLE_ISSUE;lookup_failed->FOS.SO.HANDLE_ISSUE | FOS.SO.CHECK_DEPENDENCIES | stop | Before preparing a System Options create or update |
